export function factFailure(error) {
  const body = error?.diagnosticsPayload || error?.response?.data || error?.detail
  const detail = body?.detail || body
  return detail?.code === 'FACT_EXTRACTION_BLOCKED' && Array.isArray(detail.diagnostics) ? detail : null
}
export function diagnosticKey(user, path) {
  return `review-fact-failures:v1:${user || 'local'}:${path}`
}
export function readFailures(storage, key) {
  try { const value = JSON.parse(storage.getItem(key) || '[]'); return Array.isArray(value) ? value : [] } catch { return [] }
}
export function saveFailure(storage, key, failure, filename) {
  // Retain diagnostics, not entire model prompts/repair responses, so failure
  // history does not exhaust browser storage after a few full-contract runs.
  const { attempts, ...diagnostic } = failure
  const rows = [{ ...diagnostic, filename, saved_at: new Date().toISOString() }, ...readFailures(storage,key)]
  storage.setItem(key,JSON.stringify(rows))
  return rows
}
export function createDiagnosticSession(storage, key) {
  let selected = null
  try { selected = JSON.parse(storage.getItem(`${key}:current`) || 'null') } catch {}
  return {
    current: selected, expanded: false, generation: 0,
    remember() { try { storage.setItem(`${key}:current`, JSON.stringify(this.current)) } catch {} },
    reset() { this.generation++; this.current = null; this.expanded = false; this.remember(); return this.generation },
    show(failure, generation = this.generation, autoExpand = false) {
      if (generation !== this.generation) return false
      this.current = failure; this.expanded = autoExpand; this.remember(); return true
    },
    restore(failure) { this.reset(); this.show(failure) },
    toggle() { this.expanded = !this.expanded }
  }
}
const beijingFormatter = new Intl.DateTimeFormat('zh-CN', {
  timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit',
  hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23'
})
export function formatDiagnosticTime(value) {
  if (!value) return '时间未提供'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '时间格式无效'
  return `${beijingFormatter.format(date)}（北京时间）`
}
