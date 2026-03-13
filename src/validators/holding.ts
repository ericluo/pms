import type { HoldingCreate } from '@/types/holding'

export function validateHoldingForm(data: HoldingCreate): string | null {
  if (!data.asset_id) {
    return '请选择资产'
  }
  if (data.quantity <= 0) {
    return '持仓数量必须大于 0'
  }
  if (data.cost_price <= 0) {
    return '成本价必须大于 0'
  }
  return null
}
