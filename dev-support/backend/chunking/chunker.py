from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


# =====================================================
# CHUNKING CONFIGURATION
# =====================================================

# Chunk size selected to:
# - Preserve sufficient technical context
# - Stay within embedding model limits
# - Improve retrieval accuracy



text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=1000,

    chunk_overlap=200,

    separators=[

        "\n# ",

        "\n## ",

        "\n### ",

        "```",

        "\n\n",

        "\n",

        ". ",

        " ",

        ""
    ]
)

def create_chunks(text):
    """
    Recursive Character Chunking

    Splits large documents into smaller overlapping chunks.

    Benefits:
    - Works well on scraped documentation
    - Preserves context using overlap
    - Avoids dependence on markdown structure
    - Produces consistent chunk sizes for embeddings

    Returns:
        List[str]
    """

    return text_splitter.split_text(text)