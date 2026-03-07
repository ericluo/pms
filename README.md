# 投资组合管理系统 (PMS)

一个现代化的投资组合管理系统，为个人和机构投资者提供全面的投资管理工具。

## 项目概述

PMS（Portfolio Management System）是一个功能完备、用户友好的投资组合管理系统，帮助投资者更有效地管理和分析投资组合，做出更明智的投资决策。

### 核心功能

- **投资组合管理**：创建、管理和监控多个投资组合
- **资产管理**：支持股票、基金、债券、现金等多种资产类型
- **业绩分析**：计算回报率、风险指标，与基准对比
- **市场数据**：获取实时行情和市场资讯
- **现金管理**：记录资金流水，管理现金余额
- **报告生成**：生成详细的投资组合报告

### 目标用户

- 个人投资者
- 投资顾问
- 小型投资机构

## 技术架构

### 前端技术栈

- **框架**：Vue 3 + TypeScript
- **状态管理**：Pinia
- **UI 组件库**：Element Plus
- **数据可视化**：ECharts
- **网络请求**：Axios
- **构建工具**：Vite
- **路由管理**：Vue Router

### 后端技术栈

- **语言**：Python 3.9+
- **Web 框架**：Flask
- **数据库**：SQLite
- **ORM**：SQLAlchemy
- **认证**：Flask-JWT-Extended
- **API 文档**：Flask-RESTx

## 快速开始

### 环境要求

- Node.js >= 16.0.0
- Python >= 3.9
- npm >= 8.0.0

### 安装步骤

#### 1. 克隆项目

```bash
git clone <repository-url>
cd pms
```

#### 2. 安装前端依赖

```bash
npm install
```

#### 3. 安装后端依赖

```bash
pip install -r requirements.txt
```

#### 4. 启动后端服务

```bash
python app.py
```

后端服务将在 `http://localhost:5000` 启动

#### 5. 启动前端服务

```bash
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

### 默认测试账号

- 邮箱：`test123@example.com`
- 密码：`123456`

## 项目结构

```
pms/
├── app/                      # 后端应用
│   ├── api/                  # API 路由
│   ├── models/               # 数据模型
│   ├── schemas/              # 数据验证模式
│   ├── services/             # 业务逻辑层
│   ├── utils/                # 工具函数
│   └── config/               # 配置文件
├── src/                      # 前端源代码
│   ├── api/                  # API 调用
│   ├── assets/               # 静态资源
│   ├── components/           # 公共组件
│   ├── router/               # 路由配置
│   ├── store/                # 状态管理
│   ├── types/                # TypeScript 类型定义
│   ├── utils/                # 工具函数
│   ├── views/                # 页面组件
│   └── App.vue               # 根组件
├── tests/                    # Playwright 前端测试
├── docs/                     # 项目文档
├── package.json              # 前端依赖配置
├── requirements.txt          # 后端依赖配置
├── vite.config.ts            # Vite 配置
└── playwright.config.ts      # Playwright 测试配置
```

## 数据模型

### 核心数据表

- **users** - 用户表
- **portfolios** - 投资组合表
- **assets** - 资产表（股票/基金/债券/现金）
- **holdings** - 持仓表
- **transactions** - 交易记录表
- **cash_flows** - 现金流水表
- **market_data** - 市场数据表

详细设计请参考 [数据库设计文档](./PMS_数据库 schema 设计.md)

## 开发指南

### 前端开发

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview

# 运行测试
npm run test
```

### 后端开发

```bash
# 启动开发服务器
python app.py

# 运行 API 测试
pytest
```

## 测试

### 前端测试

项目使用 Playwright 进行前端 E2E 测试：

```bash
# 运行所有测试
npx playwright test

# 运行特定测试
npx playwright test tests/smoke.spec.ts

# 生成测试报告
npx playwright test --reporter=html
```

### 后端测试

```bash
# 运行单元测试
pytest

# 运行 API 测试
python test_api.py
```

## 文档

- [需求规范文档](./PMS_需求规范文档.md)
- [数据库设计](./PMS_数据库 schema 设计.md)
- [后端架构设计](./PMS_后端技术架构设计.md)
- [前端架构设计](./PMS_前端技术架构设计.md)
- [项目实施计划](./PMS_项目实施计划.md)

## 功能特性

### 1. 投资组合管理

- 创建多个投资组合
- 设置默认投资组合
- 组合调整和再平衡
- 实时业绩跟踪

### 2. 资产管理

- 支持股票、基金、债券、现金四种资产类型
- 资产类型筛选和搜索
- 资产详情查看
- 持仓成本跟踪

### 3. 业绩分析

- 绝对回报和相对回报
- 年化收益率计算
- 风险指标（波动率、夏普比率、最大回撤）
- 基准对比分析

### 4. 市场数据

- 实时行情获取
- 市场指数跟踪
- 行业板块表现
- 市场新闻资讯

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目主页：[项目 URL]
- 问题反馈：[Issue Tracker]

## 更新日志

### v0.1.0 (2024-01-01)

- ✨ 初始版本发布
- ✨ 实现投资组合管理功能
- ✨ 实现资产管理功能（股票/基金/债券/现金）
- ✨ 实现基础业绩分析
- ✨ 实现市场数据获取
- 🐛 修复已知问题

---

**注意**：本项目仅供学习和个人使用。投资有风险，使用本系统进行的投资决策需自行承担风险。
