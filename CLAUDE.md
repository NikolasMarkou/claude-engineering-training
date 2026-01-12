# Budget App - CLAUDE.md

> **Location:** Project Root
> **Children:** [`backend/`](backend/CLAUDE.md), [`frontend/`](frontend/CLAUDE.md)

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

Budget App is a full-stack personal finance management application. It provides comprehensive tools for tracking income and expenses, setting monthly budgets, managing recurring transactions, tracking savings goals, and analyzing spending patterns through visual reports.

### Key Features

| Feature | Description |
|---------|-------------|
| Transaction Tracking | Income/expense CRUD with categories, filtering |
| Monthly Budgets | Spending limits per category with progress tracking |
| Recurring Transactions | Automated daily/weekly/monthly/yearly scheduling |
| Savings Goals | Target amounts with deadlines and contributions |
| Visual Reports | Chart.js analytics (income/expense trends, category breakdown) |
| Open Banking | Mock bank integration for transaction import |
| CSV Import | Bulk transaction import with preview/confirm |
| PIN Authentication | Simple single-user auth with JWT tokens |

---

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **Backend** | FastAPI | Latest |
| **ORM** | SQLAlchemy | Latest |
| **Database** | SQLite | 3.x |
| **Validation** | Pydantic | v2 |
| **Auth** | JWT + bcrypt | - |
| **Frontend** | SvelteKit | 2.x |
| **UI Framework** | Svelte | 5.x |
| **Language** | TypeScript | 5.x |
| **Charts** | Chart.js | 4.x |
| **Python** | Python | 3.10+ |

---

## Quick Start

### Backend

```bash
cd backend
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**URLs:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend

```bash
cd frontend
npm install
npm run dev
```

**URL:** http://localhost:5173

---

## Project Structure

```
budget-app/
├── backend/                    # FastAPI backend
│   ├── app/                   # Main application package
│   │   ├── main.py           # Entry point, CORS, routers
│   │   ├── config.py         # Pydantic settings
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models/           # 8 ORM models
│   │   ├── schemas/          # 28 Pydantic schemas
│   │   ├── routers/          # 9 routers, 41 endpoints
│   │   ├── services/         # Business logic
│   │   └── utils/            # Security utilities
│   ├── requirements.txt      # Python dependencies
│   └── budget.db             # SQLite database (auto-created)
│
├── frontend/                   # SvelteKit frontend
│   ├── src/
│   │   ├── lib/              # Shared library ($lib)
│   │   │   ├── api/         # REST client (38 methods)
│   │   │   └── stores/      # Svelte stores
│   │   └── routes/           # 10 pages
│   ├── package.json          # Node dependencies
│   └── svelte.config.js      # SvelteKit config
│
├── CLAUDE.md                   # This file (root documentation)
├── README.md                   # GitHub readme
└── CHANGELOG.md               # Version history
```

---

## Architecture Overview

### Data Flow

```
User Interface (SvelteKit)
        ↓
    API Client ($lib/api/client.ts)
        ↓
    HTTP Requests (fetch + JWT)
        ↓
    FastAPI Backend (routers/)
        ↓
    Business Logic (services/)
        ↓
    SQLAlchemy ORM (models/)
        ↓
    SQLite Database (budget.db)
```

### Backend Architecture

| Component | Location | Count | Purpose |
|-----------|----------|-------|---------|
| Models | `backend/app/models/` | 8 | Database tables (ORM) |
| Schemas | `backend/app/schemas/` | 28 | Request/response validation |
| Routers | `backend/app/routers/` | 9 | API endpoint handlers |
| Services | `backend/app/services/` | 2 | Business logic |
| Utils | `backend/app/utils/` | 1 | Security (PIN, JWT) |

### Frontend Architecture

| Component | Location | Count | Purpose |
|-----------|----------|-------|---------|
| Pages | `frontend/src/routes/` | 10 | SvelteKit routes |
| API Client | `frontend/src/lib/api/` | 38 methods | Backend communication |
| Stores | `frontend/src/lib/stores/` | 2 | Reactive state |
| Types | `frontend/src/lib/api/types.ts` | 16 | TypeScript interfaces |

---

## API Endpoints Summary

| Router | Prefix | Endpoints | Description |
|--------|--------|-----------|-------------|
| Auth | `/api/auth` | 4 | PIN setup, login, status, change |
| Transactions | `/api/transactions` | 4 | Income/expense CRUD |
| Categories | `/api/categories` | 4 | Category management |
| Budgets | `/api/budgets` | 4 | Monthly budget tracking |
| Recurring | `/api/recurring` | 5 | Scheduled transactions |
| Goals | `/api/goals` | 5 | Savings goal tracking |
| Reports | `/api/reports` | 3 | Financial analytics |
| Import | `/api/import` | 2 | CSV import |
| Banking | `/api/banking` | 10 | Open Banking (mock) |

**Total: 41 endpoints**

---

## Database Schema

### Tables (8)

| Table | Model | Primary Fields |
|-------|-------|----------------|
| `user_settings` | UserSettings | id, pin_hash, created_at |
| `categories` | Category | id, name, type, is_default |
| `transactions` | Transaction | id, amount, type, category_id, date |
| `budgets` | Budget | id, category_id, amount, month |
| `recurring_transactions` | RecurringTransaction | id, amount, frequency, next_date |
| `goals` | Goal | id, name, target_amount, current_amount |
| `bank_connections` | BankConnection | id, bank_name, account_mask |
| `pending_transactions` | PendingTransaction | id, connection_id, external_id |

---

## Configuration

### Backend Environment Variables

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./budget.db
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DEFAULT_CURRENCY=USD
```

### Frontend

No environment variables required. API base URL defaults to `http://localhost:8000`.

---

## Documentation Map

This project uses hierarchical CLAUDE.md files for comprehensive documentation.

### Backend Documentation

```
backend/CLAUDE.md                    # Backend overview
└── backend/app/CLAUDE.md           # Core app module
    ├── backend/app/models/CLAUDE.md      # ORM models (8)
    ├── backend/app/schemas/CLAUDE.md     # Pydantic schemas (28)
    ├── backend/app/routers/CLAUDE.md     # API endpoints (41)
    ├── backend/app/services/CLAUDE.md    # Business logic
    └── backend/app/utils/CLAUDE.md       # Security utilities
```

### Frontend Documentation

```
frontend/CLAUDE.md                   # Frontend overview
└── frontend/src/CLAUDE.md          # Source directory
    ├── frontend/src/lib/CLAUDE.md        # Shared library
    │   ├── frontend/src/lib/api/CLAUDE.md    # API client
    │   └── frontend/src/lib/stores/CLAUDE.md # Svelte stores
    └── frontend/src/routes/CLAUDE.md     # Pages (10)
```

---

## Development Notes

### Security Considerations

1. **SECRET_KEY**: Change in production
2. **CORS**: Configured for localhost:5173 only
3. **JWT**: 7-day token expiry
4. **Single-user**: No multi-tenancy

### Database

- Auto-created on first run
- 15 default categories seeded automatically
- Located at `backend/budget.db`

### Svelte 5 Features

The frontend uses Svelte 5 runes:
- `$state()` - Reactive state
- `$derived()` - Computed values
- `$effect()` - Side effects
- `$props()` - Component props

---

## Related Files

- [README.md](README.md) - GitHub project readme
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [backend/CLAUDE.md](backend/CLAUDE.md) - Backend documentation
- [frontend/CLAUDE.md](frontend/CLAUDE.md) - Frontend documentation
