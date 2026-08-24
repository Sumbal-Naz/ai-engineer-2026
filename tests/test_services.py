import pytest
from src.app.services import get_project_status
from src.app.exceptions import InvalidProjectIDError

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
    