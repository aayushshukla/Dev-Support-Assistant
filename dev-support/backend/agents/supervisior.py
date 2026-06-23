# backend/agents/supervisor.py

from backend.agents.router import (
    route_request
)

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

# =====================================================
# AGENTS
# =====================================================

api_agent = APISpecialistAgent()

runbook_agent = RunbookAgent()

document_agent = DocumentAgent()

code_agent = CodeDocumentationAgent()


# =====================================================
# SUPERVISOR
# =====================================================

def process_query(query):

    # =================================================
    # ROUTING
    # =================================================

    route = route_request(
        query
    )

    print(
        f"\nRoute Selected: {route}"
    )

    print(
        f"Query: {query}"
    )

    # =================================================
    # SYSTEM STATS
    # =================================================

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

    # =================================================
    # API AGENT
    # =================================================

    if route == "api":

        results = retrieve_api_context(
            query=query,
            top_k=10
        )

        context = build_context(
            results
        )

        result = api_agent.execute(
            query=query,
            context=context
        )

        result["retrieved_chunks"] = len(
            results
        )

        result["sources"] = results

        # =============================================
        # WEB FALLBACK
        # =============================================

        if should_fallback(result):

            return execute_web_fallback(

                query=query,

                search_query=
                    f"{query} API documentation"
            )

        return {

            "route": route,

            "agent": result["agent"],

            "answer": result["answer"],

            "latency": result["latency"],

            "retrieved_chunks":
                len(results),

            "sources":
                results,

            "source_type":
                "internal",

            "status":
                "completed"
        }

    # =================================================
    # RUNBOOK AGENT
    # =================================================

    elif route == "runbook":

        results = retrieve_context(
            query=query,
            top_k=10
        )

        context = build_context(
            results
        )

        result = runbook_agent.execute(
            query=query,
            context=context
        )

        result["retrieved_chunks"] = len(
            results
        )

        result["sources"] = results

        # =============================================
        # WEB FALLBACK
        # =============================================

        if should_fallback(result):

            return execute_web_fallback(

                query=query,

                search_query=
                    f"{query} troubleshooting guide"
            )

        return {

            "route": route,

            "agent": result["agent"],

            "answer": result["answer"],

            "latency": result["latency"],

            "retrieved_chunks":
                len(results),

            "sources":
                results,

            "source_type":
                "internal",

            "status":
                "completed"
        }

    # =================================================
    # CODE AGENT
    # =================================================

    elif route == "code":

        results = retrieve_code_context(
            query=query,
            top_k=10
        )

        context = build_context(
            results
        )

        result = code_agent.execute(
            query=query,
            context=context
        )

        result["retrieved_chunks"] = len(
            results
        )

        result["sources"] = results

        # =============================================
        # WEB FALLBACK
        # =============================================

        if should_fallback(result):

            return execute_web_fallback(

                query=query,

                search_query=
                    f"{query} programming documentation"
            )

        return {

            "route": route,

            "agent": result["agent"],

            "answer": result["answer"],

            "latency": result["latency"],

            "retrieved_chunks":
                len(results),

            "sources":
                results,

            "source_type":
                "internal",

            "status":
                "completed"
        }

    # =================================================
    # DOCUMENT AGENT
    # =================================================

    else:

        result = document_agent.execute(
            query=query
        )

        # =============================================
        # WEB FALLBACK
        # =============================================

        if should_fallback(result):

            return execute_web_fallback(
                query=query
            )

        return {

            "route": route,

            "agent": result["agent"],

            "answer": result["answer"],

            "latency": result["latency"],

            "retrieved_chunks":
                result["retrieved_chunks"],

            "sources":
                result["sources"],

            "citations":
                result.get(
                    "citations",
                    []
                ),

            "stats":
                result.get(
                    "stats",
                    {}
                ),

            "source_type":
                "internal",

            "status":
                "completed"
        }