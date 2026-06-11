<template>
  <div class="upload-container">
    <!-- 错误提示模态框 -->
    <div v-if="showErrorModal" class="modal-overlay" @click="closeErrorModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <span class="modal-title">错误提示</span>
          <button class="modal-close" @click="closeErrorModal">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <pre class="error-text">{{ errorMessage }}</pre>
        </div>
        <div class="modal-footer">
          <button class="modal-confirm" @click="closeErrorModal">确定</button>
        </div>
      </div>
    </div>

    <div class="upload-card">
      <div class="header">
        <h1>明月AI（Sage）合同审查</h1>
        <p>支持多文件批量上传审查</p>
      </div>

      <!-- 隐私保护提示 -->
      <div class="privacy-notice">
        <div class="privacy-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
        </div>
        <div class="privacy-text">
          <strong>隐私保护提示：</strong>为保护您的隐私，我们不会保存您上传的合同原文。生成的审查报告将自动保存至您的账户，供随时查阅。您也可自行删除。
        </div>
      </div>

      <!-- 超长合同提示 -->
      <div class="length-notice">
        <div class="length-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
        <div class="length-text">
          <strong>审查质量提示：</strong>为保证审查质量，建议上传合同不超过1万字；超长合同可能遗漏部分条款，建议拆分后逐份上传。
        </div>
      </div>

      <!-- 上传区域 -->
      <div 
        class="upload-area"
        :class="{ 'drag-over': isDragOver }"
        @dragenter.prevent="handleDragEnter"
        @dragover.prevent="handleDragOver"
        @dragleave.prevent="handleDragLeave"
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <input 
          ref="fileInput"
          type="file"
          class="file-input"
          :accept="acceptTypes"
          multiple
          @change="handleFileSelect"
        />
        
        <div class="upload-icon">
          <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M32 16V40M32 40L22 30M32 40L42 30" stroke="#409EFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
            <rect x="16" y="44" width="32" height="16" rx="2" stroke="#409EFF" stroke-width="2"></rect>
          </svg>
        </div>
        
        <p class="upload-text">点击或拖拽文件到此处上传</p>
        <p class="upload-hint">支持 .docx、.txt、.pdf 格式，单个文件不超过10MB</p>
      </div>



      <!-- 文件列表 -->
      <div v-if="contracts.length > 0" class="file-list">
        <div class="list-header">
          <span>文件列表</span>
          <span class="count">{{ contracts.length }} 个文件</span>
        </div>
        
        <div class="list-content">
          <div 
            v-for="contract in contracts" 
            :key="contract.id" 
            class="file-item"
          >
            <div class="file-info">
              <div class="file-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
              </div>
              <div class="file-details">
                <span class="filename">{{ contract.filename }}</span>
                <span class="filesize">{{ formatFileSize(contract.fileSize) }}</span>
              </div>
            </div>
            
            <div class="file-status">
              <span :class="getStatusClass(contract.status)">{{ getStatusText(contract.status) }}</span>
            </div>
            
            <div class="file-progress">
              <div class="mini-progress-bar">
                <div 
                  class="mini-progress-fill" 
                  :style="{ width: contract.progress + '%' }"
                  :class="getStatusClass(contract.status)"
                ></div>
              </div>
              <span class="progress-text">{{ contract.progress }}%</span>
            </div>
            
            <div class="file-actions">
              <button 
                v-if="contract.status === 'completed'"
                class="action-btn view-btn"
                @click="viewResult(contract)"
                title="查看结果"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0"></path>
                  <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7"></path>
                </svg>
              </button>
              
              <button 
                v-if="contract.status === 'completed'"
                class="action-btn download-btn"
                @click="downloadResult(contract)"
                title="下载报告"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
              </button>
              
              <button 
                class="action-btn delete-btn"
                @click="removeContract(contract)"
                title="删除"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 额外审查要求 -->
      <div class="additional-input">
        <label>额外审查要求（对所有文件生效）</label>
        <textarea 
          v-model="additionalInstructions"
          placeholder="请输入您的额外审查要求或背景说明，例如：重点审查保密条款、关注违约责任等..."
          rows="3"
        ></textarea>
      </div>

      <!-- 整体进度 -->
      <div v-if="contracts.length > 0" class="overall-progress">
        <div class="progress-header">
          <span>整体进度</span>
          <span>{{ completedCount }} / {{ contracts.length }}</span>
        </div>
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :style="{ width: overallProgress + '%' }"
          ></div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button 
          class="batch-btn"
          :disabled="contracts.length === 0 || isProcessing"
          @click="startBatchReview"
        >
          <span v-if="isProcessing" class="loading-spinner"></span>
          <span>{{ isProcessing ? '审查中...' : '批量审查上传' }}</span>
        </button>
        
        <button 
          v-if="completedContracts.length > 0"
          class="download-all-btn"
          @click="downloadAllAsZip"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
          打包下载ZIP
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, onActivated, watch } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { batchReviewContracts, confirmDuplicateContract, getTaskStatus, getBonusCredits } from '../utils/api';
import { initDB, getAllContracts, deleteContract } from '../utils/storage';
import JSZip from 'jszip';
import { marked } from 'marked';

