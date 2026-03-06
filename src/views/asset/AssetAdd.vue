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
          <el-input v-model="assetForm.code" placeholder="请输入资产代码" />
        </el-form-item>
        
        <el-form-item prop="name">
          <el-input v-model="assetForm.name" placeholder="请输入资产名称" />
        </el-form-item>
        
        <el-form-item prop="type">
          <el-select v-model="assetForm.type" placeholder="请选择资产类型">
            <el-option label="股票" value="股票" />
            <el-option label="基金" value="基金" />
            <el-option label="债券" value="债券" />
            <el-option label="现金" value="现金" />
          </el-select>
        </el-form-item>
        
        <el-form-item prop="market">
          <el-select v-model="assetForm.market" placeholder="请选择市场">
            <el-option label="A股" value="A股" />
            <el-option label="港股" value="港股" />
            <el-option label="美股" value="美股" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        
        <el-form-item prop="industry">
          <el-input v-model="assetForm.industry" placeholder="请输入所属行业" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleAdd">添加</el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const assetFormRef = ref()

const assetForm = ref({
  code: '',
  name: '',
  type: '',
  market: '',
  industry: ''
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
  ],
  market: [
    { required: true, message: '请选择市场', trigger: 'change' }
  ]
}

const handleAdd = async () => {
  if (!assetFormRef.value) return
  
  try {
    await assetFormRef.value.validate()
    // 添加资产逻辑
    console.log('添加资产:', assetForm.value)
    router.push('/asset')
  } catch (error) {
    console.error('添加资产失败:', error)
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