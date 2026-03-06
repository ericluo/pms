<template>
  <div class="report-list">
    <el-page-header
      @back="goBack"
      content="报告列表"
    >
      <template #extra>
        <el-button type="primary" @click="goToCreate">
          <el-icon><Plus /></el-icon>
          <span>创建报告</span>
        </el-button>
      </template>
    </el-page-header>
    
    <el-card class="report-list-card">
      <template #header>
        <span>我的报告</span>
      </template>
      <el-table :data="reports" style="width: 100%">
        <el-table-column prop="name" label="报告名称" />
        <el-table-column prop="type" label="报告类型" />
        <el-table-column prop="generated_at" label="生成时间" />
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button type="primary" size="small" @click="goToDetail(scope.row.id)">
              查看
            </el-button>
            <el-button size="small" @click="exportReport(scope.row.id)">
              导出
            </el-button>
            <el-button type="danger" size="small" @click="deleteReport(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()

const reports = ref([
  {
    id: 1,
    user_id: 1,
    portfolio_id: 1,
    name: '2023年投资组合报告',
    type: '年度报告',
    generated_at: '2024-01-01',
    created_at: '2024-01-01'
  },
  {
    id: 2,
    user_id: 1,
    portfolio_id: 1,
    name: '2023年第四季度报告',
    type: '季度报告',
    generated_at: '2024-01-01',
    created_at: '2024-01-01'
  },
  {
    id: 3,
    user_id: 1,
    portfolio_id: 1,
    name: '投资组合风险分析报告',
    type: '风险报告',
    generated_at: '2023-12-15',
    created_at: '2023-12-15'
  }
])

const goBack = () => {
  router.back()
}

const goToCreate = () => {
  router.push('/report/create')
}

const goToDetail = (id: number) => {
  router.push(`/report/${id}`)
}

const exportReport = (id: number) => {
  // 导出报告逻辑
  console.log('导出报告:', id)
}

const deleteReport = (id: number) => {
  // 删除报告逻辑
  console.log('删除报告:', id)
}
</script>

<style scoped>
.report-list {
  width: 100%;
  padding: 20px 0;
}

.report-list-card {
  margin-top: 20px;
}
</style>