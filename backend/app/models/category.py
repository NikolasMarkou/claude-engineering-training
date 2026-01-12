from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "income" or "expense"
    is_default = Column(Boolean, default=False)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
