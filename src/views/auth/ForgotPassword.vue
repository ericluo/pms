<template>
  <div class="forgot-password-container">
    <div class="forgot-password-form-wrapper">
      <div class="forgot-password-header">
        <h2>PMS</h2>
        <p>投资组合管理系统</p>
        <h3>忘记密码</h3>
      </div>
      
      <el-form
        ref="forgotPasswordFormRef"
        :model="forgotPasswordForm"
        :rules="forgotPasswordRules"
        class="forgot-password-form"
      >
        <el-form-item prop="email">
          <el-input
            v-model="forgotPasswordForm.email"
            placeholder="请输入邮箱"
            prefix-icon="el-icon-mail"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="forgot-password-button"
            :loading="loading"
            @click="handleForgotPassword"
          >
            发送重置链接
          </el-button>
        </el-form-item>
        
        <div class="form-footer">
          <span>想起密码了？</span>
          <el-link type="primary" :underline="false" @click="goToLogin">立即登录</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { forgotPassword } from '@/api/services/auth'

const router = useRouter()

const forgotPasswordFormRef = ref()
const loading = ref(false)

const forgotPasswordForm = ref({
  email: ''
})

const forgotPasswordRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

const handleForgotPassword = async () => {
  if (!forgotPasswordFormRef.value) return
  
  try {
    await forgotPasswordFormRef.value.validate()
    loading.value = true
    
    await forgotPassword(forgotPasswordForm.value.email)
    
    // 发送成功后跳转到登录页面
    router.push('/auth/login')
  } catch (error) {
    console.error('发送重置链接失败:', error)
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/auth/login')
}
</script>

<style scoped>
.forgot-password-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.forgot-password-form-wrapper {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.forgot-password-header {
  text-align: center;
  margin-bottom: 30px;
}

.forgot-password-header h2 {
  margin: 0 0 5px 0;
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
}

.forgot-password-header p {
  margin: 0 0 20px 0;
  font-size: 14px;
  color: #909399;
}

.forgot-password-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.forgot-password-form {
  width: 100%;
}

.forgot-password-button {
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
  .forgot-password-form-wrapper {
    padding: 30px 20px;
    margin: 0 20px;
  }
}
</style>