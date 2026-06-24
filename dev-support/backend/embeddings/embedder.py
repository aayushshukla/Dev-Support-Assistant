import os

from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.embeddings import Embeddings

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

EMBEDDING_MODEL = "text-embedding-3-small"


class OpenAIEmbeddingWrapper(Embeddings):

    def embed_documents(self, texts):

        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts
        )

        return [
            item.embedding
            for item in response.data
        ]

    def embed_query(self, text):

        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )

        return response.data[0].embedding


# =====================================================
# GENERATE EMBEDDING
# =====================================================

def generate_embedding(text):
    """
    Generate embedding for a single chunk.
    Used during ingestion and retrieval.
    """

    try:

        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )

        return response.data[0].embedding

    except Exception as e:

        print(
            f"Embedding Error: {str(e)}"
        )

        return None