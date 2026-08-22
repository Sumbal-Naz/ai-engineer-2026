from src.app.dataclass_examples import AIProject, ProjectStatus
from src.app.typing_examples import get_project_status


def test_ai_project():
    project = AIProject(
        name="AI Engineer 2026",
        technology="FastAPI",
        days=180,
        status=ProjectStatus.IN_PROGRESS,
    )

    assert project.name == "AI Engineer 2026"
    assert project.technology == "FastAPI"
    assert project.days == 180
    assert project.status == ProjectStatus.IN_PROGRESS
    assert project.description is None

def test_project_with_description():
    project = AIProject(
        name="AI Engineer 2026",
        technology="FastAPI",
        days=180,
        status=ProjectStatus.PLANNED,
        description="My AI engineering learning project",
    )

    assert project.description == "My AI engineering learning project"

def test_get_project_status():
    status_1 = get_project_status(1)
    status_2 = get_project_status(2)
    status_3 = get_project_status(999)
    status_4 = get_project_status("1")
    status_5 = get_project_status("2")

    assert status_1 == "completed"
    assert status_2 == "in_progress"
    assert status_3 is None
    assert status_4 == "completed"
    assert status_5 == "in_progress"
