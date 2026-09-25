#!/usr/bin/env python3
"""SageAI 打包+部署 - 排除 node_modules 和 dist"""
import tarfile, os, subprocess as sp, time, fnmatch

os.chdir(r'f:\ai\Sage')

# Exclude patterns for tar
EXCLUDE = {'node_modules', 'dist', '__pycache__', '.git', 'data', 'logs', '*.pyc', '*.tar.gz',
           '*.db', '*.db-*', '*.sqlite', '*.sqlite-*', '*.sqlite3', '*.sqlite3-*', '*.bak'}

def should_exclude(name):
    parts = name.replace('\\', '/').split('/')
    for p in parts:
        if any(fnmatch.fnmatch(p, pattern) for pattern in EXCLUDE):
            return True
    return False

print("=== Building package ===")
files = ['backend', 'frontend', 'Dockerfile.backend', 'Dockerfile.frontend', '.dockerignore', 'docker-compose.yml', 'nginx.conf', '.env.production']
tarball = 'sageai-deploy.tar.gz'
if os.path.exists(tarball):
    os.remove(tarball)
with tarfile.open(tarball, 'w:gz') as tar:
    for f in files:
        if os.path.isdir(f):
            for root, dirs, filenames in os.walk(f):
                dirs[:] = [d for d in dirs if d not in EXCLUDE]
                for fn in filenames:
                    if fn.endswith('.pyc') or fn in EXCLUDE:
                        continue
                    full = os.path.join(root, fn)
                    if should_exclude(full):
                        continue
                    # Filter frontend specific
                    if fnmatch.fnmatch(full, '*node_modules*') or fnmatch.fnmatch(full, '*dist*'):
                        continue
                    tar.add(full, arcname=full)
        else:
            tar.add(f, arcname=f)
size = os.path.getsize(tarball)/1024/1024
print(f"Package: {size:.1f}MB")

# Deploy
SCP = ['C:\\Windows\\System32\\OpenSSH\\scp.exe', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=NUL']
SSH = ['C:\\Windows\\System32\\OpenSSH\\ssh.exe', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=NUL', 'root@120.77.171.21']

print("Uploading...")
r = sp.run(SCP + [tarball, 'root@120.77.171.21:/opt/sageai/'], capture_output=True, text=True, timeout=120)
if r.returncode != 0:
    print(f"FAIL upload: {r.stderr[:200]}")
    exit(1)
print("Upload OK")

print("Stopping old...")
r = sp.run(SSH + ['cd /opt/sageai && docker compose down 2>&1 || true'], capture_output=True, text=True, timeout=30)
print(r.stdout.strip()[:100] or "done")

print("Extracting...")
# Runtime data may still live below backend in older installations: never recursively remove it.
r = sp.run(SSH + ['cd /opt/sageai && tar -xzf sageai-deploy.tar.gz 2>&1 && echo OK'], capture_output=True, text=True, timeout=30)
print(r.stdout.strip())

print("Building (wait up to 5min)...")
r = sp.run(SSH + ['cd /opt/sageai && docker compose up -d --build 2>&1'], capture_output=True, text=True, timeout=300)
for l in r.stdout.strip().split('\n')[-25:]:
    print(f"  {l}")

print("\nHealth check...")
r = sp.run(SSH + ['curl -s localhost:8000/health 2>/dev/null || echo NO'], capture_output=True, text=True, timeout=10)
print(f"Health: {r.stdout.strip()}")

if r.stdout.strip() != 'NO':
    print("\n=== DEPLOY SUCCESS ===")
else:
    print("\n[!] Backend may still be starting")
