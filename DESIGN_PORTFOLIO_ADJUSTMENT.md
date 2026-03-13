# 持仓变动功能设计文档（基于 holding_changes）

## 1. 功能概述

基于参考附图设计一个完整的持仓变动管理系统，**复用现有的 `holding_changes` 表**，支持：
- 按日期管理持仓调整
- 增加/减少持仓数量
- 现金存取、资产划转
- 文件导入导出
- 等权重调仓
- 多币种支持

### 核心设计理念

**不复用 `portfolio_adjustments` 表**，而是：
1. 增强 `holding_changes` 表字段（增加币种、汇率、公允价格等）
2. 通过 `holding_changes` 的 `adjustment_date` 字段按日期组织
3. 通过 replay `holding_changes` 重建历史持仓
4. 删除调整时自动重建持仓状态

## 2. 数据库设计

### 2.1 增强的 holding_changes 表

**现有字段保持不变，新增以下字段**：

```sql
ALTER TABLE holding_changes ADD COLUMN quantity_change DECIMAL(18,4);  -- 变动数量（正负值）
ALTER TABLE holding_changes ADD COLUMN currency VARCHAR(10) DEFAULT 'CNY';  -- 交易币种
ALTER TABLE holding_changes ADD COLUMN exchange_rate DECIMAL(10,6) DEFAULT 1.0;  -- 汇率
ALTER TABLE holding_changes ADD COLUMN fair_price DECIMAL(18,4);  -- 公允价格
ALTER TABLE holding_changes ADD COLUMN valuation_price DECIMAL(18,4);  -- 估值净价
ALTER TABLE holding_changes ADD COLUMN cost_price DECIMAL(18,4);  -- 成本价格（全价）
ALTER TABLE holding_changes ADD COLUMN weight DECIMAL(10,6);  -- 权重%
ALTER TABLE holding_changes ADD COLUMN dividend_date DATETIME;  -- 收息日期
ALTER TABLE holding_changes ADD COLUMN reason VARCHAR(200);  -- 变动原因
ALTER TABLE holding_changes ADD COLUMN adjustment_date DATE;  -- 调仓日期（索引）
```

**说明**：
- `adjustment_date`: 用于按日期查询和组织调整记录
- `quantity_change`: 明确记录变动数量（正数表示增加，负数表示减少）
- `currency` / `exchange_rate`: 支持多币种交易
- `fair_price` / `valuation_price` / `cost_price`: 支持附图中的价格字段
- `weight`: 记录持仓权重
- `dividend_date`: 收息日期
- `reason`: 调整原因说明

## 3. 界面设计

### 2.1 界面布局

```
┌─────────────────────────────────────────────────────────────────────┐
│  调仓日期：[2026-02-02]  [现金存取] [交易录入] [资产划转] [导入]    │
│                                                                      │
│  ┌──────────┬────────────────────────────────────────────────────┐  │
│  │ 日期列表 │  持仓明细表格                                      │  │
│  │          │                                                    │  │
│  │ 2026-03-13│  证券代码  证券简称  操作  公允价格  持仓数量... │  │
│  │ 2026-03-04│  1        CNY       增/减  1.0000   45415.64    │  │
│  │ 2026-02-27│  2        300760.SZ 增/减  187.1100  200.00      │  │
│  │ 2026-02-24│  ...                                            │  │
│  │ 2026-02-02│ ← 选中                                         │  │
│  │ 2026-01-29│                                                    │  │
│  │ ...      │                                                    │  │
│  └──────────┴────────────────────────────────────────────────────┘  │
│                                                   [保存] [取消]      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 功能区域

#### 左侧：调仓日期列表
- 显示所有有持仓变动的日期
- 支持点击选择日期
- 支持删除指定日期的调仓记录
- 按日期倒序排列

#### 右侧：持仓明细表格
展示字段：
- 证券代码、证券简称
- 交易币种（CNY/HKD/USD 等）
- 公允价格、估值净价
- 持仓数量、持仓市值
- 权重%、成本价格 (全价)
- 汇率、收息日期

#### 顶部工具栏
- **现金存取**: 记录现金存入/取出
- **交易录入**: 手动录入交易
- **资产划转**: 资产在不同组合间划转
- **交易流水文件导入**: 从 Excel/CSV 导入交易数据
- **持仓文件导入**: 从 Excel/CSV 导入持仓数据
- **等权重调仓**: 一键调仓使所有资产等权重
- **币种选择**: 设置基础币种

## 3. 数据库设计

### 3.1 持仓调整记录表 (portfolio_adjustments)

```sql
CREATE TABLE portfolio_adjustments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    adjustment_date DATE NOT NULL,  -- 调仓日期
    adjustment_type VARCHAR(20) NOT NULL,  
        -- 'adjustment': 持仓调整
        -- 'cash_flow': 现金存取
        -- 'transfer': 资产划转
        -- 'rebalance': 再平衡
    description TEXT,  -- 调整说明
    total_amount DECIMAL(18,2),  -- 调整总金额
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE,
    UNIQUE(portfolio_id, adjustment_date)
);

