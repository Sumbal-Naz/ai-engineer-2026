def test_create_task(client):
    """Test that a new task can be created."""

    response = client.post(
        "/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Build a REST API",
            "completed": False,
        },
    )

    assert response.status_code == 201

    assert response.json() == {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "Build a REST API",
        "completed": False,
    }


def test_get_all_tasks(client):
    """Test that all tasks are returned."""

    client.post(
        "/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Build a REST API",
            "completed": False,
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Test the task API",
            "completed": True,
        },
    )

    response = client.get("/tasks")

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": 1,
            "title": "Learn FastAPI",
            "description": "Build a REST API",
            "completed": False,
        },
        {
            "id": 2,
            "title": "Write tests",
            "description": "Test the task API",
            "completed": True,
        },
    ]


def test_get_task_by_id(client):
    """Test that an existing task can be retrieved by ID."""

    client.post(
        "/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Build a REST API",
            "completed": False,
        },
    )

    response = client.get("/tasks/1")

    assert response.status_code == 200

    assert response.json() == {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "Build a REST API",
        "completed": False,
    }


def test_get_task_by_id_not_found(client):
    """Test that requesting a missing task returns 404."""

    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found",
    }


def test_update_task(client):
    """Test that an existing task can be updated."""

    client.post(
        "/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Build a REST API",
            "completed": False,
        },
    )

    response = client.put(
        "/tasks/1",
        json={
            "title": "Master FastAPI",
            "description": "Build and test a REST API",
            "completed": True,
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": 1,
        "title": "Master FastAPI",
        "description": "Build and test a REST API",
        "completed": True,
    }


def test_update_task_not_found(client):
    """Test that updating a missing task returns 404."""

    response = client.put(
        "/tasks/999",
        json={
            "title": "Missing task",
            "description": "This task does not exist",
            "completed": False,
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Task not found",
    }


def test_delete_task(client):
    """Test that an existing task can be deleted."""

    client.post(
        "/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Build a REST API",
            "completed": False,
        },
    )

    response = client.delete("/tasks/1")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get("/tasks/1")

    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """Test that deleting a missing task returns 404."""

    response = client.delete("/tasks/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Task not found",
    }
