"""
Configuration file - Loads environment variables
This file reads settings from .env file and makes them available to the app
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from .env file
    BaseSettings automatically reads from .env
    """

    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "nyra_db"
    DB_USER: str = "nyra_user"
    DB_PASSWORD: str

    # Gemini API
    GEMINI_API_KEY: str

    # App settings
    APP_NAME: str = "Restaurant Chatbot"
    DEBUG: bool = True
    API_VERSION: str = "v1"

    # Restaurant info
    RESTAURANT_NAME: str = "Tasty Bites Café"
    RESTAURANT_HOURS: str = "11:00 AM - 11:00 PM"
    DELIVERY_AVAILABLE: bool = True

    # Database URL (constructed automatically)
    @property
    def DATABASE_URL(self) -> str:
        """Constructs MySQL connection URL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"  # Tell pydantic to read from .env file
        case_sensitive = True


# Create a single instance to use throughout the app
settings = Settings()

# For debugging - print settings (remove password for security)
if __name__ == "__main__":
    print(f"App Name: {settings.APP_NAME}")
    print(f"Database: {settings.DB_NAME}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Database URL: mysql+pymysql://{settings.DB_USER}:****@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
