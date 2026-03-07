<template>
  <div class="portfolio-edit">
    <el-page-header
      @back="goBack"
      content="编辑投资组合"
    />
    
    <el-card class="portfolio-edit-card">
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
          <el-button type="primary" @click="handleUpdate">更新</el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usePortfolioStore } from '@/store/modules/portfolio'

const router = useRouter()
const route = useRoute()
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

const handleUpdate = async () => {
  if (!portfolioFormRef.value) return
  
  try {
    await portfolioFormRef.value.validate()
    const id = Number(route.params.id)
    
    await portfolioStore.updateExistingPortfolio(id, portfolioForm.value)
    router.push(`/portfolio/${id}`)
  } catch (error) {
    console.error('更新投资组合失败:', error)
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    // 获取投资组合详情
    // portfolioStore.fetchPortfolioById(id)
    // 模拟数据
    portfolioForm.value = {
      name: '我的股票组合',
      description: '这是我的股票投资组合',
      benchmark: '沪深300',
      risk_level: '中风险',
      is_default: false
    }
  }
})
</script>

<style scoped>
.portfolio-edit {
  width: 100%;
  padding: 20px 0;
}

.portfolio-edit-card {
  margin-top: 20px;
}

.portfolio-form {
  width: 100%;
  max-width: 600px;
}
</style>