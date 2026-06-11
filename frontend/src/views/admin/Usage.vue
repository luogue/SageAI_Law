<template>
  <div class="usage-page">
    <!-- 筛选栏 -->
    <div class="filter-bar">
      <div class="filter-item">
        <span class="filter-label">用户筛选：</span>
        <el-select
          v-model="filterUserId"
          placeholder="全部用户"
          clearable
          style="width: 220px"
          @change="handleFilter"
        >
          <el-option
            v-for="u in userList"
            :key="u.user_id"
            :label="`ID:${u.user_id} | ${u.user_phone}`"
            :value="u.user_id"
          />
        </el-select>
      </div>
      <div class="filter-item">
        <el-button type="primary" @click="handleRefresh">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
      </div>
    </div>

    <!-- 表格 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="records"
        border
        stripe
        style="width: 100%"
        empty-text="暂无使用记录"
      >
        <el-table-column prop="user_phone" label="用户手机号" width="130" />
        <el-table-column prop="filename" label="合同文件名" min-width="180" show-overflow-tooltip />
        <el-table-column prop="created_at" label="审查时间" width="170">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="duration_ms" label="耗时(秒)" width="90" align="center">
          <template #default="{ row }">
            {{ row.duration_ms ? (row.duration_ms / 1000).toFixed(1) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'success' ? 'success' : 'danger'" size="small">
              {{ row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="risk_count" label="风险数" width="80" align="center" />
        <el-table-column label="操作" width="160" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewReport(row)">
              <i class="el-icon-view"></i> 查看报告
            </el-button>
            <el-button type="success" link size="small" @click="copyReportLink(row.id)">
              <i class="el-icon-link"></i> 复制链接
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleFilter"
          @current-change="handleFilter"
        />
      </div>
    </el-card>

    <!-- 报告查看弹窗 -->
    <el-dialog
      v-model="reportVisible"
      :title="reportTitle"
      width="800px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <div class="report-content" v-html="reportHtml"></div>
      <template #footer>
        <el-button type="primary" @click="reportVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { marked } from 'marked'
import { getUsageRecords, getUsageUsers, getReportDetail } from '../../api/admin'

// 筛选
const filterUserId = ref(null)
const userList = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const records = ref([])
const loading = ref(false)

// 报告弹窗
const reportVisible = ref(false)
const reportTitle = ref('')
const reportHtml = ref('')

function formatTime(isoStr) {
  if (!isoStr) return '-'
  try {
    const d = new Date(isoStr)
    const pad = n => String(n).padStart(2, '0')
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
  } catch {
    return isoStr
  }
}

async function loadUsers() {
  try {
    const res = await getUsageUsers()
    if (res.success) {
      userList.value = res.data || []
    }
  } catch (e) {
    console.error('加载用户列表失败:', e)
  }
}

async function loadRecords() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (filterUserId.value) {
      params.user_id = filterUserId.value
    }
    const res = await getUsageRecords(params)
    if (res.success) {
      records.value = res.records || []
      total.value = res.total || 0
    } else {
      ElMessage.error(res.detail || '获取记录失败')
    }
  } catch (e) {
    console.error('加载使用记录失败:', e)
    ElMessage.error('加载失败，请检查网络或管理员Token')
  } finally {
    loading.value = false
  }
}

function handleFilter() {
  currentPage.value = 1
  loadRecords()
}

function handleRefresh() {
  loadUsers()
  loadRecords()
}

async function viewReport(row) {
  loading.value = true
  try {
    const res = await getReportDetail(row.id)
    if (res.success && res.data) {
      reportTitle.value = `${res.data.filename} — ${res.data.user_phone}`
      // 使用 marked 渲染 Markdown
      reportHtml.value = marked.parse(res.data.report_markdown || '*暂无报告内容*')
      reportVisible.value = true
    } else {
      ElMessage.error(res.detail || '获取报告失败')
    }
  } catch (e) {
    console.error('获取报告失败:', e)
    ElMessage.error('获取报告失败')
  } finally {
    loading.value = false
  }
}

function copyReportLink(recordId) {
  const host = window.location.origin
  const link = `${host}/admin?report=${recordId}`
  navigator.clipboard.writeText(link).then(() => {
    ElMessage.success('报告链接已复制到剪贴板')
  }).catch(() => {
    // fallback
    const textarea = document.createElement('textarea')
    textarea.value = link
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    ElMessage.success('报告链接已复制到剪贴板')
  })
}

onMounted(() => {
  loadUsers()
  loadRecords()
})
</script>

<style scoped>
.usage-page {
  padding: 0;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.report-content {
  max-height: 60vh;
  overflow-y: auto;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.8;
  color: #303133;
}

/* Markdown 渲染样式 */
.report-content :deep(h1) { font-size: 1.5em; margin: 0.8em 0 0.4em; border-bottom: 1px solid #eee; padding-bottom: 0.3em; }
.report-content :deep(h2) { font-size: 1.3em; margin: 0.7em 0 0.3em; }
.report-content :deep(h3) { font-size: 1.15em; margin: 0.6em 0 0.2em; }
.report-content :deep(h4) { font-size: 1.05em; margin: 0.5em 0 0.15em; }
.report-content :deep(p) { margin: 0.5em 0; }
.report-content :deep(ul), .report-content :deep(ol) { padding-left: 1.5em; margin: 0.5em 0; }
.report-content :deep(li) { margin: 0.25em 0; }
.report-content :deep(table) { border-collapse: collapse; width: 100%; margin: 1em 0; }
.report-content :deep(th), .report-content :deep(td) { border: 1px solid #ddd; padding: 6px 12px; text-align: left; }
.report-content :deep(th) { background: #f5f7fa; font-weight: 600; }
.report-content :deep(code) { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }
.report-content :deep(pre) { background: #f0f0f0; padding: 12px; border-radius: 6px; overflow-x: auto; }
.report-content :deep(blockquote) { border-left: 3px solid #667eea; padding-left: 12px; margin: 0.5em 0; color: #666; }
.report-content :deep(strong) { color: #d32f2f; }
.report-content :deep(hr) { border: none; border-top: 1px solid #eee; margin: 1em 0; }
</style>
