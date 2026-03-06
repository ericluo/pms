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
        db_portfolio = Portfolio(
            user_id=user_id,
            name=portfolio_data['name'],
            description=portfolio_data.get('description'),
            benchmark=portfolio_data['benchmark'],
            risk_level=portfolio_data['risk_level']
        )
        self.db.add(db_portfolio)
        self.db.commit()
        self.db.refresh(db_portfolio)
        return db_portfolio
    
    def update_portfolio(self, portfolio_id: int, portfolio_data: dict, user_id: int) -> Optional[Portfolio]:
        db_portfolio = self.get_portfolio(portfolio_id, user_id)
        if not db_portfolio:
            return None
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
        self.db.delete(db_portfolio)
        self.db.commit()
        return True
    
    def get_portfolio_holdings(self, portfolio_id: int, user_id: int) -> List[Holding]:
        portfolio = self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            return []
        return portfolio.holdings