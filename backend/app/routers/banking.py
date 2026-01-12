from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import BankConnection, PendingTransaction, Transaction, Category
from app.schemas.bank import (
    BankConnectionCreate,
    BankConnectionResponse,
    PendingTransactionResponse,
    PendingTransactionImport,
    BankBalanceResponse,
)
from app.services.mock_bank_service import (
    get_available_banks,
    generate_mock_balance,
    generate_mock_transactions,
    suggest_category,
)

router = APIRouter()


@router.get("/banks")
def list_available_banks():
    """List available banks to connect."""
    return get_available_banks()


@router.get("/connections", response_model=list[BankConnectionResponse])
def list_connections(db: Session = Depends(get_db)):
    """List all connected bank accounts."""
    return db.query(BankConnection).filter(BankConnection.is_active == True).all()


@router.post("/connections", response_model=BankConnectionResponse, status_code=status.HTTP_201_CREATED)
def create_connection(data: BankConnectionCreate, db: Session = Depends(get_db)):
    """Connect a new bank account."""
    connection = BankConnection(
        bank_name=data.bank_name,
        account_name=data.account_name,
        account_type=data.account_type,
        balance=generate_mock_balance(data.account_type),
    )
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


@router.delete("/connections/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    """Disconnect a bank account."""
    connection = db.query(BankConnection).filter(BankConnection.id == connection_id).first()
    if not connection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found")

    db.delete(connection)
    db.commit()


@router.post("/connections/{connection_id}/sync")
def sync_connection(connection_id: int, db: Session = Depends(get_db)):
    """Sync transactions from a bank connection."""
    connection = db.query(BankConnection).filter(BankConnection.id == connection_id).first()
    if not connection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connection not found")

    # Generate mock transactions
    mock_transactions = generate_mock_transactions(count=random_transaction_count())

    # Check for existing external IDs to avoid duplicates
    existing_ids = set(
        t.external_id for t in db.query(PendingTransaction).filter(
            PendingTransaction.bank_connection_id == connection_id
        ).all()
    )

    created = 0
    for tx in mock_transactions:
        if tx["external_id"] in existing_ids:
            continue

        pending = PendingTransaction(
            bank_connection_id=connection_id,
            external_id=tx["external_id"],
            amount=tx["amount"],
            merchant_name=tx["merchant_name"],
            date=tx["date"],
            suggested_category_id=suggest_category(tx["merchant_name"], db),
            status="pending",
        )
        db.add(pending)
        created += 1

    # Update connection
    connection.last_synced = datetime.now(timezone.utc)
    connection.balance = generate_mock_balance(connection.account_type)

    db.commit()
    return {"synced": created, "balance": connection.balance}


def random_transaction_count() -> int:
    """Return a random number of transactions to generate."""
    import random
    return random.randint(5, 15)


@router.get("/pending", response_model=list[PendingTransactionResponse])
def list_pending(db: Session = Depends(get_db)):
    """List all pending transactions for review."""
    return db.query(PendingTransaction).filter(
        PendingTransaction.status == "pending"
    ).order_by(PendingTransaction.date.desc()).all()


@router.post("/pending/{pending_id}/import", response_model=dict)
def import_transaction(
    pending_id: int,
    data: PendingTransactionImport,
    db: Session = Depends(get_db)
):
    """Import a pending transaction."""
    pending = db.query(PendingTransaction).filter(PendingTransaction.id == pending_id).first()
    if not pending:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pending transaction not found")

    if pending.status != "pending":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction already processed")

    # Get category to determine type
    category = db.query(Category).filter(Category.id == data.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")

    # Create actual transaction
    transaction = Transaction(
        amount=pending.amount,
        type=category.type,
        category_id=data.category_id,
        description=pending.merchant_name,
        date=datetime.strptime(pending.date, "%Y-%m-%d").date(),
    )
    db.add(transaction)

    # Mark pending as imported
    pending.status = "imported"

    db.commit()
    return {"message": "Transaction imported", "transaction_id": transaction.id}


@router.post("/pending/{pending_id}/dismiss", status_code=status.HTTP_204_NO_CONTENT)
def dismiss_transaction(pending_id: int, db: Session = Depends(get_db)):
    """Dismiss a pending transaction."""
    pending = db.query(PendingTransaction).filter(PendingTransaction.id == pending_id).first()
    if not pending:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pending transaction not found")

    pending.status = "dismissed"
    db.commit()


@router.post("/pending/import-all")
def import_all_pending(db: Session = Depends(get_db)):
    """Import all pending transactions with their suggested categories."""
    pending_list = db.query(PendingTransaction).filter(
        PendingTransaction.status == "pending"
    ).all()

    imported = 0
    for pending in pending_list:
        if not pending.suggested_category_id:
            continue

        category = db.query(Category).filter(Category.id == pending.suggested_category_id).first()
        if not category:
            continue

        transaction = Transaction(
            amount=pending.amount,
            type=category.type,
            category_id=pending.suggested_category_id,
            description=pending.merchant_name,
            date=datetime.strptime(pending.date, "%Y-%m-%d").date(),
        )
        db.add(transaction)
        pending.status = "imported"
        imported += 1

    db.commit()
    return {"imported": imported}


@router.get("/balances", response_model=list[BankBalanceResponse])
def get_balances(db: Session = Depends(get_db)):
    """Get balances for all connected accounts."""
    connections = db.query(BankConnection).filter(BankConnection.is_active == True).all()
    return [
        BankBalanceResponse(
            bank_connection_id=c.id,
            bank_name=c.bank_name,
            account_name=c.account_name,
            account_type=c.account_type,
            balance=c.balance,
        )
        for c in connections
    ]
