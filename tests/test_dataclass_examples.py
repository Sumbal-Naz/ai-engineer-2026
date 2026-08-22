from src.app.dataclass_examples import AIProject, ProjectStatus



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

