import http from '@/utils/http'
import type { Portfolio, Holding } from '@/types'

// 获取投资组合列表
export async function getPortfolios(): Promise<Portfolio[]> {
  return http.get<Portfolio[]>('/portfolios')
}

// 获取单个投资组合详情
export async function getPortfolioById(id: number): Promise<{ portfolio: Portfolio; holdings: Holding[] }> {
  return http.get(`/portfolios/${id}`)
}

// 创建投资组合
export async function createPortfolio(portfolioData: Partial<Portfolio>): Promise<Portfolio> {
  return http.post<Portfolio>('/portfolios', portfolioData)
}

// 更新投资组合
export async function updatePortfolio(id: number, portfolioData: Partial<Portfolio>): Promise<Portfolio> {
  return http.put<Portfolio>(`/portfolios/${id}`, portfolioData)
}

// 删除投资组合
export async function deletePortfolio(id: number): Promise<{ message: string }> {
  return http.delete(`/portfolios/${id}`)
}

// 获取投资组合持仓
export async function getPortfolioHoldings(portfolioId: number): Promise<Holding[]> {
  return http.get<Holding[]>(`/portfolios/${portfolioId}/holdings`)
}

// 添加持仓
export async function addHolding(portfolioId: number, holdingData: {
  asset_id: number
  quantity: number
  cost_price: number
  current_price?: number
}): Promise<Holding> {
  return http.post<Holding>(`/portfolios/${portfolioId}/holdings`, holdingData)
}

// 更新持仓
export async function updateHolding(portfolioId: number, holdingId: number, holdingData: {
  quantity?: number
  cost_price?: number
}): Promise<Holding> {
  return http.put<Holding>(`/portfolios/${portfolioId}/holdings/${holdingId}`, holdingData)
}

// 删除持仓
export async function deleteHolding(portfolioId: number, holdingId: number): Promise<{ message: string }> {
  return http.delete(`/portfolios/${portfolioId}/holdings/${holdingId}`)
}