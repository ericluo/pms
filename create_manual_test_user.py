"""
创建前端手动测试专用用户
"""
import requests
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

print("="*80)
print("  PMS 前端手动测试 - 测试用户创建")
print("="*80)
print()

# 创建测试用户
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
test_user = {
    "username": f"manual_test_{timestamp}",
    "email": f"manual_test_{timestamp}@example.com",
    "password": "Test123456",
    "name": "手动测试用户"
}

print("创建测试用户...")
print(f"  用户名：{test_user['username']}")
print(f"  邮箱：{test_user['email']}")
print(f"  密码：Test123456")
print()

response = requests.post(f"{BASE_URL}/auth/register", json=test_user)

if response.status_code in [200, 201]:
    user_data = response.json()
    print("✅ 用户创建成功!")
    print()
    print("="*80)
    print("  登录凭证")
    print("="*80)
    print(f"  邮箱：{test_user['email']}")
    print(f"  密码：Test123456")
    print(f"  用户 ID: {user_data.get('id', 'N/A')}")
    print("="*80)
    print()
    print("请按以下步骤开始测试:")
    print()
    print("1. 打开浏览器访问：http://localhost:3000")
    print(f"2. 使用以上邮箱和密码登录")
    print("3. 按照 MANUAL_TEST_PLAN.md 中的步骤执行测试")
    print("4. 记录所有测试结果")
    print()
else:
    print(f"❌ 用户创建失败：{response.status_code}")
    print(f"错误信息：{response.text}")
