<template>
  <div class="review-v2-page">
    <section class="review-shell">
      <aside class="control-panel">
        <div class="panel-header">
          <div>
            <p class="eyebrow">审查第二版</p>
            <h1>合同审查引擎</h1>
          </div>
          <el-tag effect="plain" type="success">独立模块</el-tag>
        </div>

        <el-form label-position="top" class="review-form">
          <el-form-item label="合同类型">
            <el-select v-model="contractType" class="full-width">
              <el-option
                v-for="option in contractTypeOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
                :disabled="option.disabled"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="报告范围">
            <el-switch
              v-model="includeLowRisk"
              active-text="包含已覆盖/低风险项"
              inactive-text="仅看中高风险"
            />
          </el-form-item>

          <el-form-item label="语义判定">
            <el-switch
              v-model="useLlmReview"
              :disabled="llmStatusLoaded && !llmStatus?.available"
              active-text="启用大模型复核"
              inactive-text="仅用规则兜底"
            />
            <div
              v-if="llmStatusLoaded"
              class="llm-status"
              :class="{ available: llmStatus?.available, unavailable: !llmStatus?.available }"
            >
              {{ llmStatus.message }}
              <span v-if="llmStatus?.configured_models?.length">
                模型：{{ llmStatus.configured_models.join(' / ') }}
              </span>
            </div>
          </el-form-item>
        </el-form>

        <div
          class="upload-zone"
          :class="{ dragging: isDragging, selected: selectedFile }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="fileInput?.click()"
        >
          <input
            ref="fileInput"
            type="file"
            accept=".doc,.docx,.pdf"
            hidden
            @change="handleFileChange"
          />
          <el-icon class="upload-icon"><UploadFilled /></el-icon>
          <div class="upload-title">{{ selectedFile ? selectedFile.name : '上传合同文件' }}</div>
          <div class="upload-hint">支持 .doc / .docx / .pdf，系统按审查清单逐项检查</div>
        </div>

        <div class="action-row">
          <el-button :icon="RefreshLeft" @click="resetAll">清空</el-button>
          <el-button type="primary" :icon="Search" :loading="loading" @click="runReview">
            {{ loading ? '审查中' : '开始审查' }}
          </el-button>
        </div>

        <el-steps :active="stepActive" finish-status="success" direction="vertical" class="progress-steps">
          <el-step title="上传合同" description="读取 Word 或 PDF 文本" />
          <el-step title="加载清单" description="按合同类型加载对应审查清单" />
          <el-step title="生成报告" description="输出风险提示和修改建议" />
        </el-steps>
      </aside>

      <main class="report-panel">
        <template v-if="report">
          <div class="report-toolbar">
            <div>
              <p class="eyebrow">结构化报告</p>
              <h2>{{ report.contract_type_name }}</h2>
              <p class="file-meta">{{ report.filename }} · 已抽取 {{ report.extracted_text_length }} 字</p>
            </div>
            <div class="toolbar-actions">
              <el-radio-group v-model="riskFilter" size="small">
                <el-radio-button
                  v-for="option in riskFilterOptions"
                  :key="option"
                  :label="option"
                />
              </el-radio-group>
              <el-select v-model="coverageFilter" class="coverage-filter" size="small">
                <el-option
                  v-for="option in coverageFilterOptions"
                  :key="option"
                  :label="option === '全部' ? '全部覆盖状态' : option"
                  :value="option"
                />
              </el-select>
              <el-select v-model="issueTypeFilter" class="issue-filter" size="small">
                <el-option
                  v-for="option in issueTypeFilterOptions"
                  :key="option"
                  :label="option === '全部' ? '全部问题类型' : option"
                  :value="option"
                />
              </el-select>
              <el-select v-model="judgeSourceFilter" class="source-filter" size="small">
                <el-option
                  v-for="option in judgeSourceFilterOptions"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>
              <el-button
                type="primary"
                plain
                :icon="Download"
                :loading="exportingType === 'pdf'"
                :disabled="!!exportingType"
                @click="downloadReport('pdf')"
              >
                导出 PDF
              </el-button>
              <el-button
                type="success"
                plain
                :icon="Download"
                :loading="exportingType === 'docx'"
                :disabled="!!exportingType"
                @click="downloadReport('docx')"
              >
                导出 Word
              </el-button>
            </div>
          </div>

          <div class="format-notice">
            {{ report.report_notice || '本报告基于完整合同模板逐项审查，部分缺失项可能因合同格式简略所致，建议结合合同实际用途判断优先级。' }}
          </div>

          <div class="summary-grid">
            <div class="summary-card high">
              <span>高风险</span>
              <strong>{{ report.summary?.高 || 0 }}</strong>
            </div>
            <div class="summary-card medium">
              <span>中风险</span>
              <strong>{{ report.summary?.中 || 0 }}</strong>
            </div>
            <div class="summary-card low">
              <span>低风险</span>
              <strong>{{ report.summary?.低 || 0 }}</strong>
            </div>
            <div class="summary-card na">
              <span>不适用</span>
              <strong>{{ report.coverage_summary?.不适用 || 0 }}</strong>
            </div>
            <div class="summary-card total">
              <span>审查项</span>
              <strong>{{ report.all_items_count }}</strong>
            </div>
            <div class="summary-card clauses">
              <span>正式条款</span>
              <strong>{{ report.formal_clause_count || 0 }}</strong>
            </div>
            <div class="summary-card source">
              <span>大模型/规则</span>
              <strong>{{ report.judge_source_summary?.llm || 0 }}/{{ report.judge_source_summary?.rule_fallback || 0 }}</strong>
            </div>
            <div class="summary-card issue">
              <span>空白/缺失</span>
              <strong>{{ report.issue_type_summary?.模板空白 || 0 }}/{{ report.issue_type_summary?.完全缺失 || 0 }}</strong>
            </div>
          </div>

          <div v-if="report.global_fallback_reason" class="global-fallback">
            {{ report.global_fallback_reason }}
          </div>

          <div class="review-list">
            <article v-for="item in filteredItems" :key="item.item_id" class="review-item">
              <header class="item-header">
                <div>
                  <div class="item-title">{{ item.item_id }} · {{ item.title }}</div>
                  <div class="item-status">
                    {{ item.status }} · {{ item.coverage_status }} · {{ item.issue_type || '未分类' }} · {{ judgeSourceLabel(item.judge_source) }}
                  </div>
                </div>
                <el-tag :type="riskTagType(item.risk_level)" effect="dark">{{ riskLabel(item.risk_level) }}</el-tag>
              </header>

              <dl class="item-body">
                <dt>判定来源</dt>
                <dd>
                  {{ judgeSourceLabel(item.judge_source) }}
                  <span v-if="item.llm_confidence"> · 置信度 {{ confidenceLabel(item.llm_confidence) }}</span>
                  <span v-if="visibleFallbackReason(item)" class="fallback-reason">
                    · {{ item.fallback_reason }}
                  </span>
                </dd>
                <dt>系统判断</dt>
                <dd>{{ item.reasoning_summary }}</dd>
                <dt>问题类型</dt>
                <dd>{{ item.issue_type || '未分类' }}</dd>
                <dt>原文位置</dt>
                <dd>{{ item.evidence_location || '未召回正式条款' }}</dd>
                <dt>命中原文</dt>
                <dd>
                  <div v-if="item.evidence_clauses?.length" class="evidence-list">
                    <details
                      v-for="evidence in item.evidence_clauses"
                      :key="evidence.clause_id"
                      class="evidence-item"
                    >
                      <summary>{{ evidence.location }} · {{ evidence.section_type }}</summary>
                      <p>{{ evidence.text }}</p>
                    </details>
                  </div>
                  <span v-else class="no-evidence">无正式条款证据</span>
                </dd>
                <dt>【风险点描述】</dt>
                <dd>{{ item.risk_point_description }}</dd>
                <dt>【缺失的法律后果】</dt>
                <dd>{{ item.legal_consequence_if_missing }}</dd>
                <dt>【建议条款示例】</dt>
                <dd>{{ item.suggested_clause_example }}</dd>
                <dt>【法律依据索引】</dt>
                <dd>{{ item.legal_basis_index }}</dd>
              </dl>

              <div class="review-controls">
                <el-radio-group v-model="item.review_status" size="small">
                  <el-radio-button label="待处理" />
                  <el-radio-button label="已处理" />
                  <el-radio-button label="忽略" />
                </el-radio-group>
                <el-input
                  v-model="item.reviewer_note"
                  class="note-input"
                  size="small"
                  clearable
                  placeholder="律师复核备注"
                />
              </div>
            </article>
          </div>
        </template>

        <el-empty v-else description="上传合同后生成审查报告">
          <template #image>
            <el-icon class="empty-icon"><DocumentChecked /></el-icon>
          </template>
        </el-empty>
      </main>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { DocumentChecked, Download, RefreshLeft, Search, UploadFilled } from '@element-plus/icons-vue'
