from unittest.mock import patch
from src.app.api import app, get_current_user
from src.app.models import UserDB

def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Engineer 2026 API"
    }


# Test that the health endpoint returns a healthy status
def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


# Test that the health endpoint returns JSON
def test_health_response_headers(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/json"
    )


# Test that GET /models returns a list of models
def test_list_models(auth_client):
    response = auth_client.get("/models")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# Test that GET /models/{id} returns 404 when the model does not exist
def test_get_model_not_found(auth_client):
    # Request a model that does not exist.
    response = auth_client.get("/models/999999")

    # The API should return 404 Not Found.
    assert response.status_code == 404

    # Check the consistent error response.
    assert response.json() == {
        "error": "MODEL_NOT_FOUND",
        "message": "Model with ID 999999 not found"
    }

# Test that an existing model can be updated
def test_update_model(auth_client):
    # Create a model first
    create_response = auth_client.post(
        "/models",
        json={
            "name": "Update Test Model",
            "provider": "Test Provider"
        }
    )

    assert create_response.status_code == 201

    created_model = create_response.json()
    model_id = created_model["id"]

    # Update the model
    response = auth_client.put(
        f"/models/{model_id}",
        json={
            "name": "Updated Model",
            "provider": "OpenAI"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == model_id
    assert data["name"] == "Updated Model"
    assert data["provider"] == "OpenAI"
    assert data["description"] == "Updated Model is provided by OpenAI."

    # Read the model again to confirm the update was saved
    get_response = auth_client.get(f"/models/{model_id}")

    assert get_response.status_code == 200

    saved_model = get_response.json()

    assert saved_model["id"] == model_id
    assert saved_model["name"] == "Updated Model"
    assert saved_model["provider"] == "OpenAI"


# Test that POST /models creates a new model and returns 201 Created
def test_create_model_returns_201(auth_client):
    response = auth_client.post(
        "/models",
        json={
            "name": "HTTP Test Model 2026",
            "provider": "OpenAI"
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "HTTP Test Model 2026"
    assert data["provider"] == "OpenAI"

def test_create_duplicate_model(auth_client):
    # Create the first model.
    first_response = auth_client.post(
        "/models",
        json={
            "name": "Unique Duplicate Test Model",
            "provider": "OpenAI"
        }
    )

    # The first creation should succeed.
    assert first_response.status_code == 201

    # Try to create the same model again.
    second_response = auth_client.post(
        "/models",
        json={
            "name": "Unique Duplicate Test Model",
            "provider": "OpenAI"
        }
    )

    # A duplicate should return 409 Conflict.
    assert second_response.status_code == 409

    # Check the consistent error response.
    assert second_response.json() == {
        "error": "DUPLICATE_MODEL",
        "message": "Model 'Unique Duplicate Test Model' already exists"
    }

# Test that updating a non-existent model returns 404
def test_update_model_not_found(auth_client):
    # Try to update a model that does not exist.
    response = auth_client.put(
        "/models/999999",
        json={
            "name": "Updated Model",
            "provider": "OpenAI"
        }
    )

    # The API should return 404 Not Found.
    assert response.status_code == 404

    # Check the consistent error response.
    assert response.json() == {
        "error": "MODEL_NOT_FOUND",
        "message": "Model with ID 999999 not found"
    }


# Test that an existing model can be deleted
def test_delete_model(auth_client):
    # Create a model first
    create_response = auth_client.post(
        "/models",
        json={
            "name": "Delete Test Model",
            "provider": "Test Provider"
        }
    )

    assert create_response.status_code == 201

    model_id = create_response.json()["id"]

    # Delete the model
    response = auth_client.delete(f"/models/{model_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": model_id
    }

    # Verify that the model is actually gone
    get_response = auth_client.get(f"/models/{model_id}")

    assert get_response.status_code == 404

    assert get_response.json() == {
        "error": "MODEL_NOT_FOUND",
        "message": f"Model with ID {model_id} not found"
    }


# Test that deleting a non-existent model returns 404
def test_delete_model_not_found(auth_client):
    # Try to delete a model that does not exist.
    response = auth_client.delete("/models/99999")

    # The API should return 404 Not Found.
    assert response.status_code == 404

    # Check the consistent error response.
    assert response.json() == {
        "error": "MODEL_NOT_FOUND",
        "message": "Model with ID 99999 not found"
    }


# Test that creating a model with an empty name returns 422
def test_create_model_invalid_name(auth_client):
    response = auth_client.post(
        "/models",
        json={
            "name": "",
            "provider": "OpenAI"
        }
    )

    assert response.status_code == 422


# Test that creating a model with an empty provider returns 422
def test_create_model_invalid_provider(auth_client):
    response = auth_client.post(
        "/models",
        json={
            "name": "GPT",
            "provider": ""
        }
    )

    assert response.status_code == 422


# Test that creating a model without the required provider field returns 422
def test_create_model_missing_provider(auth_client):
    response = auth_client.post(
        "/models",
        json={
            "name": "GPT"
        }
    )

    assert response.status_code == 422


# Test that updating a model with an empty name returns 422
def test_update_model_invalid_name(auth_client):
    response = auth_client.put(
        "/models/1",
        json={
            "name": "",
            "provider": "OpenAI"
        }
    )

    assert response.status_code == 422


# Test that updating a model with an empty provider returns 422
def test_update_model_invalid_provider(auth_client):
    response = auth_client.put(
        "/models/1",
        json={
            "name": "GPT",
            "provider": ""
        }
    )

    assert response.status_code == 422

def test_protected_route_without_token(client):
    """
    Verify that the protected endpoint rejects
    requests that do not contain a JWT token.
    """

    # Send a request without an Authorization header.
    response = client.get("/protected")

    # The request should be rejected because no JWT was provided.
    assert response.status_code == 401

    # Check the authentication error returned by get_current_user.
    assert response.json()["detail"] == "Not authenticated"

def test_protected_route_with_valid_token(auth_client):
    """
    Verify that an authenticated user can access the protected endpoint.
    """

    # auth_client already contains a valid JWT token.
    response = auth_client.get("/protected")

    # The authenticated request should succeed.
    assert response.status_code == 200

    # Check the success message returned by the protected endpoint.
    assert response.json()["message"] == (
        "You have access to the protected endpoint"
    )

def test_list_models_with_limit(auth_client):
    # Request the models endpoint with a maximum of 2 models.
    response = auth_client.get(
        "/models?limit=2"
    )

    # The request should succeed.
    assert response.status_code == 200

    # The API should never return more than 2 models.
    assert len(response.json()) <= 2

def test_list_models_filter_by_provider(auth_client):
    # Request only models provided by OpenAI.
    response = auth_client.get(
        "/models?provider=OpenAI",
        headers={"X-API-Key": "my-secret-key"}
    )

    # The request should succeed.
    assert response.status_code == 200

    # Every returned model should have OpenAI as its provider.
    for model in response.json():
        assert model["provider"] == "OpenAI"

def test_list_models_sort_by_name_ascending(auth_client):
    # Request models sorted by name in ascending order.
    response = auth_client.get(
        "/models?sort_by=name&order=asc",
        headers={"X-API-Key": "my-secret-key"}
    )

    # The request should succeed.
    assert response.status_code == 200

    # Get the models from the response.
    models = response.json()

    # Extract only the model names.
    names = [model["name"] for model in models]

    # Check that the names are in ascending order.
    assert names == sorted(names)

def test_list_models_sort_by_name_descending(auth_client):
    # Request models sorted by name in descending order.
    response = auth_client.get(
        "/models?sort_by=name&order=desc",
        headers={"X-API-Key": "my-secret-key"}
    )

    # The request should succeed.
    assert response.status_code == 200

    # Get the models from the response.
    models = response.json()

    # Extract only the model names.
    names = [model["name"] for model in models]

    # Check that the names are in descending order.
    assert names == sorted(names, reverse=True)

def test_list_models_invalid_sort_by(auth_client):
    # Send an invalid sorting field.
    response = auth_client.get(
        "/models?sort_by=banana",
        headers={"X-API-Key": "my-secret-key"}
    )

    # FastAPI should reject the invalid value.
    assert response.status_code == 422

def test_list_models_invalid_order(auth_client):
    # Send an invalid sorting order.
    response = auth_client.get(
        "/models?order=random",
        headers={"X-API-Key": "my-secret-key"}
    )

    # FastAPI should reject the invalid value.
    assert response.status_code == 422

def test_list_models_filter_sort_and_paginate(auth_client):
    # Request OpenAI models, sort them by name descending,
    # and return a maximum of 2 models.
    response = auth_client.get(
        "/models?provider=OpenAI&sort_by=name&order=desc&skip=0&limit=2",
        headers={"X-API-Key": "my-secret-key"}
    )

    # The request should succeed.
    assert response.status_code == 200

    # Get the models from the response.
    models = response.json()

    # Pagination: no more than 2 models should be returned.
    assert len(models) <= 2

    # Filtering: every returned model must be from OpenAI.
    for model in models:
        assert model["provider"] == "OpenAI"

    # Sorting: names must be in descending order.
    names = [model["name"] for model in models]
    assert names == sorted(names, reverse=True)

def test_ai_endpoint(client):
    response = client.get(
        "/ai",
        params={"prompt": "Hello"}
    )

    assert response.status_code == 200

    assert response.json() == {
        "prompt": "Hello",
        "answer": "Real AI response for: Hello"
    }

def test_ai_endpoint_with_mock(client):
    with patch("src.app.api.generate_answer") as mock_generate:

        mock_generate.return_value = "Mocked AI response"

        response = client.get(
            "/ai",
            params={"prompt": "Hello"}
        )

        assert response.status_code == 200

        assert response.json() == {
            "prompt": "Hello",
            "answer": "Mocked AI response"
        }

        mock_generate.assert_called_once_with("Hello")

def override_admin_user():
    """
    Return a fake authenticated admin user.

    This returns a UserDB object because the
    /admin endpoint expects current_user.role.
    """

    return UserDB(
        id=1,
        username="test_admin",
        password_hash="fake_hash",
        is_active=True,
        role="admin"
    )

def test_protected_endpoint_as_admin(client):
    app.dependency_overrides[
    get_current_user
    ] = override_admin_user

    try:
        response = client.get("/protected")

        assert response.status_code == 200

    finally:
        app.dependency_overrides.clear()

def override_normal_user():
    """
    Return a fake authenticated normal user.

    We don't need a real password because the test
    bypasses the JWT authentication dependency.
    """

    return UserDB(
        id=2,
        username="test_user",
        password_hash="fake_hash",
        is_active=True,
        role="user"
    )

def test_admin_endpoint_as_normal_user(normal_user_client):

    response = normal_user_client.get("/admin")

    assert response.status_code == 403

    assert response.json() == {
        "detail": "Admin access required"
    }

def test_admin_endpoint_as_admin(admin_client):

    response = admin_client.get("/admin")

    assert response.status_code == 200

    assert response.json() == {
        "message": "You have admin access"
    }

def test_ai_endpoint_service_failure(client):
    """
    Verify that an AI service failure is handled
    with a proper HTTP 500 response.
    """

    with patch("src.app.api.generate_answer") as mock_generate:

        mock_generate.side_effect = Exception(
            "AI service unavailable"
        )

        response = client.get(
            "/ai",
            params={"prompt": "Hello"}
        )

        assert response.status_code == 500

        assert response.json() == {
            "detail": "AI service unavailable"
        }