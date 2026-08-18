from pydantic import BaseModel, computed_field


class AIModelRequest(BaseModel):
    name: str
    provider: str


class AIModelResponse(BaseModel):
    name: str
    provider: str

    model_config = {
        "from_attributes": True
    }

    @computed_field
    @property
    def description(self) -> str:
        return f"{self.name} is provided by {self.provider}."
