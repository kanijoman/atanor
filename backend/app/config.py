from pathlib import Path

from pydantic_settings import BaseSettings


BACKEND_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_PATH = BACKEND_ROOT / "atanor.db"


class Settings(BaseSettings):
    app_name: str = "Atanor"
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"


settings = Settings()
