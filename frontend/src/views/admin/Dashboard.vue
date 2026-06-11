<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-icon users-icon">
          <i class="el-icon-user"></i>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ stats.total_users || 0 }}</p>
          <p class="stat-label">总用户数</p>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-icon today-icon">
          <i class="el-icon-user-plus"></i>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ stats.today_users || 0 }}</p>
          <p class="stat-label">今日新增用户</p>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-icon feedback-icon">
          <i class="el-icon-message"></i>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ stats.total_feedbacks || 0 }}</p>
          <p class="stat-label">总反馈数</p>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-icon pending-icon">
          <i class="el-icon-clock"></i>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ stats.pending_feedbacks || 0 }}</p>
          <p class="stat-label">待审核反馈</p>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-icon bonus-icon">
          <i class="el-icon-gift"></i>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ stats.total_bonus_awarded || 0 }}</p>
          <p class="stat-label">已发放奖励额度</p>
        </div>
      </el-card>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-row">
      <el-card class="chart-card">
        <div class="card-header">
          <h3>近7天反馈趋势</h3>
          <el-button size="small" @click="refreshTrend">刷新</el-button>
        </div>
        <div ref="trendChart" class="chart"></div>
      </el-card>
      
      <el-card class="chart-card">
        <div class="card-header">
          <h3>反馈分类占比</h3>
          <el-button size="small" @click="refreshCategories">刷新</el-button>
        </div>
        <div ref="categoryChart" class="chart"></div>
      </el-card>
    </div>
    
    <!-- 高频触发词 -->
    <el-card class="triggers-card">
      <div class="card-header">
        <h3>高频触发词（近7天）</h3>
        <el-button size="small" @click="refreshTriggers">刷新</el-button>
      </div>
      <el-table :data="triggers" border>
        <el-table-column prop="word" label="触发词" />
        <el-table-column prop="count" label="触发次数" />
        <el-table-column prop="percentage" label="占比(%)" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>import { ref, reactive, onMounted } from 'vue';
import * as echarts from 'echarts';
import { getStatsOverview, getStatsTrend, getCategoryStats, getFrequentTriggers } from '../../api/admin';
const stats = reactive({
 total_users: 0,
 today_users: 0,
 total_feedbacks: 0,
 pending_feedbacks: 0,
 total_bonus_awarded: 0
});
const triggers = ref([]);
const trendChart = ref(null);
const categoryChart = ref(null);
let trendChartInstance = null;
let categoryChartInstance = null;
async function loadStats() {
 try {
 const result = await getStatsOverview();
 Object.assign(stats, result.data);
 }
 catch (e) {
 console.error('加载统计数据失败:', e);
 }
}
async function loadTrend() {
 try {
 const result = await getStatsTrend(7);
 const dates = result.data.map(item => item.date);
 const counts = result.data.map(item => item.count);
 if (trendChartInstance) {
 trendChartInstance.setOption({
 xAxis: { type: 'category', data: dates },
 yAxis: { type: 'value' },
 series: [{
 data: counts,
 type: 'line',
 smooth: true,
 lineStyle: { color: '#667eea' },
 areaStyle: {
 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
 { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
 { offset: 1, color: 'rgba(102, 126, 234, 0.05)' }
 ])
 }
 }]
 });
 }
 }
 catch (e) {
 console.error('加载趋势数据失败:', e);
 }
}
async function loadCategories() {
 try {
 const result = await getCategoryStats();
 const data = result.data.map(item => ({
 name: item.category,
 value: item.count
 }));
 if (categoryChartInstance) {
 categoryChartInstance.setOption({
 series: [{
 type: 'pie',
 radius: ['40%', '70%'],
 avoidLabelOverlap: false,
 itemStyle: {
 borderRadius: 10,
 borderColor: '#fff',
 borderWidth: 2
 },
 label: { show: true, formatter: '{b}: {c} ({d}%)' },
 data
 }]
 });
 }
 }
 catch (e) {
 console.error('加载分类数据失败:', e);
 }
}
async function loadTriggers() {
 try {
 const result = await getFrequentTriggers(7, 10);
 triggers.value = result.data.slice(0, 10).map(item => ({
 word: item.word,
 count: item.count,
 percentage: (item.percentage || 0).toFixed(1)
 }));
 }
 catch (e) {
 console.error('加载触发词失败:', e);
 }
}
function refreshTrend() {
 loadTrend();
}
function refreshCategories() {
 loadCategories();
}
function refreshTriggers() {
 loadTriggers();
}
onMounted(() => {
 loadStats();
 // 初始化图表
 trendChartInstance = echarts.init(trendChart.value);
 categoryChartInstance = echarts.init(categoryChart.value);
 loadTrend();
 loadCategories();
 loadTriggers();
 // 响应式调整
 window.addEventListener('resize', () => {
 trendChartInstance?.resize();
 categoryChartInstance?.resize();
 });
});
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 16px;
  color: white;
}

.users-icon { background: linear-gradient(135deg, #667eea, #764ba2); }
.today-icon { background: linear-gradient(135deg, #11998e, #38ef7d); }
.feedback-icon { background: linear-gradient(135deg, #eb3349, #f45c43); }
.pending-icon { background: linear-gradient(135deg, #f093fb, #f5576c); }
.bonus-icon { background: linear-gradient(135deg, #4facfe, #00f2fe); }

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin: 0 0 4px 0;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.chart-card {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header h3 {
  font-size: 16px;
  margin: 0;
  color: #303133;
}

.chart {
  height: 300px;
}

.triggers-card {
  padding: 20px;
}

@media (max-width: 1200px) {
  .stats-cards {
    grid-template-columns: repeat(3, 1fr);
  }
  .charts-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
