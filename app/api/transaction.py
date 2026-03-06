from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.transaction import TransactionService
from app.services.portfolio import PortfolioService
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse

api = Namespace('transactions', description='交易相关操作')

# 模型定义
transaction_model = api.model('Transaction', {
    'id': fields.Integer(readonly=True),
    'portfolio_id': fields.Integer(readonly=True),
    'asset_id': fields.Integer(required=True),
    'transaction_type': fields.String(required=True),
    'quantity': fields.Float(required=True),
    'price': fields.Float(required=True),
    'amount': fields.Float(readonly=True),
    'transaction_date': fields.DateTime(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('')
class TransactionList(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', [transaction_model])
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def get(self):
        """获取投资组合交易列表"""
        db: Session = next(get_db())
        transaction_service = TransactionService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/transactions', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        transactions = transaction_service.get_transactions(portfolio_id)
        
        return [{
            'id': t.id,
            'portfolio_id': t.portfolio_id,
            'asset_id': t.asset_id,
            'transaction_type': t.transaction_type,
            'quantity': t.quantity,
            'price': t.price,
            'amount': t.amount,
            'transaction_date': t.transaction_date,
            'created_at': t.created_at,
            'updated_at': t.updated_at
        } for t in transactions]
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(transaction_model)
    @api.response(201, '创建成功', transaction_model)
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def post(self):
        """添加交易"""
        db: Session = next(get_db())
        transaction_service = TransactionService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/transactions', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        data = request.json
        transaction = transaction_service.create_transaction(TransactionCreate(**data), portfolio_id)
        
        return {
            'id': transaction.id,
            'portfolio_id': transaction.portfolio_id,
            'asset_id': transaction.asset_id,
            'transaction_type': transaction.transaction_type,
            'quantity': transaction.quantity,
            'price': transaction.price,
            'amount': transaction.amount,
            'transaction_date': transaction.transaction_date,
            'created_at': transaction.created_at,
            'updated_at': transaction.updated_at
        }, 201

@api.route('/<int:transaction_id>')
class TransactionDetail(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', transaction_model)
    @api.response(401, '未授权')
    @api.response(404, '交易不存在')
    def get(self, transaction_id):
        """获取交易详情"""
        db: Session = next(get_db())
        transaction_service = TransactionService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/transactions', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        transaction = transaction_service.get_transaction(transaction_id, portfolio_id)
        if not transaction:
            api.abort(404, '交易不存在')
        
        return {
            'id': transaction.id,
            'portfolio_id': transaction.portfolio_id,
            'asset_id': transaction.asset_id,
            'transaction_type': transaction.transaction_type,
            'quantity': transaction.quantity,
            'price': transaction.price,
            'amount': transaction.amount,
            'transaction_date': transaction.transaction_date,
            'created_at': transaction.created_at,
            'updated_at': transaction.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(transaction_model)
    @api.response(200, '更新成功', transaction_model)
    @api.response(401, '未授权')
    @api.response(404, '交易不存在')
    def put(self, transaction_id):
        """更新交易"""
        db: Session = next(get_db())
        transaction_service = TransactionService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/transactions', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        data = request.json
        transaction = transaction_service.update_transaction(transaction_id, TransactionUpdate(**data), portfolio_id)
        if not transaction:
            api.abort(404, '交易不存在')
        
        return {
            'id': transaction.id,
            'portfolio_id': transaction.portfolio_id,
            'asset_id': transaction.asset_id,
            'transaction_type': transaction.transaction_type,
            'quantity': transaction.quantity,
            'price': transaction.price,
            'amount': transaction.amount,
            'transaction_date': transaction.transaction_date,
            'created_at': transaction.created_at,
            'updated_at': transaction.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '删除成功')
    @api.response(401, '未授权')
    @api.response(404, '交易不存在')
    def delete(self, transaction_id):
        """删除交易"""
        db: Session = next(get_db())
        transaction_service = TransactionService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 从URL路径中获取portfolio_id
        import re
        path = request.path
        match = re.search(r'/portfolios/(\d+)/transactions', path)
        if not match:
            api.abort(400, 'Invalid URL path')
        portfolio_id = int(match.group(1))
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        success = transaction_service.delete_transaction(transaction_id, portfolio_id)
        if not success:
            api.abort(404, '交易不存在')
        
        return {'message': '交易删除成功'}
