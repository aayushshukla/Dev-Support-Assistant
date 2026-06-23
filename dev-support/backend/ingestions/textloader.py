"""
TXT Loader
"""

from pathlib import Path

from backend.schemas.document import DocumentSchema


class TXTLoader:

    @staticmethod
    def load(file_path: str) -> DocumentSchema:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        return DocumentSchema(
            title=Path(file_path).stem,
            content=content,
            source=file_path,
            document_type="txt"
        )