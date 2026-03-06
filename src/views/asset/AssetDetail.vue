<template>
  <div class="asset-detail">
    <el-page-header
      @back="goBack"
      :content="asset.name"
    >
      <template #extra>
        <el-button @click="goToEdit">
          <el-icon><Edit /></el-icon>
          <span>编辑</span>
        </el-button>
      </template>
    </el-page-header>
    
    <el-card class="asset-info-card">
      <template #header>
        <span>资产信息</span>
      </template>
      <el-descriptions :column="3">
        <el-descriptions-item label="资产代码">{{ asset.code }}</el-descriptions-item>
        <el-descriptions-item label="资产名称">{{ asset.name }}</el-descriptions-item>
        <el-descriptions-item label="资产类型">{{ asset.type }}</el-descriptions-item>
        <el-descriptions-item label="市场">{{ asset.market }}</el-descriptions-item>
        <el-descriptions-item label="所属行业">{{ asset.industry || '无' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ asset.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ asset.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Edit } from '@element-plus/icons-vue'
import type { Asset } from '@/types'

const router = useRouter()
const route = useRoute()

const asset = ref<Asset>({
  id: 0,
  code: '',
  name: '',
  type: '',
  market: '',
  industry: '',
  created_at: '',
  updated_at: ''
})

const goBack = () => {
  router.back()
}

const goToEdit = () => {
  router.push(`/asset/${route.params.id}/edit`)
}

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    // 获取资产详情
    // 模拟数据
    asset.value = {
      id: id,
      code: '600000',
      name: '浦发银行',
      type: '股票',
      market: 'A股',
      industry: '银行',
      created_at: '2024-01-01',
      updated_at: '2024-01-01'
    }
  }
})
</script>

<style scoped>
.asset-detail {
  width: 100%;
  padding: 20px 0;
}

.asset-info-card {
  margin-top: 20px;
}
</style>