"""
前端日志分析工具 - 模拟添加持仓操作并捕获所有日志
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000/api"
FRONTEND_URL = "http://localhost:3000"

class LogAnalyzer:
    def __init__(self):
        self.logs = []
        self.network_requests = []
        self.errors = []
        self.performance_metrics = {
            'start_time': None,
            'login_time': None,
            'portfolio_load_time': None,
            'add_holding_time': None,
            'refresh_time': None,
            'end_time': None
        }
    
    def log(self, category, message, data=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        log_entry = {
            'timestamp': timestamp,
            'category': category,
            'message': message,
            'data': data
        }
        self.logs.append(log_entry)
        print(f"[{timestamp}] [{category}] {message}")
        if data:
            print(f"  数据：{json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
    
    def error(self, message, error_data=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        error_entry = {
            'timestamp': timestamp,
            'message': message,
            'data': error_data
        }
        self.errors.append(error_entry)
        print(f"[{timestamp}] [ERROR] ❌ {message}")
        if error_data:
            print(f"  错误详情：{json.dumps(error_data, indent=2, ensure_ascii=False)[:500]}")
    
    def network_request(self, method, url, status_code, response_time, request_data=None, response_data=None):
        entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'method': method,
            'url': url,
            'status_code': status_code,
            'response_time_ms': response_time,
            'request_data': request_data,
            'response_data': response_data
        }
        self.network_requests.append(entry)
        status_icon = "✅" if 200 <= status_code < 300 else "❌"
        print(f"[{entry['timestamp']}] [NETWORK] {status_icon} {method} {url}")
        print(f"  状态码：{status_code}, 响应时间：{response_time}ms")
    
    def analyze_console_logs(self):
        """分析前端控制台日志"""
        print("\n" + "="*80)
        print("前端控制台日志分析")
        print("="*80)
        
        # 预期的日志序列
        expected_logs = [
            "获取投资组合详情，ID:",
            "获取投资组合详情响应:",
            "响应类型:",
            "响应键:",
            "投资组合数据:",
            "持仓列表:",
            "持仓数量:",
            "提交持仓，投资组合 ID:",
            "表单数据:",
            "添加新持仓",
            "添加持仓结果:",
            "等待刷新...",
            "刷新持仓列表...",
            "获取投资组合详情，ID:",
            "持仓列表已刷新，当前持仓数量:"
        ]
        
        print("\n预期的日志序列:")
        for i, log in enumerate(expected_logs, 1):
            print(f"  {i}. {log}")
        
        print("\n检查关键日志点:")
        critical_points = [
            "提交持仓，投资组合 ID:",
            "添加持仓结果:",
            "刷新持仓列表...",
            "持仓列表已刷新"
        ]
        
        for point in critical_points:
            print(f"  - {point}: ⚠️ 需要在浏览器控制台检查")
    
    def analyze_network_requests(self):
        """分析网络请求"""
        print("\n" + "="*80)
        print("网络请求分析")
        print("="*80)
        
        if not self.network_requests:
            print("\n⚠️  暂无网络请求记录")
            print("提示：需要在浏览器中操作并查看 Network 标签")
            return
        
        print(f"\n总请求数：{len(self.network_requests)}")
        
        # 按类型分组
        api_requests = [r for r in self.network_requests if '/api/' in r['url']]
        other_requests = [r for r in self.network_requests if '/api/' not in r['url']]
        
        print(f"API 请求数：{len(api_requests)}")
        print(f"其他请求数：{len(other_requests)}")
        
        # 分析 API 请求
        print("\nAPI 请求详情:")
        for req in api_requests:
            status_icon = "✅" if 200 <= req['status_code'] < 300 else "❌"
            print(f"\n  {status_icon} {req['method']} {req['url']}")
            print(f"     状态码：{req['status_code']}")
            print(f"     响应时间：{req['response_time_ms']}ms")
            
            if req['request_data']:
                print(f"     请求数据：{json.dumps(req['request_data'], indent=2)[:200]}")
            
            if req['response_data']:
                print(f"     响应数据：{json.dumps(req['response_data'], indent=2)[:300]}")
        
        # 性能分析
        print("\n" + "="*80)
        print("性能指标分析")
        print("="*80)
        
        if self.performance_metrics['start_time']:
            print(f"\n开始时间：{self.performance_metrics['start_time']}")
        
        if self.performance_metrics['login_time']:
            print(f"登录耗时：{self.performance_metrics['login_time']}ms")
        
        if self.performance_metrics['portfolio_load_time']:
            print(f"加载投资组合耗时：{self.performance_metrics['portfolio_load_time']}ms")
        
        if self.performance_metrics['add_holding_time']:
            print(f"添加持仓耗时：{self.performance_metrics['add_holding_time']}ms")
        
        if self.performance_metrics['refresh_time']:
            print(f"刷新持仓耗时：{self.performance_metrics['refresh_time']}ms")
        
        # 响应时间统计
        if api_requests:
            avg_response_time = sum(r['response_time_ms'] for r in api_requests) / len(api_requests)
            max_response_time = max(r['response_time_ms'] for r in api_requests)
            min_response_time = min(r['response_time_ms'] for r in api_requests)
            
            print(f"\n响应时间统计:")
            print(f"  平均：{avg_response_time:.2f}ms")
            print(f"  最快：{min_response_time}ms")
            print(f"  最慢：{max_response_time}ms")
    
    def analyze_backend_response(self):
        """分析后端响应"""
        print("\n" + "="*80)
        print("后端响应分析")
        print("="*80)
        
        add_holding_requests = [
            r for r in self.network_requests 
            if 'POST' in r['method'] and '/holdings' in r['url']
        ]
        
        if not add_holding_requests:
            print("\n⚠️  未找到添加持仓请求")
            print("提示：请在浏览器中执行添加持仓操作")
            return
        
        print(f"\n找到 {len(add_holding_requests)} 个添加持仓请求")
        
        for i, req in enumerate(add_holding_requests, 1):
            print(f"\n--- 请求 {i} ---")
            print(f"URL: {req['url']}")
            print(f"方法：{req['method']}")
            print(f"状态码：{req['status_code']}")
            print(f"响应时间：{req['response_time_ms']}ms")
            
            if req['status_code'] == 201:
                print("✅ 状态码正确 (201 Created)")
            else:
                print(f"❌ 状态码异常 (期望 201, 实际 {req['status_code']})")
            
            if req['response_data']:
                response = req['response_data']
                print(f"\n响应数据结构:")
                print(f"  ID: {response.get('id', 'MISSING')}")
                print(f"  asset_id: {response.get('asset_id', 'MISSING')}")
                print(f"  quantity: {response.get('quantity', 'MISSING')}")
                print(f"  cost_price: {response.get('cost_price', 'MISSING')}")
                print(f"  current_price: {response.get('current_price', 'MISSING')}")
                print(f"  value: {response.get('value', 'MISSING')}")
                print(f"  profit: {response.get('profit', 'MISSING')}")
                print(f"  profit_percent: {response.get('profit_percent', 'MISSING')}")
                print(f"  weight: {response.get('weight', 'MISSING')}")
                
                # 检查必需字段
                required_fields = ['id', 'asset_id', 'quantity', 'cost_price', 'current_price']
                missing_fields = [f for f in required_fields if f not in response]
                
                if missing_fields:
                    print(f"\n❌ 缺失字段：{', '.join(missing_fields)}")
                else:
                    print(f"\n✅ 所有必需字段都存在")
    
    def identify_issues(self):
        """识别潜在问题"""
        print("\n" + "="*80)
        print("问题识别")
        print("="*80)
        
        issues = []
        
        # 检查错误
        if self.errors:
            issues.append(f"发现 {len(self.errors)} 个错误")
            for error in self.errors:
                issues.append(f"  - {error['message']}")
        
        # 检查失败的网络请求
        failed_requests = [
            r for r in self.network_requests 
            if r['status_code'] >= 400
        ]
        if failed_requests:
            issues.append(f"发现 {len(failed_requests)} 个失败的网络请求")
            for req in failed_requests:
                issues.append(f"  - {req['method']} {req['url']} ({req['status_code']})")
        
        # 检查慢请求
        slow_requests = [
            r for r in self.network_requests 
            if r['response_time_ms'] > 1000
        ]
        if slow_requests:
            issues.append(f"发现 {len(slow_requests)} 个慢请求 (>1000ms)")
            for req in slow_requests:
                issues.append(f"  - {req['method']} {req['url']} ({req['response_time_ms']}ms)")
        
        if issues:
            print("\n发现的问题:")
            for issue in issues:
                print(f"  ⚠️  {issue}")
        else:
            print("\n✅ 未发现明显问题")
        
        # 常见问题检查清单
        print("\n常见问题检查清单:")
        checklist = [
            "浏览器缓存是否已清除？",
            "前端代码是否已重新编译？",
            "Console 中是否有 JavaScript 错误？",
            "Network 中是否有失败的请求？",
            "添加持仓后是否触发了刷新请求？",
            "刷新请求的响应中是否包含新持仓？",
            "Vue 响应式数据是否正确更新？"
        ]
        
        for item in checklist:
            print(f"  □ {item}")
    
    def generate_report(self):
        """生成完整报告"""
        print("\n" + "="*80)
        print("完整分析报告")
        print("="*80)
        
        report = {
            'summary': {
                'total_logs': len(self.logs),
                'total_errors': len(self.errors),
                'total_network_requests': len(self.network_requests),
                'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'performance': self.performance_metrics,
            'issues_count': len(self.errors) + len([
                r for r in self.network_requests if r['status_code'] >= 400
            ])
        }
        
        print("\n报告摘要:")
        print(f"  总日志数：{report['summary']['total_logs']}")
        print(f"  错误数：{report['summary']['total_errors']}")
        print(f"  网络请求数：{report['summary']['total_network_requests']}")
        print(f"  问题数：{report['issues_count']}")
        print(f"  分析时间：{report['summary']['analysis_time']}")
        
        return report


def simulate_add_holding_flow():
    """模拟完整的添加持仓流程"""
    analyzer = LogAnalyzer()
    
    print("="*80)
    print("开始模拟添加持仓流程")
    print("="*80)
    
    analyzer.performance_metrics['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # 1. 登录
    print("\n[步骤 1] 用户登录")
    start = time.time()
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "demo_20260307203132@example.com",
            "password": "Demo123456"
        })
        login_time = (time.time() - start) * 1000
        analyzer.performance_metrics['login_time'] = f"{login_time:.2f}"
        
        token = login_response.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        analyzer.network_request(
            'POST', f'{BASE_URL}/auth/login',
            login_response.status_code, login_time,
            request_data={"email": "demo_...@example.com", "password": "***"},
            response_data={"access_token": "eyJ..."}
        )
        analyzer.log('AUTH', '登录成功', {'token_length': len(token)})
    except Exception as e:
        analyzer.error(f'登录失败：{str(e)}')
        return analyzer
    
    # 2. 获取投资组合列表
    print("\n[步骤 2] 获取投资组合列表")
    start = time.time()
    portfolios_response = requests.get(f"{BASE_URL}/portfolios", headers=headers)
    portfolio_time = (time.time() - start) * 1000
    analyzer.performance_metrics['portfolio_load_time'] = f"{portfolio_time:.2f}"
    
    analyzer.network_request(
        'GET', f'{BASE_URL}/portfolios',
        portfolios_response.status_code, portfolio_time,
        response_data=portfolios_response.json()[:2]  # 只显示前 2 个
    )
    
    portfolios = portfolios_response.json()
    portfolio_id = portfolios[0]['id']
    analyzer.log('PORTFOLIO', '获取投资组合列表成功', {
        'count': len(portfolios),
        'first_portfolio': portfolios[0]['name']
    })
    
    # 3. 获取投资组合详情
    print("\n[步骤 3] 获取投资组合详情")
    start = time.time()
    detail_response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)
    detail_time = (time.time() - start) * 1000
    
    analyzer.network_request(
        'GET', f'{BASE_URL}/portfolios/{portfolio_id}',
        detail_response.status_code, detail_time,
        response_data={
            'portfolio': detail_response.json().get('portfolio', {}),
            'holdings_count': len(detail_response.json().get('holdings', []))
        }
    )
    
    detail_data = detail_response.json()
    holdings_before = detail_data.get('holdings', [])
    analyzer.log('PORTFOLIO_DETAIL', '获取投资组合详情成功', {
        'portfolio_name': detail_data['portfolio']['name'],
        'holdings_count': len(holdings_before)
    })
    
    # 4. 添加持仓
    print("\n[步骤 4] 添加持仓")
    start = time.time()
    holding_data = {
        "asset_id": 1,
        "quantity": 100,
        "cost_price": 28.5,
        "current_price": 29.0
    }
    
    add_response = requests.post(
        f"{BASE_URL}/portfolios/{portfolio_id}/holdings",
        headers=headers,
        json=holding_data
    )
    add_time = (time.time() - start) * 1000
    analyzer.performance_metrics['add_holding_time'] = f"{add_time:.2f}"
    
    analyzer.network_request(
        'POST', f'{BASE_URL}/portfolios/{portfolio_id}/holdings',
        add_response.status_code, add_time,
        request_data=holding_data,
        response_data=add_response.json()
    )
    
    if add_response.status_code == 201:
        added_holding = add_response.json()
        analyzer.log('ADD_HOLDING', '添加持仓成功', {
            'holding_id': added_holding.get('id'),
            'asset_name': added_holding.get('asset_name', 'N/A'),
            'quantity': added_holding.get('quantity'),
            'cost_price': added_holding.get('cost_price'),
            'current_price': added_holding.get('current_price')
        })
    else:
        analyzer.error(f'添加持仓失败：{add_response.status_code}', add_response.text)
    
    # 5. 刷新持仓列表
    print("\n[步骤 5] 刷新持仓列表")
    start = time.time()
    time.sleep(0.3)  # 模拟前端延迟
    
    refresh_response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}", headers=headers)
    refresh_time = (time.time() - start) * 1000
    analyzer.performance_metrics['refresh_time'] = f"{refresh_time:.2f}"
    
    analyzer.network_request(
        'GET', f'{BASE_URL}/portfolios/{portfolio_id}',
        refresh_response.status_code, refresh_time,
        response_data={
            'holdings_count': len(refresh_response.json().get('holdings', []))
        }
    )
    
    refresh_data = refresh_response.json()
    holdings_after = refresh_data.get('holdings', [])
    analyzer.log('REFRESH', '刷新持仓列表成功', {
        'holdings_count': len(holdings_after),
        'expected_count': len(holdings_before) + 1
    })
    
    # 6. 验证
    print("\n[步骤 6] 验证新持仓")
    if len(holdings_after) == len(holdings_before) + 1:
        analyzer.log('VALIDATION', '✅ 持仓数量正确增加')
        
        # 查找新持仓
        new_holding = None
        if add_response.status_code == 201:
            added_id = added_holding['id']
            new_holding = next((h for h in holdings_after if h['id'] == added_id), None)
            
            if new_holding:
                analyzer.log('VALIDATION', '✅ 新持仓在列表中', {
                    'asset_name': new_holding['asset']['name'] if new_holding.get('asset') else 'N/A',
                    'quantity': new_holding['quantity'],
                    'current_price': new_holding['current_price']
                })
            else:
                analyzer.error('❌ 新持仓不在列表中')
    else:
        analyzer.error(f'❌ 持仓数量异常：期望 {len(holdings_before) + 1}, 实际 {len(holdings_after)}')
    
    analyzer.performance_metrics['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # 生成报告
    analyzer.analyze_console_logs()
    analyzer.analyze_network_requests()
    analyzer.analyze_backend_response()
    analyzer.identify_issues()
    analyzer.generate_report()
    
    return analyzer


if __name__ == "__main__":
    analyzer = simulate_add_holding_flow()
    
    print("\n" + "="*80)
    print("日志分析完成")
    print("="*80)
    print("\n提示：")
    print("1. 以上是基于后端 API 的模拟测试结果")
    print("2. 要查看真实的前端日志，请：")
    print("   - 打开 Microsoft Edge 浏览器")
    print("   - 访问 http://localhost:3000")
    print("   - 按 F12 打开开发者工具")
    print("   - 进入 Console 和 Network 标签")
    print("   - 执行添加持仓操作")
    print("   - 观察日志输出")
