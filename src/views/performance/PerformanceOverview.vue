<template>
  <div class="performance-overview">
    <el-page-header
      @back="goBack"
      content="业绩概览"
    />
    
    <el-card class="performance-card">
      <template #header>
        <span>业绩指标</span>
      </template>
      <div class="performance-metrics">
        <el-statistic
          title="总收益率"
          :value="totalReturn"
          :precision="2"
          suffix="%"
          :value-style="{ color: totalReturn >= 0 ? '#67C23A' : '#F56C6C' }"
        />
        <el-statistic
          title="年化收益率"
          :value="annualReturn"
          :precision="2"
          suffix="%"
          :value-style="{ color: annualReturn >= 0 ? '#67C23A' : '#F56C6C' }"
        />
        <el-statistic
          title="最大回撤"
          :value="maxDrawdown"
          :precision="2"
          suffix="%"
          :value-style="{ color: '#F56C6C' }"
        />
        <el-statistic
          title="夏普比率"
          :value="sharpeRatio"
          :precision="2"
        />
      </div>
    </el-card>
    
    <el-card class="chart-card" style="margin-top: 20px;">
      <template #header>
        <span>业绩走势</span>
      </template>
      <div class="chart-container">
        <div ref="chartRef" class="chart"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const totalReturn = ref(15.67)
const annualReturn = ref(12.34)
const maxDrawdown = ref(8.92)
const sharpeRatio = ref(1.25)

const goBack = () => {
  router.back()
}

const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['投资组合', '基准']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: '投资组合',
        type: 'line',
        stack: 'Total',
        data: [0, 2.1, 3.5, 5.2, 7.8, 10.2, 12.5, 14.1, 13.8, 14.5, 15.2, 15.67]
      },
      {
        name: '基准',
        type: 'line',
        stack: 'Total',
        data: [0, 1.5, 2.8, 4.1, 5.5, 7.2, 8.5, 9.8, 10.2, 10.8, 11.5, 12.1]
      }
    ]
  }
  
  chart.setOption(option)
}

const handleResize = () => {
  chart?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<style scoped>
.performance-overview {
  width: 100%;
  padding: 20px 0;
}

.performance-card {
  margin-top: 20px;
}

.performance-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.chart-card {
  margin-top: 20px;
}

.chart-container {
  width: 100%;
  height: 400px;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>