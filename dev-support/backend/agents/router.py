# 
# backend/agents/router.py

def route_request(query):

    query = query.lower()

    api_keywords = [

        "api",
        "endpoint",
        "request",
        "response",
        "swagger",
        "schema",
        "payload",
        "rest"

    ]

    runbook_keywords = [

        "runbook",
        "restart",
        "deploy",
        "incident",
        "troubleshoot",
        "error",
        "failure",
        "crashloopbackoff",
        "pod",
        "node not ready",
        "rollback",
        "outage",
        "recovery"
    ]
    code_keywords = [

        "class",

        "method",

        "function",

        "code",

        "source code",

        "implementation",

        "service",

        "controller",

        "repository",

        "dto",

        "entity",

        "interface",

        "explain this code",

        "document this code"
    ]

    print(f"\nQuery: {query}")

    for keyword in runbook_keywords:

        if keyword in query:

            print(
                f"Matched Runbook Keyword: {keyword}"
            )

            return "runbook"

    for keyword in api_keywords:

        if keyword in query:

            print(
                f"Matched API Keyword: {keyword}"
            )

            return "api"
    for keyword in code_keywords:

        if keyword in query:

            print(
                f"Matched Code Keyword: {keyword}"
            )

            return "code"


    return "retrieval"