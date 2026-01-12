# Schemas - CLAUDE.md

> **Location:** `backend/app/schemas/`
> **Parent:** [`backend/app/`](../CLAUDE.md)
> **Siblings:** [`models/`](../models/CLAUDE.md), [`routers/`](../routers/CLAUDE.md), [`services/`](../services/CLAUDE.md), [`utils/`](../utils/CLAUDE.md)

## Purpose

Pydantic schemas for request/response validation and serialization. Provides type-safe API contracts between frontend and backend.

## Schema Pattern

```python
# Base: Common fields
class ItemBase(BaseModel):
    name: str
    value: float

# Create: For POST requests (extends Base)
class ItemCreate(ItemBase):
    pass

# Update: For PUT/PATCH (all fields optional)
class ItemUpdate(BaseModel):
    name: str | None = None
    value: float | None = None

# Response: API output (extends Base + adds id, timestamps)
class ItemResponse(ItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # ORM mode
```

## Files & Classes

### `user.py` - Authentication (5 classes)
| Class | Fields | Purpose |
|-------|--------|---------|
| `PinSetup` | `pin: str` | Initial PIN setup request |
| `PinLogin` | `pin: str` | Login request |
| `PinChange` | `current_pin, new_pin: str` | Change PIN request |
| `Token` | `access_token, token_type: str` | JWT response |
| `UserSettingsResponse` | `currency, is_setup: bool` | Auth status |

### `category.py` - Categories (4 classes)
| Class | Fields | Purpose |
|-------|--------|---------|
| `CategoryBase` | `name, type, icon?, color?` | Shared fields |
| `CategoryCreate` | *(extends Base)* | Create request |
| `CategoryUpdate` | `name?, icon?, color?` | Update (no type change) |
| `CategoryResponse` | `+ id, is_default, created_at` | Full response |

### `transaction.py` - Transactions (4 classes)
| Class | Fields | Purpose |
|-------|--------|---------|
| `TransactionBase` | `amount, type, category_id, description?, date` | Shared fields |
| `TransactionCreate` | *(extends Base)* | Create request |
| `TransactionUpdate` | All optional | Partial update |
| `TransactionResponse` | `+ id, created_at, category: CategoryResponse` | Nested response |

### `budget.py` - Budgets (4 classes)
| Class | Fields | Purpose |
|-------|--------|---------|
| `BudgetBase` | `category_id, amount, month` | Shared fields |
| `BudgetCreate` | *(extends Base)* | Create request |
| `BudgetUpdate` | `amount: float` | Only amount updatable |
| `BudgetResponse` | `+ id, created_at, category: CategoryResponse` | Nested response |
| `BudgetStatus` | `category_id, category_name, budgeted, spent, remaining, percentage_used` | Computed report |

### `recurring.py` - Recurring Transactions (4 classes)
| Class | Fields | Purpose |
|-------|--------|---------|
| `RecurringBase` | `amount, type, category_id, description?, frequency, next_run_date` | Shared fields |
| `RecurringCreate` | *(extends Base)* | Create request |
| `RecurringUpdate` | All optional + `is_active?` | Update with toggle |
| `RecurringResponse` | `+ id, is_active, created_at, category: CategoryResponse` | Nested response |

### `goal.py` - Savings Goals (4 classes)
| Class | Fields | Purpose |
|-------|--------|---------|
| `GoalBase` | `name, target_amount, deadline` | Shared fields |
| `GoalCreate` | *(extends Base)* | Create request |
| `GoalUpdate` | All optional + `current_amount?` | Update fields |
| `GoalContribute` | `amount: float` | Contribution action |
| `GoalResponse` | `+ id, current_amount, created_at, progress_percentage, days_remaining` | Computed response |

### `bank.py` - Open Banking (5 classes)
| Class | Fields | Purpose |
|-------|--------|---------|
| `BankConnectionCreate` | `bank_name, account_name, account_type` | Connect bank |
| `BankConnectionResponse` | `+ id, balance, last_synced?, is_active, created_at` | Connection details |
| `PendingTransactionResponse` | Full fields + `suggested_category?: CategoryResponse` | Pending import |
| `PendingTransactionImport` | `category_id: int` | Import action |
| `BankBalanceResponse` | `bank_connection_id, bank_name, account_name, account_type, balance` | Balance summary |

## Computed Fields

| Schema | Field | Calculation |
|--------|-------|-------------|
| `BudgetStatus` | `spent` | Sum of expenses for category/month |
| `BudgetStatus` | `remaining` | `budgeted - spent` |
| `BudgetStatus` | `percentage_used` | `(spent / budgeted) * 100` |
| `GoalResponse` | `progress_percentage` | `(current_amount / target_amount) * 100` |
| `GoalResponse` | `days_remaining` | `(deadline - today).days` |

## Nested Relationships

These response schemas include full nested objects:
- `TransactionResponse.category` → `CategoryResponse`
- `BudgetResponse.category` → `CategoryResponse`
- `RecurringResponse.category` → `CategoryResponse`
- `PendingTransactionResponse.suggested_category` → `CategoryResponse | None`

## ORM Mode Configuration

All Response schemas use:
```python
class Config:
    from_attributes = True  # Enables SQLAlchemy → Pydantic conversion
```

## Validation Notes

- No explicit PIN length validation (handled in frontend)
- Amount fields accept any float (no minimum/maximum)
- Type fields use string literals ("income"/"expense") not Python enums
- Month format "YYYY-MM" not validated at schema level
