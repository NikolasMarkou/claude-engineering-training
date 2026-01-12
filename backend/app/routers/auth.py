from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserSettings
from app.schemas.user import (
    PinSetup,
    PinLogin,
    PinChange,
    Token,
    UserSettingsResponse,
    CurrencyUpdate,
    ExchangeRatesResponse,
)
from app.utils.security import hash_pin, verify_pin, create_access_token
from app.services.exchange_rate_service import (
    refresh_rates,
    get_all_rates,
    get_cache_info,
    invalidate_cache,
)

router = APIRouter()


@router.get("/status", response_model=UserSettingsResponse)
def get_status(db: Session = Depends(get_db)):
    user = db.query(UserSettings).first()
    if user:
        return UserSettingsResponse(currency=user.currency, is_setup=True)
    return UserSettingsResponse(currency="USD", is_setup=False)


@router.post("/setup", response_model=Token)
def setup_pin(data: PinSetup, db: Session = Depends(get_db)):
    existing = db.query(UserSettings).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PIN already set up"
        )

    user = UserSettings(pin_hash=hash_pin(data.pin))
    db.add(user)
    db.commit()

    token = create_access_token({"sub": "user"})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(data: PinLogin, db: Session = Depends(get_db)):
    user = db.query(UserSettings).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PIN not set up"
        )

    if not verify_pin(data.pin, user.pin_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid PIN"
        )

    token = create_access_token({"sub": "user"})
    return Token(access_token=token)


@router.post("/change-pin")
def change_pin(data: PinChange, db: Session = Depends(get_db)):
    user = db.query(UserSettings).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PIN not set up"
        )

    if not verify_pin(data.current_pin, user.pin_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid current PIN"
        )

    user.pin_hash = hash_pin(data.new_pin)
    db.commit()

    return {"message": "PIN changed successfully"}


@router.put("/currency")
def update_currency(data: CurrencyUpdate, db: Session = Depends(get_db)):
    """Update user's preferred currency."""
    user = db.query(UserSettings).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not set up"
        )

    user.currency = data.currency
    db.commit()

    return {"message": "Currency updated", "currency": data.currency}


@router.get("/exchange-rates", response_model=ExchangeRatesResponse)
async def get_exchange_rates():
    """Get current exchange rates."""
    await refresh_rates()
    cache_info = get_cache_info()

    return ExchangeRatesResponse(
        provider=cache_info["provider"],
        rates=get_all_rates(),
        cached_at=cache_info["cached_at"],
    )


@router.post("/exchange-rates/refresh")
async def refresh_exchange_rates():
    """Force refresh exchange rates from provider."""
    invalidate_cache()
    success = await refresh_rates()

    cache_info = get_cache_info()
    return {
        "message": "Rates refreshed" if success else "Using cached/static rates",
        "provider": cache_info["provider"],
        "cached_at": cache_info["cached_at"],
    }
