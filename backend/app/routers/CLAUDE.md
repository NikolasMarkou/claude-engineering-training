# Routers - CLAUDE.md

> **Location:** `backend/app/routers/`
> **Parent:** [`backend/app/`](../CLAUDE.md)
> **Siblings:** [`models/`](../models/CLAUDE.md), [`schemas/`](../schemas/CLAUDE.md), [`services/`](../services/CLAUDE.md), [`utils/`](../utils/CLAUDE.md)

## Purpose

FastAPI routers defining all API endpoints. Each router handles a specific domain and is registered in `main.py` with the `/api` prefix.

## Endpoint Summary (41 total)

| Router | File | Prefix | Endpoints |
|--------|------|--------|-----------|
| Auth | `auth.py` | `/api/auth` | 4 |
| Transactions | `transactions.py` | `/api/transactions` | 4 |
| Categories | `categories.py` | `/api/categories` | 4 |
| Budgets | `budgets.py` | `/api/budgets` | 4 |
| Recurring | `recurring.py` | `/api/recurring` | 5 |
| Goals | `goals.py` | `/api/goals` | 5 |
| Reports | `reports.py` | `/api/reports` | 3 |
| Import/Export | `import_export.py` | `/api/import` | 2 |
| Banking | `banking.py` | `/api/banking` | 10 |

---

## auth.py - Authentication

| Method | Path | Function | Request | Response | Status |
|--------|------|----------|---------|----------|--------|
| GET | `/status` | `get_status` | - | `UserSettingsResponse` | 200 |
| POST | `/setup` | `setup_pin` | `PinSetup` | `Token` | 201 |
| POST | `/login` | `login` | `PinLogin` | `Token` | 200 |
| POST | `/change-pin` | `change_pin` | `PinChange` | `{message}` | 200 |

**Logic:** Hash PIN with bcrypt, generate JWT tokens, verify PIN on login/change.

---

## transactions.py - Transaction CRUD

| Method | Path | Function | Request | Response | Status |
|--------|------|----------|---------|----------|--------|
| GET | `/` | `list_transactions` | Query params | `list[TransactionResponse]` | 200 |
| POST | `/` | `create_transaction` | `TransactionCreate` | `TransactionResponse` | 201 |
| PUT | `/{id}` | `update_transaction` | `TransactionUpdate` | `TransactionResponse` | 200 |
| DELETE | `/{id}` | `delete_transaction` | - | - | 204 |

**Query Parameters:** `start_date`, `end_date`, `category_id`, `type`
**Logic:** Filter by date range/category/type, order by date DESC.

---

## categories.py - Category Management

| Method | Path | Function | Request | Response | Status |
|--------|------|----------|---------|----------|--------|
| GET | `/` | `list_categories` | - | `list[CategoryResponse]` | 200 |
| POST | `/` | `create_category` | `CategoryCreate` | `CategoryResponse` | 201 |
| PUT | `/{id}` | `update_category` | `CategoryUpdate` | `CategoryResponse` | 200 |
| DELETE | `/{id}` | `delete_category` | - | - | 204 |

**Protection:** Default categories (`is_default=True`) cannot be deleted (400 error).

---

## budgets.py - Monthly Budgets

| Method | Path | Function | Request | Response | Status |
|--------|------|----------|---------|----------|--------|
| GET | `/` | `list_budgets` | `?month=YYYY-MM` | `list[BudgetResponse]` | 200 |
| POST | `/` | `create_or_update_budget` | `BudgetCreate` | `BudgetResponse` | 201 |
| GET | `/status` | `get_budget_status` | `?month=YYYY-MM` | `list[BudgetStatus]` | 200 |
| DELETE | `/{id}` | `delete_budget` | - | - | 204 |

**Upsert Logic:** Create updates existing budget if category+month combination exists.
**Status Calculation:** Aggregates expenses via `func.sum()`, computes remaining/percentage.

---

## recurring.py - Recurring Transactions

