from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.routers import auth, transactions, categories, budgets, recurring, goals, reports, import_export, banking
from app.services.seed import seed_default_categories

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed default categories
db = SessionLocal()
try:
    seed_default_categories(db)
finally:
    db.close()

app = FastAPI(title=settings.app_name)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # SvelteKit dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(budgets.router, prefix="/api/budgets", tags=["budgets"])
app.include_router(recurring.router, prefix="/api/recurring", tags=["recurring"])
app.include_router(goals.router, prefix="/api/goals", tags=["goals"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(import_export.router, prefix="/api/import", tags=["import"])
app.include_router(banking.router, prefix="/api/banking", tags=["banking"])


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
