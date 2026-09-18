from src.app.database import Base, engine

# Import the existing model so SQLAlchemy registers it.

# Import the relationship practice models so SQLAlchemy registers them.

# Create all registered database tables.
Base.metadata.create_all(bind=engine)

print("Database tables created.")
