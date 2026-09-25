<template>
  <div class="result-container">
    <div class="result-card">
      <div class="header">
        <h1>合同审查结果</h1>
        <button class="back-btn" @click="goBack">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          返回
        </button>
      </div>

      <div class="result-content">
        <div v-html="renderedMarkdown"></div>
      </div>

      <div class="feedback-section">
        <p class="feedback-title">这份审查报告对您有帮助吗？</p>
        <div class="feedback-buttons">
          <button class="feedback-btn useful" @click="openFeedback('useful')">
            <span class="emoji">👍</span>
            <span>有帮助</span>
          </button>
          <button class="feedback-btn not-useful" @click="openFeedback('not_useful')">
            <span class="emoji">👎</span>
            <span>需要改进</span>
          </button>
        </div>
      </div>

      <div class="download-buttons">
        <button class="download-btn txt-btn" @click="downloadAsTxt">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
          下载为TXT
        </button>
        
        <button class="download-btn docx-btn" @click="downloadAsDocx">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
          下载为Word
        </button>
        
        <button class="download-btn pdf-btn" @click="downloadAsPdf">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
          下载为PDF
        </button>
      </div>
    </div>

    <!-- 反馈模态框 -->
    <FeedbackModal
      :show="showFeedbackModal"
      :report-id="reportId"
      :expected-file-hash="expectedFileHash"
      @close="showFeedbackModal = false"
      @success="handleFeedbackSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { marked } from 'marked'
import FeedbackModal from './FeedbackModal.vue'
import { ElMessage } from 'element-plus'
import { getRecord } from '../utils/api'

const router = useRouter()
const route = useRoute()

const renderedMarkdown = ref('')
const showFeedbackModal = ref(false)
const reportId = ref('')
const initialFeedbackType = ref('')
const contract = ref(null)
const contractText = ref('')

const actualResult = computed(() => {
  if (contract.value && contract.value.report_markdown) {
    return contract.value.report_markdown
  }
  return ''
})

const expectedFileHash = computed(() => {
  if (contract.value && contract.value.metadata && contract.value.metadata.file_hash) {
    return contract.value.metadata.file_hash
  }
  return ''
})

onMounted(async () => {
  const recordId = route.params.id
  if (recordId) {
    try {
      const record = await getRecord(recordId)
      if (record && record.report_markdown) {
        contract.value = record
        contractText.value = record.metadata?.contract_text || ''
        renderedMarkdown.value = marked(record.report_markdown || '')
      } else {
        renderedMarkdown.value = '<p style="color: #999; text-align: center; padding: 40px;">未找到审查结果</p>'
      }
    } catch (error) {
      console.error('获取报告失败:', error)
      const message = error.response?.status === 404
        ? '报告不存在或无权访问。历史缺失报告不会关联其他记录。'
        : '获取审查结果失败，请稍后重试。'
      renderedMarkdown.value = `<p style="color: #999; text-align: center; padding: 40px;">${message}</p>`
    }
  } else {
    renderedMarkdown.value = '<p style="color: #999; text-align: center; padding: 40px;">缺少报告ID</p>'
  }
  reportId.value = String(recordId)
})

const goBack = () => {
  router.back()
}

const openFeedback = (type) => {
  const token = localStorage.getItem('token')
  if (!token) {
    ElMessage.warning('请先登录后再提交反馈')
    router.push('/login')
    return
  }
  initialFeedbackType.value = type
  showFeedbackModal.value = true
}

const handleFeedbackSuccess = (response) => {
  ElMessage.success(response.message)
}

