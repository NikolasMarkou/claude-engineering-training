# Models - CLAUDE.md

## Overview

SQLAlchemy ORM models defining the database schema. All models inherit from `Base` (declarative base) and are automatically created as tables on application startup.

## Models

### user.py - UserSettings
Single-user application settings and authentication.
- `pin_hash`: Bcrypt-hashed PIN for authentication
- `currency`: User's preferred currency (default: USD)
- `created_at`: Account creation timestamp

### category.py - Category
Transaction categories for organizing income/expenses.
- `name`: Category name (e.g., "Food & Dining")
- `type`: "income" or "expense"
- `is_default`: Protected from deletion if true
- `icon`: Font Awesome icon identifier
- `color`: Hex color code for UI display

### transaction.py - Transaction
Individual financial transactions.
- `amount`: Transaction amount (float)
- `type`: "income" or "expense"
- `category_id`: Foreign key to Category
- `description`: Optional notes
- `date`: Transaction date

### budget.py - Budget
Monthly spending limits per category.
- `category_id`: Foreign key to Category
- `amount`: Budget limit
- `month`: Format "YYYY-MM" for easy querying

### recurring.py - RecurringTransaction
Automated recurring income/expenses.
- `amount`, `type`, `category_id`, `description`: Transaction template
- `frequency`: "daily", "weekly", or "monthly"
- `next_run_date`: Next scheduled execution
- `is_active`: Enable/disable toggle

### goal.py - Goal
Savings goals with progress tracking.
- `name`: Goal name
- `target_amount`: Savings target
- `current_amount`: Progress (default 0.0)
- `deadline`: Target completion date

### bank.py - BankConnection & PendingTransaction
Open Banking integration models.

**BankConnection:**
- `bank_name`, `account_name`, `account_type`
- `balance`: Current account balance
- `last_synced`: Last sync timestamp
- `is_active`: Connection status

**PendingTransaction:**
- `bank_connection_id`: Foreign key to BankConnection
- `external_id`: Bank's transaction ID (for deduplication)
- `merchant_name`, `amount`, `date`
- `suggested_category_id`: Auto-suggested category
- `status`: "pending", "imported", or "dismissed"

## Relationships

```
Category (1) ←── (M) Transaction
Category (1) ←── (M) Budget
Category (1) ←── (M) RecurringTransaction
Category (1) ←── (M) PendingTransaction (suggested_category)
BankConnection (1) ←── (M) PendingTransaction (cascade delete)
```

## Usage

```python
from app.models import Category, Transaction, Budget
from app.database import get_db

# In a route handler
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()
```
