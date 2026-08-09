def calculate_years_to_goal(current_year: int, target_year: int) -> int:
    if target_year < current_year:
        raise ValueError("Target year cannot be before current year")
    return target_year - current_year

def calculate_age(birth_year: int, current_year: int) -> int:
    return current_year - birth_year


def main():
    print("AI Engineer 2026")
    print("My transition into modern AI engineering has started")

    years = calculate_years_to_goal(2026, 2030)
    print(f"Years to goal: {years}")

    age = calculate_age(1995, 2026)
    print(f"Age: {age}")


if __name__ == "__main__":
    main()
