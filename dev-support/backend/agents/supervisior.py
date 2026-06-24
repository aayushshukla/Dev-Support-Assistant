# backend/agents/supervisor.py

from backend.agents.router import route_request

from backend.agents.api_agent import (
    APISpecialistAgent
)

from backend.agents.runbookagent import (
    RunbookAgent
)

from backend.agents.documentagent import (
    DocumentAgent
)

from backend.agents.codedocumentationagent import (
    CodeDocumentationAgent
)

from backend.retrieval.retriever import (

    retrieve_context,

    retrieve_api_context,

    retrieve_code_context
)

from backend.generation.context_builder import (
    build_context
)

from backend.services.fallback_service import (

    should_fallback,

    execute_web_fallback
)

from backend.utils.system_stats import (
    SYSTEM_STATS
)

from backend.services.cacheservice import (

    get_cached_response,

    set_cached_response
)

# =====================================================
# AGENTS
# =====================================================

api_agent = APISpecialistAgent()

runbook_agent = RunbookAgent()

document_agent = DocumentAgent()

code_agent = CodeDocumentationAgent()

# =====================================================
# CONFIDENCE SCORE
# =====================================================

def calculate_confidence(sources):

    if not sources:

        return 0

    top_doc = sources[0]

    rerank_score = max(
        top_doc.get(
            "rerank_score",
            0
        ),
        0
    )

    similarity = max(
        top_doc.get(
            "similarity",
            0
        ),
        0
    )

    confidence = (

        rerank_score * 0.7

        +

        similarity * 0.3

    )

    confidence = min(
        round(confidence * 100),
        100
    )

    return confidence


# =====================================================
# COMMON RESPONSE BUILDER
# =====================================================

def build_response(

    route,

    result,

    sources
):

    confidence = calculate_confidence(
        sources
    )

    return {

        "route": route,

        "agent": result["agent"],

        "answer": result["answer"],

        "latency": result["latency"],

        "retrieved_chunks":
            len(sources),

        "sources":
            sources,

        "confidence":
            confidence,

        "source_type":
            "internal",

        "status":
            "completed",

        "cache":
            "miss"
    }

# =====================================================
# UPDATE STATS
# =====================================================

def update_query_stats(route):

    SYSTEM_STATS["total_queries"] += 1

    if route == "api":

        SYSTEM_STATS["api_queries"] += 1

    elif route == "runbook":

        SYSTEM_STATS["runbook_queries"] += 1

    elif route == "code":

        SYSTEM_STATS["code_queries"] += 1

    else:

        SYSTEM_STATS["document_queries"] += 1

    print("\nSYSTEM STATS")

    print(SYSTEM_STATS)


# =====================================================
# SUPERVISOR
# =====================================================

# supervisior.py — two changes inside process_query

def process_query(query, chat_history=None, model_name="gpt-4o-mini"):

    cached_response = get_cached_response(query)
    if cached_response:
        print("\n CACHE HIT")
        response = cached_response.copy()
        response["cache"] = "hit"
        return response

    print("\n CACHE MISS")

    # ── FIX: pass chat_history so router resolves "it", "that" etc ──
    route = route_request(query, chat_history=chat_history)

    print(f"\nRoute Selected: {route}")
    update_query_stats(route)

    # =================================================
    # API AGENT
    # =================================================
    if route == "api":
        results = retrieve_api_context(query=query, top_k=10)
        context = build_context(results)
        result  = api_agent.execute(
            query=query, context=context,
            chat_history=chat_history, model_name=model_name
        )
        result["sources"]          = results
        result["retrieved_chunks"] = len(results)   # ← FIX: needed by should_fallback

        response = build_response(route=route, result=result, sources=results)
        response["confidence"] = calculate_confidence(results)
        set_cached_response(query, response)
        return response

    # =================================================
    # RUNBOOK AGENT
    # =================================================
    elif route == "runbook":
        results = retrieve_context(query=query, top_k=10)
        context = build_context(results)
        result  = runbook_agent.execute(
            query=query, context=context,
            chat_history=chat_history, model_name=model_name
        )
        result["sources"]          = results
        result["retrieved_chunks"] = len(results)   # ← FIX

        response = build_response(route=route, result=result, sources=results)
        set_cached_response(query, response)
        return response

    # =================================================
    # CODE AGENT
    # =================================================
    elif route == "code":
        results = retrieve_code_context(query=query, top_k=10)
        context = build_context(results)
        result  = code_agent.execute(
            query=query, context=context,
            chat_history=chat_history, model_name=model_name
        )
        result["sources"]          = results
        result["retrieved_chunks"] = len(results)   # ← FIX

        if should_fallback(result):
            response = execute_web_fallback(
                query=query,
                search_query=f"{query} programming documentation"
            )
            response["confidence"] = 60
            set_cached_response(query, response)
            return response

        response = build_response(route=route, result=result, sources=results)
        set_cached_response(query, response)
        return response

    # =================================================
    # DOCUMENT AGENT (retrieval)
    # =================================================
    else:
        result = document_agent.execute(
            query=query, chat_history=chat_history, model_name=model_name
        )

        if should_fallback(result):
            response = execute_web_fallback(query=query)
            response["confidence"] = 60
            set_cached_response(query, response)
            return response

        confidence = calculate_confidence(result.get("sources", []))
        response = {
            "route":             route,
            "agent":             result["agent"],
            "answer":            result["answer"],
            "latency":           result["latency"],
            "retrieved_chunks":  result["retrieved_chunks"],
            "sources":           result["sources"],
            "confidence":        confidence,
            "citations":         result.get("citations", []),
            "stats":             result.get("stats", {}),
            "source_type":       "internal",
            "status":            "completed",
            "cache":             "miss",
        }
        set_cached_response(query, response)
        return response