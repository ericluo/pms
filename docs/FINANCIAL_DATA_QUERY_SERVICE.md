# Financial Data Query Service - Complete Documentation

## Overview

The Financial Data Query Service provides comprehensive market data queries with strict latency requirements and on-demand update mechanisms.

## Requirements Implementation

### ✅ Requirement 1: Real-time Price Data
- **Latency**: < 1 second (target: < 500ms)
- **Data fields**: Bid price, Ask price, Last traded price
- **Update mechanism**: On-demand query

### ✅ Requirement 2: Portfolio Holdings
- **Data fields**: Ticker, Quantity, Purchase price, Current market value, Unrealized gain/loss
- **Coverage**: All stocks in user's portfolio
- **Authorization**: User-based access control

### ✅ Requirement 3: Historical Data (Previous Trading Day)
- **Data fields**: Open, High, Low, Close, Volume
- **Time range**: Previous trading day only
- **Weekend handling**: Automatic skip of non-trading days

### ✅ Requirement 4: On-demand Query System
- **Update mechanism**: Query-on-demand (no automatic updates)
- **Processing**: Immediate query execution
- **Data freshness**: Most current available data

## Usage Examples

### Example 1: Get Real-time Price

```python
from app.utils.database import SessionLocal
from app.services.financial_data_query import FinancialDataQueryService

# Initialize service
db = SessionLocal()
service = FinancialDataQueryService(db)

# Get real-time price for stock
result = service.get_realtime_price('600036', 'stock')

# Response structure
print(f"Timestamp: {result['timestamp']}")
print(f"Code: {result['code']}")
print(f"Bid Price: ¥{result['bid_price']}")
print(f"Ask Price: ¥{result['ask_price']}")
print(f"Last Price: ¥{result['last_price']}")
print(f"Latency: {result['latency_ms']}ms")

db.close()
```

**Expected Output:**
```
Timestamp: 2026-03-07T10:30:00.123456
Code: 600036
Bid Price: ¥33.00
Ask Price: ¥33.02
Last Price: ¥33.01
Latency: 250ms
```

---

### Example 2: Get Portfolio Holdings

```python
from app.utils.database import SessionLocal
from app.services.financial_data_query import FinancialDataQueryService

db = SessionLocal()
service = FinancialDataQueryService(db)

# Get portfolio holdings
result = service.get_portfolio_holdings(portfolio_id=1, user_id=1)

# Display portfolio summary
print(f"Portfolio: {result['portfolio_name']}")
print(f"Total Market Value: ¥{result['total_market_value']:,.2f}")
print(f"Total Cost: ¥{result['total_cost']:,.2f}")
print(f"Unrealized P&L: ¥{result['total_unrealized_pnl']:,.2f} ({result['total_unrealized_pnl_percent']:.2f}%)")
print(f"Holdings Count: {result['holdings_count']}")
print()

# Display individual holdings
for holding in result['holdings']:
    print(f"Ticker: {holding['ticker']} - {holding['name']}")
    print(f"  Quantity: {holding['quantity']}")
    print(f"  Purchase Price: ¥{holding['purchase_price']:.2f}")
    print(f"  Current Price: ¥{holding['current_price']:.2f}")
    print(f"  Market Value: ¥{holding['market_value']:,.2f}")
    print(f"  Unrealized P&L: ¥{holding['unrealized_pnl']:,.2f} ({holding['unrealized_pnl_percent']:.2f}%)")
    print()

db.close()
```

**Expected Output:**
```
Portfolio: My Portfolio
Total Market Value: ¥33,000.00
Total Cost: ¥30,000.00
Unrealized P&L: ¥3,000.00 (10.00%)
Holdings Count: 1

Ticker: 600036 - 招商银行
  Quantity: 1000
  Purchase Price: ¥30.00
  Current Price: ¥33.00
  Market Value: ¥33,000.00
  Unrealized P&L: ¥3,000.00 (10.00%)
```

