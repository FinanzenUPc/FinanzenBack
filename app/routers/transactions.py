from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate, TransactionPaginatedResponse
from app.services.transaction_service import transaction_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    """Create a new transaction."""
    return transaction_service.create_transaction(db=db, transaction=transaction)


@router.get("/", response_model=TransactionPaginatedResponse)
def get_transactions(
    usuario: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all transactions with pagination metadata, optionally filtered by user."""
    if usuario:
        data = transaction_service.get_user_transactions(db=db, usuario=usuario, skip=skip, limit=limit)
        total = transaction_service.count_user_transactions(db=db, usuario=usuario)
    else:
        data = transaction_service.get_all_transactions(db=db, skip=skip, limit=limit)
        total = transaction_service.count_all_transactions(db=db)

    return TransactionPaginatedResponse(
        data=data,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific transaction."""
    transaction = transaction_service.get_transaction(db=db, transaction_id=transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction


@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Update a transaction."""
    transaction = transaction_service.update_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction_update=transaction_update
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """Delete a transaction."""
    success = transaction_service.delete_transaction(db=db, transaction_id=transaction_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return None