import { exportReviewV2Docx, exportReviewV2Pdf, getReviewV2LlmStatus, reviewContractV2File } from '../utils/api'

defineOptions({
  name: 'ContractReviewV2'
})

const contractTypeOptions = [
  { label: '房屋租赁合同', value: 'house_lease' },
  { label: '买卖合同', value: 'sale' },
  { label: '赠与合同', value: 'gift' },
  { label: '保管合同', value: 'deposit' },
  { label: '承揽合同', value: 'work_contract' },
  { label: '运输合同', value: 'transportation' },
  { label: '委托合同', value: 'agency' },
  { label: '借款合同', value: 'loan' },
  { label: '服务合同', value: 'service' },
  { label: '保证合同', value: 'guarantee' },
  { label: '融资租赁合同', value: 'finance_lease' },
  { label: '仓储合同', value: 'warehouse' },
  { label: '建设工程合同', value: 'construction' },
  { label: '技术合同', value: 'technology' },
  { label: '行纪合同', value: 'commission_agency' },
  { label: '供用电、水、气、热力合同', value: 'utility_supply' },
  { label: '中介合同', value: 'brokerage' },
  { label: '物业服务合同（待导入清单）', value: 'property_management', disabled: true }
]

const riskFilterOptions = ['全部', '高', '中', '低']
const coverageFilterOptions = ['全部', '通过', '部分覆盖', '缺失', '风险条款', '不适用']
const issueTypeFilterOptions = ['全部', '通过', '模板空白', '条款缺陷', '完全缺失', '风险条款', '不适用']
const judgeSourceFilterOptions = [
  { label: '全部判定来源', value: '全部' },
  { label: '大模型判定', value: 'llm' },
  { label: '规则兜底', value: 'rule_fallback' },
  { label: '适用条件过滤', value: 'applicability_filter' }
]

