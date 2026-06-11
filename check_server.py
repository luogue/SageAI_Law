import socket, paramiko, time

print("=== Server Status Check ===")

# 1. Port check
for port, name in [(22, "SSH"), (80, "HTTP"), (8000, "App")]:
    s = socket.socket()
    s.settimeout(3)
    r = s.connect_ex(('120.77.171.21', port))
    print(f"Port {port} ({name}): {'OPEN' if r == 0 else 'CLOSED'}")
    s.close()

# 2. SSH + Docker check
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('120.77.171.21', 22, 'root', '!1iIlL.,44166', timeout=15, banner_timeout=15)
    print("\nSSH: CONNECTED")
    
    # Docker containers
    _, stdout, _ = ssh.exec_command('docker ps --format "{{.Names}} {{.Status}} {{.Ports}}" 2>&1')
    print("Containers:")
    for line in stdout.read().decode().strip().split('\n'):
        if line: print(f"  - {line}")
    
    # Health check
    _, stdout, _ = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null')
    code = stdout.read().decode().strip()
    print(f"\nHealth check (port 8000): HTTP {code}")
    
    # Also check port 80
    _, stdout, _ = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:80/ 2>/dev/null')
    code80 = stdout.read().decode().strip()
    print(f"Health check (port 80): HTTP {code80}")
    
    ssh.close()
except Exception as e:
    print(f"\nSSH: FAILED - {e}")
