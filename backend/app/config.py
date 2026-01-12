from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Budget App"
    database_url: str = "sqlite:///./budget.db"
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 1 week
    default_currency: str = "USD"

    class Config:
        env_file = ".env"


settings = Settings()
