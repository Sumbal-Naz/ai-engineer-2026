from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for data required to create a task."""

    title: str = Field(min_length=1)
    description: str | None = None
    completed: bool = False


class TaskResponse(BaseModel):
    """Schema returned when a task is created."""

    id: int
    title: str
    description: str | None
    completed: bool


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: str = Field(min_length=1)
    description: str | None = None
    completed: bool = False
