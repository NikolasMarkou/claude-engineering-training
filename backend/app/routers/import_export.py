import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import Transaction, Category

router = APIRouter()


class CSVPreviewRow(BaseModel):
    date: str
    amount: float
    type: str
    category: str
    description: str | None


class CSVPreviewResponse(BaseModel):
    rows: list[CSVPreviewRow]
    errors: list[str]


class CSVConfirmRequest(BaseModel):
    rows: list[CSVPreviewRow]


@router.post("/csv", response_model=CSVPreviewResponse)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be CSV")

    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    rows = []
    errors = []

    required_fields = {"date", "amount", "type", "category"}
    if reader.fieldnames and not required_fields.issubset(set(reader.fieldnames)):
        missing = required_fields - set(reader.fieldnames)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required columns: {missing}"
        )

    for i, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
        try:
            # Validate date
            datetime.strptime(row["date"], "%Y-%m-%d")

            # Validate amount
            amount = float(row["amount"])
            if amount <= 0:
                errors.append(f"Row {i}: Amount must be positive")
                continue

            # Validate type
            if row["type"] not in ("income", "expense"):
                errors.append(f"Row {i}: Type must be 'income' or 'expense'")
                continue

            rows.append(CSVPreviewRow(
                date=row["date"],
                amount=amount,
                type=row["type"],
                category=row["category"],
                description=row.get("description")
            ))
        except ValueError as e:
            errors.append(f"Row {i}: {str(e)}")

    return CSVPreviewResponse(rows=rows, errors=errors)


@router.post("/confirm")
def confirm_import(data: CSVConfirmRequest, db: Session = Depends(get_db)):
    categories = {c.name: c.id for c in db.query(Category).all()}

    created = 0
    errors = []

    for i, row in enumerate(data.rows):
        category_id = categories.get(row.category)
        if not category_id:
            errors.append(f"Row {i+1}: Unknown category '{row.category}'")
            continue

        transaction = Transaction(
            date=datetime.strptime(row.date, "%Y-%m-%d").date(),
            amount=row.amount,
            type=row.type,
            category_id=category_id,
            description=row.description
        )
        db.add(transaction)
        created += 1

    db.commit()

    return {"created": created, "errors": errors}
