# Import FastAPI tools:
# FastAPI creates the API application
# Depends handles dependency injection
# HTTPException returns HTTP errors such as 404
# status provides named HTTP status codes such as HTTP_201_CREATED
from fastapi import FastAPI, Depends, HTTPException, status, Header, Query
from typing import Literal

# Import application settings from config.py
from src.app.config import settings

# Import SQLAlchemy Session for database operations
from sqlalchemy.orm import Session

# Import the database dependency that provides a database session
from src.app.database import get_db

# Import Pydantic schemas used for request validation and API responses
from src.app.schemas import (
    AIModelResponse,  # Schema for returning an AI model
    AIModelRequest,   # Schema for creating an AI model
    AIModelUpdate,    # Schema for updating an AI model
    AIModelDelete     # Schema for returning deleted model information
)


# Import service functions that contain the database/business logic
from src.app.services import (
    create_ai_model,  # Create a new AI model
    get_ai_models,    # Get all AI models
    get_model_by_id,  # Get one AI model by ID
    update_ai_model,  # Update an existing AI model
    delete_ai_model   # Delete an AI model
)


# Create the FastAPI application
# The application name and debug setting come from config.py
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

def verify_api_key(
    x_api_key: str | None = Header(default=None)
):
    # Check whether the API key is correct.
    if x_api_key != "my-secret-key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

    # Return a value when the API key is valid.
    return x_api_key

# Root endpoint
# GET / returns a basic message showing that the API is running
@app.get("/")
def root():
    return {
        "message": "AI Engineer 2026 API"
    }


# Health-check endpoint
# GET /health returns the health status of the API
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# Get all AI models
# GET /models reads all models from the database
# response_model ensures every returned model follows AIModelResponse
@app.get("/models", response_model=list[AIModelResponse])
def list_models(
    # Number of models to skip
    skip: int = Query(default=0, ge=0),

    # Maximum number of models to return
    limit: int = Query(default=10, ge=1, le=100),

    # Optional provider filter.
    provider: str | None = Query(default=None),

    # Column used for sorting.
    sort_by: Literal["id", "name", "provider"] = Query(default="id"),

    # Sorting direction.
    order: Literal["asc", "desc"] = Query(default="asc"),

    # Database session
    db: Session = Depends(get_db)
):
    # Get models using pagination
    return get_ai_models(
        db,
        skip=skip,
        limit=limit,
        provider=provider,
        sort_by=sort_by,
        order=order
    )

@app.get("/protected")
def protected_route(
    api_key: str = Depends(verify_api_key)
):
    return {
        "message": "You have access to the protected endpoint"
    }

# Create a new AI model
# POST /models receives model data and saves a new model
# Returns 201 Created when successful
@app.post(
    "/models",
    response_model=AIModelResponse,
    status_code=status.HTTP_201_CREATED
)
def create_model(
    # FastAPI validates incoming JSON using AIModelRequest
    model_data: AIModelRequest,

    # Get a database session for this request
    db: Session = Depends(get_db)
):
    # Pass the validated data to the service function
    return create_ai_model(
        db,
        model_data.name,
        model_data.provider
    )


# Get one AI model by its ID
# GET /models/{model_id}
@app.get(
    "/models/{model_id}",
    response_model=AIModelResponse
)
def get_model_by_id_endpoint(
    # Get model_id from the URL path
    model_id: int,

    # Get a database session for this request
    db: Session = Depends(get_db)
):
    # Ask the service layer to find the model
    model = get_model_by_id(db, model_id)

    # If no model exists with this ID, return HTTP 404 Not Found
    if model is None:
        raise HTTPException(
            status_code=404,
            detail="Model not found"
        )

    # Return the model when it exists
    return model


# Update an existing AI model
# PUT /models/{model_id}
@app.put(
    "/models/{model_id}",
    response_model=AIModelResponse
)
def update_model(
    # Get model_id from the URL path
    model_id: int,

    # Validate the new data sent by the client
    model_data: AIModelUpdate,

    # Get a database session for this request
    db: Session = Depends(get_db)
):
    # Call the service layer to update the model
    model = update_ai_model(
        db,
        model_id,
        model_data.name,
        model_data.provider
    )

    # If the model does not exist, return HTTP 404 Not Found
    if model is None:
        raise HTTPException(
            status_code=404,
            detail="Model not found"
        )

    # Return the updated model
    return model


# Delete an AI model
# DELETE /models/{model_id}
@app.delete(
    "/models/{model_id}",
    response_model=AIModelDelete
)
def delete_model(
    # Get model_id from the URL path
    model_id: int,

    # Get a database session for this request
    db: Session = Depends(get_db)
):
    # Call the service layer to delete the model
    model = delete_ai_model(
        db,
        model_id
    )

    # If the model does not exist, return HTTP 404 Not Found
    if model is None:
        raise HTTPException(
            status_code=404,
            detail="Model not found"
        )

    # Return information about the deleted model
    return model