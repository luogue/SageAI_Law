// API 基础地址：开发环境 http://localhost:8016，生产环境 /api
// 注意：认证接口 /auth 和用户接口 /user 在后端是独立路径，不在 /api 下
const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || '/api'
const isAbsoluteBase = API_BASE.startsWith('http')

// 主业务 API：开发 http://localhost:8016/api，生产 /api
const BASE_URL = isAbsoluteBase ? API_BASE.replace(/\/$/, '') + '/api' : API_BASE

// 认证 API：开发 http://localhost:8016/auth，生产 /auth
const AUTH_URL = isAbsoluteBase ? API_BASE.replace(/\/$/, '') + '/auth' : '/auth'

// 用户 API：开发 http://localhost:8016/user，生产 /user
const USER_URL = isAbsoluteBase ? API_BASE.replace(/\/$/, '') + '/user' : '/user'

// 生成唯一trace_id
function generateTraceId() {
  return 'trace_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 9)
}

// 请求拦截器：添加Authorization头和trace_id
function getAuthHeaders() {
  const token = localStorage.getItem('token')
  const headers = {
    'X-Trace-ID': generateTraceId()
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

// 响应拦截器：处理401错误
async function handleResponse(response) {
  if (response.status === 401) {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    window.location.href = '/login'
    throw new Error('登录已过期，请重新登录')
  }
  const data = await response.json()
  if (!response.ok) {
    // 创建一个包含response信息的错误对象
    const error = new Error(data.detail?.message || data.detail || '请求失败')
    error.response = {
      status: response.status,
      data: data.detail || data
    }
    throw error
  }
  return data
}

// 认证接口
export async function register(phone, smsCode, password, confirmPassword, inviterId = null) {
  const body = { phone, sms_code: smsCode, password, confirm_password: confirmPassword }
  if (inviterId) {
    body.inviter_id = inviterId
  }
  const response = await fetch(`${AUTH_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.detail || '注册失败')
  }
  return data
}

export async function login(phone, password) {
  const response = await fetch(`${AUTH_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone, password })
  })
  const data = await response.json()
  if (!response.ok || !data.access_token) {
    throw new Error(data.detail || '登录失败')
  }
  return data
}

export async function sendSmsCode(phone, captchaToken) {
  const response = await fetch(`${AUTH_URL}/send-code`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone, captcha_token: captchaToken })
  })
  const data = await response.json()
  if (!data.success) {
    throw new Error(data.detail || '发送验证码失败')
  }
  return data
}

export async function getCurrentUser() {
  const response = await fetch(`${AUTH_URL}/me`, {
    headers: { ...getAuthHeaders() }
  })
  return handleResponse(response)
}

// 合同审查接口
export async function reviewContract(file, additionalInstructions) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('additional_instructions', additionalInstructions || '')

  const response = await fetch(`${BASE_URL}/review`, {
    method: 'POST',
    headers: { ...getAuthHeaders() },
    body: formData
  })

  return handleResponse(response)
}

// 确认重复文件审查接口（用户确认后继续处理）
export async function confirmDuplicateContract(file, additionalInstructions) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('additional_instructions', additionalInstructions || '')

  const response = await fetch(`${BASE_URL}/contract/review/confirm-duplicate`, {
    method: 'POST',
    headers: { ...getAuthHeaders() },
    body: formData
  })

  return handleResponse(response)
}

export async function batchReviewContracts(files, additionalInstructions) {
  const formData = new FormData()
  files.forEach(file => {
    formData.append('files', file)
  })
  formData.append('additional_instructions', additionalInstructions || '')

  const response = await fetch(`${BASE_URL}/batch/review`, {
    method: 'POST',
    headers: { ...getAuthHeaders() },
    body: formData
  })

  return handleResponse(response)
}

export async function getTaskStatus(taskId) {
  const response = await fetch(`${BASE_URL}/task/${taskId}`)
  return handleResponse(response)
}

export async function getAllTasks() {
  const response = await fetch(`${BASE_URL}/tasks`)
  return handleResponse(response)
}

export async function deleteTask(taskId) {
  const response = await fetch(`${BASE_URL}/task/${taskId}`, {
    method: 'DELETE'
  })
  return handleResponse(response)
}

// 记录管理接口
export async function getRecords() {
  const response = await fetch(`${BASE_URL}/records`, {
    headers: { ...getAuthHeaders() }
  })
  return handleResponse(response)
}

export async function getRecord(recordId) {
  const response = await fetch(`${BASE_URL}/records/${recordId}`, {
    headers: { ...getAuthHeaders() }
  })
  return handleResponse(response)
}

export async function deleteRecord(recordId) {
  const response = await fetch(`${BASE_URL}/records/${recordId}`, {
    method: 'DELETE',
    headers: { ...getAuthHeaders() }
  })
  return handleResponse(response)
}

export async function downloadRecordReport(recordId, format = 'md') {
  const response = await fetch(`${BASE_URL}/download/${recordId}?format=${format}`, {
    headers: { ...getAuthHeaders() }
  })
  
  if (response.status === 401) {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    window.location.href = '/login'
    throw new Error('登录已过期，请重新登录')
  }
  
  if (!response.ok) {
    const data = await response.json()
    throw new Error(data.detail?.message || data.detail || '下载失败')
  }
  
  return response.blob()
}

export async function healthCheck() {
  const response = await fetch(`${BASE_URL}/health`)
  return handleResponse(response)
}

// 用户额度接口
export async function getBonusCredits() {
  const response = await fetch(`${USER_URL}/credits`, {
    headers: { ...getAuthHeaders() }
  })
  return handleResponse(response)
}

// 用户反馈接口
export async function submitFeedback(data) {
  const response = await fetch(`${BASE_URL}/feedback`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify({
      report_id: String(data.reportId),  // 确保转换为字符串
      feedback_type: data.feedbackType,
      categories: data.categories,
      comment: data.comment,
      upload_consent: data.uploadConsent,
      contract_text: data.uploadConsent ? data.contractText : ''
    })
  })
  return handleResponse(response)
}
