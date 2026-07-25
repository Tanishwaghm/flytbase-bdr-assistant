"""
Application configuration.
Loads environment variables and exposes typed settings used across the backend.
"""

import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env before reading variables
load_dotenv()


class Settings(BaseSettings):
    # ---------------- LLM ----------------
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # ---------------- APP ----------------
    app_env: str = os.getenv("APP_ENV", "development")
    cors_origins: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000"
    )

    request_timeout_seconds: int = int(
        os.getenv("REQUEST_TIMEOUT_SECONDS", "30")
    )

    # ---------------- CACHE ----------------
    cache_ttl_seconds: int = int(
        os.getenv("CACHE_TTL_SECONDS", "3600")
    )

    rate_limit_per_minute: int = int(
        os.getenv("RATE_LIMIT_PER_MINUTE", "20")
    )

    # ---------------- RETRIES ----------------
    max_retries: int = int(
        os.getenv("MAX_RETRIES", "3")
    )

    retry_backoff_seconds: float = float(
        os.getenv("RETRY_BACKOFF_SECONDS", "1.5")
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings():
    return Settings()