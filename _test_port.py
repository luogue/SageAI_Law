import socket, sys

host = '120.77.171.21'
port = 22

print(f"Testing TCP connection to {host}:{port}...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(30)
try:
    s.connect((host, port))
    banner = s.recv(1024)
    print(f"Port 22 OPEN, banner: {banner.decode('utf-8', errors='replace').strip()}")
    s.close()
except Exception as e:
    print(f"Port 22 FAIL: {e}")
    sys.exit(1)
