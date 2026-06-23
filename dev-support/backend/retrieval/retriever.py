from sentence_transformers import CrossEncoder

from backend.embeddings.embedder import generate_embedding
from backend.dbops.pgvectore_store import cursor


# =====================================================
# RERANKER
# =====================================================

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# =====================================================
# AUTOMATIC DOMAIN DETECTION
# =====================================================

def detect_domain(query):

    query = query.lower()

    cursor.execute(
        """
        SELECT
            domain,
            COUNT(*) AS docs
        FROM documents
        WHERE domain IS NOT NULL
        GROUP BY domain
        """
    )

    rows = cursor.fetchall()

    for domain, count in rows:

        if (
            domain
            and count >= 20
            and domain.lower() in query
        ):
            return domain

    return None

# =====================================================
# KEYWORD SEARCH
# =====================================================

def keyword_search(
    query,
    limit=20
):

    cursor.execute(
        """
        SELECT

            dc.chunk_id,
            dc.chunk_text,

            d.title,
            d.source_url,
            d.domain,
            d.category,
            d.agent_role,

            0.0 AS distance

        FROM document_chunks dc

        JOIN documents d
        ON dc.document_id = d.document_id

        WHERE

            LOWER(d.title)
            LIKE LOWER(%s)

            OR

            LOWER(dc.chunk_text)
            LIKE LOWER(%s)

        LIMIT %s
        """,
        (
            f"%{query}%",
            f"%{query}%",
            limit
        )
    )

    rows = cursor.fetchall()

    results = []

    for row in rows:

        results.append({

            "chunk_id": row[0],

            "chunk_text": row[1],

            "title": row[2],

            "source_url": row[3],

            "domain": row[4],

            "category": row[5],

            "agent_role": row[6],

            "distance": 1.0,

            "similarity": 0.0
        })

    return results


# =====================================================
# VECTOR SEARCH
# =====================================================
def vector_search(
    query,
    limit=200
):
    cursor.execute(
        """
        SELECT
            dc.chunk_id,
            dc.embedding <=> (
                SELECT embedding
                FROM document_chunks
                LIMIT 1
            ) AS distance
        FROM document_chunks dc
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    print("\nPGVECTOR TEST")
    print(rows)

    query_embedding = generate_embedding(
        query
    )

    query_vector = (
        "["
        +
        ",".join(
            str(float(x))
            for x in query_embedding
        )
        +
        "]"
    )

    domain = detect_domain(
        query
    )

    use_domain_filter = False

    if domain:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM documents
            WHERE domain = %s
            """,
            (domain,)
        )

        result = cursor.fetchone()

        count = result[0] if result else 0

        if count >= 20:
            use_domain_filter = True

   

   

    # =====================================
    # YOUR VECTOR QUERY STARTS HERE
    # =====================================

    if use_domain_filter:

        cursor.execute(
            """
            SELECT

                dc.chunk_id,
                dc.chunk_text,

                d.title,
                d.source_url,
                d.domain,
                d.category,
                d.agent_role,

                dc.embedding <=> %s::vector
                AS distance

            FROM document_chunks dc

            JOIN documents d
            ON dc.document_id = d.document_id

            WHERE d.domain = %s

            ORDER BY distance

            LIMIT %s
            """,
            (
                query_vector,
                domain,
                limit
            )
        )

    

    else:

        cursor.execute(
            """
            SELECT

                dc.chunk_id,
                dc.chunk_text,

                d.title,
                d.source_url,
                d.domain,
                d.category,
                d.agent_role,

                dc.embedding <=> %s::vector
                AS distance

            FROM document_chunks dc

            JOIN documents d
            ON dc.document_id = d.document_id

            ORDER BY distance

            LIMIT %s
            """,
            (
                query_vector,
                limit
            )
        )

    rows = cursor.fetchall()

    print(
        f"Rows Returned: {len(rows)}"
    )

    results = []

    for row in rows:

        distance = float(
            row[7]
        )

        results.append({

            "chunk_id": row[0],

            "chunk_text": row[1],

            "title": row[2],

            "source_url": row[3],

            "domain": row[4],

            "category": row[5],

            "agent_role": row[6],

            "distance": distance,

            "similarity": round(
                1 - distance,
                4
            )
        })

    print(
        f"Vector Results: {len(results)}"
    )

    return results
# def vector_search(
#     query,
#     limit=50
# ):
  
#     query_embedding = generate_embedding(
#         query
#     )
#     print(type(query_embedding))
#     print(len(query_embedding))
#     print(query_embedding[:5])

#     domain = detect_domain(
#         query
#     )

#     use_domain_filter = False

#     if domain:
#         print(f"Detected before query Domain: {domain}")
#         print(f"Use Domain before query Filter: {use_domain_filter}")
#         cursor.execute(
#             """
#             SELECT COUNT(*)
#             FROM documents
#             WHERE domain = %s
#             """,
#             (domain,)
#         )

