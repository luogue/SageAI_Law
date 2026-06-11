import paramiko

try:
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=15)
    stdin, stdout, stderr = s.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health')
    print("H:" + stdout.read().decode().strip())
    stdin, stdout, stderr = s.exec_command('docker ps --format "{{.Names}}" 2>/dev/null | grep -i sage')
    print("C:" + stdout.read().decode().strip())
    s.close()
except Exception as e:
    print("E:" + type(e).__name__)
