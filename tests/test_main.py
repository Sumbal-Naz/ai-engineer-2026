import pytest
from src.app.main import get_project_status
from src.app.exceptions import InvalidProjectIDError

from src.app.models import Person, AIModel
from src.app.services import calculate_years_to_goal, calculate_age

def test_calculate_years_to_goal():
    assert calculate_years_to_goal(2026, 2030) == 4

def test_calculate_age():
    assert calculate_age(1995, 2026) == 31

def test_invalid_calculate_age():
    with pytest.raises(ValueError):
            calculate_age(2030, 2026)

def test_invalid_target_year():
    with pytest.raises(ValueError):
        calculate_years_to_goal(2030, 2026)

def test_invalid_age_value():
    with pytest.raises(ValueError):
        calculate_age(2040, 2026)

def test_person():
    person = Person(
        name="Sumbal",
        birth_year=1995
    )

    assert person.name == "Sumbal"
    assert person.birth_year == 1995

def test_AIModel():
    model = AIModel(
        name="GPT",
        provider="OpenAI"
    )

    assert model.name == "GPT"
    assert model.provider == "OpenAI"
    assert model.describe() == "GPT is provided by OpenAI."

def test_get_project_status():
    assert get_project_status(1) == "completed"
    assert get_project_status(2) == "in_progress"
    assert get_project_status("1") == "completed"
    assert get_project_status("2") == "in_progress"


def test_get_project_status_invalid_id():
    with pytest.raises(InvalidProjectIDError):
        get_project_status(99)


def test_get_project_status_invalid_input():
    with pytest.raises(InvalidProjectIDError):
        get_project_status("abc")
    