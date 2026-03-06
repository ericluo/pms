<template>
  <div class="top-nav">
    <!-- 左侧菜单按钮（移动端） -->
    <div class="top-nav-left">
      <el-button
        type="primary"
        circle
        plain
        size="small"
        class="menu-toggle"
        @click="toggleSidebar"
      >
        <el-icon><Menu /></el-icon>
      </el-button>
    </div>
    
    <!-- 右侧用户信息 -->
    <div class="top-nav-right">
      <el-dropdown trigger="click">
        <div class="user-info">
          <el-avatar :size="32" :src="userAvatar"></el-avatar>
          <span class="user-name">{{ userName }}</span>
          <el-icon class="arrow-icon"><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="goToProfile">
              <el-icon><User /></el-icon>
              <span>个人资料</span>
            </el-dropdown-item>
            <el-dropdown-item @click="goToSettings">
              <el-icon><Setting /></el-icon>
              <span>设置</span>
            </el-dropdown-item>
            <el-dropdown-item divided @click="logout">
              <el-icon><SwitchButton /></el-icon>
              <span>退出登录</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { Menu, ArrowDown, User, Setting, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const userAvatar = ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')
const userName = ref('用户名')

// 切换侧边栏（移动端）
const toggleSidebar = () => {
  const sidebar = document.querySelector('.layout-sidebar')
  if (sidebar) {
    sidebar.classList.toggle('open')
  }
}

// 跳转到个人资料
const goToProfile = () => {
  // 跳转到个人资料页面
  console.log('跳转到个人资料页面')
}

// 跳转到设置页面
const goToSettings = () => {
  // 跳转到设置页面
  console.log('跳转到设置页面')
}

// 退出登录
const logout = async () => {
  try {
    await userStore.logoutUser()
    router.push('/auth/login')
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}

// 初始化用户信息
const initUserInfo = async () => {
  try {
    await userStore.fetchUserInfo()
    if (userStore.user) {
      userName.value = userStore.user.name || userStore.user.username
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

onMounted(() => {
  initUserInfo()
})
</script>

<style scoped>
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.top-nav-left {
  display: none;
}

.top-nav-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 10px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.user-info:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.user-name {
  margin: 0 10px;
  font-size: 14px;
  font-weight: 500;
}

.arrow-icon {
  font-size: 12px;
  transition: transform 0.3s ease;
}

.el-dropdown:hover .arrow-icon {
  transform: rotate(180deg);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .top-nav-left {
    display: block;
  }
  
  .user-name {
    display: none;
  }
}
</style>