import socket, sys

host = '120.77.171.21'

# Check port 80 (frontend)
print("Checking port 80 (HTTP)...")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((host, 80))
    s.send(b"GET / HTTP/1.1\r\nHost: 120.77.171.21\r\nConnection: close\r\n\r\n")
    resp = s.recv(4096).decode('utf-8', errors='replace')
    s.close()
    status_line = resp.split('\r\n')[0] if resp else 'no response'
    print(f"Port 80: {status_line[:120]}")
except Exception as e:
    print(f"Port 80 FAIL: {e}")

# Check port 8000 (backend API)
print("\nChecking port 8000 (API)...")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((host, 8000))
    s.send(b"GET /health HTTP/1.1\r\nHost: 120.77.171.21:8000\r\nConnection: close\r\n\r\n")
    resp = s.recv(4096).decode('utf-8', errors='replace')
    s.close()
    # Extract body
    parts = resp.split('\r\n\r\n', 1)
    body = parts[1] if len(parts) > 1 else resp
    print(f"Port 8000 /health: {body[:200]}")
except Exception as e:
    print(f"Port 8000 FAIL: {e}")