---

### Example 3: Get Previous Day History

```python
from app.utils.database import SessionLocal
from app.services.financial_data_query import FinancialDataQueryService

db = SessionLocal()
service = FinancialDataQueryService(db)

# Get previous trading day's data
result = service.get_previous_day_history('600036', 'stock')

if 'error' not in result:
    print(f"Trading Date: {result['trading_date']}")
    print(f"Open: ¥{result['open']:.2f}")
    print(f"High: ¥{result['high']:.2f}")
    print(f"Low: ¥{result['low']:.2f}")
    print(f"Close: ¥{result['close']:.2f}")
    print(f"Volume: {result['volume']:,.0f}")
    print(f"Amount: ¥{result['amount']:,.2f}")
else:
    print(f"Error: {result.get('error', 'Data not available')}")

db.close()
```

**Expected Output:**
```
Trading Date: 2026-03-06
Open: ¥32.50
High: ¥33.20
Low: ¥32.30
Close: ¥33.00
Volume: 50,000,000
Amount: ¥1,650,000,000.00
```

---

### Example 4: Comprehensive On-demand Query

```python
from app.utils.database import SessionLocal
from app.services.financial_data_query import FinancialDataQueryService

db = SessionLocal()
service = FinancialDataQueryService(db)

# Get all data in one query
result = service.query_all_data(
    instrument_code='600036',
    portfolio_id=1,
    user_id=1
)

print(f"Query Timestamp: {result['query_timestamp']}")
print(f"Total Latency: {result['total_latency_ms']}ms")
print(f"Status: {result['status']}")
print()

# Display real-time price
price_data = result['data']['realtime_price']
print("=== Real-time Price ===")
print(f"Current Price: ¥{price_data.get('current_price', 'N/A')}")
print(f"Bid/Ask: ¥{price_data.get('bid_price', 'N/A')} / ¥{price_data.get('ask_price', 'N/A')}")
print()

# Display previous day history
history_data = result['data']['previous_day_history']
if 'error' not in history_data:
    print("=== Previous Trading Day ===")
    print(f"Date: {history_data['trading_date']}")
    print(f"O/H/L/C: ¥{history_data['open']:.2f} / ¥{history_data['high']:.2f} / ¥{history_data['low']:.2f} / ¥{history_data['close']:.2f}")
    print()

# Display portfolio holdings
holdings_data = result['data']['portfolio_holdings']
if 'error' not in holdings_data:
    print("=== Portfolio Holdings ===")
    print(f"Total Value: ¥{holdings_data['total_market_value']:,.2f}")
    print(f"Unrealized P&L: ¥{holdings_data['total_unrealized_pnl']:,.2f} ({holdings_data['total_unrealized_pnl_percent']:.2f}%)")
    print(f"Number of Holdings: {holdings_data['holdings_count']}")

db.close()
```

---

### Example 5: Using Convenience Functions

```python
from app.utils.database import SessionLocal
from app.services.financial_data_query import (
    get_realtime_price,
    get_portfolio_holdings,
    get_previous_day_history
)

db = SessionLocal()

# Quick real-time price query
price = get_realtime_price(db, '600036', 'stock')
print(f"Current Price: ¥{price['current_price']}")

# Quick portfolio query
holdings = get_portfolio_holdings(db, portfolio_id=1, user_id=1)
print(f"Total Holdings: {len(holdings['holdings'])}")

# Quick historical query
history = get_previous_day_history(db, '600036', 'stock')
if 'error' not in history:
    print(f"Yesterday's Close: ¥{history['close']}")

db.close()
```

---

## API Reference

### FinancialDataQueryService Class

#### `get_realtime_price(instrument_code, instrument_type='stock')`

Get real-time price data for a financial instrument.

**Parameters:**
- `instrument_code` (str): Instrument code (e.g., '600036')
- `instrument_type` (str): Type ('stock', 'option', 'fund', etc.)

