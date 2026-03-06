<template>
  <div class="reset-password-container">
    <div class="reset-password-form-wrapper">
      <div class="reset-password-header">
        <h2>PMS</h2>
        <p>投资组合管理系统</p>
        <h3>重置密码</h3>
      </div>
      
      <el-form
        ref="resetPasswordFormRef"
        :model="resetPasswordForm"
        :rules="resetPasswordRules"
        class="reset-password-form"
      >
        <el-form-item prop="password">
          <el-input
            v-model="resetPasswordForm.password"
            type="password"
            placeholder="请输入新密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="resetPasswordForm.confirmPassword"
            type="password"
            placeholder="请确认新密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="reset-password-button"
            :loading="loading"
            @click="handleResetPassword"
          >
            重置密码
          </el-button>
        </el-form-item>
        
        <div class="form-footer">
          <span>返回登录？</span>
          <el-link type="primary" :underline="false" @click="goToLogin">立即登录</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { resetPassword } from '@/api/services/auth'

const router = useRouter()
const route = useRoute()

const resetPasswordFormRef = ref()
const loading = ref(false)
const token = ref('')

const resetPasswordForm = ref({
  password: '',
  confirmPassword: ''
})

const resetPasswordRules = {
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: string, callback: any) => {
        if (value !== resetPasswordForm.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const handleResetPassword = async () => {
  if (!resetPasswordFormRef.value) return
  
  try {
    await resetPasswordFormRef.value.validate()
    loading.value = true
    
    await resetPassword(token.value, resetPasswordForm.value.password)
    
    // 重置成功后跳转到登录页面
    router.push('/auth/login')
  } catch (error) {
    console.error('重置密码失败:', error)
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/auth/login')
}

onMounted(() => {
  // 从URL参数中获取token
  token.value = route.query.token as string || ''
  if (!token.value) {
    // 如果没有token，跳转到登录页面
    router.push('/auth/login')
  }
})
</script>

<style scoped>
.reset-password-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.reset-password-form-wrapper {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.reset-password-header {
  text-align: center;
  margin-bottom: 30px;
}

.reset-password-header h2 {
  margin: 0 0 5px 0;
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
}

.reset-password-header p {
  margin: 0 0 20px 0;
  font-size: 14px;
  color: #909399;
}

.reset-password-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.reset-password-form {
  width: 100%;
}

.reset-password-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

.form-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #909399;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .reset-password-form-wrapper {
    padding: 30px 20px;
    margin: 0 20px;
  }
}
</style>