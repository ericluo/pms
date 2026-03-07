# PMS API 文档

## 概述

本文档描述了投资组合管理系统（PMS）的 RESTful API 接口。

### 基础信息

- **基础 URL**: `http://localhost:5000/api`
- **认证方式**: JWT Bearer Token
- **数据格式**: JSON

### 认证

所有需要认证的接口都需要在请求头中携带 JWT token：

```
Authorization: Bearer <your_jwt_token>
```

## API 端点

### 1. 认证接口

#### 1.1 用户登录

**POST** `/auth/login`

**请求体**：
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**响应**：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "name": "Test User"
  }
}
```

#### 1.2 用户注册

**POST** `/auth/register`

**请求体**：
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "password123",
  "name": "New User"
}
```

**响应**：
```json
{
  "id": 2,
  "username": "newuser",
  "email": "newuser@example.com",
  "name": "New User"
}
```

#### 1.3 获取当前用户信息

**GET** `/auth/me`

**响应**：
```json
{
  "id": 1,
  "username": "testuser",
  "email": "user@example.com",
  "name": "Test User",
  "role": "user"
}
```

---

### 2. 投资组合接口

#### 2.1 获取投资组合列表

**GET** `/portfolios`

**查询参数**：
- `page` (可选): 页码，默认 1
- `per_page` (可选): 每页数量，默认 10

