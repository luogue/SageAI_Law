import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'

// Load the actual browser API module without changing its implementation.
const source = await readFile(new URL('../src/utils/api.js', import.meta.url), 'utf8')
const api = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`)
globalThis.localStorage = { getItem: () => null }
const binding = { review_run_id:'run-current', report_version:'report-current', gate_version:'gate-current', snapshot_hash:'hash-current' }
const headers = { 'X-Review-Run-Id':binding.review_run_id, 'X-Report-Version':binding.report_version,
  'X-Gate-Version':binding.gate_version, 'X-Snapshot-Hash':binding.snapshot_hash }

test('download accepts only the exact current server snapshot', async t => {
  t.mock.method(globalThis, 'fetch', async (url, options) => {
    assert.equal(JSON.parse(options.body).final_review_snapshot.review_run_id, binding.review_run_id)
    return new Response('current document', { headers })
  })
  const blob = await api.exportReviewV2Docx({ final_review_snapshot:binding })
  assert.equal(await blob.text(), 'current document')
})

for (const field of Object.keys(headers)) {
  test(`download rejects a stale ${field}`, async t => {
    t.mock.method(globalThis, 'fetch', async () => new Response('old document', { headers:{ ...headers, [field]:'old' } }))
    await assert.rejects(api.exportReviewV2Pdf({ final_review_snapshot:binding }), /EXPORT_BLOCKED_STALE_REPORT/)
  })
}

test('unversioned response cannot be downloaded', async t => {
  t.mock.method(globalThis, 'fetch', async () => new Response('old document'))
  await assert.rejects(api.exportReviewV2Docx({ final_review_snapshot:binding }), /EXPORT_BLOCKED_STALE_REPORT/)
})

test('server stale rejection is preserved', async t => {
  t.mock.method(globalThis, 'fetch', async () => new Response(JSON.stringify({ detail:{ code:'EXPORT_BLOCKED_STALE_REPORT',message:'最新审查未通过质量门，禁止导出或回退旧报告。' } }), { status:409 }))
  await assert.rejects(api.exportReviewV2Docx({ final_review_snapshot:binding }), /禁止导出或回退旧报告/)
})
