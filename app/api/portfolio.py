from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.portfolio import PortfolioService
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate, PortfolioResponse

api = Namespace('portfolios', description='投资组合相关操作')

# 模型定义
portfolio_model = api.model('Portfolio', {
    'id': fields.Integer(readonly=True),
    'user_id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String,
    'benchmark': fields.String(required=True),
    'risk_level': fields.String(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('')
class PortfolioList(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', [portfolio_model])
    @api.response(401, '未授权')
    def get(self):
        """获取投资组合列表"""
        db: Session = next(get_db())
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolios = portfolio_service.get_portfolios(int(user_id))
        
        return [{
            'id': p.id,
            'user_id': p.user_id,
            'name': p.name,
            'description': p.description,
            'benchmark': p.benchmark,
            'risk_level': p.risk_level,
            'created_at': p.created_at.isoformat() if p.created_at else None,
            'updated_at': p.updated_at.isoformat() if p.updated_at else None
        } for p in portfolios]
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(portfolio_model)
    @api.response(201, '创建成功', portfolio_model)
    @api.response(401, '未授权')
    def post(self):
        """创建投资组合"""
        db: Session = next(get_db())
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        data = request.json
        
        portfolio = portfolio_service.create_portfolio(data, int(user_id))
        
        return {
            'id': portfolio.id,
            'user_id': portfolio.user_id,
            'name': portfolio.name,
            'description': portfolio.description,
            'benchmark': portfolio.benchmark,
            'risk_level': portfolio.risk_level,
            'created_at': portfolio.created_at.isoformat() if portfolio.created_at else None,
            'updated_at': portfolio.updated_at.isoformat() if portfolio.updated_at else None
        }, 201

@api.route('/<int:portfolio_id>')
class PortfolioDetail(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功')
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def get(self, portfolio_id):
        """获取投资组合详情（包含持仓）"""
        db: Session = next(get_db())
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        # 获取持仓信息
        holdings = portfolio_service.get_portfolio_holdings(portfolio_id, int(user_id))
        
        return {
            'portfolio': {
                'id': portfolio.id,
                'user_id': portfolio.user_id,
                'name': portfolio.name,
                'description': portfolio.description,
                'benchmark': portfolio.benchmark,
                'risk_level': portfolio.risk_level,
                'is_default': portfolio.is_default,
                'created_at': portfolio.created_at.isoformat() if portfolio.created_at else None,
                'updated_at': portfolio.updated_at.isoformat() if portfolio.updated_at else None
            },
            'holdings': [{
                'id': h.id,
                'portfolio_id': h.portfolio_id,
                'asset_id': h.asset_id,
                'quantity': float(h.quantity) if h.quantity else 0,
                'cost_price': float(h.cost_price) if h.cost_price else 0,
                'current_price': float(h.current_price) if h.current_price else 0,
                'value': float(h.quantity) * float(h.current_price) if h.quantity and h.current_price else 0,
                'profit': (float(h.current_price) - float(h.cost_price)) * float(h.quantity) if h.quantity and h.cost_price and h.current_price else 0,
                'profit_rate': ((float(h.current_price) - float(h.cost_price)) / float(h.cost_price) * 100) if h.cost_price and h.current_price else 0,
                'asset': {
                    'id': h.asset.id,
                    'code': h.asset.code,
                    'name': h.asset.name,
                    'type': h.asset.type,
                    'market': h.asset.market,
                    'industry': h.asset.industry
                } if h.asset else None,
                'created_at': h.created_at.isoformat() if h.created_at else None,
                'updated_at': h.updated_at.isoformat() if h.updated_at else None
            } for h in holdings]
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(portfolio_model)
    @api.response(200, '更新成功', portfolio_model)
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def put(self, portfolio_id):
        """更新投资组合"""
        db: Session = next(get_db())
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        data = request.json
        
        portfolio = portfolio_service.update_portfolio(portfolio_id, data, int(user_id))
        
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        return {
            'id': portfolio.id,
            'user_id': portfolio.user_id,
            'name': portfolio.name,
            'description': portfolio.description,
            'benchmark': portfolio.benchmark,
            'risk_level': portfolio.risk_level,
            'created_at': portfolio.created_at.isoformat() if portfolio.created_at else None,
            'updated_at': portfolio.updated_at.isoformat() if portfolio.updated_at else None
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '删除成功')
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def delete(self, portfolio_id):
        """删除投资组合"""
        db: Session = next(get_db())
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        success = portfolio_service.delete_portfolio(portfolio_id, int(user_id))
        
        if not success:
            api.abort(404, '投资组合不存在')
        
        return {'message': '投资组合删除成功'}