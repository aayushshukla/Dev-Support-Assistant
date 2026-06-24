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

        query=request.query,

        chat_history=request.chat_history,

        model_name=request.model_name

    )