defineOptions({
  name: 'UploadPage'
});

const router = useRouter();
const emit = defineEmits(['update-credits']);

const fileInput = ref(null);
const contracts = ref([]);
const additionalInstructions = ref('');
const isProcessing = ref(false);
const isDragOver = ref(false);
const acceptTypes = '.docx,.txt,.pdf';
const allowedExtensions = ['.docx', '.txt', '.pdf'];
const maxFileSize = 10 * 1024 * 1024;
const showErrorModal = ref(false);
const errorMessage = ref('');

let isPageUnmounting = false;

// SSE 连接池：每个任务一个 EventSource 连接，后端主动推送进度
// 取代了原来的 setTimeout 轮询 —— 只需一次连接即可收到完整进度流
const taskEventSources = {};

function closeAllTaskStreams() {
  Object.keys(taskEventSources).forEach(taskId => {
    try { taskEventSources[taskId].close(); } catch (e) {}
    delete taskEventSources[taskId];
  });
}

function connectTaskStream(taskId, contract) {
  // 如果已有连接，先关闭
  if (taskEventSources[taskId]) {
    try { taskEventSources[taskId].close(); } catch (e) {}
  }
  
  const url = `/api/task/${taskId}/stream`;
  const es = new EventSource(url);
  taskEventSources[taskId] = es;
  
  es.addEventListener('status', (e) => {
    try {
      const data = JSON.parse(e.data);
      contract.status = data.status;
      contract.progress = data.progress;
    } catch (err) {
      console.error('SSE status 解析失败:', err);
    }
  });
  
  es.addEventListener('progress', (e) => {
    try {
      const data = JSON.parse(e.data);
      contract.status = data.status;
      contract.progress = data.progress;
    } catch (err) {
      console.error('SSE progress 解析失败:', err);
    }
  });
  
  es.addEventListener('result', (e) => {
    try {
      const data = JSON.parse(e.data);
      contract.status = data.status;
      contract.progress = data.progress;
      contract.result = data.result;
      contract.error = data.error;
      contract.metadata = data.metadata;
      contract.validation = data.validation;
      contract.summary = data.summary;
      contract.recordId = data.record_id;
      
      if (data.remaining_bonus !== null && data.remaining_bonus !== undefined) {
        emit('update-credits', data.remaining_bonus);
      }
      
      if (contract.status === 'completed') {
        console.log(`合同 ${contract.filename} 完成，记录ID: ${contract.recordId}`);
      }
      
      // 任务结束，关闭连接
      try { es.close(); } catch (e) {}
      delete taskEventSources[taskId];
      
      // 检查是否所有任务都完成了
      checkAllTasksDone();
    } catch (err) {
      console.error('SSE result 解析失败:', err);
    }
  });
  
  es.addEventListener('error', (e) => {
    let errData;
    try { errData = JSON.parse(e.data); } catch (_) { errData = { error: '连接异常' }; }
    contract.status = 'failed';
    contract.error = errData.error || '任务流异常';
    try { es.close(); } catch (_) {}
    delete taskEventSources[taskId];
    checkAllTasksDone();
  });
  
  es.onerror = () => {
    // EventSource 网络错误（EventSource 会自动重连，但我们不需要）
    if (es.readyState === EventSource.CLOSED) {
      delete taskEventSources[taskId];
    }
  };
}

function checkAllTasksDone() {
  const stillPending = contracts.value.some(
    c => c.taskId && c.status !== 'completed' && c.status !== 'failed'
  );
  if (!stillPending) {
    isProcessing.value = false;
    
    const failedContracts = contracts.value.filter(c => c.status === 'failed');
    if (failedContracts.length && !isPageUnmounting) {
      const errorMessages = failedContracts.map(c => `${c.filename}: ${c.error || '审查失败'}`);
      ElMessage.error(`部分合同审查失败:\n${errorMessages.join('\n')}`);
    } else if (!failedContracts.length && !isPageUnmounting) {
      ElMessage.success('所有合同审查完成');
    }
  }
}

