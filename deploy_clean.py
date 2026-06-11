"""最终清理并重新部署"""
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)
print('Connected!')

BASE = '/opt/sageai'

# 1. 彻底清理
print('=== 清理 ===')
ssh.exec_command('pkill -9 -f "docker-compose" 2>/dev/null; echo done', timeout=10)
ssh.exec_command('pkill -9 -f "docker build" 2>/dev/null; echo done', timeout=10)
time.sleep(3)
ssh.exec_command('docker container prune -f', timeout=30)

# 确认清理
stdin, stdout, stderr = ssh.exec_command(
    'ps aux | grep -E "docker-compose|docker build" | grep -v grep | wc -l',
    timeout=10
)
print(f'Remaining processes: {stdout.read().decode().strip()}')

# 2. 检查 Dockerfile 和之前的构建缓存
print('\n=== Docker info ===')
stdin, stdout, stderr = ssh.exec_command(f'cd {BASE} && docker images | grep sageai', timeout=10)
print(stdout.read().decode())

# 3. 确保 .env.production
ssh.exec_command(f'test -s {BASE}/.env.production || cp {BASE}/backend/.env {BASE}/.env.production', timeout=10)

# 4. 检查构建日志详细错误
print('\n=== Previous build error ===')
stdin, stdout, stderr = ssh.exec_command(
    'grep -i "error\|failed\|ERROR\|FAIL" /tmp/sageai-deploy.log 2>/dev/null | tail -20',
    timeout=10
)
print(stdout.read().decode() or 'No errors found')

# 5. 尝试构建 (单次, 不使用 no-cache)
print('\n=== Building backend ===')
stdin, stdout, stderr = ssh.exec_command(
    f'cd {BASE} && docker build -f Dockerfile.backend -t sageai-backend . 2>&1 | tail -50',
    timeout=600
)
exit_code = stdout.channel.recv_exit_status()
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(f'Exit: {exit_code}')
print(out[-2000:])
if err.strip():
    print(f'ERR: {err[-500:]}')

if exit_code != 0:
    print('\n后端构建失败! 尝试诊断...')
    # 测试 apt-get
    stdin, stdout, stderr = ssh.exec_command(
        'docker run --rm python:3.11-slim apt-get update 2>&1 | tail -5',
        timeout=120
    )
    print(f'apt test: {stdout.read().decode()}')

ssh.close()
print('\nDone')
