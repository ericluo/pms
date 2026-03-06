from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.cash_flow import CashFlow
from app.schemas.cash_flow import CashFlowCreate

class CashFlowService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_cash_flows(self, portfolio_id: int) -> List[CashFlow]:
        return self.db.query(CashFlow).filter(CashFlow.portfolio_id == portfolio_id).order_by(CashFlow.transaction_date.desc()).all()
    
    def get_cash_flow(self, cash_flow_id: int, portfolio_id: int) -> Optional[CashFlow]:
        return self.db.query(CashFlow).filter(
            CashFlow.id == cash_flow_id,
            CashFlow.portfolio_id == portfolio_id
        ).first()
    
    def create_cash_flow(self, cash_flow_create: CashFlowCreate, portfolio_id: int) -> CashFlow:
        db_cash_flow = CashFlow(
            portfolio_id=portfolio_id,
            type=cash_flow_create.type,
            amount=cash_flow_create.amount,
            description=cash_flow_create.description,
            transaction_date=cash_flow_create.transaction_date
        )
        self.db.add(db_cash_flow)
        self.db.commit()
        self.db.refresh(db_cash_flow)
        return db_cash_flow
    
    def delete_cash_flow(self, cash_flow_id: int, portfolio_id: int) -> bool:
        db_cash_flow = self.get_cash_flow(cash_flow_id, portfolio_id)
        if not db_cash_flow:
            return False
        self.db.delete(db_cash_flow)
        self.db.commit()
        return True
    
    def get_cash_balance(self, portfolio_id: int) -> float:
        cash_flows = self.get_cash_flows(portfolio_id)
        balance = 0.0
        for cash_flow in cash_flows:
            if cash_flow.type == "存入":
                balance += cash_flow.amount
            else:
                balance -= cash_flow.amount
        return balance