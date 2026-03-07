<template>
  <div class="asset-add">
    <el-page-header
      @back="goBack"
      content="添加资产"
    />
    
    <el-card class="asset-add-card">
      <el-form
        ref="assetFormRef"
        :model="assetForm"
        :rules="assetRules"
        class="asset-form"
      >
        <el-form-item prop="code">
          <el-input v-model="assetForm.code" placeholder="请输入资产代码" :disabled="assetForm.type === 'cash'" />
        </el-form-item>
        
        <el-form-item prop="name">
          <el-input v-model="assetForm.name" placeholder="请输入资产名称" />
        </el-form-item>
        
        <el-form-item prop="type">
          <el-select v-model="assetForm.type" placeholder="请选择资产类型" @change="handleTypeChange">
            <el-option label="股票" value="stock" />
            <el-option label="基金" value="fund" />
            <el-option label="债券" value="bond" />
            <el-option label="现金" value="cash" />
          </el-select>
        </el-form-item>
        
        <el-form-item prop="market" v-if="assetForm.type !== 'cash'">
          <el-select v-model="assetForm.market" placeholder="请选择市场">
            <el-option label="A股" value="A股" />
            <el-option label="港股" value="港股" />
            <el-option label="美股" value="美股" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <el-form-item prop="industry" v-if="assetForm.type !== 'cash'">
          <el-input v-model="assetForm.industry" placeholder="请输入所属行业" />
        </el-form-item>
        
        <el-form-item prop="interest_rate" v-if="assetForm.type === 'cash'">
          <el-input-number v-model="assetForm.interest_rate" :precision="4" :step="0.0001" :min="0" :max="1" placeholder="请输入年化利率(0-1)" />
          <span style="margin-left: 10px;">例如: 0.025 表示年化2.5%</span>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleAdd" :loading="loading">添加</el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createAsset } from '@/api/services/asset'
import { ElMessage } from 'element-plus'

const router = useRouter()

const assetFormRef = ref()
const loading = ref(false)

const assetForm = ref({
  code: '',
  name: '',
  type: 'stock',
  market: 'A股',
  industry: '',
  interest_rate: undefined as number | undefined
})

const assetRules = {
  code: [
    { required: true, message: '请输入资产代码', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入资产名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择资产类型', trigger: 'change' }
  ]
}

const handleTypeChange = (type: string) => {
  if (type === 'cash') {
    assetForm.value.code = 'CASH-' + Date.now()
    assetForm.value.market = ''
    assetForm.value.industry = ''
  } else if (!assetForm.value.market) {
    assetForm.value.market = 'A股'
  }
}

const handleAdd = async () => {
  if (!assetFormRef.value) return
  
  try {
    await assetFormRef.value.validate()
    loading.value = true
    
    const data = { ...assetForm.value }
    if (data.type !== 'cash') {
      delete data.interest_rate
    }
    
    await createAsset(data)
    ElMessage.success('资产添加成功')
    router.push('/asset')
  } catch (error: any) {
    console.error('添加资产失败:', error)
    ElMessage.error(error?.message || '添加资产失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.asset-add {
  width: 100%;
  padding: 20px 0;
}

.asset-add-card {
  margin-top: 20px;
}

.asset-form {
  width: 100%;
  max-width: 600px;
}
</style>