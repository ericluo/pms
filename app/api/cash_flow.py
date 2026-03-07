from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.cash_flow import CashFlowService
from app.services.portfolio import PortfolioService
from app.schemas.cash_flow import CashFlowCreate, CashFlowUpdate, CashFlowResponse

api = Namespace('cash-flows', description='现金流相关操作')

# 模型定义
cash_flow_model = api.model('CashFlow', {
    'id': fields.Integer(readonly=True),
    'portfolio_id': fields.Integer(readonly=True),
    'amount': fields.Float(required=True),
    'flow_type': fields.String(required=True),
    'flow_date': fields.DateTime(required=True),
    'description': fields.String,
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('')
class CashFlowList(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', [cash_flow_model])
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def get(self, portfolio_id=None):
        """获取投资组合现金流列表"""
        db: Session = next(get_db())
        cash_flow_service = CashFlowService(db)
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
        
        cash_flows = cash_flow_service.get_cash_flows(portfolio_id)
        
        return [{
            'id': c.id,
            'portfolio_id': c.portfolio_id,
            'amount': c.amount,
            'flow_type': c.flow_type,
            'flow_date': c.flow_date,
            'description': c.description,
            'created_at': c.created_at,
            'updated_at': c.updated_at
        } for c in cash_flows]
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(cash_flow_model)
    @api.response(201, '创建成功', cash_flow_model)
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def post(self):
        """添加现金流"""
        db: Session = next(get_db())
        cash_flow_service = CashFlowService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/cash-flows', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        data = request.json
        cash_flow = cash_flow_service.create_cash_flow(CashFlowCreate(**data), portfolio_id)
        
        return {
            'id': cash_flow.id,
            'portfolio_id': cash_flow.portfolio_id,
            'amount': cash_flow.amount,
            'flow_type': cash_flow.flow_type,
            'flow_date': cash_flow.flow_date,
            'description': cash_flow.description,
            'created_at': cash_flow.created_at,
            'updated_at': cash_flow.updated_at
        }, 201

@api.route('/<int:cash_flow_id>')
class CashFlowDetail(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', cash_flow_model)
    @api.response(401, '未授权')
    @api.response(404, '现金流不存在')
    def get(self, cash_flow_id):
        """获取现金流详情"""
        db: Session = next(get_db())
        cash_flow_service = CashFlowService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/cash-flows', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        cash_flow = cash_flow_service.get_cash_flow(cash_flow_id, portfolio_id)
        if not cash_flow:
            api.abort(404, '现金流不存在')
        
        return {
            'id': cash_flow.id,
            'portfolio_id': cash_flow.portfolio_id,
            'amount': cash_flow.amount,
            'flow_type': cash_flow.flow_type,
            'flow_date': cash_flow.flow_date,
            'description': cash_flow.description,
            'created_at': cash_flow.created_at,
            'updated_at': cash_flow.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(cash_flow_model)
    @api.response(200, '更新成功', cash_flow_model)
    @api.response(401, '未授权')
    @api.response(404, '现金流不存在')
    def put(self, cash_flow_id):
        """更新现金流"""
        db: Session = next(get_db())
        cash_flow_service = CashFlowService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/cash-flows', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        data = request.json
        cash_flow = cash_flow_service.update_cash_flow(cash_flow_id, CashFlowUpdate(**data), portfolio_id)
        if not cash_flow:
            api.abort(404, '现金流不存在')
        
        return {
            'id': cash_flow.id,
            'portfolio_id': cash_flow.portfolio_id,
            'amount': cash_flow.amount,
            'flow_type': cash_flow.flow_type,
            'flow_date': cash_flow.flow_date,
            'description': cash_flow.description,
            'created_at': cash_flow.created_at,
            'updated_at': cash_flow.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '删除成功')
    @api.response(401, '未授权')
    @api.response(404, '现金流不存在')
    def delete(self, cash_flow_id):
        """删除现金流"""
        db: Session = next(get_db())
        cash_flow_service = CashFlowService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/cash-flows', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        success = cash_flow_service.delete_cash_flow(cash_flow_id, portfolio_id)
        if not success:
            api.abort(404, '现金流不存在')
        
        return {'message': '现金流删除成功'}
