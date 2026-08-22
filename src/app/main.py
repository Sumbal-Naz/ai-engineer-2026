from src.app.models import Person, AIModel
from src.app.services import calculate_years_to_goal, calculate_age
from src.app.config import APP_NAME, AI_PROVIDER

from src.app.dataclass_examples import ProjectStatus, AIProject
from src.app.exceptions import InvalidProjectIDError

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# sample function to display age of a person
def display_person_age(person: Person, current_year: int) -> None:
    try:
        age = calculate_age(person.birth_year, current_year)
        print(f"{person.name}'s age: {age}")
            
    except ValueError as error:
        print(f"Invalid input: {error}")

# exceptions and logging
def get_project_status(project_id: int | str) -> str:

    logger.info(
        "Checking project status for ID: %s",
        project_id
    )

    if project_id == "1" or project_id == 1:
        return "completed"

    elif project_id == "2" or project_id == 2:
        return "in_progress"

    logger.warning(
        "Invalid project ID received: %s",
        project_id
    )

    raise InvalidProjectIDError(
        f"Unknown project ID: {project_id}"
    )

# entry point
def main():

    print(APP_NAME)
    print("My transition into modern AI engineering has started")

    years = calculate_years_to_goal(2026, 2030)
    print(f"Years to goal: {years}")
    
    person = Person(
            name="Sumbal",
            birth_year=1995
            #birth_year=2030
        )
    
    display_person_age(person, 2026)

    # sample model example
    
    model = AIModel(
        name="GPT",
        provider=AI_PROVIDER
    )

    print(model.describe())

    # dataclass examples
    project = AIProject(
        name="AI Engineer 2026",
        technology="FastAPI",
        days=180,
        status=ProjectStatus.IN_PROGRESS
    )

    print(project)

if __name__ == "__main__":
    main()
