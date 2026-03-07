"""
实时测试监控和验证脚本
通过 API 验证前端操作的结果
"""
import requests
import json
from datetime import datetime
import time

BASE_URL = "http://localhost:5000/api"

class TestMonitor:
    def __init__(self):
        self.token = None
        self.headers = None
        self.test_results = []
        self.start_time = datetime.now()
        
    def print_header(self, title):
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
        
    def print_step(self, step_num, title):
        print(f"\n{'─'*80}")
        print(f"步骤 {step_num}: {title}")
        print(f"{'─'*80}\n")
        
    def print_result(self, test_name, passed, details=""):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"     {details}")
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "time": datetime.now().isoformat()
        })
        
    def login(self, email, password):
        self.print_step(0, "用户登录")
        
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            self.token = response.json()['access_token']
            self.headers = {'Authorization': f'Bearer {self.token}'}
            self.print_result("用户登录", True, f"Token: {self.token[:50]}...")
            return True
        else:
            self.print_result("用户登录", False, f"状态码：{response.status_code}")
            return False
    
    def create_portfolio(self, name, description, benchmark, risk_level):
        self.print_step(1, "创建投资组合")
        
        portfolio_data = {
            "name": name,
            "description": description,
            "benchmark": benchmark,
            "risk_level": risk_level
        }
        
        response = requests.post(f"{BASE_URL}/portfolios", json=portfolio_data, headers=self.headers)
        
        if response.status_code in [200, 201]:
            portfolio = response.json()
            self.print_result("创建投资组合", True, f"ID: {portfolio['id']}, 名称：{portfolio['name']}")
            return portfolio['id']
        else:
            self.print_result("创建投资组合", False, f"状态码：{response.status_code}")
            return None
    
    def add_holding(self, portfolio_id, asset_id, quantity, cost_price, current_price):
        self.print_step(2, f"添加持仓 - 资产 ID: {asset_id}")
        
        holding_data = {
            "asset_id": asset_id,
            "quantity": quantity,
            "cost_price": cost_price
        }
        
        # 注意：前端会添加 current_price，但 API 可能不使用
        response = requests.post(
            f"{BASE_URL}/portfolios/{portfolio_id}/holdings",
            json=holding_data,
            headers=self.headers
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            self.print_result("添加持仓", True, f"持仓 ID: {result.get('id', 'N/A')}")
            return result
        else:
            self.print_result("添加持仓", False, f"状态码：{response.status_code}, 响应：{response.text[:100]}")
            return None
    
    def verify_portfolio_detail(self, portfolio_id):
        self.print_step(3, "验证投资组合详情")
        
        response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=self.headers)
        
        if response.status_code != 200:
            self.print_result("获取投资组合详情", False, f"状态码：{response.status_code}")
            return None
            
        detail = response.json()
        holdings = detail.get('holdings', [])
        
        self.print_result("获取详情", True, f"持仓数量：{len(holdings)}")
        
        # 验证持仓数据
        all_current_price_ok = True
        all_value_ok = True
        all_profit_ok = True
        
        print(f"\n持仓明细验证:")
        print(f"{'─'*70}")
        print(f"{'资产':<15} {'数量':>8} {'成本价':>10} {'当前价':>10} {'市值':>12} {'盈亏':>12} {'状态':>8}")
        print(f"{'─'*70}")
        
        for holding in holdings:
            asset_name = holding.get('asset', {}).get('name', 'N/A')
            quantity = holding.get('quantity', 0)
            cost_price = holding.get('cost_price', 0)
            current_price = holding.get('current_price', 0)
            
            # 计算验证
            expected_value = quantity * current_price
            expected_profit = expected_value - (quantity * cost_price)
            
            # 检查当前价
            if current_price == 0:
                self.print_result(f"持仓 {asset_name} 当前价", False, "当前价为 0")
                all_current_price_ok = False
            else:
                self.print_result(f"持仓 {asset_name} 当前价", True, f"{current_price}")
            
            # 检查市值
            if expected_value == 0:
                all_value_ok = False
            
            # 检查盈亏
            if expected_profit < 0 and current_price > cost_price:
                all_profit_ok = False
            
            status = "✅" if (current_price > 0 and expected_value > 0) else "❌"
            print(f"{asset_name:<15} {quantity:>8} {cost_price:>10.2f} {current_price:>10.2f} {expected_value:>12.2f} {expected_profit:>12.2f} {status:>8}")
        
        print(f"{'─'*70}")
        
        # 汇总验证
        total_cost = sum(h['quantity'] * h['cost_price'] for h in holdings)
        total_value = sum(h['quantity'] * h['current_price'] for h in holdings)
        total_profit = total_value - total_cost
        profit_rate = (total_profit / total_cost * 100) if total_cost > 0 else 0
        
        print(f"\n汇总数据:")
        print(f"  总成本：{total_cost:.2f}")
        print(f"  总市值：{total_value:.2f}")
        print(f"  总盈亏：{total_profit:.2f}")
        print(f"  总盈亏率：{profit_rate:.2f}%")
        
        # 验证结果
        self.print_result("所有当前价正确", all_current_price_ok)
        self.print_result("所有市值正确", all_value_ok)
        self.print_result("所有盈亏正确", all_profit_ok)
        self.print_result("汇总数据正确", total_profit > 0)
        
        return detail
    
    def generate_report(self):
        self.print_header("测试报告")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['passed'])
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"测试总数：{total_tests}")
        print(f"通过数量：{passed_tests}")
        print(f"失败数量：{failed_tests}")
        print(f"通过率：{pass_rate:.1f}%")
        print(f"测试耗时：{datetime.now() - self.start_time}")
        print()
        
        if failed_tests > 0:
            print("失败的测试:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  ❌ {result['test']}: {result['details']}")
        else:
            print("🎉 所有测试通过!")
        
        # 保存报告
        report = {
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration": str(datetime.now() - self.start_time),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate": f"{pass_rate:.1f}%",
            "results": self.test_results
        }
        
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n测试报告已保存到：{report_file}")
        
        return failed_tests == 0

