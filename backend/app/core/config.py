"""
Application settings, loaded from environment variables (see .env.example).

Keep this file as the single source of truth for configuration. Don't read
os.environ directly elsewhere in the codebase — import `settings` from here.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "InterviewLens"
    environment: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./interviewlens.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
