# backend/agents/test_supervisor.py

from backend.agents.supervisior import (
    process_query
)

query = (
    "How does Django middleware process requests?"
)

response = process_query(
    query
)

print("\n")
print("=" * 80)

print(
    f"Route: {response['route']}"
)

print("=" * 80)

print(
    response["answer"]
)

print("\nSources:")

for source in response["sources"]:

    print(
        f"- {source['title']}"
    )