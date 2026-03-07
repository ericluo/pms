from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.market_query import MarketQueryService

api = Namespace('market_query', description='市场信息查询')

# 模型定义
market_info_model = api.model('MarketInfo', {
    'code': fields.String(description='代码', readonly=True),
    'name': fields.String(description='名称', readonly=True),
    'type': fields.String(description='类型', readonly=True),
    'type_name': fields.String(description='类型名称', readonly=True),
    'market': fields.String(description='市场', readonly=True),
    'industry': fields.String(description='行业', readonly=True),
    'price': fields.Float(description='当前价格'),
    'open': fields.Float(description='开盘价'),
    'high': fields.Float(description='最高价'),
    'low': fields.Float(description='最低价'),
    'close': fields.Float(description='昨收价'),
    'change': fields.Float(description='涨跌额'),
    'change_percent': fields.Float(description='涨跌幅'),
    'volume': fields.Float(description='成交量'),
    'amount': fields.Float(description='成交额'),
    'source': fields.String(description='数据来源'),
    'update_time': fields.DateTime(description='更新时间')
})

search_result_model = api.model('SearchResult', {
    'total': fields.Integer(description='结果总数'),
    'results': fields.List(fields.Nested(market_info_model), description='搜索结果列表')
})


@api.route('/search')
class MarketSearch(Resource):
    @api.doc(params={
        'q': '搜索关键词（名称或代码）',
        'type': '资产类型（stock/fund/bond，可选）',
        'limit': '返回结果数量限制（默认 10）'
    })
    @api.response(200, '搜索成功', search_result_model)
    def get(self):
        """搜索股票或基金"""
        db: Session = next(get_db())
        service = MarketQueryService(db)
        
        # 获取参数
        keyword = request.args.get('q', '')
        asset_type = request.args.get('type')
        limit = request.args.get('limit', 10, type=int)
        
        if not keyword:
            api.abort(400, '请提供搜索关键词')
        
        # 执行搜索
        results = service.search_by_name(keyword, asset_type, limit)
        
        return {
            'total': len(results),
            'results': results
        }


@api.route('/info/<string:code>')
class MarketInfo(Resource):
    @api.doc(params={'code': '股票或基金代码'})
    @api.response(200, '获取成功', market_info_model)
    @api.response(404, '未找到该资产')
    def get(self, code):
        """根据代码获取市场信息"""
        db: Session = next(get_db())
        service = MarketQueryService(db)
        
        info = service.get_market_info_by_code(code)
        
        if not info:
            api.abort(404, f'未找到代码为 {code} 的资产')
        
        return info


@api.route('/name/<string:name>')
class MarketInfoByName(Resource):
    @api.doc(params={
        'name': '股票或基金名称',
        'exact': '是否精确匹配（true/false，默认 false）'
    })
    @api.response(200, '获取成功', market_info_model)
    @api.response(404, '未找到该资产')
    def get(self, name):
        """根据名称获取市场信息"""
        db: Session = next(get_db())
        service = MarketQueryService(db)
        
        exact = request.args.get('exact', 'false').lower() == 'true'
        
        info = service.get_market_info_by_name(name, exact)
        
        if not info:
            api.abort(404, f'未找到名称为 {name} 的资产')
        
        return info


@api.route('/sync/<string:code>')
class MarketSync(Resource):
    @api.doc(params={'code': '股票或基金代码'})
    @api.response(200, '同步成功')
    @api.response(400, '同步失败')
    @jwt_required()
    def post(self, code):
        """同步单个资产的市场数据"""
        db: Session = next(get_db())
        service = MarketQueryService(db)
        
        success = service.sync_market_data(code)
        
        if success:
            return {'message': f'成功同步 {code} 的市场数据'}
        else:
            api.abort(400, f'同步 {code} 失败')


@api.route('/sync-all')
class MarketSyncAll(Resource):
    @api.response(200, '批量同步结果')
    @jwt_required()
    def post(self):
        """批量同步所有资产的市场数据"""
        db: Session = next(get_db())
        service = MarketQueryService(db)
        
        success_count, fail_count = service.sync_all_assets()
        
        return {
            'message': '批量同步完成',
            'success': success_count,
            'failed': fail_count,
            'total': success_count + fail_count
        }


@api.route('/stock/list')
class StockList(Resource):
    @api.doc(params={
        'q': '搜索关键词（可选）',
        'limit': '返回结果数量限制（默认 10）'
    })
    @api.response(200, '获取成功')
    def get(self):
        """获取股票列表"""
        db: Session = next(get_db())
        service = MarketQueryService(db)
        
        keyword = request.args.get('q', '')
        limit = request.args.get('limit', 10, type=int)
        
        if keyword:
            results = service.search_by_name(keyword, asset_type='stock', limit=limit)
        else:
            # 获取本地数据库中的所有股票
            from app.models.asset import Asset
            stocks = db.query(Asset).filter(Asset.type == 'stock').limit(limit).all()
            results = []
            for stock in stocks:
                info = service.get_market_info_by_code(stock.code)
                if info:
                    results.append(info)
        
        return {
            'total': len(results),
            'results': results
        }


@api.route('/fund/list')
class FundList(Resource):
    @api.doc(params={
        'q': '搜索关键词（可选）',
        'limit': '返回结果数量限制（默认 10）'
    })
    @api.response(200, '获取成功')
    def get(self):
        """获取基金列表"""
        db: Session = next(get_db())
        service = MarketQueryService(db)
        
        keyword = request.args.get('q', '')
        limit = request.args.get('limit', 10, type=int)
        
        if keyword:
            results = service.search_by_name(keyword, asset_type='fund', limit=limit)
        else:
            from app.models.asset import Asset
            funds = db.query(Asset).filter(Asset.type == 'fund').limit(limit).all()
            results = []
            for fund in funds:
                info = service.get_market_info_by_code(fund.code)
                if info:
                    results.append(info)
        
        return {
            'total': len(results),
            'results': results
        }
