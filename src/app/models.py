# dataclass automatically creates useful methods such as __init__
from dataclasses import dataclass

from sqlalchemy import Boolean, String

# Mapped and mapped_column are used to define SQLAlchemy database columns
from sqlalchemy.orm import Mapped, mapped_column

# Import the SQLAlchemy Base class.
# AIModelDB will inherit from Base so SQLAlchemy knows it is a database model.
from src.app.database import Base


# A dataclass is a simple class mainly used to store data.
@dataclass
class Person:
    # Person's name
    name: str

    # Person's birth year
    birth_year: int

    # Calculate the person's age from their birth year
    def calculate_age(self, current_year: int) -> int:
        return current_year - self.birth_year

    # Return a simple introduction sentence
    def introduce(self) -> str:
        return f"My name is {self.name}."


# Regular Python class representing an AI model.
# This is not a database model.
class AIModel:
    # Create an AIModel object with a name and provider
    def __init__(self, name: str, provider: str):
        self.name = name
        self.provider = provider

    # Return a description of the AI model
    def describe(self) -> str:
        return f"{self.name} is provided by {self.provider}."


# SQLAlchemy database model.
# This class represents the ai_models table in the database.
class AIModelDB(Base):
    # Name of the database table
    __tablename__ = "ai_models"

    # Primary key column.
    # Each AI model gets a unique ID.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Database column storing the AI model's name.
    # Maximum length is 100 characters.
    name: Mapped[str] = mapped_column(String(100))

    # Database column storing the provider's name.
    # Maximum length is 100 characters.
    provider: Mapped[str] = mapped_column(String(100))

    # Database column storing description
    # Maximum lenght is 255 characters
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)


class UserDB(Base):
    """
    Database model representing an authenticated API user.
    """

    __tablename__ = "users"

    # Primary key for the user.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Unique username used during login.
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    # Hashed password stored in the database.
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Whether the account is active.
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # User role used for authorization.
    role: Mapped[str] = mapped_column(
        String(50),
        default="user",
        nullable=False,
    )
