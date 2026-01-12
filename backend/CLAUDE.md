# Backend - CLAUDE.md

## Overview

FastAPI backend for the Budget App. Provides REST API endpoints for personal finance management including transactions, budgets, recurring transactions, savings goals, reports, and Open Banking integration.

## Tech Stack

- **Framework**: FastAPI (async Python web framework)
- **ORM**: SQLAlchemy with SQLite database
- **Validation**: Pydantic schemas
- **Authentication**: JWT tokens with bcrypt password hashing
- **Server**: Uvicorn ASGI server

## Directory Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Settings and configuration
│   ├── database.py      # SQLAlchemy engine and session
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── routers/         # API endpoint handlers
│   ├── services/        # Business logic services
│   └── utils/           # Utility functions
├── requirements.txt     # Python dependencies
├── venv/                # Virtual environment
└── budget.db            # SQLite database (auto-created)
```

## Running the Backend

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/api/health

## Key Features

- PIN-based authentication with JWT tokens
- 9 API routers covering all financial operations
- 8 database models with relationships
- Auto-seeding of 15 default categories on startup
- Mock Open Banking service for demonstration
- CSV import with preview and validation

## Environment Variables

Create `.env` file to override defaults:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./budget.db
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DEFAULT_CURRENCY=USD
```
