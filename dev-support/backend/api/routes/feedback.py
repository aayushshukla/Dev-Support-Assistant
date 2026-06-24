from fastapi import APIRouter

from backend.dbops.pgvectore_store import (
    connection,
    cursor
)

router = APIRouter()


@router.post("/feedback")
def save_feedback(data: dict):

    try:

        print("\n========== FEEDBACK RECEIVED ==========")
        print(data)

        cursor.execute(
            """
            INSERT INTO feedback (

                query,
                answer,
                agent,
                feedback

            )

            VALUES (%s, %s, %s, %s)
            """,

            (

                data["query"],
                data["answer"],
                data["agent"],
                data["feedback"]
            )
        )

        connection.commit()

        print("Feedback saved successfully.")

        return {
            "status": "success"
        }

    except Exception as e:

        print("Feedback Error:", str(e))

        return {
            "status": "failed",
            "error": str(e)
        }