import time, socket, paramiko, sys

print("Waiting 180s more...", flush=True)
for i in range(18, 0, -1):
    time.sleep(10)
    print(f"  {i*10}s...", flush=True)
print("Checking now...", flush=True)

host = '120.77.171.21'

# Check port 22 (SSH)
print("\n--- SSH (port 22) ---")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(15)
    s.connect((host, 22))
    banner = s.recv(1024).decode('utf-8', errors='replace').strip()
    print(f"SSH banner: {banner[:100]}")
    s.close()
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='root', password='!1iIlL.,44166', timeout=30)
    i, o, e = ssh.exec_command('docker ps --format "table {{.Names}}\t{{.Status}}" 2>&1')
    print(f"Docker ps:\n{o.read().decode()}")
    i, o, e = ssh.exec_command('curl -s -m 5 localhost:8000/health 2>&1')
    print(f"Health: {o.read().decode().strip()}")
    ssh.close()
except Exception as ex:
    print(f"SSH FAIL: {ex}")

# Check port 80
print("\n--- HTTP (port 80) ---")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((host, 80))
    print("Port 80: OPEN")
    s.close()
except Exception as e:
    print(f"Port 80: {e}")

# Check port 8000
print("--- API (port 8000) ---")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((host, 8000))
    print("Port 8000: OPEN")
    s.close()
except Exception as e:
    print(f"Port 8000: {e}")
