// Static deployment regression only: no Docker, network, application or database access.
import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

const read = path => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8')
const dockerfile = read('Dockerfile.frontend').replace(/\\\r?\n\s*/g, ' ')
const compose = read('docker-compose.yml')
const nginx = read('nginx.conf').replace(/#.*$/gm, '')
const dockerHealth = dockerfile.match(/^HEALTHCHECK\s+(.+)$/gm) ?? []
const frontend = compose.match(/^  frontend:\s*\r?\n([\s\S]*?)(?=^  [\w-]+:|^\S|(?![\s\S]))/m)?.[1] ?? ''

function validateProbe(command) {
  // Require a real HTTP request; no shell wrapper or unconditional success command.
  assert.equal(command[0], 'wget')
  assert.ok(command.includes('--spider'))
  assert.ok(command.includes('--tries=1'))
  const urls = command.filter(token => /^https?:/.test(token))
  assert.equal(urls.length, 1)
  const url = new URL(urls[0])
  assert.equal(url.protocol, 'http:')
  assert.equal(url.hostname, '127.0.0.1')
  assert.equal(url.port || '80', '80')
  assert.equal(url.pathname, '/')
  assert.equal(url.search + url.hash + url.username + url.password, '')
  for (const token of command.slice(1)) {
    assert.ok(['--no-verbose', '--tries=1', '--spider', urls[0]].includes(token), token)
  }
}

function dockerCommand() {
  assert.equal(dockerHealth.length, 1, 'Keep exactly one active HTTP healthcheck')
  // Only permit failure propagation after wget, never "|| true" or "exit 0".
  const cmd = dockerHealth[0].match(/\bCMD\s+(.+?)\s+\|\|\s+exit\s+1\s*$/)?.[1]
  assert.ok(cmd, 'HTTP failure must return a nonzero exit code')
  return cmd.trim().split(/\s+/)
}

function composeCommand() {
  assert.match(frontend, /^    healthcheck:\s*$/m)
  assert.doesNotMatch(frontend, /^\s+disable:\s*true\s*$/m)
  const line = frontend.match(/^      test:\s*(\[.*\])\s*$/m)?.[1]
  assert.ok(line, 'Keep the Compose exec-form HTTP probe')
  const [mode, ...command] = JSON.parse(line)
  assert.equal(mode, 'CMD')
  return command
}

test('Dockerfile HTTP probe uses IPv4 and preserves failure exit', () => {
  validateProbe(dockerCommand())
})

test('Compose HTTP probe agrees with the image healthcheck', () => {
  validateProbe(composeCommand())
  assert.deepEqual(composeCommand(), dockerCommand())
})

test('probe port and page match the shipped Nginx configuration and assets', () => {
  assert.match(dockerfile, /^COPY nginx\.conf \/etc\/nginx\/conf\.d\/default\.conf\s*$/m)
  assert.match(dockerfile, /^COPY --from=builder \/app\/dist \/usr\/share\/nginx\/html\s*$/m)
  assert.match(nginx, /\blisten\s+(?:(?:0\.0\.0\.0|127\.0\.0\.1):)?80\s*;/)
  assert.match(nginx, /location\s+\/\s*\{\s*root\s+\/usr\/share\/nginx\/html\s*;\s*index\s+index\.html\s*;/)
})

test('regression guard rejects ambiguous/IPv6 addresses and wrong ports or paths', () => {
  for (const url of ['http://localhost:80/', 'http://[::1]:80/', 'http://127.0.0.1:8000/', 'http://127.0.0.1/missing']) {
    assert.throws(() => validateProbe(['wget', '--spider', '--tries=1', url]))
  }
})

test('regression guard rejects unconditional success and masked HTTP failure', () => {
  assert.throws(() => validateProbe(['true']))
  assert.throws(() => validateProbe([...dockerCommand(), '||', 'true']))
})
