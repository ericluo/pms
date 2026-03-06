from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.models.holding import Holding
from app.models.transaction import Transaction
from app.models.cash_flow import CashFlow

class PerformanceService:
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_total_return(self, portfolio_id: int) -> float:
        # 计算总回报率
        holdings = self.db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()
        total_value = sum(holding.quantity * holding.current_price for holding in holdings)
        total_cost = sum(holding.quantity * holding.cost_price for holding in holdings)
        return ((total_value - total_cost) / total_cost) * 100 if total_cost > 0 else 0
    
    def calculate_annualized_return(self, portfolio_id: int) -> float:
        # 计算年化收益率
        portfolio = self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            return 0
        
        total_return = self.calculate_total_return(portfolio_id)
        days = (datetime.utcnow() - portfolio.created_at).days
        if days == 0:
            return 0
        
        # 简单年化计算
        return (pow(1 + total_return / 100, 365 / days) - 1) * 100
    
    def calculate_sharpe_ratio(self, portfolio_id: int) -> float:
        # 计算夏普比率
        # 这里使用简化计算，实际应该使用历史数据计算
        annualized_return = self.calculate_annualized_return(portfolio_id)
        risk_free_rate = 3.0  # 假设无风险利率为3%
        volatility = 15.0  # 假设波动率为15%
        return (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
    
    def calculate_max_drawdown(self, portfolio_id: int) -> float:
        # 计算最大回撤
        # 这里使用简化计算，实际应该使用历史数据计算
        return 5.23  # 示例值
    
    def calculate_alpha_beta(self, portfolio_id: int) -> Dict[str, float]:
        # 计算Alpha和Beta
        # 这里使用简化计算，实际应该使用历史数据计算
        return {
            "alpha": 2.15,
            "beta": 0.85
        }
    
    def get_performance_metrics(self, portfolio_id: int) -> Dict[str, float]:
        total_return = self.calculate_total_return(portfolio_id)
        annualized_return = self.calculate_annualized_return(portfolio_id)
        sharpe_ratio = self.calculate_sharpe_ratio(portfolio_id)
        max_drawdown = self.calculate_max_drawdown(portfolio_id)
        alpha_beta = self.calculate_alpha_beta(portfolio_id)
        
        return {
            "total_return": round(total_return, 2),
            "annualized_return": round(annualized_return, 2),
            "daily_return": round(total_return / 30, 2),  # 简化计算
            "weekly_return": round(total_return / 4.3, 2),  # 简化计算
            "monthly_return": round(total_return, 2),
            "yearly_return": round(annualized_return, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "max_drawdown": round(max_drawdown, 2),
            "alpha": round(alpha_beta["alpha"], 2),
            "beta": round(alpha_beta["beta"], 2),
            "volatility": 18.50  # 示例值
        }