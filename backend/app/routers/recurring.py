from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RecurringTransaction, Transaction
from app.schemas.recurring import RecurringCreate, RecurringUpdate, RecurringResponse

router = APIRouter()


@router.get("", response_model=list[RecurringResponse])
def list_recurring(db: Session = Depends(get_db)):
    return db.query(RecurringTransaction).all()


@router.post("", response_model=RecurringResponse, status_code=status.HTTP_201_CREATED)
def create_recurring(data: RecurringCreate, db: Session = Depends(get_db)):
    recurring = RecurringTransaction(**data.model_dump())
    db.add(recurring)
    db.commit()
    db.refresh(recurring)
    return recurring


@router.put("/{recurring_id}", response_model=RecurringResponse)
def update_recurring(recurring_id: int, data: RecurringUpdate, db: Session = Depends(get_db)):
    recurring = db.query(RecurringTransaction).filter(RecurringTransaction.id == recurring_id).first()
    if not recurring:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring transaction not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(recurring, key, value)

    db.commit()
    db.refresh(recurring)
    return recurring


@router.delete("/{recurring_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurring(recurring_id: int, db: Session = Depends(get_db)):
    recurring = db.query(RecurringTransaction).filter(RecurringTransaction.id == recurring_id).first()
    if not recurring:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring transaction not found")

    db.delete(recurring)
    db.commit()


@router.post("/process")
def process_recurring(db: Session = Depends(get_db)):
    """Process all recurring transactions that are due."""
    today = date.today()
    due_transactions = db.query(RecurringTransaction).filter(
        RecurringTransaction.is_active == True,
        RecurringTransaction.next_run_date <= today
    ).all()

    created_count = 0
    for recurring in due_transactions:
        # Create the transaction
        transaction = Transaction(
            amount=recurring.amount,
            type=recurring.type,
            category_id=recurring.category_id,
            description=recurring.description,
            date=recurring.next_run_date
        )
        db.add(transaction)

        # Calculate next run date
        if recurring.frequency == "daily":
            recurring.next_run_date += timedelta(days=1)
        elif recurring.frequency == "weekly":
            recurring.next_run_date += timedelta(weeks=1)
        elif recurring.frequency == "monthly":
            # Add one month
            month = recurring.next_run_date.month
            year = recurring.next_run_date.year
            if month == 12:
                recurring.next_run_date = recurring.next_run_date.replace(year=year + 1, month=1)
            else:
                recurring.next_run_date = recurring.next_run_date.replace(month=month + 1)

        created_count += 1

    db.commit()
    return {"processed": created_count}
