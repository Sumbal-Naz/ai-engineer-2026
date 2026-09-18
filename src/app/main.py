from src.app.config import AI_PROVIDER, APP_NAME
from src.app.dataclass_examples import AIProject, ProjectStatus
from src.app.models import AIModel, Person
from src.app.services import calculate_age, calculate_years_to_goal


# sample function to display age of a person
def display_person_age(person: Person, current_year: int) -> None:
    try:
        age = calculate_age(person.birth_year, current_year)
        print(f"{person.name}'s age: {age}")

    except ValueError as error:
        print(f"Invalid input: {error}")


# entry point
def main():

    print(APP_NAME)
    print("My transition into modern AI engineering has started")

    years = calculate_years_to_goal(2026, 2030)
    print(f"Years to goal: {years}")

    person = Person(
        name="Sumbal",
        birth_year=1995,
        # birth_year=2030
    )

    display_person_age(person, 2026)

    # sample model example

    model = AIModel(name="GPT", provider=AI_PROVIDER)

    print(model.describe())

    # dataclass examples
    project = AIProject(
        name="AI Engineer 2026",
        technology="FastAPI",
        days=180,
        status=ProjectStatus.IN_PROGRESS,
    )

    print(project)


if __name__ == "__main__":
    main()
