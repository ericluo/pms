from datetime import date
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.holding import HoldingService
from app.services.portfolio import PortfolioService
from app.schemas.holding import HoldingCreate, HoldingUpdate, HoldingResponse

# 持仓相关 API
api = Namespace('holdings', description='持仓相关操作')

# 持仓快照相关 API
snapshot_api = Namespace('portfolio_snapshots', description='持仓快照相关操作')

# 调整相关模型
adjustment_item_model = snapshot_api.model('AdjustmentItem', {
    'asset_id': fields.Integer(required=True, description='资产 ID'),
    'adjustment_action': fields.String(
        required=True, 
        enum=['increase', 'decrease'],
        description='调整动作：increase(增) 或 decrease(减)'
    ),
    'quantity_change': fields.Float(required=True, description='调整数量（正数）'),
    'price': fields.Float(required=True, description='参考价格'),
    'currency': fields.String(description='交易币种', example='CNY'),
    'reason': fields.String(description='调整原因')
})

create_adjustment_model = snapshot_api.model('CreateAdjustment', {
    'adjustment_date': fields.String(required=True, description='调仓日期', example='2026-02-02'),
    'holdings': fields.List(
        fields.Nested(adjustment_item_model),
        required=True,
        description='持仓调整列表'
    )
})

# 模型定义
holding_model = api.model('Holding', {
    'id': fields.Integer(readonly=True),
    'portfolio_id': fields.Integer(readonly=True),
    'asset_id': fields.Integer(required=True),
    'quantity': fields.Float(required=True),
    'cost_price': fields.Float(required=True),
    'current_price': fields.Float(required=True),
    'value': fields.Float(readonly=True),
    'profit': fields.Float(readonly=True),
    'profit_percent': fields.Float(readonly=True),
    'weight': fields.Float(readonly=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('')
class HoldingList(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', [holding_model])
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def get(self, portfolio_id=None):
        """获取投资组合持仓列表"""
        db: Session = next(get_db())
        holding_service = HoldingService(db)
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
        
        holdings = holding_service.get_holdings(portfolio_id)
        holdings_with_metrics = holding_service.calculate_portfolio_weights(holdings)
        
        return holdings_with_metrics
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(holding_model)
    @api.response(201, '创建成功', holding_model)
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def post(self, portfolio_id=None):
        """添加持仓"""
        db: Session = next(get_db())
        holding_service = HoldingService(db)
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
        
        data = request.json
        holding = holding_service.create_holding(data, portfolio_id)
        
        # 计算持仓指标
        holdings = holding_service.get_holdings(portfolio_id)
        holdings_with_metrics = holding_service.calculate_portfolio_weights(holdings)
        
        # 找到刚创建的持仓
        created_holding = next((h for h in holdings_with_metrics if h['id'] == holding.id), None)
        
        return created_holding, 201

@api.route('/<int:holding_id>')
class HoldingDetail(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', holding_model)
    @api.response(401, '未授权')
    @api.response(404, '持仓不存在')
    def get(self, portfolio_id, holding_id):
        """获取持仓详情"""
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        holding = holding_service.get_holding(holding_id, portfolio_id)
        if not holding:
            api.abort(404, '持仓不存在')
        
        # 计算持仓指标
        metrics = holding_service.calculate_holding_metrics(holding)
        
        return {
            'id': holding.id,
            'portfolio_id': holding.portfolio_id,
            'asset_id': holding.asset_id,
            'quantity': holding.quantity,
            'cost_price': holding.cost_price,
            'current_price': holding.current_price,
            'value': metrics['value'],
            'profit': metrics['profit'],
            'profit_percent': metrics['profit_percent'],
            'weight': 0,  # 需要计算权重
            'created_at': holding.created_at,
            'updated_at': holding.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(holding_model)
    @api.response(200, '更新成功', holding_model)
    @api.response(401, '未授权')
    @api.response(404, '持仓不存在')
    def put(self, portfolio_id, holding_id):
        """更新持仓"""
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        data = request.json
        holding = holding_service.update_holding(holding_id, HoldingUpdate(**data), portfolio_id)
        if not holding:
            api.abort(404, '持仓不存在')
        
        # 计算持仓指标
        metrics = holding_service.calculate_holding_metrics(holding)
        
        return {
            'id': holding.id,
            'portfolio_id': holding.portfolio_id,
            'asset_id': holding.asset_id,
            'quantity': holding.quantity,
            'cost_price': holding.cost_price,
            'current_price': holding.current_price,
            'value': metrics['value'],
            'profit': metrics['profit'],
            'profit_percent': metrics['profit_percent'],
            'weight': 0,  # 需要计算权重
            'created_at': holding.created_at,
            'updated_at': holding.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '删除成功')
    @api.response(401, '未授权')
    @api.response(404, '持仓不存在')
    def delete(self, portfolio_id, holding_id):
        """删除持仓"""
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        
        # 验证投资组合是否属于该用户
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        success = holding_service.delete_holding(holding_id, portfolio_id)
        if not success:
            api.abort(404, '持仓不存在')
        
        return {'message': '持仓删除成功'}


@snapshot_api.route('/<int:portfolio_id>/snapshot-dates')
class SnapshotDatesResource(Resource):
    @snapshot_api.doc(security='Bearer')
    @jwt_required()
    @snapshot_api.response(200, '获取成功')
    @snapshot_api.response(401, '未授权')
    @snapshot_api.response(404, '投资组合不存在')
    def get(self, portfolio_id):
        """获取所有有持仓快照的日期列表"""
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            snapshot_api.abort(404, '投资组合不存在')
        
        dates = holding_service.get_snapshot_dates(portfolio_id)
        return dates, 200


@snapshot_api.route('/<int:portfolio_id>/snapshots')
class PortfolioSnapshotResource(Resource):
    @snapshot_api.doc(security='Bearer')
    @jwt_required()
    @snapshot_api.param('date', '查询日期（YYYY-MM-DD）', required=True)
    @snapshot_api.response(200, '获取成功')
    @snapshot_api.response(400, '日期参数错误')
    @snapshot_api.response(404, '投资组合不存在')
    def get(self, portfolio_id):
        """获取指定日期的持仓快照"""
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            snapshot_api.abort(404, '投资组合不存在')
        
        date_str = request.args.get('date')
        if not date_str:
            snapshot_api.abort(400, 'Missing required parameter: date')
        
        try:
            target_date = date.fromisoformat(date_str)
        except ValueError:
            snapshot_api.abort(400, 'Invalid date format. Use YYYY-MM-DD')
        
        holdings = holding_service.get_holdings_on_date(portfolio_id, target_date)
        total_market_value = sum(h['market_value'] for h in holdings) if holdings else 0
        
        return {
            'date': date_str,
            'portfolio_id': portfolio_id,
            'total_market_value': total_market_value,
            'holdings': holdings
        }, 200
    
    @snapshot_api.doc(security='Bearer')
    @jwt_required()
    @snapshot_api.param('date', '创建/更新快照日期（YYYY-MM-DD）', required=True)
    @snapshot_api.response(201, '创建成功')
    @snapshot_api.response(400, '请求参数错误')
    @snapshot_api.response(404, '投资组合不存在')
    def post(self, portfolio_id):
        """创建或更新指定日期的持仓快照"""
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            snapshot_api.abort(404, '投资组合不存在')
        
        date_str = request.args.get('date')
        if not date_str:
            snapshot_api.abort(400, 'Missing required parameter: date')
        
        try:
            snapshot_date = date.fromisoformat(date_str)
        except ValueError:
            snapshot_api.abort(400, 'Invalid date format')
        
        result = holding_service.create_or_update_snapshot(portfolio_id, snapshot_date)
        
        return {
            'success': True,
            'snapshot_date': date_str,
            **result
        }, 201


@snapshot_api.route('/<int:portfolio_id>/snapshots/<string:date_str>')
class SnapshotDateResource(Resource):
    @snapshot_api.doc(security='Bearer')
    @jwt_required()
    @snapshot_api.response(200, '删除成功')
    @snapshot_api.response(400, '日期格式错误')
    @snapshot_api.response(404, '投资组合不存在')
    def delete(self, portfolio_id, date_str):
        """删除指定日期的持仓快照"""
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            snapshot_api.abort(404, '投资组合不存在')
        
        try:
            snapshot_date = date.fromisoformat(date_str)
        except ValueError:
            snapshot_api.abort(400, 'Invalid date format')
        
        deleted_count = holding_service.delete_snapshot(portfolio_id, snapshot_date)
        
        return {
            'success': True,
            'deleted_count': deleted_count
        }, 200