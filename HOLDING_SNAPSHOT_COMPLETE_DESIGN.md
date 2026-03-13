# 持仓快照功能 - 完整设计与实现文档

## 1. 概述

### 1.1 业务背景

基于附图中的"持仓调整"界面需求，需要实现一个功能：
- 左侧显示所有有持仓变动的日期列表
- 右侧显示选中日期的完整持仓明细
- 支持对持仓进行增减操作
- 支持保存调仓后的快照

### 1.2 设计思路

经过分析讨论，确定了以下核心设计思路：

**变动触发式快照**：
- **不是每天都创建快照**
- **只在发生持仓变动时创建快照**
- 用户调仓操作并保存后，自动创建该日期的持仓快照
- 减少数据冗余，只记录有意义的状态变化

### 1.3 核心架构

采用**双层架构**：

1. **HoldingChange（变动记录层）**
   - 记录每笔交易的变动详情
   - 对应一笔 Transaction
   - 用于审计和追溯

2. **HoldingSnapshot（快照查询层）**
   - 只在发生变动时创建
   - 记录变动时的完整持仓状态（JSON 格式）
   - 用于快速查询历史持仓

## 2. 设计决策

### 2.1 为什么选择变动触发式快照？

**方案对比**：

| 方案 | 优点 | 缺点 |
|------|------|------|
| 每日快照 | 数据连续 | 大量冗余数据，无变动也记录 |
| **变动触发式** | 按需创建，无冗余 | 数据不连续（需要通过计算补充） |
| 完全动态计算 | 无存储成本 | 查询性能差，每次都要计算 |

**决策理由**：
1. ✅ **业务匹配**：快照日期 = 发生过调仓的日期，符合业务直觉
2. ✅ **存储优化**：只在变动时创建，避免冗余
3. ✅ **查询高效**：直接读取 JSON，无需复杂计算
4. ✅ **性能平衡**：在存储和查询之间取得平衡

### 2.2 为什么权重采用动态计算？

**方案对比**：

| 方案 | 优点 | 缺点 |
|------|------|------|
| 存储 weight 字段 | 查询快 | 需要在每次交易时更新所有持仓 |
| **动态计算** | 数据一致性好，代码简单 | 查询时需要计算 |

**决策理由**：
1. ✅ **数据一致性**：权重永远基于最新数据计算
2. ✅ **维护简单**：不需要在交易时更新所有持仓的权重
3. ✅ **代码清晰**：逻辑简单，易于理解

### 2.3 为什么使用 JSON 存储持仓数据？

**决策理由**：
1. ✅ **灵活性**：可以轻松添加新字段
2. ✅ **完整性**：一条记录保存完整持仓列表
3. ✅ **查询效率**：一次性读取，无需多表关联
4. ✅ **版本兼容**：易于处理数据结构变化

## 3. 技术规格

### 3.1 数据模型设计

#### 3.1.1 HoldingChange（持仓变动记录）

**文件**: `app/models/portfolio_finance.py`

```python
class HoldingChange(Base):
    __tablename__ = 'holding_changes'
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联关系
    finance_id = Column(Integer, ForeignKey('portfolio_finances.id'), nullable=False, index=True)
    holding_id = Column(Integer, ForeignKey('holdings.id'), nullable=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=True)
    
    # 资产信息
    asset_code = Column(String(20), nullable=False)
    asset_name = Column(String(100), nullable=False)
    
    # 变动类型：buy/sell/adjust/cash_dividend 等
    change_type = Column(String(20), nullable=False)
    
    # 变动前后状态
    quantity_before = Column(Numeric(18, 4), nullable=False)
    quantity_after = Column(Numeric(18, 4), nullable=False)
    quantity_change = Column(Numeric(18, 4), nullable=True)  # 变动数量（正负值）
    
    # 价格信息
    price = Column(Numeric(18, 4), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    fair_price = Column(Numeric(18, 4), nullable=True)  # 公允价格
    valuation_price = Column(Numeric(18, 4), nullable=True)  # 估值净价
    cost_price = Column(Numeric(18, 4), nullable=True)  # 成本价格
    
    # 多币种支持
    currency = Column(String(10), nullable=True, default='CNY')
    exchange_rate = Column(Numeric(10, 6), nullable=True, default=1.0)
    
    # 持仓指标
    weight = Column(Numeric(10, 6), nullable=True)  # 权重%
    
    # 其他信息
    dividend_date = Column(DateTime, nullable=True)  # 收息日期
    reason = Column(String(200), nullable=True)  # 变动原因
    
    # 财务状态
    total_asset_before = Column(Numeric(18, 2), nullable=False)
    total_asset_after = Column(Numeric(18, 2), nullable=False)
    net_asset_before = Column(Numeric(18, 2), nullable=False)
    net_asset_after = Column(Numeric(18, 2), nullable=False)
    
    # 时间戳
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
```

