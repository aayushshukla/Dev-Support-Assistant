from backend.retrieval.retriever import retrieve_context

from backend.generation.context_builder import build_context

from backend.generation.generator import generate_answer


query = "How does Django middleware process requests?"


# Retrieve relevant chunks
results = retrieve_context(
    query=query
)

# Build context
context = build_context(
    results
)

print("\nRetrieved Context:")
print("=" * 80)
print(context[:2000])

# Generate answer
answer = generate_answer(
    query=query,
    context=context
)

print("\nGenerated Answer:")
print("=" * 80)
print(answer)