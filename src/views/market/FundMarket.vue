<template>
  <div class="fund-market">
    <el-page-header
      @back="goBack"
      content="基金市场"
    />
    
    <el-card class="fund-list-card">
      <template #header>
        <div class="card-header">
          <span>基金列表</span>
          <el-input
            v-model="searchQuery"
            placeholder="搜索基金"
            prefix-icon="el-icon-search"
            style="width: 200px"
          />
        </div>
      </template>
      <el-table :data="filteredFunds" style="width: 100%">
        <el-table-column prop="code" label="基金代码" />
        <el-table-column prop="name" label="基金名称" />
        <el-table-column prop="nav" label="净值" />
        <el-table-column prop="change" label="日涨跌幅" :formatter="formatChange" />
        <el-table-column prop="yearly_return" label="年化收益率" />
        <el-table-column prop="manager" label="基金经理" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const searchQuery = ref('')

const funds = ref([
  {
    code: '000001',
    name: '华夏成长混合',
    nav: 1.5234,
    change: 0.85,
    yearly_return: '12.5%',
    manager: '张三'
  },
  {
    code: '110022',
    name: '易方达消费行业股票',
    nav: 2.8567,
    change: 1.25,
    yearly_return: '15.8%',
    manager: '李四'
  },
  {
    code: '161005',
    name: '富国天惠成长混合A',
    nav: 3.2456,
    change: -0.35,
    yearly_return: '10.2%',
    manager: '王五'
  },
  {
    code: '001475',
    name: '易方达国防军工混合',
    nav: 1.8765,
    change: 2.15,
    yearly_return: '8.5%',
    manager: '赵六'
  }
])

const filteredFunds = computed(() => {
  if (!searchQuery.value) {
    return funds.value
  }
  return funds.value.filter(fund => 
    fund.name.includes(searchQuery.value) || fund.code.includes(searchQuery.value)
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
.fund-market {
  width: 100%;
  padding: 20px 0;
}

.fund-list-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>