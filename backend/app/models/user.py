from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    pin_hash = Column(String, nullable=False)
    currency = Column(String, default="USD")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
