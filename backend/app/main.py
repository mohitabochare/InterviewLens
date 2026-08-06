"""
FastAPI application entrypoint.

Run with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.api.routes import health
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health.router)


@app.get("/", tags=["root"])
def root() -> dict:
    return {"message": f"{settings.app_name} API is running."}
