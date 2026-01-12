from sqlalchemy.orm import Session

from app.models import Category

DEFAULT_CATEGORIES = [
    # Expenses
    {"name": "Food & Dining", "type": "expense", "icon": "utensils", "color": "#FF6B6B"},
    {"name": "Transportation", "type": "expense", "icon": "car", "color": "#4ECDC4"},
    {"name": "Housing", "type": "expense", "icon": "home", "color": "#45B7D1"},
    {"name": "Utilities", "type": "expense", "icon": "bolt", "color": "#96CEB4"},
    {"name": "Healthcare", "type": "expense", "icon": "heart", "color": "#FF8B94"},
    {"name": "Entertainment", "type": "expense", "icon": "film", "color": "#9B59B6"},
    {"name": "Shopping", "type": "expense", "icon": "shopping-bag", "color": "#F39C12"},
    {"name": "Personal Care", "type": "expense", "icon": "spa", "color": "#E74C3C"},
    {"name": "Education", "type": "expense", "icon": "book", "color": "#3498DB"},
    {"name": "Other Expense", "type": "expense", "icon": "ellipsis-h", "color": "#95A5A6"},
    # Income
    {"name": "Salary", "type": "income", "icon": "briefcase", "color": "#2ECC71"},
    {"name": "Freelance", "type": "income", "icon": "laptop", "color": "#1ABC9C"},
    {"name": "Investments", "type": "income", "icon": "chart-line", "color": "#27AE60"},
    {"name": "Gifts", "type": "income", "icon": "gift", "color": "#F1C40F"},
    {"name": "Other Income", "type": "income", "icon": "plus-circle", "color": "#16A085"},
]


def seed_default_categories(db: Session) -> None:
    """Seed default categories if they don't exist."""
    existing = db.query(Category).filter(Category.is_default == True).count()
    if existing > 0:
        return  # Already seeded

    for cat_data in DEFAULT_CATEGORIES:
        category = Category(**cat_data, is_default=True)
        db.add(category)

    db.commit()
