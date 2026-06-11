"""
SageAI 最终部署脚本
使用方法: python deploy_final.py
构建需要 5-10 分钟，请耐心等待
"""
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)
print('Connected!')

BASE = '/opt/sageai'

# 1. 确保 .env.production 存在
stdin, stdout, stderr = ssh.exec_command(
    f'test -s {BASE}/.env.production || cp {BASE}/backend/.env {BASE}/.env.production; echo DONE',
    timeout=10
)
print(f'.env.production: {stdout.read().decode().strip()}')

# 2. 停止旧容器
print('Stopping old containers...')
stdin, stdout, stderr = ssh.exec_command(
    f'cd {BASE} && docker-compose down --remove-orphans 2>&1 || echo "no containers"',
    timeout=60
)
out = stdout.read().decode('utf-8', errors='replace')
print(out.strip())

# 3. 清理
ssh.exec_command('docker container prune -f', timeout=30)

# 4. 构建并启动 (后台运行)
print('\nStarting build and deploy (this takes 5-10 minutes)...')
print('Build output will be saved to /tmp/sageai-deploy.log')
print('You can monitor with: tail -f /tmp/sageai-deploy.log')
print()

# 使用非阻塞方式启动
transport = ssh.get_transport()
channel = transport.open_session()
channel.setblocking(0)
channel.exec_command(
    f'cd {BASE} && '
    f'docker-compose up -d --build > /tmp/sageai-deploy.log 2>&1'
)
time.sleep(5)

# 5. 轮询检查 (每30秒)
max_wait = 600  # 最多等10分钟
elapsed = 0
while elapsed < max_wait:
    time.sleep(30)
    elapsed += 30

    # 检查容器状态
    chk_chan = transport.open_session()
    chk_chan.exec_command(
        'docker ps --filter name=sageai --format "{{.Names}}\t{{.Status}}" 2>&1'
    )
    time.sleep(2)
    containers = chk_chan.recv(4096).decode('utf-8', errors='replace').strip()

    if containers:
        # 检查健康状态
        hc_chan = transport.open_session()
        hc_chan.exec_command('curl -s -w "\\nHTTP:%{http_code}" http://localhost:8000/health 2>&1')
        time.sleep(3)
        health = hc_chan.recv(4096).decode('utf-8', errors='replace').strip()
        
        if 'HTTP:200' in health:
            print(f'\n[OK] Deploy SUCCESS after {elapsed}s!')
            print(f'Containers:\n{containers}')
            print(f'Health: {health}')
            print(f'Web: http://120.77.171.21')
            print(f'API: http://120.77.171.21:8000')
            ssh.close()
            exit(0)
        else:
            print(f'[{elapsed}s] Containers found but not healthy: {health[:100]}')
    else:
        # 检查构建日志中的错误
        log_chan = transport.open_session()
        log_chan.exec_command('tail -5 /tmp/sageai-deploy.log 2>/dev/null | grep -i error || echo "building..."')
        time.sleep(2)
        log = log_chan.recv(4096).decode('utf-8', errors='replace').strip()
        print(f'[{elapsed}s] Waiting... {log[:150]}')

# 超时
print(f'\n[WARN] Deploy timed out after {max_wait}s')
print('\nFinal status:')

# 打印日志最后30行
chk_chan = transport.open_session()
chk_chan.exec_command('tail -30 /tmp/sageai-deploy.log 2>/dev/null')
time.sleep(2)
print(chk_chan.recv(8192).decode('utf-8', errors='replace'))

# 检查当前容器
chk_chan2 = transport.open_session()
chk_chan2.exec_command('docker ps -a --filter name=sageai --format "table {{.Names}}\t{{.Status}}"')
time.sleep(2)
print(chk_chan2.recv(8192).decode('utf-8', errors='replace'))

ssh.close()
print('\nPlease check the server manually:')
print('  ssh root@120.77.171.21')
print('  cd /opt/sageai')
print('  cat /tmp/sageai-deploy.log')
print('  docker-compose ps')
