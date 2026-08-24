from pydantic import BaseModel, Field, computed_field, field_validator


class AIModelRequest(BaseModel):
    name: str = Field(min_length=2)
    provider: str = Field(min_length=2)

    @field_validator("name", "provider")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty")
        return value


class AIModelResponse(BaseModel):
    id: int
    name: str
    provider: str

    model_config = {
        "from_attributes": True
    }

    @computed_field
    @property
    def description(self) -> str:
        return f"{self.name} is provided by {self.provider}."

class AIModelUpdate(BaseModel):
    name: str = Field(min_length=2)
    provider: str = Field(min_length=2)

    @field_validator("name", "provider")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty")

        return value

class AIModelDelete(BaseModel):
    id: int


