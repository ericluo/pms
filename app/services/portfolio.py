from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.models.holding import Holding
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate

class PortfolioService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_portfolios(self, user_id: int) -> List[Portfolio]:
        return self.db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    
    def get_portfolio(self, portfolio_id: int, user_id: int) -> Optional[Portfolio]:
        return self.db.query(Portfolio).filter(
            Portfolio.id == portfolio_id,
            Portfolio.user_id == user_id
        ).first()
    
    def create_portfolio(self, portfolio_data: dict, user_id: int) -> Portfolio:
        # 检查用户是否已有投资组合
        existing_portfolios = self.db.query(Portfolio).filter(Portfolio.user_id == user_id).count()
        
        # 如果是第一个投资组合，自动设置为默认
        is_default = portfolio_data.get('is_default', False)
        if existing_portfolios == 0:
            is_default = True
        elif is_default:
            # 如果设置为默认，将其他投资组合设置为非默认
            self.db.query(Portfolio).filter(
                Portfolio.user_id == user_id,
                Portfolio.is_default == True
            ).update({Portfolio.is_default: False})
        
        db_portfolio = Portfolio(
            user_id=user_id,
            name=portfolio_data['name'],
            description=portfolio_data.get('description'),
            benchmark=portfolio_data['benchmark'],
            risk_level=portfolio_data['risk_level'],
            is_default=is_default
        )
        self.db.add(db_portfolio)
        self.db.commit()
        self.db.refresh(db_portfolio)
        return db_portfolio
    
    def update_portfolio(self, portfolio_id: int, portfolio_data: dict, user_id: int) -> Optional[Portfolio]:
        db_portfolio = self.get_portfolio(portfolio_id, user_id)
        if not db_portfolio:
            return None
        
        # 处理默认投资组合逻辑
        if 'is_default' in portfolio_data and portfolio_data['is_default']:
            # 将其他投资组合设置为非默认
            self.db.query(Portfolio).filter(
                Portfolio.user_id == user_id,
                Portfolio.is_default == True,
                Portfolio.id != portfolio_id
            ).update({Portfolio.is_default: False})
        
        for key, value in portfolio_data.items():
            if value is not None:
                setattr(db_portfolio, key, value)
        self.db.commit()
        self.db.refresh(db_portfolio)
        return db_portfolio
    
    def delete_portfolio(self, portfolio_id: int, user_id: int) -> bool:
        db_portfolio = self.get_portfolio(portfolio_id, user_id)
        if not db_portfolio:
            return False
        
        # 检查是否是默认投资组合
        is_default = db_portfolio.is_default
        
        self.db.delete(db_portfolio)
        self.db.commit()
        
        # 如果删除的是默认投资组合，将第一个投资组合设置为默认
        if is_default:
            remaining_portfolio = self.db.query(Portfolio).filter(
                Portfolio.user_id == user_id
            ).first()
            if remaining_portfolio:
                remaining_portfolio.is_default = True
                self.db.commit()
        
        return True
    
    def get_portfolio_holdings(self, portfolio_id: int, user_id: int) -> List[Holding]:
        portfolio = self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            return []
        return portfolio.holdings