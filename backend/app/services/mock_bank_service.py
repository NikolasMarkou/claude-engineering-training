import random
import uuid
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models import Category

# Mock merchants with their typical amounts and categories
MOCK_MERCHANTS = [
    # Food & Dining
    {"name": "Starbucks", "category": "Food & Dining", "min": 4, "max": 15, "type": "expense"},
    {"name": "McDonald's", "category": "Food & Dining", "min": 8, "max": 25, "type": "expense"},
    {"name": "Chipotle", "category": "Food & Dining", "min": 10, "max": 20, "type": "expense"},
    {"name": "Whole Foods", "category": "Food & Dining", "min": 30, "max": 150, "type": "expense"},
    {"name": "Trader Joe's", "category": "Food & Dining", "min": 25, "max": 100, "type": "expense"},
    # Shopping
    {"name": "Amazon", "category": "Shopping", "min": 15, "max": 200, "type": "expense"},
    {"name": "Walmart", "category": "Shopping", "min": 20, "max": 150, "type": "expense"},
    {"name": "Target", "category": "Shopping", "min": 25, "max": 120, "type": "expense"},
    {"name": "Best Buy", "category": "Shopping", "min": 50, "max": 500, "type": "expense"},
    # Entertainment
    {"name": "Netflix", "category": "Entertainment", "min": 15, "max": 23, "type": "expense"},
    {"name": "Spotify", "category": "Entertainment", "min": 10, "max": 16, "type": "expense"},
    {"name": "AMC Theatres", "category": "Entertainment", "min": 15, "max": 50, "type": "expense"},
    # Transportation
    {"name": "Shell Gas Station", "category": "Transportation", "min": 30, "max": 80, "type": "expense"},
    {"name": "Uber", "category": "Transportation", "min": 10, "max": 45, "type": "expense"},
    {"name": "Lyft", "category": "Transportation", "min": 12, "max": 40, "type": "expense"},
    # Utilities
    {"name": "Electric Company", "category": "Utilities", "min": 80, "max": 200, "type": "expense"},
    {"name": "Water Utility", "category": "Utilities", "min": 30, "max": 80, "type": "expense"},
    {"name": "Internet Provider", "category": "Utilities", "min": 50, "max": 100, "type": "expense"},
    # Healthcare
    {"name": "CVS Pharmacy", "category": "Healthcare", "min": 10, "max": 100, "type": "expense"},
    {"name": "Walgreens", "category": "Healthcare", "min": 10, "max": 80, "type": "expense"},
    # Income
    {"name": "Payroll - Direct Deposit", "category": "Salary", "min": 2000, "max": 5000, "type": "income"},
    {"name": "Freelance Payment", "category": "Freelance", "min": 200, "max": 2000, "type": "income"},
]

MOCK_BANKS = [
    {"name": "Chase Bank", "accounts": ["Checking", "Savings"]},
    {"name": "Bank of America", "accounts": ["Checking", "Savings", "Credit Card"]},
    {"name": "Wells Fargo", "accounts": ["Checking"]},
    {"name": "Capital One", "accounts": ["Savings", "Credit Card"]},
]


def get_available_banks() -> list[dict]:
    """Return list of mock banks available to connect."""
    return MOCK_BANKS


def generate_mock_balance(account_type: str) -> float:
    """Generate a realistic mock balance based on account type."""
    if account_type == "checking":
        return round(random.uniform(500, 8000), 2)
    elif account_type == "savings":
        return round(random.uniform(1000, 25000), 2)
    elif account_type == "credit":
        return round(random.uniform(-3000, 0), 2)  # Credit cards show negative (owed)
    return round(random.uniform(1000, 5000), 2)


def suggest_category(merchant_name: str, db: Session) -> int | None:
    """Suggest a category based on merchant name."""
    # Find matching merchant
    for merchant in MOCK_MERCHANTS:
        if merchant["name"].lower() in merchant_name.lower():
            # Find category in database
            category = db.query(Category).filter(
                Category.name == merchant["category"]
            ).first()
            if category:
                return category.id

    # Default to "Other Expense" if no match
    other = db.query(Category).filter(Category.name == "Other Expense").first()
    return other.id if other else None


def generate_mock_transactions(count: int = 10) -> list[dict]:
    """Generate a list of mock transactions."""
    transactions = []
    today = date.today()

    for _ in range(count):
        merchant = random.choice(MOCK_MERCHANTS)
        days_ago = random.randint(0, 30)
        tx_date = today - timedelta(days=days_ago)
        amount = round(random.uniform(merchant["min"], merchant["max"]), 2)

        transactions.append({
            "external_id": str(uuid.uuid4()),
            "merchant_name": merchant["name"],
            "amount": amount,
            "date": tx_date.isoformat(),
            "type": merchant["type"],
            "category_hint": merchant["category"],
        })

    # Sort by date descending
    transactions.sort(key=lambda x: x["date"], reverse=True)
    return transactions
