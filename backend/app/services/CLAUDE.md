# Services - CLAUDE.md

## Overview

Business logic services separated from API handlers. Contains data seeding and mock Open Banking implementation.

## Service Files

### seed.py - Default Category Seeding

Seeds 15 default categories on application startup.

**Expense Categories (10):**
| Name | Icon | Color |
|------|------|-------|
| Food & Dining | utensils | #e74c3c |
| Transportation | car | #3498db |
| Housing | home | #9b59b6 |
| Utilities | bolt | #f1c40f |
| Healthcare | medkit | #1abc9c |
| Entertainment | film | #e91e63 |
| Shopping | shopping-bag | #ff9800 |
| Personal Care | spa | #00bcd4 |
| Education | graduation-cap | #673ab7 |
| Other Expense | ellipsis-h | #95a5a6 |

**Income Categories (5):**
| Name | Icon | Color |
|------|------|-------|
| Salary | briefcase | #27ae60 |
| Freelance | laptop | #2ecc71 |
| Investments | chart-line | #16a085 |
| Gifts | gift | #e74c3c |
| Other Income | plus-circle | #3498db |

**Usage:**
```python
from app.services.seed import seed_default_categories
from app.database import SessionLocal

db = SessionLocal()
seed_default_categories(db)
```

### mock_bank_service.py - Open Banking Simulation

Simulates real Open Banking API for demonstration purposes.

**Available Mock Banks:**
- Chase Bank (Checking, Savings)
- Bank of America (Checking, Savings, Credit Card)
- Wells Fargo (Checking)
- Capital One (Savings, Credit Card)

**Mock Merchants (40 total):**
Organized by category with realistic amount ranges:

| Category | Merchants | Amount Range |
|----------|-----------|--------------|
| Food & Dining | Starbucks, McDonald's, Chipotle, Whole Foods, Trader Joe's | $4-$150 |
| Shopping | Amazon, Walmart, Target, Best Buy | $15-$300 |
| Entertainment | Netflix, Spotify, AMC Theatres | $10-$50 |
| Transportation | Shell Gas, Uber, Lyft | $15-$80 |
| Utilities | Electric Company, Water Utility, Internet Provider | $50-$200 |
| Healthcare | CVS Pharmacy, Walgreens | $10-$100 |
| Income | Payroll Deposit, Freelance Payment | $500-$5000 |

**Functions:**

`generate_mock_balance(account_type: str) -> float`
- Checking: $500-$8,000
- Savings: $1,000-$25,000
- Credit: -$3,000 to $0 (debt as negative)

`generate_mock_transactions(count: int) -> list[dict]`
- Generates 5-15 realistic transactions
- Random merchants from database
- Dates within last 30 days
- UUID external_id for deduplication

`suggest_category(merchant_name: str, db: Session) -> int | None`
- Maps merchant names to categories
- Case-insensitive substring matching
- Falls back to "Other Expense" if no match
- Returns category_id

**Example Transaction:**
```python
{
    "external_id": "uuid-string",
    "merchant_name": "Starbucks",
    "amount": 7.50,
    "date": "2026-01-10",
    "type": "expense"
}
```
