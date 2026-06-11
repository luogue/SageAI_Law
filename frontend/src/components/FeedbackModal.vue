<template>
  <div v-if="show" class="modal-overlay" @click.self="handleClose">
    <div class="modal-content">
      <div class="modal-header">
        <h2>帮助我们改进 SageAI</h2>
        <button class="close-btn" @click="handleClose">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <div class="modal-body">
        <div class="feedback-type">
          <p class="label">您觉得这份审查报告：</p>
          <div class="type-buttons">
            <button
              class="type-btn"
              :class="{ active: feedbackType === 'useful' }"
              @click="feedbackType = 'useful'"
            >
              <span class="emoji">👍</span>
              <span>很有帮助</span>
            </button>
            <button
              class="type-btn"
              :class="{ active: feedbackType === 'not_useful' }"
              @click="feedbackType = 'not_useful'"
            >
              <span class="emoji">👎</span>
              <span>不太有用</span>
            </button>
            <button
              class="type-btn"
              :class="{ active: feedbackType === 'detailed' }"
              @click="feedbackType = 'detailed'"
            >
              <span class="emoji">📝</span>
              <span>需要更详细</span>
            </button>
          </div>
        </div>

        <div class="categories">
          <p class="label">请选择问题分类（可多选）：</p>
          <div class="category-buttons">
            <button
              v-for="cat in categoryOptions"
              :key="cat"
              class="category-btn"
              :class="{ active: categories.includes(cat) }"
              @click="toggleCategory(cat)"
            >
              {{ cat }}
            </button>
          </div>
        </div>

        <div class="comment">
          <p class="label">详细描述（20-500个字符）：</p>
          <textarea
            v-model="comment"
            placeholder="请告诉我们您的具体想法或建议..."
            rows="4"
            maxlength="500"
          ></textarea>
          <div class="char-count">
            <span :class="{ error: comment.length > 0 && comment.length < 20 }">
              {{ comment.length }}/500
            </span>
          </div>
        </div>

        <div class="upload-consent">
            <label class="checkbox-label">
                <input type="checkbox" v-model="uploadConsent" @change="handleConsentChange">
                <span>同意上传本次合同文本，仅用于模型训练（严格保密）</span>
            </label>
            <div class="reward-notice basic">
                <p>📌 提交反馈后，我们将在1-2个工作日内审核，审核通过后将赠送您3次免费审查额度。</p>
            </div>
        </div>

        <div v-if="uploadConsent" class="contract-upload">
          <p class="label">上传合同文件：</p>
          <div class="file-upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleFileDrop">
            <input
              ref="contractFileInput"
              type="file"
              accept=".docx,.txt,.pdf"
              style="display:none"
              @change="handleFileSelect"
            />
            <div v-if="!contractFile" class="upload-placeholder">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#409EFF" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="12" y1="18" x2="12" y2="12"></line>
                <line x1="9" y1="15" x2="15" y2="15"></line>
              </svg>
              <p>点击或拖拽上传合同文件</p>
              <span class="file-hint">支持 .docx、.txt、.pdf 格式，单文件不超过10MB</span>
            </div>
            <div v-else class="uploaded-file">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#67C23A" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
              </svg>
              <span class="file-name">{{ contractFile.name }}</span>
              <button class="remove-file-btn" @click.stop="removeContractFile">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="cancel-btn" @click="handleClose">取消</button>
        <button
          class="submit-btn"
          :class="{ disabled: isSubmitting || !feedbackType }"
          :disabled="isSubmitting || !feedbackType"
          @click="handleSubmit"
        >
          <span v-if="isSubmitting" class="loading-spinner"></span>
          {{ isSubmitting ? '提交中...' : '提交反馈' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || '/api'
const BASE_URL = API_BASE.startsWith('http') ? API_BASE.replace(/\/$/, '') + '/api' : API_BASE

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  reportId: {
    type: String,
    default: ''
  },
  expectedFileHash: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'success'])

const feedbackType = ref('')
const categories = ref([])
const comment = ref('')
const uploadConsent = ref(false)
const isSubmitting = ref(false)
const contractFile = ref(null)
const contractFileInput = ref(null)

