import http from '@/utils/http'
import type { User, LoginResponse } from '@/types'

// 登录
export async function login(credentials: { email: string; password: string }): Promise<LoginResponse> {
  const response = await http.post<{ access_token: string; token_type: string; user: User }>('/auth/login', credentials)
  return {
    token: response.access_token,
    user: response.user
  }
}

// 注册
export async function register(userData: { username: string; email: string; password: string; name: string }): Promise<{ message: string }> {
  return http.post('/auth/register', userData)
}

// 登出
export async function logout(): Promise<{ message: string }> {
  return http.post('/auth/logout')
}

// 获取当前用户信息
export async function getUserInfo(): Promise<User> {
  return http.get<User>('/auth/me')
}

// 忘记密码
export async function forgotPassword(email: string): Promise<{ message: string }> {
  return http.post('/auth/forgot-password', { email })
}

// 重置密码
export async function resetPassword(token: string, password: string): Promise<{ message: string }> {
  return http.post('/auth/reset-password', { token, password })
}