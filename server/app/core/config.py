from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import os

# Ensure the repo root .env is loaded regardless of current working directory
ROOT_DOTENV = Path(__file__).resolve().parents[3] / ".env"
if ROOT_DOTENV.exists():
    load_dotenv(ROOT_DOTENV)


class Settings(BaseSettings):
    APP_NAME: str = "Secure API"
    API_V1_PREFIX: str = "/api/v1"
    JWT_SECRET: str = Field(default="change-this-in-prod", description="JWT secret key")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    DATABASE_URL: str
    ENV: str = "development"
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file_encoding = "utf-8"


settings = Settings()
