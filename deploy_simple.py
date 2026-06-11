"""简单部署 - 长超时"""
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)
print('Connected!')

BASE = '/opt/sageai'

# 创建 .env.production
stdin, stdout, stderr = ssh.exec_command(
    f'test -s {BASE}/.env.production || cp {BASE}/backend/.env {BASE}/.env.production'
)
stdout.channel.recv_exit_status()

# 停止旧容器
print('Stopping old containers...')
stdin, stdout, stderr = ssh.exec_command(
    f'cd {BASE} && docker compose down --remove-orphans 2>&1 || docker-compose down --remove-orphans 2>&1 || true',
    timeout=60
)
stdout.channel.recv_exit_status()

# 清理
ssh.exec_command('docker container prune -f', timeout=30)

# 构建和启动 (一步完成)
print('Building and starting (this may take 5-10 minutes)...')
cmd = f'cd {BASE} && docker compose up -d --build 2>&1 || docker-compose up -d --build 2>&1'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=1800)  # 30 min timeout

# 等待完成
exit_code = stdout.channel.recv_exit_status()
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')

print(f'exit_code: {exit_code}')
print(f'output (last 3000 chars):\n{out[-3000:]}')
if err.strip():
    print(f'stderr:\n{err[-1000:]}')

# 等待
print('\nWaiting 20s for services...')
time.sleep(20)

# 检查
print('\n=== Status ===')
stdin, stdout, stderr = ssh.exec_command(
    f'cd {BASE} && (docker compose ps 2>&1 || docker-compose ps 2>&1)',
    timeout=30
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out)
if err.strip(): print(err[:500])

print('\n=== Health ===')
stdin, stdout, stderr = ssh.exec_command(
    'curl -s -w "\\nHTTP:%{http_code}" http://localhost:8000/health 2>&1',
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace')[:500])

# Logs
print('\n=== Logs ===')
stdin, stdout, stderr = ssh.exec_command(
    f'cd {BASE} && (docker compose logs --tail=30 backend 2>&1 || docker-compose logs --tail=30 backend 2>&1)',
    timeout=30
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out[-1500:])
if err.strip(): print(f'ERR: {err[:500]}')

ssh.close()
print('\nDone!')
