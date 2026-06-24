# from backend.agents.router import route_request

# queries = [

#     "How to restart Jenkins?",

#     "Pod CrashLoopBackOff troubleshooting",

#     "Deployment failed",

#     "Node not ready",

#     "What is Docker?"
# ]

# for query in queries:

#     print(
#         query,
#         "=>",
#         route_request(query)
#     )

from backend.agents.router import (
    route_request
)

tests = [

    "Explain UserService class",

    "What does vector_search function do",

    "Explain Employee entity",

    "Document this controller",

    "What is Docker"
]

for query in tests:

    print(
        query,
        "=>",
        route_request(query)
    )