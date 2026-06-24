import time

from backend.generation.generator import (
    generate_answer
)


class CodeDocumentationAgent:

    AGENT_NAME = "Code Documentation Agent"

    def build_prompt(
        self,
        query,
        context
    ):

        return f"""
You are a Code Documentation Agent.

Always structure your response as:

# Code Analysis

## Summary

## Purpose

## Parameters

## Return Value

## Dependencies

## Example Usage

## Notes

Context:
{context}

Question:
{query}

Instructions:

- Use ONLY information from the provided context.
- Do not invent code behavior.
- If information is missing, explicitly mention it.
- Format the response using markdown.

Response Format:

## Summary

## Purpose

## Parameters

## Return Value

## Dependencies

## Example Usage

## Notes
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
                round(
                    latency,
                    2
                )
        }