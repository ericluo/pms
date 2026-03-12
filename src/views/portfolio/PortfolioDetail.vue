<template>
  <div class="portfolio-detail">
    <el-page-header
      @back="goBack"
      :content="portfolio.name"
    >
      <template #extra>
        <el-button @click="goToEdit">
          <el-icon><Edit /></el-icon>
          <span>编辑</span>
        </el-button>
      </template>
    </el-page-header>
    
    <el-card class="portfolio-info-card">
      <template #header>
        <span>组合信息</span>
      </template>
      <el-descriptions :column="3">
        <el-descriptions-item label="组合名称">
          {{ portfolio.name }}
          <el-tag v-if="portfolio.is_default" size="small" type="primary" effect="dark" style="margin-left: 8px;">默认</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="业绩基准">{{ portfolio.benchmark }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">{{ portfolio.risk_level }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(portfolio.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formatDate(portfolio.updated_at) }}</el-descriptions-item>
      </el-descriptions>
      <div class="portfolio-description">
        <h4>组合描述</h4>
        <p>{{ portfolio.description || '无' }}</p>
      </div>
    </el-card>
    
    <el-card class="portfolio-holdings-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>持仓明细</span>
          <el-button type="primary" size="small" @click="addHolding">
            <el-icon><Plus /></el-icon>
            <span>添加持仓</span>
          </el-button>
        </div>
      </template>
      <el-table :data="holdings" style="width: 100%" v-loading="loading">
        <el-table-column label="资产名称">
          <template #default="scope">
            {{ scope.row.asset?.name || scope.row.asset_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="资产代码">
          <template #default="scope">
            {{ scope.row.asset?.code || scope.row.asset_code || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="资产类型" width="80">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.asset?.type)">
              {{ getTypeName(scope.row.asset?.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="持仓数量" />
        <el-table-column prop="cost_price" label="成本价" />
        <el-table-column prop="current_price" label="当前价" />
        <el-table-column prop="value" label="市值">
          <template #default="scope">
            {{ formatCurrency(scope.row.value) }}
          </template>
        </el-table-column>
        <el-table-column prop="profit" label="盈亏">
          <template #default="scope">
            <span :class="scope.row.profit >= 0 ? 'profit-positive' : 'profit-negative'">
              {{ formatCurrency(scope.row.profit) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="profit_rate" label="盈亏率(%)">
          <template #default="scope">
            <span :class="scope.row.profit_rate >= 0 ? 'profit-positive' : 'profit-negative'">
              {{ scope.row.profit_rate?.toFixed(2) }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button size="small" @click="editHolding(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteHoldingById(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="holdings.length === 0 && !loading" description="暂无持仓，请添加" />
    </el-card>

    <!-- 添加/编辑持仓对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="holdingForm" label-width="100px" label-position="left">
        <el-form-item label="选择资产" required>
          <el-input
            v-model="assetFilter"
            placeholder="搜索资产代码或名称..."
            prefix-icon="Search"
            clearable
          />
          <el-select
            v-model="holdingForm.asset_id"
            placeholder="请选择资产"
            filterable
            style="width: 100%; margin-top: 8px;"
          >
            <el-option
              v-for="asset in filteredAssets"
              :key="asset.id"
              :label="`${asset.code} - ${asset.name}`"
              :value="asset.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="持仓数量" required>
          <el-input-number
            v-model="holdingForm.quantity"
            :min="0"
            :precision="2"
            :step="100"
            style="width: 100%"
            placeholder="请输入持仓数量"
          />
        </el-form-item>
        <el-form-item label="成本价" required>
          <el-input-number
            v-model="holdingForm.cost_price"
            :min="0"
            :precision="4"
            :step="0.01"
            style="width: 100%"
            placeholder="请输入成本价"
          />
        </el-form-item>
        <el-form-item label="当前价">
          <el-input-number
            v-model="holdingForm.current_price"
            :min="0"
            :precision="4"
            :step="0.01"
            style="width: 100%"
            placeholder="请输入当前价"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitHolding" :loading="loading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePortfolioStore } from '@/store/modules/portfolio'
import { Edit, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Portfolio, Holding, Asset } from '@/types'
import { getPortfolioById, addHolding, updateHolding, deleteHolding } from '@/api/services/portfolio'
import { getAssets } from '@/api/services/asset'

const router = useRouter()
const route = useRoute()
const portfolioStore = usePortfolioStore()

const loading = ref(false)
const portfolio = ref<Portfolio>({
  id: 0,
  user_id: 0,
  name: '',
  description: '',
  benchmark: '',
  risk_level: '',
  is_default: false,
  created_at: '',
  updated_at: ''
})

const holdings = ref<Holding[]>([])

// 添加持仓对话框
const dialogVisible = ref(false)
const dialogTitle = ref('添加持仓')
const isEditMode = ref(false)
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
const assetList = ref<Asset[]>([])
const assetLoading = ref(false)
const assetFilter = ref('')

const filteredAssets = computed(() => {
  if (!assetFilter.value) return assetList.value
  return assetList.value.filter(asset => 
    asset.code.toLowerCase().includes(assetFilter.value.toLowerCase()) ||
    asset.name.toLowerCase().includes(assetFilter.value.toLowerCase())
  )
})

const typeNames: Record<string, string> = {
  'stock': '股票',
  'fund': '基金',
  'bond': '债券',
  'cash': '现金'
}

const getTypeName = (type?: string) => {
  return type ? (typeNames[type] || type) : ''
}

const getTypeTagType = (type?: string) => {
  const tagTypes: Record<string, string> = {
    'stock': 'danger',
    'fund': 'success',
    'bond': 'warning',
    'cash': 'info'
  }
  return type ? (tagTypes[type] || '') : ''
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const formatCurrency = (value: number) => {
  if (value === undefined || value === null) return '¥0.00'
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value)
}

const fetchPortfolioDetail = async () => {
  const id = Number(route.params.id)
  if (!id) {
    console.error('投资组合 ID 无效:', route.params.id)
    return
  }
  
  loading.value = true
  try {
    console.log('获取投资组合详情，ID:', id)
    const response = await getPortfolioById(id)
    console.log('获取投资组合详情响应:', response)
    console.log('响应类型:', typeof response)
    console.log('响应键:', Object.keys(response))
    
    // 检查响应格式
    if (response && typeof response === 'object') {
      if ('portfolio' in response) {
        portfolio.value = response.portfolio
        console.log('投资组合数据:', portfolio.value)
      } else {
        console.error('响应中没有 portfolio 字段')
        ElMessage.error('数据格式错误')
        return
      }
      
      if ('holdings' in response) {
        holdings.value = response.holdings || []
        console.log('持仓列表:', holdings.value)
        console.log('持仓数量:', holdings.value.length)
      } else {
        console.warn('响应中没有 holdings 字段')
        holdings.value = []
      }
    } else {
      console.error('响应不是对象类型:', response)
      ElMessage.error('数据格式错误')
    }
  } catch (error: any) {
    console.error('获取投资组合详情失败:', error)
    console.error('错误详情:', error.response?.data)
    ElMessage.error(error?.message || '获取投资组合详情失败')
  } finally {
    loading.value = false
  }
}

// 加载资产列表
const loadAssets = async () => {
  assetLoading.value = true
  try {
    const response = await getAssets()
    assetList.value = response
  } catch (error: any) {
    console.error('加载资产列表失败:', error)
    ElMessage.error('加载资产列表失败')
  } finally {
    assetLoading.value = false
  }
}

// 打开添加持仓对话框
const openAddDialog = async () => {
  dialogTitle.value = '添加持仓'
  isEditMode.value = false
  holdingForm.value = {
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
  }
  await loadAssets()
  dialogVisible.value = true
}

// 打开编辑持仓对话框
const openEditDialog = async (holding: Holding) => {
  dialogTitle.value = '编辑持仓'
  isEditMode.value = true
  holdingForm.value = {
    ...holding,
    portfolio_id: Number(route.params.id)
  }
  await loadAssets()
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  holdingForm.value = {
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
  }
  assetFilter.value = ''
}

// 提交持仓（添加或编辑）
const submitHolding = async () => {
  console.log('=== 开始提交持仓 ===')
  console.log('asset_id:', holdingForm.value.asset_id)
  console.log('quantity:', holdingForm.value.quantity)
  console.log('cost_price:', holdingForm.value.cost_price)
  
  if (!holdingForm.value.asset_id) {
    console.log('验证失败：没有选择资产')
    ElMessage.warning('请选择资产')
    return
  }
  if (holdingForm.value.quantity <= 0) {
    console.log('验证失败：数量不大于 0')
    ElMessage.warning('持仓数量必须大于 0')
    return
  }
  if (holdingForm.value.cost_price <= 0) {
    console.log('验证失败：成本价不大于 0')
    ElMessage.warning('成本价必须大于 0')
    return
  }
  
  console.log('验证通过，准备提交')

  loading.value = true
  try {
    const portfolioId = Number(route.params.id)
    console.log('提交持仓，投资组合 ID:', portfolioId, '表单数据:', holdingForm.value)
    
    if (isEditMode.value) {
      // 编辑模式
      console.log('编辑持仓 ID:', holdingForm.value.id)
      await updateHolding(portfolioId, holdingForm.value.id, {
        quantity: holdingForm.value.quantity,
        cost_price: holdingForm.value.cost_price
      })
      ElMessage.success('持仓更新成功')
    } else {
      // 添加模式 - 直接调用 http.post 测试
      console.log('添加新持仓 - 直接调用')
      import('@/utils/http').then(({ default: http }) => {
        console.log('准备发送 POST 请求...')
        http.post(`/portfolios/${portfolioId}/holdings`, {
          asset_id: holdingForm.value.asset_id,
          quantity: holdingForm.value.quantity,
          cost_price: holdingForm.value.cost_price,
          current_price: holdingForm.value.current_price
        }).then(result => {
          console.log('POST 请求成功！结果:', result)
          ElMessage.success('持仓添加成功')
          dialogVisible.value = false
          resetForm()
          fetchPortfolioDetail()
        }).catch(error => {
          console.error('POST 请求失败:', error)
          ElMessage.error('添加失败：' + (error.message || '未知错误'))
        })
      })
      return // 提前返回，不执行后面的代码
    }
    dialogVisible.value = false
    
    // 重置表单
    resetForm()
    
    // 刷新持仓列表 - 使用短暂的延迟确保后端事务已提交
    console.log('等待刷新...')
    await new Promise(resolve => setTimeout(resolve, 300))
    console.log('刷新持仓列表...')
    await fetchPortfolioDetail()
    console.log('持仓列表已刷新，当前持仓数量:', holdings.value.length)
  } catch (error: any) {
    console.error('提交持仓失败:', error)
    console.error('错误详情:', error.response?.data)
    ElMessage.error(error?.response?.data?.message || error.message || '提交持仓失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.back()
}

const goToEdit = () => {
  router.push(`/portfolio/${route.params.id}/edit`)
}

const addHolding = () => {
  openAddDialog()
}

const editHolding = (holding: Holding) => {
  openEditDialog(holding)
}

const deleteHoldingById = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该持仓吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const portfolioId = Number(route.params.id)
    await deleteHolding(portfolioId, id)
    ElMessage.success('删除成功')
    await fetchPortfolioDetail()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除持仓失败:', error)
      ElMessage.error(error?.message || '删除持仓失败')
    }
  }
}

onMounted(() => {
  fetchPortfolioDetail()
})
</script>

<style scoped>
.portfolio-detail {
  width: 100%;
  padding: 20px 0;
}

.portfolio-info-card {
  margin-top: 20px;
}

.portfolio-description {
  margin-top: 20px;
}

.portfolio-description h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 500;
}

.portfolio-holdings-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profit-positive {
  color: #f56c6c;
}

.profit-negative {
  color: #67c23a;
}
</style>