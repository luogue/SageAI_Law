import paramiko, socket
socket.setdefaulttimeout(120)
s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    s.connect('120.77.171.21', username='root', password='!1iIlL.,44166', timeout=120, banner_timeout=120)
    print("SSH connected")
    i, o, e = s.exec_command('docker ps --format "table {{.Names}}\t{{.Status}}" 2>&1; echo ---; docker-compose ps 2>&1; echo ---; curl -s -m 5 localhost:8000/health 2>&1')
    print(o.read().decode())
    s.close()
except Exception as ex:
    print(f"FAIL: {ex}")