const categoryOptions = [
  '风险遗漏',
  '误判',
  '建议不实用',
  '格式问题',
  '其他'
]

const toggleCategory = (cat) => {
  const index = categories.value.indexOf(cat)
  if (index > -1) {
    categories.value.splice(index, 1)
  } else {
    categories.value.push(cat)
  }
}

const handleConsentChange = () => {
  if (!uploadConsent.value) {
    contractFile.value = null
  }
}

const triggerFileInput = () => {
  contractFileInput.value?.click()
}

const handleFileDrop = (event) => {
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    handleFile(files[0])
  }
}

const handleFileSelect = (event) => {
  const files = event.target?.files
  if (files && files.length > 0) {
    handleFile(files[0])
  }
}

// 计算文件MD5
async function calculateFileMD5(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = async (e) => {
      try {
        const buffer = e.target.result
        const SparkMD5 = await import('spark-md5')
        const hash = SparkMD5.default.ArrayBuffer.hash(buffer)
        resolve(hash)
      } catch (error) {
        reject(error)
      }
    }
    reader.onerror = reject
    reader.readAsArrayBuffer(file)
  })
}

const handleFile = async (file) => {
  const allowedExtensions = ['.docx', '.txt', '.pdf']
  const extension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'))
  
  if (!allowedExtensions.includes(extension)) {
    ElMessage.warning('不支持的文件格式，请上传 .docx、.txt、.pdf 文件')
    return
  }
  
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.warning('文件大小超过限制（最大10MB）')
    return
  }
  
  // ========== MD5校验：确保上传的合同文件与原始审查的合同一致 ==========
  if (props.expectedFileHash) {
    try {
      const fileHash = await calculateFileMD5(file)
      console.log('[反馈上传-MD5校验] 期望hash:', props.expectedFileHash, '实际hash:', fileHash)
      
      if (fileHash !== props.expectedFileHash) {
        ElMessage.error('上传的合同文件与原始审查的合同不一致，请上传原始合同文件')
        return
      }
      console.log('[反馈上传-MD5校验] ✅ MD5一致，允许上传')
    } catch (error) {
      console.error('[反馈上传-MD5校验] 计算MD5失败:', error)
      ElMessage.error('文件校验失败，请重试')
      return
    }
  }
  
  // ========== 字数校验：检查合同字数上限 ==========
  try {
    const text = await file.text()
    // 统计中文字数
    const chineseChars = text.match(/[\u4e00-\u9fff]/g) || []
    const chineseCount = chineseChars.length
    const totalChars = text.length
    const MAX_WORDS = 20000
    
    console.log(`[反馈上传-字数校验] 文件名: ${file.name}, 中文字数: ${chineseCount}, 总字符数: ${totalChars}, 上限: ${MAX_WORDS}`)
    
    if (chineseCount > MAX_WORDS) {
      console.warn(`[反馈上传-字数校验] ❌ 校验失败 - 中文字数 ${chineseCount} 超过上限 ${MAX_WORDS}`)
      ElMessage.error(`合同文本过长（当前${chineseCount}字），单次最大上传字数为 ${MAX_WORDS} 字。建议您精简合同或选择核心章节上传。`)
      return
    }
    console.log(`[反馈上传-字数校验] ✅ 校验通过 - 中文字数 ${chineseCount}`)
  } catch (error) {
    console.error('[反馈上传-字数校验] 读取文件内容失败:', error)
    // 读取失败不阻止上传，后端会再次校验
  }
  
  contractFile.value = file
}

const removeContractFile = () => {
  contractFile.value = null
}

const handleClose = () => {
  // 重置表单
  feedbackType.value = ''
  categories.value = []
  comment.value = ''
  uploadConsent.value = false
  contractFile.value = null
  isSubmitting.value = false
  emit('close')
}

