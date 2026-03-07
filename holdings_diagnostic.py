"""
持仓添加和删除功能诊断脚本
测试持仓添加和删除功能的完整性
"""
import requests
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def print_step(step_num, title):
    print(f"\n{'─'*80}")
    print(f"步骤 {step_num}: {title}")
    print(f"{'─'*80}\n")

def test_holdings_functions():
    print_section("持仓添加和删除功能诊断")
    print(f"诊断时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "登录": False,
        "获取投资组合": False,
        "添加持仓": False,
        "验证添加": False,
        "删除持仓": False,
        "验证删除": False
    }
    
    # 步骤 1: 登录
    print_step(1, "用户登录")
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "demo_20260307203132@example.com",
        "password": "Demo123456"
    })
    
    if login_response.status_code == 200:
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print(f"✅ 登录成功")
        results["登录"] = True
    else:
        print(f"❌ 登录失败：{login_response.status_code}")
        return results
    
    # 步骤 2: 获取投资组合
    print_step(2, "获取投资组合详情")
    portfolio_id = 208  # 使用之前创建的投资组合
    response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        initial_holdings_count = len(data.get('holdings', []))
        print(f"✅ 获取成功")
        print(f"   组合名称：{data['portfolio']['name']}")
        print(f"   当前持仓数量：{initial_holdings_count}")
        results["获取投资组合"] = True
    else:
        print(f"❌ 获取失败：{response.status_code}")
        return results
    
    # 步骤 3: 添加持仓
    print_step(3, "添加持仓测试")
    
    # 先检查是否有可用资产
    assets_response = requests.get(f"{BASE_URL}/assets", headers=headers)
    if assets_response.status_code == 200:
        assets = assets_response.json()
        if len(assets) > 0:
            test_asset = assets[0]
            print(f"使用测试资产：{test_asset['name']} (ID: {test_asset['id']})")
            
            holding_data = {
                "asset_id": test_asset['id'],
                "quantity": 50,
                "cost_price": 25.00,
                "current_price": 26.00
            }
            
            print(f"添加持仓数据:")
            print(f"   资产 ID: {test_asset['id']}")
            print(f"   数量：50")
            print(f"   成本价：25.00")
            print(f"   当前价：26.00")
            
            add_response = requests.post(
                f"{BASE_URL}/portfolios/{portfolio_id}/holdings",
                json=holding_data,
                headers=headers
            )
            
            print(f"\nAPI 响应状态码：{add_response.status_code}")
            
            if add_response.status_code in [200, 201]:
                result = add_response.json()
                print(f"✅ 添加持仓成功")
                print(f"   持仓 ID: {result.get('id', 'N/A')}")
                print(f"   资产 ID: {result.get('asset_id', 'N/A')}")
                print(f"   数量：{result.get('quantity', 'N/A')}")
                print(f"   成本价：{result.get('cost_price', 'N/A')}")
                print(f"   当前价：{result.get('current_price', 'N/A')}")
                results["添加持仓"] = True
                
                # 验证添加
                print_step(4, "验证持仓添加")
                verify_response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)
                if verify_response.status_code == 200:
                    verify_data = verify_response.json()
                    new_holdings_count = len(verify_data.get('holdings', []))
                    print(f"当前持仓数量：{new_holdings_count}")
                    print(f"预期持仓数量：{initial_holdings_count + 1}")
                    
                    if new_holdings_count == initial_holdings_count + 1:
                        print(f"✅ 持仓添加验证成功")
                        results["验证添加"] = True
                        
                        # 获取新添加的持仓
                        new_holding = None
                        for h in verify_data['holdings']:
                            if h['id'] == result.get('id'):
                                new_holding = h
                                break
                        
                        if new_holding:
                            print(f"\n新持仓详情:")
                            asset_name = new_holding.get('asset', {}).get('name', 'N/A')
                            print(f"   资产名称：{asset_name}")
                            print(f"   持仓数量：{new_holding['quantity']}")
                            print(f"   成本价：{new_holding['cost_price']}")
                            print(f"   当前价：{new_holding['current_price']}")
                            
                            # 检查当前价
                            if new_holding['current_price'] == 0:
                                print(f"\n⚠️  警告：当前价为 0，这可能是前端显示问题的原因")
                            else:
                                print(f"\n✅ 当前价正确：{new_holding['current_price']}")
                        else:
                            print(f"❌ 未找到新添加的持仓")
                    else:
                        print(f"❌ 持仓数量未增加")
                else:
                    print(f"❌ 验证失败：{verify_response.status_code}")
            else:
                print(f"❌ 添加失败：{add_response.status_code}")
                print(f"响应：{add_response.text[:200]}")
        else:
            print(f"❌ 系统中没有可用资产")
    else:
        print(f"❌ 获取资产列表失败：{assets_response.status_code}")
    
    # 步骤 5: 删除持仓测试 (如果有持仓)
    print_step(5, "删除持仓测试")
    
    final_response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)
    if final_response.status_code == 200:
        final_data = final_response.json()
        holdings = final_data.get('holdings', [])
        
        if len(holdings) > 0:
            # 选择最后一个持仓进行删除测试
            test_holding = holdings[-1]
            holding_id_to_delete = test_holding['id']
            
            print(f"准备删除持仓:")
            print(f"   持仓 ID: {holding_id_to_delete}")
            asset_name = test_holding.get('asset', {}).get('name', 'N/A')
            print(f"   资产名称：{asset_name}")
            print(f"   数量：{test_holding['quantity']}")
            
            # 执行删除
            delete_response = requests.delete(
                f"{BASE_URL}/portfolios/{portfolio_id}/holdings/{holding_id_to_delete}",
                headers=headers
            )
            
            print(f"\n删除 API 响应状态码：{delete_response.status_code}")
            
            if delete_response.status_code == 200:
                print(f"✅ 删除成功")
                results["删除持仓"] = True
                
                # 验证删除
                print_step(6, "验证持仓删除")
                verify_delete_response = requests.get(
                    f"{BASE_URL}/portfolios/{portfolio_id}",
                    headers=headers
                )
                
                if verify_delete_response.status_code == 200:
                    verify_delete_data = verify_delete_response.json()
                    final_count = len(verify_delete_data.get('holdings', []))
                    print(f"删除后持仓数量：{final_count}")
                    print(f"预期持仓数量：{len(holdings) - 1}")
                    
                    if final_count == len(holdings) - 1:
                        print(f"✅ 持仓删除验证成功")
                        results["验证删除"] = True
                    else:
                        print(f"❌ 持仓数量未正确减少")
                else:
                    print(f"❌ 验证删除失败：{verify_delete_response.status_code}")
            else:
                print(f"❌ 删除失败：{delete_response.status_code}")
                print(f"响应：{delete_response.text[:200]}")
        else:
            print(f"⚠️  没有持仓可供删除测试")
    
    return results

def generate_diagnostic_results(results):
    print_section("诊断结果汇总")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    failed_tests = total_tests - passed_tests
    
    print(f"测试总数：{total_tests}")
    print(f"通过数量：{passed_tests}")
    print(f"失败数量：{failed_tests}")
    print(f"通过率：{(passed_tests/total_tests*100):.1f}%")
    print()
    
    print("详细结果:")
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {status} - {test_name}")
    
    print()
    if failed_tests == 0:
        print("🎉 所有测试通过！持仓添加和删除功能正常。")
    else:
        print("⚠️  发现以下问题:")
        for test_name, passed in results.items():
            if not passed:
                print(f"  - {test_name} 功能异常")
        
        print()
        print("建议排查步骤:")
        print("1. 检查前端按钮事件绑定")
        print("2. 检查 API 调用参数")
        print("3. 检查后端路由定义")
        print("4. 检查数据库连接")
        print("5. 查看浏览器控制台错误")
        print("6. 查看 Network 面板请求")

if __name__ == "__main__":
    results = test_holdings_functions()
    generate_diagnostic_results(results)
    
    print(f"\n{'='*80}")
    print(f"诊断完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