const fileInput = ref(null)
const selectedFile = ref(null)
const contractType = ref('house_lease')
const includeLowRisk = ref(true)
const useLlmReview = ref(true)
const llmStatus = ref(null)
const llmStatusLoaded = ref(false)
const isDragging = ref(false)
const loading = ref(false)
const exportingType = ref('')
const report = ref(null)
const riskFilter = ref('全部')
const coverageFilter = ref('全部')
const issueTypeFilter = ref('全部')
const judgeSourceFilter = ref('全部')
const stepActive = ref(0)

const filteredItems = computed(() => {
  if (!report.value?.items) return []
  return report.value.items.filter(item => {
    const riskMatched = riskFilter.value === '全部' || item.risk_level === riskFilter.value
    const coverageMatched = coverageFilter.value === '全部' || item.coverage_status === coverageFilter.value
    const issueMatched = issueTypeFilter.value === '全部' || item.issue_type === issueTypeFilter.value
    const sourceMatched = judgeSourceFilter.value === '全部' || item.judge_source === judgeSourceFilter.value
    return riskMatched && coverageMatched && issueMatched && sourceMatched
  })
})

function judgeSourceLabel(source) {
  if (source === 'llm') return '大模型判定'
  if (source === 'applicability_filter') return '适用条件过滤'
  return '规则兜底'
}

function confidenceLabel(confidence) {
  const labels = { high: '高', medium: '中', low: '低' }
  return labels[confidence] || confidence
}

function visibleFallbackReason(item) {
  if (!item?.fallback_reason) return ''
  if (report.value?.global_fallback_reason === item.fallback_reason) return ''
  return item.fallback_reason
}

async function loadLlmStatus() {
  try {
    const status = await getReviewV2LlmStatus()
    llmStatus.value = status
    if (!status.available) {
      useLlmReview.value = false
    }
  } catch (error) {
    llmStatus.value = {
      available: false,
      configured_models: [],
      message: '无法读取大模型状态，本次默认仅用规则兜底。'
    }
    useLlmReview.value = false
  } finally {
    llmStatusLoaded.value = true
  }
}

onMounted(() => {
  loadLlmStatus()
})

function handleFileChange(event) {
  const file = event.target.files?.[0]
  setFile(file)
}

