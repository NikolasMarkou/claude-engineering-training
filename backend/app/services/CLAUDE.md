# Services - CLAUDE.md

> **Location:** `backend/app/services/`
> **Parent:** [`backend/app/`](../CLAUDE.md)
> **Siblings:** [`models/`](../models/CLAUDE.md), [`schemas/`](../schemas/CLAUDE.md), [`routers/`](../routers/CLAUDE.md), [`utils/`](../utils/CLAUDE.md)

## Purpose

Business logic services separated from API handlers. Contains data seeding and mock Open Banking implementation.

---

## seed.py - Default Category Seeding

### Constant: `DEFAULT_CATEGORIES`

15 default categories seeded on application startup:

**Expense Categories (10):**

| Name | Icon | Color | Type |
|------|------|-------|------|
| Food & Dining | `utensils` | `#FF6B6B` | expense |
| Transportation | `car` | `#4ECDC4` | expense |
| Housing | `home` | `#45B7D1` | expense |
| Utilities | `bolt` | `#96CEB4` | expense |
| Healthcare | `heart` | `#FF8B94` | expense |
| Entertainment | `film` | `#9B59B6` | expense |
| Shopping | `shopping-bag` | `#F39C12` | expense |
| Personal Care | `spa` | `#E74C3C` | expense |
| Education | `book` | `#3498DB` | expense |
| Other Expense | `ellipsis-h` | `#95A5A6` | expense |

**Income Categories (5):**

| Name | Icon | Color | Type |
|------|------|-------|------|
| Salary | `briefcase` | `#2ECC71` | income |
| Freelance | `laptop` | `#1ABC9C` | income |
| Investments | `chart-line` | `#27AE60` | income |
| Gifts | `gift` | `#F1C40F` | income |
| Other Income | `plus-circle` | `#16A085` | income |

### Function: `seed_default_categories(db: Session) -> None`

**Purpose:** Idempotent seeding of default categories
**Called from:** `main.py` on application startup

```python
def seed_default_categories(db: Session) -> None:
    # Check if already seeded
    existing = db.query(Category).filter(Category.is_default == True).count()
    if existing > 0:
        return  # Prevent duplicates

    # Create all default categories
    for cat_data in DEFAULT_CATEGORIES:
        category = Category(**cat_data, is_default=True)
        db.add(category)

    db.commit()
```

---

## mock_bank_service.py - Open Banking Simulation

### Constant: `MOCK_BANKS`

```python
[
    {"name": "Chase Bank", "accounts": ["Checking", "Savings"]},
    {"name": "Bank of America", "accounts": ["Checking", "Savings", "Credit Card"]},
    {"name": "Wells Fargo", "accounts": ["Checking"]},
    {"name": "Capital One", "accounts": ["Savings", "Credit Card"]},
]
```

### Constant: `MOCK_MERCHANTS`

40 merchants organized by category with amount ranges:

| Category | Merchants | Amount Range |
|----------|-----------|--------------|
| Food & Dining | Starbucks, McDonald's, Chipotle, Whole Foods, Trader Joe's | $4-$150 |
| Shopping | Amazon, Walmart, Target, Best Buy | $15-$500 |
| Entertainment | Netflix, Spotify, AMC Theatres | $10-$50 |
| Transportation | Shell Gas, Uber, Lyft | $10-$80 |
| Utilities | Electric, Water, Internet | $30-$200 |
| Healthcare | CVS, Walgreens | $10-$100 |
| Income | Payroll, Freelance | $200-$5000 |

### Function: `get_available_banks() -> list[dict]`

Returns `MOCK_BANKS` list for UI dropdown.

### Function: `generate_mock_balance(account_type: str) -> float`

| Account Type | Balance Range |
|--------------|---------------|
| `checking` | $500 - $8,000 |
| `savings` | $1,000 - $25,000 |
| `credit` | -$3,000 - $0 (debt) |
| default | $1,000 - $5,000 |

### Function: `suggest_category(merchant_name: str, db: Session) -> int | None`

**Logic:**
1. Case-insensitive substring matching against `MOCK_MERCHANTS`
2. Query database for matching category by name
3. Fallback to "Other Expense" if no match
4. Returns `category_id` or `None`

```python
# Example: "Starbucks Coffee" → matches "Starbucks" → "Food & Dining" category
```

### Function: `generate_mock_transactions(count: int = 10) -> list[dict]`

**Returns:** List of mock transactions sorted by date (newest first)

```python
{
    "external_id": "uuid-string",      # For deduplication
    "merchant_name": "Starbucks",
    "amount": 7.50,
    "date": "2026-01-10",              # ISO format
    "type": "expense",                 # or "income"
    "category_hint": "Food & Dining",
}
```

**Generation:**
- Random merchant from `MOCK_MERCHANTS`
- Date: Today minus 0-30 days (random)
- Amount: Random within merchant's min-max range
- UUID external_id for deduplication

---

## Usage in Routers

```python
# In banking.py
from app.services.mock_bank_service import (
    get_available_banks,
    generate_mock_balance,
    generate_mock_transactions,
    suggest_category,
)

# Sync endpoint uses all functions
@router.post("/connections/{id}/sync")
def sync_connection(id: int, db: Session = Depends(get_db)):
    transactions = generate_mock_transactions(random.randint(5, 15))
    for tx in transactions:
        category_id = suggest_category(tx["merchant_name"], db)
        # Create PendingTransaction with suggested category
```

---

## Extension Points

To integrate real Open Banking:
1. Replace `get_available_banks()` with API call to provider
2. Replace `generate_mock_balance()` with real balance fetch
3. Replace `generate_mock_transactions()` with actual transaction sync
4. Keep `suggest_category()` for auto-categorization (or enhance with ML)
