<template>
  <div class="layout">
    <el-container class="layout-container">
      <!-- 侧边栏 -->
      <el-aside width="200px" class="layout-sidebar">
        <Sidebar />
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container class="layout-main">
        <!-- 顶部导航 -->
        <el-header height="60px" class="layout-header">
          <TopNav />
        </el-header>
        
        <!-- 内容区域 -->
        <el-main class="layout-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import Sidebar from './Sidebar.vue'
import TopNav from './TopNav.vue'
</script>

<style scoped>
.layout {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.layout-container {
  height: 100%;
}

.layout-sidebar {
  background-color: #2c3e50;
  color: white;
  height: 100%;
  overflow-y: auto;
}

.layout-main {
  height: 100%;
  background-color: #f5f7fa;
}

.layout-header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
}

.layout-content {
  padding: 20px;
  overflow-y: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .layout-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 1000;
    height: 100vh;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .layout-sidebar.open {
    transform: translateX(0);
  }
  
  .layout-main {
    width: 100%;
  }
}
</style>