**Returns:** Dict with real-time price data

**Response Fields:**
- `timestamp` (str): Data retrieval timestamp
- `code` (str): Instrument code
- `name` (str): Instrument name
- `type` (str): Instrument type
- `bid_price` (float): Current bid price
- `ask_price` (float): Current ask price
- `last_price` (float): Last traded price
- `current_price` (float): Current market price
- `open` (float): Opening price
- `high` (float): Highest price
- `low` (float): Lowest price
- `close` (float): Previous close price
- `change` (float): Price change
- `change_percent` (float): Price change percentage
- `volume` (float): Trading volume
- `amount` (float): Trading amount
- `data_source` (str): Data source name
- `latency_ms` (int): Data latency in milliseconds

**Latency Requirement:** < 1000ms (target: < 500ms)

---

#### `get_portfolio_holdings(portfolio_id, user_id)`

Get current holdings information for user's portfolio.

**Parameters:**
- `portfolio_id` (int): Portfolio ID
- `user_id` (int): User ID (for authorization)

**Returns:** Dict with portfolio holdings data

**Response Fields:**
- `timestamp` (str): Query timestamp
- `portfolio_id` (int): Portfolio ID
- `portfolio_name` (str): Portfolio name
- `user_id` (int): User ID
- `total_market_value` (float): Total market value
- `total_cost` (float): Total cost basis
- `total_unrealized_pnl` (float): Total unrealized profit/loss
- `total_unrealized_pnl_percent` (float): Total P&L percentage
- `holdings_count` (int): Number of holdings
- `holdings` (list): List of holdings
- `data_source` (str): Data source
- `latency_ms` (int): Query latency

**Holding Fields:**
- `ticker` (str): Stock ticker symbol
- `name` (str): Stock name
- `type` (str): Asset type
- `quantity` (float): Quantity held
- `purchase_price` (float): Purchase price
- `current_price` (float): Current market price
- `market_value` (float): Market value
- `cost_basis` (float): Cost basis
- `unrealized_pnl` (float): Unrealized profit/loss
- `unrealized_pnl_percent` (float): P&L percentage
- `holding_id` (int): Holding ID
- `asset_id` (int): Asset ID

**Authorization:** Users can only access their own portfolios

---

#### `get_previous_day_history(instrument_code, instrument_type='stock')`

Get historical market data from the previous trading day.

**Parameters:**
- `instrument_code` (str): Instrument code
- `instrument_type` (str): Type of instrument

**Returns:** Dict with historical data

**Response Fields:**
- `timestamp` (str): Query timestamp
- `code` (str): Instrument code
- `name` (str): Instrument name
- `type` (str): Instrument type
- `trading_date` (str): Trading date (ISO format)
- `open` (float): Opening price
- `high` (float): Highest price
- `low` (float): Lowest price
- `close` (float): Closing price
- `volume` (float): Trading volume
- `amount` (float): Trading amount
- `change` (float): Price change
- `change_percent` (float): Price change percentage
- `data_source` (str): Data source
- `latency_ms` (int): Query latency

**Weekend Handling:** Automatically skips weekends and holidays

---

#### `query_all_data(instrument_code, portfolio_id=None, user_id=None)`

On-demand query system - retrieves all data in a single call.

**Parameters:**
- `instrument_code` (str): Financial instrument code
- `portfolio_id` (int, optional): Portfolio ID for holdings
- `user_id` (int, optional): User ID for authorization

**Returns:** Dict with comprehensive data package

**Response Fields:**
- `query_timestamp` (str): Overall query timestamp
- `instrument_code` (str): Instrument code
- `data` (dict): Contains all data types
  - `realtime_price` (dict): Real-time price data
  - `previous_day_history` (dict): Historical data
  - `portfolio_holdings` (dict): Portfolio holdings (if requested)
- `total_latency_ms` (int): Total query latency
- `status` (str): Query status ('success' or 'warning')

