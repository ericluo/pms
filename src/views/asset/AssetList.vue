<template>
  <div class="asset-list">
    <el-page-header
      @back="goBack"
      content="资产列表"
    >
      <template #extra>
        <el-button type="primary" @click="goToAdd">
          <el-icon><Plus /></el-icon>
          <span>添加资产</span>
        </el-button>
      </template>
    </el-page-header>
    
    <el-card class="asset-list-card">
      <template #header>
        <div class="card-header">
          <span>我的资产</span>
          <div class="filters">
            <el-select v-model="typeFilter" placeholder="资产类型" clearable style="width: 120px; margin-right: 10px;">
              <el-option label="股票" value="stock" />
              <el-option label="基金" value="fund" />
              <el-option label="债券" value="bond" />
              <el-option label="现金" value="cash" />
            </el-select>
            <el-input
              v-model="searchQuery"
              placeholder="搜索资产"
              prefix-icon="el-icon-search"
              style="width: 200px"
            />
          </div>
        </div>
      </template>
      
      <el-table :data="filteredAssets" style="width: 100%" v-loading="loading">
        <el-table-column prop="code" label="资产代码" width="120" />
        <el-table-column prop="name" label="资产名称" />
        <el-table-column label="资产类型" width="100">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.type)">{{ getTypeName(scope.row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="market" label="市场" width="100" />
        <el-table-column prop="industry" label="行业" width="120" />
        <el-table-column prop="interest_rate" label="利率(%)" width="100">
          <template #default="scope">
            {{ scope.row.interest_rate ? scope.row.interest_rate + '%' : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button type="primary" size="small" @click="goToDetail(scope.row.id)">
              查看
            </el-button>
            <el-button size="small" @click="goToEdit(scope.row.id)">
              编辑
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
import { Plus } from '@element-plus/icons-vue'
import type { Asset } from '@/types'
import { getAssets } from '@/api/services/asset'

const router = useRouter()

const searchQuery = ref('')
const typeFilter = ref('')
const loading = ref(false)
const assets = ref<Asset[]>([])

const typeNames: Record<string, string> = {
  'stock': '股票',
  'fund': '基金',
  'bond': '债券',
  'cash': '现金'
}

const getTypeName = (type: string) => {
  return typeNames[type] || type
}

const getTypeTagType = (type: string) => {
  const tagTypes: Record<string, string> = {
    'stock': 'danger',
    'fund': 'success',
    'warning': 'bond',
    'cash': 'info'
  }
  return tagTypes[type] || ''
}

const filteredAssets = computed(() => {
  let result = assets.value
  
  if (typeFilter.value) {
    result = result.filter(asset => asset.type === typeFilter.value)
  }
  
  if (searchQuery.value) {
    result = result.filter(asset => 
      asset.name.includes(searchQuery.value) || 
      asset.code.includes(searchQuery.value)
    )
  }
  
  return result
})

const fetchAssets = async () => {
  loading.value = true
  try {
    const response = await getAssets()
    assets.value = response
  } catch (error) {
    console.error('获取资产列表失败:', error)
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.back()
}

const goToAdd = () => {
  router.push('/asset/add')
}

const goToDetail = (id: number) => {
  router.push(`/asset/${id}`)
}

const goToEdit = (id: number) => {
  router.push(`/asset/${id}/edit`)
}

onMounted(() => {
  fetchAssets()
})
</script>

<style scoped>
.asset-list {
  width: 100%;
  padding: 20px 0;
}

.asset-list-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters {
  display: flex;
  align-items: center;
}
</style>