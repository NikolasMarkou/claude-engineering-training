from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserSettings
from app.schemas.user import PinSetup, PinLogin, PinChange, Token, UserSettingsResponse
from app.utils.security import hash_pin, verify_pin, create_access_token

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
