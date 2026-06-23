"""
PGVector Store

Responsibilities:
- PostgreSQL Connection
- PGVector Registration
- Document Storage
- Content Storage
- Chunk Storage
- Transaction Management
- Debug Utilities
"""

import logging
import psycopg2
import os
from pgvector.psycopg2 import (
    register_vector
)

# =====================================================
# LOGGING CONFIGURATION
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s"
)

logger = logging.getLogger(__name__)

# =====================================================
# DATABASE CONNECTION
# =====================================================

logger.info(
    "Connecting to PostgreSQL..."
)

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "developer_assistant"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )
    register_vector(conn)
    return conn
connection = get_connection()

register_vector(
    connection
)

cursor = connection.cursor()

logger.info(
    "PostgreSQL connection established"
)

# =====================================================
# TRANSACTION HELPERS
# =====================================================

def commit():

    connection.commit()

    logger.info(
        "Transaction committed"
    )


def rollback():

    connection.rollback()

    logger.error(
        "Transaction rolled back"
    )


# =====================================================
# INSERT DOCUMENT
# =====================================================

def insert_document(
    source_url,
    domain,
    domain_group,
    category,
    title,
    content_hash,
    agent_role,
    last_scraped_at
):

    logger.info(
        f"Inserting document: {title}"
    )

    cursor.execute(
        """
        INSERT INTO documents(

            source_url,
            domain,
            domain_group,
            category,
            title,
            content_hash,
            agent_role,
            last_scraped_at

        )

        VALUES(

            %s,%s,%s,%s,
            %s,%s,%s,%s

        )

        ON CONFLICT(content_hash)
        DO NOTHING

        RETURNING document_id
        """,
        (
            source_url,
            domain,
            domain_group,
            category,
            title,
            content_hash,
            agent_role,
            last_scraped_at
        )
    )

    result = cursor.fetchone()

    # Duplicate Document

    if result is None:

        logger.warning(
            f"Duplicate document detected: {title}"
        )

        return None

    document_id = result[0]

    logger.info(
        f"Document inserted successfully. "
        f"ID={document_id}"
    )

    return document_id


# =====================================================
# INSERT DOCUMENT CONTENT
# =====================================================

def insert_document_content(
    document_id,
    content_text,
    code_examples
):

    logger.info(
        f"Storing content for "
        f"document_id={document_id}"
    )

    cursor.execute(
        """
        INSERT INTO document_content(

            document_id,
            content_text,
            code_examples

        )

        VALUES(

            %s,%s,%s

        )
        """,
        (
            document_id,
            content_text,
            code_examples
        )
    )


# =====================================================
# INSERT CHUNK
# =====================================================

def insert_chunk(
    document_id,
    chunk_index,
    chunk_text,
    embedding
):

    cursor.execute(
        """
        INSERT INTO document_chunks(

            document_id,
            chunk_index,
            chunk_text,
            embedding

        )

        VALUES(

            %s,%s,%s,%s

        )
        """,
        (
            document_id,
            chunk_index,
            chunk_text,
            embedding
        )
    )


# =====================================================
# DOCUMENT COUNT
# =====================================================

def get_document_count():

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM documents
        """
    )

    result = cursor.fetchone()

    return (
        result[0]
        if result
        else 0
    )


# =====================================================
# CHUNK COUNT
# =====================================================

def get_chunk_count(
    document_id
):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM document_chunks
        WHERE document_id = %s
        """,
        (
            document_id,
        )
    )

    result = cursor.fetchone()

    return (
        result[0]
        if result
        else 0
    )


# =====================================================
# DOCUMENT LOOKUP
# =====================================================

def get_document_by_title(
    title
):

    cursor.execute(
        """
        SELECT

            document_id,
            title,
            domain

        FROM documents

        WHERE title = %s
        """,
        (
            title,
        )
    )

    return cursor.fetchone()


# =====================================================
# DEBUG DOCUMENT CHUNKS
# =====================================================

def debug_document_chunks(
    document_id
):

    cursor.execute(
        """
        SELECT

            chunk_id,

            LEFT(
                chunk_text,
                300
            )

        FROM document_chunks

        WHERE document_id = %s
        """,
        (
            document_id,
        )
    )

    rows = cursor.fetchall()

    logger.info(
        f"Chunks found: {len(rows)}"
    )

    for row in rows:

        logger.info(
            "=" * 60
        )

        logger.info(
            f"Chunk ID: {row[0]}"
        )

        logger.info(
            row[1]
        )






def get_total_documents():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM documents")
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        cursor.close()
        conn.close()

def get_total_chunks():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM document_chunks")
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        cursor.close()
        conn.close()

def get_total_domains():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(DISTINCT domain) FROM documents")
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        cursor.close()
        conn.close()

def get_total_categories():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(DISTINCT category) FROM documents")
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        cursor.close()
        conn.close()

def print_document_stats():
    logger.info("=" * 60)
    logger.info(f"Documents : {get_total_documents()}")
    logger.info(f"Chunks    : {get_total_chunks()}")
    logger.info(f"Domains   : {get_total_domains()}")
    logger.info(f"Categories: {get_total_categories()}")
    logger.info("=" * 60)

# =====================================================
# CLOSE CONNECTION
# =====================================================

def close_connection():

    cursor.close()

    connection.close()

    logger.info(
        "Database connection closed"
    )


if __name__ == "__main__":
    print_document_stats()


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print_document_stats()