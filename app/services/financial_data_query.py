"""
Financial Data Query Service
Provides real-time and historical market data with on-demand query mechanism
Supports stocks, options, and portfolio holdings查询
"""
import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.asset import Asset
from app.models.market_data import MarketData
from app.models.holding import Holding
from app.models.portfolio import Portfolio


class FinancialDataQueryService:
    """
    Financial data query service with on-demand update mechanism
    Provides real-time prices, portfolio holdings, and historical data
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self._cache = {}
        self._cache_timeout = 1  # 1 second cache timeout
    
    # ========================================================================
    # Requirement 1: Real-time Price Data
    # ========================================================================
    
    def get_realtime_price(self, instrument_code: str, instrument_type: str = 'stock') -> Dict[str, Any]:
        """
        Get real-time price data for a financial instrument
        
        Args:
            instrument_code: Instrument code (e.g., '600036' for stock)
            instrument_type: Type of instrument ('stock', 'option', 'fund', etc.)
            
        Returns:
            Dictionary containing:
            - timestamp: Data retrieval timestamp
            - code: Instrument code
            - name: Instrument name
            - type: Instrument type
            - bid_price: Current bid price
            - ask_price: Current ask price
            - last_price: Last traded price
            - current_price: Current market price
            - open: Opening price
            - high: Highest price
            - low: Lowest price
            - close: Previous close price
            - volume: Trading volume
            - amount: Trading amount
            - change: Price change
            - change_percent: Price change percentage
            - data_source: Data source name
            - latency_ms: Data latency in milliseconds
            
        Example:
            >>> service.get_realtime_price('600036', 'stock')
            {
                'timestamp': '2026-03-07T10:30:00.123456',
                'code': '600036',
                'name': '招商银行',
                'type': 'stock',
                'bid_price': 33.00,
                'ask_price': 33.02,
                'last_price': 33.01,
                'current_price': 33.01,
                ...
            }
        """
        start_time = time.time()
        
        # Check cache first (1 second validity)
        cache_key = f"realtime_{instrument_code}"
        if cache_key in self._cache:
            cached_data, cache_time = self._cache[cache_key]
            if (datetime.now() - cache_time).total_seconds() < self._cache_timeout:
                return cached_data
        
        # Fetch real-time data
        try:
            if instrument_type == 'stock':
                realtime_data = self._fetch_stock_realtime_data(instrument_code)
            elif instrument_type == 'option':
                realtime_data = self._fetch_option_realtime_data(instrument_code)
            elif instrument_type == 'fund':
                realtime_data = self._fetch_fund_realtime_data(instrument_code)
            else:
                realtime_data = self._fetch_generic_realtime_data(instrument_code, instrument_type)
            
            if not realtime_data:
                return self._build_error_response(instrument_code, "Data not available")
            
            # Add metadata
            realtime_data['timestamp'] = datetime.now().isoformat()
            realtime_data['code'] = instrument_code
            realtime_data['type'] = instrument_type
            
            # Calculate latency
            latency_ms = int((time.time() - start_time) * 1000)
            realtime_data['latency_ms'] = latency_ms
            
            # Verify latency requirement (< 1000ms)
            if latency_ms > 1000:
                realtime_data['warning'] = f"High latency: {latency_ms}ms (target: <1000ms)"
            
            # Cache the result
            self._cache[cache_key] = (realtime_data, datetime.now())
            
            return realtime_data
            
        except Exception as e:
            return self._build_error_response(instrument_code, str(e))
    
    def _fetch_stock_realtime_data(self, code: str) -> Optional[Dict[str, Any]]:
        """Fetch real-time stock data from Sina/Tencent API"""
        try:
            # Add market prefix
            if not code.startswith('sh') and not code.startswith('sz'):
                if code.startswith('6') or code.startswith('9'):
                    code = 'sh' + code
                else:
                    code = 'sz' + code
            
            # Try Sina API first
            url = f"http://hq.sinajs.cn/list={code}"
            response = self.session.get(url, timeout=2)
            response.encoding = 'gbk'
            
            # Parse response
            # Format: var hq_str_sh600036="name,open,prev_close,current,high,low,..."
            import re
            match = re.search(r'"([^"]*)"', response.text)
            if not match:
                return None
            
            parts = match.group(1).split(',')
            if len(parts) < 32:
                return None
            
            current_price = float(parts[3]) if parts[3] else 0
            prev_close = float(parts[2]) if parts[2] else 0
            
            return {
                'name': parts[0],
                'current_price': current_price,
                'last_price': current_price,
                'bid_price': current_price - 0.01,  # Estimate
                'ask_price': current_price + 0.01,  # Estimate
                'open': float(parts[1]) if parts[1] else 0,
                'high': float(parts[4]) if parts[4] else 0,
                'low': float(parts[5]) if parts[5] else 0,
                'close': prev_close,
                'change': current_price - prev_close,
                'change_percent': ((current_price - prev_close) / prev_close * 100) if prev_close else 0,
                'volume': float(parts[8]) if parts[8] else 0,
                'amount': float(parts[9]) if parts[9] else 0,
                'data_source': 'sina'
            }
            
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return None
    
    def _fetch_option_realtime_data(self, code: str) -> Optional[Dict[str, Any]]:
        """Fetch real-time option data"""
        # TODO: Implement option data fetching from appropriate API
        # For now, return placeholder
        return {
            'name': f"Option {code}",
            'current_price': 0.0,
            'last_price': 0.0,
            'bid_price': 0.0,
            'ask_price': 0.0,
            'open': 0.0,
            'high': 0.0,
            'low': 0.0,
            'close': 0.0,
            'change': 0.0,
            'change_percent': 0.0,
            'volume': 0.0,
            'amount': 0.0,
            'data_source': 'placeholder'
        }
    
    def _fetch_fund_realtime_data(self, code: str) -> Optional[Dict[str, Any]]:
        """Fetch real-time fund data"""
        # TODO: Implement fund data fetching
        return None
    
    def _fetch_generic_realtime_data(self, code: str, instrument_type: str) -> Optional[Dict[str, Any]]:
        """Fetch generic instrument data"""
        return None
    
    def _build_error_response(self, code: str, error_message: str) -> Dict[str, Any]:
        """Build error response"""
        return {
            'timestamp': datetime.now().isoformat(),
            'code': code,
            'error': error_message,
            'bid_price': None,
            'ask_price': None,
            'last_price': None,
            'current_price': None,
            'data_source': 'error',
            'latency_ms': 0
        }
    
    # ========================================================================
    # Requirement 2: Portfolio Holdings
    # ========================================================================
    
    def get_portfolio_holdings(self, portfolio_id: int, user_id: int) -> Dict[str, Any]:
        """
        Get current holdings information for user's portfolio
        
        Args:
            portfolio_id: Portfolio ID
            user_id: User ID (for authorization)
            
        Returns:
            Dictionary containing:
            - timestamp: Query timestamp
            - portfolio_id: Portfolio ID
            - portfolio_name: Portfolio name
            - user_id: User ID
            - total_market_value: Total market value of portfolio
            - total_cost: Total cost basis
            - total_unrealized_pnl: Total unrealized profit/loss
            - total_unrealized_pnl_percent: Total unrealized P&L percentage
            - holdings: List of holdings with details
            - data_source: Data source
            - latency_ms: Query latency
            
        Example:
            >>> service.get_portfolio_holdings(1, 1)
            {
                'timestamp': '2026-03-07T10:30:00.123456',
                'portfolio_id': 1,
                'portfolio_name': 'My Portfolio',
                'holdings': [
                    {
                        'ticker': '600036',
                        'name': '招商银行',
                        'quantity': 1000,
                        'purchase_price': 30.00,
                        'current_price': 33.00,
                        'market_value': 33000.00,
                        'cost_basis': 30000.00,
                        'unrealized_pnl': 3000.00,
                        'unrealized_pnl_percent': 10.0,
                        ...
                    },
                    ...
                ],
                ...
            }
        """
        start_time = time.time()
        
        try:
            # Verify portfolio ownership
            portfolio = self.db.query(Portfolio).filter(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id
            ).first()
            
            if not portfolio:
                return {
                    'timestamp': datetime.now().isoformat(),
                    'error': 'Portfolio not found or access denied',
                    'holdings': [],
                    'data_source': 'error'
                }
            
            # Get all holdings
            holdings = self.db.query(Holding).filter(
                Holding.portfolio_id == portfolio_id
            ).all()
            
            holdings_data = []
            total_market_value = 0.0
            total_cost = 0.0
            
            for holding in holdings:
                # Get current market price
                current_price = self._get_current_price(holding.asset_id)
                
                # Calculate metrics
                quantity = float(holding.quantity) if holding.quantity else 0
                purchase_price = float(holding.cost_price) if holding.cost_price else 0
                market_value = quantity * current_price
                cost_basis = quantity * purchase_price
                unrealized_pnl = market_value - cost_basis
                unrealized_pnl_percent = (unrealized_pnl / cost_basis * 100) if cost_basis else 0
                
                holding_data = {
                    'ticker': holding.asset.code if holding.asset else 'N/A',
                    'name': holding.asset.name if holding.asset else 'N/A',
                    'type': holding.asset.type if holding.asset else 'N/A',
                    'quantity': quantity,
                    'purchase_price': purchase_price,
                    'current_price': current_price,
                    'market_value': round(market_value, 2),
                    'cost_basis': round(cost_basis, 2),
                    'unrealized_pnl': round(unrealized_pnl, 2),
                    'unrealized_pnl_percent': round(unrealized_pnl_percent, 2),
                    'holding_id': holding.id,
                    'asset_id': holding.asset_id,
                    'created_at': holding.created_at.isoformat() if holding.created_at else None,
                    'updated_at': holding.updated_at.isoformat() if holding.updated_at else None
                }
                
                holdings_data.append(holding_data)
                total_market_value += market_value
                total_cost += cost_basis
            
            # Calculate totals
            total_unrealized_pnl = total_market_value - total_cost
            total_unrealized_pnl_percent = (total_unrealized_pnl / total_cost * 100) if total_cost else 0
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'portfolio_id': portfolio_id,
                'portfolio_name': portfolio.name,
                'user_id': user_id,
                'total_market_value': round(total_market_value, 2),
                'total_cost': round(total_cost, 2),
                'total_unrealized_pnl': round(total_unrealized_pnl, 2),
                'total_unrealized_pnl_percent': round(total_unrealized_pnl_percent, 2),
                'holdings_count': len(holdings_data),
                'holdings': holdings_data,
                'data_source': 'database_with_realtime_prices',
                'latency_ms': latency_ms
            }
            
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'holdings': [],
                'data_source': 'error'
            }
    
    def _get_current_price(self, asset_id: int) -> float:
        """Get current price for an asset"""
        try:
            # Try to get latest market data
            latest_data = self.db.query(MarketData).filter(
                MarketData.asset_id == asset_id
            ).order_by(MarketData.date.desc()).first()
            
            if latest_data:
                return float(latest_data.close)
            
            # If no market data, try real-time API
            asset = self.db.query(Asset).filter(Asset.id == asset_id).first()
            if asset:
                realtime_data = self.get_realtime_price(asset.code, asset.type)
                if realtime_data and 'current_price' in realtime_data:
                    return realtime_data['current_price']
            
            return 0.0
            
        except Exception:
            return 0.0
    
    # ========================================================================
    # Requirement 3: Historical Data (Previous Trading Day)
    # ========================================================================
    
    def get_previous_day_history(self, instrument_code: str, instrument_type: str = 'stock') -> Dict[str, Any]:
        """
        Get historical market data from the previous trading day
        
        Args:
            instrument_code: Instrument code
            instrument_type: Type of instrument
            
        Returns:
            Dictionary containing:
            - timestamp: Query timestamp
            - code: Instrument code
            - name: Instrument name
            - type: Instrument type
            - trading_date: Trading date
            - open: Opening price
            - high: Highest price
            - low: Lowest price
            - close: Closing price
            - volume: Trading volume
            - amount: Trading amount
            - change: Price change from previous day
            - change_percent: Price change percentage
            - data_source: Data source
            - latency_ms: Query latency
            
        Example:
            >>> service.get_previous_day_history('600036', 'stock')
            {
                'timestamp': '2026-03-07T10:30:00.123456',
                'code': '600036',
                'name': '招商银行',
                'trading_date': '2026-03-06',
                'open': 32.50,
                'high': 33.20,
                'low': 32.30,
                'close': 33.00,
                'volume': 50000000,
                'amount': 1650000000,
                'change': 0.50,
                'change_percent': 1.54,
                ...
            }
        """
        start_time = time.time()
        
        try:
            # Get asset from database
            asset = self.db.query(Asset).filter(Asset.code == instrument_code).first()
            
            if not asset:
                return {
                    'timestamp': datetime.now().isoformat(),
                    'error': 'Instrument not found',
                    'data_source': 'error'
                }
            
            # Calculate previous trading day
            today = datetime.now().date()
            previous_day = today - timedelta(days=1)
            
            # Skip weekends
            if previous_day.weekday() == 5:  # Saturday
                previous_day -= timedelta(days=1)
            elif previous_day.weekday() == 6:  # Sunday
                previous_day -= timedelta(days=2)
            
            # Get historical data from database
            historical_data = self.db.query(MarketData).filter(
                MarketData.asset_id == asset.id,
                MarketData.date == previous_day
            ).first()
            
            if historical_data:
                # Found in database
                latency_ms = int((time.time() - start_time) * 1000)
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'code': asset.code,
                    'name': asset.name,
                    'type': asset.type,
                    'trading_date': previous_day.isoformat(),
                    'open': float(historical_data.open),
                    'high': float(historical_data.high),
                    'low': float(historical_data.low),
                    'close': float(historical_data.close),
                    'volume': float(historical_data.volume),
                    'amount': float(historical_data.amount),
                    'change': 0.0,  # Would need previous day's close to calculate
                    'change_percent': 0.0,
                    'data_source': 'database',
                    'latency_ms': latency_ms
                }
            else:
                # Try to fetch from external API (if available)
                # For now, return not found
                latency_ms = int((time.time() - start_time) * 1000)
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'code': asset.code,
                    'name': asset.name,
                    'type': asset.type,
                    'trading_date': previous_day.isoformat(),
                    'error': 'Historical data not available',
                    'data_source': 'not_found',
                    'latency_ms': latency_ms
                }
                
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'data_source': 'error'
            }
    
    # ========================================================================
    # Requirement 4: On-demand Query System
    # ========================================================================
    
    def query_all_data(self, instrument_code: str, portfolio_id: Optional[int] = None, 
                      user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        On-demand query system - retrieves all data in a single call
        
        Args:
            instrument_code: Financial instrument code
            portfolio_id: Optional portfolio ID for holdings
            user_id: Optional user ID for authorization
            
        Returns:
            Comprehensive data package including:
            - realtime_price: Real-time price data
            - previous_day_history: Historical data from previous trading day
            - portfolio_holdings: Portfolio holdings (if portfolio_id provided)
            - query_timestamp: Overall query timestamp
            - total_latency_ms: Total query latency
            
        Example:
            >>> service.query_all_data('600036', portfolio_id=1, user_id=1)
            {
                'query_timestamp': '2026-03-07T10:30:00.123456',
                'instrument_code': '600036',
                'realtime_price': {...},
                'previous_day_history': {...},
                'portfolio_holdings': {...},
                'total_latency_ms': 250
            }
        """
        query_start = time.time()
        
        result = {
            'query_timestamp': datetime.now().isoformat(),
            'instrument_code': instrument_code,
            'data': {}
        }
        
        # 1. Get real-time price
        result['data']['realtime_price'] = self.get_realtime_price(instrument_code)
        
        # 2. Get previous day history
        result['data']['previous_day_history'] = self.get_previous_day_history(instrument_code)
        
        # 3. Get portfolio holdings (if requested)
        if portfolio_id and user_id:
            result['data']['portfolio_holdings'] = self.get_portfolio_holdings(portfolio_id, user_id)
        
        # Calculate total latency
        total_latency_ms = int((time.time() - query_start) * 1000)
        result['total_latency_ms'] = total_latency_ms
        result['status'] = 'success' if total_latency_ms < 5000 else 'warning'
        
        return result
    
    def clear_cache(self):
        """Clear query cache"""
        self._cache.clear()
    
    def set_cache_timeout(self, timeout_seconds: int):
        """Set cache timeout"""
        self._cache_timeout = timeout_seconds


# Convenience functions
def get_realtime_price(db: Session, code: str, instrument_type: str = 'stock') -> Dict[str, Any]:
    """Get real-time price (convenience function)"""
    service = FinancialDataQueryService(db)
    return service.get_realtime_price(code, instrument_type)


def get_portfolio_holdings(db: Session, portfolio_id: int, user_id: int) -> Dict[str, Any]:
    """Get portfolio holdings (convenience function)"""
    service = FinancialDataQueryService(db)
    return service.get_portfolio_holdings(portfolio_id, user_id)


def get_previous_day_history(db: Session, code: str, instrument_type: str = 'stock') -> Dict[str, Any]:
    """Get previous day history (convenience function)"""
    service = FinancialDataQueryService(db)
    return service.get_previous_day_history(code, instrument_type)
