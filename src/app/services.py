# Import the SQLAlchemy Session type.
# It is used for type hints when working with database sessions.
# Import Python's built-in logging module.
import logging
from typing import Any

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from src.app.auth import hash_password
from src.app.exceptions import (
    DuplicateModelError,
    InvalidProjectIDError,
    ModelNotFoundError,
)

# Import the SQLAlchemy database model for AI models.
from src.app.models import AIModelDB, UserDB

# Create a logger for this module.
# __name__ helps identify where a log message came from.
logger = logging.getLogger(__name__)


# Calculate how many years remain between the current year
# and a target year.
def calculate_years_to_goal(current_year: int, target_year: int) -> int:
    # A target year cannot be earlier than the current year.
    if target_year < current_year:
        raise ValueError("Target year cannot be before current year")

    # Return the difference between the two years.
    return target_year - current_year


# Calculate a person's age using their birth year
# and the current year.
def calculate_age(birth_year: int, current_year: int) -> int:
    # A birth year cannot be later than the current year.
    if birth_year > current_year:
        raise ValueError("Birth year cannot be after current year")

    # Return the calculated age.
    return current_year - birth_year


# Create and save a new AI model in the database.
def create_ai_model(db: Session, name: str, provider: str) -> AIModelDB:

    # Check whether a model with the same name already exists.
    existing_model = db.query(AIModelDB).filter(AIModelDB.name == name).first()

    # If it exists, raise a business exception.
    if existing_model:
        raise DuplicateModelError(f"Model '{name}' already exists")

    # Create a new AIModelDB object.
    # At this point, it only exists in Python memory.
    model = AIModelDB(name=name, provider=provider)

    # Add the new model object to the database session.
    db.add(model)

    # Save (commit) the changes permanently to the database.
    db.commit()

    # Reload the model from the database.
    # This updates the object with database-generated values,
    # such as the ID.
    db.refresh(model)

    # Return the newly created database model.
    return model


# Retrieve AI models from the database using pagination.
def get_ai_models(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    provider: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
) -> list[AIModelDB]:

    # Start a query for all AI models.
    query = db.query(AIModelDB)

    # Apply provider filtering only when a provider was supplied.
    if provider:
        query = query.filter(AIModelDB.provider == provider)

    sort_column: Any
    # Choose the column to sort by.
    if sort_by == "name":
        sort_column = AIModelDB.name
    elif sort_by == "provider":
        sort_column = AIModelDB.provider
    else:
        sort_column = AIModelDB.id

    # Choose ascending or descending order.
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # Skip the requested number of records.
    query = query.offset(skip)

    # Limit the number of records returned.
    query = query.limit(limit)

    # Execute the query and return the results as a list.
    return query.all()


# Retrieve a single AI model using its ID.
def get_model_by_id(db: Session, model_id: int) -> AIModelDB | None:

    # Query the database for a model whose ID matches model_id.
    # .first() returns the first matching record or None if no record exists.
    return db.query(AIModelDB).filter(AIModelDB.id == model_id).first()


# Update an existing AI model in the database.
def update_ai_model(db: Session, model_id: int, name: str, provider: str) -> AIModelDB:

    # Find the existing model.
    model = get_model_by_id(db, model_id)

    # Raise a business exception if it doesn't exist.
    if model is None:
        raise ModelNotFoundError(f"Model with ID {model_id} not found")

    # Update the model's name.
    model.name = name

    # Update the model's provider.
    model.provider = provider

    # Save the changes to the database.
    db.commit()

    # Reload the model to get its latest database values.
    db.refresh(model)

    # Return the updated model.
    return model


# Delete an AI model from the database.
def delete_ai_model(db: Session, model_id: int) -> AIModelDB:

    # Find the model that should be deleted.
    model = get_model_by_id(db, model_id)

    # Raise an exception if the model doesn't exist.
    if model is None:
        raise ModelNotFoundError(f"Model with ID {model_id} not found")

    # Mark the model for deletion.
    db.delete(model)

    # Permanently apply the deletion to the database.
    db.commit()

    # Return the deleted model object.
    # Note: The object is no longer stored in the database.
    return model


# ==============================
# Exceptions and Logging
# ==============================


# Get the status of a project using its ID.
def get_project_status(project_id: int | str) -> str:
    # Log that we are checking the project status.
    logger.info("Checking project status for ID: %s", project_id)

    # Accept both the integer 1 and string "1".
    if project_id == "1" or project_id == 1:
        return "completed"

    # Accept both the integer 2 and string "2".
    elif project_id == "2" or project_id == 2:
        return "in_progress"

    # Log a warning when an invalid project ID is received.
    logger.warning("Invalid project ID received: %s", project_id)

    # Raise our custom exception for unknown project IDs.
    raise InvalidProjectIDError(f"Unknown project ID: {project_id}")


def get_required_model(db: Session, model_id: int) -> AIModelDB:

    model = get_model_by_id(db, model_id)

    if model is None:
        raise ModelNotFoundError(f"Model with ID {model_id} not found")

    return model


def create_user(db: Session, username: str, password: str) -> UserDB:
    """
    Create a new user with a securely hashed password.
    """

    existing_user = db.query(UserDB).filter(UserDB.username == username).first()

    if existing_user:
        raise ValueError("Username already exists")

    hashed_password = hash_password(password)

    user = UserDB(
        username=username,
        password_hash=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# A simple service that represents an AI/LLM operation.
# In a real AI application, this could call an LLM,
# an ML model, or an external AI API.


def generate_answer(prompt: str) -> str:
    """
    Generate an answer for the given prompt.

    For now, this is only a simple implementation.
    Later, this could call a real AI model.
    """

    return f"Real AI response for: {prompt}"
