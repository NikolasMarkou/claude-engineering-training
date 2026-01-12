# Changelog

All notable changes to the Budget App project.

## [0.2.1] - 2026-01-12

### Documentation
- **Hierarchical CLAUDE.md Documentation**
  - Root CLAUDE.md with full project overview, architecture, and documentation map
  - Backend documentation tree (backend/, app/, models/, schemas/, routers/, services/, utils/)
  - Frontend documentation tree (frontend/, src/, lib/, api/, stores/, routes/)
  - Situational awareness links (Location, Parent, Children, Siblings) in all files
  - 14 CLAUDE.md files covering every module and subdirectory

---

## [0.2.0] - 2026-01-12

### Added
- **Open Banking Integration (Mock)**
  - Connect mock bank accounts (Chase, Bank of America, Wells Fargo, Capital One)
  - Sync transactions from connected accounts
  - Auto-categorization based on merchant names
  - Pending transaction review with category selection
  - Single and bulk import functionality
  - Account balance display
  - `/banking` page in frontend with account cards and transaction review UI

### Backend
- `models/bank.py` - BankConnection and PendingTransaction models
- `schemas/bank.py` - Banking Pydantic schemas
- `routers/banking.py` - Banking API endpoints
- `services/mock_bank_service.py` - Mock transaction generation service

### Frontend
- Banking page with connect/sync/review workflow
- Banking link added to navigation

---

## [0.1.0] - 2026-01-12

### Added
- **Core Budgeting Features**
  - PIN-based authentication with JWT tokens
  - Transaction management (income/expense) with categories
  - 15 default categories (10 expense, 5 income)
  - Monthly budgets with spending tracking
  - Recurring transactions with auto-generation (daily/weekly/monthly)
  - Savings goals with deadline and contribution tracking
  - Reports with charts (income vs expenses, category breakdown, 6-month trends)
  - CSV import with preview and confirmation

### Backend (FastAPI + SQLite)
- SQLAlchemy ORM models
- Pydantic schemas for validation
- RESTful API endpoints for all features
- bcrypt password hashing
- JWT token authentication

### Frontend (SvelteKit + Svelte 5)
- Responsive dashboard with summary cards
- Transaction list with filtering
- Budget management with progress bars
- Goal tracking with contributions
- Recurring transaction management
- Reports page with Chart.js visualizations
- Settings page (PIN change, category management, CSV import)
- Login/PIN setup flow

### Infrastructure
- Python virtual environment setup
- SQLite database with auto-migration
- Default category seeding on startup