function handleDrop(event) {
  isDragging.value = false
  const file = event.dataTransfer.files?.[0]
  setFile(file)
}

function setFile(file) {
  if (!file) return
  const lowerName = file.name.toLowerCase()
  if (!lowerName.endsWith('.doc') && !lowerName.endsWith('.docx') && !lowerName.endsWith('.pdf')) {
    ElMessage.error('请上传 .doc、.docx 或 .pdf 文件')
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.error('文件不能超过 10MB')
    return
  }
  selectedFile.value = file
  stepActive.value = 1
}

async function runReview() {
  if (!selectedFile.value) {
    ElMessage.warning('请先上传合同文件')
    return
  }

  loading.value = true
  stepActive.value = 2
  try {
    const data = await reviewContractV2File(
      selectedFile.value,
      contractType.value,
      includeLowRisk.value,
      useLlmReview.value
    )
    report.value = {
      ...data,
      filename: data.filename || selectedFile.value.name,
      items: (data.items || []).map(item => ({
        ...item,
        review_status: item.review_status || '待处理',
        reviewer_note: item.reviewer_note || ''
      }))
    }
    stepActive.value = 3
    riskFilter.value = '全部'
    coverageFilter.value = '全部'
    issueTypeFilter.value = '全部'
    judgeSourceFilter.value = '全部'
    ElMessage.success('审查报告已生成')
  } catch (error) {
    stepActive.value = 1
    ElMessage.error(error.message || '审查失败')
  } finally {
    loading.value = false
  }
}

function buildExportPayload() {
  return {
    filename: report.value.filename || '合同审查报告',
    contract_type_name: report.value.contract_type_name,
    summary: report.value.summary,
    coverage_summary: report.value.coverage_summary,
    issue_type_summary: report.value.issue_type_summary,
    judge_source_summary: report.value.judge_source_summary,
    llm_status: report.value.llm_status,
    global_fallback_reason: report.value.global_fallback_reason,
    report_notice: report.value.report_notice,
    items: report.value.items
  }
}

function triggerBrowserDownload(blob, filename) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.style.display = 'none'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  window.setTimeout(() => URL.revokeObjectURL(url), 1000)
}

async function downloadReport(format) {
  if (!report.value) return
  exportingType.value = format
  try {
    const payload = buildExportPayload()
    const blob = format === 'docx'
      ? await exportReviewV2Docx(payload)
      : await exportReviewV2Pdf(payload)
    const baseName = (report.value.filename || '合同审查报告').replace(/\.[^/.]+$/, '')
    const extension = format === 'docx' ? 'docx' : 'pdf'
    triggerBrowserDownload(blob, `${baseName}_审查第二版报告.${extension}`)
    ElMessage.success(`${format === 'docx' ? 'Word' : 'PDF'}报告已开始下载`)
  } catch (error) {
    ElMessage.error(error.message || '报告导出失败')
  } finally {
    exportingType.value = ''
  }
}

function resetAll() {
  selectedFile.value = null
  report.value = null
  riskFilter.value = '全部'
  coverageFilter.value = '全部'
  issueTypeFilter.value = '全部'
  judgeSourceFilter.value = '全部'
  stepActive.value = 0
  if (fileInput.value) fileInput.value.value = ''
}

function riskTagType(level) {
  if (level === '不适用') return 'info'
  if (level === '高') return 'danger'
  if (level === '中') return 'warning'
  return 'success'
}

function riskLabel(level) {
  return level === '不适用' ? '不适用' : `${level}风险`
}
</script>

<style scoped>
.review-v2-page {
  min-height: calc(100vh - 56px);
  background: #f5f7fb;
  padding: 24px;
  box-sizing: border-box;
}

.review-shell {
  display: grid;
  grid-template-columns: 360px minmax(0, 1fr);
  gap: 20px;
  max-width: 1360px;
  width: 100%;
  margin: 0 auto;
}

.control-panel,
.report-panel {
  background: #fff;
  border: 1px solid #e6eaf2;
  border-radius: 8px;
  box-shadow: 0 12px 30px rgba(21, 34, 50, 0.06);
}

.control-panel {
  padding: 22px;
  align-self: start;
}

.report-panel {
  min-height: 720px;
  padding: 24px;
}

.panel-header,
.report-toolbar,
.item-header,
.action-row,
.review-controls {
  display: flex;
  align-items: center;
}

.panel-header,
.report-toolbar,
.item-header {
  justify-content: space-between;
  gap: 16px;
}

