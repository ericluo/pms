import http from '@/utils/http'
import type { Report } from '@/types'

// 创建报告
export const createReport = async (data: {
  portfolio_id: number
  type: string
  title: string
}): Promise<Report> => {
  const response = await http.post('/api/reports', data)
  return response.data
}

// 获取报告列表
export const getReports = async (): Promise<Report[]> => {
  const response = await http.get('/api/reports')
  return response.data
}

// 获取报告详情
export const getReportDetail = async (id: number): Promise<Report> => {
  const response = await http.get(`/api/reports/${id}`)
  return response.data
}

// 删除报告
export const deleteReport = async (id: number): Promise<{ message: string }> => {
  const response = await http.delete(`/api/reports/${id}`)
  return response.data
}

// 导出报告
export const exportReport = async (id: number): Promise<Blob> => {
  const response = await http.get(`/api/reports/${id}/export`, {
    responseType: 'blob'
  })
  return response.data
}