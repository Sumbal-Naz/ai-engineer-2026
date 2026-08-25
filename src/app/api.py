from fastapi import FastAPI, Depends, HTTPException, status
from src.app.config import settings
from sqlalchemy.orm import Session

from src.app.database import get_db

from src.app.schemas import (
    AIModelResponse,
    AIModelRequest,
    AIModelUpdate,
    AIModelDelete)

from src.app.services import (
    create_ai_model,
    get_ai_models,
    get_model_by_id,
    update_ai_model,
    delete_ai_model)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

# read sample 1
@app.get("/")
def root():
    return {
        "message": "AI Engineer 2026 API"
    }

# read sample 2
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# read data sample 1
@app.get("/models")
def list_models(
    db: Session = Depends(get_db)
):
    return get_ai_models(db)

# add data
@app.post("/models", response_model=AIModelResponse, status_code=status.HTTP_201_CREATED)
def create_model(
    model_data: AIModelRequest,
    db: Session = Depends(get_db)
):
    return create_ai_model(
        db,
        model_data.name,
        model_data.provider
    )

@app.get("/models/{model_id}", response_model=AIModelResponse)
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

# update/add data
@app.put("/models/{model_id}", response_model=AIModelResponse)
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

@app.delete("/models/{model_id}", response_model=AIModelDelete)
def delete_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    model = delete_ai_model(
        db,
        model_id
    )
    if model is None:
        raise HTTPException(
            status_code=404,
            detail="Model not found"
        )
        
    return model