CREATE INDEX idx_adjustments_portfolio_date ON portfolio_adjustments(portfolio_id, adjustment_date);
```

### 3.2 持仓变动明细表 (holding_adjustments)

```sql
CREATE TABLE holding_adjustments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adjustment_id INTEGER NOT NULL,
    holding_id INTEGER,  -- 可为空（新增持仓时）
    asset_id INTEGER NOT NULL,
    adjustment_action VARCHAR(10) NOT NULL,  -- 'increase' / 'decrease'
    quantity_before DECIMAL(18,4) NOT NULL,
    quantity_after DECIMAL(18,4) NOT NULL,
    quantity_change DECIMAL(18,4) NOT NULL,  -- 正数为增，负数为减
    price DECIMAL(18,4) NOT NULL,  -- 参考价格
    amount DECIMAL(18,2) NOT NULL,  -- 变动金额 = quantity_change * price
    currency VARCHAR(10) DEFAULT 'CNY',  -- 交易币种
    exchange_rate DECIMAL(10,6) DEFAULT 1.0,  -- 汇率
    reason VARCHAR(100),  -- 变动原因
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (adjustment_id) REFERENCES portfolio_adjustments(id) ON DELETE CASCADE,
    FOREIGN KEY (holding_id) REFERENCES holdings(id),
    FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE INDEX idx_holding_adjustments_adjustment ON holding_adjustments(adjustment_id);
CREATE INDEX idx_holding_adjustments_asset ON holding_adjustments(asset_id);
```

### 3.3 持仓快照表 (holding_snapshots)

```sql
CREATE TABLE holding_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    asset_id INTEGER NOT NULL,
    snapshot_date DATE NOT NULL,
    quantity DECIMAL(18,4) NOT NULL,
    cost_price DECIMAL(18,4) NOT NULL,
    current_price DECIMAL(18,4) NOT NULL,
    market_value DECIMAL(18,2) NOT NULL,
    weight DECIMAL(10,6),  -- 权重百分比
    currency VARCHAR(10) DEFAULT 'CNY',
    exchange_rate DECIMAL(10,6) DEFAULT 1.0,
    dividend_date DATE,  -- 收息日期
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES assets(id),
    UNIQUE(portfolio_id, asset_id, snapshot_date)
);

CREATE INDEX idx_snapshots_portfolio_date ON holding_snapshots(portfolio_id, snapshot_date);
```

### 3.4 投资组合配置表 (portfolio_configs)

```sql
CREATE TABLE portfolio_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL UNIQUE,
    base_currency VARCHAR(10) DEFAULT 'CNY',
    default_exchange_rate DECIMAL(10,6) DEFAULT 1.0,
    last_valuation_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
);
```

## 4. 核心架构

### 4.1 数据流

```
用户操作
  ↓
API 接口 (holding_adjustment.py)
  ↓
Service 层 (holding_adjustment.py)
  ↓
创建/更新 holding_changes 记录
  ↓
自动更新 holdings 表（实时持仓）
  ↓
查询时 replay holding_changes 重建历史持仓
```

### 4.2 历史持仓重建算法

```python
def get_holdings_on_date(portfolio_id, target_date):
    # 1. 获取目标日期之前的所有 holding_changes
    changes = query.filter(
        HoldingChange.adjustment_date <= target_date
    ).order_by(HoldingChange.adjustment_date)
    
    # 2. 按资产分组，依次应用变动
    holdings_map = {}
    for change in changes:
        asset_id = change.asset_id
        holdings_map[asset_id] = {
            'quantity': change.quantity_after,
            'cost_price': change.cost_price,
            'current_price': change.fair_price,
            # ... 其他字段
        }
    
    # 3. 返回最终状态
    return holdings_map.values()
