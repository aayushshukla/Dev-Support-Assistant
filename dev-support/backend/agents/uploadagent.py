
# backend/services/upload_service.py

import logging
import traceback

from backend.ingestions.upload_ingestion import (
    ingest_file
)

logger = logging.getLogger(__name__)


def process_upload(file_path):

    logger.info(
        f"Processing upload: {file_path}"
    )

    try:

        result = ingest_file(
            file_path
        )

        # ==========================================
        # DUPLICATE FILE
        # ==========================================

        if (

            result.get(
                "duplicate_documents",
                0
            ) > 0

            and

            result.get(
                "documents_processed",
                0
            ) == 0

        ):

            logger.warning(
                "Duplicate file detected"
            )

            return {

                "status":
                    "duplicate",

                "message":
                    "File already exists in the system.",

                "documents_processed":
                    result.get(
                        "documents_processed",
                        0
                    ),

                "chunks_created":
                    result.get(
                        "chunks_created",
                        0
                    ),

                "duplicate_documents":
                    result.get(
                        "duplicate_documents",
                        0
                    ),

                "duplicate_files":
                    result.get(
                        "duplicate_files",
                        []
                    )
            }

        # ==========================================
        # SUCCESS
        # ==========================================

        logger.info(
            "Upload completed successfully"
        )

        return {

            "status":
                "success",

            "message":
                "File processed successfully.",

            **result
        }

    except Exception as e:

        logger.exception(
            "Upload failed"
        )

        return {

            "status":
                "failed",

            "message":
                "File ingestion failed.",

            "error":
                str(e),

            "traceback":
                traceback.format_exc()
        }

