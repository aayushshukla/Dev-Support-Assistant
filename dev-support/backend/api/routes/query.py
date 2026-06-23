from fastapi import APIRouter

from backend.api.models.request_model import (
    QuestionRequest
)

from backend.agents.supervisior import (
    process_query
)

router = APIRouter()


@router.post("/ask")
def ask_question(
    request: QuestionRequest
):

    return process_query(
        request.query
    )