const downloadAsTxt = () => {
  const text = actualResult.value.replace(/[#*`]/g, '')
  const baseName = contract.value ? contract.value.filename.replace(/\.[^/.]+$/, '') : '合同审查'
  downloadFile(text, `${baseName}_审查结果.txt`, 'text/plain')
}

const downloadAsDocx = () => {
  const text = actualResult.value.replace(/[#*`]/g, '')
  const baseName = contract.value ? contract.value.filename.replace(/\.[^/.]+$/, '') : '合同审查'
  const content = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>
      <w:r>
        <w:t>${escapeXml(text)}</w:t>
      </w:r>
    </w:p>
  </w:body>
</w:document>`

  const zip = createDocx(content)
  downloadFile(zip, `${baseName}_审查结果.docx`, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
}

const downloadAsPdf = () => {
  const text = actualResult.value.replace(/[#*`]/g, '')
  const baseName = contract.value ? contract.value.filename.replace(/\.[^/.]+$/, '') : '合同审查'
  const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>合同审查报告</title>
  <style>
    body { font-family: SimSun, serif; padding: 40px; line-height: 1.8; }
    h1 { text-align: center; color: #333; }
    h2 { color: #409EFF; border-bottom: 2px solid #409EFF; padding-bottom: 10px; }
    h3 { color: #666; }
    p { margin: 10px 0; }
    ul, ol { margin-left: 20px; }
  </style>
</head>
<body>
  <h1>合同审查报告</h1>
  <div>${marked(actualResult.value)}</div>
</body>
</html>`

  downloadFile(htmlContent, `${baseName}_审查结果.html`, 'text/html')
  ElMessage.info('已下载为HTML文件，可使用浏览器打印功能转换为PDF')
}

const downloadFile = (content, filename, type) => {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const escapeXml = (text) => {
  const replacements = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&apos;'
  }
  return text.replace(/[&<>"']/g, match => replacements[match])
}

const createDocx = (content) => {
  return content
}
</script>

<style scoped>
.result-container {
  min-height: 100vh;
  background: #FEFEFE;
  padding: 20px;
}

.result-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  max-width: 900px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 40px 20px;
  border-bottom: 1px solid #eee;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #f5f7fa;
  border: none;
  border-radius: 8px;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #e8eef5;
  color: #4080FF;
}

.result-content {
  padding: 30px 40px;
  max-height: 600px;
  overflow-y: auto;
}

.result-content :deep(h1) {
  font-size: 20px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  /* 移除下划线，避免与报告标题重复 */
}

.result-content :deep(h2) {
  font-size: 16px;
  color: #4080FF;
  margin-top: 20px;
  margin-bottom: 10px;
}

.result-content :deep(h3) {
  font-size: 14px;
  color: #666;
  margin-top: 15px;
  margin-bottom: 8px;
}

.result-content :deep(p) {
  font-size: 14px;
  color: #555;
  line-height: 1.8;
  margin: 8px 0;
}

.result-content :deep(ul),
.result-content :deep(ol) {
  margin-left: 20px;
  padding-left: 0;
}

.result-content :deep(li) {
  font-size: 14px;
  color: #555;
  line-height: 1.8;
  margin: 5px 0;
}

.result-content :deep(strong) {
  color: #333;
  font-weight: 600;
}

.result-content :deep(code) {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.feedback-section {
  padding: 20px 40px;
  border-top: 1px solid #eee;
  background: #fafafa;
}

.feedback-title {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #666;
}

.feedback-buttons {
  display: flex;
  gap: 15px;
}

.feedback-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 25px;
  border: none;
  border-radius: 25px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.feedback-btn.useful {
  background: #e8f5e9;
  color: #27ae60;
}

.feedback-btn.useful:hover {
  background: #c8e6c9;
}

.feedback-btn.not-useful {
  background: #fff3e0;
  color: #f39c12;
}

.feedback-btn.not-useful:hover {
  background: #ffe0b2;
}

.emoji {
  font-size: 18px;
}

.download-buttons {
  display: flex;
  gap: 15px;
  padding: 20px 40px;
  border-top: 1px solid #eee;
}

.download-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.download-btn.txt-btn {
  background: #4080FF;
  color: white;
}

.download-btn.txt-btn:hover {
  background: #3070EE;
}

.download-btn.docx-btn {
  background: #27ae60;
  color: white;
}

.download-btn.docx-btn:hover {
  background: #1e8449;
}

.download-btn.pdf-btn {
  background: #e74c3c;
  color: white;
}

.download-btn.pdf-btn:hover {
  background: #c0392b;
}
</style>
