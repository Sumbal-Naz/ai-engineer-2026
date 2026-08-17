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