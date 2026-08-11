from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Atanor"
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./atanor.db"


settings = Settings()
