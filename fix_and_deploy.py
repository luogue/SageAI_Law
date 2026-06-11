"""修复并部署"""
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)

# 检查 .env.production
print("=== 检查环境文件 ===")
for f in ['.env.production', '.env', 'backend/.env']:
    stdin, stdout, stderr = ssh.exec_command(f'ls -la /opt/sageai/{f} 2>&1')
    print(f'{f}: {stdout.read().decode().strip()}')

# 如果没有 .env.production，从 backend/.env 复制
stdin, stdout, stderr = ssh.exec_command('test -f /opt/sageai/.env.production && echo EXISTS || echo MISSING')
result = stdout.read().decode().strip()
print(f'.env.production: {result}')

if result == 'MISSING':
    print('创建 .env.production...')
    stdin, stdout, stderr = ssh.exec_command('cp /opt/sageai/backend/.env /opt/sageai/.env.production')
    stdout.channel.recv_exit_status()
    print('已创建')

# 重启容器
print('\n=== 重启 Docker 容器 ===')
cmds = [
    'cd /opt/sageai',
    'docker-compose down --remove-orphans 2>&1',
    'docker-compose build --no-cache 2>&1',
    'docker-compose up -d 2>&1',
]

for cmd in cmds:
    print(f'\n>> {cmd}')
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=600)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    print(f'  exit={exit_code}')
    if out.strip():
        # 打印最后10行
        lines = out.strip().split('\n')
        for line in lines[-10:]:
            print(f'    {line[:150]}')
    if err.strip() and exit_code != 0:
        print(f'  ERR: {err[:500]}')

# 等待启动
print('\n等待服务启动 (15秒)...')
time.sleep(15)

# 检查
print('\n=== 容器状态 ===')
stdin, stdout, stderr = ssh.exec_command('docker ps --filter name=sageai --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"')
print(stdout.read().decode())

print('\n=== 健康检查 ===')
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:8000/health 2>&1')
print(stdout.read().decode())

# 如果没有运行，查看日志
stdin, stdout, stderr = ssh.exec_command('docker ps --filter name=sageai --format "{{.Names}}"')
containers = stdout.read().decode().strip()
if not containers:
    print('\n=== 容器未运行，查看构建日志 ===')
    stdin, stdout, stderr = ssh.exec_command('docker-compose logs --tail=50 2>&1')
    print(stdout.read().decode())
    print(stderr.read().decode())

ssh.close()
