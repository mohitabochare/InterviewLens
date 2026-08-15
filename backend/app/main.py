import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes import health
from app.api.routes import session
from app.core.config import settings
from app.core.database import Base, engine
from app.models import session as session_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(health.router)
app.include_router(session.router)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_PATH = os.path.join(BASE_DIR, "..", "frontend", "index.html")


@app.get("/", tags=["root"])
def root() -> dict:
    return {"message": f"{settings.app_name} API is running."}


@app.get("/dashboard")
def dashboard():
    return FileResponse(FRONTEND_PATH)