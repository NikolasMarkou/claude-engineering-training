import datetime as dt

from pydantic import BaseModel

from app.schemas.category import CategoryResponse


class BankConnectionCreate(BaseModel):
    bank_name: str
    account_name: str
    account_type: str  # "checking", "savings", "credit"


class BankConnectionResponse(BaseModel):
    id: int
    bank_name: str
    account_name: str
    account_type: str
    balance: float
    last_synced: dt.datetime | None
    is_active: bool
    created_at: dt.datetime

    class Config:
        from_attributes = True


class PendingTransactionResponse(BaseModel):
    id: int
    bank_connection_id: int
    external_id: str
    amount: float
    merchant_name: str
    date: str
    suggested_category_id: int | None
    suggested_category: CategoryResponse | None
    status: str
    created_at: dt.datetime

    class Config:
        from_attributes = True


class PendingTransactionImport(BaseModel):
    category_id: int


class BankBalanceResponse(BaseModel):
    bank_connection_id: int
    bank_name: str
    account_name: str
    account_type: str
    balance: float
