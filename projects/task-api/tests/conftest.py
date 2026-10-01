import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.task_service import reset_tasks


@pytest.fixture
def client():
    """Provide a FastAPI test client."""

    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_task_storage():
    """Reset task storage before each test."""

    reset_tasks()
