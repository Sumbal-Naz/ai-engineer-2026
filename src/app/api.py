from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.app.database import get_db
from src.app.services import create_ai_model, get_ai_models
from src.app.models import AIModel
from src.app.schemas import AIModelResponse, AIModelRequest

app = FastAPI()

@app.post("/model", response_model=AIModelResponse)
def create_model(
    model_data: AIModelRequest,
    db: Session = Depends(get_db)
):
    return create_ai_model(
        db,
        model_data.name,
        model_data.provider
    )

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


@app.get("/models")
def list_models(
    db: Session = Depends(get_db)
):
    return get_ai_models(db)
