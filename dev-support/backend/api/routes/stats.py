# backend/api/routes/stats.py

from fastapi import APIRouter
from backend.dbops.pgvectore_store import cursor

router = APIRouter()


@router.get("/stats")
def get_stats():

    cursor.execute(
        "SELECT COUNT(*) FROM documents"
    )
    result1 = cursor.fetchone()

    documents = (
        result1[0]
        if result1
        else 0
    )

    cursor.execute(
        "SELECT COUNT(*) FROM document_chunks"
    )
    result2 = cursor.fetchone()
    chunks = (
    result2[0]
    if result2
    else 0
    )
    cursor.execute(
        """
        SELECT COUNT(DISTINCT domain)
        FROM documents
        """
    )
    result3 = cursor.fetchone()

    domains = (
        result3[0]
        if result3
        else 0
    )

    cursor.execute(
        """
        SELECT COUNT(DISTINCT category)
        FROM documents
        """
    )
    result4 = cursor.fetchone()

    categories = (
        result4[0]
        if result4
        else 0
    )

    return {
        "total_documents": documents,
        "total_chunks": chunks,
        "total_domains": domains,
        "total_categories": categories
    }