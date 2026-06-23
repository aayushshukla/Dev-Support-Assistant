from pydantic import BaseModel


class AgentResponse(BaseModel):

    answer: str

    citations: list

    query_stats: dict