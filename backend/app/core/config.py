import os
from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "CampusConnect Backend"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "YOUR_SECRET_KEY_PLEASE_CHANGE_IN_PRODUCTION" # TODO: Change this
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/campusconnect"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Environment: 'development', 'production', 'testing'
    ENVIRONMENT: str = "development"
    
    # CORS Configuration
    # In production, this should be a list of allowed origins
    # For development, we'll allow all origins (handled in main.py)
    # Empty list means allow all in development
    BACKEND_CORS_ORIGINS: List[str] = []  # Empty list = allow all in development

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
