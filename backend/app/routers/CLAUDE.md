# Routers - CLAUDE.md

## Overview

FastAPI routers defining all API endpoints. Each router handles a specific domain and is registered in `main.py` with the `/api` prefix.

## Router Files

### auth.py - `/api/auth`
PIN-based authentication endpoints.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/status` | Check if PIN is set up, return currency |
| POST | `/setup` | Initial PIN setup, returns JWT token |
| POST | `/login` | Authenticate with PIN, returns JWT token |
| POST | `/change-pin` | Change existing PIN |

### transactions.py - `/api/transactions`
Transaction CRUD operations.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List transactions (filters: start_date, end_date, category_id, type) |
| POST | `/` | Create new transaction |
| PUT | `/{id}` | Update transaction |
| DELETE | `/{id}` | Delete transaction |

### categories.py - `/api/categories`
Category management with default protection.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List all categories |
| POST | `/` | Create custom category |
| PUT | `/{id}` | Update category |
| DELETE | `/{id}` | Delete (fails for default categories) |

### budgets.py - `/api/budgets`
Monthly budget tracking.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Get budgets for month (query: month=YYYY-MM) |
| POST | `/` | Create/update budget (upsert) |
| GET | `/status` | Get spending status with progress |
| DELETE | `/{id}` | Delete budget |

### recurring.py - `/api/recurring`
Recurring transaction management.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List all recurring transactions |
| POST | `/` | Create recurring transaction |
| PUT | `/{id}` | Update recurring transaction |
| DELETE | `/{id}` | Delete recurring transaction |
| POST | `/process` | Process all due recurring transactions |

### goals.py - `/api/goals`
Savings goals with contributions.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List goals with progress metrics |
| POST | `/` | Create savings goal |
| PUT | `/{id}` | Update goal |
| POST | `/{id}/contribute` | Add contribution to goal |
| DELETE | `/{id}` | Delete goal |

### reports.py - `/api/reports`
Financial analytics and summaries.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/monthly-summary` | Income, expenses, net for month |
| GET | `/category-breakdown` | Spending per category for month |
| GET | `/trends` | Historical income/expense trends (1-24 months) |

### import_export.py - `/api/import`
CSV import with validation.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/csv` | Upload CSV, returns preview with validation |
| POST | `/confirm` | Confirm and import validated rows |

### banking.py - `/api/banking`
Open Banking integration (mock).

| Method | Path | Description |
|--------|------|-------------|
| GET | `/banks` | List available mock banks |
| GET | `/connections` | List active bank connections |
| POST | `/connections` | Connect new bank account |
| DELETE | `/connections/{id}` | Disconnect bank |
| POST | `/connections/{id}/sync` | Sync transactions from bank |
| GET | `/pending` | List pending transactions for review |
| POST | `/pending/{id}/import` | Import single pending transaction |
| POST | `/pending/{id}/dismiss` | Dismiss pending transaction |
| POST | `/pending/import-all` | Bulk import all pending |
| GET | `/balances` | Get all account balances |

## Common Patterns

### Database Dependency
```python
@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### Response Models
```python
@router.get("/items/{id}", response_model=ItemResponse)
def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

### Query Parameters
```python
@router.get("/items")
def get_items(
    start_date: date | None = None,
    category_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Item)
    if start_date:
        query = query.filter(Item.date >= start_date)
    if category_id:
        query = query.filter(Item.category_id == category_id)
    return query.all()
```
