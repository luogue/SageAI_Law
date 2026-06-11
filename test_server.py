"""简单测试服务器连接和docker状态"""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)
print('Connected!')

# 测试 docker-compose
stdin, stdout, stderr = ssh.exec_command('cd /opt/sageai && docker-compose ps 2>&1', timeout=30)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(f'compose ps:\n{out}')
if err:
    print(f'compose err:\n{err}')

# 测试 docker
stdin, stdout, stderr = ssh.exec_command('docker ps -a 2>&1', timeout=30)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(f'\ndocker ps:\n{out}')

# 直接运行docker而非docker-compose
stdin, stdout, stderr = ssh.exec_command('ls -la /opt/sageai/Dockerfile.backend /opt/sageai/docker-compose.yml 2>&1', timeout=30)
out = stdout.read().decode('utf-8', errors='replace')
print(f'\nfiles:\n{out}')

ssh.close()