const handleSubmit = async () => {
  if (!feedbackType.value || isSubmitting.value) {
    return
  }

  // 验证问题分类是否必选
  if (categories.value.length === 0) {
    ElMessage.warning('请至少选择一个问题分类')
    return
  }

  // 验证描述长度
  if (comment.value.trim().length < 20) {
    ElMessage.warning('反馈描述至少需要20个字符')
    return
  }

  isSubmitting.value = true

  try {
    const formData = new FormData()
    formData.append('report_id', props.reportId)
    formData.append('feedback_type', feedbackType.value)
    formData.append('categories', JSON.stringify(categories.value))
    formData.append('comment', comment.value)
    formData.append('upload_consent', String(uploadConsent.value))
    
    // 如果用户同意上传合同，附加文件及期望的MD5哈希值
    if (uploadConsent.value && contractFile.value) {
      formData.append('contract_file', contractFile.value)
      if (props.expectedFileHash) {
        formData.append('expected_file_hash', props.expectedFileHash)
      }
    }

    const token = localStorage.getItem('token')
    const response = await fetch(`${BASE_URL}/feedback`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })

    const data = await response.json()

    if (data.success) {
      ElMessage.success('感谢您的反馈！我们将尽快审核，审核通过后将赠送您免费审查额度。')
      emit('success', data)
      handleClose()
    } else {
      ElMessage.error(data.message || '提交反馈失败')
    }
  } catch (error) {
    console.error('提交反馈失败:', error)
    ElMessage.error('提交反馈失败，请稍后重试')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f5f7fa;
  color: #666;
}

.modal-body {
  padding: 24px;
}

.label {
  color: #333;
  font-weight: 500;
  margin-bottom: 12px;
  font-size: 14px;
}

.feedback-type {
  margin-bottom: 24px;
}

.type-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.type-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 12px;
  background: #f5f7fa;
  border: 2px solid transparent;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.type-btn:hover {
  background: #e8ecf0;
}

.type-btn.active {
  background: #e8f4fd;
  border-color: #409EFF;
  color: #409EFF;
}

.type-btn .emoji {
  font-size: 24px;
}

.type-btn span {
  font-size: 13px;
}

.categories {
  margin-bottom: 24px;
}

.category-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-btn {
  padding: 8px 16px;
  background: #f5f7fa;
  border: 2px solid transparent;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  color: #666;
  transition: all 0.2s;
}

.category-btn:hover {
  background: #e8ecf0;
}

.category-btn.active {
  background: #e8f4fd;
  border-color: #409EFF;
  color: #409EFF;
}

.comment {
  margin-bottom: 24px;
}

.comment textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
  box-sizing: border-box;
}

.comment textarea:focus {
  outline: none;
  border-color: #409EFF;
}

.char-count {
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.char-count .error {
  color: #f56c6c;
  font-weight: 500;
}

.upload-consent {
  margin-bottom: 24px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input {
  margin-top: 2px;
}

.reward-notice {
  margin-top: 12px;
  padding: 12px;
  background: #e8f4fd;
  border-radius: 8px;
  border-left: 4px solid #409EFF;
}

.reward-notice.basic {
  background: #f5f7fa;
  border-left-color: #999;
}

.reward-notice p {
  margin: 0;
  color: #409EFF;
  font-size: 13px;
  line-height: 1.6;
}

.reward-notice.basic p {
  color: #666;
}

.contract-upload {
  margin-bottom: 24px;
}

.file-upload-area {
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s;
}

.file-upload-area:hover {
  border-color: #409EFF;
  background: #f0f7ff;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.upload-placeholder p {
  margin: 0;
  color: #409EFF;
  font-size: 14px;
}

.upload-placeholder .file-hint {
  font-size: 12px;
  color: #999;
}

.uploaded-file {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f0f9eb;
  border-radius: 6px;
}

.uploaded-file .file-name {
  flex: 1;
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-file-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 2px;
  border-radius: 4px;
  flex-shrink: 0;
}

.remove-file-btn:hover {
  color: #f56c6c;
  background: #fef0f0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #eee;
}

.cancel-btn {
  padding: 12px 24px;
  background: #f5f7fa;
  border: none;
  border-radius: 8px;
  color: #666;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background: #e8ecf0;
}

.submit-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.submit-btn:hover:not(.disabled) {
  opacity: 0.9;
}

.submit-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
