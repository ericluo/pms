"""
市场信息查询服务
支持根据股票/基金名称查询代码、价格等市场信息
集成多个外部数据源：新浪财经、腾讯财经、东方财富等
"""
import requests
import re
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.asset import Asset
from app.models.market_data import MarketData


class MarketQueryService:
    """市场信息查询服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    # ========================================================================
    # 核心查询方法
    # ========================================================================
    
    def search_by_name(self, name: str, asset_type: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        根据名称搜索股票或基金
        
        Args:
            name: 股票或基金名称（支持部分匹配）
            asset_type: 资产类型（'stock'/'fund'/'bond'），None 表示全部
            limit: 返回结果数量限制
            
        Returns:
            包含匹配资产的列表，每个资产包含代码、名称、类型、市场价格等信息
        """
        results = []
        
        # 1. 从本地数据库搜索
        local_results = self._search_local_database(name, asset_type, limit)
        results.extend(local_results)
        
        # 2. 如果本地结果不足，从外部 API 搜索
        if len(results) < limit:
            external_results = self._search_external_api(name, asset_type, limit - len(results))
            # 去重（避免与本地结果重复）
            existing_codes = {r['code'] for r in results}
            for ext_result in external_results:
                if ext_result['code'] not in existing_codes:
                    results.append(ext_result)
        
        return results[:limit]
    
    def get_market_info_by_code(self, code: str) -> Optional[Dict]:
        """
        根据代码获取市场信息
        
        Args:
            code: 股票或基金代码
            
        Returns:
            包含完整市场信息的字典，如果不存在则返回 None
        """
        # 1. 从本地数据库获取
        asset = self.db.query(Asset).filter(Asset.code == code).first()
        
        if asset:
            # 获取最新市场数据
            latest_data = self._get_latest_market_data(asset.id)
            return self._build_market_info(asset, latest_data)
        
        # 2. 从外部 API 获取
        return self._fetch_from_external_api(code)
    
    def get_market_info_by_name(self, name: str, exact: bool = False) -> Optional[Dict]:
        """
        根据名称获取市场信息（精确或模糊匹配）
        
        Args:
            name: 股票或基金名称
            exact: 是否精确匹配
            
        Returns:
            匹配的第一个资产的市场信息
        """
        if exact:
            asset = self.db.query(Asset).filter(Asset.name == name).first()
            if asset:
                latest_data = self._get_latest_market_data(asset.id)
                return self._build_market_info(asset, latest_data)
        else:
            # 模糊匹配，返回第一个结果
            asset = self.db.query(Asset).filter(Asset.name.like(f'%{name}%')).first()
            if asset:
                latest_data = self._get_latest_market_data(asset.id)
                return self._build_market_info(asset, latest_data)
        
        return None
    
    # ========================================================================
    # 本地数据库搜索
    # ========================================================================
    
    def _search_local_database(self, name: str, asset_type: Optional[str], limit: int) -> List[Dict]:
        """从本地数据库搜索资产"""
        query = self.db.query(Asset).filter(
            or_(
                Asset.name.like(f'%{name}%'),
                Asset.code.like(f'%{name}%')
            )
        )
        
        if asset_type:
            query = query.filter(Asset.type == asset_type)
        
        assets = query.limit(limit).all()
        
        results = []
        for asset in assets:
            latest_data = self._get_latest_market_data(asset.id)
            results.append(self._build_market_info(asset, latest_data))
        
        return results
    
    def _get_latest_market_data(self, asset_id: int) -> Optional[Dict]:
        """获取资产的最新市场数据"""
        market_data = self.db.query(MarketData).filter(
            MarketData.asset_id == asset_id
        ).order_by(MarketData.date.desc()).first()
        
        if market_data:
            return {
                'price': float(market_data.close),
                'open': float(market_data.open),
                'high': float(market_data.high),
                'low': float(market_data.low),
                'volume': float(market_data.volume),
                'amount': float(market_data.amount),
                'date': market_data.date
            }
        return None
    
    def _build_market_info(self, asset: Asset, market_data: Optional[Dict]) -> Dict:
        """构建市场信息字典"""
        from app.models.asset import ASSET_TYPE_NAMES
        
        info = {
            'code': asset.code,
            'name': asset.name,
            'type': asset.type,
            'type_name': ASSET_TYPE_NAMES.get(asset.type, asset.type),
            'market': asset.market,
            'industry': asset.industry,
            'source': 'local',
            'created_at': asset.created_at.isoformat() if asset.created_at else None
        }
        
        if market_data:
            info.update(market_data)
            # 计算涨跌幅（如果有昨日数据）
            if 'price' in market_data:
                # 简化计算，实际应该与昨日收盘价比较
                info['change'] = 0.0
                info['change_percent'] = 0.0
        
        return info
    
    # ========================================================================
    # 外部 API 集成
    # ========================================================================
    
    def _search_external_api(self, name: str, asset_type: Optional[str], limit: int) -> List[Dict]:
        """从外部 API 搜索资产"""
        results = []
        
        try:
            # 使用新浪财经搜索 API
            if asset_type in [None, 'stock']:
                stock_results = self._search_sina_stock(name, limit)
                results.extend(stock_results)
            
            if asset_type in [None, 'fund']:
                fund_results = self._search_sina_fund(name, limit - len(results))
                results.extend(fund_results)
                
        except Exception as e:
            print(f"外部 API 搜索失败：{e}")
        
        return results
    
    def _search_sina_stock(self, keyword: str, limit: int) -> List[Dict]:
        """
        使用新浪财经搜索股票
        
        API: http://suggest3.sinajs.cn/suggest/key=关键词
        """
        try:
            url = f"http://suggest3.sinajs.cn/suggest/key={keyword}"
            response = self.session.get(url, timeout=5)
            response.encoding = 'utf-8'
            
            # 解析返回结果
            # 格式：var _suggest = "列表 1=股票 1^股票 2^...";
            match = re.search(r'"([^"]*)"', response.text)
            if not match:
                return []
            
            items = match.group(1).split('^')
            results = []
            
            for item in items[:limit]:
                parts = item.split(',')
                if len(parts) >= 3:
                    code = parts[0]
                    # 处理代码前缀
                    if code.startswith('sh') or code.startswith('sz'):
                        code = code[2:]
                    
                    results.append({
                        'code': code,
                        'name': parts[1],
                        'type': 'stock',
                        'type_name': '股票',
                        'market': self._get_market_by_code(code),
                        'source': 'sina',
                        '_full_data': parts  # 保留完整数据用于后续处理
                    })
            
            return results
            
        except Exception as e:
            print(f"新浪财经搜索失败：{e}")
            return []
    
    def _search_sina_fund(self, keyword: str, limit: int) -> List[Dict]:
        """
        使用新浪财经搜索基金
        
        API: http://fund.sina.com.cn/dfxh/search.php?act=2&key=关键词
        """
        try:
            url = f"http://fund.sina.com.cn/dfxh/search.php?act=2&key={keyword}"
            response = self.session.get(url, timeout=5)
            response.encoding = 'gbk'
            
            # 解析 HTML 结果
            # 这里简化处理，实际应该使用 BeautifulSoup
            results = []
            
            # TODO: 实现基金搜索解析
            return results
            
        except Exception as e:
            print(f"新浪基金搜索失败：{e}")
            return []
    
    def _fetch_from_external_api(self, code: str) -> Optional[Dict]:
        """
        从外部 API 获取市场数据
        
        支持的 API:
        1. 新浪财经：http://hq.sinajs.cn/list=sh600519
        2. 腾讯财经：http://qt.gtimg.cn/q=sh600519
        """
        # 尝试多个数据源
        data = self._fetch_sina_market_data(code)
        if not data:
            data = self._fetch_tencent_market_data(code)
        
        return data
    
    def _fetch_sina_market_data(self, code: str) -> Optional[Dict]:
        """
        从新浪财经获取实时行情
        
        API: http://hq.sinajs.cn/list=sh600519
        """
        try:
            # 添加市场前缀
            if not code.startswith('sh') and not code.startswith('sz'):
                if code.startswith('6') or code.startswith('9'):
                    code = 'sh' + code
                else:
                    code = 'sz' + code
            
            url = f"http://hq.sinajs.cn/list={code}"
            response = self.session.get(url, timeout=5)
            response.encoding = 'gbk'
            
            # 解析结果
            # 格式：var hq_str_sh600519="股票名，开盘，昨收，当前，最高，最低，..."
            match = re.search(r'"([^"]*)"', response.text)
            if not match:
                return None
            
            parts = match.group(1).split(',')
            if len(parts) < 32:
                return None
            
            return {
                'code': code[2:],
                'name': parts[0],
                'price': float(parts[3]) if parts[3] else 0,
                'open': float(parts[1]) if parts[1] else 0,
                'high': float(parts[4]) if parts[4] else 0,
                'low': float(parts[5]) if parts[5] else 0,
                'close': float(parts[2]) if parts[2] else 0,  # 昨收
                'current_price': float(parts[3]) if parts[3] else 0,
                'change': float(parts[3]) - float(parts[2]) if parts[3] and parts[2] else 0,
                'change_percent': ((float(parts[3]) - float(parts[2])) / float(parts[2]) * 100) if parts[2] else 0,
                'volume': float(parts[8]) if parts[8] else 0,
                'amount': float(parts[9]) if parts[9] else 0,
                'source': 'sina_realtime',
                'update_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"新浪财经行情获取失败：{e}")
            return None
    
    def _fetch_tencent_market_data(self, code: str) -> Optional[Dict]:
        """
        从腾讯财经获取实时行情
        
        API: http://qt.gtimg.cn/q=sh600519
        """
        try:
            # 添加市场前缀
            if not code.startswith('sh') and not code.startswith('sz'):
                if code.startswith('6') or code.startswith('9'):
                    code = 'sh' + code
                else:
                    code = 'sz' + code
            
            url = f"http://qt.gtimg.cn/q={code}"
            response = self.session.get(url, timeout=5)
            response.encoding = 'gbk'
            
            # 解析结果
            # 格式：v_sh600519="51~贵州茅台~600519~1850.00~..."
            match = re.search(r'"([^"]*)"', response.text)
            if not match:
                return None
            
            parts = match.group(1).split('~')
            if len(parts) < 50:
                return None
            
            return {
                'code': code[2:],
                'name': parts[1],
                'price': float(parts[3]) if parts[3] else 0,
                'open': float(parts[5]) if parts[5] else 0,
                'high': float(parts[33]) if parts[33] else 0,
                'low': float(parts[34]) if parts[34] else 0,
                'close': float(parts[4]) if parts[4] else 0,  # 昨收
                'current_price': float(parts[3]) if parts[3] else 0,
                'change': float(parts[32]) if parts[32] else 0,
                'change_percent': float(parts[39]) if parts[39] else 0,
                'volume': float(parts[6]) if parts[6] else 0,
                'amount': float(parts[37]) if parts[37] else 0,
                'source': 'tencent',
                'update_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"腾讯财经行情获取失败：{e}")
            return None
    
    def _get_market_by_code(self, code: str) -> str:
        """根据代码判断市场"""
        if code.startswith('6') or code.startswith('9'):
            return '上海证券交易所'
        elif code.startswith('0') or code.startswith('3'):
            return '深圳证券交易所'
        elif code.startswith('4') or code.startswith('8'):
            return '北京证券交易所'
        return ''
    
    # ========================================================================
    # 数据同步方法
    # ========================================================================
    
    def sync_market_data(self, code: str) -> bool:
        """
        同步市场数据到本地数据库
        
        Args:
            code: 股票或基金代码
            
        Returns:
            是否同步成功
        """
        try:
            # 1. 获取或创建资产
            asset = self.db.query(Asset).filter(Asset.code == code).first()
            
            if not asset:
                # 从外部 API 获取资产信息
                external_info = self._fetch_from_external_api(code)
                if not external_info:
                    return False
                
                asset = Asset(
                    code=code,
                    name=external_info['name'],
                    type='stock',
                    market=self._get_market_by_code(code)
                )
                self.db.add(asset)
                self.db.commit()
                self.db.refresh(asset)
            
            # 2. 获取实时行情
            market_info = self._fetch_from_external_api(code)
            if not market_info:
                return False
            
            # 3. 创建市场数据记录
            today = datetime.now().date()
            existing_data = self.db.query(MarketData).filter(
                MarketData.asset_id == asset.id,
                MarketData.date == today
            ).first()
            
            if existing_data:
                # 更新现有记录
                existing_data.open = market_info['open']
                existing_data.high = market_info['high']
                existing_data.low = market_info['low']
                existing_data.close = market_info['price']
                existing_data.volume = market_info['volume']
                existing_data.amount = market_info['amount']
            else:
                # 创建新记录
                new_data = MarketData(
                    asset_id=asset.id,
                    date=today,
                    open=market_info['open'],
                    high=market_info['high'],
                    low=market_info['low'],
                    close=market_info['price'],
                    volume=market_info['volume'],
                    amount=market_info['amount']
                )
                self.db.add(new_data)
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            print(f"同步市场数据失败：{e}")
            return False
    
    def sync_all_assets(self) -> Tuple[int, int]:
        """
        同步所有资产的市场数据
        
        Returns:
            (成功数量，失败数量)
        """
        assets = self.db.query(Asset).filter(Asset.type.in_(['stock', 'fund'])).all()
        
        success_count = 0
        fail_count = 0
        
        for asset in assets:
            # 添加延时避免请求过快
            time.sleep(0.5)
            
            if self.sync_market_data(asset.code):
                success_count += 1
            else:
                fail_count += 1
        
        return success_count, fail_count


# 便捷函数
def search_stock_by_name(name: str, db: Session, limit: int = 10) -> List[Dict]:
    """便捷函数：搜索股票"""
    service = MarketQueryService(db)
    return service.search_by_name(name, asset_type='stock', limit=limit)


def search_fund_by_name(name: str, db: Session, limit: int = 10) -> List[Dict]:
    """便捷函数：搜索基金"""
    service = MarketQueryService(db)
    return service.search_by_name(name, asset_type='fund', limit=limit)


def get_market_info(code: str, db: Session) -> Optional[Dict]:
    """便捷函数：获取市场信息"""
    service = MarketQueryService(db)
    return service.get_market_info_by_code(code)
