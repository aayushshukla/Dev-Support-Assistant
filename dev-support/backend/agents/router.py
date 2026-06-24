# backend/agents/router.py

# =====================================================
# FOLLOW-UP RESOLVER
# Handles short queries like "how to stop it",
# "give me an example", "what about kubernetes"
# by checking last assistant turn for context
# =====================================================

FOLLOWUP_TRIGGERS = [
    "it", "that", "this", "same", "above",
    "how to", "how do", "what about", "show me",
    "give me", "can you", "tell me more", "explain more",
    "stop", "start", "run", "kill", "remove", "delete",
    "get", "list", "check", "view", "create",
]

def is_followup(query):
    """Short queries with pronouns or action verbs are follow-ups."""
    words = query.lower().split()
    if len(words) <= 5:
        for trigger in FOLLOWUP_TRIGGERS:
            if trigger in query.lower():
                return True
    return False


def resolve_query_with_history(query, chat_history):
    """
    For follow-up queries, prepend the last assistant
    response so keyword matching works on full context.
    e.g. "how to stop it" + "Docker is a container..."
    becomes "Docker is a container... how to stop it"
    which matches docker/container runbook keywords.
    """
    if not chat_history:
        return query

    if not is_followup(query):
        return query

    # find last assistant turn
    last_assistant = ""
    for turn in reversed(chat_history):
        if turn.get("role") == "assistant":
            last_assistant = turn.get("content", "")[:300]
            break

    if last_assistant:
        resolved = f"{last_assistant} {query}"
        print(f"Follow-up detected. Resolved: {resolved[:100]}...")
        return resolved

    return query


# =====================================================
# KEYWORD LISTS
# Rule: be specific — only add words that
# UNAMBIGUOUSLY signal a route. Never add general
# tech terms like "docker" or "kubernetes" here
# because "what is docker" is a knowledge question
# not a runbook operation.
# =====================================================

# Runbook = operational commands, incidents, fixes
RUNBOOK_KEYWORDS = [
    "runbook",
    "restart",
    "troubleshoot",
    "incident",
    "outage",
    "recovery",
    "crashloopbackoff",
    "node not ready",
    "rollback deployment",
    "how to stop",
    "how to start",
    "how to restart",
    "how to run",
    "how to check",
    "how to kill",
    "how to remove",
    "how to deploy",
    "systemctl",
    "journalctl",
    "kubectl",
    "docker stop",
    "docker run",
    "docker ps",
    "docker rm",
    "docker logs",
]

# API = endpoint, schema, request/response structure
API_KEYWORDS = [
    "api",
    "endpoint",
    "swagger",
    "schema",
    "payload",
    "rest",
    "http method",
    "request body",
    "response body",
    "status code",
    "authentication token",
    "bearer token",
]

# Code = source code explanation, classes, methods
CODE_KEYWORDS = [
    "class",
    "method",
    "function",
    "source code",
    "implementation",
    "controller",
    "repository",
    "dto",
    "entity",
    "interface",
    "explain this code",
    "document this code",
    "how does this function",
    "what does this class",
]


def route_request(query, chat_history=None):

    # resolve follow-ups before routing
    resolved = resolve_query_with_history(
        query, chat_history
    ).lower()

    original = query.lower()

    print(f"\nOriginal query : {original}")
    if resolved != original:
        print(f"Resolved query : {resolved[:120]}")

    # check resolved (context-aware) query for runbook
    for keyword in RUNBOOK_KEYWORDS:
        if keyword in resolved:
            print(f"Matched Runbook Keyword: '{keyword}'")
            return "runbook"

    # check original query for api (don't let history bleed in)
    for keyword in API_KEYWORDS:
        if keyword in original:
            print(f"Matched API Keyword: '{keyword}'")
            return "api"

    # check original query for code
    for keyword in CODE_KEYWORDS:
        if keyword in original:
            print(f"Matched Code Keyword: '{keyword}'")
            return "code"

    print("No keyword matched → retrieval")
    return "retrieval"