const completedContracts = computed(() => contracts.value.filter(c => c.status === 'completed'));
const completedCount = computed(() => completedContracts.value.length);
const overallProgress = computed(() => {
  if (contracts.value.length === 0) {
    return 0;
  }
  const total = contracts.value.reduce((sum, c) => sum + c.progress, 0);
  return Math.round(total / contracts.value.length);
});

// 组件挂载时加载
onMounted(async () => {
  await initDB();
  // 只在首次挂载时初始化，KeepAlive 缓存恢复时不执行
  console.log('UploadPage 组件已挂载，contracts 数组保持缓存状态');
});

// 组件激活时（从 KeepAlive 缓存恢复）
onActivated(() => {
  console.log('UploadPage 从缓存激活，文件列表应保持原样');
  // 注意：不要在onActivated中自动启动轮询，避免切换页面时重复调用api/task
  // 轮询应该只在用户点击"批量审查上传"按钮后启动
});

onUnmounted(() => {
  isPageUnmounting = true;
  closeAllTaskStreams();
});

function triggerFileInput() {
  fileInput.value?.click();
}

function handleFileSelect(event) {
  const files = Array.from(event.target.files || []);
  addFiles(files);
}

function handleDragEnter() {
  isDragOver.value = true;
}

function handleDragOver() {
  isDragOver.value = true;
}

function handleDragLeave() {
  isDragOver.value = false;
}

function handleDrop(event) {
  isDragOver.value = false;
  const files = Array.from(event.dataTransfer?.files || []);
  addFiles(files);
}

function validateFile(file) {
  const extension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
  
  if (!allowedExtensions.includes(extension)) {
    return {
      valid: false,
      message: '不支持的文件格式，请上传.docx/.txt/.pdf文件',
      filename: file.name
    };
  }
  
  if (file.size > maxFileSize) {
    return {
      valid: false,
      message: '文件大小超过限制（最大10MB）',
      filename: file.name
    };
  }
  
  if (contracts.value.some(c => c.filename === file.name && c.status !== 'completed')) {
    return {
      valid: false,
      message: '文件已在列表中',
      filename: file.name
    };
  }
  
  return {
    valid: true,
    message: '',
    filename: file.name
  };
}

function showError(message) {
  errorMessage.value = message;
  showErrorModal.value = true;
}

function closeErrorModal() {
  showErrorModal.value = false;
  errorMessage.value = '';
}

// 计算文件的MD5哈希值
async function calculateFileMD5(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const buffer = e.target.result;
        // 使用spark-md5库计算MD5哈希值（与后端保持一致）
        const SparkMD5 = await import('spark-md5');
        const hash = SparkMD5.default.ArrayBuffer.hash(buffer);
        resolve(hash);
      } catch (error) {
        reject(error);
      }
    };
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

// 检查文件是否已在后端完成审查
async function checkDuplicateByHash(fileHash) {
  try {
    // 获取所有已完成审查的记录
    const { getRecords } = await import('../utils/api');
    const records = await getRecords();
    
    console.log('=== MD5重复检查调试信息 ===');
    console.log('当前文件hash:', fileHash);
    console.log('获取到的记录数:', records?.length || 0);
    
    if (records && Array.isArray(records)) {
      // 打印所有记录的metadata
      records.forEach((record, index) => {
        console.log(`记录${index + 1}:`, {
          id: record.id,
          filename: record.filename,
          file_hash: record.metadata?.file_hash || '无'
        });
      });
      
      // 检查是否有相同hash的记录
      const duplicate = records.find(record => 
        record.metadata?.file_hash === fileHash
      );
      
      if (duplicate) {
        console.log('找到重复记录:', duplicate);
      } else {
        console.log('未找到重复记录');
      }
      
      return duplicate;
    }
    return null;
  } catch (error) {
    console.error('检查重复文件失败:', error);
    return null;
  }
}

