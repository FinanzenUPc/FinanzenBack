from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:
    @staticmethod
    def get_transaction(db: Session, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID."""
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()

    @staticmethod
    def get_user_transactions(db: Session, usuario: str, skip: int = 0, limit: int = 100) -> List[Transaction]:
        """Get all transactions for a user."""
        return db.query(Transaction).filter(Transaction.usuario == usuario).offset(skip).limit(limit).all()

    @staticmethod
    def count_user_transactions(db: Session, usuario: str) -> int:
        """Count all transactions for a user."""
        return db.query(Transaction).filter(Transaction.usuario == usuario).count()

    @staticmethod
    def get_all_transactions(db: Session, skip: int = 0, limit: int = 1000) -> List[Transaction]:
        """Get all transactions."""
        return db.query(Transaction).offset(skip).limit(limit).all()

    @staticmethod
    def count_all_transactions(db: Session) -> int:
        """Count all transactions."""
        return db.query(Transaction).count()

    @staticmethod
    def create_transaction(db: Session, transaction: TransactionCreate) -> Transaction:
        """Create a new transaction."""
        db_transaction = Transaction(**transaction.model_dump())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def update_transaction(
        db: Session,
        transaction_id: int,
        transaction_update: TransactionUpdate
    ) -> Optional[Transaction]:
        """Update transaction."""
        db_transaction = TransactionService.get_transaction(db, transaction_id)
        if not db_transaction:
            return None

        update_data = transaction_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_transaction, field, value)

        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def delete_transaction(db: Session, transaction_id: int) -> bool:
        """Delete transaction."""
        db_transaction = TransactionService.get_transaction(db, transaction_id)
        if not db_transaction:
            return False

        db.delete(db_transaction)
        db.commit()
        return True


transaction_service = TransactionService()
