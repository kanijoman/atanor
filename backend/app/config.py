from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Atanor"
    app_env: str = "development"
    log_level: str = "INFO"


settings = Settings()