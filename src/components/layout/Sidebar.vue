<template>
  <div class="sidebar">
    <!-- 品牌名称 -->
    <div class="sidebar-brand">
      <h2>PMS</h2>
      <p>投资组合管理系统</p>
    </div>
    
    <!-- 导航菜单 -->
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      background-color="#2c3e50"
      text-color="#fff"
      active-text-color="#409EFF"
      router
    >
      <el-menu-item index="/portfolio">
        <el-icon><House /></el-icon>
        <span>投资组合</span>
      </el-menu-item>
      
      <el-menu-item index="/asset">
        <el-icon><Goods /></el-icon>
        <span>资产管理</span>
      </el-menu-item>
      
      <el-menu-item index="/performance">
        <el-icon><DataLine /></el-icon>
        <span>业绩分析</span>
      </el-menu-item>
      
      <el-menu-item index="/market">
        <el-icon><TrendCharts /></el-icon>
        <span>市场数据</span>
      </el-menu-item>
      
      <el-menu-item index="/cash">
        <el-icon><Money /></el-icon>
        <span>现金管理</span>
      </el-menu-item>
      
      <el-menu-item index="/report">
        <el-icon><Document /></el-icon>
        <span>报告生成</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { House, Goods, DataLine, TrendCharts, Money, Document } from '@element-plus/icons-vue'

const route = useRoute()

const activeMenu = computed(() => {
  const path = route.path
  return path.split('/')[1] ? `/${path.split('/')[1]}` : '/portfolio'
})
</script>

<style scoped>
.sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.sidebar-brand {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;
}

.sidebar-brand h2 {
  margin: 0 0 5px 0;
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.sidebar-brand p {
  margin: 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
}

.sidebar-menu {
  flex: 1;
  border-right: none;
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
  margin: 0 10px;
  border-radius: 4px;
}

.sidebar-menu .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-menu .el-menu-item.is-active {
  background-color: rgba(64, 158, 255, 0.2);
}
</style>