"""
持仓显示问题快速诊断脚本
检查后端服务、前端服务、API 连接等
"""
import requests
from datetime import datetime
import json

BASE_URL = "http://localhost:5000/api"

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def print_step(step_num, title):
    print(f"\n{'─'*80}")
    print(f"步骤 {step_num}: {title}")
    print(f"{'─'*80}\n")

def check_backend():
    print_step(1, "检查后端服务")
    
    try:
        # 尝试访问 API 根路径
        response = requests.get(f"{BASE_URL}/", timeout=5)
        # 如果返回 200 或 404 (API 文档不存在但服务运行) 都认为服务正常
        if response.status_code in [200, 404]:
            print("✅ 后端服务运行正常")
            print(f"   API 地址：http://localhost:5000/api")
            print(f"   如果 404 是正常的，因为根路径可能未定义")
            return True
        else:
            print(f"❌ 后端服务异常：{response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 后端服务未运行或无法连接")
        print("   请确保已执行：python app.py")
        return False
    except Exception as e:
        print(f"❌ 检查失败：{e}")
        return False

def check_frontend():
    print_step(2, "检查前端服务")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务运行正常")
            print(f"   前端地址：http://localhost:3000")
            return True
        else:
            print(f"❌ 前端服务异常：{response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 前端服务未运行或无法连接")
        print("   请确保已执行：npm run dev")
        return False
    except Exception as e:
        print(f"❌ 检查失败：{e}")
        return False

def test_login():
    print_step(3, "测试登录功能")
    
    login_data = {
        "email": "demo_20260307203132@example.com",
        "password": "Demo123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            token = response.json()['access_token']
            print("✅ 登录成功")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print(f"❌ 登录失败：{response.status_code}")
            print(f"   响应：{response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ 登录异常：{e}")
        return None

def test_get_portfolio(token, portfolio_id=208):
    print_step(4, f"测试获取投资组合详情 (ID: {portfolio_id})")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            holdings = data.get('holdings', [])
            print("✅ 获取投资组合详情成功")
            print(f"   组合名称：{data['portfolio']['name']}")
            print(f"   持仓数量：{len(holdings)}")
            
            if len(holdings) > 0:
                print(f"\n   持仓明细:")
                for h in holdings:
                    asset_name = h.get('asset', {}).get('name', 'N/A')
                    quantity = h.get('quantity', 0)
                    cost_price = h.get('cost_price', 0)
                    current_price = h.get('current_price', 0)
                    value = quantity * current_price
                    profit = value - (quantity * cost_price)
                    
                    print(f"   - {asset_name}: 数量={quantity}, 成本价={cost_price}, "
                          f"当前价={current_price}, 市值={value:.2f}, 盈亏={profit:.2f}")
                
                # 检查当前价是否为 0
                zero_current_price = sum(1 for h in holdings if h.get('current_price', 0) == 0)
                if zero_current_price > 0:
                    print(f"\n⚠️  警告：{zero_current_price} 笔持仓的当前价为 0")
                else:
                    print(f"\n✅ 所有持仓的当前价都正常")
            else:
                print(f"⚠️  警告：持仓列表为空")
            
            return data
        else:
            print(f"❌ 获取失败：{response.status_code}")
            print(f"   响应：{response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ 获取异常：{e}")
        return None

def test_add_holding(token, portfolio_id=208):
    print_step(5, "测试添加持仓")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    holding_data = {
        "asset_id": 1,
        "quantity": 10,
        "cost_price": 30.00
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/portfolios/{portfolio_id}/holdings",
            json=holding_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ 添加持仓成功")
            print(f"   持仓 ID: {result.get('id', 'N/A')}")
            print(f"   资产 ID: {result.get('asset_id', 'N/A')}")
            print(f"   数量：{result.get('quantity', 'N/A')}")
            return result
        else:
            print(f"❌ 添加失败：{response.status_code}")
            print(f"   响应：{response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ 添加异常：{e}")
        return None

def generate_diagnostic_report(results):
    print_section("诊断报告")
    
    print(f"诊断时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_passed = all(results.values())
    
    if all_passed:
        print("✅ 所有检查通过！系统运行正常。")
        print()
        print("建议操作步骤:")
        print("1. 打开 Microsoft Edge 浏览器")
        print("2. 访问：http://localhost:3000")
        print("3. 登录：demo_20260307203132@example.com / Demo123456")
        print("4. 进入投资组合页面")
        print("5. 选择或创建投资组合")
        print("6. 点击'添加持仓'测试功能")
    else:
        print("❌ 发现以下问题:")
        for check, passed in results.items():
            if not passed:
                print(f"  - {check}")
        print()
        print("请先解决上述问题后再进行测试。")
    
    print()
    print("="*80)

# 主程序
if __name__ == "__main__":
    print_section("持仓显示问题 - 快速诊断工具")
    print(f"诊断时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 检查后端
    backend_ok = check_backend()
    results["后端服务"] = backend_ok
    
    if not backend_ok:
        generate_diagnostic_report(results)
        exit(1)
    
    # 检查前端
    frontend_ok = check_frontend()
    results["前端服务"] = frontend_ok
    
    if not frontend_ok:
        generate_diagnostic_report(results)
        exit(1)
    
    # 测试登录
    token = test_login()
    results["登录功能"] = token is not None
    
    if not token:
        generate_diagnostic_report(results)
        exit(1)
    
    # 测试获取投资组合
    portfolio_data = test_get_portfolio(token)
    results["获取投资组合"] = portfolio_data is not None
    
    # 测试添加持仓
    if portfolio_data:
        # 先不实际添加，只验证 API 可用
        print(f"\n{'─'*80}")
        print("提示：如需测试添加持仓功能，请在浏览器中手动操作")
        print(f"{'─'*80}")
    
    # 生成报告
    generate_diagnostic_report(results)
    
    print(f"\n✅ 诊断完成！")
    print(f"\n详细测试指南请查看：HOLDING_DISPLAY_TEST_GUIDE.md")
    print(f"最终测试报告请查看：FINAL_TEST_REPORT.md")
