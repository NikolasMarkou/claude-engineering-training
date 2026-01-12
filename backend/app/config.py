from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    app_name: str = "Budget App"
    database_url: str = "sqlite:///./budget.db"
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 1 week
    default_currency: str = "USD"

    # Exchange rate settings
    exchange_rate_provider: Literal["static", "frankfurter", "exchangerate-api"] = "frankfurter"
    exchange_rate_api_key: str | None = None  # Required for exchangerate-api
    exchange_rate_cache_minutes: int = 60  # Cache duration in minutes

    class Config:
        env_file = ".env"


settings = Settings()
