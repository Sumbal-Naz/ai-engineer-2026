# Import tools for creating the database engine and managing sessions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Database connection URL
# This creates a SQLite database file named "ai_engineer.db"
# in the project's current directory.
DATABASE_URL = "sqlite:///./ai_engineer.db"


# Create the SQLAlchemy database engine.
# The engine manages the connection between our Python application
# and the SQLite database.
engine = create_engine(
    DATABASE_URL,

    # SQLite normally restricts a connection to the thread that created it.
    # Setting this to False allows the connection to be used across threads,
    # which is useful when working with FastAPI.
    connect_args={"check_same_thread": False}
)


# Create a session factory.
# Each database session created by SessionLocal() can be used
# to interact with the database.
SessionLocal = sessionmaker(
    # Changes are not automatically committed to the database.
    autocommit=False,

    # Changes are not automatically sent (flushed) to the database.
    # We control when this happens manually.
    autoflush=False,

    # Connect every session created by this factory to our engine.
    bind=engine
)


# Create the base class for all SQLAlchemy ORM models.
# Future database models will inherit from this Base class.
class Base(DeclarativeBase):
    pass


# Dependency function for providing a database session.
# FastAPI can use this function with Depends(get_db).
def get_db():
    # Create a new database session.
    db = SessionLocal()

    try:
        # Provide the database session to the route/function using it.
        yield db

    finally:
        # Always close the database session after the request is finished,
        # even if an error occurs.
        db.close()