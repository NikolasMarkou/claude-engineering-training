from datetime import datetime

from pydantic import BaseModel

from app.schemas.category import CategoryResponse


class BudgetBase(BaseModel):
    category_id: int
    amount: float
    month: str  # Format: "YYYY-MM"


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    amount: float


class BudgetResponse(BudgetBase):
    id: int
    created_at: datetime
    category: CategoryResponse

    class Config:
        from_attributes = True


class BudgetStatus(BaseModel):
    category_id: int
    category_name: str
    budgeted: float
    spent: float
    remaining: float
    percentage_used: float
