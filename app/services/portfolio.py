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
    
    def add_holding(self, portfolio_id: int, asset_id: int, quantity: float, cost_price: float, current_price: float, user_id: int) -> Holding:
        # 验证投资组合是否存在
        portfolio = self.get_portfolio(portfolio_id, user_id)
        if not portfolio:
            raise ValueError('投资组合不存在')
        
        # 创建持仓
        holding = Holding(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
            quantity=quantity,
            cost_price=cost_price,
            current_price=current_price
        )
        self.db.add(holding)
        self.db.commit()
        self.db.refresh(holding)
        return holding
    
    def get_holding(self, holding_id: int, user_id: int) -> Optional[Holding]:
        # 通过投资组合关联查询，确保用户有权限访问
        holding = self.db.query(Holding).join(Portfolio).filter(
            Holding.id == holding_id,
            Portfolio.user_id == user_id
        ).first()
        return holding
    
    def update_holding(self, holding_id: int, quantity: Optional[float] = None, cost_price: Optional[float] = None, current_price: Optional[float] = None, user_id: int = None) -> Optional[Holding]:
        holding = self.get_holding(holding_id, user_id)
        if not holding:
            return None
        
        if quantity is not None:
            holding.quantity = quantity
        if cost_price is not None:
            holding.cost_price = cost_price
        if current_price is not None:
            holding.current_price = current_price
        
        self.db.commit()
        self.db.refresh(holding)
        return holding
    
    def delete_holding(self, holding_id: int, user_id: int) -> bool:
        holding = self.get_holding(holding_id, user_id)
        if not holding:
            return False
        
        self.db.delete(holding)
        self.db.commit()
        return True