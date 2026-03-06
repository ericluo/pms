from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.asset import AssetService
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse

api = Namespace('assets', description='资产相关操作')

# 模型定义
asset_model = api.model('Asset', {
    'id': fields.Integer(readonly=True),
    'code': fields.String(required=True),
    'name': fields.String(required=True),
    'type': fields.String(required=True),
    'market': fields.String(required=True),
    'industry': fields.String,
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('')
class AssetList(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', [asset_model])
    @api.response(401, '未授权')
    def get(self):
        """获取资产列表"""
        db: Session = next(get_db())
        asset_service = AssetService(db)
        
        assets = asset_service.get_assets()
        
        return [{
            'id': a.id,
            'code': a.code,
            'name': a.name,
            'type': a.type,
            'market': a.market,
            'industry': a.industry,
            'created_at': a.created_at,
            'updated_at': a.updated_at
        } for a in assets]
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(asset_model)
    @api.response(201, '创建成功', asset_model)
    @api.response(401, '未授权')
    def post(self):
        """创建资产"""
        db: Session = next(get_db())
        asset_service = AssetService(db)
        
        data = request.json
        asset = asset_service.create_asset(AssetCreate(**data))
        
        return {
            'id': asset.id,
            'code': asset.code,
            'name': asset.name,
            'type': asset.type,
            'market': asset.market,
            'industry': asset.industry,
            'created_at': asset.created_at,
            'updated_at': asset.updated_at
        }, 201

@api.route('/<int:asset_id>')
class AssetDetail(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功', asset_model)
    @api.response(401, '未授权')
    @api.response(404, '资产不存在')
    def get(self, asset_id):
        """获取资产详情"""
        db: Session = next(get_db())
        asset_service = AssetService(db)
        
        asset = asset_service.get_asset(asset_id)
        
        if not asset:
            api.abort(404, '资产不存在')
        
        return {
            'id': asset.id,
            'code': asset.code,
            'name': asset.name,
            'type': asset.type,
            'market': asset.market,
            'industry': asset.industry,
            'created_at': asset.created_at,
            'updated_at': asset.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.expect(asset_model)
    @api.response(200, '更新成功', asset_model)
    @api.response(401, '未授权')
    @api.response(404, '资产不存在')
    def put(self, asset_id):
        """更新资产"""
        db: Session = next(get_db())
        asset_service = AssetService(db)
        
        data = request.json
        asset = asset_service.update_asset(asset_id, AssetUpdate(**data))
        
        if not asset:
            api.abort(404, '资产不存在')
        
        return {
            'id': asset.id,
            'code': asset.code,
            'name': asset.name,
            'type': asset.type,
            'market': asset.market,
            'industry': asset.industry,
            'created_at': asset.created_at,
            'updated_at': asset.updated_at
        }
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '删除成功')
    @api.response(401, '未授权')
    @api.response(404, '资产不存在')
    def delete(self, asset_id):
        """删除资产"""
        db: Session = next(get_db())
        asset_service = AssetService(db)
        
        success = asset_service.delete_asset(asset_id)
        
        if not success:
            api.abort(404, '资产不存在')
        
        return {'message': '资产删除成功'}