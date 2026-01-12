import datetime as dt

from pydantic import BaseModel


class GoalBase(BaseModel):
    name: str
    target_amount: float
    deadline: dt.date


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    name: str | None = None
    target_amount: float | None = None
    current_amount: float | None = None
    deadline: dt.date | None = None


class GoalContribute(BaseModel):
    amount: float


class GoalResponse(GoalBase):
    id: int
    current_amount: float
    created_at: dt.datetime
    progress_percentage: float
    days_remaining: int

    class Config:
        from_attributes = True
