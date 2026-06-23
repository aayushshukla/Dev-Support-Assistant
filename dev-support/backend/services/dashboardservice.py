from backend.dbops.pgvectore_store import get_connection
from backend.utils.system_stats import (
    SYSTEM_STATS
)

def get_dashboard_stats():

    conn = get_connection()

    cursor = conn.cursor()

    # Documents
    cursor.execute("""
        SELECT COUNT(*)
        FROM documents
    """)

    result = cursor.fetchone()
    documents = result[0] if result else 0
    # Chunks
    cursor.execute("""
        SELECT COUNT(*)
        FROM document_chunks
    """)

    result = cursor.fetchone()
    chunks = result[0] if result else 0

    # Domains
    cursor.execute("""
        SELECT COUNT(DISTINCT domain)
        FROM documents
    """)

    result = cursor.fetchone()
    domains = result[0] if result else 0

    # Categories
    cursor.execute("""
        SELECT COUNT(DISTINCT category)
        FROM documents
    """)

    result = cursor.fetchone()
    categories = result[0] if result else 0

    # Agent Distribution
    cursor.execute("""
        SELECT
            agent_role,
            COUNT(*) AS total
        FROM documents
        GROUP BY agent_role
        ORDER BY total DESC
    """)

    agent_distribution = [

        {
            "agent_role": row[0],
            "count": row[1]
        }

        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return {

    "documents": documents,

    "chunks": chunks,

    "domains": domains,

    "categories": categories,

    "agent_distribution":
        agent_distribution,

    "query_stats":
        SYSTEM_STATS
     }