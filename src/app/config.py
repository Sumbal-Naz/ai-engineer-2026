import os

from dotenv import load_dotenv

load_dotenv()


APP_NAME = os.getenv("APP_NAME", "AI Engineer 2026")
AI_PROVIDER = os.getenv("AI_PROVIDER", "OpenAI")
