import requests
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.models.holding import Holding
from app.models.market_data import MarketData

class MarketDataService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_stock_data(self, code: str) -> Dict[str, float]:
        # 这里使用模拟数据，实际应该从API获取
        # 例如使用新浪财经、东方财富等API
        return {
            "price": 1850.00,
            "change": 50.00,
            "change_percent": 2.78,
            "open": 1800.00,
            "high": 1860.00,
            "low": 1790.00,
            "volume": 1000000,
            "amount": 1850000000
        }
    
    def get_index_data(self, code: str) -> Dict[str, float]:
        # 这里使用模拟数据，实际应该从API获取
        return {
            "price": 4500.00,
            "change": 90.00,
            "change_percent": 2.04,
            "open": 4410.00,
            "high": 4510.00,
            "low": 4400.00,
            "volume": 1000000000,
            "amount": 450000000000
        }
    
    def get_stocks_market_data(self) -> List[Dict]:
        # 获取股票市场数据
        assets = self.db.query(Asset).filter(Asset.type == "股票").limit(10).all()
        result = []
        for asset in assets:
            data = self.get_stock_data(asset.code)
            result.append({
                "code": asset.code,
                "name": asset.name,
                "price": data["price"],
                "change": data["change"],
                "change_percent": data["change_percent"],
                "open": data["open"],
                "high": data["high"],
                "low": data["low"],
                "volume": data["volume"],
                "amount": data["amount"]
            })
        return result
    
    def get_indices_market_data(self) -> List[Dict]:
        # 获取市场指数数据
        indices = [
            {"code": "000300.SH", "name": "沪深300"},
            {"code": "000001.SH", "name": "上证指数"},
            {"code": "399001.SZ", "name": "深证成指"},
            {"code": "399006.SZ", "name": "创业板指"}
        ]
        result = []
        for index in indices:
            data = self.get_index_data(index["code"])
            result.append({
                "code": index["code"],
                "name": index["name"],
                "price": data["price"],
                "change": data["change"],
                "change_percent": data["change_percent"],
                "open": data["open"],
                "high": data["high"],
                "low": data["low"],
                "volume": data["volume"],
                "amount": data["amount"]
            })
        return result
    
    def update_market_data(self, asset_id: int) -> bool:
        # 更新资产的市场数据
        asset = self.db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            return False
        
        try:
            data = self.get_stock_data(asset.code)
            # 更新持仓的当前价格
            holdings = self.db.query(Holding).filter(Holding.asset_id == asset_id).all()
            for holding in holdings:
                holding.current_price = data["price"]
            
            # 保存市场数据历史
            market_data = MarketData(
                asset_id=asset_id,
                date=datetime.utcnow().date(),
                open=data["open"],
                high=data["high"],
                low=data["low"],
                close=data["price"],
                volume=data["volume"],
                amount=data["amount"]
            )
            self.db.add(market_data)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

class MarketService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_market_data(self, asset_id: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        query = self.db.query(MarketData)
        
        if asset_id:
            query = query.filter(MarketData.asset_id == asset_id)
        
        if start_date:
            query = query.filter(MarketData.date >= start_date)
        
        if end_date:
            query = query.filter(MarketData.date <= end_date)
        
        return query.all()
    
    def get_market_data_by_id(self, market_data_id: int):
        return self.db.query(MarketData).filter(MarketData.id == market_data_id).first()
    
    def create_market_data(self, data):
        market_data = MarketData(**data)
        self.db.add(market_data)
        self.db.commit()
        self.db.refresh(market_data)
        return market_data
    
    def update_market_data(self, market_data_id: int, data):
        market_data = self.db.query(MarketData).filter(MarketData.id == market_data_id).first()
        if not market_data:
            return None
        
        for key, value in data.items():
            setattr(market_data, key, value)
        
        self.db.commit()
        self.db.refresh(market_data)
        return market_data
    
    def delete_market_data(self, market_data_id: int):
        market_data = self.db.query(MarketData).filter(MarketData.id == market_data_id).first()
        if not market_data:
            return False
        
        self.db.delete(market_data)
        self.db.commit()
        return True