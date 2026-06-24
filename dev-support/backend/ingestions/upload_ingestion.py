

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
# AGENT TYPE DETECTOR
# =====================================================

def detect_agent_type(

    source_url,

    category=None,

    domain=None

):

    text = (

        f"{source_url} "
        f"{category} "
        f"{domain}"

    ).lower()

    if "runbook" in text:

        return "runbook"

    elif "api" in text:

        return "api"

    elif (

        "spring" in text

        or

        "fastapi" in text

        or

        "django" in text

        or

        "code" in text

    ):

        return "code"

    return "document"


# =====================================================
# DOCUMENT PROCESSOR
# =====================================================

def process_documents(documents):

    total_documents = 0

    total_chunks = 0

    failed_documents = 0

    duplicate_documents = 0

    duplicate_files = []

    for document in documents:

        try:

            content_text = document.get(
                "content_text"
            )

            if not content_text:

                raise ValueError(
                    "content_text is empty"
                )

            title = document.get(
                "title",
                "Untitled"
            )

            source_url = document.get(
                "source_url",
                "uploaded_document"
            )

            domain = document.get(
                "domain",
                "General"
            )

            domain_group = document.get(
                "domain_group",
                "General"
            )

            category = document.get(
                "category",
                "Documentation"
            )

            doc_category = document.get(
                "doc_category",
                "unknown"
            )

            agent_role = document.get(
                "agent_role",
                "document_agent"
            )

            code_examples = document.get(
                "code_examples",
                ""
            )

            # =========================================
            # DETECT AGENT TYPE
            # =========================================

            agent_type = detect_agent_type(

                source_url=source_url,

                category=category,

                domain=domain
            )

            # =========================================
            # CONTENT HASH
            # =========================================

            content_hash = generate_hash(
                content_text
            )

            # =========================================
            # INSERT DOCUMENT
            # =========================================

            document_id = insert_document(

                source_url=source_url,

                domain=domain,

                domain_group=domain_group,

                category=category,

                doc_category=doc_category,

                title=title,

                content_hash=content_hash,

                agent_role=agent_role,

                agent_type=agent_type,

                last_scraped_at=datetime.now()
            )

            # Duplicate

            if not document_id:

                duplicate_documents += 1

                duplicate_files.append(
                    title
                )

                continue

            # =========================================
            # STORE CONTENT
            # =========================================

            insert_document_content(

                document_id=document_id,

                content_text=content_text,

                code_examples=code_examples
            )

            # =========================================
            # CHUNKING
            # =========================================

            chunks = create_chunks(
                content_text
            )

            chunks = [

                chunk.strip()

                for chunk in chunks

                if chunk and chunk.strip()
            ]

            total_chunks += len(
                chunks
            )

            print(
                f"Generated "
                f"{len(chunks)} chunks"
            )

            # =========================================
            # EMBEDDINGS + INSERT CHUNKS
            # =========================================

            for chunk in chunks:

                try:

                    embedding = generate_embedding(
                        chunk
                    )

                    if embedding is None:

                        print(
                            "Embedding failed. "
                            "Skipping chunk."
                        )

                        continue

                    insert_chunk(

                        document_id=document_id,

                        chunk_text=chunk,

                        embedding=embedding
                    )

                except Exception as e:

                    print(
                        f"Chunk failed: "
                        f"{str(e)}"
                    )

                    continue

            commit()

            total_documents += 1

            print(
                f"Processed: {title}"
            )

        except Exception as e:

            rollback()

            failed_documents += 1

            print("\n" + "=" * 80)

            print(
                f"ERROR PROCESSING DOCUMENT: "
               
            )

            print(
                f"Exception: {str(e)}"
            )

            print("\nDocument Metadata:")

            print(document)

            print("\nTraceback:")

            traceback.print_exc()

            print("=" * 80)

            continue

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

    # ==============================================
    # CSV
    # ==============================================

    if extension == ".csv":

        validate_csv_schema(
            file_path
        )

        documents = load_csv(
            file_path
        )

        doc_category = "csv"

    # ==============================================
    # PDF
    # ==============================================

    elif extension == ".pdf":

        documents = load_pdf(
            file_path
        )

        doc_category = "pdf"

    # ==============================================
    # MARKDOWN
    # ==============================================

    elif extension in [

        ".md",

        ".markdown"
    ]:

        documents = load_markdown(
            file_path
        )

        doc_category = "markdown"

    else:

        raise ValueError(

            f"Unsupported file type: "
            f"{extension}"
        )

    # ==============================================
    # ENRICH METADATA
    # ==============================================

    for document in documents:

        document["doc_category"] = (
            doc_category
        )

        document["source_url"] = str(
            file_path
        )

    print(

        f"Loaded "
        f"{len(documents)} document(s)"
    )

    return process_documents(
        documents
    )


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    upload_folder = Path(
        "./backend/uploads"
    )

    files = list(
        upload_folder.glob("*")
    )

    print(
        f"\nFound {len(files)} files"
    )

    for file in files:

        print(
            f"\nProcessing: {file.name}"
        )

        try:

            result = ingest_file(
                str(file)
            )

            print(result)

        except Exception as e:

            print(
                f"Failed: {file.name}"
            )

            print(e)

