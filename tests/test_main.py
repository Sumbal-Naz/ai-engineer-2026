import pytest

from src.app.main import calculate_years_to_goal, calculate_age


def test_calculate_years_to_goal():
    assert calculate_years_to_goal(2026, 2030) == 4

def test_calculate_age():
    assert calculate_age(1995, 2026) == 31

def test_invalid_target_year():
    with pytest.raises(ValueError):
        calculate_years_to_goal(2030, 2026)