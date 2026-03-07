"""
市场查询服务使用示例
"""

# ============================================================================
# 示例 1: 基础查询 - 按名称搜索股票
# ============================================================================

from app.services.market_query import MarketQueryService
from app.utils.database import SessionLocal

# 创建数据库会话
db = SessionLocal()
service = MarketQueryService(db)

# 搜索名称包含"茅台"的股票
print("=" * 60)
print("示例 1: 搜索股票 - 茅台")
print("=" * 60)

results = service.search_by_name('茅台', asset_type='stock', limit=5)

for result in results:
    print(f"代码：{result['code']}")
    print(f"名称：{result['name']}")
    print(f"市场：{result['market']}")
    print(f"价格：¥{result.get('price', 'N/A')}")
    print(f"涨跌幅：{result.get('change_percent', 0):.2f}%")
    print("-" * 60)

# ============================================================================
# 示例 2: 按代码查询市场信息
# ============================================================================

print("\n" + "=" * 60)
print("示例 2: 按代码查询 - 600519")
print("=" * 60)

info = service.get_market_info_by_code('600519')

if info:
    print(f"股票名称：{info['name']}")
    print(f"当前价格：¥{info['price']}")
    print(f"开盘价：¥{info['open']}")
    print(f"最高价：¥{info['high']}")
    print(f"最低价：¥{info['low']}")
    print(f"昨收价：¥{info['close']}")
    print(f"涨跌额：¥{info['change']}")
    print(f"涨跌幅：{info['change_percent']:.2f}%")
    print(f"成交量：{info['volume']:,.0f}")
    print(f"成交额：¥{info['amount']:,.0f}")
    print(f"数据来源：{info['source']}")
else:
    print("未找到该股票")

# ============================================================================
# 示例 3: 搜索基金
# ============================================================================

print("\n" + "=" * 60)
print("示例 3: 搜索基金 - 沪深 300")
print("=" * 60)

fund_results = service.search_by_name('沪深 300', asset_type='fund', limit=5)

for fund in fund_results:
    print(f"代码：{fund['code']}")
    print(f"名称：{fund['name']}")
    print(f"类型：{fund['type_name']}")
    print(f"价格：¥{fund.get('price', 'N/A')}")
    print("-" * 60)

# ============================================================================
# 示例 4: 使用便捷函数
# ============================================================================

from app.services.market_query import search_stock_by_name, get_market_info

print("\n" + "=" * 60)
print("示例 4: 使用便捷函数")
print("=" * 60)

# 搜索股票
stocks = search_stock_by_name('平安银行', db, limit=3)
print(f"找到 {len(stocks)} 只股票:")
for stock in stocks:
    print(f"  - {stock['code']}: {stock['name']}")

# 获取市场信息
info = get_market_info('000001', db)
if info:
    print(f"\n平安银行当前价格：¥{info['price']}")

# ============================================================================
# 示例 5: 数据同步
# ============================================================================

print("\n" + "=" * 60)
print("示例 5: 同步市场数据")
print("=" * 60)

# 同步单个股票
success = service.sync_market_data('600519')
if success:
    print("✓ 贵州茅台数据同步成功")
else:
    print("✗ 贵州茅台数据同步失败")

# 批量同步（示例，实际使用请谨慎）
# success_count, fail_count = service.sync_all_assets()
# print(f"同步完成：成功{success_count}个，失败{fail_count}个")

# ============================================================================
# 示例 6: API 调用（需要启动服务器）
# ============================================================================

import requests

print("\n" + "=" * 60)
print("示例 6: RESTful API 调用")
print("=" * 60)

# 假设服务器运行在 http://localhost:5000
api_base = "http://localhost:5000/api/market_query"

try:
    # 搜索股票
    response = requests.get(f"{api_base}/search", params={"q": "茅台", "type": "stock"})
    if response.status_code == 200:
        data = response.json()
        print(f"API 搜索结果：找到 {data['total']} 条记录")
        if data['results']:
            first = data['results'][0]
            print(f"  第一条：{first['name']} ({first['code']})")
    
    # 获取市场信息
    response = requests.get(f"{api_base}/info/600519")
    if response.status_code == 200:
        data = response.json()
        print(f"\nAPI 获取行情：{data['name']} ¥{data['price']}")
        
except requests.exceptions.RequestException:
    print("API 调用失败，请确保服务器正在运行")

# ============================================================================
# 示例 7: 高级搜索技巧
# ============================================================================

print("\n" + "=" * 60)
print("示例 7: 高级搜索技巧")
print("=" * 60)

# 按代码搜索
results = service.search_by_name('600', asset_type='stock', limit=3)
print(f"代码包含'600'的股票：{len(results)} 个")

# 部分名称匹配
results = service.search_by_name('银行', asset_type='stock', limit=3)
print(f"名称包含'银行'的股票：{len(results)} 个")

# 不限制类型（搜索所有资产）
results = service.search_by_name('沪深', limit=5)
print(f"名称包含'沪深'的所有资产：{len(results)} 个")

# ============================================================================
# 清理资源
# ============================================================================

db.close()
print("\n" + "=" * 60)
print("示例执行完成")
print("=" * 60)
