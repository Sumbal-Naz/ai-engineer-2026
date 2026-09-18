# Import the SQLAlchemy tools needed for an in-memory test database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the shared SQLAlchemy Base class.
from src.app.database import Base

# Import the relationship practice models.
from src.app.relationship_models import AIModelRelationship, ProviderDB


def test_provider_has_many_models():
    # Create a temporary in-memory SQLite database for this test.
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )

    # Create all database tables in the temporary database.
    Base.metadata.create_all(bind=engine)

    # Create a session factory connected to the temporary database.
    TestingSessionLocal = sessionmaker(bind=engine)

    # Create a database session.
    db = TestingSessionLocal()

    try:
        # Create one provider.
        provider = ProviderDB(name="OpenAI")

        # Create two AI models.
        model_1 = AIModelRelationship(name="GPT-4")
        model_2 = AIModelRelationship(name="GPT-5")

        # Connect both models to the same provider.
        model_1.provider = provider
        model_2.provider = provider

        # Add the provider and models to the session.
        db.add(provider)
        db.add(model_1)
        db.add(model_2)

        # Save everything to the temporary database.
        db.commit()

        # Refresh the provider with the latest database data.
        db.refresh(provider)

        # Verify the provider was saved correctly.
        assert provider.name == "OpenAI"

        # Verify the provider has two related models.
        assert len(provider.models) == 2

        # Verify the relationship works in the other direction.
        assert model_1.provider.name == "OpenAI"
        assert model_2.provider.name == "OpenAI"

    finally:
        # Always close the database session.
        db.close()
