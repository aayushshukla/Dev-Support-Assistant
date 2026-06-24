"""
JSON Loader
"""

import json
from pathlib import Path

from backend.schemas.document import DocumentSchema


class JSONLoader:

    @staticmethod
    def load(file_path: str) -> DocumentSchema:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        content = json.dumps(
            data,
            indent=2
        )

        return DocumentSchema(
            title=Path(file_path).stem,
            content=content,
            source=file_path,
            document_type="json"
        )