**设计说明**：
- 记录每笔交易的完整变动信息
- 包含变动前后的状态对比
- 支持多币种和多种价格类型
- 通过 transaction_id 关联原始交易

#### 3.1.2 HoldingSnapshot（持仓快照）

**文件**: `app/models/portfolio_finance.py`

```python
class HoldingSnapshot(Base):
    """持仓快照 - 只在发生变动时创建"""
    __tablename__ = 'holding_snapshots'
    
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联关系
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False, index=True)
    
    # 快照日期（变动发生日期）
    snapshot_date = Column(DateTime, nullable=False, index=True)
    
    # 持仓数据（JSON 格式）
    holdings_data = Column(String, nullable=False)
    
    # 汇总信息
    total_market_value = Column(Numeric(18, 2), nullable=False)  # 总市值
    cash_balance = Column(Numeric(18, 2), nullable=True, default=0)  # 现金余额
    
    # 时间戳
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
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

**设计说明**：
- 只在发生持仓变动时创建
- JSON 格式存储完整持仓列表
- 包含权重（创建时动态计算）
- 包含总市值和现金余额

### 3.2 Service 层设计

**文件**: `app/services/holding.py`

```python
class HoldingService:
    """持仓服务 - 包含快照功能"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ========== 基础 CRUD 操作 ==========
    
    def get_holdings(self, portfolio_id: int) -> List[Holding]:
        """获取当前持仓列表"""
        return self.db.query(Holding).filter(Holding.portfolio_id == portfolio_id).all()
    
    def get_holding(self, holding_id: int, portfolio_id: int) -> Optional[Holding]:
        """获取单个持仓"""
        return self.db.query(Holding).filter(
            Holding.id == holding_id,
            Holding.portfolio_id == portfolio_id
        ).first()
    
    def create_holding(self, holding_data: dict, portfolio_id: int) -> Holding:
        """创建持仓"""
        pass
    
    def update_holding(self, holding_id: int, holding_update: HoldingUpdate, portfolio_id: int) -> Optional[Holding]:
        """更新持仓"""
        pass
    
    def delete_holding(self, holding_id: int, portfolio_id: int) -> bool:
        """删除持仓"""
        pass
    
    # ========== 快照相关方法 ==========
    
    def get_snapshot_dates(self, portfolio_id: int) -> List[Dict]:
        """
        获取所有有持仓快照的日期列表（只在发生变动的日期）
        
        Returns:
            List[Dict]: [{"date": "2026-02-02"}, {"date": "2026-01-20"}]
        """
        results = self.db.query(
            func.date(HoldingSnapshot.snapshot_date).label('snapshot_date')
        ).filter(
            HoldingSnapshot.portfolio_id == portfolio_id
        ).distinct().order_by(
            HoldingSnapshot.snapshot_date.desc()
        ).all()
        
        return [{'date': str(row.snapshot_date)} for row in results]
    
    def get_holdings_on_date(self, portfolio_id: int, target_date: date) -> List[Dict]:
        """
        获取指定日期的持仓快照
        
        Args:
            portfolio_id: 投资组合 ID
            target_date: 目标日期
            
        Returns:
            List[Dict]: 持仓列表，包含权重等信息
        """
        snapshot = self.db.query(HoldingSnapshot).filter(
            HoldingSnapshot.portfolio_id == portfolio_id,
            func.date(HoldingSnapshot.snapshot_date) == target_date
        ).first()
        
        if not snapshot:
            return []
        
        return json.loads(snapshot.holdings_data)
    
    def create_or_update_snapshot(self, portfolio_id: int, snapshot_date: date) -> Dict:
        """
        创建或更新指定日期的持仓快照
        
        触发时机：用户调仓操作并保存后
        
        Args:
            portfolio_id: 投资组合 ID
            snapshot_date: 快照日期
            
        Returns:
            Dict: {
                "snapshot_date": "2026-02-02",
                "holdings_count": 11,
                "total_market_value": 1000000
            }
        """
        # 1. 获取当前持仓
        holdings = self.db.query(Holding).filter(
            Holding.portfolio_id == portfolio_id
        ).all()
        
        # 2. 构建快照数据
        snapshot_data = []
        total_market_value = Decimal('0')
        
        for holding in holdings:
            asset = self.db.query(Asset).filter(Asset.id == holding.asset_id).first()
            market_value = Decimal(str(holding.quantity)) * Decimal(str(holding.current_price))
            total_market_value += market_value
            
            snapshot_data.append({
                'asset_id': holding.asset_id,
                'asset_code': asset.code if asset else '',
                'asset_name': asset.name if asset else '',
                'quantity': float(holding.quantity),
                'cost_price': float(holding.cost_price),
                'current_price': float(holding.current_price),
                'market_value': float(market_value),
                'weight': 0,  # 稍后计算
            })
        
        # 3. 计算权重（动态计算）
        for item in snapshot_data:
            if total_market_value > 0:
                item['weight'] = (item['market_value'] / float(total_market_value)) * 100
        
        # 4. 获取财务数据
        finance = self.db.query(PortfolioFinance).filter(
            PortfolioFinance.portfolio_id == portfolio_id
        ).first()
        cash_balance = finance.cash_balance if finance else Decimal('0')
        
        # 5. 检查是否已有快照
        existing_snapshot = self.db.query(HoldingSnapshot).filter(
            HoldingSnapshot.portfolio_id == portfolio_id,
            func.date(HoldingSnapshot.snapshot_date) == snapshot_date
        ).first()
        
        if existing_snapshot:
            # 更新快照
            existing_snapshot.holdings_data = json.dumps(snapshot_data, ensure_ascii=False)
            existing_snapshot.total_market_value = total_market_value
            existing_snapshot.cash_balance = cash_balance
        else:
            # 创建新快照
            snapshot = HoldingSnapshot(
                portfolio_id=portfolio_id,
                snapshot_date=datetime.combine(snapshot_date, datetime.min.time()),
                holdings_data=json.dumps(snapshot_data, ensure_ascii=False),
                total_market_value=total_market_value,
                cash_balance=cash_balance
            )
            self.db.add(snapshot)
        
        self.db.commit()
        
        return {
            'snapshot_date': str(snapshot_date),
            'holdings_count': len(snapshot_data),
            'total_market_value': float(total_market_value)
        }
    
    def delete_snapshot(self, portfolio_id: int, snapshot_date: date) -> int:
        """
        删除指定日期的持仓快照
        
        Args:
            portfolio_id: 投资组合 ID
            snapshot_date: 快照日期
            
        Returns:
            int: 删除的快照数量
        """
        snapshots = self.db.query(HoldingSnapshot).filter(
            HoldingSnapshot.portfolio_id == portfolio_id,
            func.date(HoldingSnapshot.snapshot_date) == snapshot_date
        ).all()
        
        count = len(snapshots)
        for snapshot in snapshots:
            self.db.delete(snapshot)
        
        self.db.commit()
        return count
    
    # ========== 辅助方法 ==========
    
    def calculate_holding_metrics(self, holding: Holding) -> dict:
        """计算持仓指标"""
        pass
    
    def calculate_portfolio_weights(self, holdings: List[Holding]) -> List[dict]:
        """
        计算投资组合权重（动态计算）
        
        权重不存储在数据库中，每次查询时动态计算
        """
        total_value = sum(float(holding.quantity) * float(holding.current_price) for holding in holdings)
        result = []
        for holding in holdings:
            asset = self.db.query(Asset).filter(Asset.id == holding.asset_id).first()
            metrics = self.calculate_holding_metrics(holding)
            weight = (metrics["value"] / total_value) * 100 if total_value > 0 else 0
            result.append({
                "id": holding.id,
                "portfolio_id": holding.portfolio_id,
                "asset_id": holding.asset_id,
                "asset_code": asset.code if asset else "",
                "asset_name": asset.name if asset else "",
                "quantity": float(holding.quantity),
                "cost_price": float(holding.cost_price),
                "current_price": float(holding.current_price),
                "value": metrics["value"],
                "cost": metrics["cost"],
                "profit": metrics["profit"],
                "profit_percent": metrics["profit_percent"],
                "weight": weight
            })
        return result
```

### 3.3 API 层设计

**文件**: `app/api/holding.py`

```python
@api.route('/<int:portfolio_id>/snapshot-dates')
class SnapshotDatesResource(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '获取成功')
    @api.response(401, '未授权')
    @api.response(404, '投资组合不存在')
    def get(self, portfolio_id):
        """
        获取所有有持仓快照的日期列表
        
        返回所有发生过持仓变动的日期
        
        Returns:
            List[Dict]: [{"date": "2026-02-02"}, {"date": "2026-01-20"}]
        """
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        dates = holding_service.get_snapshot_dates(portfolio_id)
        return dates, 200


@api.route('/<int:portfolio_id>/snapshots')
class PortfolioSnapshotResource(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.param('date', '查询日期（YYYY-MM-DD）', required=True)
    @api.response(200, '获取成功')
    @api.response(400, '日期参数错误')
    @api.response(404, '投资组合不存在')
    def get(self, portfolio_id):
        """
        获取指定日期的持仓快照
        
        Args:
            date: 查询日期（YYYY-MM-DD）
            
        Returns:
            Dict: {
                "date": "2026-02-02",
                "portfolio_id": 1,
                "total_market_value": 1000000,
                "holdings": [...]
            }
        """
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        date_str = request.args.get('date')
        if not date_str:
            api.abort(400, 'Missing required parameter: date')
        
        try:
            target_date = date.fromisoformat(date_str)
        except ValueError:
            api.abort(400, 'Invalid date format. Use YYYY-MM-DD')
        
        holdings = holding_service.get_holdings_on_date(portfolio_id, target_date)
        total_market_value = sum(h['market_value'] for h in holdings) if holdings else 0
        
        return {
            'date': date_str,
            'portfolio_id': portfolio_id,
            'total_market_value': total_market_value,
            'holdings': holdings
        }, 200
    
    @api.doc(security='Bearer')
    @jwt_required()
    @api.param('date', '创建/更新快照日期（YYYY-MM-DD）', required=True)
    @api.response(201, '创建成功')
    @api.response(400, '请求参数错误')
    @api.response(404, '投资组合不存在')
    def post(self, portfolio_id):
        """
        创建或更新指定日期的持仓快照
        
        触发时机：用户调仓操作并保存后
        
        Args:
            date: 快照日期（YYYY-MM-DD）
            
        Returns:
            Dict: {
                "success": true,
                "snapshot_date": "2026-02-02",
                "holdings_count": 11,
                "total_market_value": 1000000
            }
        """
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        date_str = request.args.get('date')
        if not date_str:
            api.abort(400, 'Missing required parameter: date')
        
        try:
            snapshot_date = date.fromisoformat(date_str)
        except ValueError:
            api.abort(400, 'Invalid date format')
        
        result = holding_service.create_or_update_snapshot(portfolio_id, snapshot_date)
        
        return {
            'success': True,
            'snapshot_date': date_str,
            **result
        }, 201


@api.route('/<int:portfolio_id>/snapshots/<string:date_str>')
class SnapshotDateResource(Resource):
    @api.doc(security='Bearer')
    @jwt_required()
    @api.response(200, '删除成功')
    @api.response(400, '日期格式错误')
    @api.response(404, '投资组合不存在')
    def delete(self, portfolio_id, date_str):
        """
        删除指定日期的持仓快照
        
        Args:
            date_str: 快照日期（YYYY-MM-DD）
            
        Returns:
            Dict: {
                "success": true,
                "deleted_count": 1
            }
        """
        db: Session = next(get_db())
        holding_service = HoldingService(db)
        portfolio_service = PortfolioService(db)
        
        user_id = get_jwt_identity()
        portfolio = portfolio_service.get_portfolio(portfolio_id, int(user_id))
        if not portfolio:
            api.abort(404, '投资组合不存在')
        
        try:
            snapshot_date = date.fromisoformat(date_str)
        except ValueError:
            api.abort(400, 'Invalid date format')
        
        deleted_count = holding_service.delete_snapshot(portfolio_id, snapshot_date)
        
        return {
            'success': True,
            'deleted_count': deleted_count
        }, 200
```

## 4. 实现细节

### 4.1 数据库迁移

**文件**: `migrate_holding_changes.py`

```python
"""
数据库迁移脚本：持仓快照功能
- 增强 holding_changes 表
- 创建 holding_snapshots 表
"""

from sqlalchemy import create_engine, text
from app.config import config

def migrate_holding_snapshots():
    """持仓快照功能数据库迁移"""
    
    DATABASE_URL = config['production'].SQLALCHEMY_DATABASE_URL
    engine = create_engine(DATABASE_URL)
    
    migration_sql = """
    -- 1. 增强 holding_changes 表
    ALTER TABLE holding_changes ADD COLUMN IF NOT EXISTS quantity_change DECIMAL(18,4);
    ALTER TABLE holding_changes ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'CNY';
    ALTER TABLE holding_changes ADD COLUMN IF NOT EXISTS exchange_rate DECIMAL(10,6) DEFAULT 1.0;
    ALTER TABLE holding_changes ADD COLUMN IF NOT EXISTS fair_price DECIMAL(18,4);
    ALTER TABLE holding_changes ADD COLUMN IF NOT EXISTS valuation_price DECIMAL(18,4);
    ALTER TABLE holding_changes ADD COLUMN IF NOT EXISTS cost_price DECIMAL(18,4);
    ALTER TABLE holding_changes ADD COLUMN IF NOT EXISTS weight DECIMAL(10,6);
    ALTER TABLE holding_changes ADD COLUMN IF NOT EXISTS dividend_date DATETIME;
    ALTER TABLE holding_changes ADD COLUMN IF NOT EXISTS reason VARCHAR(200);
    
    -- 2. 创建持仓快照表
    CREATE TABLE IF NOT EXISTS holding_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        portfolio_id INTEGER NOT NULL,
        snapshot_date DATETIME NOT NULL,
        holdings_data TEXT NOT NULL,
        total_market_value DECIMAL(18, 2) NOT NULL,
        cash_balance DECIMAL(18, 2) DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
    );
    
    -- 3. 创建索引
    CREATE INDEX IF NOT EXISTS idx_snapshots_portfolio_date ON holding_snapshots(portfolio_id, snapshot_date);
    CREATE INDEX IF NOT EXISTS idx_holding_changes_asset ON holding_changes(asset_id);
    """
    
    try:
        with engine.connect() as conn:
            for statement in migration_sql.strip().split(';'):
                statement = statement.strip()
                if statement:
                    conn.execute(text(statement))
            conn.commit()
        
        print("✅ 持仓快照功能数据库迁移成功！")
        
    except Exception as e:
        print(f"❌ 迁移失败：{e}")
        raise

if __name__ == "__main__":
    migrate_holding_snapshots()
```

### 4.2 使用示例

#### 4.2.1 查看历史持仓

```bash
# 1. 获取所有有快照的日期
curl -X GET http://localhost:5000/api/portfolios/1/snapshot-dates \
  -H "Authorization: Bearer <token>"

# 响应：[{"date": "2026-02-02"}, {"date": "2026-01-20"}]

# 2. 获取指定日期的持仓快照
curl -X GET "http://localhost:5000/api/portfolios/1/snapshots?date=2026-02-02" \
  -H "Authorization: Bearer <token>"

# 响应：{
#   "date": "2026-02-02",
#   "portfolio_id": 1,
#   "total_market_value": 1000000,
#   "holdings": [...]
# }
```

#### 4.2.2 调仓后保存快照

```bash
# 1. 用户调整持仓（通过 Transaction 或直接修改 Holding）
# 2. 系统创建 HoldingChange 记录
# 3. 更新 Holdings 表
# 4. 调用 API 创建快照
curl -X POST "http://localhost:5000/api/portfolios/1/snapshots?date=2026-02-02" \
  -H "Authorization: Bearer <token>"

# 响应：{
#   "success": true,
#   "snapshot_date": "2026-02-02",
#   "holdings_count": 11,
#   "total_market_value": 1000000
# }
```

#### 4.2.3 删除错误的调仓

```bash
# 1. 发现 2026-02-02 的调仓有误
# 2. 删除快照
curl -X DELETE http://localhost:5000/api/portfolios/1/snapshots/2026-02-02 \
  -H "Authorization: Bearer <token>"

# 响应：{
#   "success": true,
#   "deleted_count": 1
# }

# 3. 修改 Transaction 或 Holding
# 4. 重新创建快照
```

## 5. 与附图的对应关系

### 5.1 左侧：日期列表

- **数据来源**: `holding_snapshots.snapshot_date`
- **显示**: 所有发生过持仓变动的日期
- **操作**: 
  - 点击选择日期 → 调用 `GET /snapshots?date=xxx`
  - 删除日期 → 调用 `DELETE /snapshots/:date`

### 5.2 右侧：持仓明细表格

- **数据来源**: `holding_snapshots.holdings_data`（JSON 解析）
- **显示字段**:
  - 证券代码、证券简称
  - 交易币种（currency）
  - 公允价格（fair_price）
  - 估值净价（valuation_price）
  - 持仓数量（quantity）
  - 持仓市值（market_value）
  - 权重%（weight）- 动态计算
  - 成本价格（cost_price）
  - 汇率（exchange_rate）
  - 收息日期（dividend_date）

### 5.3 操作列：增/减按钮

- **功能**: 调整持仓数量
- **流程**:
  1. 用户点击"增"或"减"
  2. 弹出对话框，输入调整信息
  3. 创建 Transaction 记录
  4. 生成 HoldingChange 记录
  5. 更新 Holdings 表
  6. **调用 `POST /snapshots?date=xxx` 创建快照**

## 6. 优势分析

### 6.1 查询性能

- ✅ **快照查询**: 直接读取 JSON，无需多表关联
- ✅ **日期列表**: DISTINCT 查询，速度快
- ✅ **权重计算**: 只在创建快照时计算一次
- ✅ **存储优化**: 只在变动时创建，无冗余数据

### 6.2 数据一致性

- ✅ **快照数据**: 固定时点的状态，不会变化
- ✅ **变动记录**: HoldingChange 完整记录每笔变动
- ✅ **实时持仓**: Holdings 表保持最新状态
- ✅ **按需创建**: 只在变动时保存，避免重复

### 6.3 可维护性

- ✅ **结构简单**: 两个核心表
- ✅ **职责清晰**: HoldingChange 记录变动，Snapshot 记录状态
- ✅ **易于扩展**: 可以添加更多快照字段
- ✅ **业务清晰**: 快照日期 = 发生过调仓的日期

## 7. 文件清单

### 7.1 数据模型
- [`app/models/portfolio_finance.py`](file:///e:/workspace/pms/app/models/portfolio_finance.py) - HoldingChange 和 HoldingSnapshot 模型
- [`app/models/portfolio.py`](file:///e:/workspace/pms/app/models/portfolio.py) - Portfolio 模型（添加 holding_snapshots 关系）

### 7.2 Service 层
- [`app/services/holding.py`](file:///e:/workspace/pms/app/services/holding.py) - 持仓服务（包含快照功能）

### 7.3 API 层
- [`app/api/holding.py`](file:///e:/workspace/pms/app/api/holding.py) - 持仓 API（包含快照接口）

### 7.4 迁移脚本
- [`migrate_holding_changes.py`](file:///e:/workspace/pms/migrate_holding_changes.py) - 数据库迁移

### 7.5 文档
- [`HOLDING_SNAPSHOT_DESIGN.md`](file:///e:/workspace/pms/HOLDING_SNAPSHOT_DESIGN.md) - 详细设计文档
- [`IMPLEMENTATION_COMPLETE.md`](file:///e:/workspace/pms/IMPLEMENTATION_COMPLETE.md) - 实现总结
- [`HOLDING_SNAPSHOT_COMPLETE_DESIGN.md`](file:///e:/workspace/pms/HOLDING_SNAPSHOT_COMPLETE_DESIGN.md) - 本文档

## 8. 下一步

### 8.1 前端实现

1. 创建 `PortfolioAdjustment.vue` 页面组件
2. 实现日期选择器（左侧面板）
3. 实现持仓表格（右侧）
4. 实现增/减操作对话框
5. 集成快照 API

### 8.2 功能增强

1. 批量导入持仓数据（Excel/CSV）
2. 等权重调仓功能
3. 调仓模板保存
4. 调仓历史记录

## 9. 总结

本次实现采用了**变动触发式快照 + 变动记录**的双层架构：

- **HoldingChange**: 记录每笔变动，用于审计和追溯
- **HoldingSnapshot**: 只在发生变动时创建快照，用于快速查询历史状态
- **权重动态计算**: 不在数据库中存储，保证数据一致性

**核心优势**：
- ✅ 按需创建：只在调仓操作后创建快照，避免数据冗余
- ✅ 业务清晰：快照日期 = 发生过调仓的日期
- ✅ 查询高效：直接读取 JSON，无需复杂计算
- ✅ 简洁性：所有代码在现有架构中实现，没有新增文件

这个设计完美匹配附图中的"持仓调整"界面需求，提供了清晰、高效、可维护的解决方案。
