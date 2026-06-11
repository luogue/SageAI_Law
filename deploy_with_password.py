"""SageAI 一键部署脚本（带密码）"""
import subprocess
import sys
import os

SERVER = "root@120.77.171.21"
PASSWORD = "!1iIlL.,44166"
PROJECT_DIR = "/opt/sageai"
BACKEND_CONTAINER = "sageai-backend"
LOCAL_BASE = "f:/ai/Sage"

FILES_TO_UPLOAD = [
    ("backend/auth/routes.py", "backend/auth/routes.py"),
    ("backend/utils/sms_client.py", "backend/utils/sms_client.py"),
    ("backend/storage/crud.py", "backend/storage/crud.py"),
    ("backend/reset_password.py", "backend/reset_password.py"),
]

def run_cmd(cmd, check=True, capture=True):
    print(f"  [CMD] {cmd[:120]}{'...' if len(cmd) > 120 else ''}")
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if check and result.returncode != 0:
        print(f"  [ERR] {result.stderr}")
        if not result.stderr.strip():
            print(f"  [OUT] {result.stdout}")
    return result

def ssh_cmd_with_password(cmd):
    """使用 sshpass 在服务器上执行命令"""
    full_cmd = f'sshpass -p "{PASSWORD}" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 {SERVER} "{cmd}"'
    return run_cmd(full_cmd, check=False)

def scp_upload_with_password(local_path, remote_path):
    """使用 sshpass 上传文件到服务器"""
    full_cmd = f'sshpass -p "{PASSWORD}" scp -o StrictHostKeyChecking=no -o ConnectTimeout=10 "{local_path}" {SERVER}:{PROJECT_DIR}/{remote_path}'
    return run_cmd(full_cmd)

def main():
    print("=" * 60)
    print("SageAI 部署脚本（带密码）")
    print("=" * 60)
    
    # 检查 sshpass 是否可用
    print("\n[检查] 检查 sshpass...")
    r = run_cmd("sshpass --version", check=False)
    if r.returncode != 0:
        print("  [WARN] sshpass 未安装，尝试使用 plink...")
        # 尝试使用 plink (Windows PuTTY)
        r = run_cmd("where plink", check=False)
        if r.returncode != 0:
            print("  [ERROR] 未找到 sshpass 或 plink，请安装后重试")
            print("\n推荐方案：安装 OpenSSH 和 sshpass")
            print("Windows: 安装 Git Bash 或使用 WSL")
            return
        else:
            print("  [OK] plink 可用")
            use_plink = True
    else:
        print("  [OK] sshpass 可用")
        use_plink = False
    
    # 0. 检查 SSH 连接
    print("\n[0/5] 检查 SSH 连接...")
    if use_plink:
        # 使用 plink
        plink_path = r.stdout.strip()
        cmd = f'"{plink_path}" -ssh -pw "{PASSWORD}" {SERVER} "echo OK"'
    else:
        cmd = f'sshpass -p "{PASSWORD}" ssh -o StrictHostKeyChecking=no {SERVER} "echo OK"'
    
    r = run_cmd(cmd, check=False)
    if r.returncode != 0:
        print(f"  SSH 连接失败: {r.stderr[:200]}")
        return
    
    print("  [OK] SSH 连接正常")
    
    # 1. 上传所有后端文件
    print("\n[1/5] 上传后端文件...")
    for local, remote in FILES_TO_UPLOAD:
        print(f"  上传 {local} -> {remote}")
        local_full = f"{LOCAL_BASE}/{local}"
        if use_plink:
            cmd = f'"{plink_path}" -batch -ssh -pw "{PASSWORD}" {SERVER} "mkdir -p {PROJECT_DIR}/backend/auth {PROJECT_DIR}/backend/utils {PROJECT_DIR}/backend/storage"'
            run_cmd(cmd, check=False)
            cmd = f'"{plink_path}" -batch -pw "{PASSWORD}" -scp "{local_full}" {SERVER}:{PROJECT_DIR}/{remote}'
        else:
            cmd = f'sshpass -p "{PASSWORD}" scp -o StrictHostKeyChecking=no "{local_full}" {SERVER}:{PROJECT_DIR}/{remote}'
        r = run_cmd(cmd, check=False)
        if r.returncode == 0:
            print(f"  [OK] {local}")
        else:
            print(f"  [FAIL] {local}: {r.stderr[:100]}")
    
    # 2. 上传前端 dist
    print("\n[2/5] 上传前端构建产物...")
    if use_plink:
        cmd = f'"{plink_path}" -batch -ssh -pw "{PASSWORD}" {SERVER} "mkdir -p {PROJECT_DIR}/frontend/dist"'
        run_cmd(cmd, check=False)
        cmd = f'"{plink_path}" -batch -pw "{PASSWORD}" -scp -r "{LOCAL_BASE}/frontend/dist/*" {SERVER}:{PROJECT_DIR}/frontend/dist/'
    else:
        cmd = f'sshpass -p "{PASSWORD}" scp -o StrictHostKeyChecking=no -r "{LOCAL_BASE}/frontend/dist/*" {SERVER}:{PROJECT_DIR}/frontend/dist/'
    r = run_cmd(cmd, check=False)
    if r.returncode == 0:
        print("  [OK] 前端文件上传完成")
    else:
        print(f"  [WARN] 前端上传可能有问题: {r.stderr[:200]}")
    
    # 3. 重建 Docker
    print("\n[3/5] 重建 Docker 容器...")
    if use_plink:
        cmd = f'"{plink_path}" -batch -ssh -pw "{PASSWORD}" {SERVER} "cd {PROJECT_DIR} && docker-compose down && docker-compose build --no-cache backend frontend 2>&1 | tail -20 && docker-compose up -d"'
    else:
        cmd = f'sshpass -p "{PASSWORD}" ssh -o StrictHostKeyChecking=no {SERVER} "cd {PROJECT_DIR} && docker-compose down && docker-compose build --no-cache backend frontend 2>&1 | tail -20 && docker-compose up -d"'
    r = run_cmd(cmd, check=False)
    print(f"  结果: {r.stdout.strip()[:500] if r.stdout else r.stderr.strip()[:500]}")
    
    # 等待服务启动
    import time
    print("  等待服务启动 (15秒)...")
    time.sleep(15)
    
    # 4. 重置密码
    print("\n[4/5] 重置密码...")
    if use_plink:
        cmd = f'"{plink_path}" -batch -ssh -pw "{PASSWORD}" {SERVER} "docker exec {BACKEND_CONTAINER} python /app/reset_password.py 15680793860 123456"'
    else:
        cmd = f'sshpass -p "{PASSWORD}" ssh -o StrictHostKeyChecking=no {SERVER} "docker exec {BACKEND_CONTAINER} python /app/reset_password.py 15680793860 123456"'
    r = run_cmd(cmd, check=False)
    print(f"  {r.stdout.strip() if r.stdout else r.stderr.strip()}")
    
    # 5. 测试
    print("\n[5/5] 测试接口...")
    if use_plink:
        cmd = f'"{plink_path}" -batch -ssh -pw "{PASSWORD}" {SERVER} \'curl -s -w " HTTP:%{{http_code}}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{{"phone":"+8615680793860","password":"123456"}}\''
    else:
        cmd = f'sshpass -p "{PASSWORD}" ssh -o StrictHostKeyChecking=no {SERVER} \'curl -s -w " HTTP:%{{http_code}}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{{"phone":"+8615680793860","password":"123456"}}\''
    r = run_cmd(cmd, check=False)
    print(f"  登录测试: {r.stdout.strip()}")
    
    print("\n" + "=" * 60)
    print("部署完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()