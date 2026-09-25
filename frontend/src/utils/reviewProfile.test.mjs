import test from 'node:test'
import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { ref } from 'vue'
import { useReviewProfile } from './reviewProfile.mjs'

// Exercise the UI against the actual server catalog, not a duplicated fixture.
const root = fileURLToPath(new URL('../../../', import.meta.url))
const catalog = JSON.parse(execFileSync('python', ['-c',
  'import json; from review_v2.profile_catalog import profile_catalog; print(json.dumps(profile_catalog(), ensure_ascii=False))'],
{ cwd: root, env: { ...process.env, PYTHONPATH: 'backend', PYTHONIOENCODING: 'utf-8' }, encoding: 'utf8' }))

function setup() {
  const type = ref('house_lease')
  return { type, ...useReviewProfile(type, ref(catalog)) }
}

for (const type of ['work_contract', 'transportation', 'investment', 'shareholders', 'labor', 'equity_transfer', 'sale']) {
  test(`lease -> ${type}: refresh context, preserve preferences, submit displayed values`, () => {
    const p = setup()
    p.userIdentity.value = '出租人'
    p.contractScenario.value = '投资/转租'
    p.riskAppetite.value = '激进'
    p.bargainingPosition.value = '弱势方'
    p.type.value = type
    assert.equal(p.userIdentity.value, catalog[type].identities[0])
    assert.equal(p.contractScenario.value, catalog[type].scenarios[0])
    assert.equal(p.riskAppetite.value, '激进')
    assert.equal(p.bargainingPosition.value, '弱势方')
    for (const preset of ['conservative', 'standard', 'aggressive']) {
      p.setProfilePreset(preset)
      assert.equal(p.userIdentity.value, catalog[type].identities[0])
      assert.equal(p.contractScenario.value, catalog[type].scenarios[0])
    }
    const submitted = p.buildProfile()
    assert.equal(submitted.review_role, p.userIdentity.value)
    assert.equal(submitted.user_identity, p.userIdentity.value)
    assert.equal(submitted.contract_scenario, p.contractScenario.value)
    assert.equal(submitted.contract_type, type)
    assert.doesNotMatch(JSON.stringify([submitted, p.identityOptions.value, p.scenarioOptions.value]), /个人租客|居住用途|投资\/转租/)
  })
}

test('lease offers both parties and residential usage; presets retain selected landlord', () => {
  const p = setup()
  assert.ok(p.identityOptions.value.includes('承租人'))
  assert.ok(p.identityOptions.value.includes('出租人'))
  assert.ok(p.scenarioOptions.value.includes('居住用途'))
  p.userIdentity.value = '出租人'
  p.setProfilePreset('conservative')
  assert.equal(p.userIdentity.value, '出租人')
})

test('request profile exposes no result-to-form reclassification operation', () => {
  const p = setup()
  p.riskAppetite.value = '保守'
  assert.equal(p.applyReviewProfile, undefined)
  assert.equal(p.type.value, 'house_lease')
  assert.equal(p.riskAppetite.value, '保守')
  p.type.value = 'investment'
  assert.ok(!p.scenarioOptions.value.includes('危险品公路运输'))
  assert.equal(p.userIdentity.value, '投资方')
})

test('new file/reset clears contextual choices even for same type, retains preference', () => {
  const p = setup()
  p.userIdentity.value = '出租人'
  p.contractScenario.value = '商业经营'
  p.riskAppetite.value = '激进'
  p.resetContext()
  assert.equal(p.userIdentity.value, '承租人')
  assert.equal(p.contractScenario.value, '居住用途')
  assert.equal(p.riskAppetite.value, '激进')
})

test('unknown contracts stay neutral', () => {
  const p = setup()
  p.type.value = 'unknown'
  assert.equal(p.userIdentity.value, '合同当事人')
  assert.equal(p.contractScenario.value, '一般合同')
})
