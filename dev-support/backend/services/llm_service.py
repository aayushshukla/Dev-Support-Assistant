from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def get_llm():
    return client

def generate_answer(
    query,
    context
):

    prompt = f"""
You are a Developer Assistant.

Answer using only the supplied context.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(

        model=os.getenv("MODEL_NAME","gpt-4o-mini"),

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1
    )

    return (
        response
        .choices[0]
        .message
        .content
    )