```

## 5. API 接口设计

### 5.1 获取调仓日期列表

```typescript
/**
 * GET /api/portfolios/:portfolio_id/adjustment-dates
 * 获取所有有持仓变动的日期列表
 */
interface GetAdjustmentDatesResponse {
  dates: Array<{
    date: string;  // YYYY-MM-DD
    adjustment_count: number;  // 变动笔数
    total_market_value: number;  // 总市值
    created_at: string;
  }>;
}
```

### 4.2 获取指定日期的持仓明细

```typescript
/**
 * GET /api/portfolios/:portfolio_id/holdings?date=2026-02-02
 * 获取指定日期的持仓明细（支持快照或动态计算）
 */
interface GetHoldingsResponse {
  date: string;
  portfolio_id: number;
  total_market_value: number;
  holdings: Array<{
    id: number;
    asset_id: number;
    asset_code: string;
    asset_name: string;
    currency: string;
    fair_price: number;
    valuation_price: number;
    quantity: number;
    market_value: number;
    weight: number;
    cost_price: number;
    exchange_rate: number;
    dividend_date?: string;
  }>;
}
```

### 4.3 创建调仓记录

```typescript
/**
 * POST /api/portfolios/:portfolio_id/adjustments
 * 创建或更新调仓记录
 */
interface CreateAdjustmentRequest {
  adjustment_date: string;
  adjustment_type: 'adjustment' | 'cash_flow' | 'transfer' | 'rebalance';
  description?: string;
  holdings: Array<{
    asset_id: number;
    adjustment_action: 'increase' | 'decrease';
    quantity_change: number;  // 正数=增加，负数=减少
    price: number;
    currency?: string;
    exchange_rate?: number;
    reason?: string;
  }>;
}

interface CreateAdjustmentResponse {
  adjustment_id: number;
  success: boolean;
  updated_holdings: number[];
}
```

### 4.4 删除调仓记录

```typescript
/**
 * DELETE /api/portfolios/:portfolio_id/adjustment-dates/:date
 * 删除指定日期的所有调仓记录
 */
interface DeleteAdjustmentResponse {
  success: boolean;
  deleted_count: number;
  message: string;
}
```

### 4.5 导入调仓数据

```typescript
/**
 * POST /api/portfolios/:portfolio_id/adjustments/import
 * 从 Excel/CSV 文件导入调仓数据
 */
interface ImportAdjustmentRequest {
  adjustment_date: string;
  file: File;  // Excel/CSV 文件
  import_type: 'transaction' | 'holding';
}

interface ImportAdjustmentResponse {
  success: boolean;
  imported_count: number;
  failed_count: number;
  errors: Array<{
    row: number;
    asset_code?: string;
    message: string;
  }>;
  warnings: Array<{
    row: number;
    message: string;
  }>;
}
```

### 5.6 等权重调仓

```typescript
/**
 * POST /api/portfolios/:portfolio_id/adjustments/rebalance
 * 执行等权重调仓
 */
interface RebalanceRequest {
  target_date: string;
  assets?: number[];  // 可选，指定要调仓的资产列表
  tolerance?: number;  // 容忍度，默认 0.01 (1%)
}

interface RebalanceResponse {
  success: boolean;
  adjustments: Array<{
    asset_id: number;
    asset_code: string;
    current_weight: number;
    target_weight: number;
    quantity_change: number;
    estimated_amount: number;
  }>;
  total_adjustment_amount: number;
}
```

## 6. 前端组件设计

### 5.1 组件结构

```
src/views/portfolio/
├── PortfolioAdjustment.vue       # 主页面组件
├── components/
│   ├── AdjustmentDatesPanel.vue  # 左侧日期列表面板
│   ├── HoldingAdjustmentTable.vue # 右侧持仓明细表格
│   ├── AdjustmentDialog.vue      # 调整对话框
│   ├── CashFlowDialog.vue        # 现金存取对话框
│   ├── TransferDialog.vue        # 资产划转对话框
│   ├── ImportDialog.vue          # 导入对话框
│   └── RebalanceDialog.vue       # 等权重调仓对话框
└── composables/
    └── usePortfolioAdjustment.ts # 组合式函数（业务逻辑）
```

### 5.2 核心状态管理

```typescript
// src/views/portfolio/composables/usePortfolioAdjustment.ts

interface UsePortfolioAdjustmentReturn {
  // 状态
  loading: Ref<boolean>;
  selectedDate: Ref<string>;
  adjustmentDates: Ref<string[]>;
  holdings: Ref<HoldingDetail[]>;
  
