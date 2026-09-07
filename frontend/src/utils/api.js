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

  // Vite/nginx may return an empty or non-JSON response when the upstream API
  // is unavailable.  Parsing it unconditionally hides the real failure behind
  // "Unexpected end of JSON input".  Read once and validate the payload so all
  // API callers receive an actionable error instead.
  const responseText = await response.text()
  let data = null
  if (responseText.trim()) {
    try {
      data = JSON.parse(responseText)
    } catch (error) {
      const message = response.ok
        ? '服务响应格式异常，请稍后重试'
        : `服务请求失败（HTTP ${response.status}）`
      throw new Error(message)
    }
  }

  if (!response.ok) {
    // 创建一个包含response信息的错误对象
    const error = new Error(data?.detail?.message || data?.detail || `服务请求失败（HTTP ${response.status}）`)
    error.response = {
      status: response.status,
      data: data?.detail || data
    }
    throw error
  }

  if (data === null && response.status !== 204) {
    throw new Error('服务返回空响应，请稍后重试')
  }
  return data
}

// 认证接口（注册已关闭，仅管理员可创建用户）
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

// review-v2 路由前缀（不在 /api 下，直接挂载在根路径）
const REVIEW_V2_BASE = isAbsoluteBase ? API_BASE.replace(/\/$/, '') : ''

// 合同审查第二版：清单式文件审查
export async function reviewContractV2File(file, contractType = 'house_lease', includeLowRisk = true, useLlm = true, profile = {}) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('contract_type', contractType)
  formData.append('include_low_risk', includeLowRisk ? 'true' : 'false')
  formData.append('use_llm', useLlm ? 'true' : 'false')
  formData.append('profile_json', JSON.stringify(profile))

  const response = await fetch(`${REVIEW_V2_BASE}/review-v2/file`, {
    method: 'POST',
    headers: { ...getAuthHeaders() },
    body: formData
  })

  const result = await handleResponse(response)
  if (import.meta.env.DEV) {
    // Request-local provenance, not a guessed build version or cached report.
    // No contract text or credentials are included in this diagnostic.
    console.info('[review-v2 runtime]', JSON.stringify({
      trace: result.production_path_trace,
      release_quality_gate: result.release_quality_gate,
      element_states: (result.items || []).map(item => ({
        rule: item.item_id,
        coverage: item.coverage_status,
        elements: (item.coverage_elements || []).map(element => ({
          id: element.element_id, status: element.status,
          prerequisite: element.prerequisite_status
        })),
        searched_absent_elements: (item.decision_trace?.element_absence_searches || [])
          .filter(search => search.result === 'NOT_FOUND').map(search => search.element_id)
      }))
    }))
  }
  return result
}

// 合同审查第二版：诉讼策略分析
export async function reviewV2LitigationAnalysis(contractText, contractType = 'house_lease', profile = {}) {
  const response = await fetch(`${REVIEW_V2_BASE}/review-v2/litigation-analysis`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify({
      contract_text: contractText,
      contract_type: contractType,
      include_low_risk: true,
      use_llm: true,
      profile: profile
    })
  })
  return handleResponse(response)
}

// 合同审查第二版：商业谈判分析
export async function reviewV2NegotiationAnalysis(contractText, contractType = 'house_lease', profile = {}) {
  const response = await fetch(`${REVIEW_V2_BASE}/review-v2/negotiation-analysis`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify({
      contract_text: contractText,
      contract_type: contractType,
      include_low_risk: true,
      use_llm: true,
      profile: profile
    })
  })
  return handleResponse(response)
}

// 合同审查第二版：跨地域裁判预判
export async function reviewV2JurisdictionPrediction(contractText, contractType = 'house_lease', profile = {}) {
  const response = await fetch(`${REVIEW_V2_BASE}/review-v2/jurisdiction-prediction`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify({
      contract_text: contractText,
      contract_type: contractType,
      include_low_risk: true,
      use_llm: true,
      profile: profile
    })
  })
  return handleResponse(response)
}

// 合同审查第二版：大模型语义复核状态
export async function getReviewV2LlmStatus() {
  const response = await fetch(`${REVIEW_V2_BASE}/review-v2/llm-status`, {
    method: 'GET',
    headers: { ...getAuthHeaders() }
  })

  return handleResponse(response)
}

async function exportReviewV2Report(report, format) {
  const response = await fetch(`${REVIEW_V2_BASE}/review-v2/export-${format}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify(report)
  })

  if (response.status === 401) {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    window.location.href = '/login'
    throw new Error('登录已过期，请重新登录')
  }

  if (!response.ok) {
    let message = `${format.toUpperCase()}导出失败`
    try {
      const data = await response.json()
      message = data.detail?.message || data.detail || message
    } catch (error) {
      // 非 JSON 错误响应时保留默认提示
    }
    throw new Error(message)
  }

  const blob = await response.blob()
  if (!blob || blob.size === 0) {
    throw new Error(`${format.toUpperCase()}导出结果为空`)
  }
  return blob
}

// 合同审查第二版：导出 PDF 报告
export async function exportReviewV2Pdf(report) {
  return exportReviewV2Report(report, 'pdf')
}

// 合同审查第二版：导出 Word 报告
export async function exportReviewV2Docx(report) {
  return exportReviewV2Report(report, 'docx')
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
