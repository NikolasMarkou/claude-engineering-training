import datetime as dt

from pydantic import BaseModel

from app.schemas.category import CategoryResponse


class TransactionBase(BaseModel):
    amount: float
    type: str  # "income" or "expense"
    category_id: int
    description: str | None = None
    date: dt.date


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: float | None = None
    type: str | None = None
    category_id: int | None = None
    description: str | None = None
    date: dt.date | None = None


class TransactionResponse(TransactionBase):
    id: int
    created_at: dt.datetime
    category: CategoryResponse

    class Config:
        from_attributes = True
