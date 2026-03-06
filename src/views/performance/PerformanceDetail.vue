<template>
  <div class="performance-detail">
    <el-page-header
      @back="goBack"
      content="业绩详细分析"
    />
    
    <el-card class="performance-details-card">
      <template #header>
        <span>详细业绩指标</span>
      </template>
      <el-descriptions :column="2">
        <el-descriptions-item label="总收益率">15.67%</el-descriptions-item>
        <el-descriptions-item label="年化收益率">12.34%</el-descriptions-item>
        <el-descriptions-item label="最大回撤">8.92%</el-descriptions-item>
        <el-descriptions-item label="夏普比率">1.25</el-descriptions-item>
        <el-descriptions-item label="波动率">15.2%</el-descriptions-item>
        <el-descriptions-item label="信息比率">0.85</el-descriptions-item>
        <el-descriptions-item label="阿尔法">3.2%</el-descriptions-item>
        <el-descriptions-item label="贝塔">0.95</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.performance-detail {
  width: 100%;
  padding: 20px 0;
}

.performance-details-card {
  margin-top: 20px;
}
</style>