"""快速修复 docker-compose 兼容性问题"""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)
print('Connected!')

# 找到 docker_client.py 文件
cmd = "python3 -c \"import compose.cli.docker_client; print(compose.cli.docker_client.__file__)\" 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
filepath = stdout.read().decode('utf-8', errors='replace').strip()
print(f'Docker client file: {filepath}')

if filepath:
    # 修复: 移除 ssl_version 参数
    # 原始: kwargs_from_env(environment=environment, ssl_version=tls_version)
    # 修复: kwargs_from_env(environment=environment)
    
    # 先备份
    ssh.exec_command(f'cp {filepath} {filepath}.bak', timeout=5)
    
    # 执行 sed 替换
    fix_cmd = (
        f"sed -i 's/environment=environment, ssl_version=tls_version/environment=environment/' {filepath}"
    )
    print(f'Fixing...')
    stdin, stdout, stderr = ssh.exec_command(fix_cmd, timeout=10)
    stdout.channel.recv_exit_status()
    
    # 验证修复
    stdin, stdout, stderr = ssh.exec_command(f'grep "kwargs_from_env" {filepath}', timeout=10)
    print(f'After fix: {stdout.read().decode().strip()}')

    # 测试
    print('\nTesting docker-compose...')
    stdin, stdout, stderr = ssh.exec_command('cd /opt/sageai && docker-compose ps 2>&1', timeout=10)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    print(f'Result: {out.strip()}')
    if err.strip():
        if 'ssl_version' in err:
            print(f'Still has ssl_version error!')
        else:
            print(f'Error: {err[:200]}')

ssh.close()
print('\nDone!')
