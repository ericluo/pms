<template>
  <div class="portfolio-list">
    <el-page-header
      @back="goBack"
      content="投资组合列表"
    >
      <template #extra>
        <el-button type="primary" @click="goToCreate">
          <el-icon><Plus /></el-icon>
          <span>创建投资组合</span>
        </el-button>
      </template>
    </el-page-header>
    
    <el-card class="portfolio-list-card">
      <template #header>
        <div class="card-header">
          <span>我的投资组合</span>
          <el-input
            v-model="searchQuery"
            placeholder="搜索投资组合"
            prefix-icon="el-icon-search"
            style="width: 200px"
          />
        </div>
      </template>
      
      <el-table :data="filteredPortfolios" style="width: 100%">
        <el-table-column label="组合名称">
          <template #default="scope">
            <div class="portfolio-name">
              <span>{{ scope.row.name }}</span>
              <el-tag v-if="scope.row.is_default" size="small" type="primary" effect="dark">默认</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="benchmark" label="业绩基准" />
        <el-table-column prop="risk_level" label="风险等级" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button type="primary" size="small" @click="goToDetail(scope.row.id)">
              查看
            </el-button>
            <el-button size="small" @click="goToEdit(scope.row.id)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deletePortfolio(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePortfolioStore } from '@/store/modules/portfolio'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()
const portfolioStore = usePortfolioStore()

const searchQuery = ref('')

const filteredPortfolios = computed(() => {
  if (!searchQuery.value) {
    return portfolioStore.portfolios
  }
  return portfolioStore.portfolios.filter(portfolio => 
    portfolio.name.includes(searchQuery.value)
  )
})

const goBack = () => {
  router.back()
}

const goToCreate = () => {
  router.push('/portfolio/create')
}

const goToDetail = (id: number) => {
  router.push(`/portfolio/${id}`)
}

const goToEdit = (id: number) => {
  router.push(`/portfolio/${id}/edit`)
}

const deletePortfolio = (id: number) => {
  // 删除投资组合逻辑
  console.log('删除投资组合:', id)
}

onMounted(() => {
  // 获取投资组合列表
  portfolioStore.fetchPortfolios()
})
</script>

<style scoped>
.portfolio-list {
  width: 100%;
  padding: 20px 0;
}

.portfolio-list-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.portfolio-name {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>