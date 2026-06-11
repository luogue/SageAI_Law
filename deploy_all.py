"""SageAI 一键部署 + 密码重置脚本"""
import subprocess
import sys
import os

SERVER = "root@120.77.171.21"
PROJECT_DIR = "/opt/sageai"
BACKEND_CONTAINER = "sageai-backend"
FRONTEND_CONTAINER = "sageai-frontend"
LOCAL_BASE = "f:/ai/Sage"

# 需要上传的文件
FILES_TO_UPLOAD = [
    ("backend/auth/routes.py", "backend/auth/routes.py"),
    ("backend/utils/sms_client.py", "backend/utils/sms_client.py"),
    ("backend/storage/crud.py", "backend/storage/crud.py"),
    ("backend/reset_password.py", "backend/reset_password.py"),
]

def run_cmd(cmd, check=True, capture=True):
    """运行本地命令"""
    print(f"  [CMD] {cmd[:120]}{'...' if len(cmd) > 120 else ''}")
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if check and result.returncode != 0:
        print(f"  [ERR] {result.stderr}")
        if not result.stderr.strip():
            print(f"  [OUT] {result.stdout}")
    return result

def ssh_cmd(cmd):
    """在服务器上执行命令"""
    full_cmd = f'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 {SERVER} "{cmd}"'
    return run_cmd(full_cmd, check=False)

def scp_upload(local_path, remote_path):
    """上传文件到服务器"""
    full_cmd = f'scp -o StrictHostKeyChecking=no -o ConnectTimeout=10 "{local_path}" {SERVER}:{PROJECT_DIR}/{remote_path}'
    return run_cmd(full_cmd)

def main():
    print("=" * 60)
    print("SageAI 部署脚本 v3")
    print("=" * 60)
    
    # 0. 检查 SSH 连接
    print("\n[0/5] 检查 SSH 连接...")
    r = ssh_cmd("echo OK")
    if r.returncode != 0:
        print(f"  SSH 连接失败: {r.stderr}")
        print("\n请手动执行以下步骤：")
        print(f"  1. 上传文件到 {SERVER}:{PROJECT_DIR}/")
        for local, remote in FILES_TO_UPLOAD:
            print(f"     scp {LOCAL_BASE}/{local} {SERVER}:{PROJECT_DIR}/{remote}")
        print(f"  2. 上传前端: scp -r {LOCAL_BASE}/frontend/dist/* {SERVER}:{PROJECT_DIR}/frontend/dist/")
        print(f"  3. SSH 登录后执行:")
        print(f"     cd {PROJECT_DIR}")
        print(f"     docker-compose down")
        print(f"     docker-compose build --no-cache backend frontend")
        print(f"     docker-compose up -d")
        print(f"  4. 重置密码:")
        print(f"     docker exec {BACKEND_CONTAINER} python /app/reset_password.py 15680793860 123456")
        print(f"  5. 测试:")
        print(f'     curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{{"phone":"+8615680793860","password":"123456"}}\'')
        return
    
    print("  [OK] SSH 连接正常")
    
    # 1. 上传所有后端文件
    print("\n[1/5] 上传后端文件...")
    for local, remote in FILES_TO_UPLOAD:
        print(f"  上传 {local} -> {remote}")
        r = scp_upload(f"{LOCAL_BASE}/{local}", remote)
        if r.returncode != 0:
            print(f"  [WARN] 上传失败: {r.stderr}")
    
    # 2. 上传前端 dist
    print("\n[2/5] 上传前端构建产物...")
    r = ssh_cmd(f"mkdir -p {PROJECT_DIR}/frontend/dist")
    r = run_cmd(
        f'scp -o StrictHostKeyChecking=no -o ConnectTimeout=10 -r '
        f'{LOCAL_BASE}/frontend/dist/* {SERVER}:{PROJECT_DIR}/frontend/dist/',
        check=False
    )
    if r.returncode == 0:
        print("  [OK] 前端文件上传完成")
    else:
        print(f"  [WARN] 前端上传可能有问题: {r.stderr[:200] if r.stderr else 'unknown'}")
    
    # 3. 重建 Docker
    print("\n[3/5] 重建 Docker 容器...")
    r = ssh_cmd(f"cd {PROJECT_DIR} && docker-compose down")
    print(f"  down: {r.stdout.strip() if r.stdout else r.stderr.strip()}")
    
    r = ssh_cmd(f"cd {PROJECT_DIR} && docker-compose build --no-cache backend frontend 2>&1 | tail -20")
    print(f"  build: {r.stdout.strip()[:500] if r.stdout else r.stderr.strip()[:500]}")
    
    r = ssh_cmd(f"cd {PROJECT_DIR} && docker-compose up -d")
    print(f"  up: {r.stdout.strip() if r.stdout else r.stderr.strip()}")
    
    # 等待服务启动
    import time
    print("  等待服务启动 (10秒)...")
    time.sleep(10)
    
    # 4. 重置密码
    print("\n[4/5] 重置密码...")
    r = ssh_cmd(f"docker exec {BACKEND_CONTAINER} python /app/reset_password.py 15680793860 123456")
    print(f"  {r.stdout.strip() if r.stdout else r.stderr.strip()}")
    
    # 5. 测试
    print("\n[5/5] 测试接口...")
    r = ssh_cmd(
        'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login '
        '-H "Content-Type: application/json" '
        '-d \'{"phone":"+8615680793860","password":"123456"}\''
    )
    print(f"  登录测试: {r.stdout.strip()}")
    
    r = ssh_cmd(
        'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/register '
        '-H "Content-Type: application/json" '
        '-d \'{"phone":"+8615680793860","sms_code":"123456","password":"123456","confirm_password":"123456"}\''
    )
    print(f"  注册测试: {r.stdout.strip()}")
    
    print("\n" + "=" * 60)
    print("部署完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
