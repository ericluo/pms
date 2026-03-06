<template>
  <div class="cash-flow">
    <el-page-header
      @back="goBack"
      content="现金流水"
    />
    
    <el-card class="cash-flow-card">
      <template #header>
        <div class="card-header">
          <span>现金流水记录</span>
          <el-button type="primary" size="small" @click="addCashFlow">
            <el-icon><Plus /></el-icon>
            <span>添加流水</span>
          </el-button>
        </div>
      </template>
      <el-table :data="cashFlows" style="width: 100%">
        <el-table-column prop="transaction_date" label="日期" />
        <el-table-column prop="type" label="类型" />
        <el-table-column prop="amount" label="金额" :formatter="formatAmount" />
        <el-table-column prop="description" label="描述" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()

const cashFlows = ref([
  {
    id: 1,
    portfolio_id: 1,
    type: '存入',
    amount: 5000.00,
    description: '工资收入',
    transaction_date: '2024-01-15',
    created_at: '2024-01-15'
  },
  {
    id: 2,
    portfolio_id: 1,
    type: '取出',
    amount: 2000.00,
    description: '日常消费',
    transaction_date: '2024-01-10',
    created_at: '2024-01-10'
  },
  {
    id: 3,
    portfolio_id: 1,
    type: '分红',
    amount: 1000.00,
    description: '股票分红',
    transaction_date: '2024-01-05',
    created_at: '2024-01-05'
  },
  {
    id: 4,
    portfolio_id: 1,
    type: '存入',
    amount: 10000.00,
    description: '年终奖',
    transaction_date: '2023-12-31',
    created_at: '2023-12-31'
  },
  {
    id: 5,
    portfolio_id: 1,
    type: '取出',
    amount: 3000.00,
    description: '房租',
    transaction_date: '2023-12-20',
    created_at: '2023-12-20'
  }
])

const formatAmount = (row: any, _column: any, cellValue: number) => {
  const type = row.type
  if (type === '存入' || type === '分红') {
    return `<span style="color: #67C23A">+${cellValue}</span>`
  } else {
    return `<span style="color: #F56C6C">-${cellValue}</span>`
  }
}

const goBack = () => {
  router.back()
}

const addCashFlow = () => {
  // 添加现金流水逻辑
  console.log('添加现金流水')
}
</script>

<style scoped>
.cash-flow {
  width: 100%;
  padding: 20px 0;
}

.cash-flow-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>