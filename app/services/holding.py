import json
from typing import List, Optional, Dict
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from app.models.holding import Holding
from app.models.asset import Asset
from app.models.portfolio_finance import HoldingChange, PortfolioFinance, HoldingSnapshot
from app.models.portfolio import Portfolio
from app.schemas.holding import HoldingCreate, HoldingUpdate

class HoldingService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_holdings(self, portfolio_id: int) -> List[Holding]:
        return self.db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()
    
    def get_snapshot_dates(self, portfolio_id: int) -> List[Dict]:
        """获取所有有持仓快照的日期列表（只在发生变动的日期）"""
        results = self.db.query(
            func.date(HoldingSnapshot.snapshot_date).label('snapshot_date')
        ).filter(
            HoldingSnapshot.portfolio_id == portfolio_id
        ).distinct().order_by(
            HoldingSnapshot.snapshot_date.desc()
        ).all()
        
        return [
            {
                'date': str(row.snapshot_date),
            }
            for row in results
        ]
    
    def get_holding(self, holding_id: int, portfolio_id: int) -> Optional[Holding]:
        return self.db.query(Holding).filter(
            Holding.id == holding_id,
            Holding.portfolio_id == portfolio_id
        ).first()
    
    def create_holding(self, holding_data: dict, portfolio_id: int) -> Holding:
        db_holding = Holding(
            portfolio_id=portfolio_id,
            asset_id=holding_data.get('asset_id'),
            quantity=holding_data.get('quantity', 0),
            cost_price=holding_data.get('cost_price', 0),
            current_price=holding_data.get('current_price', 0)
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
        value = float(holding.quantity) * float(holding.current_price)
        cost = float(holding.quantity) * float(holding.cost_price)
        profit = value - cost
        profit_percent = (profit / cost) * 100 if cost > 0 else 0
        return {
            "value": value,
            "cost": cost,
            "profit": profit,
            "profit_percent": profit_percent
        }
    
    def calculate_portfolio_weights(self, holdings: List[Holding]) -> List[dict]:
        total_value = sum(float(holding.quantity) * float(holding.current_price) for holding in holdings)
        result = []
        for holding in holdings:
            asset = self.db.query(Asset).filter(Asset.id == holding.asset_id).first()
            metrics = self.calculate_holding_metrics(holding)
            weight = (metrics["value"] / total_value) * 100 if total_value > 0 else 0
            result.append({
                "id": holding.id,
                "portfolio_id": holding.portfolio_id,
                "asset_id": holding.asset_id,
                "asset_code": asset.code if asset else "",
                "asset_name": asset.name if asset else "",
                "quantity": float(holding.quantity),
                "cost_price": float(holding.cost_price),
                "current_price": float(holding.current_price),
                "value": metrics["value"],
                "cost": metrics["cost"],
                "profit": metrics["profit"],
                "profit_percent": metrics["profit_percent"],
                "weight": weight
            })
        return result
    
    def get_holdings_on_date(self, portfolio_id: int, target_date: date) -> List[Dict]:
        """
        从持仓快照中获取指定日期的持仓数据
        """
        # 查询该日期的快照
        snapshot = self.db.query(HoldingSnapshot).filter(
            HoldingSnapshot.portfolio_id == portfolio_id,
            func.date(HoldingSnapshot.snapshot_date) == target_date
        ).first()
        
        if not snapshot:
            return []
        
        # 解析 JSON 数据
        return json.loads(snapshot.holdings_data)
    
    def create_or_update_snapshot(self, portfolio_id: int, snapshot_date: date) -> Dict:
        """
        创建或更新指定日期的持仓快照
        """
        # 获取当前持仓
        holdings = self.db.query(Holding).filter(
            Holding.portfolio_id == portfolio_id
        ).all()
        
        # 获取资产信息并构建快照数据
        snapshot_data = []
        total_market_value = Decimal('0')
        
        for holding in holdings:
            asset = self.db.query(Asset).filter(Asset.id == holding.asset_id).first()
            market_value = Decimal(str(holding.quantity)) * Decimal(str(holding.current_price))
            total_market_value += market_value
            
            snapshot_data.append({
                'asset_id': holding.asset_id,
                'asset_code': asset.code if asset else '',
                'asset_name': asset.name if asset else '',
                'quantity': float(holding.quantity),
                'cost_price': float(holding.cost_price),
                'current_price': float(holding.current_price),
                'market_value': float(market_value),
                'weight': 0,  # 稍后计算
            })
        
        # 计算权重
        for item in snapshot_data:
            if total_market_value > 0:
                item['weight'] = (item['market_value'] / float(total_market_value)) * 100
        
        # 获取财务数据
        finance = self.db.query(PortfolioFinance).filter(
            PortfolioFinance.portfolio_id == portfolio_id
        ).first()
        cash_balance = finance.cash_balance if finance else Decimal('0')
        
        # 检查是否已有快照
        existing_snapshot = self.db.query(HoldingSnapshot).filter(
            HoldingSnapshot.portfolio_id == portfolio_id,
            func.date(HoldingSnapshot.snapshot_date) == snapshot_date
        ).first()
        
        if existing_snapshot:
            # 更新快照
            existing_snapshot.holdings_data = json.dumps(snapshot_data, ensure_ascii=False)
            existing_snapshot.total_market_value = total_market_value
            existing_snapshot.cash_balance = cash_balance
        else:
            # 创建新快照
            snapshot = HoldingSnapshot(
                portfolio_id=portfolio_id,
                snapshot_date=datetime.combine(snapshot_date, datetime.min.time()),
                holdings_data=json.dumps(snapshot_data, ensure_ascii=False),
                total_market_value=total_market_value,
                cash_balance=cash_balance
            )
            self.db.add(snapshot)
        
        self.db.commit()
        
        return {
            'snapshot_date': str(snapshot_date),
            'holdings_count': len(snapshot_data),
            'total_market_value': float(total_market_value)
        }
    
    def delete_snapshot(self, portfolio_id: int, snapshot_date: date) -> int:
        """删除指定日期的持仓快照"""
        snapshots = self.db.query(HoldingSnapshot).filter(
            HoldingSnapshot.portfolio_id == portfolio_id,
            func.date(HoldingSnapshot.snapshot_date) == snapshot_date
        ).all()
        
        count = len(snapshots)
        for snapshot in snapshots:
            self.db.delete(snapshot)
        
        self.db.commit()
        return count