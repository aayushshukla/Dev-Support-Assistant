# 
# backend/agents/api_agent.py

import time

from backend.generation.generator import (
    generate_answer
)


class APISpecialistAgent:

    AGENT_NAME = "API Specialist Agent"

    def build_system_prompt(self):

        return """
You are an API Specialist Agent.

Your job is to explain APIs using ONLY the
retrieved documentation.

Always return the answer in this format:

# API Analysis

## Summary

## Endpoint

## Purpose

## Request Parameters

## Request Example

## Response Example

## Authentication

## Notes

Rules:

1. Use ONLY information from the supplied documentation.
2. Do not use external knowledge.
3. If information is missing, explicitly state:
   "Information not available in the retrieved documentation."
4. Never invent endpoints, request bodies, or responses.
5. Keep explanations technical and concise.
6. Never generate a Sources section.
7. Citations are handled by the application.
"""

    def execute(
        self,
        query,
        context
    ):

        print(
            "\nAPI AGENT EXECUTED\n"
        )

        start = time.perf_counter()

        answer = generate_answer(
            query=query,
            context=context,
            system_prompt=self.build_system_prompt()
        )

        latency = (
            time.perf_counter() - start
        ) * 1000

        return {

            "agent": self.AGENT_NAME,

            "answer": answer,

            "latency": round(
                latency,
                2
            ),

            "stats": {

                "retrieval_time_ms": 0,

                "llm_time_ms": round(
                    latency,
                    2
                ),

                "total_time_ms": round(
                    latency,
                    2
                ),

                "sources_used": 0
            }
        }