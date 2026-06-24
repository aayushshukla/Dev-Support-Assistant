from pydantic import BaseModel
from typing import List, Dict

class QuestionRequest(BaseModel):

    query: str
    chat_history: List[Dict] = []
    model_name: str = "gpt-4o-mini"


class IndexRequest(BaseModel):

    filename: str