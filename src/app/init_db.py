from src.app.database import Base, engine
from src.app.models import AIModelDB

Base.metadata.create_all(bind=engine)

print("Database tables created.")
