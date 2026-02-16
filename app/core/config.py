# app/core/config.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "RAG Lab"
    environment: str = "local"
     # Must be set in .env

    model_config = SettingsConfigDict(
        env_file=".env",  # Ensure this file exists in project root
        extra="ignore"
    )

settings = Settings()
