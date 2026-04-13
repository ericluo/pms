from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.holding import Holding
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
    
    def _update_holding_after_transaction(self, portfolio_id: int, asset_id: int, trans_type: str, quantity: Decimal, price: Decimal):
        holding = self.db.query(Holding).filter(
            Holding.portfolio_id == portfolio_id,
            Holding.asset_id == asset_id
        ).first()
        
        if trans_type == 'buy':
            if holding:
                total_cost = holding.cost_price * holding.quantity + price * quantity
                new_quantity = holding.quantity + quantity
                holding.cost_price = total_cost / new_quantity if new_quantity > 0 else Decimal('0')
                holding.quantity = new_quantity
            else:
                holding = Holding(
                    portfolio_id=portfolio_id,
                    asset_id=asset_id,
                    quantity=quantity,
                    cost_price=price,
                    current_price=price
                )
                self.db.add(holding)
                
        elif trans_type == 'sell':
            if holding:
                holding.quantity -= quantity
                if holding.quantity <= 0:
                    self.db.delete(holding)
    
    def create_transaction(self, transaction_data: dict, portfolio_id: int) -> Transaction:
        db_transaction = Transaction(
            portfolio_id=portfolio_id,
            asset_id=transaction_data['asset_id'],
            type=transaction_data['transaction_type'],
            quantity=transaction_data['quantity'],
            price=transaction_data['price'],
            amount=transaction_data.get('amount') or transaction_data['quantity'] * transaction_data['price'],
            fee=transaction_data.get('fee') or 0,
            transaction_date=transaction_data['transaction_date']
        )
        self.db.add(db_transaction)
        self._update_holding_after_transaction(
            portfolio_id,
            transaction_data['asset_id'],
            transaction_data['transaction_type'],
            transaction_data['quantity'],
            transaction_data['price']
        )
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction
    
    def delete_transaction(self, transaction_id: int, portfolio_id: int) -> bool:
        db_transaction = self.get_transaction(transaction_id, portfolio_id)
        if not db_transaction:
            return False
        
        trans_type = db_transaction.transaction_type
        quantity = db_transaction.quantity
        price = db_transaction.price
        asset_id = db_transaction.asset_id
        
        self.db.delete(db_transaction)
        
        if trans_type == 'buy':
            self._revert_buy_holding(portfolio_id, asset_id, quantity, price)
        elif trans_type == 'sell':
            self._revert_sell_holding(portfolio_id, asset_id, quantity, price)
        
        self.db.commit()
        return True
    
    def _revert_buy_holding(self, portfolio_id: int, asset_id: int, quantity: Decimal, price: Decimal):
        holding = self.db.query(Holding).filter(
            Holding.portfolio_id == portfolio_id,
            Holding.asset_id == asset_id
        ).first()
        
        if holding:
            holding.quantity -= quantity
            if holding.quantity <= 0:
                self.db.delete(holding)
    
    def _revert_sell_holding(self, portfolio_id: int, asset_id: int, quantity: Decimal, price: Decimal):
        holding = self.db.query(Holding).filter(
            Holding.portfolio_id == portfolio_id,
            Holding.asset_id == asset_id
        ).first()
        
        if holding:
            holding.quantity += quantity
        else:
            holding = Holding(
                portfolio_id=portfolio_id,
                asset_id=asset_id,
                quantity=quantity,
                cost_price=price,
                current_price=price
            )
            self.db.add(holding)