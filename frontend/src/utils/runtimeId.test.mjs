import assert from 'node:assert/strict'
import test from 'node:test'

import { createRuntimeId } from './runtimeId.mjs'

const UUID_V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/

test('uses native randomUUID when available', () => {
  const expected = '11111111-1111-4111-8111-111111111111'
  assert.equal(createRuntimeId({ randomUUID: () => expected }), expected)
})

test('creates a UUID when randomUUID is unavailable', () => {
  const cryptoApi = {
    getRandomValues(bytes) {
      bytes.fill(7)
      return bytes
    }
  }
  assert.match(createRuntimeId(cryptoApi), UUID_V4)
})

test('works when the Web Crypto API is unavailable', () => {
  assert.match(createRuntimeId(undefined), UUID_V4)
})
