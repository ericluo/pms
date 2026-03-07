#!/bin/bash
# PMS 测试运行脚本

echo "=========================================="
echo "PMS 系统测试套件"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 函数：运行后端测试
run_backend_tests() {
    echo -e "${YELLOW}[1/3] 运行后端单元测试...${NC}"
    echo ""
    
    # 检查 pytest 是否安装
    if ! command -v pytest &> /dev/null; then
        echo -e "${RED}错误：pytest 未安装，请先安装依赖${NC}"
        echo "运行：pip install -r requirements.txt"
        return 1
    fi
    
    # 运行后端测试
    cd "$(dirname "$0")"
    pytest tests/test_backend.py -v --tb=short --cov=app --cov-report=term-missing
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 后端测试通过${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ 后端测试失败${NC}"
        ((FAILED_TESTS++))
    fi
    
    ((TOTAL_TESTS++))
    echo ""
}

# 函数：运行前端测试
run_frontend_tests() {
    echo -e "${YELLOW}[2/3] 运行前端组件测试...${NC}"
    echo ""
    
    # 检查 npm 是否安装
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}错误：npm 未安装${NC}"
        return 1
    fi
    
    # 检查 vitest 是否安装
    if [ ! -d "node_modules/vitest" ]; then
        echo -e "${YELLOW}警告：vitest 未安装，正在安装依赖...${NC}"
        npm install
    fi
    
    # 运行前端测试
    npm run test:unit
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 前端测试通过${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ 前端测试失败${NC}"
        ((FAILED_TESTS++))
    fi
    
    ((TOTAL_TESTS++))
    echo ""
}

# 函数：运行 E2E 测试
run_e2e_tests() {
    echo -e "${YELLOW}[3/3] 运行 E2E 测试...${NC}"
    echo ""
    
    # 检查 playwright 是否安装
    if [ ! -d "node_modules/@playwright/test" ]; then
        echo -e "${YELLOW}警告：playwright 未安装，正在安装依赖...${NC}"
        npm install
        npx playwright install
    fi
    
    # 运行 E2E 测试
    npm run test:e2e
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ E2E 测试通过${NC}"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ E2E 测试失败${NC}"
        ((FAILED_TESTS++))
    fi
    
    ((TOTAL_TESTS++))
    echo ""
}

# 函数：显示测试结果
show_summary() {
    echo "=========================================="
    echo "测试总结"
    echo "=========================================="
    echo "总测试数：$TOTAL_TESTS"
    echo -e "${GREEN}通过：$PASSED_TESTS${NC}"
    echo -e "${RED}失败：$FAILED_TESTS${NC}"
    echo ""
    
    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${GREEN}🎉 所有测试通过！${NC}"
        exit 0
    else
        echo -e "${RED}❌ 部分测试失败，请检查错误信息${NC}"
        exit 1
    fi
}

# 主函数
main() {
    case "${1:-all}" in
        backend)
            run_backend_tests
            ;;
        frontend)
            run_frontend_tests
            ;;
        e2e)
            run_e2e_tests
            ;;
        all)
            run_backend_tests
            run_frontend_tests
            run_e2e_tests
            ;;
        *)
            echo "用法：$0 {backend|frontend|e2e|all}"
            exit 1
            ;;
    esac
    
    show_summary
}

# 执行主函数
main "$@"
