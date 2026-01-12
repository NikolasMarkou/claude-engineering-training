from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class BankConnection(Base):
    __tablename__ = "bank_connections"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String, nullable=False)
    account_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)  # "checking", "savings", "credit"
    balance = Column(Float, default=0.0)
    last_synced = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    pending_transactions = relationship("PendingTransaction", back_populates="bank_connection", cascade="all, delete-orphan")


class PendingTransaction(Base):
    __tablename__ = "pending_transactions"

    id = Column(Integer, primary_key=True, index=True)
    bank_connection_id = Column(Integer, ForeignKey("bank_connections.id"), nullable=False)
    external_id = Column(String, nullable=False)  # ID from the bank
    amount = Column(Float, nullable=False)
    merchant_name = Column(String, nullable=False)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    suggested_category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    status = Column(String, default="pending")  # "pending", "imported", "dismissed"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    bank_connection = relationship("BankConnection", back_populates="pending_transactions")
    suggested_category = relationship("Category")