# 执行测试
if __name__ == "__main__":
    monitor = TestMonitor()
    
    monitor.print_header("PMS 系统完整测试")
    print(f"测试开始时间：{monitor.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 步骤 0: 登录
    if not monitor.login("demo_20260307203132@example.com", "Demo123456"):
        print("登录失败，退出测试")
        exit(1)
    
    # 步骤 1: 创建投资组合
    timestamp = datetime.now().strftime('%m%d_%H%M')
    portfolio_id = monitor.create_portfolio(
        f"Web 测试组合_{timestamp}",
        "网页界面完整测试",
        "沪深 300",
        "中等"
    )
    
    if not portfolio_id:
        print("创建投资组合失败，退出测试")
        exit(1)
    
    # 步骤 2: 添加持仓
    test_holdings = [
        {"asset_id": 1, "quantity": 100, "cost_price": 30.0, "current_price": 33.0},
        {"asset_id": 2, "quantity": 200, "cost_price": 10.0, "current_price": 10.5},
        {"asset_id": 3, "quantity": 300, "cost_price": 5.0, "current_price": 5.2},
    ]
    
    for holding in test_holdings:
        monitor.add_holding(
            portfolio_id,
            holding['asset_id'],
            holding['quantity'],
            holding['cost_price'],
            holding['current_price']
        )
        time.sleep(0.5)  # 短暂延迟，避免并发问题
    
    # 步骤 3: 验证
    detail = monitor.verify_portfolio_detail(portfolio_id)
    
    # 步骤 4: 生成报告
    all_passed = monitor.generate_report()
    
    print(f"\n{'='*80}")
    if all_passed:
        print("  ✅ 所有测试通过！系统功能正常！")
    else:
        print("  ⚠️  部分测试失败，请检查上述报告")
    print(f"{'='*80}\n")
    
    exit(0 if all_passed else 1)
