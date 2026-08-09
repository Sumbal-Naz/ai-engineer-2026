def calculate_years_to_goal(current_year: int, target_year: int) -> int:
    if target_year < current_year:
        raise ValueError("Target year cannot be before current year")
    return target_year - current_year

def calculate_age(birth_year: int, current_year: int) -> int:
    return current_year - birth_year