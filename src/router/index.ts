import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Layout from '@/components/layout/Layout.vue'

const routes: Array<RouteRecordRaw> = [
  // 认证路由
  {
    path: '/auth',
    component: () => import('@/views/auth/AuthLayout.vue'),
    children: [
      { path: 'login', component: () => import('@/views/auth/Login.vue') },
      { path: 'register', component: () => import('@/views/auth/Register.vue') },
      { path: 'forgot-password', component: () => import('@/views/auth/ForgotPassword.vue') },
      { path: 'reset-password', component: () => import('@/views/auth/ResetPassword.vue') }
    ]
  },
  // 主路由
  {
    path: '/',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      // 投资组合
      {
        path: 'portfolio',
        component: () => import('@/views/portfolio/PortfolioLayout.vue'),
        children: [
          { path: '', component: () => import('@/views/portfolio/PortfolioList.vue') },
          { path: 'create', component: () => import('@/views/portfolio/PortfolioCreate.vue') },
          { path: ':id', component: () => import('@/views/portfolio/PortfolioDetail.vue') },
          { path: ':id/edit', component: () => import('@/views/portfolio/PortfolioEdit.vue') }
        ]
      },
      // 资产管理
      {
        path: 'asset',
        component: () => import('@/views/asset/AssetLayout.vue'),
        children: [
          { path: '', component: () => import('@/views/asset/AssetList.vue') },
          { path: 'add', component: () => import('@/views/asset/AssetAdd.vue') },
          { path: ':id', component: () => import('@/views/asset/AssetDetail.vue') },
          { path: ':id/edit', component: () => import('@/views/asset/AssetEdit.vue') }
        ]
      },
      // 业绩分析
      {
        path: 'performance',
        component: () => import('@/views/performance/PerformanceLayout.vue'),
        children: [
          { path: '', component: () => import('@/views/performance/PerformanceOverview.vue') },
          { path: 'detail', component: () => import('@/views/performance/PerformanceDetail.vue') },
          { path: 'risk', component: () => import('@/views/performance/RiskAnalysis.vue') },
          { path: 'comparison', component: () => import('@/views/performance/BenchmarkComparison.vue') }
        ]
      },
      // 市场数据
      {
        path: 'market',
        component: () => import('@/views/market/MarketLayout.vue'),
        children: [
          { path: '', component: () => import('@/views/market/MarketOverview.vue') },
          { path: 'stock', component: () => import('@/views/market/StockMarket.vue') },
          { path: 'fund', component: () => import('@/views/market/FundMarket.vue') },
          { path: 'industry', component: () => import('@/views/market/IndustrySector.vue') },
          { path: 'news', component: () => import('@/views/market/MarketNews.vue') }
        ]
      },
      // 现金管理
      {
        path: 'cash',
        component: () => import('@/views/cash/CashLayout.vue'),
        children: [
          { path: '', component: () => import('@/views/cash/CashBalance.vue') },
          { path: 'flow', component: () => import('@/views/cash/CashFlow.vue') },
          { path: 'plan', component: () => import('@/views/cash/FundPlan.vue') }
        ]
      },
      // 报告生成
      {
        path: 'report',
        component: () => import('@/views/report/ReportLayout.vue'),
        children: [
          { path: '', component: () => import('@/views/report/ReportList.vue') },
          { path: 'create', component: () => import('@/views/report/ReportCreate.vue') },
          { path: ':id', component: () => import('@/views/report/ReportDetail.vue') }
        ]
      },
      // 首页
      { path: '', redirect: '/portfolio' }
    ]
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const token = localStorage.getItem('token')
  
  if (requiresAuth && !token) {
    next('/auth/login')
  } else {
    next()
  }
})

export default router