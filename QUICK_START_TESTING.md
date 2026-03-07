# 市场数据测试快速启动指南

## 🚀 快速开始

### 1. 安装依赖

```bash
# 确保已安装 pytest
pip install pytest pytest-cov
```

### 2. 运行测试

#### 方式一：运行所有测试（推荐）
```bash
python run_market_tests.py
```

#### 方式二：运行特定测试文件
```bash
# 模型测试
python -m pytest tests/test_market_data_model.py -v

# 服务测试
python -m pytest tests/test_market_data_service.py -v

# 增强测试
python -m pytest tests/test_financial_data_query_enhanced.py -v

# API 集成测试
python -m pytest tests/test_market_api_integration.py -v

# 性能测试
python -m pytest tests/test_market_performance.py -v
```

#### 方式三：运行特定测试用例
```bash
# 运行单个测试
python -m pytest tests/test_market_data_model.py::TestMarketDataModel::test_create_market_data -v

# 运行测试类
python -m pytest tests/test_market_data_model.py::TestMarketDataModel -v
```

### 3. 生成覆盖率报告

```bash
# 生成 HTML 报告
python -m pytest tests/ --cov=app --cov-report=html

# 打开报告
# Windows
start htmlcov/index.html
# Linux/Mac
open htmlcov/index.html
```

### 4. 查看测试报告

```bash
# 查看完整测试报告
cat docs/TEST_REPORT_MARKET_DATA.md

# 查看总结
cat TEST_SUMMARY.md
```

---

## 📁 测试文件结构

```
tests/
├── conftest.py                          # 测试配置和 fixtures
├── test_market_data_model.py            # 市场数据模型测试（18 个用例）
├── test_market_data_service.py          # 市场数据服务测试（24 个用例）
├── test_financial_data_query_enhanced.py # 金融查询增强测试（35+ 个用例）
├── test_market_api_integration.py       # API 集成测试（30+ 个用例）
├── test_market_performance.py           # 性能测试（15 个用例）
├── test_market_mocks.py                 # Mock 工具类
└── test_market_query.py                 # 原有市场查询测试

docs/
├── TEST_REPORT_MARKET_DATA.md           # 详细测试报告
└── FINANCIAL_DATA_QUERY_SERVICE.md      # 金融查询服务文档

根目录/
├── run_market_tests.py                  # 测试运行脚本
├── TEST_SUMMARY.md                      # 测试总结
└── QUICK_START_TESTING.md               # 本文件
```

---

## 🎯 测试覆盖的功能

### 1. 市场数据模型 (MarketData)
- ✅ 创建和验证
- ✅ 关系映射
- ✅ 唯一约束
- ✅ 数值精度
- ✅ 边界条件
- ✅ 查询性能

### 2. 市场数据服务
- ✅ MarketDataService: 股票/指数数据获取
- ✅ MarketService: CRUD 操作
- ✅ 外部 API 集成（Mock）
- ✅ 异常处理

### 3. 金融数据查询服务
- ✅ 实时价格查询
- ✅ 投资组合持仓
- ✅ 历史数据查询
- ✅ 按需查询系统
- ✅ 缓存机制

### 4. API 接口
- ✅ REST CRUD 接口
- ✅ JWT 认证
- ✅ 搜索接口
- ✅ 数据同步接口

### 5. 性能测试
- ✅ 响应时间
- ✅ 并发性能
- ✅ 吞吐量
- ✅ 缓存性能

---

## 📊 测试统计

| 测试类型 | 文件数 | 用例数 | 覆盖率目标 |
|---------|--------|--------|-----------|
| 单元测试 | 3 | 77+ | ≥ 85% |
| 集成测试 | 1 | 30+ | ≥ 85% |
| 性能测试 | 1 | 15+ | - |
| Mock 工具 | 1 | - | - |
| **总计** | **6** | **122+** | **≥ 85%** |

---

## 🔧 常用命令

### 基础测试
```bash
# 运行所有测试
python run_market_tests.py

# 运行并显示日志
python -m pytest tests/ -v -o log_cli=true
```

### 选择性测试
```bash
# 只运行市场相关测试
python -m pytest tests/test_market*.py -v

# 排除性能测试
python -m pytest tests/ -v -k "not performance"
```

### 调试测试
```bash
# 显示打印输出
python -m pytest tests/test_market_data_model.py -v -s

# 遇到第一个失败就停止
python -m pytest tests/ -x

# 显示局部变量
python -m pytest tests/ -l
```

### 覆盖率相关
```bash
# 查看覆盖率摘要
python -m pytest tests/ --cov=app --cov-report=term-missing

# 生成 HTML 报告
python -m pytest tests/ --cov=app --cov-report=html

# 生成 XML 报告（用于 CI）
python -m pytest tests/ --cov=app --cov-report=xml
```

---

## 🐛 常见问题

### Q1: 测试失败提示 "fixture 'test_asset' not found"
**解决方案**: 确保 conftest.py 文件存在且包含必要的 fixtures

### Q2: 外部 API 调用失败
**解决方案**: 测试已使用 Mock 隔离外部依赖，确保 Mock 配置正确

### Q3: 数据库锁定错误
**解决方案**: SQLite 数据库文件被锁定，关闭其他数据库连接后重试

### Q4: 性能测试超时
**解决方案**: 调整性能基准或使用更小的数据集

---

## 📚 参考资料

- [pytest 官方文档](https://docs.pytest.org/)
- [测试报告](docs/TEST_REPORT_MARKET_DATA.md)
- [测试总结](TEST_SUMMARY.md)

---

## ✅ 验收清单

- [ ] 所有测试文件已创建
- [ ] 测试用例数 >= 122 个
- [ ] 代码覆盖率 >= 85%
- [ ] 性能测试达标
- [ ] 测试报告已生成
- [ ] Mock 工具类已提供
- [ ] 自动化脚本已创建

---

**最后更新**: 2026-03-07
**维护者**: PMS 开发团队
