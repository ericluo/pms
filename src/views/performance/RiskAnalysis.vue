<template>
  <div class="risk-analysis">
    <el-page-header
      @back="goBack"
      content="风险分析"
    />
    
    <el-card class="risk-card">
      <template #header>
        <span>风险指标</span>
      </template>
      <div class="risk-metrics">
        <el-statistic
          title="波动率"
          :value="volatility"
          :precision="2"
          suffix="%"
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
        <el-statistic
          title="贝塔系数"
          :value="beta"
          :precision="2"
        />
      </div>
    </el-card>
    
    <el-card class="drawdown-card" style="margin-top: 20px;">
      <template #header>
        <span>最大回撤分析</span>
      </template>
      <div class="drawdown-chart-container">
        <div ref="drawdownChartRef" class="drawdown-chart"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()

const drawdownChartRef = ref<HTMLElement>()
let drawdownChart: echarts.ECharts | null = null

const volatility = ref(15.2)
const maxDrawdown = ref(8.92)
const sharpeRatio = ref(1.25)
const beta = ref(0.95)

const goBack = () => {
  router.back()
}

const initDrawdownChart = () => {
  if (!drawdownChartRef.value) return
  
  drawdownChart = echarts.init(drawdownChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis'
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
        name: '最大回撤',
        type: 'line',
        data: [0, -2.1, -3.5, -5.2, -7.8, -8.92, -7.5, -6.2, -5.1, -4.2, -3.5, -2.8]
      }
    ]
  }
  
  drawdownChart.setOption(option)
}

const handleResize = () => {
  drawdownChart?.resize()
}

onMounted(() => {
  initDrawdownChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  drawdownChart?.dispose()
})
</script>

<style scoped>
.risk-analysis {
  width: 100%;
  padding: 20px 0;
}

.risk-card {
  margin-top: 20px;
}

.risk-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.drawdown-card {
  margin-top: 20px;
}

.drawdown-chart-container {
  width: 100%;
  height: 400px;
}

.drawdown-chart {
  width: 100%;
  height: 100%;
}
</style>