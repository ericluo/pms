"""
PMS 问题修复验证测试脚本
验证两个关键问题的修复:
1. 投资组合详情页数据加载问题
2. 持仓添加功能异常问题
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def print_test_result(test_name, passed, details=""):
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {test_name}")
    if details:
        print(f"  详情：{details}")
    return passed

# 测试开始
print_section("PMS 问题修复验证测试")
print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 步骤 1: 创建测试用户并登录
print_section("步骤 1: 创建测试用户并登录")

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
test_user = {
    "username": f"test_verify_{timestamp}",
    "email": f"test_verify_{timestamp}@example.com",
    "password": "Test123456",
    "name": "测试用户"
}

print("创建测试用户...")
response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
test_passed_1 = response.status_code in [200, 201]
print_test_result("用户注册", test_passed_1, f"状态码：{response.status_code}")

if not test_passed_1:
    print(f"错误：{response.text}")
    exit(1)

user_data = response.json()
print(f"用户 ID: {user_data.get('id', 'N/A')}")

# 登录
print("\n用户登录...")
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": test_user['email'],
    "password": "Test123456"
})
test_passed_2 = login_response.status_code == 200
print_test_result("用户登录", test_passed_2)

if not test_passed_2:
    print(f"错误：{login_response.text}")
    exit(1)

token = login_response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
print(f"Token: {token[:50]}...")

# 步骤 2: 创建测试投资组合
print_section("步骤 2: 创建测试投资组合")

portfolio_data = {
    "name": "验证测试组合",
    "description": "用于验证问题修复的投资组合",
    "benchmark": "沪深 300",
    "risk_level": "中等"
}

print("创建投资组合...")
response = requests.post(f"{BASE_URL}/portfolios", json=portfolio_data, headers=headers)
test_passed_3 = response.status_code in [200, 201]
print_test_result("投资组合创建", test_passed_3)

if not test_passed_3:
    print(f"错误：{response.text}")
    exit(1)

portfolio = response.json()
portfolio_id = portfolio['id']
print(f"投资组合 ID: {portfolio_id}")
print(f"投资组合名称：{portfolio['name']}")

# 步骤 3: 验证问题 1 - 获取投资组合详情
print_section("步骤 3: 验证问题 1 - 投资组合详情页数据加载")

print(f"获取投资组合 {portfolio_id} 的详情...")
response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)
test_passed_4 = response.status_code == 200
print_test_result("API 调用成功", test_passed_4)

if test_passed_4:
    data = response.json()
    
    # 验证响应格式
    has_portfolio = 'portfolio' in data
    print_test_result("响应包含 portfolio 字段", has_portfolio)
    
    has_holdings = 'holdings' in data
    print_test_result("响应包含 holdings 字段", has_holdings)
    
    # 验证投资组合数据
    if has_portfolio:
        portfolio_info = data['portfolio']
        print(f"\n投资组合详细信息:")
        print(f"  - ID: {portfolio_info.get('id', 'N/A')}")
        print(f"  - 名称：{portfolio_info.get('name', 'N/A')}")
        print(f"  - 描述：{portfolio_info.get('description', 'N/A')}")
        print(f"  - 业绩基准：{portfolio_info.get('benchmark', 'N/A')}")
        print(f"  - 风险等级：{portfolio_info.get('risk_level', 'N/A')}")
        print(f"  - 创建时间：{portfolio_info.get('created_at', 'N/A')}")
        print(f"  - 更新时间：{portfolio_info.get('updated_at', 'N/A')}")
        
        # 验证关键字段
        test_passed_5 = (
            portfolio_info.get('name') == portfolio_data['name'] and
            portfolio_info.get('benchmark') == portfolio_data['benchmark'] and
            portfolio_info.get('risk_level') == portfolio_data['risk_level']
        )
        print_test_result("投资组合数据完整性", test_passed_5)
    
    # 验证持仓数据
    if has_holdings:
        holdings = data['holdings']
        print(f"\n持仓列表:")
        print(f"  - 持仓数量：{len(holdings)}")
        print_test_result("持仓列表为空 (预期行为)", len(holdings) == 0)

# 步骤 4: 创建测试资产
print_section("步骤 4: 创建测试资产")

from app.utils.database import get_db
from app.models.asset import Asset

db = next(get_db())

# 查询或创建招商银行资产
cmb_asset = db.query(Asset).filter(Asset.code == "600036").first()
if not cmb_asset:
    cmb_asset = Asset(code="600036", name="招商银行", type="stock", market="上海证券交易所", industry="银行")
    db.add(cmb_asset)
    db.commit()
    db.refresh(cmb_asset)
    print(f"创建招商银行资产，ID: {cmb_asset.id}")
else:
    print(f"使用已存在的招商银行资产，ID: {cmb_asset.id}")

# 查询或创建民生银行资产
cmc_asset = db.query(Asset).filter(Asset.code == "600016").first()
if not cmc_asset:
    cmc_asset = Asset(code="600016", name="民生银行", type="stock", market="上海证券交易所", industry="银行")
    db.add(cmc_asset)
    db.commit()
    db.refresh(cmc_asset)
    print(f"创建民生银行资产，ID: {cmc_asset.id}")
else:
    print(f"使用已存在的民生银行资产，ID: {cmc_asset.id}")

db.close()

# 步骤 5: 验证问题 2 - 添加持仓并验证刷新
print_section("步骤 5: 验证问题 2 - 持仓添加功能")

# 添加第一笔持仓 - 招商银行
print("添加第一笔持仓 (招商银行)...")
holding1_data = {
    "asset_id": cmb_asset.id,
    "quantity": 100,
    "cost_price": 30.0
}

response = requests.post(
    f"{BASE_URL}/portfolios/{portfolio_id}/holdings?portfolio_id={portfolio_id}",
    json=holding1_data,
    headers=headers
)
test_passed_6 = response.status_code in [200, 201]
print_test_result("持仓添加 API 调用", test_passed_6)

if test_passed_6:
    holding1 = response.json()
    print(f"持仓 ID: {holding1.get('id', 'N/A')}")
    print(f"资产 ID: {holding1.get('asset_id', 'N/A')}")
    print(f"数量：{holding1.get('quantity', 'N/A')}")
    print(f"成本价：{holding1.get('cost_price', 'N/A')}")

# 添加第二笔持仓 - 民生银行
print("\n添加第二笔持仓 (民生银行)...")
holding2_data = {
    "asset_id": cmc_asset.id,
    "quantity": 100,
    "cost_price": 10.0
}

response = requests.post(
    f"{BASE_URL}/portfolios/{portfolio_id}/holdings?portfolio_id={portfolio_id}",
    json=holding2_data,
    headers=headers
)
test_passed_7 = response.status_code in [200, 201]
print_test_result("持仓添加 API 调用", test_passed_7)

if test_passed_7:
    holding2 = response.json()
    print(f"持仓 ID: {holding2.get('id', 'N/A')}")
    print(f"资产 ID: {holding2.get('asset_id', 'N/A')}")
    print(f"数量：{holding2.get('quantity', 'N/A')}")
    print(f"成本价：{holding2.get('cost_price', 'N/A')}")

# 验证持仓刷新 - 重新获取投资组合详情
print(f"\n验证持仓刷新 - 重新获取投资组合 {portfolio_id} 的详情...")
response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)
test_passed_8 = response.status_code == 200
print_test_result("重新获取详情 API 调用", test_passed_8)

if test_passed_8:
    data = response.json()
    holdings = data.get('holdings', [])
    
    print(f"\n持仓列表验证:")
    print(f"  - 持仓数量：{len(holdings)}")
    
    test_passed_9 = len(holdings) == 2
    print_test_result("持仓数量为 2 (预期值)", test_passed_9)
    
    if len(holdings) == 2:
        # 验证持仓数据
        print(f"\n持仓明细:")
        for i, holding in enumerate(holdings, 1):
            print(f"\n持仓 {i}:")
            print(f"  - 资产 ID: {holding.get('asset_id', 'N/A')}")
            print(f"  - 资产名称：{holding.get('asset', {}).get('name', 'N/A')}")
            print(f"  - 资产代码：{holding.get('asset', {}).get('code', 'N/A')}")
            print(f"  - 数量：{holding.get('quantity', 'N/A')}")
            print(f"  - 成本价：{holding.get('cost_price', 'N/A')}")
            print(f"  - 当前价：{holding.get('current_price', 'N/A')}")
            print(f"  - 市值：{holding.get('value', 'N/A')}")
        
        # 验证持仓数据正确性
        holding1_correct = (
            holdings[0]['asset_id'] == cmb_asset.id and
            holdings[0]['quantity'] == 100 and
            holdings[0]['cost_price'] == 30.0
        )
        holding2_correct = (
            holdings[1]['asset_id'] == cmc_asset.id and
            holdings[1]['quantity'] == 100 and
            holdings[1]['cost_price'] == 10.0
        )
        
        test_passed_10 = holding1_correct and holding2_correct
        print_test_result("持仓数据准确性", test_passed_10)

# 步骤 6: 总体测试结果
print_section("测试结果汇总")

all_tests = [
    ("用户注册", test_passed_1),
    ("用户登录", test_passed_2),
    ("投资组合创建", test_passed_3),
    ("API 调用成功", test_passed_4),
    ("响应包含 portfolio 字段", has_portfolio if 'has_portfolio' in locals() else False),
    ("响应包含 holdings 字段", has_holdings if 'has_holdings' in locals() else False),
    ("投资组合数据完整性", test_passed_5 if 'test_passed_5' in locals() else False),
    ("持仓添加 API 调用 1", test_passed_6),
    ("持仓添加 API 调用 2", test_passed_7),
    ("重新获取详情 API 调用", test_passed_8),
    ("持仓数量为 2", test_passed_9 if 'test_passed_9' in locals() else False),
    ("持仓数据准确性", test_passed_10 if 'test_passed_10' in locals() else False),
]

passed_count = sum(1 for _, passed in all_tests if passed)
total_count = len(all_tests)

print(f"\n总测试数：{total_count}")
print(f"通过数：{passed_count}")
print(f"失败数：{total_count - passed_count}")
print(f"通过率：{(passed_count/total_count)*100:.1f}%\n")

print("详细测试结果:")
for test_name, passed in all_tests:
    print_test_result(test_name, passed)

# 最终结论
print_section("最终结论")

problem1_fixed = all([
    test_passed_4,
    has_portfolio if 'has_portfolio' in locals() else False,
    has_holdings if 'has_holdings' in locals() else False,
    test_passed_5 if 'test_passed_5' in locals() else False
])

problem2_fixed = all([
    test_passed_6,
    test_passed_7,
    test_passed_8,
    test_passed_9 if 'test_passed_9' in locals() else False,
    test_passed_10 if 'test_passed_10' in locals() else False
])

if problem1_fixed:
    print("[PASS] 问题 1 (投资组合详情页数据加载) 已解决")
    print("   - API 正常返回投资组合详情")
    print("   - 响应格式正确 (包含 portfolio 和 holdings 字段)")
    print("   - 数据完整准确")
else:
    print("[FAIL] 问题 1 (投资组合详情页数据加载) 未解决")

if problem2_fixed:
    print("\n[PASS] 问题 2 (持仓添加功能) 已解决")
    print("   - 持仓添加 API 调用成功")
    print("   - 重新获取详情时持仓列表已刷新")
    print("   - 持仓数据准确无误")
else:
    print("\n[FAIL] 问题 2 (持仓添加功能) 未解决")

print(f"\n{'='*80}")
if problem1_fixed and problem2_fixed:
    print("  [SUCCESS] 所有问题均已解决！")
else:
    print("  [WARNING] 仍有问题未解决，请检查上述测试结果")
print(f"{'='*80}\n")

# 清理测试数据
print("清理测试数据...")
try:
    # 删除投资组合 (会自动删除关联的持仓)
    requests.delete(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)
    print("✅ 测试数据已清理")
except Exception as e:
    print(f"⚠️  清理测试数据失败：{e}")

print(f"\n测试完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
