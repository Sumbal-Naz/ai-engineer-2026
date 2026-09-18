# Import FastAPI tools:
# FastAPI creates the API application
# Depends handles dependency injection
# HTTPException returns HTTP errors such as 404
# status provides named HTTP status codes such as HTTP_201_CREATED
from typing import Literal

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Import SQLAlchemy Session for database operations
from sqlalchemy.orm import Session

# Import password verification and JWT token creation functions.
from src.app.auth import create_access_token, verify_password

# Import application settings from config.py
from src.app.config import settings

# Import the database dependency that provides a database session
from src.app.database import get_db
from src.app.exceptions import DuplicateModelError, ModelNotFoundError

# Import the database user model.
from src.app.models import UserDB

# Import Pydantic schemas used for request validation and API responses
from src.app.schemas import (
    AIModelDelete,  # Schema for returning deleted model information
    AIModelRequest,  # Schema for creating an AI model
    AIModelResponse,  # Schema for returning an AI model
    AIModelUpdate,  # Schema for updating an AI model
    ErrorResponse,
    Token,
    UserCreate,
    UserResponse,
)

# Import service functions that contain the database/business logic
from src.app.services import (
    create_ai_model,  # Create a new AI model
    create_user,
    delete_ai_model,  # Delete an AI model
    generate_answer,
    get_ai_models,  # Get all AI models
    get_required_model,
    update_ai_model,  # Update an existing AI model
)

# Create the FastAPI application
# The application name and debug setting come from config.py
app = FastAPI(
    title=settings.app_name,
    description="REST API for managing AI models, authentication, and AI services.",
    version="1.0.0",
    debug=settings.debug,
)


@app.exception_handler(ModelNotFoundError)
async def model_not_found_handler(request: Request, exc: ModelNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "MODEL_NOT_FOUND", "message": str(exc)},
    )


@app.exception_handler(DuplicateModelError)
async def duplicate_model_handler(request: Request, exc: DuplicateModelError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": "DUPLICATE_MODEL", "message": str(exc)},
    )


def verify_api_key(x_api_key: str | None = Header(default=None)):
    # Check whether the API key is correct.
    if x_api_key != "my-secret-key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

    # Return a value when the API key is valid.
    return x_api_key


# Root endpoint
# GET / returns a basic message showing that the API is running
@app.get("/", tags=["Message"])
def root():
    return {"message": "AI Engineer 2026 API"}


# Health-check endpoint
# GET /health returns the health status of the API
@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}


# Authentication section #


@app.post(
    "/register",
    response_model=UserResponse,
    tags=["Authentication"],
    summary="Register a new user",
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, username=user.username, password=user.password)


@app.post(
    "/login",
    response_model=Token,
    tags=["Authentication"],
    summary="Login and obtain an access token",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(user_id=user.id, username=user.username)

    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserDB:
    """
    Verify the JWT access token and return the authenticated user.
    """

    try:
        # Decode and verify the JWT signature.
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
        ) from err

    except jwt.InvalidTokenError as err:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        ) from err

    # Get the user's ID from the JWT subject claim.
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    # Find the user in the database.
    user = db.query(UserDB).filter(UserDB.id == int(user_id)).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    # Make sure the account is still active.
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")

    return user


def require_admin(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    """
    Allow access only to authenticated users with the admin role.
    """

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return current_user


@app.get("/protected", tags=["Authentication"], summary="Access a protected endpoint")
def protected_route(current_user: UserDB = Depends(get_current_user)):
    """
    Protected endpoint that requires a valid JWT access token.

    The get_current_user dependency:
    1. Reads the JWT from the Authorization header.
    2. Verifies the token.
    3. Finds the corresponding user.
    4. Ensures the user is active.
    5. Returns the authenticated UserDB object.
    """

    return {"message": "You have access to the protected endpoint"}


@app.get("/admin", tags=["Administration"], summary="Access the admin endpoint")
def admin_route(current_user: UserDB = Depends(get_current_user)):
    """
    Admin-only endpoint.

    The user must be authenticated and have the
    admin role to access this endpoint.
    """

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {"message": "You have admin access"}


@app.get("/admin-only", tags=["Tests"], summary="Test endpoint for admins")
def admin_only(current_user: UserDB = Depends(require_admin)):
    """
    Test endpoint accessible only to administrators.
    """

    return {
        "message": "Welcome, admin!",
        "username": current_user.username,
        "role": current_user.role,
    }


# model section #


# Get all AI models
# GET /models reads all models from the database
# response_model ensures every returned model follows AIModelResponse
@app.get(
    "/models",
    response_model=list[AIModelResponse],
    tags=["Models"],
    summary="Get all AI models",
)
def list_models(
    # Number of models to skip
    skip: int = Query(default=0, ge=0, description="Number of models to skip"),
    # Maximum number of models to return
    limit: int = Query(
        default=10, ge=1, le=100, description="Maximum number of models to return"
    ),
    # Optional provider filter.
    provider: str | None = Query(default=None, description="Filter models by provider"),
    # Column used for sorting.
    sort_by: Literal["id", "name", "provider"] = Query(
        default="id", description="Column used to sort the models"
    ),
    # Sorting direction.
    order: Literal["asc", "desc"] = Query(
        default="asc", description="Sorting direction"
    ),
    # Database session
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    # Get models using pagination
    return get_ai_models(
        db, skip=skip, limit=limit, provider=provider, sort_by=sort_by, order=order
    )


# Get one AI model by its ID
# GET /models/{model_id}
@app.get(
    "/models/{model_id}",
    response_model=AIModelResponse,
    tags=["Models"],
    summary="Get an AI model by ID",
    responses={404: {"model": ErrorResponse, "description": "AI model not found"}},
)
def get_model_by_id_endpoint(
    # Get model_id from the URL path
    model_id: int,
    # Get a database session for this request
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    return get_required_model(db, model_id)


# Create a new AI model
# POST /models receives model data and saves a new model
# Returns 201 Created when successful
@app.post(
    "/models",
    response_model=AIModelResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Models"],
    summary="Create a new AI model",
    responses={409: {"model": ErrorResponse, "description": "AI model already exists"}},
)
def create_model(
    # FastAPI validates incoming JSON using AIModelRequest
    model_data: AIModelRequest,
    # Get a database session for this request
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    # Pass the validated data to the service function
    return create_ai_model(db, model_data.name, model_data.provider)


# Update an existing AI model
# PUT /models/{model_id}
@app.put(
    "/models/{model_id}",
    response_model=AIModelResponse,
    tags=["Models"],
    summary="Update an AI model",
)
def update_model(
    model_id: int,
    model_data: AIModelUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):

    return update_ai_model(db, model_id, model_data.name, model_data.provider)


# Delete an AI model
# DELETE /models/{model_id}
@app.delete(
    "/models/{model_id}",
    response_model=AIModelDelete,
    tags=["Models"],
    summary="Delete an AI model",
)
def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):

    return delete_ai_model(db, model_id)


@app.get(
    "/ai",
    tags=["AI"],
    summary="Generate an AI answer",
    description="Generate an answer using the configured AI service.",
    responses={500: {"model": ErrorResponse, "description": "AI service unavailable"}},
)
def ask_ai(prompt: str):
    """
    Generate an answer using the AI service.

    If the AI service fails, return a controlled
    HTTP 500 error instead of exposing the exception.
    """

    try:
        answer = generate_answer(prompt)

    except Exception as err:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail="AI service unavailable",
        ) from err
    return {"prompt": prompt, "answer": answer}
