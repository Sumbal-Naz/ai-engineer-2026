from pydantic import BaseModel


class AIModelRequest(BaseModel):
    name: str
    provider: str


class AIModelResponse(BaseModel):
    name: str
    provider: str
    description: str