# Import SQLAlchemy tools for defining database columns.
from sqlalchemy import ForeignKey, String

# Import SQLAlchemy ORM tools for typed models and relationships.
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Import the shared Base class for SQLAlchemy models.
from src.app.database import Base


# Provider database model.
# One provider can have many AI models.
class ProviderDB(Base):
    # Name of the database table.
    __tablename__ = "providers"

    # Primary key for each provider.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Name of the provider, for example OpenAI.
    name: Mapped[str] = mapped_column(String(100))

    # Relationship to all AI models belonging to this provider.
    models: Mapped[list["AIModelRelationship"]] = relationship(
        back_populates="provider"
    )


# AI model database model used specifically for relationship practice.
class AIModelRelationship(Base):
    # Name of the database table.
    __tablename__ = "ai_model_relationships"

    # Primary key for each AI model.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Name of the AI model.
    name: Mapped[str] = mapped_column(String(100))

    # Foreign key connecting this model to a provider.
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"))

    # Relationship to the provider this AI model belongs to.
    provider: Mapped["ProviderDB"] = relationship(back_populates="models")
