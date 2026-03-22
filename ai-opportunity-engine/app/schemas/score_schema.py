from pydantic import BaseModel


class ScoreResponse(BaseModel):
    product: str
    score: int
