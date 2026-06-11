"""清理重复构建进程，重新部署"""
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)
print('Connected!')

BASE = '/opt/sageai'

# 杀掉所有旧的构建进程
print('Killing old build processes...')
ssh.exec_command('pkill -f "docker build" 2>/dev/null; echo done', timeout=10)
ssh.exec_command('pkill -f "docker-compose up" 2>/dev/null; echo done', timeout=10)
time.sleep(3)

# 确认清理完成
stdin, stdout, stderr = ssh.exec_command(
    'ps aux | grep -E "docker build|docker-compose up" | grep -v grep | wc -l',
    timeout=10
)
count = stdout.read().decode('utf-8', errors='replace').strip()
print(f'Remaining build processes: {count}')

# 确保 .env.production 存在且有内容
stdin, stdout, stderr = ssh.exec_command(
    f'if [ ! -s {BASE}/.env.production ]; then cp {BASE}/backend/.env {BASE}/.env.production; echo CREATED; else echo EXISTS; fi',
    timeout=10
)
print(f'.env.production: {stdout.read().decode().strip()}')

# 停止旧容器
print('\nStopping old containers...')
stdin, stdout, stderr = ssh.exec_command(f'cd {BASE} && docker-compose down 2>&1', timeout=120)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out.strip() or 'OK')
if err.strip(): print(f'ERR: {err[:200]}')

# 清理
ssh.exec_command('docker container prune -f', timeout=30)
ssh.exec_command('docker image prune -f', timeout=30)

# 重新构建 - 这次只用 docker-compose build，不用 --no-cache（利用缓存加速）
print('\nBuilding images...')
cmd = f'cd {BASE} && docker-compose build 2>&1'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=1200)  # 20 min

exit_code = stdout.channel.recv_exit_status()
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')

print(f'Build exit: {exit_code}')
print(f'Output (last 2000):\n{out[-2000:]}')
if err.strip():
    print(f'Stderr:\n{err[-500:]}')

if exit_code != 0:
    print('\nBuild failed!')
    ssh.close()
    exit(1)

# 启动
print('\nStarting services...')
stdin, stdout, stderr = ssh.exec_command(f'cd {BASE} && docker-compose up -d 2>&1', timeout=120)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out.strip() or 'OK')
if err.strip(): print(f'ERR: {err[:200]}')

# 等待
print('\nWaiting 15 seconds...')
time.sleep(15)

# 检查
print('\n=== Status ===')
stdin, stdout, stderr = ssh.exec_command(f'cd {BASE} && docker-compose ps 2>&1', timeout=10)
print(stdout.read().decode())

print('=== Health ===')
stdin, stdout, stderr = ssh.exec_command(
    'curl -s -w "\\nHTTP:%{http_code}" http://localhost:8000/health 2>&1',
    timeout=10
)
out = stdout.read().decode('utf-8', errors='replace')
print(out.strip()[:500])

# 如果失败，打印日志
if 'HTTP:200' not in out:
    print('\n=== Backend Logs ===')
    stdin, stdout, stderr = ssh.exec_command(f'cd {BASE} && docker-compose logs backend 2>&1', timeout=30)
    out = stdout.read().decode('utf-8', errors='replace')
    print(out[-1500:])

ssh.close()
print('\nDone!')
