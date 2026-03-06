import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, register, logout, getUserInfo } from '@/api/services/auth'
import type { User } from '@/types'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function loginUser(credentials: { email: string; password: string }) {
    loading.value = true
    error.value = null
    try {
      const response = await login(credentials)
      token.value = response.token
      user.value = response.user
      localStorage.setItem('token', response.token)
      return response
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function registerUser(userData: { username: string; email: string; password: string; name: string }) {
    loading.value = true
    error.value = null
    try {
      const response = await register(userData)
      return response
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logoutUser() {
    try {
      await logout()
    } finally {
      user.value = null
      token.value = null
      localStorage.removeItem('token')
    }
  }

  async function fetchUserInfo() {
    if (!token.value) return
    
    loading.value = true
    error.value = null
    try {
      const response = await getUserInfo()
      user.value = response
    } catch (err: any) {
      error.value = err.message
      // 如果获取用户信息失败，清除token
      if (err.status === 401) {
        user.value = null
        token.value = null
        localStorage.removeItem('token')
      }
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    loginUser,
    registerUser,
    logoutUser,
    fetchUserInfo
  }
})