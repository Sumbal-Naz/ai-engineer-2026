from fastapi import FastAPI

from app.api import router

app = FastAPI(title="Task Management API")

app.include_router(router)
