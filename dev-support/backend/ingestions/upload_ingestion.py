from datetime import datetime
from pathlib import Path
import hashlib
import traceback

import pandas as pd

from backend.ingestions.csvloader import (
    load_csv
)

from backend.ingestions.pdf_loader import (
    load_pdf
)

from backend.ingestions.markdown_loader import (
    load_markdown
)

from backend.chunking.chunker import (
    create_chunks
)

from backend.embeddings.embedder import (
    generate_embedding
)

from backend.dbops.pgvectore_store import (
    insert_document,
    insert_document_content,
    insert_chunk,
    commit,
    rollback
)


# =====================================================
# CSV VALIDATION
# =====================================================

def validate_csv_schema(file_path):

    df = pd.read_csv(
        file_path,
        nrows=1
    )

    required_columns = [
        "title",
        "content_text"
    ]

    missing_columns = [

        column

        for column in required_columns

        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )

    print(
        "Schema validation passed"
    )


# =====================================================
# HASH GENERATION
# =====================================================

def generate_hash(content):

    return hashlib.sha256(
        content.encode(
            "utf-8"
        )
    ).hexdigest()


# =====================================================
# DOCUMENT PROCESSOR
# =====================================================

def process_documents(documents):

    total_documents = 0
    total_chunks = 0
    failed_documents = 0

    duplicate_documents = 0
    duplicate_files = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        try:

            content_text = document.get(
                "content_text"
            )

            title = document.get(
                "title"
            )

            if not content_text:

                raise ValueError(
                    "content_text is empty"
                )

            if not title:

                title = "Untitled"

            source_url = document.get(
                "source_url"
            )

            domain = document.get(
                "domain"
            )

            domain_group = document.get(
                "domain_group"
            )

            category = document.get(
                "category"
            )

            agent_role = document.get(
                "agent_role"
            )

            code_examples = document.get(
                "code_examples"
            )

            content_hash = generate_hash(
                content_text
            )

            document_id = insert_document(

                source_url=source_url,

                domain=domain,

                domain_group=domain_group,

                category=category,

                title=title,

                content_hash=content_hash,

                agent_role=agent_role,

                last_scraped_at=datetime.now()
            )

            if not document_id:

                duplicate_documents += 1

                duplicate_files.append(
                    title
                )

                continue

            insert_document_content(

                document_id=document_id,

                content_text=content_text,

                code_examples=code_examples
            )

            chunks = create_chunks(
                content_text
            )

            total_chunks += len(
                chunks
            )

            for chunk_index, chunk in enumerate(
                chunks
            ):

                embedding = generate_embedding(
                    chunk
                )

                insert_chunk(

                    document_id=document_id,

                    chunk_index=chunk_index,

                    chunk_text=chunk,

                    embedding=embedding
                )

            commit()

            total_documents += 1

        except Exception:

            rollback()

            failed_documents += 1

            traceback.print_exc()

    return {

        "documents_processed":
        total_documents,

        "chunks_created":
        total_chunks,

        "failed_documents":
        failed_documents,

        "duplicate_documents":
        duplicate_documents,

        "duplicate_files":
        duplicate_files
    }


# =====================================================
# MAIN INGESTION ENTRYPOINT
# =====================================================

def ingest_file(file_path):

    extension = (
        Path(file_path)
        .suffix
        .lower()
    )

    if extension == ".csv":

        validate_csv_schema(
            file_path
        )

        documents = load_csv(
            file_path
        )

    elif extension == ".pdf":

        documents = load_pdf(
            file_path
        )

    elif extension in [
        ".md",
        ".markdown"
    ]:

        documents = load_markdown(
            file_path
        )

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    print(
        f"Loaded {len(documents)} document(s)"
    )

    return process_documents(
        documents
    )