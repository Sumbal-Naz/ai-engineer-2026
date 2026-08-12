from src.app.models import Person, AIModel
from src.app.services import calculate_years_to_goal, calculate_age


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
    
    try:
        age = calculate_age(person.birth_year, 2026)
        print(f"{person.name}'s age: {age}")
        
    except ValueError as error:
        print(f"Invalid input: {error}")
    
    
    model = AIModel(
        name="GPT",
        provider="OpenAI"
    )

    print(model.describe())
   


if __name__ == "__main__":
    main()
