import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getPortfolios, getPortfolioById, createPortfolio, updatePortfolio, deletePortfolio } from '@/api/services/portfolio'
import type { Portfolio, Holding } from '@/types'

export const usePortfolioStore = defineStore('portfolio', () => {
  const portfolios = ref<Portfolio[]>([])
  const currentPortfolio = ref<Portfolio | null>(null)
  const holdings = ref<Holding[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const totalValue = computed(() => {
    return holdings.value.reduce((sum, holding) => {
      const value = parseFloat(holding.value.toString()) || 0
      return sum + value
    }, 0)
  })

  async function fetchPortfolios() {
    loading.value = true
    error.value = null
    try {
      const response = await getPortfolios()
      portfolios.value = response
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function fetchPortfolioById(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await getPortfolioById(id)
      currentPortfolio.value = response.portfolio
      holdings.value = response.holdings
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function createNewPortfolio(portfolioData: Partial<Portfolio>) {
    loading.value = true
    error.value = null
    try {
      const response = await createPortfolio(portfolioData)
      portfolios.value.push(response)
      return response
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateExistingPortfolio(id: number, portfolioData: Partial<Portfolio>) {
    loading.value = true
    error.value = null
    try {
      const response = await updatePortfolio(id, portfolioData)
      const index = portfolios.value.findIndex(p => p.id === id)
      if (index !== -1) {
        portfolios.value[index] = response
      }
      if (currentPortfolio.value?.id === id) {
        currentPortfolio.value = response
      }
      return response
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteExistingPortfolio(id: number) {
    loading.value = true
    error.value = null
    try {
      await deletePortfolio(id)
      portfolios.value = portfolios.value.filter(p => p.id !== id)
      if (currentPortfolio.value?.id === id) {
        currentPortfolio.value = null
        holdings.value = []
      }
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    portfolios,
    currentPortfolio,
    holdings,
    loading,
    error,
    totalValue,
    fetchPortfolios,
    fetchPortfolioById,
    createNewPortfolio,
    updateExistingPortfolio,
    deleteExistingPortfolio
  }
})