/** 押金裁判 API */
const API_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || ''
const BASE = API_BASE.startsWith('http') ? API_BASE.replace(/\/$/, '') : ''

function getAuthHeaders() {
  const token = localStorage.getItem('token')
  const headers = { 'Content-Type': 'application/json' }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

export async function adjudicateDeposit(facts) {
  const response = await fetch(`${BASE}/api/adjudicate/deposit`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(facts)
  })

  if (response.status === 401) {
    localStorage.removeItem('token')
    window.location.href = '/login'
    throw new Error('登录已过期')
  }

  const data = await response.json()
  if (!data.success) {
    throw new Error(data.result || '裁判请求失败')
  }
  return data
}
