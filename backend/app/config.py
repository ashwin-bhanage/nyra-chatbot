"""
Configuration file - Production Ready
Supports both MySQL (local) and PostgreSQL (production)
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # === DATABASE SETTINGS ===
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "nyra_db"
    DB_USER: str = "nyra_user"
    DB_PASSWORD: str = ""

    # For production PostgreSQL (Render provides this)
    DATABASE_URL: Optional[str] = None

    # === API KEYS ===
    GEMINI_API_KEY: str = ""

    # === APP SETTINGS ===
    APP_NAME: str = "Restaurant Chatbot"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    ENVIRONMENT: str = "development"

    # === RESTAURANT INFO ===
    RESTAURANT_NAME: str = "Royal Spice Kitchen"
    RESTAURANT_HOURS: str = "11:00 AM - 11:00 PM"
    DELIVERY_AVAILABLE: bool = True

    # === CORS ===
    FRONTEND_URL: str = "http://localhost:5173"

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)
            return url
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production" or self.DATABASE_URL is not None

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()
