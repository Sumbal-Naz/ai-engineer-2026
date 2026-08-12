from src.app.models import Person, AIModel
from src.app.services import calculate_years_to_goal, calculate_age

def display_person_age(person: Person, current_year: int) -> None:
    try:
        age = calculate_age(person.birth_year, current_year)
        print(f"{person.name}'s age: {age}")
            
    except ValueError as error:
        print(f"Invalid input: {error}")

def main():

    print("AI Engineer 2026")
    print("My transition into modern AI engineering has started")

    years = calculate_years_to_goal(2026, 2030)
    print(f"Years to goal: {years}")
    
    person = Person(
            name="Sumbal",
            birth_year=1995
            #birth_year=2030
        )
    
    display_person_age(person, 2026)
    
    
    model = AIModel(
        name="GPT",
        provider="OpenAI"
    )

    print(model.describe())
   


if __name__ == "__main__":
    main()
