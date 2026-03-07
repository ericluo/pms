"""
PMS 测试运行脚本
运行所有测试并生成覆盖率报告
"""
import subprocess
import sys
import os

def run_tests():
    """运行所有测试"""
    print("=" * 80)
    print("PMS 项目完整测试套件")
    print("=" * 80)
    
    # 测试文件列表
    test_files = [
        "tests/test_simple.py",
        "tests/test_backend.py",
        "tests/test_complete_services.py",
        "tests/test_complete_apis.py"
    ]
    
    # 运行测试
    cmd = [
        sys.executable, "-m", "pytest",
        "-v",
        "--tb=short",
        "--maxfail=5"
    ] + test_files
    
    print(f"\n运行命令：{' '.join(cmd)}")
    print("\n" + "=" * 80 + "\n")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 输出结果
    print(result.stdout)
    if result.stderr:
        print("错误输出:")
        print(result.stderr)
    
    # 解析结果
    lines = result.stdout.split('\n')
    passed = 0
    failed = 0
    errors = 0
    
    for line in lines:
        if 'passed' in line:
            for part in line.split():
                if part.isdigit():
                    passed = int(part)
                    break
        if 'failed' in line:
            for part in line.split():
                if part.isdigit():
                    failed = int(part)
                    break
        if 'error' in line:
            for part in line.split():
                if part.isdigit():
                    errors = int(part)
                    break
    
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    print(f"通过：{passed}")
    print(f"失败：{failed}")
    print(f"错误：{errors}")
    print(f"总计：{passed + failed + errors}")
    print("=" * 80)
    
    return result.returncode == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
