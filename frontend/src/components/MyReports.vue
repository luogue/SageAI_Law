<template>
  <div class="my-reports">
    <!-- 页面标题和隐私提示 -->
    <div class="page-header">
      <h2>我的报告</h2>
      <div class="privacy-hint">
        <div class="hint-content" :class="{ collapsed: hintCollapsed }">
          <span class="hint-icon">🔒</span>
          <span class="hint-text">为保护您的隐私，我们不会保存您上传的合同原文。生成的审查报告将自动保存至您的账户，供随时查阅。您也可自行删除。</span>
        </div>
        <button class="hint-toggle" @click="hintCollapsed = !hintCollapsed">
          {{ hintCollapsed ? '展开' : '收起' }}
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <span>加载中...</span>
    </div>

    <!-- 空状态 -->
    <div v-else-if="reports.length === 0" class="empty-state">
      <div class="empty-icon">📋</div>
      <p>暂无审查报告</p>
      <p class="empty-hint">上传合同并完成审查后，报告将自动保存到这里</p>
    </div>

    <!-- 报告列表 -->
    <div v-else class="reports-list">
      <div
        v-for="report in reports"
        :key="report.id"
        class="report-item"
      >
        <div class="report-info">
          <div class="report-filename">{{ report.filename }}</div>
          <div class="report-time">{{ formatDate(report.created_at) }}</div>
          <div class="report-summary">{{ getSummary(report) }}</div>
        </div>
        <div class="report-actions">
          <button class="btn btn-primary" @click="viewReport(report)">
            <span>📄</span>
            <span>查看报告</span>
          </button>
          <button class="btn btn-feedback" @click="openFeedback(report)">
            <span>💬</span>
            <span>反馈</span>
          </button>
          <button class="btn btn-danger" @click="showDeleteConfirm(report)">
            <span>🗑️</span>
            <span>删除</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 删除确认弹窗 -->
    <div v-if="deletingReport" class="modal-overlay" @click.self="cancelDelete">
      <div class="modal-content confirm-modal">
        <div class="confirm-icon">⚠️</div>
        <h3>确认删除</h3>
        <p>确定要删除报告「{{ deletingReport.filename }}」吗？</p>
        <p class="warning-text">删除后无法恢复！</p>
        <div class="confirm-actions">
          <button class="btn btn-secondary" @click="cancelDelete">取消</button>
          <button class="btn btn-danger" @click="confirmDelete">确认删除</button>
        </div>
      </div>
    </div>

    <!-- 反馈弹窗 -->
    <FeedbackModal
      :show="showFeedbackModal"
      :report-id="currentReportForFeedback?.id || ''"
      :expected-file-hash="currentReportForFeedback?.metadata?.file_hash || ''"
      @close="closeFeedbackModal"
      @success="handleFeedbackSuccess"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getRecords, deleteRecord } from '../utils/api';
import FeedbackModal from '../components/FeedbackModal.vue';

const router = useRouter();

const reports = ref([]);
const loading = ref(false);
const hintCollapsed = ref(false);
const deletingReport = ref(null);

// 反馈弹窗相关
const showFeedbackModal = ref(false);
const currentReportForFeedback = ref(null);

onMounted(() => {
  loadReports();
});

async function loadReports() {
  loading.value = true;
  try {
    reports.value = await getRecords();
  } catch (error) {
    console.error('加载报告失败:', error);
    reports.value = [];
  } finally {
    loading.value = false;
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  // 确保时间字符串是有效的
  if (typeof dateStr !== 'string') {
    dateStr = String(dateStr);
  }
  // 如果时间字符串不包含时区信息，可能是UTC时间，需要转换
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) {
    return '无效时间';
  }
  // 使用Asia/Shanghai时区确保正确转换
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'Asia/Shanghai'
  });
}

function getSummary(report) {
  return '点击查看完整报告';
}

function viewReport(report) {
  router.push(`/report/${report.id}`);
}

function openFeedback(report) {
  currentReportForFeedback.value = report;
  showFeedbackModal.value = true;
}

function closeFeedbackModal() {
  showFeedbackModal.value = false;
  currentReportForFeedback.value = null;
}

function handleFeedbackSuccess() {
  showFeedbackModal.value = false;
  currentReportForFeedback.value = null;
}

function showDeleteConfirm(report) {
  deletingReport.value = report;
}

function cancelDelete() {
  deletingReport.value = null;
}

async function confirmDelete() {
  if (!deletingReport.value) return;
  try {
    await deleteRecord(deletingReport.value.id);
    reports.value = reports.value.filter(r => r.id !== deletingReport.value.id);
  } catch (error) {
    console.error('删除报告失败:', error);
  } finally {
    deletingReport.value = null;
  }
}
</script>

<style scoped>
.my-reports {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h2 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #1a1a1a;
}

.privacy-hint {
  background: #f5f9ff;
  border: 1px solid #e1ecff;
  border-radius: 8px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.hint-content {
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.hint-content.collapsed {
  max-height: 40px;
  overflow: hidden;
}

.hint-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.hint-text {
  font-size: 13px;
  color: #666;
  line-height: 1.5;
}

.hint-toggle {
  background: none;
  border: none;
  color: #4a90d9;
  font-size: 13px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.hint-toggle:hover {
  background: rgba(74, 144, 217, 0.1);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #666;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4a90d9;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 16px;
  color: #666;
  margin: 8px 0;
}

.empty-hint {
  font-size: 14px !important;
  color: #999 !important;
}

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.report-item {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  transition: box-shadow 0.2s;
}

.report-item:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.report-info {
  flex: 1;
}

.report-filename {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.report-time {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}

.report-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.report-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #4a90d9;
  color: #fff;
}

.btn-primary:hover {
  background: #3a7bc8;
}

.btn-danger {
  background: #ff6b6b;
  color: #fff;
}

.btn-danger:hover {
  background: #ee5a5a;
}

.btn-feedback {
  background: #67c23a;
  color: #fff;
}

.btn-feedback:hover {
  background: #5cb83a;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 900px;
  max-height: 80vh;
  overflow: hidden;
}

/* 确认弹窗 */
.confirm-modal {
  max-width: 400px;
  text-align: center;
  padding: 30px;
}

.confirm-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.confirm-modal h3 {
  margin: 0 0 12px;
}

.confirm-modal p {
  color: #666;
  margin: 8px 0;
}

.warning-text {
  color: #ff6b6b !important;
  font-weight: 500;
}

.confirm-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}
</style>
