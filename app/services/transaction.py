from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_transactions(self, portfolio_id: int) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.portfolio_id == portfolio_id).order_by(Transaction.transaction_date.desc()).all()
    
    def get_transaction(self, transaction_id: int, portfolio_id: int) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.portfolio_id == portfolio_id
        ).first()
    
    def create_transaction(self, transaction_create: TransactionCreate, portfolio_id: int) -> Transaction:
        db_transaction = Transaction(
            portfolio_id=portfolio_id,
            asset_id=transaction_create.asset_id,
            type=transaction_create.type,
            quantity=transaction_create.quantity,
            price=transaction_create.price,
            amount=transaction_create.amount,
            fee=transaction_create.fee or 0,
            transaction_date=transaction_create.transaction_date
        )
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction
    
    def delete_transaction(self, transaction_id: int, portfolio_id: int) -> bool:
        db_transaction = self.get_transaction(transaction_id, portfolio_id)
        if not db_transaction:
            return False
        self.db.delete(db_transaction)
        self.db.commit()
        return True