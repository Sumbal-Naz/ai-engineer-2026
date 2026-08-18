from sqlalchemy.orm import Session
from src.app.models import AIModelDB

def calculate_years_to_goal(current_year: int, target_year: int) -> int:
    if target_year < current_year:
        raise ValueError("Target year cannot be before current year")
    return target_year - current_year

def calculate_age(birth_year: int, current_year: int) -> int:
    if birth_year > current_year:
        raise ValueError("Birth year cannot be after current year")
    return current_year - birth_year

def create_ai_model(
        db: Session,
        name: str,
        provider: str
) -> AIModelDB:

    model = AIModelDB(
        name=name,
        provider=provider
    )

    db.add(model)
    db.commit()
    db.refresh(model)

    return model

def get_ai_models(db: Session) -> list[AIModelDB]:
    return db.query(AIModelDB).all()
