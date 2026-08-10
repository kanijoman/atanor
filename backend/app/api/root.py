from fastapi import APIRouter

from app.config import settings


router = APIRouter()


@router.get("/")
def root() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "status": "running",
    }