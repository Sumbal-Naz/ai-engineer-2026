from fastapi import APIRouter, HTTPException, status

from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task,
    update_task,
)

router = APIRouter()


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_endpoint(task: TaskCreate) -> TaskResponse:
    """Create a new task."""

    return create_task(task)


@router.get(
    "/tasks",
    response_model=list[TaskResponse],
)
def get_tasks() -> list[TaskResponse]:
    """Return all tasks."""

    return get_all_tasks()


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
def get_task_by_id(task_id: int) -> TaskResponse:
    """Return a task by ID."""

    try:
        return get_task(task_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        ) from None


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
def update_task_by_id(
    task_id: int,
    task: TaskUpdate,
) -> TaskResponse:
    """Update an existing task."""

    try:
        return update_task(task_id, task)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        ) from None


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_by_id(task_id: int) -> None:
    """Delete an existing task."""

    try:
        delete_task(task_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        ) from None
