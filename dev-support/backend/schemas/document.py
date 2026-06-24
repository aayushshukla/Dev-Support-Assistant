"""
Common document model used by all loaders.
"""

from pydantic import BaseModel


class DocumentSchema(BaseModel):
    title: str
    content: str
    source: str
    document_type: str