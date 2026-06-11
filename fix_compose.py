"""修复 docker-compose 兼容性问题并部署"""
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)
print('Connected!')

BASE = '/opt/sageai'

# 方法1: 升级 docker-compose
print('=== 修复 docker-compose ===')
cmd = 'pip install --upgrade docker-compose 2>&1'
print(f'Running: {cmd}')
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
exit_code = stdout.channel.recv_exit_status()
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(f'exit={exit_code}')
print(out[-500:])
if err.strip(): print(f'ERR: {err[:300]}')

# 方法2: 升级 docker Python 包
print('\n=== 升级 docker Python 包 ===')
cmd = 'pip install --upgrade docker 2>&1'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
exit_code = stdout.channel.recv_exit_status()
out = stdout.read().decode('utf-8', errors='replace')
print(out[-300:])

# 测试 docker-compose 是否修复
print('\n=== 测试 docker-compose ===')
stdin, stdout, stderr = ssh.exec_command(f'cd {BASE} && docker-compose version 2>&1', timeout=10)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(f'version: {out.strip()}')
if err.strip(): print(f'err: {err[:200]}')

# 如果还是不行，尝试直接修复源码
stdin, stdout, stderr = ssh.exec_command(f'cd {BASE} && docker-compose ps 2>&1', timeout=10)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')

if 'ssl_version' in err:
    print('\n=== 直接修复 Python 源码 ===')
    # 找到并修复 docker_client.py
    cmd = "python3 -c \"import compose.cli.docker_client; print(compose.cli.docker_client.__file__)\" 2>&1"
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    filepath = stdout.read().decode('utf-8', errors='replace').strip()
    print(f'File: {filepath}')
    
    if filepath:
        # 修复: 移除 ssl_version 参数
        fix_cmd = (
            f"sed -i 's/kwargs = kwargs_from_env(environment=environment, ssl_version=tls_version)/"
            f"kwargs = kwargs_from_env(environment=environment)/' {filepath}"
        )
        print(f'Fixing: {fix_cmd[:120]}...')
        stdin, stdout, stderr = ssh.exec_command(fix_cmd, timeout=10)
        stdout.channel.recv_exit_status()

    # 再次测试
    stdin, stdout, stderr = ssh.exec_command(f'cd {BASE} && docker-compose ps 2>&1', timeout=10)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    print(f'After fix: {out.strip()}')
    if err.strip(): print(f'err: {err[:300]}')

# 创建 .env.production
ssh.exec_command(f'test -s {BASE}/.env.production || cp {BASE}/backend/.env {BASE}/.env.production', timeout=10)

# 部署
print('\n=== 停止旧容器 ===')
stdin, stdout, stderr = ssh.exec_command(f'cd {BASE} && docker-compose down --remove-orphans 2>&1 || true', timeout=60)
stdout.channel.recv_exit_status()
print('Done')

print('\n=== 构建并启动 (5-10分钟) ===')
cmd = f'cd {BASE} && docker-compose up -d --build 2>&1'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=1800)

# 等待
exit_code = stdout.channel.recv_exit_status()
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')

# 检查是否成功
if 'ssl_version' in err or exit_code != 0:
    print(f'\n=== 错误 (exit={exit_code}) ===')
    print(err[-1000:])
    
    # 回退: 直接使用 docker build 和 docker run
    print('\n=== 回退方案: 直接 docker build ===')
    
    print('Building backend...')
    stdin, stdout, stderr = ssh.exec_command(
        f'cd {BASE} && docker build -f Dockerfile.backend -t sageai-backend . 2>&1',
        timeout=900
    )
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    print(f'Backend build exit={exit_code}')
    print(out[-500:])
    
    if exit_code == 0:
        print('\nBuilding frontend...')
        stdin, stdout, stderr = ssh.exec_command(
            f'cd {BASE} && docker build -f Dockerfile.frontend -t sageai-frontend . 2>&1',
            timeout=900
        )
        exit_code = stdout.channel.recv_exit_status()
        out = stdout.read().decode('utf-8', errors='replace')
        print(f'Frontend build exit={exit_code}')
        print(out[-500:])
        
        if exit_code == 0:
            # 停止并删除旧容器
            ssh.exec_command('docker stop sageai-backend sageai-frontend 2>/dev/null || true', timeout=10)
            ssh.exec_command('docker rm sageai-backend sageai-frontend 2>/dev/null || true', timeout=10)
            
            # 创建网络
            ssh.exec_command('docker network create sageai-network 2>/dev/null || true', timeout=10)
            
            # 启动后端
            stdin, stdout, stderr = ssh.exec_command(
                f'docker run -d --name sageai-backend --network sageai-network '
                f'--restart unless-stopped -p 8000:8000 '
                f'--env-file {BASE}/.env.production '
                f'-e ENV=production -e DATABASE_URL=sqlite:////app/data/app.db '
                f'-v sageai-db-data:/app/data -v sageai-log-data:/app/logs '
                f'sageai-backend 2>&1',
                timeout=30
            )
            print(stdout.read().decode())
            print(stderr.read().decode())
            
            # 启动前端
            stdin, stdout, stderr = ssh.exec_command(
                f'docker run -d --name sageai-frontend --network sageai-network '
                f'--restart unless-stopped -p 80:80 '
                f'sageai-frontend 2>&1',
                timeout=30
            )
            print(stdout.read().decode())
            print(stderr.read().decode())
else:
    print('\n=== Build output ===')
    print(out[-1000:])

# 等待
print('\nWaiting 20s...')
time.sleep(20)

# 检查
print('\n=== Status ===')
stdin, stdout, stderr = ssh.exec_command(
    'docker ps --filter name=sageai --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"',
    timeout=10
)
print(stdout.read().decode())

print('\n=== Health ===')
stdin, stdout, stderr = ssh.exec_command(
    'curl -s -w "\\nHTTP:%{http_code}" http://localhost:8000/health 2>&1',
    timeout=10
)
print(stdout.read().decode()[:500])

ssh.close()
print('\nDone!')
