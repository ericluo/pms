// 用户类型
export interface User {
  id: number
  username: string
  email: string
  name: string
  role: string
  created_at: string
  updated_at: string
}

// 投资组合类型
export interface Portfolio {
  id: number
  user_id: number
  name: string
  description: string
  benchmark: string
  risk_level: string
  created_at: string
  updated_at: string
}

// 资产类型
export interface Asset {
  id: number
  code: string
  name: string
  type: string
  market: string
  industry: string
  created_at: string
  updated_at: string
}

// 持仓类型
export interface Holding {
  id: number
  portfolio_id: number
  asset_id: number
  quantity: number
  cost_price: number
  current_price: number
  value: number
  profit: number
  profit_rate: number
  asset?: Asset
  created_at: string
  updated_at: string
}

// 交易记录类型
export interface Transaction {
  id: number
  portfolio_id: number
  asset_id: number
  type: string
  quantity: number
  price: number
  amount: number
  fee: number
  transaction_date: string
  asset?: Asset
  created_at: string
}

// 现金流水类型
export interface CashFlow {
  id: number
  portfolio_id: number
  type: string
  amount: number
  description: string
  transaction_date: string
  created_at: string
}

// 市场数据类型
export interface MarketData {
  id: number
  asset_id: number
  date: string
  open: number
  high: number
  low: number
  close: number
  volume: number
  amount: number
  created_at: string
}

// 报告类型
export interface Report {
  id: number
  portfolio_id: number
  portfolio_name: string
  type: string
  title: string
  generated_at: string
  url?: string
}

// 登录响应类型
export interface LoginResponse {
  token: string
  user: User
}

// 错误响应类型
export interface ErrorResponse {
  message: string
  status: number
}

// 分页响应类型
export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  page_size: number
  pages: number
}