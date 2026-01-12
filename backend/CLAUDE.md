# Backend - CLAUDE.md

> **Location:** `backend/`
> **Parent:** [Project Root](../CLAUDE.md)
> **Children:** [`app/`](app/CLAUDE.md)
> **Siblings:** [`frontend/`](../frontend/CLAUDE.md)

## Purpose

FastAPI backend for the Budget App. Provides REST API endpoints for personal finance management including transactions, budgets, recurring transactions, savings goals, reports, and Open Banking integration.

---

## Directory Structure

```
backend/
├── app/                     # Main application package
│   ├── main.py             # FastAPI entry point
│   ├── config.py           # Settings configuration
│   ├── database.py         # SQLAlchemy setup
│   ├── models/             # ORM models (8 models)
│   ├── schemas/            # Pydantic schemas (28 classes)
│   ├── routers/            # API endpoints (41 endpoints)
│   ├── services/           # Business logic
│   └── utils/              # Security utilities
├── requirements.txt        # Python dependencies
├── venv/                   # Virtual environment
└── budget.db               # SQLite database (auto-created)
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| Validation | Pydantic |
| Auth | JWT + bcrypt |
| Server | Uvicorn |

---

## Quick Start

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000
```

---

## API Endpoints

**Base URL:** `http://localhost:8000/api`

| Category | Prefix | Endpoints | Description |
|----------|--------|-----------|-------------|
| Auth | `/auth` | 4 | PIN setup, login, change |
| Transactions | `/transactions` | 4 | Income/expense CRUD |
| Categories | `/categories` | 4 | Category management |
| Budgets | `/budgets` | 4 | Monthly budget tracking |
| Recurring | `/recurring` | 5 | Scheduled transactions |
| Goals | `/goals` | 5 | Savings goal tracking |
| Reports | `/reports` | 3 | Financial analytics |
| Import | `/import` | 2 | CSV import |
| Banking | `/banking` | 10 | Open Banking (mock) |

**Total:** 41 endpoints

---

## Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/api/health

---

## Database

**Location:** `backend/budget.db` (auto-created on first run)

### Tables (8)

| Table | Model | Purpose |
|-------|-------|---------|
| `user_settings` | UserSettings | PIN and preferences |
| `categories` | Category | Transaction categories |
| `transactions` | Transaction | Income/expenses |
| `budgets` | Budget | Monthly limits |
| `recurring_transactions` | RecurringTransaction | Scheduled items |
| `goals` | Goal | Savings targets |
| `bank_connections` | BankConnection | Connected accounts |
| `pending_transactions` | PendingTransaction | Awaiting import |

---

## Configuration

### Environment Variables (.env)

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./budget.db
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DEFAULT_CURRENCY=USD
```

### Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| `app_name` | "Budget App" | Application name |
| `database_url` | `sqlite:///./budget.db` | Database connection |
| `secret_key` | `"change-this-in-production"` | JWT signing key |
| `algorithm` | `"HS256"` | JWT algorithm |
| `access_token_expire_minutes` | `10080` | Token lifetime (7 days) |
| `default_currency` | `"USD"` | Default currency |

---

## Key Features

### Authentication
- PIN-based single-user auth
- Bcrypt password hashing
- JWT tokens (7-day expiry)

### Categories
- 15 default categories (10 expense, 5 income)
- Protected from deletion
- Custom categories supported

### Open Banking (Mock)
- 4 mock banks (Chase, BofA, Wells Fargo, Capital One)
- 40 mock merchants with realistic amounts
- Auto-categorization by merchant name
- Transaction deduplication via external_id

### Reports
- Monthly summary (income/expenses/net)
- Category breakdown
- 6-month trend analysis

---

## Dependencies

```
fastapi
uvicorn[standard]
sqlalchemy
pydantic
pydantic-settings
python-multipart
passlib[bcrypt]
bcrypt<5.0.0
python-jose[cryptography]
python-dateutil
```

---

## Security Notes

1. **Change SECRET_KEY** in production
2. **CORS** configured for localhost:5173 only
3. **No rate limiting** implemented
4. **JWT tokens** not verified on endpoints (development mode)
5. **Single-user** design (no multi-tenancy)

---

## Related Documentation

- [`app/`](app/CLAUDE.md) - Core application module
- [`app/models/`](app/models/CLAUDE.md) - Database models
- [`app/schemas/`](app/schemas/CLAUDE.md) - Request/response schemas
- [`app/routers/`](app/routers/CLAUDE.md) - API endpoints
- [`app/services/`](app/services/CLAUDE.md) - Business logic
- [`app/utils/`](app/utils/CLAUDE.md) - Security utilities
