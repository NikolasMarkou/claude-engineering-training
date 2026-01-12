from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Budget, Transaction, Category
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse, BudgetStatus

router = APIRouter()


@router.get("", response_model=list[BudgetResponse])
def list_budgets(month: str = Query(..., description="Format: YYYY-MM"), db: Session = Depends(get_db)):
    return db.query(Budget).filter(Budget.month == month).all()


@router.post("", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_budget(data: BudgetCreate, db: Session = Depends(get_db)):
    existing = db.query(Budget).filter(
        Budget.category_id == data.category_id,
        Budget.month == data.month
    ).first()

    if existing:
        existing.amount = data.amount
        db.commit()
        db.refresh(existing)
        return existing

    budget = Budget(**data.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.get("/status", response_model=list[BudgetStatus])
def get_budget_status(month: str = Query(..., description="Format: YYYY-MM"), db: Session = Depends(get_db)):
    budgets = db.query(Budget).filter(Budget.month == month).all()

    result = []
    for budget in budgets:
        # Calculate spending for this category in this month
        year, month_num = month.split("-")
        start_date = f"{year}-{month_num}-01"

        # Get last day of month
        if month_num == "12":
            end_date = f"{int(year)+1}-01-01"
        else:
            end_date = f"{year}-{int(month_num)+1:02d}-01"

        spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.category_id == budget.category_id,
            Transaction.type == "expense",
            Transaction.date >= start_date,
            Transaction.date < end_date
        ).scalar() or 0.0

        remaining = budget.amount - spent
        percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0

        result.append(BudgetStatus(
            category_id=budget.category_id,
            category_name=budget.category.name,
            budgeted=budget.amount,
            spent=spent,
            remaining=remaining,
            percentage_used=round(percentage, 1)
        ))

    return result


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")

    db.delete(budget)
    db.commit()
