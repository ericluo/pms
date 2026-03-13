# 持仓快照设计文档

## 设计理念

基于附图中的"持仓调整"界面，采用**变动触发式持仓快照**的设计方案：

### 核心概念

1. **HoldingChange** - 单笔持仓变动记录
   - 对应一笔 Transaction
   - 记录单个 Asset 的变动
   - 用于审计和追溯

2. **HoldingSnapshot** - 持仓快照（变动触发）
   - **只在发生持仓变动时创建**
   - 记录变动发生时的**完整持仓列表**（JSON 格式）
   - 每个投资组合 + 变动日期 = 一条记录
   - 用于快速查询历史持仓状态
   - **不是每天都创建，只在有调仓操作的日期创建**

## 数据模型

### 1. HoldingChange（现有表增强）

```python
class HoldingChange(Base):
    __tablename__ = 'holding_changes'
    
    id = Column(Integer, primary_key=True)
    finance_id = Column(Integer, ForeignKey('portfolio_finances.id'))
    holding_id = Column(Integer, ForeignKey('holdings.id'))
    asset_id = Column(Integer, ForeignKey('assets.id'))
    asset_code = Column(String(20))
    asset_name = Column(String(100))
    change_type = Column(String(20))  # buy/sell/adjust/cash_dividend
    quantity_before = Column(Numeric(18, 4))
    quantity_after = Column(Numeric(18, 4))
    quantity_change = Column(Numeric(18, 4))  # 变动数量（正负值）
    price = Column(Numeric(18, 4))
    amount = Column(Numeric(18, 2))
    currency = Column(String(10), default='CNY')  # 交易币种
    exchange_rate = Column(Numeric(10, 6), default=1.0)  # 汇率
    fair_price = Column(Numeric(18, 4))  # 公允价格
    valuation_price = Column(Numeric(18, 4))  # 估值净价
    cost_price = Column(Numeric(18, 4))  # 成本价格
    weight = Column(Numeric(10, 6))  # 权重%
    dividend_date = Column(DateTime)  # 收息日期
    reason = Column(String(200))  # 变动原因
    total_asset_before = Column(Numeric(18, 2))
    total_asset_after = Column(Numeric(18, 2))
    net_asset_before = Column(Numeric(18, 2))
    net_asset_after = Column(Numeric(18, 2))
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    created_at = Column(DateTime)
```

**说明**：
- 每笔交易（Transaction）产生一条 HoldingChange
- 记录变动前后的状态
- 包含丰富的价格信息（公允价格、估值净价、成本价格）
- 支持多币种（currency + exchange_rate）

### 2. HoldingSnapshot（新增表）

```python
class HoldingSnapshot(Base):
    __tablename__ = 'holding_snapshots'
    
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    snapshot_date = Column(DateTime, index=True)  # 快照日期
    holdings_data = Column(String)  # JSON 格式的持仓数据
    total_market_value = Column(Numeric(18, 2))  # 总市值
    cash_balance = Column(Numeric(18, 2))  # 现金余额
    created_at = Column(DateTime)
```

**JSON 数据结构**：
```json
[
  {
    "asset_id": 1,
    "asset_code": "000001",
    "asset_name": "平安银行",
    "quantity": 1000,
    "cost_price": 10.5,
    "current_price": 11.2,
    "market_value": 11200,
    "weight": 1.05
  },
  {
    "asset_id": 2,
    "asset_code": "300760.SZ",
    "asset_name": "迈瑞医疗",
    "quantity": 200,
    "cost_price": 290.6,
    "current_price": 187.11,
    "market_value": 37422,
    "weight": 3.5
  }
]
```

**说明**：
- **只在发生持仓变动的日期创建**（不是每天都有）
- holdings_data 字段存储完整的持仓列表（JSON 格式）
- 包含权重（weight）字段（动态计算后存储）
- 包含总市值和现金余额
- **触发时机**：用户进行调仓操作并保存时

## API 设计

### 1. 获取快照日期列表

```
GET /api/portfolios/:portfolio_id/snapshot-dates
```

**响应**：
```json
[
  { "date": "2026-02-02" },
  { "date": "2026-01-20" },
  { "date": "2026-01-15" }
]
```

### 2. 获取指定日期的持仓快照

```
GET /api/portfolios/:portfolio_id/snapshots?date=2026-02-02
```

**响应**：
```json
{
  "date": "2026-02-02",
  "portfolio_id": 1,
  "total_market_value": 1000000,
  "holdings": [
    {
      "asset_id": 1,
      "asset_code": "000001",
      "asset_name": "平安银行",
      "quantity": 1000,
      "cost_price": 10.5,
      "current_price": 10.5,
      "market_value": 10500,
      "weight": 1.05
    }
  ]
}
```

### 3. 创建/更新持仓快照

```
POST /api/portfolios/:portfolio_id/snapshots?date=2026-02-02
```

**说明**：
- 基于当前 holdings 表创建快照
- 如果该日期已有快照，则更新
- 自动计算权重和总市值

**响应**：
```json
{
  "success": true,
  "snapshot_date": "2026-02-02",
  "holdings_count": 11,
  "total_market_value": 1000000
}
```

