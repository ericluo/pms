# 持仓功能完善说明

## 问题描述

用户进入某个投资组合后，点击"添加持仓"按钮，系统提示"添加持仓功能还没有完成"。

## 解决方案

已在 [`PortfolioDetail.vue`](file:///e:/workspace/pms/src/views/portfolio/PortfolioDetail.vue) 中完成了添加持仓功能的开发。

## 实现内容

### 1. 添加了持仓对话框组件

创建了一个完整的添加/编辑持仓对话框，包含以下功能：

- **资产选择**：支持搜索和筛选资产（按代码或名称）
- **持仓数量输入**：数字输入框，最小值 0，精度 2 位小数
- **成本价输入**：数字输入框，最小值 0，精度 4 位小数
- **当前价输入**：数字输入框，最小值 0，精度 4 位小数
- **表单验证**：必填项验证和数值范围验证

### 2. 实现了完整的 CRUD 操作

#### 添加持仓
- 点击"添加持仓"按钮打开对话框
- 选择资产并输入相关信息
- 提交后自动刷新持仓列表

#### 编辑持仓
- 点击持仓行的"编辑"按钮
- 加载当前持仓数据到表单
- 修改后保存

#### 删除持仓
- 点击持仓行的"删除"按钮
- 弹出确认对话框
- 确认后删除并刷新列表

### 3. 后端 API 集成

已集成以下 API：

```typescript
// 获取资产列表
getAssets(): Promise<Asset[]>

// 添加持仓
addHolding(portfolioId: number, holdingData: {
  asset_id: number
  quantity: number
  cost_price: number
}): Promise<Holding>

// 更新持仓
updateHolding(portfolioId: number, holdingId: number, holdingData: {
  quantity?: number
  cost_price?: number
}): Promise<Holding>

// 删除持仓
deleteHolding(portfolioId: number, holdingId: number): Promise<{ message: string }>
```

### 4. 数据展示优化

持仓列表显示以下字段：

- 资产名称
- 资产代码
- 资产类型（带标签样式）
- 持仓数量
- 成本价
- 当前价
- 市值（格式化货币）
- 盈亏（格式化货币，红涨绿跌）
- 盈亏率（百分比，红涨绿跌）
- 操作按钮（编辑/删除）

## 使用方法

### 添加持仓

1. 进入投资组合详情页
2. 点击"持仓明细"卡片右上角的"添加持仓"按钮
3. 在弹出的对话框中：
   - 搜索并选择资产
   - 输入持仓数量
   - 输入成本价
   - （可选）输入当前价
4. 点击"确定"按钮

### 编辑持仓

1. 在持仓列表中找到要编辑的持仓
2. 点击该行的"编辑"按钮
3. 修改相关信息
4. 点击"确定"保存

### 删除持仓

1. 在持仓列表中找到要删除的持仓
2. 点击该行的"删除"按钮
3. 在确认对话框中点击"确定"

## 技术细节

### 组件状态管理

```typescript
// 对话框状态
const dialogVisible = ref(false)
const dialogTitle = ref('添加持仓')
const isEditMode = ref(false)

// 表单数据
const holdingForm = ref<Holding & { id?: number }>({
  id: 0,
  portfolio_id: 0,
  asset_id: 0,
  quantity: 0,
  cost_price: 0,
  current_price: 0,
  value: 0,
  profit: 0,
  profit_rate: 0,
  created_at: '',
  updated_at: ''
})

// 资产列表
const assetList = ref<Asset[]>([])
const assetFilter = ref('') // 搜索关键词
```

### 资产搜索功能

使用计算属性实现资产列表的实时过滤：

```typescript
const filteredAssets = computed(() => {
  if (!assetFilter.value) return assetList.value
  return assetList.value.filter(asset => 
    asset.code.toLowerCase().includes(assetFilter.value.toLowerCase()) ||
    asset.name.toLowerCase().includes(assetFilter.value.toLowerCase())
  )
})
```

### 表单验证

```typescript
const submitHolding = async () => {
  // 验证资产选择
  if (!holdingForm.value.asset_id) {
    ElMessage.warning('请选择资产')
    return
  }
  // 验证数量
  if (holdingForm.value.quantity <= 0) {
    ElMessage.warning('持仓数量必须大于 0')
    return
  }
  // 验证成本价
  if (holdingForm.value.cost_price <= 0) {
    ElMessage.warning('成本价必须大于 0')
    return
  }
  // ... 提交逻辑
}
```

## API 测试结果

已通过 Postman/curl 测试验证后端 API 正常工作：

```bash
# 添加持仓 - 成功返回 201
POST /api/portfolios/{portfolio_id}/holdings?portfolio_id={portfolio_id}
{
  "asset_id": 1,
  "quantity": 1000,
  "cost_price": 10.5,
  "current_price": 11.2
}

# 响应示例
{
  "id": 1,
  "asset_id": 1,
  "asset_code": "000001",
  "asset_name": "平安银行",
  "quantity": 1000.0,
  "cost_price": 10.5,
  "current_price": 11.2,
  "value": 11200.0,
  "cost": 10500.0,
  "profit": 700.0,
  "profit_percent": 6.67,
  "weight": 100.0
}
```

## 相关文件

- 前端视图：[`src/views/portfolio/PortfolioDetail.vue`](file:///e:/workspace/pms/src/views/portfolio/PortfolioDetail.vue)
- 投资组合 API：[`src/api/services/portfolio.ts`](file:///e:/workspace/pms/src/api/services/portfolio.ts)
- 资产 API：[`src/api/services/asset.ts`](file:///e:/workspace/pms/src/api/services/asset.ts)
- 类型定义：[`src/types/index.ts`](file:///e:/workspace/pms/src/types/index.ts)

## 后端 API 文件

- 持仓 API：[`app/api/holding.py`](file:///e:/workspace/pms/app/api/holding.py)
- 持仓 Service：[`app/services/holding.py`](file:///e:/workspace/pms/app/services/holding.py)
- 持仓 Model：[`app/models/holding.py`](file:///e:/workspace/pms/app/models/holding.py)

## 测试建议

1. **功能测试**
   - 测试添加持仓的完整流程
   - 测试编辑持仓功能
   - 测试删除持仓功能
   - 测试资产搜索功能

2. **边界测试**
   - 测试输入 0 或负数的情况
   - 测试不选择资产直接提交
   - 测试大额数值输入

3. **UI/UX 测试**
   - 测试对话框打开/关闭动画
   - 测试表单验证提示
   - 测试加载状态显示
   - 测试空状态显示

## 完成时间

2026-03-07

## 状态

✅ **已完成** - 添加持仓功能现已完全可用