#         result = cursor.fetchone()

#         count = (
#             result[0]
#             if result
#             else 0
#         )

#         if count >= 20:

#             use_domain_filter = True

#     if use_domain_filter:

#         cursor.execute(
#             """
#             SELECT

#                 dc.chunk_id,
#                 dc.chunk_text,

#                 d.title,
#                 d.source_url,
#                 d.domain,
#                 d.category,
#                 d.agent_role,

#                 dc.embedding <=> %s::vector
#                 AS distance

#             FROM document_chunks dc

#             JOIN documents d
#             ON dc.document_id = d.document_id

#             WHERE d.domain = %s

#             ORDER BY distance

#             LIMIT %s
#             """,
#             (
#                 query_embedding,
#                 domain,
#                 limit
#             )
#         )

#     else:

#         cursor.execute(
#             """
#             SELECT

#                 dc.chunk_id,
#                 dc.chunk_text,

#                 d.title,
#                 d.source_url,
#                 d.domain,
#                 d.category,
#                 d.agent_role,

#                 dc.embedding <=> %s::vector
#                 AS distance

#             FROM document_chunks dc

#             JOIN documents d
#             ON dc.document_id = d.document_id

#             ORDER BY distance

#             LIMIT %s
#             """,
#             (
#                 query_embedding,
#                 limit
#             )
#         )

#     rows = cursor.fetchall()


#     print(
#         f"Rows returned from vector query: {len(rows)}"
#     )

#     if rows:
#         print(
#             f"First distance: {rows[0][7]}"
#         )

#     results = []

#     for row in rows:

#         distance = float(
#             row[7]
#         )

#         results.append({

#             "chunk_id": row[0],

#             "chunk_text": row[1],

#             "title": row[2],

#             "source_url": row[3],

#             "domain": row[4],

#             "category": row[5],

#             "agent_role": row[6],

#             "distance": distance,

#             "similarity": round(
#                 1 - distance,
#                 4
#             )
#         })

#     return results
# =====================================================
# HYBRID SEARCH
# =====================================================

def hybrid_search(query):

    keyword_results = keyword_search(
        query=query,
        limit=50
    )

    vector_results = vector_search(
        query=query,
        limit=100
    )

    print(
        f"Keyword Results: {len(keyword_results)}"
    )

    print(
        f"Vector Results: {len(vector_results)}"
    )

    merged = {}

    for item in keyword_results:

        merged[
            item["chunk_id"]
        ] = item
        print(vector_results)
    for item in vector_results:

        merged[
            item["chunk_id"]
        ] = item

    print(
        f"Merged Results: {len(merged)}"
    )

    print("\nTop Vector Results")


    return list(
        merged.values()
    )

# =====================================================
# RERANK RESULTS
# =====================================================

def rerank_results(
    query,
    candidates
):

    print(
        f"Candidates before rerank: {len(candidates)}"
    )

    if not candidates:
        return []

    pairs = [

        (
            query,
            item["chunk_text"]
        )

        for item in candidates
    ]

    scores = reranker.predict(
        pairs
    )

    query_domain = detect_domain(
        query
    )

    STOPWORDS = {

        "what",
        "is",
        "how",
        "why",
        "where",
        "when",
        "a",
        "an",
        "the",
        "does",
        "do",
        "did",
        "can",
        "could",
        "would",
        "should",
        "are",
        "was",
        "were"
    }

    query_terms = [

        term

        for term in query.lower().split()

        if term not in STOPWORDS
    ]

    for item, score in zip(
        candidates,
        scores
    ):

        title = item[
            "title"
        ].lower()

        title_boost = 0

        for term in query_terms:

            if term in title:

                title_boost += 3

        similarity = item.get(
            "similarity",
            0
        )

        # ---------------------------------
        # Domain Boost
        # ---------------------------------

        domain_boost = 0

        if (
            query_domain
            and item.get(
                "domain"
            ) == query_domain
        ):

            domain_boost = 1

        # ---------------------------------
        # Uploaded Document Boost
        # ---------------------------------

        source_boost = 0

        source_url = item.get(
            "source_url",
            ""
        ).lower()

        if (
            "backend/uploads" in source_url
            or source_url.endswith(".pdf")
            or source_url.endswith(".md")
        ):

            source_boost = 2

        # ---------------------------------
        # Store Scores
        # ---------------------------------

        item["rerank_score"] = float(
            score
        )

        item["title_boost"] = (
            title_boost
        )

        item["domain_boost"] = (
            domain_boost
        )

        item["source_boost"] = (
            source_boost
        )

        # ---------------------------------
        # Final Score
        # ---------------------------------

        item["final_score"] = (

            float(score) * 0.75

            +

            similarity * 0.20

            +

            title_boost * 0.05

            +

            domain_boost

            +

            source_boost
        )

    candidates.sort(

        key=lambda x:
        x["final_score"],

        reverse=True
    )

    print(
        "\nTop Results After Reranking"
    )

    for item in candidates[:10]:

        print(

            f"{item['title']} | "

            f"score={round(item['final_score'], 4)} | "

            f"title_boost={item.get('title_boost', 0)} | "

            f"domain_boost={item.get('domain_boost', 0)} | "

            f"source_boost={item.get('source_boost', 0)} | "

            f"similarity={item.get('similarity', 0)}"
        )

    return candidates


