"""
测试准备脚本 - 创建测试数据
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

# 步骤 1: 创建测试用户
print_section("步骤 1: 创建测试用户账户")

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
test_user = {
    "username": f"testuser_{timestamp}",
    "email": f"test_{timestamp}@example.com",
    "password": "Test123456",
    "name": "测试用户"
}

print(f"创建用户:")
print(f"  - 用户名：{test_user['username']}")
print(f"  - 邮箱：{test_user['email']}")
print(f"  - 姓名：{test_user['name']}")

# 注册用户
response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
if response.status_code in [200, 201]:
    user_data = response.json()
    print(f"✓ 用户注册成功")
    print(f"  - 用户 ID: {user_data.get('id', 'N/A')}")
else:
    print(f"✗ 用户注册失败：{response.text}")
    exit(1)

# 登录获取 token
print(f"\n用户登录...")
login_data = {
    "email": test_user['email'],
    "password": "Test123456"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code == 200:
    auth_data = response.json()
    token = auth_data['access_token']
    print(f"✓ 登录成功")
    print(f"  - Token: {token[:50]}...")
else:
    print(f"✗ 登录失败：{response.text}")
    exit(1)

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# 步骤 2: 创建投资组合
print_section("步骤 2: 创建投资组合")

portfolio_name = "测试投资组合"
portfolio_data = {
    "name": portfolio_name,
    "description": "手动测试用投资组合",
    "benchmark": "沪深 300",
    "risk_level": "中等"
}

print(f"创建投资组合:")
print(f"  - 名称：{portfolio_name}")
print(f"  - 描述：{portfolio_data['description']}")

response = requests.post(f"{BASE_URL}/portfolios", json=portfolio_data, headers=headers)
if response.status_code in [200, 201]:
    portfolio = response.json()
    portfolio_id = portfolio['id']
    print(f"✓ 投资组合创建成功")
    print(f"  - 投资组合 ID: {portfolio_id}")
    print(f"  - 名称：{portfolio['name']}")
    print(f"  - 创建时间：{portfolio.get('created_at', 'N/A')}")
else:
    print(f"✗ 投资组合创建失败：{response.text}")
    exit(1)

# 步骤 3: 创建资产
print_section("步骤 3: 创建资产记录")

# 创建招商银行资产
print("创建招商银行资产...")
cmb_asset = {
    "code": "600036",
    "name": "招商银行",
    "type": "stock",
    "market": "上海证券交易所",
    "industry": "银行"
}
response = requests.post(f"{BASE_URL}/assets", json=cmb_asset, headers=headers)
if response.status_code in [200, 201]:
    cmb_data = response.json()
    cmb_id = cmb_data['id']
    print(f"✓ 招商银行创建成功")
    print(f"  - 资产 ID: {cmb_id}")
    print(f"  - 代码：600036")
else:
    # 如果已存在，查询获取
    response = requests.get(f"{BASE_URL}/assets?code=600036", headers=headers)
    if response.status_code == 200:
        assets = response.json()
        if assets:
            cmb_id = assets[0]['id']
            print(f"[INFO] 使用已存在的招商银行资产，ID: {cmb_id}")
        else:
            print(f"✗ 无法获取招商银行资产：{response.text}")
            exit(1)
    else:
        print(f"✗ 创建/查询招商银行失败：{response.text}")
        exit(1)

# 创建民生银行资产
print("\n创建民生银行资产...")
cmc_asset = {
    "code": "600016",
    "name": "民生银行",
    "type": "stock",
    "market": "上海证券交易所",
    "industry": "银行"
}
response = requests.post(f"{BASE_URL}/assets", json=cmc_asset, headers=headers)
if response.status_code in [200, 201]:
    cmc_data = response.json()
    cmc_id = cmc_data['id']
    print(f"✓ 民生银行创建成功")
    print(f"  - 资产 ID: {cmc_id}")
    print(f"  - 代码：600016")
else:
    # 如果已存在，查询获取
    response = requests.get(f"{BASE_URL}/assets?code=600016", headers=headers)
    if response.status_code == 200:
        assets = response.json()
        if assets:
            cmc_id = assets[0]['id']
            print(f"[INFO] 使用已存在的民生银行资产，ID: {cmc_id}")
        else:
            print(f"✗ 无法获取民生银行资产：{response.text}")
            exit(1)
    else:
        print(f"✗ 创建/查询民生银行失败：{response.text}")
        exit(1)

# 步骤 4: 添加持仓
print_section("步骤 4: 添加持仓记录")

# 添加招商银行持仓
print("添加招商银行持仓...")
cmb_holding = {
    "asset_id": cmb_id,
    "quantity": 100,
    "cost_price": 30.0
}
response = requests.post(f"{BASE_URL}/portfolios/{portfolio_id}/holdings?portfolio_id={portfolio_id}", 
                         json=cmb_holding, headers=headers)
if response.status_code in [200, 201]:
    holding_data = response.json()
    print(f"✓ 招商银行持仓添加成功")
    print(f"  - 持仓 ID: {holding_data['id']}")
    print(f"  - 数量：100 股")
    print(f"  - 成本价：30.00 元")
else:
    print(f"✗ 招商银行持仓添加失败：{response.text}")

# 添加民生银行持仓
print("\n添加民生银行持仓...")
cmc_holding = {
    "asset_id": cmc_id,
    "quantity": 100,
    "cost_price": 10.0
}
response = requests.post(f"{BASE_URL}/portfolios/{portfolio_id}/holdings?portfolio_id={portfolio_id}", 
                         json=cmc_holding, headers=headers)
if response.status_code in [200, 201]:
    holding_data = response.json()
    print(f"✓ 民生银行持仓添加成功")
    print(f"  - 持仓 ID: {holding_data['id']}")
    print(f"  - 数量：100 股")
    print(f"  - 成本价：10.00 元")
else:
    print(f"✗ 民生银行持仓添加失败：{response.text}")

# 步骤 5: 显示测试信息
print_section("测试准备完成")

print(f"服务器地址：http://localhost:5000")
print(f"\n测试账户信息:")
print(f"  - 用户名：{test_user['username']}")
print(f"  - 邮箱：{test_user['email']}")
print(f"  - 密码：Test123456")
print(f"\n投资组合信息:")
print(f"  - 投资组合 ID: {portfolio_id}")
print(f"  - 名称：{portfolio_name}")
print(f"\n持仓信息:")
print(f"  - 招商银行 (600036): 100 股 @ 30.00 元")
print(f"  - 民生银行 (600016): 100 股 @ 10.00 元")
print(f"\nToken: {token}")
print(f"\n{'='*80}")
print(f"服务器正在运行，可以进行手动测试")
print(f"{'='*80}\n")

# 保存测试信息到文件
test_info = {
    "server_url": "http://localhost:5000",
    "username": test_user['username'],
    "email": test_user['email'],
    "password": "Test123456",
    "token": token,
    "portfolio_id": portfolio_id,
    "portfolio_name": portfolio_name,
    "assets": [
        {"name": "招商银行", "code": "600036", "id": cmb_id},
        {"name": "民生银行", "code": "600016", "id": cmc_id}
    ]
}

with open('test_credentials.json', 'w', encoding='utf-8') as f:
    json.dump(test_info, f, ensure_ascii=False, indent=2)

print(f"测试信息已保存到：test_credentials.json")