| Method | Path | Function | Request | Response | Status |
|--------|------|----------|---------|----------|--------|
| GET | `/` | `list_recurring` | - | `list[RecurringResponse]` | 200 |
| POST | `/` | `create_recurring` | `RecurringCreate` | `RecurringResponse` | 201 |
| PUT | `/{id}` | `update_recurring` | `RecurringUpdate` | `RecurringResponse` | 200 |
| DELETE | `/{id}` | `delete_recurring` | - | - | 204 |
| POST | `/process` | `process_recurring` | - | `{processed: int}` | 200 |

**Process Logic:** Creates Transaction records for due items, calculates next_run_date based on frequency (daily +1 day, weekly +7 days, monthly +1 month).

---

## goals.py - Savings Goals

| Method | Path | Function | Request | Response | Status |
|--------|------|----------|---------|----------|--------|
| GET | `/` | `list_goals` | - | `list[GoalResponse]` | 200 |
| POST | `/` | `create_goal` | `GoalCreate` | `GoalResponse` | 201 |
| PUT | `/{id}` | `update_goal` | `GoalUpdate` | `GoalResponse` | 200 |
| POST | `/{id}/contribute` | `contribute_to_goal` | `GoalContribute` | `GoalResponse` | 200 |
| DELETE | `/{id}` | `delete_goal` | - | - | 204 |

**Computed Fields:** `progress_percentage` and `days_remaining` calculated in helper function.

---

## reports.py - Analytics

| Method | Path | Function | Request | Response | Status |
|--------|------|----------|---------|----------|--------|
| GET | `/monthly-summary` | `monthly_summary` | `?month=YYYY-MM` | `{month, income, expenses, net}` | 200 |
| GET | `/category-breakdown` | `category_breakdown` | `?month=YYYY-MM` | `list[{category_id, name, type, total}]` | 200 |
| GET | `/trends` | `trends` | `?months=1-24` | `list[MonthlySummary]` | 200 |

**Aggregations:** Uses `func.sum()` and `group_by()` for analytics.

---

## import_export.py - CSV Import

| Method | Path | Function | Request | Response | Status |
|--------|------|----------|---------|----------|--------|
| POST | `/csv` | `upload_csv` | `UploadFile` | `{rows, errors}` | 200 |
| POST | `/confirm` | `confirm_import` | `{rows}` | `{created, errors}` | 200 |

**CSV Format:** Required columns: `date`, `amount`, `type`, `category`. Optional: `description`.
**Validation:** Date format, positive amounts, valid type, category existence.

---

## banking.py - Open Banking (10 endpoints)

| Method | Path | Function | Request | Response | Status |
|--------|------|----------|---------|----------|--------|
| GET | `/banks` | `list_available_banks` | - | `list[BankInfo]` | 200 |
| GET | `/connections` | `list_connections` | - | `list[BankConnectionResponse]` | 200 |
| POST | `/connections` | `create_connection` | `BankConnectionCreate` | `BankConnectionResponse` | 201 |
| DELETE | `/connections/{id}` | `delete_connection` | - | - | 204 |
| POST | `/connections/{id}/sync` | `sync_connection` | - | `{synced, balance}` | 200 |
| GET | `/pending` | `list_pending` | - | `list[PendingTransactionResponse]` | 200 |
| POST | `/pending/{id}/import` | `import_transaction` | `PendingTransactionImport` | `{message, transaction_id}` | 200 |
| POST | `/pending/{id}/dismiss` | `dismiss_transaction` | - | - | 204 |
| POST | `/pending/import-all` | `import_all_pending` | - | `{imported}` | 200 |
| GET | `/balances` | `get_balances` | - | `list[BankBalanceResponse]` | 200 |

**Sync Logic:** Generates mock transactions, checks external_id for deduplication, auto-suggests categories.

---

## Common Patterns

### Database Dependency
```python
@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### Partial Updates
```python
for key, value in data.model_dump(exclude_unset=True).items():
    setattr(item, key, value)
```

### Error Handling
```python
if not item:
    raise HTTPException(status_code=404, detail="Item not found")
```