.panel-header h1,
.report-toolbar h2 {
  margin: 0;
  color: #182230;
}

.panel-header h1 {
  font-size: 24px;
}

.report-toolbar h2 {
  font-size: 22px;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 12px;
  color: #64748b;
}

.review-form {
  margin-top: 22px;
}

.full-width {
  width: 100%;
}

.upload-zone {
  margin-top: 10px;
  border: 1px dashed #aab7c9;
  border-radius: 8px;
  padding: 34px 18px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #f8fafc;
}

.upload-zone:hover,
.upload-zone.dragging {
  border-color: #4080ff;
  background: #eef6ff;
}

.upload-zone.selected {
  border-style: solid;
  border-color: #67c23a;
  background: #f3fbf0;
}

.upload-icon {
  font-size: 36px;
  color: #4080ff;
}

.upload-title {
  margin-top: 12px;
  font-weight: 700;
  color: #1f2937;
  word-break: break-all;
}

.upload-hint,
.file-meta,
.item-status {
  color: #64748b;
  font-size: 13px;
}

.action-row {
  justify-content: flex-end;
  margin-top: 18px;
  gap: 10px;
}

.llm-status {
  margin-top: 8px;
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.6;
}

.llm-status span {
  display: block;
  margin-top: 2px;
}

.llm-status.available {
  color: #166534;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.llm-status.unavailable {
  color: #92400e;
  background: #fffbeb;
  border: 1px solid #fde68a;
}

.progress-steps {
  margin-top: 28px;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.format-notice {
  margin: 18px 0 0;
  padding: 10px 12px;
  border: 1px solid #d8e2f1;
  border-radius: 8px;
  background: #f8fbff;
  color: #475569;
  font-size: 13px;
  line-height: 1.6;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 12px;
  margin: 22px 0;
}

.summary-card {
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e8edf5;
  background: #f8fafc;
}

.summary-card span {
  display: block;
  font-size: 13px;
  color: #64748b;
}

.summary-card strong {
  display: block;
  margin-top: 8px;
  font-size: 28px;
  color: #182230;
}

.summary-card.high {
  background: #fff5f5;
  border-color: #ffd6d6;
}

.summary-card.medium {
  background: #fff9ed;
  border-color: #ffe1ad;
}

.summary-card.low {
  background: #f1fbf4;
  border-color: #cdeed6;
}

.summary-card.na {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.summary-card.source {
  background: #f7f5ff;
  border-color: #ddd6fe;
}

.summary-card.issue {
  background: #f0f9ff;
  border-color: #bae6fd;
}

.global-fallback {
  margin: -8px 0 18px;
  padding: 10px 12px;
  border-radius: 8px;
  color: #92400e;
  background: #fffbeb;
  border: 1px solid #fde68a;
  font-size: 13px;
  line-height: 1.6;
}

.review-list {
  display: grid;
  gap: 14px;
}

.coverage-filter,
.issue-filter,
.source-filter {
  width: 150px;
}

.source-filter {
  width: 132px;
}

.review-item {
  border: 1px solid #e6eaf2;
  border-radius: 8px;
  padding: 18px;
  background: #fff;
}

.item-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

.item-body {
  margin: 16px 0;
}

.item-body dt {
  font-size: 13px;
  font-weight: 700;
  color: #334155;
  margin-top: 12px;
}

.item-body dd {
  margin: 6px 0 0;
  color: #475569;
  line-height: 1.7;
}

.fallback-reason {
  color: #b45309;
}

.evidence-list {
  display: grid;
  gap: 8px;
}

.evidence-item {
  border: 1px solid #e8edf5;
  border-radius: 6px;
  background: #f8fafc;
  padding: 8px 10px;
}

.evidence-item summary {
  cursor: pointer;
  color: #1f6feb;
  font-weight: 600;
}

.evidence-item p {
  margin: 8px 0 0;
  color: #334155;
  white-space: pre-wrap;
}

.no-evidence {
  color: #94a3b8;
}

.review-controls {
  gap: 12px;
  border-top: 1px solid #edf1f7;
  padding-top: 14px;
}

.note-input {
  flex: 1;
}

.empty-icon {
  font-size: 80px;
  color: #b7c2d2;
}

@media (max-width: 980px) {
  .review-shell {
    grid-template-columns: 1fr;
  }

  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .report-toolbar,
  .toolbar-actions,
  .review-controls {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
