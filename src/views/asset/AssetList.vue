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
          <el-input
            v-model="searchQuery"
            placeholder="搜索资产"
            prefix-icon="el-icon-search"
            style="width: 200px"
          />
        </div>
      </template>
      
      <el-table :data="filteredAssets" style="width: 100%">
        <el-table-column prop="code" label="资产代码" />
        <el-table-column prop="name" label="资产名称" />
        <el-table-column prop="type" label="资产类型" />
        <el-table-column prop="market" label="市场" />
        <el-table-column prop="industry" label="行业" />
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="primary" size="small" @click="goToDetail(scope.row.id)">
              查看
            </el-button>
            <el-button size="small" @click="goToEdit(scope.row.id)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteAsset(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import type { Asset } from '@/types'

const router = useRouter()

const searchQuery = ref('')

const assets = ref<Asset[]>([
  {
    id: 1,
    code: '600000',
    name: '浦发银行',
    type: '股票',
    market: 'A股',
    industry: '银行',
    created_at: '2024-01-01',
    updated_at: '2024-01-01'
  },
  {
    id: 2,
    code: '000001',
    name: '平安银行',
    type: '股票',
    market: 'A股',
    industry: '银行',
    created_at: '2024-01-02',
    updated_at: '2024-01-02'
  }
])

const filteredAssets = computed(() => {
  if (!searchQuery.value) {
    return assets.value
  }
  return assets.value.filter(asset => 
    asset.name.includes(searchQuery.value) || asset.code.includes(searchQuery.value)
  )
})

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

const deleteAsset = (id: number) => {
  // 删除资产逻辑
  console.log('删除资产:', id)
}
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
</style>