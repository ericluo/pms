from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.models.holding import Holding
from app.models.asset import Asset
from app.schemas.holding import HoldingCreate, HoldingUpdate

class HoldingService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_holdings(self, portfolio_id: int) -> List[Holding]:
        return self.db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()
    
    def get_holding(self, holding_id: int, portfolio_id: int) -> Optional[Holding]:
        return self.db.query(Holding).filter(
            Holding.id == holding_id,
            Holding.portfolio_id == portfolio_id
        ).first()
    
    def create_holding(self, holding_create: HoldingCreate, portfolio_id: int) -> Holding:
        db_holding = Holding(
            portfolio_id=portfolio_id,
            asset_id=holding_create.asset_id,
            quantity=holding_create.quantity,
            cost_price=holding_create.cost_price,
            current_price=holding_create.current_price
        )
        self.db.add(db_holding)
        self.db.commit()
        self.db.refresh(db_holding)
        return db_holding
    
    def update_holding(self, holding_id: int, holding_update: HoldingUpdate, portfolio_id: int) -> Optional[Holding]:
        db_holding = self.get_holding(holding_id, portfolio_id)
        if not db_holding:
            return None
        for key, value in holding_update.dict(exclude_unset=True).items():
            setattr(db_holding, key, value)
        self.db.commit()
        self.db.refresh(db_holding)
        return db_holding
    
    def delete_holding(self, holding_id: int, portfolio_id: int) -> bool:
        db_holding = self.get_holding(holding_id, portfolio_id)
        if not db_holding:
            return False
        self.db.delete(db_holding)
        self.db.commit()
        return True
    
    def calculate_holding_metrics(self, holding: Holding) -> dict:
        value = holding.quantity * holding.current_price
        cost = holding.quantity * holding.cost_price
        profit = value - cost
        profit_percent = (profit / cost) * 100 if cost > 0 else 0
        return {
            "value": value,
            "cost": cost,
            "profit": profit,
            "profit_percent": profit_percent
        }
    
    def calculate_portfolio_weights(self, holdings: List[Holding]) -> List[dict]:
        total_value = sum(holding.quantity * holding.current_price for holding in holdings)
        result = []
        for holding in holdings:
            asset = self.db.query(Asset).filter(Asset.id == holding.asset_id).first()
            metrics = self.calculate_holding_metrics(holding)
            weight = (metrics["value"] / total_value) * 100 if total_value > 0 else 0
            result.append({
                "id": holding.id,
                "asset_id": holding.asset_id,
                "asset_code": asset.code if asset else "",
                "asset_name": asset.name if asset else "",
                "quantity": holding.quantity,
                "cost_price": holding.cost_price,
                "current_price": holding.current_price,
                "value": metrics["value"],
                "cost": metrics["cost"],
                "profit": metrics["profit"],
                "profit_percent": metrics["profit_percent"],
                "weight": weight
            })
        return result