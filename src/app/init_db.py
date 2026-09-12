from src.app.database import Base, engine

# Import the existing model so SQLAlchemy registers it.
from src.app.models import AIModelDB, UserDB

# Import the relationship practice models so SQLAlchemy registers them.
from src.app.relationship_models import (
    ProviderDB,
    AIModelRelationship
)


# Create all registered database tables.
Base.metadata.create_all(bind=engine)

print("Database tables created.")