  // 方法
  loadAdjustmentDates: () => Promise<void>;
  selectDate: (date: string) => Promise<void>;
  deleteDate: (date: string) => Promise<void>;
  adjustHolding: (holding: HoldingDetail, action: 'increase' | 'decrease') => void;
  submitAdjustment: (data: AdjustmentForm) => Promise<void>;
  importAdjustments: (file: File, date: string) => Promise<ImportResult>;
  rebalance: (options: RebalanceOptions) => Promise<void>;
}

export function usePortfolioAdjustment(portfolioId: number) {
  const loading = ref(false);
  const selectedDate = ref(formatDate(new Date()));
  const adjustmentDates = ref<string[]>([]);
  const holdings = ref<HoldingDetail[]>([]);
  
  // 加载调仓日期列表
  const loadAdjustmentDates = async () => {
    loading.value = true;
    try {
      const response = await api.get(`/portfolios/${portfolioId}/adjustment-dates`);
      adjustmentDates.value = response.dates.map(d => d.date);
    } finally {
      loading.value = false;
    }
  };
  
  // 选择日期并加载持仓
  const selectDate = async (date: string) => {
    loading.value = true;
    try {
      selectedDate.value = date;
      const response = await api.get(
        `/portfolios/${portfolioId}/holdings`,
        { params: { date } }
      );
      holdings.value = response.holdings;
    } finally {
      loading.value = false;
    }
  };
  
  // 删除日期
  const deleteDate = async (date: string) => {
    try {
      await api.delete(`/portfolios/${portfolioId}/adjustment-dates/${date}`);
      await loadAdjustmentDates();
      ElMessage.success('删除成功');
    } catch (error) {
      ElMessage.error('删除失败');
    }
  };
  
  return {
    loading,
    selectedDate,
    adjustmentDates,
    holdings,
    loadAdjustmentDates,
    selectDate,
    deleteDate,
    // ... 其他方法
  };
}
```

### 5.3 主页面组件

```vue
<!-- src/views/portfolio/PortfolioAdjustment.vue -->
<template>
  <div class="portfolio-adjustment">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <el-date-picker
        v-model="selectedDate"
        type="date"
        placeholder="选择调仓日期"
        @change="selectDate"
      />
      
      <el-button @click="openCashFlowDialog">现金存取</el-button>
      <el-button @click="openTransactionDialog">交易录入</el-button>
      <el-button @click="openTransferDialog">资产划转</el-button>
      <el-button @click="openImportDialog">交易流水文件导入</el-button>
      <el-button @click="openHoldingImportDialog">持仓文件导入</el-button>
      <el-button @click="openRebalanceDialog">等权重调仓</el-button>
      
      <el-select v-model="currency" placeholder="币种">
        <el-option label="CNY" value="CNY" />
        <el-option label="HKD" value="HKD" />
        <el-option label="USD" value="USD" />
      </el-select>
    </div>
    
    <!-- 主体内容 -->
    <div class="content">
      <!-- 左侧日期列表 -->
      <AdjustmentDatesPanel
        :dates="adjustmentDates"
        :selected-date="selectedDate"
        @select="selectDate"
        @delete="deleteDate"
      />
      
      <!-- 右侧持仓表格 -->
      <HoldingAdjustmentTable
        :holdings="holdings"
        :loading="loading"
        @adjust="adjustHolding"
      />
    </div>
    
    <!-- 底部按钮 -->
    <div class="footer">
      <el-button @click="saveAdjustments">保存</el-button>
      <el-button @click="cancel">取消</el-button>
    </div>
    
    <!-- 对话框组件 -->
    <AdjustmentDialog v-model="dialogVisible" :data="selectedHolding" />
    <CashFlowDialog v-model="cashFlowDialogVisible" />
    <TransferDialog v-model="transferDialogVisible" />
    <ImportDialog v-model="importDialogVisible" />
    <RebalanceDialog v-model="rebalanceDialogVisible" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { usePortfolioAdjustment } from './composables/usePortfolioAdjustment';
import AdjustmentDatesPanel from './components/AdjustmentDatesPanel.vue';
import HoldingAdjustmentTable from './components/HoldingAdjustmentTable.vue';
import AdjustmentDialog from './components/AdjustmentDialog.vue';
import CashFlowDialog from './components/CashFlowDialog.vue';
import TransferDialog from './components/TransferDialog.vue';
import ImportDialog from './components/ImportDialog.vue';
import RebalanceDialog from './components/RebalanceDialog.vue';

