from datetime import date
from dateutil.relativedelta import relativedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Transaction, Category

router = APIRouter()


@router.get("/monthly-summary")
def monthly_summary(month: str = Query(..., description="Format: YYYY-MM"), db: Session = Depends(get_db)):
    year, month_num = month.split("-")
    start_date = f"{year}-{month_num}-01"

    if month_num == "12":
        end_date = f"{int(year)+1}-01-01"
    else:
        end_date = f"{year}-{int(month_num)+1:02d}-01"

    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "income",
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).scalar() or 0.0

    expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "expense",
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).scalar() or 0.0

    return {
        "month": month,
        "income": income,
        "expenses": expenses,
        "net": income - expenses
    }


@router.get("/category-breakdown")
def category_breakdown(month: str = Query(..., description="Format: YYYY-MM"), db: Session = Depends(get_db)):
    year, month_num = month.split("-")
    start_date = f"{year}-{month_num}-01"

    if month_num == "12":
        end_date = f"{int(year)+1}-01-01"
    else:
        end_date = f"{year}-{int(month_num)+1:02d}-01"

    results = db.query(
        Category.id,
        Category.name,
        Category.type,
        func.sum(Transaction.amount).label("total")
    ).join(Transaction).filter(
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).group_by(Category.id).all()

    return [
        {
            "category_id": r.id,
            "category_name": r.name,
            "type": r.type,
            "total": r.total or 0
        }
        for r in results
    ]


@router.get("/trends")
def trends(months: int = Query(6, ge=1, le=24), db: Session = Depends(get_db)):
    today = date.today()
    result = []

    for i in range(months - 1, -1, -1):
        target_date = today - relativedelta(months=i)
        month_str = target_date.strftime("%Y-%m")
        year, month_num = month_str.split("-")

        start_date = f"{year}-{month_num}-01"
        if month_num == "12":
            end_date = f"{int(year)+1}-01-01"
        else:
            end_date = f"{year}-{int(month_num)+1:02d}-01"

        income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.type == "income",
            Transaction.date >= start_date,
            Transaction.date < end_date
        ).scalar() or 0.0

        expenses = db.query(func.sum(Transaction.amount)).filter(
            Transaction.type == "expense",
            Transaction.date >= start_date,
            Transaction.date < end_date
        ).scalar() or 0.0

        result.append({
            "month": month_str,
            "income": income,
            "expenses": expenses,
            "net": income - expenses
        })

    return result
