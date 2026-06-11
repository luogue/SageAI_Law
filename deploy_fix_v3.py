"""上传修复文件到服务器并重建 Docker"""
import paramiko
import os

host = "120.77.171.21"
port = 22
user = "root"
password = "SageAI2026!@#$%^"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, user, password)

sftp = ssh.open_sftp()

local_root = r"f:\ai\Sage"
remote_root = "/opt/sageai"

# 上传修改的后端文件
files_to_upload = [
    "backend/auth/routes.py",
]

for f in files_to_upload:
    local = os.path.join(local_root, f)
    remote = f"{remote_root}/{f}"
    print(f"上传: {f}")
    sftp.put(local, remote)

# 上传 frontend dist
import os as _os
dist_path = os.path.join(local_root, "frontend", "dist")
remote_dist = f"{remote_root}/frontend/dist"

print(f"\n上传前端 dist/ 到 {remote_dist}")
for root, dirs, files in _os.walk(dist_path):
    rel = _os.path.relpath(root, dist_path)
    remote_dir = f"{remote_dist}/{rel}".replace("\\", "/")
    if rel == ".":
        remote_dir = remote_dist
    try:
        sftp.stat(remote_dir)
    except:
        # 递归创建目录
        ssh.exec_command(f"mkdir -p '{remote_dir}'")
    for fname in files:
        local_file = _os.path.join(root, fname)
        remote_file = f"{remote_dir}/{fname}".replace("\\", "/")
        sftp.put(local_file, remote_file)

print(f"\n前端文件上传完成")
sftp.close()

# 在服务器上重建 Docker
print("\n========== 重建 Docker 容器 ==========")
cmds = [
    "cd /opt/sageai",
    "docker stop sageai 2>/dev/null; docker rm sageai 2>/dev/null",
    "docker build -t sageai .",
    "docker run -d --name sageai --env-file /opt/sageai/.env -p 8000:8000 --restart unless-stopped sageai",
    "sleep 3",
    # 测试后端接口
    'curl -s -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"123456"}\'',
    "echo ''",
    'curl -s -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","sms_code":"123456","password":"123456","confirm_password":"123456"}\'',
]

for cmd in cmds:
    print(f"\n>>> {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out:
        print(out.strip())
    if err:
        print("STDERR:", err.strip())

# 更新 Nginx 前端文件（如果 nginx 直接 serve dist 目录）
print("\n========== 重载 Nginx ==========")
stdin, stdout, stderr = ssh.exec_command("nginx -s reload 2>&1")
print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()
print("\n========== 部署完成 ==========")
