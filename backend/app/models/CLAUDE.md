# Models - CLAUDE.md

> **Location:** `backend/app/models/`
> **Parent:** [`backend/app/`](../CLAUDE.md)
> **Siblings:** [`schemas/`](../schemas/CLAUDE.md), [`routers/`](../routers/CLAUDE.md), [`services/`](../services/CLAUDE.md), [`utils/`](../utils/CLAUDE.md)

## Purpose

SQLAlchemy ORM models defining the database schema for the Budget App. All models inherit from `Base` (declarative base from `database.py`) and are automatically created as tables on application startup.

## Files

| File | Model(s) | Table Name | Purpose |
|------|----------|------------|---------|
| `__init__.py` | - | - | Exports all models |
| `user.py` | `UserSettings` | `user_settings` | Single-user authentication and preferences |
| `category.py` | `Category` | `categories` | Transaction categorization |
| `transaction.py` | `Transaction` | `transactions` | Income/expense records |
| `budget.py` | `Budget` | `budgets` | Monthly spending limits |
| `recurring.py` | `RecurringTransaction` | `recurring_transactions` | Automated scheduled transactions |
| `goal.py` | `Goal` | `goals` | Savings targets with deadlines |
| `bank.py` | `BankConnection`, `PendingTransaction` | `bank_connections`, `pending_transactions` | Open Banking integration |

## Model Details

### UserSettings (`user.py`)
```python
id: Integer (PK)
pin_hash: String (NOT NULL)      # Bcrypt-hashed PIN
currency: String (DEFAULT="USD") # Preferred currency
created_at: DateTime (UTC)       # Account creation
```
**Relationships:** None (singleton root entity)

### Category (`category.py`)
```python
id: Integer (PK)
name: String (NOT NULL)          # e.g., "Food & Dining"
type: String (NOT NULL)          # "income" or "expense"
is_default: Boolean (DEFAULT=False)  # Protected from deletion
icon: String (nullable)          # Font Awesome icon name
color: String (nullable)         # Hex color code
created_at: DateTime (UTC)
```
**Relationships:** Referenced by Transaction, Budget, RecurringTransaction, PendingTransaction

### Transaction (`transaction.py`)
```python
id: Integer (PK)
amount: Float (NOT NULL)
type: String (NOT NULL)          # "income" or "expense"
category_id: Integer (FK → categories.id, NOT NULL)
description: String (nullable)
date: Date (NOT NULL)
created_at: DateTime (UTC)
```
**Relationships:** `category` → Category (many-to-one)

### Budget (`budget.py`)
```python
id: Integer (PK)
category_id: Integer (FK → categories.id, NOT NULL)
amount: Float (NOT NULL)         # Monthly limit
month: String (NOT NULL)         # Format: "YYYY-MM"
created_at: DateTime (UTC)
```
**Relationships:** `category` → Category (many-to-one)

### RecurringTransaction (`recurring.py`)
```python
id: Integer (PK)
amount: Float (NOT NULL)
type: String (NOT NULL)          # "income" or "expense"
category_id: Integer (FK → categories.id, NOT NULL)
description: String (nullable)
frequency: String (NOT NULL)     # "daily", "weekly", "monthly"
next_run_date: Date (NOT NULL)
is_active: Boolean (DEFAULT=True)
created_at: DateTime (UTC)
```
**Relationships:** `category` → Category (many-to-one)

### Goal (`goal.py`)
```python
id: Integer (PK)
name: String (NOT NULL)
target_amount: Float (NOT NULL)
current_amount: Float (DEFAULT=0.0)
deadline: Date (NOT NULL)
created_at: DateTime (UTC)
```
**Relationships:** None (standalone entity)

### BankConnection (`bank.py`)
```python
id: Integer (PK)
bank_name: String (NOT NULL)
account_name: String (NOT NULL)
account_type: String (NOT NULL)  # "checking", "savings", "credit"
balance: Float (DEFAULT=0.0)
last_synced: DateTime (nullable)
is_active: Boolean (DEFAULT=True)
created_at: DateTime (UTC)
```
**Relationships:** `pending_transactions` → PendingTransaction[] (one-to-many, cascade delete)

### PendingTransaction (`bank.py`)
```python
id: Integer (PK)
bank_connection_id: Integer (FK → bank_connections.id, NOT NULL)
external_id: String (NOT NULL)   # Bank's transaction ID (deduplication)
amount: Float (NOT NULL)
merchant_name: String (NOT NULL)
date: String (NOT NULL)          # "YYYY-MM-DD"
suggested_category_id: Integer (FK → categories.id, nullable)
status: String (DEFAULT="pending")  # "pending", "imported", "dismissed"
created_at: DateTime (UTC)
```
**Relationships:** `bank_connection` → BankConnection, `suggested_category` → Category

## Entity Relationship Diagram

```
UserSettings (singleton)

Category (1) ←─────┬── (M) Transaction
                   ├── (M) Budget
                   ├── (M) RecurringTransaction
                   └── (M) PendingTransaction (suggested)

Goal (standalone)

BankConnection (1) ←── (M) PendingTransaction (cascade delete)
```

## Usage Pattern

```python
from app.models import Category, Transaction, Budget
from app.database import get_db
from sqlalchemy.orm import Session

def get_transactions(db: Session):
    return db.query(Transaction).join(Category).all()
```

## Key Design Decisions

1. **Timezone-aware timestamps:** All `created_at` use `datetime.now(timezone.utc)`
2. **Soft type enums:** Type fields stored as strings (not Python enums)
3. **Month as string:** Budgets use "YYYY-MM" format for easy querying
4. **Cascade delete:** Only PendingTransaction cascades from BankConnection
5. **No updated_at:** Models lack update tracking (potential improvement)
