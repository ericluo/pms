<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>页面不存在</h2>
      <p>抱歉，您访问的页面不存在或已被删除</p>
      <el-button type="primary" @click="goToHome">返回首页</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
.not-found {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.not-found-content {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.not-found-content h1 {
  margin: 0 0 20px 0;
  font-size: 72px;
  font-weight: bold;
  color: #409EFF;
}

.not-found-content h2 {
  margin: 0 0 10px 0;
  font-size: 24px;
  font-weight: 500;
  color: #303133;
}

.not-found-content p {
  margin: 0 0 30px 0;
  font-size: 16px;
  color: #909399;
}
</style>