const route = useRoute();
const portfolioId = Number(route.params.id);

const {
  loading,
  selectedDate,
  adjustmentDates,
  holdings,
  loadAdjustmentDates,
  selectDate,
  deleteDate,
  adjustHolding,
} = usePortfolioAdjustment(portfolioId);

const dialogVisible = ref(false);
const cashFlowDialogVisible = ref(false);
const transferDialogVisible = ref(false);
const importDialogVisible = ref(false);
const rebalanceDialogVisible = ref(false);
const currency = ref('CNY');
const selectedHolding = ref(null);

// 初始化
onMounted(() => {
  loadAdjustmentDates();
});

// 打开调整对话框
const adjustHolding = (holding, action) => {
  selectedHolding.value = holding;
  dialogVisible.value = true;
};

// 保存
const saveAdjustments = async () => {
  // TODO: 实现保存逻辑
};

// 取消
const cancel = () => {
  // TODO: 实现取消逻辑
};
</script>

<style scoped>
.portfolio-adjustment {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.toolbar {
  display: flex;
  gap: 8px;
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
}

.content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 16px;
  border-top: 1px solid #e4e7ed;
}
</style>
```

## 7. 业务流程

### 7.1 持仓调整流程

```
1. 用户选择调仓日期
   ↓
2. 系统加载该日期的持仓快照（或动态计算）
   ↓
3. 用户点击"增"或"减"按钮
   ↓
4. 弹出调整对话框，输入调整信息
   ↓
5. 系统计算调整后的数量和金额
   ↓
6. 用户确认提交
   ↓
7. 系统创建 holding_adjustments 记录
   ↓
8. 系统更新 holdings 表
   ↓
9. 系统创建/更新 holding_snapshots
   ↓
10. 刷新持仓列表显示
```

### 7.2 文件导入流程

```
1. 用户点击"交易流水文件导入"
   ↓
2. 选择 Excel/CSV 文件
   ↓
3. 系统解析文件内容
   ↓
4. 数据验证（资产代码、数量、价格等）
   ↓
5. 显示预览和错误信息
   ↓
6. 用户确认导入
   ↓
7. 批量创建交易记录和持仓变动
   ↓
8. 更新持仓和快照
   ↓
9. 显示导入结果（成功/失败数量）
```

### 7.3 等权重调仓流程

```
1. 用户点击"等权重调仓"
   ↓
2. 系统计算当前各资产权重
   ↓
3. 计算目标权重（100% / 资产数量）
   ↓
4. 计算需要调整的金额和数量
   ↓
5. 显示调仓方案预览
   ↓
6. 用户确认执行
   ↓
7. 批量创建调整记录
   ↓
8. 更新持仓和快照
   ↓
9. 显示调仓结果
```

## 8. 数据验证规则

### 8.1 持仓调整验证

```typescript
const adjustmentValidationRules = {
  // 数量必须大于 0
  quantity_change: {
    required: true,
    type: 'number',
    min: 0,
    message: '调整数量必须大于 0'
  },
  
  // 价格必须大于 0
  price: {
    required: true,
    type: 'number',
    min: 0,
    message: '价格必须大于 0'
  },
  
  // 减少时不能超过当前持仓
  validateReduce: (holding, change) => {
    if (holding.quantity < change) {
      return '减少数量不能超过当前持仓';
    }
    return true;
  }
};
```

### 8.2 导入文件验证

```typescript
const importValidationRules = {
  // 必填字段
  required_fields: ['证券代码', '数量', '价格'],
  
  // 证券代码格式
  asset_code_pattern: /^[0-9]{6}\.[A-Z]{2,3}$|^[A-Z]{1,4}$/,
  
  // 数值精度
  quantity_precision: 4,
  price_precision: 4,
  amount_precision: 2
};
```

## 9. 性能优化

### 8.1 查询优化

```sql
-- 使用覆盖索引减少回表
CREATE INDEX idx_holdings_snapshot_covering 
ON holding_snapshots(portfolio_id, snapshot_date, asset_id)
INCLUDE (quantity, cost_price, current_price, market_value);

-- 分区表（大数据量时）
-- 按日期范围分区，提高历史查询性能
```

### 8.2 缓存策略

```typescript
// 使用 Vue Query 缓存持仓数据
const queryClient = useQueryClient();

