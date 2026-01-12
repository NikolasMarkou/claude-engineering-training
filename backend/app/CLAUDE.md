# Backend App - CLAUDE.md

## Overview

Core application module containing the FastAPI app instance, configuration, database setup, and all submodules for models, schemas, routers, services, and utilities.

## Entry Points

### main.py
- Creates FastAPI app instance
- Configures CORS middleware (allows localhost:5173)
- Registers all API routers under `/api` prefix
- Initializes database tables on startup
- Seeds default categories on first run
- Health check endpoint at `/api/health`

### config.py
- Pydantic Settings for configuration management
- Loads from environment variables and `.env` file
- Settings: app_name, database_url, secret_key, algorithm, token expiration, default currency

### database.py
- SQLAlchemy engine creation with SQLite
- SessionLocal factory for database sessions
- `get_db()` dependency for FastAPI route injection
- Base class for ORM model inheritance

## Submodules

| Directory | Purpose |
|-----------|---------|
| `models/` | SQLAlchemy ORM model definitions |
| `schemas/` | Pydantic request/response validation |
| `routers/` | API endpoint handlers |
| `services/` | Business logic and external services |
| `utils/` | Shared utility functions |

## Request Flow

```
HTTP Request
    → CORS Middleware
    → Router (path matching)
    → Endpoint Handler
    → Database Session (via Depends)
    → Pydantic Response Serialization
    → HTTP Response
```

## Startup Sequence

1. Database tables created via `Base.metadata.create_all()`
2. Default categories seeded via `seed_default_categories()`
3. CORS middleware configured
4. All routers registered
5. App ready to serve requests
