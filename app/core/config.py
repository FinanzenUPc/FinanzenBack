from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Finanzen Backend"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://postgres:1234@localhost:5434/finanzen_db"

    # PostgreSQL credentials (for scripts)
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "1234"
    POSTGRES_DB: str = "finanzen_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5434"

    # Security
    SECRET_KEY: str = "my-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS - Permitir múltiples orígenes
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173"
    ]

    # Permitir parseo de lista desde string (para Railway/Render)
    @property
    def cors_origins(self) -> List[str]:
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
        return self.BACKEND_CORS_ORIGINS

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
