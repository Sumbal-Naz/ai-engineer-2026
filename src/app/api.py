from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.database import get_db
from src.app.models import AIModel

from src.app.schemas import (
    AIModelResponse,
    AIModelRequest,
    AIModelUpdate)

from src.app.services import (
    create_ai_model,
    get_ai_models,
    get_model_by_id,
    update_ai_model)

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
        "id": 0,
        "name": model.name,
        "provider": model.provider,
        "description": model.describe()
    }


@app.get("/models")
def list_models(
    db: Session = Depends(get_db)
):
    return get_ai_models(db)

@app.get("/model/{model_id}", response_model=AIModelResponse)
def get_model_by_id_endpoint(
    model_id: int,
    db: Session = Depends(get_db)
):
    model = get_model_by_id(db, model_id)

    if model is None:
        raise HTTPException(
            status_code=404,
            detail="Model not found"
        )

    return model

@app.put("/model/{model_id}", response_model=AIModelResponse)
def update_model(
    model_id: int,
    model_data: AIModelUpdate,
    db: Session = Depends(get_db)
):
    model = update_ai_model(
        db,
        model_id,
        model_data.name,
        model_data.provider
    )

    if model is None:
        raise HTTPException(
            status_code=404,
            detail="Model not found"
        )

    return model