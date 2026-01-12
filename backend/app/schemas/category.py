from datetime import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    type: str  # "income" or "expense"
    icon: str | None = None
    color: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    color: str | None = None


class CategoryResponse(CategoryBase):
    id: int
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True