**响应**：
```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "我的投资组合",
    "description": "长期价值投资",
    "benchmark": "沪深 300",
    "risk_level": "中风险",
    "is_default": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 2.2 创建投资组合

**POST** `/portfolios`

**请求体**：
```json
{
  "name": "成长型组合",
  "description": "专注于成长股投资",
  "benchmark": "中证 500",
  "risk_level": "高风险",
  "is_default": false
}
```

**响应**：
```json
{
  "id": 2,
  "user_id": 1,
  "name": "成长型组合",
  "description": "专注于成长股投资",
  "benchmark": "中证 500",
  "risk_level": "高风险",
  "is_default": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 2.3 获取投资组合详情

**GET** `/portfolios/<id>`

**响应**：
```json
{
  "portfolio": {
    "id": 1,
    "user_id": 1,
    "name": "我的投资组合",
    "description": "长期价值投资",
    "benchmark": "沪深 300",
    "risk_level": "中风险",
    "is_default": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "holdings": [
    {
      "id": 1,
      "portfolio_id": 1,
      "asset_id": 1,
      "quantity": 1000,
      "cost_price": 10.5,
      "current_price": 11.2,
      "value": 11200,
      "profit": 700,
      "profit_percent": 6.67,
      "asset": {
        "id": 1,
        "code": "600000",
        "name": "浦发银行",
        "type": "stock",
        "market": "A 股",
        "industry": "银行"
      }
    }
  ]
}
```

#### 2.4 更新投资组合

**PUT** `/portfolios/<id>`

**请求体**：
```json
{
  "name": "更新后的组合名称",
  "is_default": true
}
```

**响应**：
```json
{
  "id": 1,
  "user_id": 1,
  "name": "更新后的组合名称",
  "description": "长期价值投资",
  "benchmark": "沪深 300",
  "risk_level": "中风险",
  "is_default": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

#### 2.5 删除投资组合

**DELETE** `/portfolios/<id>`

**响应**：
```json
{
  "message": "投资组合删除成功"
}
```

---

### 3. 资产接口

#### 3.1 获取资产列表

**GET** `/assets`

**查询参数**：
- `type` (可选): 资产类型筛选 (stock/fund/bond/cash)
- `market` (可选): 市场筛选

**响应**：
```json
[
  {
    "id": 1,
    "code": "600000",
    "name": "浦发银行",
    "type": "stock",
    "market": "A 股",
    "industry": "银行",
    "interest_rate": null,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "code": "CASH-1704067200000",
    "name": "余额宝",
    "type": "cash",
    "market": null,
    "industry": null,
    "interest_rate": 0.025,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 3.2 获取资产类型列表

**GET** `/assets/types`

**响应**：
```json
[
  {"value": "stock", "label": "股票"},
  {"value": "fund", "label": "基金"},
  {"value": "bond", "label": "债券"},
  {"value": "cash", "label": "现金"}
]
```

#### 3.3 创建资产

**POST** `/assets`

**请求体**（股票）：
```json
{
  "code": "600000",
  "name": "浦发银行",
  "type": "stock",
  "market": "A 股",
  "industry": "银行"
}
```

**请求体**（现金）：
```json
{
  "code": "CASH-001",
  "name": "银行存款",
  "type": "cash",
  "interest_rate": 0.03
}
```

**响应**：
```json
{
  "id": 3,
  "code": "600000",
  "name": "浦发银行",
  "type": "stock",
  "market": "A 股",
  "industry": "银行",
  "interest_rate": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 3.4 获取资产详情

**GET** `/assets/<id>`

**响应**：
```json
{
  "id": 1,
  "code": "600000",
  "name": "浦发银行",
  "type": "stock",
  "market": "A 股",
  "industry": "银行",
  "interest_rate": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 3.5 更新资产

**PUT** `/assets/<id>`

**请求体**：
```json
{
  "name": "更新后的名称",
  "industry": "更新后的行业"
}
```

**响应**：
```json
{
  "id": 1,
  "code": "600000",
  "name": "更新后的名称",
  "type": "stock",
  "market": "A 股",
  "industry": "更新后的行业",
  "interest_rate": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

#### 3.6 删除资产

**DELETE** `/assets/<id>`

**响应**：
```json
{
  "message": "资产删除成功"
}
```

---

### 4. 持仓接口

#### 4.1 获取持仓列表

**GET** `/portfolios/<portfolio_id>/holdings`

**响应**：
```json
[
  {
    "id": 1,
    "portfolio_id": 1,
    "asset_id": 1,
    "quantity": 1000,
    "cost_price": 10.5,
    "current_price": 11.2,
    "value": 11200,
    "profit": 700,
    "profit_percent": 6.67,
    "weight": 0.35,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 4.2 添加持仓

**POST** `/portfolios/<portfolio_id>/holdings`

**请求体**：
```json
{
  "asset_id": 1,
  "quantity": 1000,
  "cost_price": 10.5,
  "current_price": 11.2
}
```

**响应**：
```json
{
  "id": 1,
  "portfolio_id": 1,
  "asset_id": 1,
  "quantity": 1000,
  "cost_price": 10.5,
  "current_price": 11.2,
  "value": 11200,
  "profit": 700,
  "profit_percent": 6.67,
  "weight": 0.35
}
```

---

### 5. 错误响应

所有接口在发生错误时返回统一格式的错误响应：

```json
{
  "error": "错误信息"
}
```

#### 常见错误码

- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未授权，需要登录
- `403 Forbidden`: 禁止访问，权限不足
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误

---

## 数据字典

### 资产类型 (type)

| 值 | 说明 | 特点 |
|----|------|------|
| `stock` | 股票 | 需要实时行情，有涨跌停限制 |
| `fund` | 基金 | 包括 ETF、开放式基金等 |
| `bond` | 债券 | 包括国债、企业债等 |
| `cash` | 现金 | 现金及现金等价物，如余额宝 |

### 风险等级 (risk_level)

| 值 | 说明 |
|----|------|
| `低风险` | 保守型投资，波动小 |
| `中风险` | 平衡型投资，适度波动 |
| `高风险` | 激进型投资，波动大 |

### 市场类型 (market)

| 值 | 说明 |
|----|------|
| `A 股` | 中国大陆股市 |
| `港股` | 香港股市 |
| `美股` | 美国股市 |
| `其他` | 其他市场 |

---

## 更新日志

### v0.1.0 (2024-01-01)

- ✨ 初始版本
- ✨ 实现用户认证接口
- ✨ 实现投资组合 CRUD 接口
- ✨ 实现资产 CRUD 接口
- ✨ 实现持仓管理接口
- ✨ 添加资产类型筛选功能
