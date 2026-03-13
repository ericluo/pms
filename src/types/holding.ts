import type { Asset } from './asset'

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

export interface HoldingCreate {
  asset_id: number
  quantity: number
  cost_price: number
  current_price?: number
}

export interface HoldingUpdate {
  quantity?: number
  cost_price?: number
  current_price?: number
}
