import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Console shop API"

    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    SECRET: str | None = os.getenv("SECRET")

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
