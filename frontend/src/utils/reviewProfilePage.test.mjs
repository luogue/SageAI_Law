import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { pathToFileURL } from 'node:url'
import { createRenderer, nextTick } from 'vue'
import { parse, compileScript } from '@vue/compiler-sfc'

const require = createRequire(import.meta.url)
const storage = new Map()
globalThis.localStorage = { getItem: k => storage.get(k) ?? null, setItem: (k,v) => storage.set(k,v), removeItem: k => storage.delete(k) }
globalThis.window = { location: { pathname: '/contract-review-v2' } }
const session = new Map()
globalThis.sessionStorage = { getItem: k => session.get(k) ?? null, setItem: (k,v) => session.set(k,v) }
const source = readFileSync(new URL('../views/ContractReviewV2.vue', import.meta.url), 'utf8')
const options = {
  house_lease: { identities: ['承租人', '出租人'], scenarios: ['居住用途'] },
  work_contract: { identities: ['定作方', '承揽方'], scenarios: ['承揽加工'] },
  transportation: { identities: ['托运人', '承运人'], scenarios: ['货物运输'] }
}
let finishRequest
let sent
globalThis.__reviewPageApi = {
  getReviewV2LlmStatus: async () => ({ available: false }),
  getReviewV2ProfileOptions: async () => options,
  reviewContractV2File: (...args) => { sent = args; return new Promise(resolve => { finishRequest = resolve }) },
  exportReviewV2Docx: () => {}, exportReviewV2Pdf: () => {}
}
let code = compileScript(parse(source).descriptor, { id: 'profile-page-test' }).content
code = code.replace(/from 'vue'/g, `from ${JSON.stringify(pathToFileURL(require.resolve('vue').replace(/index\.js$/, 'index.mjs')).href)}`)
  .replace(/import \{ ElMessage \} from 'element-plus'/, 'const ElMessage = { success() {}, error() {}, warning() {} }')
  .replace(/import \{ (.+) \} from '@element-plus\/icons-vue'/, 'const { $1 } = {}')
  .replace(/import \{ (.+) \} from '\.\.\/utils\/api'/, 'const { $1 } = globalThis.__reviewPageApi')
  .replace(/from '\.\.\/utils\/reviewProfile.mjs'/, `from ${JSON.stringify(new URL('./reviewProfile.mjs', import.meta.url).href)}`)
  .replace(/from '\.\.\/utils\/factDiagnostics.mjs'/, `from ${JSON.stringify(new URL('./factDiagnostics.mjs', import.meta.url).href)}`)
const { default: Page } = await import(`data:text/javascript;base64,${Buffer.from(code).toString('base64')}`)

// Mount the real SFC setup with Vue's renderer and mocked network/UI chrome.
// No copied request handler: these tests execute runReview/setFile/resetAll.
const renderer = createRenderer({
  createElement: () => ({}), createText: () => ({}), createComment: () => ({}),
  insert() {}, remove() {}, setText() {}, setElementText() {}, patchProp() {},
  parentNode: () => null, nextSibling: () => null
})
async function mount(retainSelection = false) {
  if (!retainSelection) session.clear()
  const app = renderer.createApp({ ...Page, render: () => null })
  const vm = app.mount({})
  await new Promise(resolve => setImmediate(resolve))
  return { app, state: vm.$.setupState }
}
const file = { name: 'contract.docx', size: 100 }

test('report classification stays separate from selected type and request profile', async () => {
  const { app, state: s } = await mount()
  s.setFile(file)
  s.riskAppetite = '激进'
  const running = s.runReview()
  await new Promise(resolve => setImmediate(resolve))
  assert.equal(sent[4].risk_appetite, '激进')
  finishRequest({ contract_type: 'transportation', profile: { user_identity: '承运人', contract_scenario: '货物运输' }, items: [] })
  await running
  await nextTick()
  assert.equal(s.contractType, 'house_lease')
  assert.equal(s.userIdentity, '承租人')
  assert.equal(s.contractScenario, '居住用途')
  assert.equal(s.report.contract_type, 'transportation')
  assert.equal(s.riskAppetite, '激进')
  assert.ok(s.report)
  assert.equal(s.buildProfile().review_role, '承租人')
  app.unmount()
})

test('two confidentiality submissions retain the manual selection despite sale responses', async () => {
  const { app, state: s } = await mount()
  s.contractType = 'confidentiality'
  s.setFile(file)
  for (let i = 0; i < 2; i++) {
    const running = s.runReview()
    await new Promise(resolve => setImmediate(resolve))
    assert.equal(sent[1], 'confidentiality')
    assert.equal(sent[4].contract_type, 'confidentiality')
    finishRequest({ contract_type: 'sale', profile: { user_identity: '买方', contract_scenario: '商品买卖' }, items: [] })
    await running
    await nextTick()
    assert.equal(s.contractType, 'confidentiality')
    assert.equal(s.report.contract_type, 'sale')
    assert.notEqual(s.userIdentity, '买方')
  }
  app.unmount()
})

test('historical sale failure and new review reset cannot overwrite the selected type', async () => {
  const { app, state: s } = await mount()
  s.contractType = 'confidentiality'
  s.restoreFailure({ contract_type: 'sale', filename: 'history.docx', task_id: 'old', diagnostics: [] })
  assert.equal(s.contractType, 'confidentiality')
  s.resetAll()
  s.setFile(file)
  assert.equal(s.contractType, 'confidentiality')
  assert.equal(s.buildProfile().contract_type, 'confidentiality')
  app.unmount()
  const restored = await mount(true)
  assert.equal(restored.state.contractType, 'confidentiality')
  assert.equal(restored.state.buildProfile().contract_type, 'confidentiality')
  restored.app.unmount()
})

test('successive manual types remain independent from previous report types', async () => {
  const { app, state: s } = await mount()
  let previous = 'house_lease'
  for (const type of ['labor', 'non_compete', 'confidentiality', 'sale']) {
    s.contractType = type
    s.setFile(file)
    const running = s.runReview()
    await new Promise(resolve => setImmediate(resolve))
    assert.equal(sent[1], type)
    finishRequest({ contract_type: previous, items: [] })
    await running
    await nextTick()
    assert.equal(s.contractType, type)
    previous = type
  }
  app.unmount()
})

for (const change of ['type', 'file', 'preference', 'clear']) {
  test(`late lease response cannot overwrite ${change} change`, async () => {
    const { app, state: s } = await mount()
    s.setFile(file)
    const running = s.runReview()
    await new Promise(resolve => setImmediate(resolve))
    if (change === 'type') s.contractType = 'work_contract'
    if (change === 'file') s.setFile({ name: 'next.docx', size: 200 })
    if (change === 'preference') s.riskAppetite = '激进'
    if (change === 'clear') s.resetAll()
    finishRequest({ contract_type: 'house_lease', profile: { user_identity: '出租人', contract_scenario: '居住用途' }, items: [] })
    await running
    await nextTick()
    assert.equal(s.report, null)
    assert.notEqual(s.userIdentity, '出租人')
    assert.equal(s.loading, false)
    if (change === 'type') assert.equal(s.userIdentity, '定作方')
    if (change === 'preference') assert.equal(s.riskAppetite, '激进')
    app.unmount()
  })
}
