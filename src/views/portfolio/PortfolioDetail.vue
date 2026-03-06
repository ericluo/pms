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
        <el-descriptions-item label="组合名称">{{ portfolio.name }}</el-descriptions-item>
        <el-descriptions-item label="业绩基准">{{ portfolio.benchmark }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">{{ portfolio.risk_level }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ portfolio.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ portfolio.updated_at }}</el-descriptions-item>
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
      <el-table :data="holdings" style="width: 100%">
        <el-table-column prop="asset.name" label="资产名称" />
        <el-table-column prop="asset.code" label="资产代码" />
        <el-table-column prop="quantity" label="持仓数量" />
        <el-table-column prop="cost_price" label="成本价" />
        <el-table-column prop="current_price" label="当前价" />
        <el-table-column prop="value" label="市值" />
        <el-table-column prop="profit" label="盈亏" />
        <el-table-column prop="profit_rate" label="盈亏率" />
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button size="small" @click="editHolding(scope.row.id)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteHolding(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePortfolioStore } from '@/store/modules/portfolio'
import { Edit, Plus } from '@element-plus/icons-vue'
import type { Portfolio, Holding } from '@/types'

const router = useRouter()
const route = useRoute()
const portfolioStore = usePortfolioStore()

const portfolio = ref<Portfolio>({
  id: 0,
  user_id: 0,
  name: '',
  description: '',
  benchmark: '',
  risk_level: '',
  created_at: '',
  updated_at: ''
})

const holdings = ref<Holding[]>([
  {
    id: 1,
    portfolio_id: 1,
    asset_id: 1,
    quantity: 100,
    cost_price: 100,
    current_price: 110,
    value: 11000,
    profit: 1000,
    profit_rate: 10,
    asset: {
      id: 1,
      code: '600000',
      name: '浦发银行',
      type: '股票',
      market: 'A股',
      industry: '银行',
      created_at: '',
      updated_at: ''
    },
    created_at: '',
    updated_at: ''
  }
])

const goBack = () => {
  router.back()
}

const goToEdit = () => {
  router.push(`/portfolio/${route.params.id}/edit`)
}

const addHolding = () => {
  // 添加持仓逻辑
  console.log('添加持仓')
}

const editHolding = (id: number) => {
  // 编辑持仓逻辑
  console.log('编辑持仓:', id)
}

const deleteHolding = (id: number) => {
  // 删除持仓逻辑
  console.log('删除持仓:', id)
}

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    // 获取投资组合详情
    portfolioStore.fetchPortfolioById(id)
  }
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
</style>