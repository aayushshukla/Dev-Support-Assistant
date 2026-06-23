# backend/agents/document_agent.py

import time

from backend.retrieval.retriever import (
    retrieve_context
)

from backend.generation.context_builder import (
    build_context
)

from backend.generation.generator import (
    generate_answer
)


class DocumentAgent:

    def execute(
        self,
        query: str
    ):

        retrieval_start = time.time()

        results = retrieve_context(
            query=query,
            top_k=10
        )

        retrieval_time = (
            time.time() - retrieval_start
        ) * 1000

        context = build_context(
            results
        )

        llm_start = time.time()

        answer = generate_answer(
            query=query,
            context=context
        )

        llm_time = (
            time.time() - llm_start
        ) * 1000

        citations = []

        seen = set()

        for item in results:

            if item["source_url"] not in seen:

                citations.append({
                    "title": item["title"],
                    "source_url": item["source_url"],
                    "domain": item["domain"],
                    "category": item["category"]
                })

                seen.add(
                    item["source_url"]
                )

        return {

            "agent": "Document Agent",

            "answer": answer,

            "latency": round(
                retrieval_time +
                llm_time,
                2
            ),

            "retrieved_chunks":
                len(results),

            "sources":
                results,

            "citations":
                citations,

            "stats": {

                "retrieval_time_ms":
                    round(
                        retrieval_time,
                        2
                    ),

                "llm_time_ms":
                    round(
                        llm_time,
                        2
                    ),

                "total_time_ms":
                    round(
                        retrieval_time +
                        llm_time,
                        2
                    ),

                "sources_used":
                    len(citations)
            }
        }