<template>
  <div class="portfolio-create">
    <el-page-header
      @back="goBack"
      content="创建投资组合"
    />
    
    <el-card class="portfolio-create-card">
      <el-form
        ref="portfolioFormRef"
        :model="portfolioForm"
        :rules="portfolioRules"
        class="portfolio-form"
      >
        <el-form-item prop="name">
          <el-input v-model="portfolioForm.name" placeholder="请输入组合名称" />
        </el-form-item>
        
        <el-form-item prop="description">
          <el-input
            v-model="portfolioForm.description"
            type="textarea"
            placeholder="请输入组合描述"
            rows="3"
          />
        </el-form-item>
        
        <el-form-item prop="benchmark">
          <el-select v-model="portfolioForm.benchmark" placeholder="请选择业绩基准">
            <el-option label="沪深300" value="沪深300" />
            <el-option label="中证500" value="中证500" />
            <el-option label="创业板指" value="创业板指" />
            <el-option label="上证指数" value="上证指数" />
          </el-select>
        </el-form-item>
        
        <el-form-item prop="risk_level">
          <el-select v-model="portfolioForm.risk_level" placeholder="请选择风险等级">
            <el-option label="低风险" value="低风险" />
            <el-option label="中风险" value="中风险" />
            <el-option label="高风险" value="高风险" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="portfolioForm.is_default">设为默认投资组合</el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleCreate">创建</el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePortfolioStore } from '@/store/modules/portfolio'

const router = useRouter()
const portfolioStore = usePortfolioStore()

const portfolioFormRef = ref()

const portfolioForm = ref({
  name: '',
  description: '',
  benchmark: '',
  risk_level: '',
  is_default: false
})

const portfolioRules = {
  name: [
    { required: true, message: '请输入组合名称', trigger: 'blur' },
    { min: 1, max: 100, message: '组合名称长度应在1-100之间', trigger: 'blur' }
  ],
  benchmark: [
    { required: true, message: '请选择业绩基准', trigger: 'change' }
  ],
  risk_level: [
    { required: true, message: '请选择风险等级', trigger: 'change' }
  ]
}

const handleCreate = async () => {
  if (!portfolioFormRef.value) return
  
  try {
    await portfolioFormRef.value.validate()
    
    await portfolioStore.createNewPortfolio(portfolioForm.value)
    router.push('/portfolio')
  } catch (error: any) {
    console.error('创建投资组合失败:', error)
    alert('创建投资组合失败: ' + (error?.message || '未知错误'))
  }
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.portfolio-create {
  width: 100%;
  padding: 20px 0;
}

.portfolio-create-card {
  margin-top: 20px;
}

.portfolio-form {
  width: 100%;
  max-width: 600px;
}
</style>