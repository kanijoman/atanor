import logging

from fastapi import FastAPI

from app.config import settings


logging.basicConfig(level=settings.log_level)

logger = logging.getLogger("atanor")

app = FastAPI(title=settings.app_name)

logger.info("Atanor application started")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "status": "running",
    }