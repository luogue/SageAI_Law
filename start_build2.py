"""启动后台构建 - 不等待"""
import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)
print('Connected!')

BASE = '/opt/sageai'

# 使用 transport + channel 方式，不等待命令完成
print('Starting build in background...')
transport = ssh.get_transport()
channel = transport.open_session()
channel.setblocking(0)
channel.exec_command(f'cd {BASE} && docker-compose up -d --build > /tmp/sageai-build.log 2>&1')
print('Build started! PID check...')
time.sleep(2)

# Check that something is running
channel2 = transport.open_session()
channel2.exec_command('sleep 2 && ps aux | grep docker-compose | grep -v grep | head -3')
time.sleep(3)
out = channel2.recv(4096).decode('utf-8', errors='replace')
if out.strip():
    print(f'Build process found: {out.strip()[:200]}')
else:
    print('Build may have finished quickly or failed')
    # Check logs
    channel3 = transport.open_session()
    channel3.exec_command('cat /tmp/sageai-build.log 2>/dev/null | tail -10')
    time.sleep(2)
    log = channel3.recv(8192).decode('utf-8', errors='replace')
    print(f'Build log:\n{log}')

ssh.close()
print('\nBuild is running. Check with: python f:/ai/Sage/check_build.py')
