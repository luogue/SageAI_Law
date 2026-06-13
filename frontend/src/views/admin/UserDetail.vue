<template>
  <div class="user-detail-page">
    <!-- 返回按钮 -->
    <div class="back-btn">
      <el-button @click="goBack">
        <i class="el-icon-arrow-left"></i> 返回用户列表
      </el-button>
    </div>

    <el-card shadow="never" class="user-info-card">
      <h3 class="card-title">用户基本信息</h3>
      <div class="info-grid">
        <div class="info-item">
          <span class="label">用户ID</span>
          <span class="value">{{ userInfo.id }}</span>
        </div>
        <div class="info-item">
          <span class="label">手机号</span>
          <span class="value">{{ userInfo.mobile }}</span>
        </div>
        <div class="info-item">
          <span class="label">剩余免费审查次数</span>
          <span class="value">{{ userInfo.bonus_credits }}</span>
        </div>
        <div class="info-item">
          <span class="label">账号状态</span>
          <el-tag :type="userInfo.status === 'normal' ? 'success' : 'danger'" size="small">
            {{ userInfo.status === 'normal' ? '正常' : '封禁' }}
          </el-tag>
        </div>
        <div class="info-item">
          <span class="label">注册时间</span>
          <span class="value">{{ formatTime(userInfo.created_at) }}</span>
        </div>
        <div class="info-item">
          <span class="label">最后活跃时间</span>
          <span class="value">{{ userInfo.last_active_at ? formatTime(userInfo.last_active_at) : '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">邀请人ID</span>
          <span class="value">{{ userInfo.invited_by || '-' }}</span>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="quick-actions">
        <el-button
          v-if="userInfo.status === 'normal'"
          type="danger"
          size="small"
          @click="handleBan"
        >
          <i class="el-icon-ban"></i> 封禁用户
        </el-button>
        <el-button
          v-else
          type="success"
          size="small"
          @click="handleUnban"
        >
          <i class="el-icon-check"></i> 解封用户
        </el-button>
        <el-button type="primary" size="small" @click="handleAddCredits">
          <i class="el-icon-plus"></i> 增加额度
        </el-button>
        <el-button type="warning" size="small" @click="handleReduceCredits">
          <i class="el-icon-minus"></i> 减少额度
        </el-button>
      </div>
    </el-card>

    <!-- 额度变动流水 -->
    <el-card shadow="never" class="credit-logs-card">
      <h3 class="card-title">额度变动流水</h3>
      <el-table
        v-loading="logsLoading"
        :data="creditLogs"
        border
        stripe
        style="width: 100%"
        empty-text="暂无额度变动记录"
      >
        <el-table-column prop="created_at" label="操作时间" width="170">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="admin_user" label="操作人" width="120" />
        <el-table-column prop="action" label="操作类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getActionType(row.action)" size="small">
              {{ getActionLabel(row.action) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="detail" label="操作详情" />
      </el-table>
    </el-card>

    <!-- 审查记录列表 -->
    <el-card shadow="never" class="records-card">
      <div class="card-header">
        <h3 class="card-title">审查记录列表</h3>
        <div class="page-info">共 {{ recordsTotal }} 条记录</div>
      </div>
      <el-table
        v-loading="recordsLoading"
        :data="records"
        border
        stripe
        style="width: 100%"
        empty-text="暂无审查记录"
      >
        <el-table-column prop="id" label="记录ID" width="100" align="center" />
        <el-table-column prop="filename" label="合同文件名" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="审查时间" width="170">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'success' ? 'success' : 'danger'" size="small">
              {{ row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="risk_count" label="风险数量" width="90" align="center" />
        <el-table-column label="操作" width="200" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewFinalReport(row)">
              <i class="el-icon-file-text"></i> 最终报告
            </el-button>
            <el-button type="success" link size="small" @click="viewRawReport(row)">
              <i class="el-icon-file"></i> 原始报告
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="recordsPage"
          v-model:page-size="recordsSize"
          :page-sizes="[10, 20, 50]"
          :total="recordsTotal"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadRecords"
          @current-change="loadRecords"
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

    <!-- 原始报告查看弹窗 -->
    <el-dialog
      v-model="rawReportVisible"
      :title="rawReportTitle"
      width="800px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <div class="raw-report-content">
        <pre>{{ rawReportContent }}</pre>
      </div>
      <template #footer>
        <el-button type="primary" @click="rawReportVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 封禁/解封弹窗 -->
    <el-dialog
      v-model="banVisible"
      :title="isBanAction ? '封禁用户' : '解封用户'"
      width="400px"
      :close-on-click-modal="false"
    >
      <p>确定要{{ isBanAction ? '封禁' : '解封' }}用户 {{ userInfo.mobile }} 吗？</p>
      <el-form-item :label="isBanAction ? '封禁理由' : '解封理由'">
        <el-input v-model="banReason" type="textarea" :placeholder="`请输入${isBanAction ? '封禁' : '解封'}理由`" />
      </el-form-item>
      <template #footer>
        <el-button @click="banVisible = false">取消</el-button>
        <el-button :type="isBanAction ? 'danger' : 'primary'" @click="confirmBanAction">
          确定{{ isBanAction ? '封禁' : '解封' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 额度调整弹窗 -->
    <el-dialog
      v-model="creditsVisible"
      :title="isAddCredits ? '增加额度' : '减少额度'"
      width="400px"
      :close-on-click-modal="false"
    >
      <p>当前剩余额度：{{ userInfo.bonus_credits }} 次</p>
      <el-form-item :label="isAddCredits ? '增加数量' : '减少数量'">
        <el-input-number v-model="creditsAmount" :min="1" :max="isAddCredits ? 100 : userInfo.bonus_credits || 1" />
      </el-form-item>
      <el-form-item label="操作理由">
        <el-input v-model="creditsReason" placeholder="请输入操作理由（可选）" />
      </el-form-item>
      <template #footer>
        <el-button @click="creditsVisible = false">取消</el-button>
        <el-button :type="isAddCredits ? 'primary' : 'warning'" @click="confirmCreditsAction">
          确定{{ isAddCredits ? '增加' : '减少' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import {
  getUserDetail,
  getUserRecords,
  getFinalReport,
  getRawReport,
  banUser,
  unbanUser,
  addUserCredits,
  reduceUserCredits
} from '../../api/admin'

const route = useRoute()
const userId = ref(Number(route.params.id))

// 用户信息
const userInfo = reactive({
  id: 0,
  mobile: '',
  bonus_credits: 0,
  status: 'normal',
  created_at: '',
  last_active_at: '',
  invited_by: null
})

// 额度变动流水
const creditLogs = ref([])
const logsLoading = ref(false)

// 审查记录
const records = ref([])
const recordsPage = ref(1)
const recordsSize = ref(20)
const recordsTotal = ref(0)
const recordsLoading = ref(false)

// 报告弹窗
const reportVisible = ref(false)
const reportTitle = ref('')
const reportHtml = ref('')

const rawReportVisible = ref(false)
const rawReportTitle = ref('')
const rawReportContent = ref('')

// 操作弹窗
const banVisible = ref(false)
const isBanAction = ref(true)
const banReason = ref('')

const creditsVisible = ref(false)
const isAddCredits = ref(true)
const creditsAmount = ref(1)
const creditsReason = ref('')

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

function getActionType(action) {
  if (action === 'add_credits') return 'success'
  if (action === 'reduce_credits') return 'warning'
  if (action === 'ban_user') return 'danger'
  if (action === 'unban_user') return 'info'
  return 'default'
}

function getActionLabel(action) {
  const labels = {
    'add_credits': '增加额度',
    'reduce_credits': '减少额度',
    'ban_user': '封禁用户',
    'unban_user': '解封用户'
  }
  return labels[action] || action
}

async function loadUserDetail() {
  logsLoading.value = true
  try {
    const res = await getUserDetail(userId.value)
    if (res.success) {
      Object.assign(userInfo, res.data.user)
      creditLogs.value = res.data.credit_logs || []
    } else {
      ElMessage.error(res.detail || '获取用户详情失败')
    }
  } catch (e) {
    console.error('加载用户详情失败:', e)
    ElMessage.error('加载失败')
  } finally {
    logsLoading.value = false
  }
}

async function loadRecords() {
  recordsLoading.value = true
  try {
    const res = await getUserRecords(userId.value, {
      page: recordsPage.value,
      size: recordsSize.value
    })
    if (res.success) {
      records.value = res.data || []
      recordsTotal.value = res.total || 0
    } else {
      ElMessage.error(res.detail || '获取审查记录失败')
    }
  } catch (e) {
    console.error('加载审查记录失败:', e)
    ElMessage.error('加载失败')
  } finally {
    recordsLoading.value = false
  }
}

async function viewFinalReport(row) {
  try {
    const res = await getFinalReport(userId.value, row.id)
    if (res.success) {
      reportTitle.value = `${res.data.filename} - 最终报告`
      reportHtml.value = marked.parse(res.data.report_markdown || '*暂无报告内容*')
      reportVisible.value = true
    } else {
      ElMessage.error(res.detail || '获取报告失败')
    }
  } catch (e) {
    console.error('获取报告失败:', e)
    ElMessage.error('获取报告失败')
  }
}

async function viewRawReport(row) {
  try {
    const res = await getRawReport(userId.value, row.id)
    if (res.success) {
      rawReportTitle.value = `${res.data.filename} - 原始报告`
      rawReportContent.value = res.data.raw_output || '暂无原始报告内容'
      rawReportVisible.value = true
    } else {
      ElMessage.error(res.detail || '获取原始报告失败')
    }
  } catch (e) {
    console.error('获取原始报告失败:', e)
    ElMessage.error('获取原始报告失败')
  }
}

function handleBan() {
  isBanAction.value = true
  banReason.value = ''
  banVisible.value = true
}

function handleUnban() {
  isBanAction.value = false
  banReason.value = ''
  banVisible.value = true
}

function handleAddCredits() {
  isAddCredits.value = true
  creditsAmount.value = 1
  creditsReason.value = ''
  creditsVisible.value = true
}

function handleReduceCredits() {
  isAddCredits.value = false
  creditsAmount.value = 1
  creditsReason.value = ''
  creditsVisible.value = true
}

async function confirmBanAction() {
  try {
    const res = isBanAction.value
      ? await banUser(userId.value, banReason.value)
      : await unbanUser(userId.value, banReason.value)
    if (res.success) {
      ElMessage.success(isBanAction.value ? '封禁成功' : '解封成功')
      banVisible.value = false
      loadUserDetail()
    } else {
      ElMessage.error(res.detail || (isBanAction.value ? '封禁失败' : '解封失败'))
    }
  } catch (e) {
    console.error('操作失败:', e)
    ElMessage.error(isBanAction.value ? '封禁失败' : '解封失败')
  }
}

async function confirmCreditsAction() {
  try {
    const res = isAddCredits.value
      ? await addUserCredits(userId.value, creditsAmount.value, creditsReason.value)
      : await reduceUserCredits(userId.value, creditsAmount.value, creditsReason.value)
    if (res.success) {
      ElMessage.success(isAddCredits.value
        ? `成功增加 ${creditsAmount.value} 次免费审查额度`
        : `成功减少 ${creditsAmount.value} 次免费审查额度`
      )
      creditsVisible.value = false
      loadUserDetail()
    } else {
      ElMessage.error(res.detail || (isAddCredits.value ? '增加额度失败' : '减少额度失败'))
    }
  } catch (e) {
    console.error('操作失败:', e)
    ElMessage.error(isAddCredits.value ? '增加额度失败' : '减少额度失败')
  }
}

function goBack() {
  window.history.back()
}

onMounted(() => {
  loadUserDetail()
  loadRecords()
})
</script>

<style scoped>
.user-detail-page {
  padding: 0;
}

.back-btn {
  margin-bottom: 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.page-info {
  font-size: 14px;
  color: #909399;
}

.user-info-card {
  margin-bottom: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item .label {
  font-size: 14px;
  color: #909399;
}

.info-item .value {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.quick-actions {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}

.credit-logs-card {
  margin-bottom: 20px;
}

.records-card {
  margin-bottom: 20px;
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

.raw-report-content {
  max-height: 60vh;
  overflow-y: auto;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
}

.raw-report-content pre {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
  color: #303133;
  margin: 0;
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

@media (max-width: 1200px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>