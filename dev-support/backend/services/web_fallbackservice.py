# backend/services/web_fallbackservice.py

import os
import requests

from backend.services.llm_service import (
    generate_answer
)


SERPER_API_KEY = os.getenv(
    "SERPER_API_KEY"
)

SERPER_URL = (
    "https://google.serper.dev/search"
)


def search_web(
    query: str,
    max_results: int = 5
):

    print(
        f"\n🌐 WEB SEARCH: {query}"
    )

    try:

        # ==========================================
        # VALIDATE API KEY
        # ==========================================

        if not SERPER_API_KEY:

            raise ValueError(
                "SERPER_API_KEY not found."
            )

        # ==========================================
        # CALL SERPER API
        # ==========================================

        payload = {
            "q": query
        }

        headers = {

            "X-API-KEY":
                SERPER_API_KEY,

            "Content-Type":
                "application/json"
        }

        response = requests.post(

            SERPER_URL,

            json=payload,

            headers=headers,

            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        organic_results = data.get(
            "organic",
            []
        )[:max_results]

        # ==========================================
        # NO RESULTS
        # ==========================================

        if not organic_results:

            return {

                "agent":
                    "Web Agent",

                "answer":
                    "No relevant external documentation found.",

                "sources": [],

                "retrieved_chunks": 0,

                "source_type":
                    "external",

                "status":
                    "completed"
            }

        # ==========================================
        # BUILD CONTEXT
        # ==========================================

        context = ""

        sources = []

        for idx, result in enumerate(
            organic_results
        ):

            title = result.get(
                "title",
                "No Title"
            )

            snippet = result.get(
                "snippet",
                "No Description Available"
            )

            url = result.get(
                "link",
                ""
            )

            context += f"""
Document {idx + 1}

Title:
{title}

Content:
{snippet}

URL:
{url}

----------------------------------------
"""

            sources.append({

                "title":
                    title,

                "source_url":
                    url,

                "domain":
                    "External",

                "content":
                    snippet
            })

        # ==========================================
        # GENERATE FINAL ANSWER
        # ==========================================

        answer = generate_answer(

            query=query,

            context=context
        )

        print(
            f"Retrieved {len(sources)} "
            f"external sources."
        )

        # ==========================================
        # RESPONSE
        # ==========================================

        return {

            "agent":
                "Web Agent",

            "answer":
                answer,

            "sources":
                sources,

            "retrieved_chunks":
                len(sources),

            "source_type":
                "external",

            "stats": {

                "sources_used":
                    len(sources)
            },

            "status":
                "completed"
        }

    except requests.exceptions.Timeout:

        return {

            "agent":
                "Web Agent",

            "answer":
                "Web search timed out.",

            "sources": [],

            "retrieved_chunks": 0,

            "source_type":
                "external",

            "status":
                "failed"
        }

    except requests.exceptions.HTTPError as e:

        return {

            "agent":
                "Web Agent",

            "answer":
                f"Serper API error: {str(e)}",

            "sources": [],

            "retrieved_chunks": 0,

            "source_type":
                "external",

            "status":
                "failed"
        }

    except Exception as e:

        print(
            f"Web Search Error: {str(e)}"
        )

        return {

            "agent":
                "Web Agent",

            "answer":
                f"External search failed: {str(e)}",

            "sources": [],

            "retrieved_chunks": 0,

            "source_type":
                "external",

            "status":
                "failed"
        }