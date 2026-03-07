import axios from '@/utils/http'
import type { Asset } from '@/types'

export const getAssets = (params?: { type?: string; market?: string }) => {
  return axios.get<Asset[]>('/assets', { params })
}

export const getAssetById = (id: number) => {
  return axios.get<Asset>(`/assets/${id}`)
}

export const createAsset = (data: Partial<Asset>) => {
  return axios.post('/assets', data)
}

export const updateAsset = (id: number, data: Partial<Asset>) => {
  return axios.put(`/assets/${id}`, data)
}

export const deleteAsset = (id: number) => {
  return axios.delete(`/assets/${id}`)
}

export const getAssetTypes = () => {
  return axios.get<{ value: string; label: string }[]>('/assets/types')
}
