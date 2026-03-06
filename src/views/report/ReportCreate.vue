<template>
  <div class="report-create">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>创建报告</span>
        </div>
      </template>
      
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="投资组合" prop="portfolio_id">
          <el-select v-model="form.portfolio_id" placeholder="请选择投资组合">
            <el-option
              v-for="portfolio in portfolios"
              :key="portfolio.id"
              :label="portfolio.name"
              :value="portfolio.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="报告类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择报告类型">
            <el-option label="月度报告" value="月度报告" />
            <el-option label="季度报告" value="季度报告" />
            <el-option label="年度报告" value="年度报告" />
            <el-option label="自定义报告" value="自定义报告" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="报告标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入报告标题" />
        </el-form-item>
        
        <el-form-item label="报告周期" prop="period">
          <el-date-picker
            v-model="form.period"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="包含内容">
          <el-checkbox-group v-model="form.content">
            <el-checkbox label="持仓分析">持仓分析</el-checkbox>
            <el-checkbox label="业绩分析">业绩分析</el-checkbox>
            <el-checkbox label="风险分析">风险分析</el-checkbox>
            <el-checkbox label="交易记录">交易记录</el-checkbox>
            <el-checkbox label="现金流水">现金流水</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm">生成报告</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { createReport } from '@/api/services/report'
import { getPortfolios } from '@/api/services/portfolio'
import type { Portfolio } from '@/types'

const router = useRouter()
const formRef = ref()

const portfolios = ref<Portfolio[]>([])

const form = reactive({
  portfolio_id: '',
  type: '',
  title: '',
  period: null as any,
  content: [] as string[]
})

const rules = {
  portfolio_id: [
    { required: true, message: '请选择投资组合', trigger: 'change' }
  ],
  type: [
    { required: true, message: '请选择报告类型', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入报告标题', trigger: 'blur' }
  ],
  period: [
    { required: true, message: '请选择报告周期', trigger: 'change' }
  ]
}

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const response = await createReport({
          portfolio_id: form.portfolio_id,
          type: form.type,
          title: form.title
        })
        
        ElMessage.success('报告生成成功')
        router.push('/report')
      } catch (error) {
        ElMessage.error('报告生成失败，请稍后重试')
      }
    } else {
      return false
    }
  })
}

const resetForm = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
}

onMounted(async () => {
  try {
    const response = await getPortfolios()
    portfolios.value = response
  } catch (error) {
    ElMessage.error('获取投资组合失败')
  }
})
</script>

<style scoped>
.report-create {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>