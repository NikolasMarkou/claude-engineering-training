import datetime as dt

from pydantic import BaseModel

from app.schemas.category import CategoryResponse


class RecurringBase(BaseModel):
    amount: float
    type: str  # "income" or "expense"
    category_id: int
    description: str | None = None
    frequency: str  # "daily", "weekly", "monthly"
    next_run_date: dt.date


class RecurringCreate(RecurringBase):
    pass


class RecurringUpdate(BaseModel):
    amount: float | None = None
    type: str | None = None
    category_id: int | None = None
    description: str | None = None
    frequency: str | None = None
    next_run_date: dt.date | None = None
    is_active: bool | None = None


class RecurringResponse(RecurringBase):
    id: int
    is_active: bool
    created_at: dt.datetime
    category: CategoryResponse

    class Config:
        from_attributes = True