async function addFiles(files) {
  for (const file of files) {
    const validation = validateFile(file);
    
    if (!validation.valid) {
      ElMessage.warning(`${validation.filename}: ${validation.message}`);
      continue;
    }
    
    // 计算文件MD5并检查是否重复
    try {
      const fileHash = await calculateFileMD5(file);
      
      // 先检查当前会话中是否有重复
      const localDuplicate = contracts.value.find(c => 
        c.fileHash === fileHash && c.status === 'completed'
      );
      
      if (localDuplicate) {
        ElMessage.warning(`${file.name}: 该合同已上传并生成审查结果，请勿重复上传`);
        continue;
      }
      
      // 再检查后端数据库中是否有重复
      const serverDuplicate = await checkDuplicateByHash(fileHash);
      if (serverDuplicate) {
        ElMessage.warning(`${file.name}: 该合同已在"我的报告"中存在，请勿重复上传`);
        continue;
      }
      
      const contract = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
        filename: file.name,
        fileSize: file.size,
        status: 'pending',
        progress: 0,
        file: file,
        fileHash: fileHash,  // 保存文件hash
        result: null,
        error: null,
        metadata: null,
        validation: null,
        summary: null,
        taskId: null,
        createdAt: new Date().toISOString()
      };
      contracts.value.push(contract);
    } catch (error) {
      console.error('计算文件hash失败:', error);
      // 如果计算hash失败，仍然添加文件，但不进行重复检查
      const contract = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
        filename: file.name,
        fileSize: file.size,
        status: 'pending',
        progress: 0,
        file: file,
        fileHash: null,
        result: null,
        error: null,
        metadata: null,
        validation: null,
        summary: null,
        taskId: null,
        createdAt: new Date().toISOString()
      };
      contracts.value.push(contract);
    }
  }
}

function removeContract(contract) {
  const index = contracts.value.findIndex(c => c.id === contract.id);
  if (index !== -1) {
    contracts.value.splice(index, 1);
    if (contract.status === 'completed') {
      deleteContract(contract.id);
    }
  }
}

function getStatusClass(status) {
  switch (status) {
    case 'completed': return 'status-completed';
    case 'failed': return 'status-failed';
    case 'processing': return 'status-processing';
    case 'uploading': return 'status-uploading';
    default: return 'status-pending';
  }
}

function getStatusText(status) {
  switch (status) {
    case 'completed': return '已完成';
    case 'failed': return '失败';
    case 'processing': return '审查中';
    case 'uploading': return '上传和审查中';
    default: return '等待中';
  }
}

