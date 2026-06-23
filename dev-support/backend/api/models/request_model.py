from pydantic import BaseModel


class QuestionRequest(BaseModel):

    query: str


class IndexRequest(BaseModel):

    filename: str