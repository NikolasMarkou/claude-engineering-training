# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Budget App - A personal budgeting application with transaction tracking, monthly budgets, recurring transactions, savings goals, and visual analytics.

## Tech Stack

- **Backend**: FastAPI + SQLite + SQLAlchemy
- **Frontend**: SvelteKit (Svelte 5)
- **Python**: 3.10+ with virtual environment

## Commands

### Backend

```bash
# Activate virtual environment
cd backend
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000

# The API is available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# The app is available at http://localhost:5173
```

## Architecture

### Backend (`backend/app/`)

- `main.py` - FastAPI app entry point, CORS config, router registration
- `config.py` - Settings via pydantic-settings
- `database.py` - SQLAlchemy engine and session setup
- `models/` - SQLAlchemy ORM models (UserSettings, Category, Transaction, Budget, RecurringTransaction, Goal, BankConnection, PendingTransaction)
- `schemas/` - Pydantic request/response schemas
- `routers/` - API endpoint handlers (auth, transactions, categories, budgets, recurring, goals, reports, import_export, banking)
- `services/` - Business logic (seed.py for default categories, mock_bank_service.py for Open Banking simulation)
- `utils/security.py` - PIN hashing and JWT token handling

### Frontend (`frontend/src/`)

- `lib/api/` - API client and TypeScript types
- `lib/stores/` - Svelte stores for auth and categories
- `routes/` - SvelteKit pages (dashboard, transactions, banking, budgets, recurring, goals, reports, settings, login)

### API Endpoints

- `/api/auth/*` - PIN setup, login, change
- `/api/transactions/*` - CRUD with date/category/type filters
- `/api/categories/*` - CRUD (default categories protected)
- `/api/budgets/*` - Monthly budgets with status tracking
- `/api/recurring/*` - Auto-generated recurring transactions
- `/api/goals/*` - Savings goals with contribution tracking
- `/api/reports/*` - Monthly summary, category breakdown, trends
- `/api/import/*` - CSV import with preview/confirm flow
- `/api/banking/*` - Open Banking (mock) - connect accounts, sync transactions, review and import

## Database

SQLite database stored at `backend/budget.db`. Tables are auto-created on startup. Default categories are seeded automatically.
