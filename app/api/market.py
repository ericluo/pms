from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.market import MarketService

api = Namespace('market', description='市场数据相关操作')

# 模型定义
market_data_model = api.model('MarketData', {
    'id': fields.Integer(readonly=True),
    'asset_id': fields.Integer(required=True),
    'date': fields.DateTime(required=True),
    'open': fields.Float,
    'high': fields.Float,
    'low': fields.Float,
    'close': fields.Float,
    'volume': fields.Float,
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('/data')
class MarketDataList(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', [market_data_model])
    @api.response(401, '未授权')
    def get(self):
        """获取市场数据列表"""
        db: Session = next(get_db())
        market_service = MarketService(db)
        
        asset_id = request.args.get('asset_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        market_data = market_service.get_market_data(asset_id, start_date, end_date)
        
        return [{
            'id': m.id,
            'asset_id': m.asset_id,
            'date': m.date,
            'open': m.open,
            'high': m.high,
            'low': m.low,
            'close': m.close,
            'volume': m.volume,
            'created_at': m.created_at,
            'updated_at': m.updated_at
        } for m in market_data]
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(market_data_model)
    @api.response(201, '创建成功', market_data_model)
    @api.response(401, '未授权')
    def post(self):
        """添加市场数据"""
        db: Session = next(get_db())
        market_service = MarketService(db)
        
        data = request.json
        market_data = market_service.create_market_data(data)
        
        return {
            'id': market_data.id,
            'asset_id': market_data.asset_id,
            'date': market_data.date,
            'open': market_data.open,
            'high': market_data.high,
            'low': market_data.low,
            'close': market_data.close,
            'volume': market_data.volume,
            'created_at': market_data.created_at,
            'updated_at': market_data.updated_at
        }, 201

@api.route('/data/<int:market_data_id>')
class MarketDataDetail(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', market_data_model)
    @api.response(401, '未授权')
    @api.response(404, '市场数据不存在')
    def get(self, market_data_id):
        """获取市场数据详情"""
        db: Session = next(get_db())
        market_service = MarketService(db)
        
        market_data = market_service.get_market_data_by_id(market_data_id)
        if not market_data:
            api.abort(404, '市场数据不存在')
        
        return {
            'id': market_data.id,
            'asset_id': market_data.asset_id,
            'date': market_data.date,
            'open': market_data.open,
            'high': market_data.high,
            'low': market_data.low,
            'close': market_data.close,
            'volume': market_data.volume,
            'created_at': market_data.created_at,
            'updated_at': market_data.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(market_data_model)
    @api.response(200, '更新成功', market_data_model)
    @api.response(401, '未授权')
    @api.response(404, '市场数据不存在')
    def put(self, market_data_id):
        """更新市场数据"""
        db: Session = next(get_db())
        market_service = MarketService(db)
        
        data = request.json
        market_data = market_service.update_market_data(market_data_id, data)
        if not market_data:
            api.abort(404, '市场数据不存在')
        
        return {
            'id': market_data.id,
            'asset_id': market_data.asset_id,
            'date': market_data.date,
            'open': market_data.open,
            'high': market_data.high,
            'low': market_data.low,
            'close': market_data.close,
            'volume': market_data.volume,
            'created_at': market_data.created_at,
            'updated_at': market_data.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '删除成功')
    @api.response(401, '未授权')
    @api.response(404, '市场数据不存在')
    def delete(self, market_data_id):
        """删除市场数据"""
        db: Session = next(get_db())
        market_service = MarketService(db)
        
        success = market_service.delete_market_data(market_data_id)
        if not success:
            api.abort(404, '市场数据不存在')
        
        return {'message': '市场数据删除成功'}
