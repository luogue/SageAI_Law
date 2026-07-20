// 管理员 API 封装
// 后端 admin 路由在 /admin/... 下（独立于 /api/ 路径）
const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || ''
const ADMIN_BASE_URL = API_BASE.startsWith('http') ? API_BASE.replace(/\/$/, '') + '/admin' : '/admin'

// 获取管理员 token
function getAdminToken() {
  return localStorage.getItem('admin_token')
}

// 请求拦截器
async function adminRequest(url, options = {}) {
  const token = getAdminToken()
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }
  if (token) {
    headers['X-Admin-Token'] = token
  }

  const response = await fetch(`${ADMIN_BASE_URL}${url}`, {
    ...options,
    headers
  })

  if (response.status === 401) {
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_username')
    window.location.href = '/admin/login'
    throw new Error('登录已过期，请重新登录')
  }

  const data = await response.json()
  if (!response.ok || !data.success) {
    throw new Error(data.detail || '请求失败')
  }
  return data
}

// ========== 登录 ==========
export async function adminLogin(username, password) {
  const response = await fetch(`${ADMIN_BASE_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username, password })
  })
  return response.json()
}

// ========== 反馈管理 ==========
export async function getFeedbacks(params = {}) {
  const query = new URLSearchParams(params)
  return adminRequest(`/feedbacks?${query}`)
}

export async function getFeedbackDetail(id) {
  return adminRequest(`/feedbacks/${id}`)
}

export async function approveFeedback(id, bonusCredits = 3) {
  return adminRequest(`/feedbacks/${id}/approve?bonus_credits=${bonusCredits}`, {
    method: 'POST'
  })
}

export async function rejectFeedback(id, reason = '') {
  return adminRequest(`/feedbacks/${id}/reject?reason=${encodeURIComponent(reason)}`, {
    method: 'POST'
  })
}

export async function batchApproveFeedbacks(ids, bonusCredits = 3) {
  return adminRequest(`/feedbacks/batch-approve?bonus_credits=${bonusCredits}`, {
    method: 'POST',
    body: JSON.stringify({ feedback_ids: ids })
  })
}

// ========== 黑名单管理 ==========
export async function getBlacklist() {
  return adminRequest('/blacklist')
}

export async function addToBlacklist(type, value, reason = '', expiresAt = null) {
  const params = new URLSearchParams({ type, value, reason })
  if (expiresAt) params.append('expires_at', expiresAt)
  return adminRequest(`/blacklist?${params}`, { method: 'POST' })
}

export async function removeFromBlacklist(type, value) {
  return adminRequest(`/blacklist?type=${type}&value=${encodeURIComponent(value)}`, {
    method: 'DELETE'
  })
}

export async function getAutoBanStats(hours = 24) {
  return adminRequest(`/blacklist/auto-ban-stats?hours=${hours}`)
}

// ========== 数据统计 ==========
export async function getStatsOverview() {
  return adminRequest('/stats/overview')
}

export async function getStatsTrend(days = 7) {
  return adminRequest(`/stats/trend?days=${days}`)
}

export async function getCategoryStats() {
  return adminRequest('/stats/categories')
}

export async function getFrequentTriggers(days = 7, limit = 20) {
  return adminRequest(`/intercept-logs/frequent-triggers?days=${days}&limit=${limit}`)
}

// ========== 系统设置 ==========
export async function getSettings() {
  return adminRequest('/settings')
}

// ========== 白名单管理 ==========
export async function getWhitelist() {
  return adminRequest('/whitelist')
}

export async function addWhitelistWord(word) {
  return adminRequest(`/whitelist?word=${encodeURIComponent(word)}`, { method: 'POST' })
}

export async function removeWhitelistWord(word) {
  return adminRequest(`/whitelist/${encodeURIComponent(word)}`, { method: 'DELETE' })
}

// ========== 使用记录 ==========
export async function getUsageRecords(params = {}) {
  const query = new URLSearchParams()
  if (params.user_id) query.append('user_id', params.user_id)
  if (params.page) query.append('page', params.page)
  if (params.page_size) query.append('page_size', params.page_size)
  return adminRequest(`/usage?${query}`)
}

export async function getUsageUsers() {
  return adminRequest('/usage/users')
}

export async function getReportDetail(recordId) {
  return adminRequest(`/report/${recordId}`)
}

// ========== 用户管理 ==========
export async function getUsers(params = {}) {
  const query = new URLSearchParams()
  if (params.page) query.append('page', params.page)
  if (params.size) query.append('size', params.size)
  if (params.mobile) query.append('mobile', params.mobile)
  if (params.status) query.append('status', params.status)
  return adminRequest(`/users?${query}`)
}

export async function getUserDetail(userId) {
  return adminRequest(`/users/${userId}`)
}

export async function banUser(userId, reason = '') {
  return adminRequest(`/users/${userId}/ban?reason=${encodeURIComponent(reason)}`, {
    method: 'POST'
  })
}

export async function unbanUser(userId, reason = '') {
  return adminRequest(`/users/${userId}/unban?reason=${encodeURIComponent(reason)}`, {
    method: 'POST'
  })
}

// 创建用户
export async function createUser({ mobile, password, countryCode = '+86', bonusCredits = 3 }) {
  const params = new URLSearchParams({ mobile, password, country_code: countryCode, bonus_credits: bonusCredits })
  return adminRequest(`/users/create?${params}`, { method: 'POST' })
}

// 审核通过用户
export async function approveUser(userId) {
  return adminRequest(`/users/${userId}/approve`, { method: 'POST' })
}

export async function addUserCredits(userId, amount, reason = '') {
  const params = new URLSearchParams({ amount })
  if (reason) params.append('reason', reason)
  return adminRequest(`/users/${userId}/add-credits?${params}`, {
    method: 'POST'
  })
}

export async function reduceUserCredits(userId, amount, reason = '') {
  const params = new URLSearchParams({ amount })
  if (reason) params.append('reason', reason)
  return adminRequest(`/users/${userId}/reduce-credits?${params}`, {
    method: 'POST'
  })
}

export async function getUserRecords(userId, params = {}) {
  const query = new URLSearchParams()
  if (params.page) query.append('page', params.page)
  if (params.size) query.append('size', params.size)
  return adminRequest(`/users/${userId}/records?${query}`)
}

export async function getFinalReport(userId, recordId) {
  return adminRequest(`/users/${userId}/records/${recordId}/final-report`)
}

export async function getRawReport(userId, recordId) {
  return adminRequest(`/users/${userId}/records/${recordId}/raw-report`)
}
