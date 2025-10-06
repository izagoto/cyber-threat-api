from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_VERSION: str
    ENVIRONMENT: str
    DATABASE_URL: str
    APP_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()
DATABASE_URL = settings.DATABASE_URL
