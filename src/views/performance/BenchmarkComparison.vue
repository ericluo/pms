<template>
  <div class="benchmark-comparison">
    <el-page-header
      @back="goBack"
      content="基准对比"
    />
    
    <el-card class="comparison-card">
      <template #header>
        <span>投资组合与基准对比</span>
      </template>
      <div class="comparison-chart-container">
        <div ref="chartRef" class="comparison-chart"></div>
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
      data: ['投资组合', '沪深300', '中证500']
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
        data: [0, 2.1, 3.5, 5.2, 7.8, 10.2, 12.5, 14.1, 13.8, 14.5, 15.2, 15.67]
      },
      {
        name: '沪深300',
        type: 'line',
        data: [0, 1.5, 2.8, 4.1, 5.5, 7.2, 8.5, 9.8, 10.2, 10.8, 11.5, 12.1]
      },
      {
        name: '中证500',
        type: 'line',
        data: [0, 1.2, 2.5, 3.8, 5.2, 6.8, 8.1, 9.5, 9.8, 10.5, 11.2, 11.8]
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
.benchmark-comparison {
  width: 100%;
  padding: 20px 0;
}

.comparison-card {
  margin-top: 20px;
}

.comparison-chart-container {
  width: 100%;
  height: 400px;
}

.comparison-chart {
  width: 100%;
  height: 100%;
}
</style>