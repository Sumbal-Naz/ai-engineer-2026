from fastapi.testclient import TestClient

from src.app.api import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Engineer 2026 API"
    }

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }

def test_get_model():
    response = client.get("/model")
    assert response.status_code == 200
    data =  response.json()

    assert data["name"] == "GPT"
    assert data["provider"] == "OpenAI"
    assert data["description"] == "GPT is provided by OpenAI."

def test_update_model():
    # Create a model
    create_response = client.post(
        "/model",
        json={
            "name": "Test Model",
            "provider": "Test Provider"
        }
    )

    assert create_response.status_code == 200

    created_model = create_response.json()
    model_id = created_model["id"]

    # Update the model
    response = client.put(
        f"/model/{model_id}",
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

    # Read the model again from the API
    get_response = client.get(f"/model/{model_id}")

    assert get_response.status_code == 200

    saved_model = get_response.json()

    assert saved_model["id"] == model_id
    assert saved_model["name"] == "Updated Model"
    assert saved_model["provider"] == "OpenAI"

def test_update_model_not_found():
    response = client.put(
        "/model/999999",
        json={
            "name": "Updated Model",
            "provider": "OpenAI"
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Model not found"
    }

def test_delete_model():
    # Create a model first
    create_response = client.post(
        "/model",
        json={
            "name": "Test Model",
            "provider": "Test Provider"
        }
    )

    assert create_response.status_code == 200

    model_id = create_response.json()["id"]

    # Delete the model
    response = client.delete(f"/model/{model_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": model_id
    }

    # Verify that the model is actually gone
    get_response = client.get(f"/model/{model_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Model not found"
    }

def test_delete_model_not_found():
    response = client.delete("/model/99999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Model not found"
    }
