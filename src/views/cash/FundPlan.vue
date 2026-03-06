<template>
  <div class="fund-plan">
    <el-page-header
      @back="goBack"
      content="资金计划"
    />
    
    <el-card class="fund-plan-card">
      <template #header>
        <div class="card-header">
          <span>资金使用计划</span>
          <el-button type="primary" size="small" @click="addPlan">
            <el-icon><Plus /></el-icon>
            <span>添加计划</span>
          </el-button>
        </div>
      </template>
      <el-table :data="fundPlans" style="width: 100%">
        <el-table-column prop="name" label="计划名称" />
        <el-table-column prop="amount" label="金额" />
        <el-table-column prop="start_date" label="开始日期" />
        <el-table-column prop="end_date" label="结束日期" />
        <el-table-column prop="status" label="状态" />
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

const fundPlans = ref([
  {
    id: 1,
    name: '购房计划',
    amount: 500000.00,
    start_date: '2024-01-01',
    end_date: '2025-12-31',
    status: '进行中',
    description: '为购买新房积累资金'
  },
  {
    id: 2,
    name: '子女教育计划',
    amount: 200000.00,
    start_date: '2024-01-01',
    end_date: '2030-12-31',
    status: '进行中',
    description: '为子女教育积累资金'
  },
  {
    id: 3,
    name: '退休计划',
    amount: 1000000.00,
    start_date: '2024-01-01',
    end_date: '2040-12-31',
    status: '进行中',
    description: '为退休生活积累资金'
  }
])

const goBack = () => {
  router.back()
}

const addPlan = () => {
  // 添加资金计划逻辑
  console.log('添加资金计划')
}
</script>

<style scoped>
.fund-plan {
  width: 100%;
  padding: 20px 0;
}

.fund-plan-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>