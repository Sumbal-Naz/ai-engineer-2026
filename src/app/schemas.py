# Import Pydantic tools:
# BaseModel: Base class for creating data validation models.
# Field: Adds validation rules and metadata to fields.
# computed_field: Includes a calculated property in the model output.
# field_validator: Creates custom validation functions for fields.
from pydantic import BaseModel, Field, computed_field, field_validator


# Schema used when creating a new AI model.
# This validates data received from the client.
class AIModelRequest(BaseModel):
    # The model name must contain at least 2 characters.
    name: str = Field(min_length=2)

    # The provider name must contain at least 2 characters.
    provider: str = Field(min_length=2)

    # Apply this validator to both the "name" and "provider" fields.
    @field_validator("name", "provider")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        # Remove spaces from the beginning and end of the value.
        value = value.strip()

        # Reject values that become empty after removing whitespace.
        if not value:
            raise ValueError("Value cannot be empty")

        # Return the cleaned and validated value.
        return value


# Schema used when sending AI model data back to the client.
class AIModelResponse(BaseModel):
    # Unique database ID of the AI model.
    id: int

    # Name of the AI model.
    name: str

    # Provider of the AI model.
    provider: str

    # Allow Pydantic to create this schema directly from
    # SQLAlchemy ORM model objects and their attributes.
    model_config = {"from_attributes": True}

    # Create an additional field whose value is calculated automatically.
    @computed_field  # type: ignore[prop-decorator]
    @property
    def description(self) -> str:
        # Return a human-readable description of the AI model.
        return f"{self.name} is provided by {self.provider}."


# Schema used when updating an existing AI model.
class AIModelUpdate(BaseModel):
    # Updated model name must contain at least 2 characters.
    name: str = Field(min_length=2)

    # Updated provider name must contain at least 2 characters.
    provider: str = Field(min_length=2)

    # Validate and clean both fields before accepting the update.
    @field_validator("name", "provider")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        # Remove leading and trailing whitespace.
        value = value.strip()

        # Reject empty values after whitespace is removed.
        if not value:
            raise ValueError("Value cannot be empty")

        # Return the cleaned value.
        return value


# Schema used when identifying an AI model to delete.
class AIModelDelete(BaseModel):
    # ID of the AI model that should be deleted.
    id: int


class ErrorResponse(BaseModel):
    # A machine-readable error code.
    error: str

    # A human-readable explanation of the error.
    message: str


class UserCreate(BaseModel):
    """
    Data required to create a new user.
    """

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)


class Token(BaseModel):
    """
    JWT access token returned after successful login.
    """

    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    role: str

    model_config = {"from_attributes": True}
