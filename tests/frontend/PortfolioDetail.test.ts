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

    // 检查持仓数据是否显示（数量直接显示，没有千位分隔符）
    expect(wrapper.text()).toContain('平安银行')
    expect(wrapper.text()).toContain('000001')
    expect(wrapper.text()).toContain('1000')
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

  it('应该格式化货币显示', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: []
    })

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 测试货币格式化（formatCurrency 返回带 ¥ 符号的格式）
    expect(wrapper.vm.formatCurrency(1234567.89)).toContain('1,234,567.89')
    expect(wrapper.vm.formatCurrency(0)).toBe('¥0.00')
  })

  it('应该正确显示资产类型标签', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: mockPortfolio,
      holdings: []
    })

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 测试资产类型（stock 返回 'danger', fund 返回 'success', bond 返回 'warning'）
    expect(wrapper.vm.getTypeTagType('stock')).toBe('danger')
    expect(wrapper.vm.getTypeTagType('fund')).toBe('success')
    expect(wrapper.vm.getTypeTagType('bond')).toBe('warning')
    expect(wrapper.vm.getTypeName('stock')).toBe('股票')
    expect(wrapper.vm.getTypeName('fund')).toBe('基金')
    expect(wrapper.vm.getTypeName('bond')).toBe('债券')
  })

  it('应该处理加载状态', async () => {
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
      }
    })

    // 等待所有异步操作完成
    await flushPromises()

    // 加载完成后 loading 应该是 false
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
})

describe('PortfolioDetail - 方法测试', () => {
  let router: any
  let pinia: any

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

    vi.clearAllMocks()
  })

  it('应该正确过滤资产列表', async () => {
    const mockAssets = [
      { id: 1, code: '000001', name: '平安银行', type: 'stock' },
      { id: 2, code: '600519', name: '贵州茅台', type: 'stock' },
      { id: 3, code: '300750', name: '宁德时代', type: 'stock' }
    ]

    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: { id: 1, name: '测试', user_id: 1 },
      holdings: []
    })
    vi.mocked(getAssets).mockResolvedValue(mockAssets)

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 加载资产
    await wrapper.vm.loadAssets()
    await flushPromises()

    // 初始状态 - 显示所有资产
    expect(wrapper.vm.filteredAssets.length).toBe(3)

    // 设置过滤条件
    wrapper.vm.assetFilter = '平安'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.filteredAssets.length).toBe(1)
    expect(wrapper.vm.filteredAssets[0].name).toBe('平安银行')

    // 搜索 "600"
    wrapper.vm.assetFilter = '600'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.filteredAssets.length).toBe(1)
    expect(wrapper.vm.filteredAssets[0].code).toBe('600519')
  })

  it('应该正确打开添加持仓对话框', async () => {
    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: { id: 1, name: '测试', user_id: 1 },
      holdings: []
    })
    vi.mocked(getAssets).mockResolvedValue([])

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 调用打开对话框方法
    await wrapper.vm.openAddDialog()
    await flushPromises()

    // 验证对话框状态
    expect(wrapper.vm.dialogVisible).toBe(true)
    expect(wrapper.vm.isEditMode).toBe(false)
    expect(wrapper.vm.dialogTitle).toBe('添加持仓')
  })

  it('应该正确打开编辑持仓对话框', async () => {
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
      }
    }

    vi.mocked(getPortfolioById).mockResolvedValue({
      portfolio: { id: 1, name: '测试', user_id: 1 },
      holdings: [mockHolding]
    })
    vi.mocked(getAssets).mockResolvedValue([])

    router.push('/portfolio/1')
    await router.isReady()

    const wrapper = mount(PortfolioDetail, {
      global: {
        plugins: [router, pinia]
      }
    })

    await flushPromises()

    // 调用打开编辑对话框方法
    await wrapper.vm.openEditDialog(mockHolding)
    await flushPromises()

    // 验证对话框状态
    expect(wrapper.vm.dialogVisible).toBe(true)
    expect(wrapper.vm.isEditMode).toBe(true)
    expect(wrapper.vm.dialogTitle).toBe('编辑持仓')
  })
})
