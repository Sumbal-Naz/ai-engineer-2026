from src.app.main import calculate_years_to_goal


def test_calculate_years_to_goal():
    assert calculate_years_to_goal(2026, 2030) == 4
