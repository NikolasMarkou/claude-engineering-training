# Backend App - CLAUDE.md

> **Location:** `backend/app/`
> **Parent:** [`backend/`](../CLAUDE.md)
> **Children:** [`models/`](models/CLAUDE.md), [`schemas/`](schemas/CLAUDE.md), [`routers/`](routers/CLAUDE.md), [`services/`](services/CLAUDE.md), [`utils/`](utils/CLAUDE.md)

## Purpose

Core FastAPI application module containing the app instance, configuration, database setup, and all submodules for the Budget App API.

---

## Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app entry point, middleware, routers |
| `config.py` | Pydantic Settings configuration |
| `database.py` | SQLAlchemy engine and session setup |

---

## main.py - Application Entry Point

### Startup Sequence

```python
# 1. Create database tables
Base.metadata.create_all(bind=engine)

# 2. Seed default categories
db = SessionLocal()
seed_default_categories(db)
db.close()

# 3. Create FastAPI app
app = FastAPI(title=settings.app_name)

# 4. Configure CORS
app.add_middleware(CORSMiddleware, ...)

# 5. Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# ... 8 more routers
```

### CORS Configuration

```python
allow_origins=["http://localhost:5173"]  # SvelteKit dev server
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

### Registered Routers

| Router | Prefix | Endpoints |
|--------|--------|-----------|
| auth | `/api/auth` | 4 |
| transactions | `/api/transactions` | 4 |
| categories | `/api/categories` | 4 |
| budgets | `/api/budgets` | 4 |
| recurring | `/api/recurring` | 5 |
| goals | `/api/goals` | 5 |
| reports | `/api/reports` | 3 |
| import_export | `/api/import` | 2 |
| banking | `/api/banking` | 10 |

### Health Check

```python
@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
```

---

## config.py - Settings

### Configuration Class

```python
class Settings(BaseSettings):
    app_name: str = "Budget App"
    database_url: str = "sqlite:///./budget.db"
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days
    default_currency: str = "USD"

    class Config:
        env_file = ".env"
```

### Environment Override

All settings can be overridden via:
- `.env` file in backend directory
- Environment variables

---

## database.py - Database Setup

### SQLAlchemy Configuration

```python
# Engine with SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for ORM models
Base = declarative_base()
```

### Dependency Injection

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Used in routers:
```python
@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

---

## Submodules

### models/
SQLAlchemy ORM models (8 models, 8 tables):
- UserSettings, Category, Transaction, Budget
- RecurringTransaction, Goal, BankConnection, PendingTransaction

### schemas/
Pydantic request/response schemas (28 classes):
- Base, Create, Update, Response patterns per domain

### routers/
API endpoint handlers (41 endpoints total):
- CRUD operations, reports, banking integration

### services/
Business logic:
- `seed.py` - Default category seeding (15 categories)
- `mock_bank_service.py` - Open Banking simulation (40 merchants, 4 banks)

### utils/
Utility functions:
- `security.py` - PIN hashing (bcrypt), JWT tokens

---

## Request Flow

```
HTTP Request
    ↓
CORS Middleware
    ↓
Router (path matching)
    ↓
Endpoint Handler (business logic)
    ↓
Database Session (Depends(get_db))
    ↓
Pydantic Response (serialization)
    ↓
HTTP Response
```

---

## Key Imports

```python
# In routers
from app.database import get_db
from app.models import Transaction, Category
from app.schemas import TransactionCreate, TransactionResponse
from app.utils.security import hash_pin, create_access_token
from app.services.mock_bank_service import suggest_category
```
