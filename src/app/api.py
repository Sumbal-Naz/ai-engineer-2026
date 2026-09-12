# Import FastAPI tools:
# FastAPI creates the API application
# Depends handles dependency injection
# HTTPException returns HTTP errors such as 404
# status provides named HTTP status codes such as HTTP_201_CREATED
from fastapi import FastAPI, Depends, HTTPException, status, Header, Query, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from typing import Literal

import jwt

# Import application settings from config.py
from src.app.config import settings

# Import SQLAlchemy Session for database operations
from sqlalchemy.orm import Session

# Import the database dependency that provides a database session
from src.app.database import get_db

# Import the database user model.
from src.app.models import UserDB

# Import password verification and JWT token creation functions.
from src.app.auth import verify_password, create_access_token

# Import Pydantic schemas used for request validation and API responses
from src.app.schemas import (
    UserCreate,
    UserResponse,
    Token
)

from src.app.schemas import (
    AIModelResponse,  # Schema for returning an AI model
    AIModelRequest,   # Schema for creating an AI model
    AIModelUpdate,    # Schema for updating an AI model
    AIModelDelete,    # Schema for returning deleted model information
    ErrorResponse
)

from src.app.services import (
    create_user
)

# Import service functions that contain the database/business logic
from src.app.services import (
    create_ai_model,  # Create a new AI model
    get_ai_models,    # Get all AI models
    get_model_by_id,  # Get one AI model by ID
    get_required_model,
    update_ai_model,  # Update an existing AI model
    delete_ai_model   # Delete an AI model
)

from src.app.exceptions import (
    ModelNotFoundError,
    DuplicateModelError
)


# Create the FastAPI application
# The application name and debug setting come from config.py
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

@app.exception_handler(ModelNotFoundError)
async def model_not_found_handler(
    request: Request,
    exc: ModelNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "MODEL_NOT_FOUND",
            "message": str(exc)
        }
    )


@app.exception_handler(DuplicateModelError)
async def duplicate_model_handler(
    request: Request,
    exc: DuplicateModelError
):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "DUPLICATE_MODEL",
            "message": str(exc)
        }
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

# Authentication section #

@app.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(
        db=db,
        username=user.username,
        password=user.password
    )

@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(UserDB)
        .filter(UserDB.username == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        user_id=user.id,
        username=user.username
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserDB:
    """
    Verify the JWT access token and return the authenticated user.
    """

    try:
        # Decode and verify the JWT signature.
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )

    # Get the user's ID from the JWT subject claim.
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )

    # Find the user in the database.
    user = (
        db.query(UserDB)
        .filter(UserDB.id == int(user_id))
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    # Make sure the account is still active.
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    return user

def require_admin(
    current_user: UserDB = Depends(get_current_user)
) -> UserDB:
    """
    Allow access only to authenticated users with the admin role.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user

@app.get("/admin-only")
def admin_only(
    current_user: UserDB = Depends(require_admin)
):
    """
    Test endpoint accessible only to administrators.
    """

    return {
        "message": "Welcome, admin!",
        "username": current_user.username,
        "role": current_user.role
    }


# model section #

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
    db: Session = Depends(get_db),

    current_user: UserDB = Depends(get_current_user)
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
    db: Session = Depends(get_db),

    current_user: UserDB = Depends(get_current_user)
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
    db: Session = Depends(get_db),

    current_user: UserDB = Depends(get_current_user)
):
    return get_required_model(db, model_id)


# Update an existing AI model
# PUT /models/{model_id}
@app.put(
    "/models/{model_id}",
    response_model=AIModelResponse
)
def update_model(
    model_id: int,
    model_data: AIModelUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):

    return update_ai_model(
        db,
        model_id,
        model_data.name,
        model_data.provider
    )


# Delete an AI model
# DELETE /models/{model_id}
@app.delete(
    "/models/{model_id}",
    response_model=AIModelDelete
)
def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):

    return delete_ai_model(
        db,
        model_id
    )


