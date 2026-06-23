from fastapi import APIRouter

from backend.api.models.request_model import (
    IndexRequest
)

router = APIRouter()


@router.post("/index")
def index_document(

    request: IndexRequest
):

    return {

        "message":
        "Indexing triggered",

        "filename":
        request.filename
    }