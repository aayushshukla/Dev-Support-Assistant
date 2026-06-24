import time

from backend.generation.generator import (
    generate_answer
)


class RunbookAgent:

    AGENT_NAME = "Runbook Agent"

    def build_prompt(
        self,
        query,
        context
    ):

        return f"""
You are a Runbook Execution Agent.

Always structure your response as:

# Runbook Analysis

## Incident Summary

## Possible Causes

## Resolution Steps

## Validation Steps

## Rollback Plan

## Notes

Context:
{context}

Question:
{query}

Instructions:

- Use ONLY information from provided documentation.
- Do not invent troubleshooting steps.
- If information is missing, explicitly mention it.
- Format using markdown.
"""

    def execute(
        self,
        query,
        context,
        chat_history=None,
        model_name="gpt-4o-mini"
    ):

        start = time.perf_counter()

        prompt = self.build_prompt(
            query=query,
            context=context
        )

        answer = generate_answer(
            query=query,
            context=prompt,
            chat_history=chat_history,

           model_name=model_name
        )

        latency = (
            time.perf_counter() - start
        ) * 1000

        return {

            "agent":
                self.AGENT_NAME,

            "answer":
                answer,

            "latency":
                round(latency, 2)
        }