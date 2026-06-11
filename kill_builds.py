"""杀掉所有构建进程"""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=30)
print('Connected!')

# 杀掉所有 docker 构建进程
print('Killing all docker build processes...')
cmds = [
    'pkill -9 -f "docker build" 2>/dev/null; echo "killed docker build"',
    'pkill -9 -f "docker-compose build" 2>/dev/null; echo "killed compose build"',
    'pkill -9 -f "docker-compose up" 2>/dev/null; echo "killed compose up"',
    'docker stop $(docker ps -q) 2>/dev/null; echo "stopped containers"',
    'docker container prune -f 2>/dev/null; echo "pruned containers"',
]

for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace')
    print(f'  {out.strip()}')

# 确认没有残留
stdin, stdout, stderr = ssh.exec_command(
    'ps aux | grep -E "docker build|docker-compose" | grep -v grep | wc -l',
    timeout=10
)
count = stdout.read().decode('utf-8', errors='replace').strip()
print(f'\nRemaining build processes: {count}')

print('All cleaned up!')
ssh.close()
