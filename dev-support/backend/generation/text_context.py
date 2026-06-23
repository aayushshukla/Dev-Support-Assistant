from backend.retrieval.retriever import (
    retrieve_context
)

from backend.generation.context_builder import (
    build_context
)

query = (
    "How does Django middleware process requests?"
)

results = retrieve_context(
    query=query
)

context = build_context(
    results
)

print(context)