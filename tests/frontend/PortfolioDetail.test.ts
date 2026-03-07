/**
 * PMS 前端组件单元测试
 * 使用 Vitest + @vue/test-utils 进行测试
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'
import PortfolioDetail from '@/views/portfolio/PortfolioDetail.vue'

// Mock API 调用
vi.mock('@/api/services/portfolio', () => ({
  getPortfolioById: vi.fn(),
  addHolding: vi.fn(),
  updateHolding: vi.fn(),
  deleteHolding: vi.fn()
}))

vi.mock('@/api/services/asset', () => ({
  getAssets: vi.fn()
}))

// Mock Element Plus 消息
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn(),
    info: vi.fn()
  },
  ElMessageBox: {
    confirm: vi.fn()
  }
}))

import { getPortfolioById, addHolding, updateHolding, deleteHolding } from '@/api/services/portfolio'
import { getAssets } from '@/api/services/asset'
import { ElMessage, ElMessageBox } from 'element-plus'

describe('PortfolioDetail', () => {
  let router: any
  let pinia: any

  const mockPortfolio = {
    id: 1,
    user_id: 1,
    name: '测试组合',
    description: '测试描述',
    benchmark: '沪深 300',
    risk_level: '中等',
    is_default: false,
    created_at: '2024-01-01T00:00:00',
    updated_at: '2024-01-01T00:00:00'
  }

  const mockHolding = {
    id: 1,
    portfolio_id: 1,
    asset_id: 1,
    quantity: 1000,
    cost_price: 10.5,
    current_price: 11.2,
    value: 11200,
    profit: 700,
    profit_rate: 6.67,
    asset: {
      id: 1,
      code: '000001',
      name: '平安银行',
      type: 'stock',
      market: '深圳证券交易所',
      industry: '金融'
    },
    created_at: '2024-01-01T00:00:00',
    updated_at: '2024-01-01T00:00:00'
  }

  const mockAsset = {
    id: 1,
    code: '000001',
    name: '平安银行',
    type: 'stock',
    market: '深圳证券交易所',
    industry: '金融'
  }

  beforeEach(() => {
    pinia = createPinia()
    setActivePinia(pinia)

    router = createRouter({
      history: createMemoryHistory(),
      routes: [
        {
          path: '/portfolio/:id',
          name: 'PortfolioDetail',
          component: PortfolioDetail
        }
      ]
    })

    // 重置所有 mock
    vi.clearAllMocks()
  })

  it('应该成功渲染投资组合详情页面', async () => {
    // Mock API 响应
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: []
    })

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      },
      props: {
        id: '1'
      }
    })

    await flushPromises()

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.text()).toContain('测试组合')
  })

  it('应该显示持仓列表', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: [mockHolding]
    })

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 检查持仓表格是否存在
    const table = wrapper.find('.el-table')
    expect(table.exists()).toBe(true)

    // 检查持仓数据是否显示
    expect(wrapper.text()).toContain('平安银行')
    expect(wrapper.text()).toContain('000001')
    expect(wrapper.text()).toContain('1,000')
  })

  it('应该打开添加持仓对话框', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: []
    })

    vi.mocked(getAssets).mockResolvedValue([mockAsset])

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 点击添加持仓按钮
    const addButton = wrapper.find('button.el-button:has(.el-icon-plus)')
    await addButton.trigger('click')
    await flushPromises()

    // 检查对话框是否打开
    const dialog = wrapper.find('.el-dialog')
    expect(dialog.exists()).toBe(true)
    expect(wrapper.vm.dialogVisible).toBe(true)
  })

  it('应该能够提交添加持仓表单', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: []
    })

    vi.mocked(getAssets).mockResolvedValue([mockAsset])
    vi.mocked(addHolding).mockResolvedValue({
      id: 2,
      portfolio_id: 1,
      asset_id: 1,
      quantity: 1000,
      cost_price: 10.5
    })

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 打开对话框
    const addButton = wrapper.find('button.el-button:has(.el-icon-plus)')
    await addButton.trigger('click')
    await flushPromises()

    // 填写表单
    await wrapper.vm.$data.holdingForm.asset_id = 1
    await wrapper.vm.$data.holdingForm.quantity = 1000
    await wrapper.vm.$data.holdingForm.cost_price = 10.5

    // 提交表单
    await wrapper.vm.submitHolding()
    await flushPromises()

    // 验证 API 被调用
    expect(addHolding).toHaveBeenCalledWith(1, {
      asset_id: 1,
      quantity: 1000,
      cost_price: 10.5
    })

    // 验证显示成功消息
    expect(ElMessage.success).toHaveBeenCalled()
  })

  it('应该验证持仓表单 - 未选择资产', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: []
    })

    vi.mocked(getAssets).mockResolvedValue([mockAsset])

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 打开对话框
    const addButton = wrapper.find('button.el-button:has(.el-icon-plus)')
    await addButton.trigger('click')
    await flushPromises()

    // 不选择资产直接提交
    await wrapper.vm.submitHolding()
    await flushPromises()

    // 验证显示警告消息
    expect(ElMessage.warning).toHaveBeenCalledWith('请选择资产')
    expect(addHolding).not.toHaveBeenCalled()
  })

  it('应该验证持仓表单 - 数量无效', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: []
    })

    vi.mocked(getAssets).mockResolvedValue([mockAsset])

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 打开对话框
    const addButton = wrapper.find('button.el-button:has(.el-icon-plus)')
    await addButton.trigger('click')
    await flushPromises()

    // 填写表单 - 数量为 0
    await wrapper.vm.$data.holdingForm.asset_id = 1
    await wrapper.vm.$data.holdingForm.quantity = 0
    await wrapper.vm.$data.holdingForm.cost_price = 10.5

    // 提交表单
    await wrapper.vm.submitHolding()
    await flushPromises()

    // 验证显示警告消息
    expect(ElMessage.warning).toHaveBeenCalledWith('持仓数量必须大于 0')
    expect(addHolding).not.toHaveBeenCalled()
  })

  it('应该能够删除持仓', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: [mockHolding]
    })

    vi.mocked(deleteHolding).mockResolvedValue({ message: '删除成功' })
    vi.mocked(ElMessageBox.confirm).mockResolvedValue(true)

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 点击删除按钮
    const deleteButtons = wrapper.findAll('button.el-button--danger')
    expect(deleteButtons.length).toBeGreaterThan(0)
    
    await deleteButtons[0].trigger('click')
    await flushPromises()

    // 验证确认对话框被调用
    expect(ElMessageBox.confirm).toHaveBeenCalled()
    expect(deleteHolding).toHaveBeenCalledWith(1, 1)
  })

  it('应该格式化货币显示', () => {
    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    // 测试货币格式化
    expect(wrapper.vm.formatCurrency(1234567.89)).toContain('1,234,567.89')
    expect(wrapper.vm.formatCurrency(0)).toBe('0.00')
  })

  it('应该正确显示资产类型标签', () => {
    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    // 测试资产类型
    expect(wrapper.vm.getTypeTagType('stock')).toBe('')
    expect(wrapper.vm.getTypeTagType('fund')).toBe('success')
    expect(wrapper.vm.getTypeTagType('bond')).toBe('warning')
    expect(wrapper.vm.getTypeName('stock')).toBe('股票')
    expect(wrapper.vm.getTypeName('fund')).toBe('基金')
    expect(wrapper.vm.getTypeName('bond')).toBe('债券')
  })

  it('应该处理加载状态', async () => {
    // 模拟 API 延迟
    vi.mocked(getPortfolioById).mockImplementation(() => {
      return new Promise(resolve => {
        setTimeout(() => {
          resolve({
            portfolio: mockPortfolio,
            holdings: []
          })
        }, 100)
      })
    })

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    // 初始状态应该是加载中
    expect(wrapper.vm.loading).toBe(true)

    await flushPromises()

    // 加载完成后
    expect(wrapper.vm.loading).toBe(false)
    expect(getPortfolioById).toHaveBeenCalled()
  })

  it('应该处理 API 错误', async () => {
    vi.mocked(getPortfolioById).mockRejectedValue(new Error('网络错误'))

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 验证显示错误消息
    expect(ElMessage.error).toHaveBeenCalled()
  })

  it('应该能够编辑持仓', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: [mockHolding]
    })

    vi.mocked(getAssets).mockResolvedValue([mockAsset])
    vi.mocked(updateHolding).mockResolvedValue({
      id: 1,
      quantity: 1500,
      cost_price: 11.0
    })

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 点击编辑按钮
    const editButtons = wrapper.findAll('button.el-button:not(.el-button--danger)')
    const editButton = editButtons.find(btn => btn.text() === '编辑')
    expect(editButton).toBeDefined()
    
    if (editButton) {
      await editButton.trigger('click')
      await flushPromises()

      // 检查对话框是否打开
      expect(wrapper.vm.dialogVisible).toBe(true)
      expect(wrapper.vm.isEditMode).toBe(true)
      expect(wrapper.vm.dialogTitle).toBe('编辑持仓')
    }
  })
})

describe('PortfolioDetail - 计算属性', () => {
  let pinia: any

  beforeEach(() => {
    pinia = createPinia()
    setActivePinia(pinia)
  })

  it('应该过滤资产列表', async () => {
    const mockAssets = [
      { id: 1, code: '000001', name: '平安银行', type: 'stock' },
      { id: 2, code: '600519', name: '贵州茅台', type: 'stock' },
      { id: 3, code: '300750', name: '宁德时代', type: 'stock' }
    ]

    vi.mocked(getAssets).mockResolvedValue(mockAssets)

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [createPinia()]
      }
    })

    await wrapper.vm.loadAssets()

    // 初始状态 - 显示所有资产
    expect(wrapper.vm.filteredAssets.length).toBe(3)

    // 搜索"平安"
    await wrapper.vm.$data.assetFilter = '平安'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.filteredAssets.length).toBe(1)
    expect(wrapper.vm.filteredAssets[0].name).toBe('平安银行')

    // 搜索"600"
    await wrapper.vm.$data.assetFilter = '600'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.filteredAssets.length).toBe(1)
    expect(wrapper.vm.filteredAssets[0].code).toBe('600519')
  })
})
