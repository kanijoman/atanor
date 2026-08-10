import logging

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.root import router as root_router
from app.config import settings


logging.basicConfig(level=settings.log_level)

logger = logging.getLogger("atanor")

app = FastAPI(title=settings.app_name)

app.include_router(root_router)
app.include_router(health_router)

logger.info("Atanor application started")