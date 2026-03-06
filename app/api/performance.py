from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.performance import PerformanceService
from app.services.portfolio import PortfolioService

api = Namespace('performance', description='性能分析相关操作')

# 模型定义
performance_model = api.model('Performance', {
    'total_return': fields.Float,
    'annualized_return': fields.Float,
    'volatility': fields.Float,
    'sharpe_ratio': fields.Float,
    'max_drawdown': fields.Float,
    'portfolio_value': fields.Float,
    'cash_flow': fields.Float,
    'time_period': fields.String
})

@api.route('')
class PerformanceDetail(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', performance_model)
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def get(self):
        """获取投资组合性能分析"""
        db: Session = next(get_db())
        performance_service = PerformanceService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/performance', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        # 获取性能指标
        performance = performance_service.calculate_performance(portfolio_id)
        
        return {
            'total_return': performance['total_return'],
            'annualized_return': performance['annualized_return'],
            'volatility': performance['volatility'],
            'sharpe_ratio': performance['sharpe_ratio'],
            'max_drawdown': performance['max_drawdown'],
            'portfolio_value': performance['portfolio_value'],
            'cash_flow': performance['cash_flow'],
            'time_period': performance['time_period']
        }
