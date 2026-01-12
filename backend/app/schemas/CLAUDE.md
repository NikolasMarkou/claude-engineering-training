# Schemas - CLAUDE.md

## Overview

Pydantic schemas for request/response validation and serialization. Each schema file corresponds to a model and defines Create, Update, and Response schemas.

## Schema Pattern

Each domain follows a consistent pattern:

```python
# Base schema with shared fields
class ItemBase(BaseModel):
    name: str
    value: float

# Create schema (request body for POST)
class ItemCreate(ItemBase):
    pass

# Update schema (request body for PUT/PATCH - optional fields)
class ItemUpdate(BaseModel):
    name: str | None = None
    value: float | None = None

# Response schema (API response with ID and timestamps)
class ItemResponse(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode
```

## Schema Files

### user.py
- `PinSetup`: PIN string for initial setup
- `PinLogin`: PIN string for authentication
- `PinChange`: Current PIN + new PIN for changing
- `Token`: JWT access token response
- `UserSettingsResponse`: Currency and setup status

### category.py
- `CategoryCreate`: name, type, icon, color
- `CategoryUpdate`: All fields optional
- `CategoryResponse`: Includes id, is_default, created_at

### transaction.py
- `TransactionCreate`: amount, type, category_id, description, date
- `TransactionUpdate`: All fields optional
- `TransactionResponse`: Includes nested `CategoryResponse`

### budget.py
- `BudgetCreate`: category_id, amount, month (YYYY-MM)
- `BudgetUpdate`: Only amount updatable
- `BudgetResponse`: Includes nested `CategoryResponse`
- `BudgetStatus`: Computed fields (spent, remaining, percentage_used)

### recurring.py
- `RecurringCreate`: amount, type, category_id, description, frequency, next_run_date
- `RecurringUpdate`: All fields optional + is_active
- `RecurringResponse`: Includes nested `CategoryResponse`

### goal.py
- `GoalCreate`: name, target_amount, deadline
- `GoalUpdate`: All fields optional
- `GoalContribute`: amount for contribution
- `GoalResponse`: Includes computed `progress_percentage`, `days_remaining`

### bank.py
- `BankConnectionCreate`: bank_name, account_name, account_type
- `BankConnectionResponse`: Full connection data
- `PendingTransactionResponse`: With nested optional `CategoryResponse`
- `PendingTransactionImport`: category_id for import action
- `BankBalanceResponse`: Summary for balance display

## ORM Mode

All Response schemas use `from_attributes = True` to enable automatic conversion from SQLAlchemy models:

```python
class Config:
    from_attributes = True
```

This allows returning ORM objects directly from endpoints:

```python
@router.get("/items/{id}", response_model=ItemResponse)
def get_item(id: int, db: Session = Depends(get_db)):
    return db.query(Item).get(id)  # Automatically serialized
```
