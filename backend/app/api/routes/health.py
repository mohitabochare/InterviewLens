"""
Basic health-check endpoint. Useful for confirming the server is running,
and later for uptime checks / deployment smoke tests.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}
