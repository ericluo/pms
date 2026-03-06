<template>
  <div class="report-detail">
    <el-page-header
      @back="goBack"
      :content="report.name"
    />
    
    <el-card class="report-info-card">
      <template #header>
        <span>报告信息</span>
      </template>
      <el-descriptions :column="3">
        <el-descriptions-item label="报告名称">{{ report.name }}</el-descriptions-item>
        <el-descriptions-item label="报告类型">{{ report.type }}</el-descriptions-item>
        <el-descriptions-item label="生成时间">{{ report.generated_at }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ report.created_at }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
    
    <el-card class="report-content-card" style="margin-top: 20px;">
      <template #header>
        <span>报告内容</span>
      </template>
      <div class="report-content">
        <h3>投资组合概览</h3>
        <p>本报告提供了投资组合的详细分析，包括业绩表现、资产配置、风险评估等内容。</p>
        
        <h3>业绩表现</h3>
        <p>投资组合在过去一年的总收益率为15.67%，年化收益率为12.34%，超过基准收益率3.5个百分点。</p>
        
        <h3>资产配置</h3>
        <p>投资组合的资产配置如下：股票占比60%，基金占比30%，债券占比10%。</p>
        
        <h3>风险评估</h3>
        <p>投资组合的波动率为15.2%，最大回撤为8.92%，夏普比率为1.25，风险水平适中。</p>
      </div>
      <div class="report-actions" style="margin-top: 20px;">
        <el-button type="primary" @click="exportReport">导出报告</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const report = ref({
  id: 0,
  user_id: 0,
  portfolio_id: 0,
  name: '',
  type: '',
  generated_at: '',
  created_at: ''
})

const goBack = () => {
  router.back()
}

const exportReport = () => {
  // 导出报告逻辑
  console.log('导出报告:', report.value.id)
}

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    // 获取报告详情
    // 模拟数据
    report.value = {
      id: id,
      user_id: 1,
      portfolio_id: 1,
      name: '2023年投资组合报告',
      type: '年度报告',
      generated_at: '2024-01-01',
      created_at: '2024-01-01'
    }
  }
})
</script>

<style scoped>
.report-detail {
  width: 100%;
  padding: 20px 0;
}

.report-info-card {
  margin-top: 20px;
}

.report-content-card {
  margin-top: 20px;
}

.report-content {
  line-height: 1.6;
}

.report-content h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: 500;
}

.report-content p {
  margin-bottom: 15px;
}

.report-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>