"""
市场行情数据测试运行脚本
一键执行所有市场数据相关测试并生成报告
"""
import subprocess
import sys
import os
from datetime import datetime

def run_tests():
    """运行所有市场数据相关测试"""
    
    test_files = [
        'tests/test_market_data_model.py',
        'tests/test_market_data_service.py',
        'tests/test_financial_data_query_enhanced.py',
        'tests/test_market_api_integration.py',
        'tests/test_market_performance.py',
        'tests/test_market_mocks.py'
    ]
    
    print("=" * 80)
    print("市场行情数据测试套件")
    print("=" * 80)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 运行测试
    cmd = [
        sys.executable, '-m', 'pytest',
        *test_files,
        '-v',
        '--tb=short',
        '-o', 'log_cli=true',
        '-o', 'log_cli_level=INFO'
    ]
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    print("=" * 80)
    print(f"结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    if result.returncode == 0:
        print("\n✅ 所有测试通过！")
    else:
        print(f"\n❌ 测试失败，退出码：{result.returncode}")
    
    return result.returncode

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
