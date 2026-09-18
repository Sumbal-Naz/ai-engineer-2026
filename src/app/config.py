import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


APP_NAME = os.getenv("APP_NAME", "AI Engineer 2026")
AI_PROVIDER = os.getenv("AI_PROVIDER", "OpenAI")


class Settings(BaseSettings):
    app_name: str = "AI Engineer 2026"
    debug: bool = False
    database_url: str = "sqlite:///./ai_engineer.db"
    environment: str = "development"
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
