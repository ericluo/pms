<template>
  <div class="market-news">
    <el-page-header
      @back="goBack"
      content="市场新闻"
    />
    
    <el-card class="news-list-card">
      <template #header>
        <span>最新市场新闻</span>
      </template>
      <el-timeline>
        <el-timeline-item
          v-for="news in newsList"
          :key="news.id"
          :timestamp="news.time"
        >
          <el-card>
            <h3>{{ news.title }}</h3>
            <p>{{ news.content }}</p>
            <div class="news-source">{{ news.source }}</div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const newsList = ref([
  {
    id: 1,
    title: '央行降准0.5个百分点，释放长期资金约1.2万亿元',
    content: '中国人民银行决定于2024年1月15日降低金融机构存款准备金率0.5个百分点，释放长期资金约1.2万亿元，以支持实体经济发展。',
    time: '2024-01-10 09:30',
    source: '央行网站'
  },
  {
    id: 2,
    title: '沪深300指数创年内新高，市场情绪乐观',
    content: '受利好政策影响，沪深300指数今日上涨1.5%，创年内新高，市场情绪乐观，资金持续流入。',
    time: '2024-01-09 15:30',
    source: '证券时报'
  },
  {
    id: 3,
    title: '科技股集体爆发，半导体板块领涨',
    content: '科技股今日集体爆发，半导体板块领涨，芯片ETF上涨3.2%，多家科技公司发布财报超预期。',
    time: '2024-01-08 14:00',
    source: '上海证券报'
  },
  {
    id: 4,
    title: '新能源汽车销量持续增长，行业景气度高',
    content: '2023年12月新能源汽车销量同比增长35%，连续12个月保持两位数增长，行业景气度持续高涨。',
    time: '2024-01-07 10:00',
    source: '中国汽车工业协会'
  }
])

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.market-news {
  width: 100%;
  padding: 20px 0;
}

.news-list-card {
  margin-top: 20px;
}

.news-source {
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
  text-align: right;
}

.el-timeline-item__timestamp {
  font-size: 14px;
  color: #909399;
}

.el-card {
  margin-bottom: 10px;
}
</style>