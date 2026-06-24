import os
import asyncio
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from sentence_transformers import CrossEncoder
from rank_bm25 import BM25Okapi

from backend.dbops.pgvectore_store import cursor
from backend.embeddings.embedder import generate_embedding

_executor = ThreadPoolExecutor(max_workers=2)

# =====================================================
# CROSS ENCODER — load once
# =====================================================

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# =====================================================
# BM25 INDEX — build once at startup, not per request
# =====================================================

_bm25_index = None
_bm25_rows  = []

def _build_bm25_index():
    global _bm25_index, _bm25_rows
    print("Building BM25 index...")
    cursor.execute("""
        SELECT
            dc.chunk_id, dc.chunk_text,
            d.title, d.source_url, d.domain,
            d.category, d.agent_role, d.agent_type
        FROM document_chunks dc
        JOIN documents d ON dc.document_id = d.document_id
    """)
    _bm25_rows = cursor.fetchall()
    corpus = [row[1].lower().split() for row in _bm25_rows]
    _bm25_index = BM25Okapi(corpus)
    print(f"BM25 index built over {len(_bm25_rows)} chunks")

# Call this ONCE when your app starts
_build_bm25_index()

# =====================================================
# VECTOR SEARCH
# =====================================================

def vector_search(query, limit=20):
    query_embedding = generate_embedding(query)
    if query_embedding is None:
        return []

    query_vector = "[" + ",".join(str(float(x)) for x in query_embedding) + "]"

    cursor.execute("""
        SELECT
            dc.chunk_id, dc.chunk_text,
            d.title, d.source_url, d.domain,
            d.category, d.agent_role, d.agent_type,
            dc.embedding <=> %s::vector AS distance
        FROM document_chunks dc
        JOIN documents d ON dc.document_id = d.document_id
        ORDER BY distance
        LIMIT %s
    """, (query_vector, limit))

    results = []
    for row in cursor.fetchall():
        distance   = float(row[8])
        similarity = round(1 - distance, 4)
        results.append({
            "chunk_id": row[0], "chunk_text": row[1],
            "title": row[2],    "source_url": row[3],
            "domain": row[4],   "category": row[5],
            "agent_role": row[6], "agent_type": row[7],
            "distance": distance, "similarity": similarity,
        })
    return results

# =====================================================
# BM25 SEARCH — uses pre-built index, fast
# =====================================================

def bm25_search(query, limit=20):
    if _bm25_index is None:
        return []

    scores     = _bm25_index.get_scores(query.lower().split())
    top_idx    = np.argsort(scores)[::-1][:limit]

    results = []
    for idx in top_idx:
        if scores[idx] == 0:
            continue                          # skip zero-score matches
        row = _bm25_rows[idx]
        results.append({
            "chunk_id": row[0], "chunk_text": row[1],
            "title": row[2],    "source_url": row[3],
            "domain": row[4],   "category": row[5],
            "agent_role": row[6], "agent_type": row[7],
            "distance": 0.0,
            "similarity": round(float(scores[idx]), 4),
            "bm25_score": round(float(scores[idx]), 4),
        })
    return results

# =====================================================
# RECIPROCAL RANK FUSION
# =====================================================

def reciprocal_rank_fusion(result_lists, k=60):
    scores    = {}
    doc_store = {}
    for result_list in result_lists:
        for rank, doc in enumerate(result_list):
            cid = doc["chunk_id"]
            scores[cid]    = scores.get(cid, 0) + 1 / (k + rank + 1)
            doc_store[cid] = doc
    merged = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    fused  = []
    for chunk_id, rrf_score in merged:
        doc = doc_store[chunk_id]
        doc["rrf_score"] = round(rrf_score, 6)
        fused.append(doc)
    return fused

# =====================================================
# CROSS ENCODER — run in thread pool to avoid blocking
# =====================================================

def _rerank_sync(query, candidates):
    """Runs in executor thread — safe to block here."""
    pairs  = [(query, item["chunk_text"]) for item in candidates]
    scores = reranker.predict(pairs)
    for item, score in zip(candidates, scores):
        item["rerank_score"] = float(score)
        rrf = item.get("rrf_score", 0)
        item["final_score"]  = float(score) * 0.70 + rrf * 100 * 0.30
    candidates.sort(key=lambda x: x["final_score"], reverse=True)
    return candidates

async def rerank_results_async(query, candidates):
    if not candidates:
        return []
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, _rerank_sync, query, candidates)

def rerank_results(query, candidates):
    """Sync wrapper — use this if your stack is not async."""
    if not candidates:
        return []
    return _rerank_sync(query, candidates)

# =====================================================
# HYBRID SEARCH
# =====================================================

def hybrid_search(query, limit=20):
    vector_results = vector_search(query, limit=limit)
    bm25_results   = bm25_search(query,   limit=limit)
    return reciprocal_rank_fusion([vector_results, bm25_results])

# =====================================================
# RETRIEVAL FUNCTIONS
# =====================================================

def retrieve_context(query, top_k=5):
    candidates = hybrid_search(query)
    reranked   = rerank_results(query, candidates)
    return reranked[:top_k]

def retrieve_api_context(query, top_k=5):
    candidates = [
        c for c in hybrid_search(query)
        if c.get("agent_type") == "api" or "api" in c.get("category", "").lower()
    ]
    return rerank_results(query, candidates)[:top_k]

def retrieve_code_context(query, top_k=5):
    candidates = [
        c for c in hybrid_search(query)
        if c.get("agent_type") == "code" or c.get("agent_role") == "code_agent"
    ]
    return rerank_results(query, candidates)[:top_k]

def retrieve_runbook_context(query, top_k=5):
    candidates = [
        c for c in hybrid_search(query)
        if c.get("agent_type") == "runbook"
    ]
    return rerank_results(query, candidates)[:top_k]

# =====================================================
# CACHE REFRESH — call if documents change
# =====================================================

def refresh_bm25_index():
    _build_bm25_index()