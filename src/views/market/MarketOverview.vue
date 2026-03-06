<template>
  <div class="market-overview">
    <el-page-header
      @back="goBack"
      content="市场概览"
    />
    
    <el-card class="market-indices-card">
      <template #header>
        <span>市场指数</span>
      </template>
      <el-table :data="marketIndices" style="width: 100%">
        <el-table-column prop="name" label="指数名称" />
        <el-table-column prop="code" label="指数代码" />
        <el-table-column prop="current" label="当前值" />
        <el-table-column prop="change" label="涨跌幅" :formatter="formatChange" />
        <el-table-column prop="volume" label="成交量" />
      </el-table>
    </el-card>
    
    <el-card class="market-sectors-card" style="margin-top: 20px;">
      <template #header>
        <span>行业板块</span>
      </template>
      <div class="sector-chart-container">
        <div ref="sectorChartRef" class="sector-chart"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()

const sectorChartRef = ref<HTMLElement>()
let sectorChart: echarts.ECharts | null = null

const marketIndices = ref([
  {
    name: '上证指数',
    code: '000001.SH',
    current: 3500.25,
    change: 1.25,
    volume: '2.1亿'
  },
  {
    name: '深证成指',
    code: '399001.SZ',
    current: 14500.75,
    change: 0.85,
    volume: '1.8亿'
  },
  {
    name: '创业板指',
    code: '399006.SZ',
    current: 3200.50,
    change: 1.50,
    volume: '1.2亿'
  },
  {
    name: '沪深300',
    code: '000300.SH',
    current: 4800.30,
    change: 1.10,
    volume: '1.5亿'
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

const initSectorChart = () => {
  if (!sectorChartRef.value) return
  
  sectorChart = echarts.init(sectorChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [
      {
        name: '行业涨幅',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 3.2, name: '银行' },
          { value: 2.8, name: '科技' },
          { value: 2.5, name: '医药' },
          { value: 1.8, name: '消费' },
          { value: 1.5, name: '能源' },
          { value: 1.2, name: '房地产' }
        ]
      }
    ]
  }
  
  sectorChart.setOption(option)
}

const handleResize = () => {
  sectorChart?.resize()
}

onMounted(() => {
  initSectorChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  sectorChart?.dispose()
})
</script>

<style scoped>
.market-overview {
  width: 100%;
  padding: 20px 0;
}

.market-indices-card {
  margin-top: 20px;
}

.market-sectors-card {
  margin-top: 20px;
}

.sector-chart-container {
  width: 100%;
  height: 400px;
}

.sector-chart {
  width: 100%;
  height: 100%;
}
</style>