---

### Cache Management

#### `clear_cache()`

Clear query cache.

```python
service.clear_cache()
```

#### `set_cache_timeout(timeout_seconds)`

Set cache timeout.

```python
service.set_cache_timeout(5)  # 5 seconds cache
```

---

## Error Handling

### Real-time Data Unavailable

```python
result = service.get_realtime_price('INVALID_CODE', 'stock')

if 'error' in result:
    print(f"Error: {result['error']}")
    print(f"Timestamp: {result['timestamp']}")
    # Handle error gracefully
```

### Portfolio Not Found

```python
result = service.get_portfolio_holdings(999, 1)

if 'error' in result:
    print("Portfolio not found or access denied")
```

### Historical Data Not Available

```python
result = service.get_previous_day_history('600036', 'stock')

if 'error' in result:
    print(f"Historical data not available: {result.get('error')}")
```

---

## Performance Characteristics

### Latency Targets

| Operation | Target | Typical | Maximum |
|-----------|--------|---------|---------|
| Real-time Price Query | < 500ms | 200ms | 1000ms |
| Portfolio Holdings | < 1000ms | 500ms | 2000ms |
| Previous Day History | < 200ms | 100ms | 500ms |
| Comprehensive Query | < 2000ms | 1000ms | 5000ms |

### Caching

- **Default timeout**: 1 second
- **Cache key**: Instrument code + query type
- **Cache invalidation**: Manual or timeout-based

---

## Best Practices

### 1. Error Handling

```python
try:
    result = service.get_realtime_price('600036', 'stock')
    if 'error' in result:
        print(f"Data unavailable: {result['error']}")
    else:
        print(f"Current price: ¥{result['current_price']}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 2. Batch Queries

Use `query_all_data()` for better performance when you need multiple data types:

```python
# Good: Single comprehensive query
result = service.query_all_data('600036', portfolio_id=1, user_id=1)

# Less efficient: Multiple separate queries
price = service.get_realtime_price('600036')
history = service.get_previous_day_history('600036')
holdings = service.get_portfolio_holdings(1, 1)
```

### 3. Authorization

Always verify user ownership of portfolios:

```python
# Service automatically checks authorization
result = service.get_portfolio_holdings(portfolio_id, user_id)

if 'error' in result:
    # Either portfolio doesn't exist or user doesn't own it
    print("Access denied or portfolio not found")
```

### 4. Latency Monitoring

```python
result = service.get_realtime_price('600036', 'stock')

if result['latency_ms'] > 1000:
    print(f"Warning: High latency {result['latency_ms']}ms")
```

---

## Testing

Run tests:

```bash
python -m pytest tests/test_financial_data_query.py -v
```

Example test:

```python
def test_get_realtime_price(db_session, test_asset):
    service = FinancialDataQueryService(db_session)
    result = service.get_realtime_price(test_asset.code, 'stock')
    
    assert 'timestamp' in result
    assert 'current_price' in result
    assert result['latency_ms'] < 5000
```

---

## Migration Guide

### From MarketQueryService

If you're migrating from the older `MarketQueryService`:

```python
# Old way
from app.services.market_query import MarketQueryService
service = MarketQueryService(db)
info = service.get_market_info_by_code('600036')

# New way (recommended)
from app.services.financial_data_query import FinancialDataQueryService
service = FinancialDataQueryService(db)
result = service.get_realtime_price('600036', 'stock')
```

**Benefits:**
- ✅ Stricter latency requirements
- ✅ Better error handling
- ✅ More comprehensive data fields
- ✅ Built-in portfolio integration
- ✅ On-demand query optimization

---

## Support

For issues or questions:
1. Check this documentation
2. Review test examples in `tests/test_financial_data_query.py`
3. Check error messages in response dictionaries
4. Monitor latency metrics

---

**Version**: 1.0.0  
**Last Updated**: 2026-03-07  
**Status**: Production Ready ✅
