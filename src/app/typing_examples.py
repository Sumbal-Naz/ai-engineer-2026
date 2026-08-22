
def greet(name: str) -> str:
    return f"Hello {name}"

def calculate_total(price: float, quantity: int) -> float:
    return price * quantity

def is_adult(age: int) -> bool:
    return age >= 18

def calculate_sum(numbers: list[int]) -> int:
    return sum(numbers)

def get_user() -> dict[str, str]:
    return {
        "name": "Sumbal",
        "role": "AI Engineer"
    }


# instead fo using Union imported form typing  as Optional[str] 
# we can use str | None

def get_phone(user_id: int) -> str | None:
    if user_id == 1:
        return "03001234567"
    return None

# and instead of using Union imported from typing as Union[int, str]
# we can use user_id: int | str
def process_id(user_id: int | str) -> str:
    return str(user_id)

def get_project_status(project_id: int | str) -> str | None:
    if project_id == "1" or project_id == 1:
        return "completed"
    elif project_id == "2" or project_id == 2:
        return "in_progress"
    else:
        return None
