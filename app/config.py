# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, HttpUrl
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Store Sentinel Uptime Inspector"
    ENVIRONMENT: str = "development"
    API_KEY: SecretStr = Field(default=SecretStr("dev_secret_api_key_12345"))
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./dev_sentinel.db",
        env="DATABASE_URL"
    )
    
    # Crawler Limits
    CRAWL_INTERVAL_MINUTES: int = 10
    MAX_CRAWL_DEPTH: int = 2
    MAX_CONCURRENT_REQUESTS: int = 10
    REQUEST_TIMEOUT_SECONDS: float = 10.0
    
    # Notification Settings
    SMTP_HOST: str = Field(default="localhost")
    SMTP_PORT: int = Field(default=1025)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: SecretStr = Field(default=SecretStr(""))
    EMAILS_FROM_EMAIL: str = Field(default="sentinel@store-monitor.local")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