# =====================================================
# RETRIEVE CONTEXT
# =====================================================

def retrieve_context(
    query,
    top_k=5
):

    candidates = hybrid_search(
        query
    )

    reranked = rerank_results(

        query=query,

        candidates=candidates
    )

    return reranked[:top_k]

# =====================================================
# API RETRIEVAL
# =====================================================

def retrieve_api_context(
    query,
    top_k=10
):

    candidates = hybrid_search(
        query
    )

    reranked = rerank_results(
        query=query,
        candidates=candidates
    )

    api_results = []

    for item in reranked:

        text = (

            item.get(
                "title",
                ""
            )

            +

            " "

            +

            item.get(
                "chunk_text",
                ""
            )

        ).lower()

        score = item.get(
            "final_score",
            0
        )

        api_boost = 0

        # API indicators

        if "/api/" in text:
            api_boost += 3

        if "endpoint" in text:
            api_boost += 3

        if "get " in text:
            api_boost += 2

        if "post " in text:
            api_boost += 2

        if "put " in text:
            api_boost += 2

        if "delete " in text:
            api_boost += 2

        if "request example" in text:
            api_boost += 2

        if "response example" in text:
            api_boost += 2

        if "authentication" in text:
            api_boost += 2

        item["api_boost"] = (
            api_boost
        )

        item["final_score"] = (
            score
            +
            api_boost
        )

        api_results.append(
            item
        )

    api_results.sort(

        key=lambda x:
        x["final_score"],

        reverse=True
    )

    print(
        "\nTop API Results"
    )

    for item in api_results[:10]:

        print(

            f"{item['title']} | "

            f"score={round(item['final_score'], 4)} | "

            f"api_boost={item.get('api_boost', 0)}"
        )

    return api_results[:top_k]

# =====================================================
# CODE RETRIEVAL
# =====================================================

# =====================================================
# CODE RETRIEVAL
# =====================================================

def retrieve_code_context(
    query,
    top_k=10
):

    # Get larger candidate pool from existing retrieval
    candidates = retrieve_context(
        query=query,
        top_k=50
    )

    print(
        f"\nCandidates before code rerank: {len(candidates)}"
    )

    STOPWORDS = {

        "what",
        "does",
        "is",
        "how",
        "explain",
        "describe",
        "tell",
        "me",
        "about",
        "the",
        "a",
        "an",
        "of",
        "in",
        "for",
        "class",
        "method",
        "function",
        "do",
        "this"
    }

    query_terms = [

        term.lower()

        for term in query.split()

        if (
            term.lower() not in STOPWORDS
            and len(term) > 2
        )
    ]

    print(
        f"Code Query Terms: {query_terms}"
    )

    for item in candidates:

        title = item.get(
            "title",
            ""
        ).lower()

        chunk_text = item.get(
            "chunk_text",
            ""
        ).lower()

        title_match = 0
        code_boost = 0

        # ==================================
        # Strong Exact Name Match
        # ==================================

        for term in query_terms:

            if term in title:

                title_match += 30

            if term in chunk_text:

                title_match += 1

        # ==================================
        # Code Specific Boost
        # ==================================

        code_keywords = [

            "class",
            "method",
            "function",
            "service",
            "controller",
            "repository",
            "entity",
            "dto",
            "interface",
            "enum"
        ]

        for keyword in code_keywords:

            if keyword in title:

                code_boost += 3

            if keyword in chunk_text:

                code_boost += 1

        # ==================================
        # Java API Documentation Boost
        # ==================================

        if title.startswith(
            "class "
        ):
            code_boost += 5

        if title.startswith(
            "interface "
        ):
            code_boost += 5

        # ==================================
        # Preserve Existing Score
        # ==================================

        base_score = item.get(
            "final_score",
            0
        )

        item["title_match"] = (
            title_match
        )

        item["code_boost"] = (
            code_boost
        )

        item["final_score"] = (

            base_score

            +

            title_match

            +

            code_boost
        )

    candidates.sort(

        key=lambda x:
        x["final_score"],

        reverse=True
    )

    print(
        "\nTop Code Results"
    )

    for item in candidates[:10]:

        print(

            f"{item['title']} | "

            f"score={round(item['final_score'], 4)} | "

            f"title_match={item.get('title_match', 0)} | "

            f"code_boost={item.get('code_boost', 0)}"
        )

    return candidates[:top_k]