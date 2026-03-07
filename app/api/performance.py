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
    def get(self, portfolio_id=None):
        """获取投资组合性能分析"""
        db: Session = next(get_db())
        performance_service = PerformanceService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从路径参数或查询参数获取 portfolio_id
        if portfolio_id is None:
            portfolio_id = request.args.get('portfolio_id', type=int)
        
        if not portfolio_id:
            api.abort(400, 'Missing portfolio_id parameter')
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        # 获取性能指标
        performance = performance_service.get_performance_metrics(portfolio_id)
        
        return {
            'total_return': performance['total_return'],
            'annualized_return': performance['annualized_return'],
            'volatility': performance['volatility'],
            'sharpe_ratio': performance['sharpe_ratio'],
            'max_drawdown': performance['max_drawdown'],
            'portfolio_value': performance.get('portfolio_value', 0),
            'cash_flow': performance.get('cash_flow', 0),
            'time_period': 'all'
        }
