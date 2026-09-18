from src.app.config import settings


def test_app_name():
    assert settings.app_name == "AI Engineer 2026"


def test_debug():
    assert settings.debug is True


def test_database_url():
    assert settings.database_url == "sqlite:///./ai_engineer.db"


def test_environment():
    assert settings.environment == "development"
