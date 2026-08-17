from fastapi import FastAPI

from src.app.models import AIModel
from src.app.schemas import AIModelResponse, AIModelRequest

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "AI Engineer 2026 API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/model", response_model=AIModelResponse)
def get_model():
    model = AIModel(
        name="GPT",
        provider="OpenAI"
    )

    return {
        "name": model.name,
        "provider": model.provider,
        "description": model.describe()
    }

@app.post("/model", response_model=AIModelResponse)
def create_model(model_data: AIModelRequest):
    model = AIModel(
        name=model_data.name,
        provider=model_data.provider
    )

    return {
        "name": model.name,
        "provider": model.provider,
        "description": model.describe()
    }