function formatFileSize(bytes) {
  if (bytes === 0) {
    return '0 B';
  }
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function startBatchReview() {
  if (contracts.value.length === 0 || isProcessing.value) {
    return;
  }
  
  // 检查剩余额度
  try {
    const credits = await getBonusCredits();
    if (credits.bonus_credits <= 0) {
      ElMessage.warning('您的免费额度已用完，请获取更多额度后再试');
      return;
    }
  } catch (error) {
    console.error('获取额度失败:', error);
    ElMessage.error('获取额度信息失败，请稍后重试');
    return;
  }
  
  isProcessing.value = true;
  
  const pendingContracts = contracts.value.filter(c => c.status === 'pending' || c.status === 'failed');
  
  try {
    // 逐个处理文件，以便处理重复上传的情况
    for (const contract of pendingContracts) {
      contract.status = 'uploading';
      contract.progress = 10;
      
      try {
        const response = await batchReviewContracts([contract.file], additionalInstructions.value);
        
        if (response.success && response.task_ids && response.task_ids.length > 0) {
          contract.taskId = response.task_ids[0];
          contract.status = 'uploading';
          contract.progress = 20;
        } else {
          contract.status = 'failed';
          contract.error = response.message || '提交失败';
        }
      } catch (error) {
        // 处理重复上传错误
        if (error.response && error.response.status === 409) {
          const detail = error.response.data || {};
          
          if (detail.error_code === 'DUPLICATE_UPLOAD') {
            // 弹出确认对话框
            try {
              await ElMessageBox.confirm(
                detail.message,
                '重复上传确认',
                {
                  confirmButtonText: '继续审查',
                  cancelButtonText: '取消',
                  type: 'warning'
                }
              );
              
              // 用户确认后，调用确认重复上传接口
              const response = await confirmDuplicateContract(contract.file, additionalInstructions.value);
              
              if (response.success) {
                contract.result = response.result;
                contract.metadata = response.metadata;
                contract.validation = response.validation;
                contract.summary = response.summary;
                contract.recordId = response.record_id;
                contract.status = 'completed';
                contract.progress = 100;
                
                if (response.remaining_bonus !== null && response.remaining_bonus !== undefined) {
                  emit('update-credits', response.remaining_bonus);
                }
              } else {
                contract.status = 'failed';
                contract.error = response.message || '处理失败';
              }
            } catch (cancelError) {
              // 用户取消
              contract.status = 'pending';
              contract.progress = 0;
              ElMessage.info('已取消审查');
            }
          } else {
            contract.status = 'failed';
            contract.error = detail.message || '处理失败';
          }
        } else if (error.response && error.response.status === 400) {
          // 处理批量上传时的拒绝文件错误
          const detail = error.response.data || {};
          if (detail.rejected_files && detail.rejected_files.length > 0) {
            const rejectedFile = detail.rejected_files.find(rf => rf.filename === contract.filename);
            if (rejectedFile) {
              if (rejectedFile.error_code === 'DUPLICATE_UPLOAD') {
                // MD5重复，提示用户
                ElMessage.warning(rejectedFile.message);
                contract.status = 'failed';
                contract.error = rejectedFile.message;
              } else {
                contract.status = 'failed';
                contract.error = rejectedFile.message || '文件被拒绝';
              }
            } else {
              contract.status = 'failed';
              contract.error = detail.message || '请求参数错误';
            }
          } else {
            contract.status = 'failed';
            contract.error = detail.message || '请求参数错误';
          }
        } else {
          let errorMsg = '提交失败: ';
          if (error.response) {
            const status = error.response.status;
            const detail = error.response.data || {};
            
            if (status === 400) {
              errorMsg = detail.message || '请求参数错误';
            } else if (status === 422) {
              errorMsg = detail.message || '文件校验失败';
            } else if (status === 500) {
              errorMsg = detail.message || '服务器内部错误';
            }
          } else {
            errorMsg += error.message;
          }
          contract.status = 'failed';
          contract.error = errorMsg;
        }
      }
    }
    
    // 为每个有 taskId 的任务建立 SSE 连接（替代轮询）
    const hasProcessingTasks = contracts.value.some(c => c.taskId && c.status !== 'completed' && c.status !== 'failed');
    
    if (hasProcessingTasks) {
      contracts.value.forEach(contract => {
        if (contract.taskId && contract.status !== 'completed' && contract.status !== 'failed') {
          connectTaskStream(contract.taskId, contract);
        }
      });
    } else {
      // 所有任务都已完成或失败，重置状态
      isProcessing.value = false;
    }
  } catch (error) {
    console.error('批量审查失败:', error);
    ElMessage.error('批量审查失败: ' + error.message);
    isProcessing.value = false;
  }
}

async function viewResult(contract) {
  // 如果有recordId，直接跳转
  if (contract.recordId) {
    router.push(`/report/${contract.recordId}`);
    return;
  }
  
  // 如果没有recordId但有taskId，尝试从任务状态获取
  if (contract.taskId) {
    try {
      const taskStatus = await getTaskStatus(contract.taskId);
      if (taskStatus.record_id) {
        contract.recordId = taskStatus.record_id;
        router.push(`/report/${taskStatus.record_id}`);
        return;
      } else {
        // 如果任务已完成但没有recordId，直接跳转到我的报告页面
        router.push('/reports');
        return;
      }
    } catch (error) {
      console.error('获取任务状态失败:', error);
      // 获取失败，直接跳转到我的报告页面
      router.push('/reports');
      return;
    }
  }
  
  // 如果都没有，直接跳转到我的报告页面
  router.push('/reports');
}

function downloadResult(contract) {
  if (!contract.result) {
    return;
  }
  const text = contract.result.replace(/[#*`]/g, '');
  const blob = new Blob([text], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  const baseName = contract.filename.replace(/\.[^/.]+$/, '');
  a.download = `${baseName}_审查结果.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

async function downloadAllAsZip() {
  const zip = new JSZip();
  for (const contract of completedContracts.value) {
    if (contract.result) {
      const text = contract.result.replace(/[#*`]/g, '');
      const baseName = contract.filename.replace(/\.[^/.]+$/, '');
      zip.file(`${baseName}_审查结果.txt`, text);
    }
  }
  const content = await zip.generateAsync({ type: 'blob' });
  const url = URL.createObjectURL(content);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'contract_reviews.zip';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.modal-close {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f5f7fa;
  color: #666;
}

.modal-body {
  padding: 20px;
  max-height: 300px;
  overflow-y: auto;
}

.error-text {
  white-space: pre-wrap;
  word-break: break-all;
  font-size: 14px;
  color: #f56c6c;
  margin: 0;
  font-family: inherit;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

.modal-confirm {
  padding: 8px 24px;
  background: #409EFF;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.modal-confirm:hover {
  background: #3a8ee6;
}

.upload-container {
  flex: 1;
  background: #FEFEFE;
  display: flex;
  justify-content: center;
  padding: 20px;
  padding-top: 40px;
  box-sizing: border-box;
}

.upload-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 30px;
  width: 100%;
  max-width: 800px;
}

.length-notice {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border-left: 4px solid #f59e0b;
  border-radius: 8px;
  margin-bottom: 20px;
}

.length-icon {
  flex-shrink: 0;
  color: #f59e0b;
  margin-top: 2px;
}

.length-text {
  font-size: 13px;
  color: #333;
  line-height: 1.6;
}

.length-text strong {
  color: #d97706;
}

.privacy-notice {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-left: 4px solid #409EFF;
  border-radius: 8px;
  margin-bottom: 20px;
}

.privacy-icon {
  flex-shrink: 0;
  color: #409EFF;
  margin-top: 2px;
}

.privacy-text {
  font-size: 13px;
  color: #333;
  line-height: 1.6;
}

.privacy-text strong {
  color: #409EFF;
}

.header {
  text-align: center;
  margin-bottom: 24px;
}

.header h1 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 22px;
}