// 预加载相邻日期的数据
const prefetchAdjacentDates = async (selectedDate: string) => {
  const prevDate = previousTradingDay(selectedDate);
  const nextDate = nextTradingDay(selectedDate);
  
  queryClient.prefetchQuery({
    queryKey: ['holdings', portfolioId, prevDate],
    queryFn: () => fetchHoldings(portfolioId, prevDate)
  });
  
  queryClient.prefetchQuery({
    queryKey: ['holdings', portfolioId, nextDate],
    queryFn: () => fetchHoldings(portfolioId, nextDate)
  });
};
```

## 10. 错误处理

### 10.1 常见错误场景

```typescript
const errorMessages = {
  DATE_NOT_FOUND: '该日期没有持仓记录',
  HOLDING_NOT_FOUND: '持仓不存在',
  INSUFFICIENT_HOLDING: '持仓数量不足',
  INVALID_PRICE: '价格无效',
  DUPLICATE_ADJUSTMENT: '该日期已有调整记录',
  IMPORT_FORMAT_ERROR: '文件格式错误，请上传 Excel 或 CSV 文件',
  ASSET_NOT_FOUND: '资产代码不存在'
};
```

### 10.2 异常处理

```typescript
try {
  await submitAdjustment(data);
} catch (error) {
  if (error.code === 'INSUFFICIENT_HOLDING') {
    ElMessage.error('持仓数量不足，无法完成调整');
  } else if (error.code === 'DUPLICATE_ADJUSTMENT') {
    ElMessage.warning('该日期已有调整记录，请先删除或修改');
  } else {
    ElMessage.error('操作失败，请稍后重试');
  }
}
```

## 11. 测试计划

### 11.1 单元测试

```typescript
describe('PortfolioAdjustment', () => {
  test('should load adjustment dates', async () => {
    // 测试加载日期列表
  });
  
  test('should calculate quantity change correctly', () => {
    // 测试数量计算
  });
  
  test('should validate reduce action', () => {
    // 测试减少验证
  });
});
```

### 11.2 集成测试

```typescript
describe('Adjustment Flow', () => {
  test('complete adjustment flow', async () => {
    // 1. 选择日期
    // 2. 调整持仓
    // 3. 保存
    // 4. 验证结果
  });
});
```

### 11.3 E2E 测试

```typescript
describe('E2E Tests', () => {
  test('import holdings from Excel', async () => {
    // 1. 上传文件
    // 2. 预览数据
    // 3. 确认导入
    // 4. 验证导入结果
  });
});
```

## 12. 部署计划

### 12.1 数据库迁移

```sql
-- 1. 增强 holding_changes 表字段
ALTER TABLE holding_changes ADD COLUMN quantity_change DECIMAL(18,4);
ALTER TABLE holding_changes ADD COLUMN currency VARCHAR(10) DEFAULT 'CNY';
ALTER TABLE holding_changes ADD COLUMN exchange_rate DECIMAL(10,6) DEFAULT 1.0;
ALTER TABLE holding_changes ADD COLUMN fair_price DECIMAL(18,4);
ALTER TABLE holding_changes ADD COLUMN valuation_price DECIMAL(18,4);
ALTER TABLE holding_changes ADD COLUMN cost_price DECIMAL(18,4);
ALTER TABLE holding_changes ADD COLUMN weight DECIMAL(10,6);
ALTER TABLE holding_changes ADD COLUMN dividend_date DATETIME;
ALTER TABLE holding_changes ADD COLUMN reason VARCHAR(200);
ALTER TABLE holding_changes ADD COLUMN adjustment_date DATE;

-- 2. 创建索引
CREATE INDEX idx_holding_changes_adjustment_date ON holding_changes(adjustment_date);

-- 3. 验证数据完整性
```

### 12.2 后端部署

```bash
# 1. 更新代码
git pull origin main

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行数据库迁移
alembic upgrade head

# 4. 重启服务
systemctl restart pms-backend
```

### 12.3 前端部署

```bash
# 1. 构建
npm run build

# 2. 部署到 CDN/Nginx
cp -r dist/* /var/www/pms/

# 3. 清除缓存
nginx -s reload
```

## 13. 后续优化方向

1. **智能调仓建议**: 基于历史数据和市场情况提供调仓建议
2. **批量操作**: 支持同时调整多个持仓
3. **调仓模板**: 保存常用的调仓方案
4. **调仓日志**: 记录所有调仓操作的审计日志
5. **权限控制**: 不同用户对调仓操作的权限管理
6. **移动端适配**: 支持移动端进行调仓操作
