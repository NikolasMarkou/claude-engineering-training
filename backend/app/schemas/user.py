from pydantic import BaseModel


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


class UserSettingsResponse(BaseModel):
    currency: str
    is_setup: bool

    class Config:
        from_attributes = True
