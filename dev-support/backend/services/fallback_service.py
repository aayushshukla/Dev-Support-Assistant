from backend.services.web_fallbackservice import (
    search_web
)


def should_fallback(result):

    retrieved_chunks = result.get(
        "retrieved_chunks",
        0
    )

    sources = result.get(
        "sources",
        []
    )

    answer = result.get(
        "answer",
        ""
    ).lower()

    if retrieved_chunks == 0:
        return True

    if len(sources) == 0:
        return True

    fallback_phrases = [

        "could not find sufficient information",

        "insufficient information",

        "no relevant documentation found",

        "no information available"
    ]

    for phrase in fallback_phrases:

        if phrase in answer:
            return True

    return False


def execute_web_fallback(
    query,
    search_query=None
):

    if search_query is None:

        search_query = query

    print(
        "\n🌐 WEB FALLBACK ACTIVATED"
    )

    web_result = search_web(
        query=search_query
    )

    return {

        "route": "web",

        "agent":
            web_result.get(
                "agent",
                "Web Agent"
            ),

        "answer":
            web_result.get(
                "answer"
            ),

        "latency": 0,

        "retrieved_chunks":
            web_result.get(
                "retrieved_chunks",
                0
            ),

        "sources":
            web_result.get(
                "sources",
                []
            ),

        "source_type":
            "external",

        "stats":
            web_result.get(
                "stats",
                {}
            ),

        "status":
            "completed"
    }