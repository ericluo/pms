"""
应用启动和数据准备脚本
创建测试用户和投资组合
"""
import requests
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

print("="*80)
print("  PMS 应用启动和数据准备")
print("="*80)
print()

# 步骤 1: 创建测试用户
print("步骤 1: 创建测试用户账户")
print("-" * 80)

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
test_user = {
    "username": f"demo_user_{timestamp}",
    "email": f"demo_{timestamp}@example.com",
    "password": "Demo123456",
    "name": "演示用户"
}

print(f"用户信息:")
print(f"  - 用户名：{test_user['username']}")
print(f"  - 邮箱：{test_user['email']}")
print(f"  - 密码：Demo123456")
print(f"  - 姓名：{test_user['name']}")
print()

response = requests.post(f"{BASE_URL}/auth/register", json=test_user)

if response.status_code in [200, 201]:
    user_data = response.json()
    user_id = user_data.get('id')
    print(f"✅ 用户创建成功!")
    print(f"  - 用户 ID: {user_id}")
else:
    print(f"❌ 用户创建失败：{response.status_code}")
    print(f"错误信息：{response.text}")
    exit(1)

# 步骤 2: 用户登录获取 Token
print("\n步骤 2: 用户登录获取认证 Token")
print("-" * 80)

login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": test_user['email'],
    "password": "Demo123456"
})

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print(f"✅ 登录成功!")
    print(f"  - Token: {token[:50]}...")
else:
    print(f"❌ 登录失败：{login_response.status_code}")
    exit(1)

# 步骤 3: 创建投资组合
print("\n步骤 3: 创建测试投资组合")
print("-" * 80)

portfolio_data = {
    "name": "演示投资组合",
    "description": "这是一个用于演示的投资组合",
    "benchmark": "沪深 300",
    "risk_level": "中等"
}

print(f"投资组合信息:")
print(f"  - 名称：{portfolio_data['name']}")
print(f"  - 描述：{portfolio_data['description']}")
print(f"  - 业绩基准：{portfolio_data['benchmark']}")
print(f"  - 风险等级：{portfolio_data['risk_level']}")
print()

response = requests.post(f"{BASE_URL}/portfolios", json=portfolio_data, headers=headers)

if response.status_code in [200, 201]:
    portfolio = response.json()
    portfolio_id = portfolio['id']
    print(f"✅ 投资组合创建成功!")
    print(f"  - 投资组合 ID: {portfolio_id}")
    print(f"  - 名称：{portfolio['name']}")
    print(f"  - 创建时间：{portfolio.get('created_at', 'N/A')}")
else:
    print(f"❌ 投资组合创建失败：{response.status_code}")
    print(f"错误信息：{response.text}")
    exit(1)

# 步骤 4: 验证投资组合详情
print("\n步骤 4: 验证投资组合详情")
print("-" * 80)

response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)

if response.status_code == 200:
    detail = response.json()
    print(f"✅ 投资组合详情获取成功!")
    print(f"  - 组合名称：{detail['portfolio']['name']}")
    print(f"  - 业绩基准：{detail['portfolio'].get('benchmark', 'N/A')}")
    print(f"  - 风险等级：{detail['portfolio'].get('risk_level', 'N/A')}")
    print(f"  - 持仓数量：{len(detail.get('holdings', []))}")
else:
    print(f"❌ 获取投资组合详情失败：{response.status_code}")

# 步骤 5: 保存测试凭证
print("\n步骤 5: 保存测试凭证")
print("-" * 80)

test_credentials = {
    "server_status": {
        "frontend": "http://localhost:3000",
        "backend": "http://localhost:5000"
    },
    "user": {
        "id": user_id,
        "username": test_user['username'],
        "email": test_user['email'],
        "password": "Demo123456",
        "name": test_user['name']
    },
    "portfolio": {
        "id": portfolio_id,
        "name": portfolio_data['name'],
        "description": portfolio_data['description'],
        "benchmark": portfolio_data['benchmark'],
        "risk_level": portfolio_data['risk_level']
    },
    "token": token,
    "created_at": datetime.now().isoformat()
}

import json
with open('demo_credentials.json', 'w', encoding='utf-8') as f:
    json.dump(test_credentials, f, ensure_ascii=False, indent=2)

print(f"✅ 测试凭证已保存到：demo_credentials.json")

# 完成
print()
print("="*80)
print("  应用启动和数据准备完成!")
print("="*80)
print()
print("服务器信息:")
print(f"  - 前端地址：http://localhost:3000")
print(f"  - 后端地址：http://localhost:5000")
print(f"  - API 文档：http://localhost:5000/api/docs")
print()
print("登录信息:")
print(f"  - 邮箱：{test_user['email']}")
print(f"  - 密码：Demo123456")
print()
print("投资组合信息:")
print(f"  - 组合 ID: {portfolio_id}")
print(f"  - 组合名称：{portfolio_data['name']}")
print()
print("下一步操作:")
print(f"  1. 打开浏览器访问：http://localhost:3000")
print(f"  2. 使用以上邮箱和密码登录")
print(f"  3. 进入'投资组合'页面")
print(f"  4. 点击'{portfolio_data['name']}'查看详情")
print()
print("="*80)
