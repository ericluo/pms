<template>
  <div class="stock-market">
    <el-page-header
      @back="goBack"
      content="股票市场"
    />
    
    <el-card class="stock-list-card">
      <template #header>
        <div class="card-header">
          <span>股票列表</span>
          <el-input
            v-model="searchQuery"
            placeholder="搜索股票"
            prefix-icon="el-icon-search"
            style="width: 200px"
          />
        </div>
      </template>
      <el-table :data="filteredStocks" style="width: 100%">
        <el-table-column prop="code" label="股票代码" />
        <el-table-column prop="name" label="股票名称" />
        <el-table-column prop="current" label="当前价" />
        <el-table-column prop="change" label="涨跌幅" :formatter="formatChange" />
        <el-table-column prop="volume" label="成交量" />
        <el-table-column prop="market_cap" label="市值" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const searchQuery = ref('')

const stocks = ref([
  {
    code: '600000',
    name: '浦发银行',
    current: 10.50,
    change: 1.25,
    volume: '1.2亿',
    market_cap: '3000亿'
  },
  {
    code: '000001',
    name: '平安银行',
    current: 15.20,
    change: 0.85,
    volume: '8000万',
    market_cap: '2500亿'
  },
  {
    code: '601318',
    name: '中国平安',
    current: 45.60,
    change: -0.50,
    volume: '5000万',
    market_cap: '8000亿'
  },
  {
    code: '000858',
    name: '五粮液',
    current: 160.20,
    change: 2.10,
    volume: '3000万',
    market_cap: '6000亿'
  }
])

const filteredStocks = computed(() => {
  if (!searchQuery.value) {
    return stocks.value
  }
  return stocks.value.filter(stock => 
    stock.name.includes(searchQuery.value) || stock.code.includes(searchQuery.value)
  )
})

const formatChange = (_row: any, _column: any, cellValue: number) => {
  return cellValue >= 0 
    ? `<span style="color: #67C23A">+${cellValue}%</span>`
    : `<span style="color: #F56C6C">${cellValue}%</span>`
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.stock-market {
  width: 100%;
  padding: 20px 0;
}

.stock-list-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>