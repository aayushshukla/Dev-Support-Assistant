from backend.ingestions.upload_ingestion import (
    ingest_file
)


def process_upload(file_path):

    try:

        result = ingest_file(
            file_path
        )

        if result.get(
            "duplicate_documents",
            0
        ) > 0 and result.get(
            "documents_processed",
            0
        ) == 0:

            return {

                "status":
                "duplicate",

                **result
            }

        return {

            "status":
            "success",

            **result
        }

    except Exception as e:

        return {

            "status":
            "failed",

            "error":
            str(e)
        }