.header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 12px;
  padding: 32px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.upload-area:hover {
  border-color: #409EFF;
  background: #f8fafc;
}

.newbie-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 20px;
  color: #92400e;
  font-size: 13px;
  margin-bottom: 20px;
}

.upload-area.drag-over {
  border-color: #409EFF;
  background: #e8f4fd;
}

.file-input {
  display: none;
}

.upload-icon {
  margin-bottom: 12px;
}

.upload-text {
  margin: 0 0 6px 0;
  font-size: 15px;
  color: #333;
}

.upload-hint {
  margin: 0;
  font-size: 12px;
  color: #999;
}

.additional-input {
  margin-bottom: 20px;
}

.additional-input label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: #333;
}

.additional-input textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
  font-size: 13px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.additional-input textarea:focus {
  outline: none;
  border-color: #409EFF;
}

.overall-progress {
  margin-bottom: 16px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
  color: #666;
}

.progress-bar {
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #409EFF, #667eea);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.batch-btn {
  flex: 1;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.batch-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.batch-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.download-all-btn {
  padding: 12px 20px;
  background: #67c23a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.download-all-btn:hover {
  opacity: 0.9;
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

.file-list {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.list-header {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f8fafc;
  border-bottom: 1px solid #eee;
  font-size: 13px;
  color: #666;
}

.list-header .count {
  color: #999;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.2s;
}

.file-item:hover {
  background: #fafafa;
}

.file-item:last-child {
  border-bottom: none;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.file-icon {
  color: #409EFF;
  flex-shrink: 0;
}

.file-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.filename {
  font-size: 13px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.filesize {
  font-size: 11px;
  color: #999;
}

.file-status {
  margin: 0 16px;
}

.file-status span {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
}

.status-pending {
  background: #f5f7fa;
  color: #666;
}

.status-uploading, .status-processing {
  background: #fff7e6;
  color: #e6a23c;
}

.status-completed {
  background: #f0f9ff;
  color: #67c23a;
}

.status-failed {
  background: #fef0f0;
  color: #f56c6c;
}

.file-progress {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 120px;
}

.mini-progress-bar {
  flex: 1;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.mini-progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.mini-progress-fill.status-pending {
  background: #ddd;
}

.mini-progress-fill.status-uploading, .mini-progress-fill.status-processing {
  background: #e6a23c;
}

.mini-progress-fill.status-completed {
  background: #67c23a;
}

.mini-progress-fill.status-failed {
  background: #f56c6c;
}

.progress-text {
  font-size: 11px;
  color: #999;
  width: 35px;
  text-align: right;
}

.file-actions {
  display: flex;
  gap: 6px;
  margin-left: 12px;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.view-btn {
  background: #f0f9ff;
  color: #409EFF;
}

.view-btn:hover {
  background: #e8f4fd;
}

.download-btn {
  background: #f0fdf4;
  color: #67c23a;
}

.download-btn:hover {
  background: #dcfce7;
}

.delete-btn {
  background: #fef2f2;
  color: #f56c6c;
}

.delete-btn:hover {
  background: #fee2e2;
}
</style>
