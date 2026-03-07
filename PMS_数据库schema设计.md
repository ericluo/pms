# 投资组合管理系统 (PMS) 数据库schema设计

## 1. 数据库概述

本设计基于SQLite数据库，为投资组合管理系统提供数据存储支持。数据库包含7个核心表，分别是用户表、投资组合表、资产表、持仓表、交易记录表、现金流水表和市场数据表。这些表之间通过外键关联，形成完整的数据关系网络。

## 2. 表结构设计

### 2.1 用户表 (users)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 用户ID |
| `username` | `VARCHAR(50)` | `UNIQUE NOT NULL` | 用户名 |
| `email` | `VARCHAR(100)` | `UNIQUE NOT NULL` | 邮箱 |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` | 密码哈希 |
| `name` | `VARCHAR(100)` | `NOT NULL` | 真实姓名 |
| `role` | `VARCHAR(20)` | `NOT NULL DEFAULT 'user'` | 角色（admin/user） |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 更新时间 |

**索引**：
- `CREATE INDEX idx_users_username ON users(username);`
- `CREATE INDEX idx_users_email ON users(email);`

### 2.2 投资组合表 (portfolios)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 组合ID |
| `user_id` | `INTEGER` | `NOT NULL REFERENCES users(id) ON DELETE CASCADE` | 用户ID |
| `name` | `VARCHAR(100)` | `NOT NULL` | 组合名称 |
| `description` | `TEXT` | | 组合描述 |
| `benchmark` | `VARCHAR(50)` | `NOT NULL` | 业绩基准 |
| `risk_level` | `VARCHAR(20)` | `NOT NULL` | 风险等级 |
| `is_default` | `BOOLEAN` | `NOT NULL DEFAULT FALSE` | 是否为默认投资组合 |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 更新时间 |

**索引**：
- `CREATE INDEX idx_portfolios_user_id ON portfolios(user_id);`

### 资产类型说明

资产表（assets）的 `type` 字段支持以下类型：

| 类型值 | 说明 | 特点 |
|--------|------|------|
| `stock` | 股票 | 需要实时行情支持 |
| `fund` | 基金 | 包括ETF、开放式基金等 |
| `bond` | 债券 | 包括国债、企业债等 |
| `cash` | 现金 | 现金及现金等价物（如余额宝） |

### 2.3 资产表 (assets)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 资产ID |
| `code` | `VARCHAR(20)` | `UNIQUE NOT NULL` | 资产代码 |
| `name` | `VARCHAR(100)` | `NOT NULL` | 资产名称 |
| `type` | `VARCHAR(20)` | `NOT NULL` | 资产类型（股票/基金/债券等） |
| `market` | `VARCHAR(50)` | `NOT NULL` | 市场（A股/港股/美股等） |
| `industry` | `VARCHAR(50)` | | 所属行业 |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 更新时间 |

**索引**：
- `CREATE INDEX idx_assets_code ON assets(code);`
- `CREATE INDEX idx_assets_type ON assets(type);`
- `CREATE INDEX idx_assets_market ON assets(market);`
- `CREATE INDEX idx_assets_industry ON assets(industry);`

### 2.4 持仓表 (holdings)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 持仓ID |
| `portfolio_id` | `INTEGER` | `NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE` | 组合ID |
| `asset_id` | `INTEGER` | `NOT NULL REFERENCES assets(id)` | 资产ID |
| `quantity` | `DECIMAL(18,4)` | `NOT NULL` | 持仓数量 |
| `cost_price` | `DECIMAL(18,4)` | `NOT NULL` | 持仓成本价 |
| `current_price` | `DECIMAL(18,4)` | `NOT NULL` | 当前价格 |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 更新时间 |

**索引**：
- `CREATE INDEX idx_holdings_portfolio_id ON holdings(portfolio_id);`
- `CREATE INDEX idx_holdings_asset_id ON holdings(asset_id);`
- `CREATE UNIQUE INDEX idx_holdings_portfolio_asset ON holdings(portfolio_id, asset_id);`

### 2.5 交易记录表 (transactions)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 交易ID |
| `portfolio_id` | `INTEGER` | `NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE` | 组合ID |
| `asset_id` | `INTEGER` | `NOT NULL REFERENCES assets(id)` | 资产ID |
| `type` | `VARCHAR(10)` | `NOT NULL` | 交易类型（买入/卖出） |
| `quantity` | `DECIMAL(18,4)` | `NOT NULL` | 交易数量 |
| `price` | `DECIMAL(18,4)` | `NOT NULL` | 交易价格 |
| `amount` | `DECIMAL(18,2)` | `NOT NULL` | 交易金额 |
| `fee` | `DECIMAL(18,2)` | `DEFAULT 0` | 交易费用 |
| `transaction_date` | `TIMESTAMP` | `NOT NULL` | 交易日期 |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

**索引**：
- `CREATE INDEX idx_transactions_portfolio_id ON transactions(portfolio_id);`
- `CREATE INDEX idx_transactions_asset_id ON transactions(asset_id);`
- `CREATE INDEX idx_transactions_transaction_date ON transactions(transaction_date);`

### 2.6 现金流水表 (cash_flows)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 流水ID |
| `portfolio_id` | `INTEGER` | `NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE` | 组合ID |
| `type` | `VARCHAR(20)` | `NOT NULL` | 流水类型（存入/取出/分红/利息等） |
| `amount` | `DECIMAL(18,2)` | `NOT NULL` | 金额 |
| `description` | `TEXT` | | 描述 |
| `transaction_date` | `TIMESTAMP` | `NOT NULL` | 交易日期 |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

**索引**：
- `CREATE INDEX idx_cash_flows_portfolio_id ON cash_flows(portfolio_id);`
- `CREATE INDEX idx_cash_flows_transaction_date ON cash_flows(transaction_date);`

### 2.7 市场数据表 (market_data)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 数据ID |
| `asset_id` | `INTEGER` | `NOT NULL REFERENCES assets(id) ON DELETE CASCADE` | 资产ID |
| `date` | `DATE` | `NOT NULL` | 日期 |
| `open` | `DECIMAL(18,4)` | `NOT NULL` | 开盘价 |
| `high` | `DECIMAL(18,4)` | `NOT NULL` | 最高价 |
| `low` | `DECIMAL(18,4)` | `NOT NULL` | 最低价 |
| `close` | `DECIMAL(18,4)` | `NOT NULL` | 收盘价 |
| `volume` | `DECIMAL(20,2)` | `NOT NULL` | 成交量 |
| `amount` | `DECIMAL(20,2)` | `NOT NULL` | 成交额 |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

**索引**：
- `CREATE INDEX idx_market_data_asset_id ON market_data(asset_id);`
- `CREATE INDEX idx_market_data_date ON market_data(date);`
- `CREATE UNIQUE INDEX idx_market_data_asset_date ON market_data(asset_id, date);`

### 2.8 投资组合财务状态表 (portfolio_finances)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 财务记录ID |
| `portfolio_id` | `INTEGER` | `NOT NULL UNIQUE REFERENCES portfolios(id) ON DELETE CASCADE` | 组合ID（每个组合唯一） |
| `cash_balance` | `DECIMAL(18,2)` | `NOT NULL DEFAULT 0` | 现金余额 |
| `total_asset` | `DECIMAL(18,2)` | `NOT NULL DEFAULT 0` | 总资产 |
| `liability` | `DECIMAL(18,2)` | `NOT NULL DEFAULT 0` | 负债金额 |
| `net_asset` | `DECIMAL(18,2)` | `NOT NULL DEFAULT 0` | 净资产 |
| `cost_basis` | `DECIMAL(18,2)` | `NOT NULL DEFAULT 0` | 成本基础 |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 更新时间 |

**说明**：
- 投资组合财务状态表存储组合的实时财务指标
- 总资产 = 现金余额 + Σ(持仓数量 × 当前价格)
- 负债 = |现金余额|（当现金为负时）
- 净资产 = 总资产 - 负债

**索引**：
- `CREATE UNIQUE INDEX idx_portfolio_finances_portfolio_id ON portfolio_finances(portfolio_id);`

### 2.9 投资组合财务历史记录表 (portfolio_finance_history)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 历史记录ID |
| `finance_id` | `INTEGER` | `NOT NULL REFERENCES portfolio_finances(id) ON DELETE CASCADE` | 财务记录ID |
| `record_date` | `TIMESTAMP` | `NOT NULL` | 记录日期 |
| `cash_balance` | `DECIMAL(18,2)` | `NOT NULL` | 现金余额 |
| `total_asset` | `DECIMAL(18,2)` | `NOT NULL` | 总资产 |
| `liability` | `DECIMAL(18,2)` | `NOT NULL` | 负债金额 |
| `net_asset` | `DECIMAL(18,2)` | `NOT NULL` | 净资产 |
| `cost_basis` | `DECIMAL(18,2)` | `NOT NULL` | 成本基础 |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

**索引**：
- `CREATE INDEX idx_portfolio_finance_history_finance_id ON portfolio_finance_history(finance_id);`
- `CREATE INDEX idx_portfolio_finance_history_record_date ON portfolio_finance_history(record_date);`

### 2.10 持仓变动记录表 (holding_changes)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 变动记录ID |
| `finance_id` | `INTEGER` | `NOT NULL REFERENCES portfolio_finances(id) ON DELETE CASCADE` | 财务记录ID |
| `holding_id` | `INTEGER` | `REFERENCES holdings(id)` | 持仓ID |
| `asset_id` | `INTEGER` | `NOT NULL REFERENCES assets(id)` | 资产ID |
| `asset_code` | `VARCHAR(20)` | `NOT NULL` | 资产代码 |
| `asset_name` | `VARCHAR(100)` | `NOT NULL` | 资产名称 |
| `change_type` | `VARCHAR(20)` | `NOT NULL` | 变动类型（buy/sell/adjust） |
| `quantity_before` | `DECIMAL(18,4)` | `NOT NULL` | 变动前数量 |
| `quantity_after` | `DECIMAL(18,4)` | `NOT NULL` | 变动后数量 |
| `price` | `DECIMAL(18,4)` | `NOT NULL` | 交易价格 |
| `amount` | `DECIMAL(18,2)` | `NOT NULL` | 交易金额 |
| `total_asset_before` | `DECIMAL(18,2)` | `NOT NULL` | 变动前总资产 |
| `total_asset_after` | `DECIMAL(18,2)` | `NOT NULL` | 变动后总资产 |
| `net_asset_before` | `DECIMAL(18,2)` | `NOT NULL` | 变动前净资产 |
| `net_asset_after` | `DECIMAL(18,2)` | `NOT NULL` | 变动后净资产 |
| `transaction_id` | `INTEGER` | `REFERENCES transactions(id)` | 关联交易ID |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

**索引**：
- `CREATE INDEX idx_holding_changes_finance_id ON holding_changes(finance_id);`
- `CREATE INDEX idx_holding_changes_asset_id ON holding_changes(asset_id);`

## 3. 数据关系图

```mermaid
erDiagram
    USER ||--o{ PORTFOLIO : has
    PORTFOLIO ||--o{ HOLDING : contains
    PORTFOLIO ||--o{ TRANSACTION : has
    PORTFOLIO ||--o{ CASH_FLOW : has
    PORTFOLIO ||--|| PORTFOLIO_FINANCE : has
    PORTFOLIO_FINANCE ||--o{ PORTFOLIO_FINANCE_HISTORY : has
    PORTFOLIO_FINANCE ||--o{ HOLDING_CHANGE : has
    ASSET ||--o{ HOLDING : is_held_in
    ASSET ||--o{ TRANSACTION : is_traded
    ASSET ||--o{ MARKET_DATA : has_history

    USER {
        INTEGER id
        VARCHAR username
        VARCHAR email
        VARCHAR password_hash
        VARCHAR name
        VARCHAR role
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    PORTFOLIO {
        INTEGER id
        INTEGER user_id
        VARCHAR name
        TEXT description
        VARCHAR benchmark
        VARCHAR risk_level
        BOOLEAN is_default
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    ASSET {
        INTEGER id
        VARCHAR code
        VARCHAR name
        VARCHAR type          -- stock/fund/bond/cash
        VARCHAR market
        VARCHAR industry
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    HOLDING {
        INTEGER id
        INTEGER portfolio_id
        INTEGER asset_id
        DECIMAL quantity
        DECIMAL cost_price
        DECIMAL current_price
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    TRANSACTION {
        INTEGER id
        INTEGER portfolio_id
        INTEGER asset_id
        VARCHAR type
        DECIMAL quantity
        DECIMAL price
        DECIMAL amount
        DECIMAL fee
        TIMESTAMP transaction_date
        TIMESTAMP created_at
    }

    CASH_FLOW {
        INTEGER id
        INTEGER portfolio_id
        VARCHAR type
        DECIMAL amount
        TEXT description
        TIMESTAMP transaction_date
        TIMESTAMP created_at
    }

    MARKET_DATA {
        INTEGER id
        INTEGER asset_id
        DATE date
        DECIMAL open
        DECIMAL high
        DECIMAL low
        DECIMAL close
        DECIMAL volume
        DECIMAL amount
        TIMESTAMP created_at
    }
```

## 数据关系说明

### 用户-投资组合关系
- 一个用户可以拥有多个投资组合（1:N）
- 每个投资组合必须且仅能有一个默认组合（通过 is_default 字段标识）

### 投资组合-资产关系（通过持仓表关联）
- 一个投资组合可以持有0到n个资产（1:N）
- 一个资产可以被多个投资组合持有（N:N，通过 holdings 表实现）
- 资产类型支持：股票(stock)、基金(fund)、债券(bond)、现金(cash)

### 关系遍历示例
```
获取用户的所有资产：
1. 用户 -> 投资组合 (portfolios)
2. 投资组合 -> 持仓 (holdings)
3. 持仓 -> 资产 (assets)
```

## 4. 数据模型详细设计

### 4.1 用户模型

**功能**：存储用户信息，包括登录凭证和个人信息。

**关系**：
- 一个用户可以拥有多个投资组合（一对多关系）。

**约束**：
- 用户名和邮箱必须唯一。
- 密码必须加密存储。
- 角色默认为'user'。

### 4.2 投资组合模型

**功能**：存储投资组合的基本信息，如名称、描述、基准和风险等级。

**关系**：
- 一个投资组合属于一个用户（多对一关系）。
- 一个投资组合可以包含多个持仓（一对多关系）。
- 一个投资组合可以有多个交易记录（一对多关系）。
- 一个投资组合可以有多个现金流水（一对多关系）。

**约束**：
- 必须属于某个用户。
- 必须指定业绩基准和风险等级。

### 4.3 资产模型

**功能**：存储资产的基本信息，如代码、名称、类型、市场和行业。

**关系**：
- 一个资产可以被多个投资组合持有（一对多关系）。
- 一个资产可以有多个交易记录（一对多关系）。
- 一个资产可以有多个市场数据记录（一对多关系）。

**约束**：
- 资产代码必须唯一。
- 必须指定资产类型和市场。

### 4.4 持仓模型

**功能**：存储投资组合的资产持仓信息，包括数量、成本价和当前价格。

**关系**：
- 一个持仓属于一个投资组合（多对一关系）。
- 一个持仓对应一个资产（多对一关系）。

**约束**：
- 一个投资组合对同一个资产只能有一个持仓记录。
- 持仓数量和价格必须大于0。

### 4.5 交易记录模型

**功能**：存储投资组合的交易记录，包括买入和卖出操作。

**关系**：
- 一个交易记录属于一个投资组合（多对一关系）。
- 一个交易记录对应一个资产（多对一关系）。

**约束**：
- 交易类型只能是'买入'或'卖出'。
- 交易数量和价格必须大于0。
- 交易金额必须等于数量乘以价格。

### 4.6 现金流水模型

**功能**：存储投资组合的现金流动记录，如存入、取出、分红和利息等。

**关系**：
- 一个现金流水属于一个投资组合（多对一关系）。

**约束**：
- 流水类型必须是预定义的类型之一。
- 金额必须大于0。

### 4.7 市场数据模型

**功能**：存储资产的历史市场数据，包括开盘价、最高价、最低价、收盘价、成交量和成交额。

**关系**：
- 一个市场数据记录对应一个资产（多对一关系）。

**约束**：
- 一个资产在一天内只能有一条市场数据记录。
- 价格和成交量必须大于等于0。

## 5. 数据库初始化脚本

```sql
-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建投资组合表
CREATE TABLE IF NOT EXISTS portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    benchmark VARCHAR(50) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 创建资产表
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    market VARCHAR(50) NOT NULL,
    industry VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建持仓表
CREATE TABLE IF NOT EXISTS holdings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    asset_id INTEGER NOT NULL,
    quantity DECIMAL(18,4) NOT NULL,
    cost_price DECIMAL(18,4) NOT NULL,
    current_price DECIMAL(18,4) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES assets(id),
    UNIQUE(portfolio_id, asset_id)
);

-- 创建交易记录表
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    asset_id INTEGER NOT NULL,
    type VARCHAR(10) NOT NULL,
    quantity DECIMAL(18,4) NOT NULL,
    price DECIMAL(18,4) NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    fee DECIMAL(18,2) DEFAULT 0,
    transaction_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

-- 创建现金流水表
CREATE TABLE IF NOT EXISTS cash_flows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    type VARCHAR(20) NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    description TEXT,
    transaction_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
);

-- 创建市场数据表
CREATE TABLE IF NOT EXISTS market_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(18,4) NOT NULL,
    high DECIMAL(18,4) NOT NULL,
    low DECIMAL(18,4) NOT NULL,
    close DECIMAL(18,4) NOT NULL,
    volume DECIMAL(20,2) NOT NULL,
    amount DECIMAL(20,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE,
    UNIQUE(asset_id, date)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_portfolios_user_id ON portfolios(user_id);
CREATE INDEX IF NOT EXISTS idx_assets_code ON assets(code);
CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(type);
CREATE INDEX IF NOT EXISTS idx_assets_market ON assets(market);
CREATE INDEX IF NOT EXISTS idx_assets_industry ON assets(industry);
CREATE INDEX IF NOT EXISTS idx_holdings_portfolio_id ON holdings(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_holdings_asset_id ON holdings(asset_id);
CREATE INDEX IF NOT EXISTS idx_transactions_portfolio_id ON transactions(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_transactions_asset_id ON transactions(asset_id);
CREATE INDEX IF NOT EXISTS idx_transactions_transaction_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_cash_flows_portfolio_id ON cash_flows(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_cash_flows_transaction_date ON cash_flows(transaction_date);
CREATE INDEX IF NOT EXISTS idx_market_data_asset_id ON market_data(asset_id);
CREATE INDEX IF NOT EXISTS idx_market_data_date ON market_data(date);

-- 插入示例数据
-- 插入用户数据
INSERT INTO users (username, email, password_hash, name, role) VALUES
('admin', 'admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '管理员', 'admin'),
('user1', 'user1@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '用户一', 'user');

-- 插入资产数据
INSERT INTO assets (code, name, type, market, industry) VALUES
('600519.SH', '贵州茅台', '股票', 'A股', '白酒'),
('000858.SZ', '五粮液', '股票', 'A股', '白酒'),
('601318.SH', '中国平安', '股票', 'A股', '保险'),
('600036.SH', '招商银行', '股票', 'A股', '银行'),
('000333.SZ', '美的集团', '股票', 'A股', '家电'),
('510300.SH', '沪深300ETF', '基金', 'A股', 'ETF'),
('510500.SH', '中证500ETF', '基金', 'A股', 'ETF'),
('000001.SH', '上证指数', '指数', 'A股', '指数'),
('399001.SZ', '深证成指', '指数', 'A股', '指数'),
('399006.SZ', '创业板指', '指数', 'A股', '指数');

-- 插入投资组合数据
INSERT INTO portfolios (user_id, name, description, benchmark, risk_level) VALUES
(1, '我的投资组合', '个人投资组合', '沪深300', 'medium'),
(1, '保守型组合', '低风险投资组合', '中证500', 'low'),
(2, '进取型组合', '高风险投资组合', '创业板指', 'high');

-- 插入持仓数据
INSERT INTO holdings (portfolio_id, asset_id, quantity, cost_price, current_price) VALUES
(1, 1, 10, 1800.00, 1850.00),
(1, 2, 100, 160.00, 165.00),
(1, 3, 500, 45.00, 46.00),
(2, 4, 1000, 35.00, 36.00),
(2, 6, 10000, 4.50, 4.60),
(3, 5, 200, 50.00, 52.00),
(3, 7, 5000, 6.00, 6.20);

-- 插入交易记录数据
INSERT INTO transactions (portfolio_id, asset_id, type, quantity, price, amount, fee, transaction_date) VALUES
(1, 1, '买入', 10, 1800.00, 18000.00, 18.00, '2026-01-01 10:00:00'),
(1, 2, '买入', 100, 160.00, 16000.00, 16.00, '2026-01-02 11:00:00'),
(1, 3, '买入', 500, 45.00, 22500.00, 22.50, '2026-01-03 14:00:00'),
(2, 4, '买入', 1000, 35.00, 35000.00, 35.00, '2026-01-04 09:30:00'),
(2, 6, '买入', 10000, 4.50, 45000.00, 45.00, '2026-01-05 10:00:00'),
(3, 5, '买入', 200, 50.00, 10000.00, 10.00, '2026-01-06 11:30:00'),
(3, 7, '买入', 5000, 6.00, 30000.00, 30.00, '2026-01-07 13:00:00');

-- 插入现金流水数据
INSERT INTO cash_flows (portfolio_id, type, amount, description, transaction_date) VALUES
(1, '存入', 100000.00, '初始投资', '2026-01-01 09:00:00'),
(2, '存入', 80000.00, '初始投资', '2026-01-01 09:00:00'),
(3, '存入', 120000.00, '初始投资', '2026-01-01 09:00:00'),
(1, '取出', 10000.00, '应急资金', '2026-02-01 10:00:00'),
(2, '分红', 500.00, '股票分红', '2026-02-15 15:00:00'),
(3, '利息', 100.00, '现金利息', '2026-02-28 16:00:00');

-- 插入市场数据
INSERT INTO market_data (asset_id, date, open, high, low, close, volume, amount) VALUES
(1, '2026-03-01', 1800.00, 1860.00, 1790.00, 1850.00, 1000000, 1850000000),
(2, '2026-03-01', 160.00, 166.00, 159.00, 165.00, 2000000, 330000000),
(3, '2026-03-01', 45.00, 46.50, 44.50, 46.00, 5000000, 230000000),
(4, '2026-03-01', 35.00, 36.50, 34.50, 36.00, 8000000, 288000000),
(5, '2026-03-01', 50.00, 52.50, 49.50, 52.00, 3000000, 156000000),
(6, '2026-03-01', 4.50, 4.65, 4.45, 4.60, 20000000, 92000000),
(7, '2026-03-01', 6.00, 6.30, 5.90, 6.20, 15000000, 93000000),
(8, '2026-03-01', 4000.00, 4050.00, 3990.00, 4020.00, 100000000, 402000000000),
(9, '2026-03-01', 13000.00, 13200.00, 12950.00, 13100.00, 80000000, 1048000000000),
(10, '2026-03-01', 2500.00, 2550.00, 2490.00, 2520.00, 60000000, 151200000000);
```

## 6. 数据库优化策略

### 6.1 索引优化
- **合理创建索引**：为频繁查询的字段创建索引，如用户表的username和email字段，投资组合表的user_id字段等。
- **复合索引**：对于经常一起查询的字段，创建复合索引，如持仓表的portfolio_id和asset_id字段。
- **唯一索引**：对于需要唯一性约束的字段，如资产代码和市场数据表的资产ID与日期组合，创建唯一索引。

### 6.2 查询优化
- **避免全表扫描**：使用索引字段进行查询，避免全表扫描。
- **使用JOIN优化**：合理使用JOIN操作，减少多次查询。
- **分页查询**：对于大数据量的查询，使用分页减少数据传输量。
- **预编译语句**：使用预编译语句，提高查询性能。

### 6.3 数据维护
- **定期清理**：定期清理过期的市场数据，避免数据库过大。
- **备份策略**：定期备份数据库，确保数据安全。
- **事务管理**：使用事务确保数据一致性，尤其是在涉及多个表的操作时。

### 6.4 性能监控
- **查询分析**：定期分析慢查询，优化查询语句。
- **数据库状态**：监控数据库的状态，如连接数、缓存使用情况等。
- **存储空间**：监控数据库的存储空间使用情况，及时清理不必要的数据。

## 7. 数据库安全

### 7.1 访问控制
- **最小权限原则**：数据库用户只授予必要的权限。
- **密码管理**：使用强密码，定期更换。
- **访问日志**：记录数据库访问日志，便于审计。

### 7.2 数据保护
- **数据加密**：敏感数据如密码使用加密存储。
- **备份加密**：备份数据进行加密存储。
- **传输加密**：使用SSL/TLS加密数据库传输。

### 7.3 防止SQL注入
- **参数化查询**：使用参数化查询，避免SQL注入攻击。
- **输入验证**：对用户输入进行严格验证。
- **ORM使用**：使用ORM框架，减少直接SQL操作。

## 8. 结论

本数据库schema设计详细描述了投资组合管理系统的数据库结构，包括表结构、字段定义、索引设计、关系映射和初始化脚本。该设计基于SQLite数据库，通过合理的表结构和索引设计，确保系统能够高效地存储和查询数据。

数据库设计考虑了系统的功能需求，包括用户管理、投资组合管理、资产管理、持仓管理、交易记录管理、现金流水管理和市场数据管理等核心功能。通过外键关联和约束，确保数据的一致性和完整性。

该数据库设计将作为系统开发的基础，为投资组合管理系统提供可靠的数据存储支持。