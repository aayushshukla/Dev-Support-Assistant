from pathlib import Path
from datetime import datetime
import hashlib

from backend.ingestions.csvloader import load_csv
from backend.chunking.chunker import create_chunks
from backend.embeddings.embedder import generate_embedding

from backend.dbops.pgvectore_store import (
    insert_document,
    insert_document_content,
    insert_chunk,connection
)


def generate_hash(content):

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


# =====================================================
# LOAD ALL CSV FILES
# =====================================================

all_documents = []

csv_folder = Path("./backend/data/")

csv_files = list(
    csv_folder.glob("*.csv")
)

print(
    f"\nFound {len(csv_files)} CSV files"
)

for csv_file in csv_files:

    print(
        f"Loading: {csv_file.name}"
    )

    documents = load_csv(
        str(csv_file)
    )

    print(
        f"Loaded {len(documents)} documents"
    )

    all_documents.extend(
        documents
    )

print(
    f"\nTotal Documents Loaded: "
    f"{len(all_documents)}"
)


# =====================================================
# INGEST DOCUMENTS
# =====================================================

total_chunks = 0

for index, document in enumerate(
        all_documents,
        start=1
):

    try:

        content_text = document[
            "content_text"
        ]

        content_hash = document.get(
            "content_hash"
        )

        if not content_hash:

            content_hash = generate_hash(
                content_text
            )

        document_id = insert_document(

            source_url=document[
                "source_url"
            ],

            domain=document[
                "domain"
            ],

            domain_group=document[
                "domain_group"
            ],

            category=document[
                "category"
            ],

            title=document[
                "title"
            ],

            content_hash=content_hash,

            agent_role=document[
                "agent_role"
            ],

            last_scraped_at=datetime.now()
        )

        # Duplicate document
        if document_id is None:

            print(
                f"[{index}] Duplicate skipped"
            )

            connection.rollback()

            continue

        insert_document_content(

            document_id=document_id,

            content_text=content_text,

            code_examples=document.get(
                "code_examples"
            )
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

        connection.commit()

        print(
            f"[{index}/{len(all_documents)}] "
            f"Document {document_id} "
            f"→ {len(chunks)} chunks"
        )

    except Exception as e:

        connection.rollback()

        print(
            f"\nError in document {index}"
        )

        print(e)

        print(
            document.get(
                "title",
                "Unknown"
            )
        )

        continue