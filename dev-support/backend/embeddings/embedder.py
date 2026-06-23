from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings

# Load BGE embedding model once during application startup
# Used for:
# 1. Semantic chunking
# 2. Document embeddings
# 3. Query embeddings
model = SentenceTransformer(
    "BAAI/bge-base-en-v1.5"
)


class BGEEmbeddingWrapper(Embeddings):
    """
    Wrapper required by LangChain SemanticChunker.

    Converts text into vector embeddings that help identify
    semantic boundaries between topics.
    """

    def embed_documents(self, texts):
        """
        Generate embeddings for multiple text chunks.
        Used during semantic chunking.
        """
        return model.encode(
            texts,
            normalize_embeddings=True
        ).tolist()

    def embed_query(self, text):
        """
        Generate embedding for a single query.
        Used during semantic similarity calculations.
        """
        return model.encode(
            text,
            normalize_embeddings=True
        ).tolist()


def generate_embedding(text):
    """
    Generate vector embedding for a document chunk.

    Used before storing chunks in pgvector.
    """
    return model.encode(
        text,
        normalize_embeddings=True
    ).tolist()