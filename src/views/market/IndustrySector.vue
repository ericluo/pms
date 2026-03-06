<template>
  <div class="industry-sector">
    <el-page-header
      @back="goBack"
      content="行业板块"
    />
    
    <el-card class="industry-list-card">
      <template #header>
        <span>行业板块列表</span>
      </template>
      <el-table :data="industries" style="width: 100%">
        <el-table-column prop="name" label="行业名称" />
        <el-table-column prop="change" label="涨跌幅" :formatter="formatChange" />
        <el-table-column prop="volume" label="成交量" />
        <el-table-column prop="market_cap" label="总市值" />
        <el-table-column prop="leading_stock" label="龙头股" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const industries = ref([
  {
    name: '银行',
    change: 1.25,
    volume: '50亿',
    market_cap: '10万亿',
    leading_stock: '招商银行'
  },
  {
    name: '科技',
    change: 2.15,
    volume: '80亿',
    market_cap: '15万亿',
    leading_stock: '腾讯控股'
  },
  {
    name: '医药',
    change: 0.85,
    volume: '40亿',
    market_cap: '8万亿',
    leading_stock: '恒瑞医药'
  },
  {
    name: '消费',
    change: 1.55,
    volume: '60亿',
    market_cap: '12万亿',
    leading_stock: '贵州茅台'
  },
  {
    name: '能源',
    change: -0.55,
    volume: '30亿',
    market_cap: '6万亿',
    leading_stock: '中国石油'
  },
  {
    name: '房地产',
    change: 0.35,
    volume: '25亿',
    market_cap: '5万亿',
    leading_stock: '万科A'
  }
])

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
.industry-sector {
  width: 100%;
  padding: 20px 0;
}

.industry-list-card {
  margin-top: 20px;
}
</style>