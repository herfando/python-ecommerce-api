import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/dbname")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")

settings = Settings()