### 4. 删除持仓快照

```
DELETE /api/portfolios/:portfolio_id/snapshots/2026-02-02
```

## 使用场景

### 场景 1：查看历史某天的持仓

```
1. 用户选择日期：2026-02-02
2. 查询快照：GET /api/portfolios/1/snapshots?date=2026-02-02
3. 返回该日期的完整持仓列表
```

### 场景 2：调仓操作（触发快照创建）

```
1. 用户调整持仓（通过 Transaction 或直接修改 Holding）
2. 系统自动创建 HoldingChange 记录
3. 用户点击"保存"按钮
4. 调用 POST /api/portfolios/1/snapshots?date=2026-02-02
5. **创建该日期的持仓快照（因为发生了变动）**
6. 如果该日期已有快照，则更新
```

### 场景 3：删除错误的调仓

```
1. 用户发现 2026-02-02 的调仓有误
2. 删除快照：DELETE /api/portfolios/1/snapshots/2026-02-02
3. 修改 Transaction 或 Holding
4. 重新创建快照
```

## 权重计算

权重**不存储在 Holding 表中**，而是在查询时动态计算：

```python
def calculate_portfolio_weights(holdings):
    total_value = sum(h.quantity * h.current_price for h in holdings)
    
    for holding in holdings:
        market_value = holding.quantity * holding.current_price
        weight = (market_value / total_value) * 100 if total_value > 0 else 0
        
        yield {
            **holding,
            'market_value': market_value,
            'weight': weight
        }
```

**优点**：
- 数据一致性最好（权重永远是最新的）
- 不需要在每次交易时更新所有持仓的权重
- 代码逻辑简单清晰

## 数据库迁移

```sql
-- 创建持仓快照表
CREATE TABLE holding_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    snapshot_date DATETIME NOT NULL,
    holdings_data TEXT NOT NULL,  -- JSON 格式
    total_market_value DECIMAL(18, 2) NOT NULL,
    cash_balance DECIMAL(18, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_snapshots_portfolio_date ON holding_snapshots(portfolio_id, snapshot_date);

-- 增强 holding_changes 表
ALTER TABLE holding_changes ADD COLUMN quantity_change DECIMAL(18,4);
ALTER TABLE holding_changes ADD COLUMN currency VARCHAR(10) DEFAULT 'CNY';
ALTER TABLE holding_changes ADD COLUMN exchange_rate DECIMAL(10,6) DEFAULT 1.0;
ALTER TABLE holding_changes ADD COLUMN fair_price DECIMAL(18,4);
ALTER TABLE holding_changes ADD COLUMN valuation_price DECIMAL(18,4);
ALTER TABLE holding_changes ADD COLUMN cost_price DECIMAL(18,4);
ALTER TABLE holding_changes ADD COLUMN weight DECIMAL(10,6);
ALTER TABLE holding_changes ADD COLUMN dividend_date DATETIME;
ALTER TABLE holding_changes ADD COLUMN reason VARCHAR(200);
```

## 与附图的对应关系

### 左侧：日期列表
- 数据来源：`holding_snapshots.snapshot_date`
- 显示所有有快照的日期
- 支持删除（删除快照）

### 右侧：持仓明细表格
- 数据来源：`holding_snapshots.holdings_data`（JSON 解析）
- 显示字段：
  - 证券代码、证券简称
  - 交易币种（currency）
  - 公允价格（fair_price）
  - 估值净价（valuation_price）
  - 持仓数量（quantity）
  - 持仓市值（market_value）
  - 权重%（weight）
  - 成本价格（cost_price）
  - 汇率（exchange_rate）
  - 收息日期（dividend_date）

### 操作列：增/减按钮
- 触发 Transaction 创建
- 同时记录 HoldingChange
- 保存时更新快照

## 优势分析

### 1. 查询性能
- ✅ 快照查询：直接读取 JSON，无需复杂计算
- ✅ 日期列表：DISTINCT 查询，速度快
- ✅ 权重动态计算：只在创建快照时计算一次
- ✅ **存储优化**：只在变动时创建，无冗余数据

### 2. 数据一致性
- ✅ 快照数据：固定时点的状态，不会变化
- ✅ 变动记录：HoldingChange 完整记录每笔变动
- ✅ 实时持仓：Holdings 表保持最新状态
- ✅ **按需创建**：只在变动时保存，避免重复

### 3. 可维护性
- ✅ 结构简单：两个核心表
- ✅ 职责清晰：HoldingChange 记录变动，Snapshot 记录状态
- ✅ 易于扩展：可以添加更多快照字段
- ✅ **业务清晰**：快照 = 发生过调仓的日期

## 相关文件

- 数据模型：[`app/models/portfolio_finance.py`](file:///e:/workspace/pms/app/models/portfolio_finance.py)
- Service 层：[`app/services/holding.py`](file:///e:/workspace/pms/app/services/holding.py)
- API 接口：[`app/api/holding.py`](file:///e:/workspace/pms/app/api/holding.py)
- 迁移脚本：[`migrate_holding_changes.py`](file:///e:/workspace/pms/migrate_holding_changes.py)
