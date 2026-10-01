from app.schemas import TaskCreate, TaskResponse, TaskUpdate

# In-memory task storage.
tasks: dict[int, TaskResponse] = {}

# Simple ID counter for this exercise.
_next_task_id = 1


def create_task(task: TaskCreate) -> TaskResponse:
    """Create and store a new task."""

    global _next_task_id

    new_task = TaskResponse(
        id=_next_task_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
    )

    tasks[_next_task_id] = new_task
    _next_task_id += 1

    return new_task


def get_all_tasks() -> list[TaskResponse]:
    """Return all stored tasks."""

    return list(tasks.values())


def get_task(task_id: int) -> TaskResponse:
    """Return a task by ID."""

    if task_id not in tasks:
        raise KeyError(task_id)

    return tasks[task_id]


def reset_tasks() -> None:
    """Reset in-memory task storage for testing."""

    global _next_task_id

    tasks.clear()
    _next_task_id = 1


def update_task(task_id: int, task: TaskUpdate) -> TaskResponse:
    """Update an existing task."""

    if task_id not in tasks:
        raise KeyError(task_id)

    updated_task = TaskResponse(
        id=task_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
    )

    tasks[task_id] = updated_task

    return updated_task


def delete_task(task_id: int) -> None:
    """Delete an existing task."""

    if task_id not in tasks:
        raise KeyError(task_id)

    del tasks[task_id]
