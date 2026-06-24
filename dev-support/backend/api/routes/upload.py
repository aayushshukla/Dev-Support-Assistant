import os

from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from backend.agents.uploadagent import (
    process_upload
)

router = APIRouter()

UPLOAD_DIR = "backend/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

ALLOWED_EXTENSIONS = {
    ".csv",
    ".pdf",
    ".md",
    ".markdown"
}


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:

        return {

            "status":
            "failed",

            "error":
            "Filename missing"
        }

    extension = (
        Path(file.filename)
        .suffix
        .lower()
    )

    if extension not in ALLOWED_EXTENSIONS:

        return {

            "status":
            "failed",

            "error":
            f"Unsupported file type: "
            f"{extension}"
        }

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    result = process_upload(
        file_path
    )

    return {

        "filename":
        file.filename,

        **result
    }