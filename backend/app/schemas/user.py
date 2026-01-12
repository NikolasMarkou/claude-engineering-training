from pydantic import BaseModel, field_validator
from typing import List
from app.models.currency import SUPPORTED_CURRENCIES


class PinSetup(BaseModel):
    pin: str


class PinLogin(BaseModel):
    pin: str


class PinChange(BaseModel):
    current_pin: str
    new_pin: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrencyUpdate(BaseModel):
    """Request schema for updating user's currency preference."""
    currency: str

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        if v not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Currency must be one of: {', '.join(SUPPORTED_CURRENCIES)}")
        return v


class UserSettingsResponse(BaseModel):
    currency: str
    is_setup: bool
    available_currencies: List[str] = SUPPORTED_CURRENCIES

    class Config:
        from_attributes = True


class ExchangeRatesResponse(BaseModel):
    """Response schema for exchange rates endpoint."""
    provider: str
    rates: dict
    cached_at: str | None = None
