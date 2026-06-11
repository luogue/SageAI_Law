#!/usr/bin/env python3
"""
SageAI 一键部署脚本（paramiko版）
- 打包项目（排除 node_modules/dist/__pycache__/.git）
- 通过 SFTP 上传到服务器
- 远程执行 docker compose 构建部署
- 健康检查 & 验证
"""
import os
import tarfile
import time
import io
import sys
import paramiko

# ========== 配置 ==========
SERVER_IP = "120.77.171.21"
SSH_USER = "root"
SSH_PASS = "!1iIlL.,44166"
REMOTE_DIR = "/opt/sageai"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TARBALL_NAME = "sageai-deploy.tar.gz"

# 要打包的文件/目录
INCLUDE_FILES = [
    "backend",
    "frontend",
    "Dockerfile.backend",
    "Dockerfile.frontend",
    "docker-compose.yml",
    "nginx.conf",
    ".env.production",
]

# 排除的目录/文件
EXCLUDE_DIRS = {"node_modules", "dist", "__pycache__", ".git", "logs", "uploaded_files", "__pycache__", ".pytest_cache"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".tar.gz", ".log"}


def build_package():
    """打包项目"""
    tarball = os.path.join(PROJECT_ROOT, TARBALL_NAME)
    if os.path.exists(tarball):
        os.remove(tarball)

    os.chdir(PROJECT_ROOT)
    include_set = set(INCLUDE_FILES)

    with tarfile.open(tarball, "w:gz") as tar:
        for item in INCLUDE_FILES:
            full = os.path.join(PROJECT_ROOT, item)
            if not os.path.exists(full):
                print(f"  [!] 跳过（不存在）: {item}")
                continue

            if os.path.isdir(full):
                for root, dirs, files in os.walk(full):
                    # 过滤目录
                    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                    for fn in files:
                        # 过滤文件
                        if fn in EXCLUDE_DIRS:
                            continue
                        _, ext = os.path.splitext(fn)
                        if ext in EXCLUDE_EXTS:
                            continue
                        # 跳过 node_modules 下的文件
                        fpath = os.path.join(root, fn)
                        if "node_modules" in fpath.replace("\\", "/").split("/"):
                            continue
                        arcname = os.path.relpath(fpath, PROJECT_ROOT)
                        tar.add(fpath, arcname=arcname)
            else:
                tar.add(full, arcname=item)

    size_mb = os.path.getsize(tarball) / (1024 * 1024)
    print(f"  [OK] 打包完成: {size_mb:.1f} MB")
    return tarball


def ssh_exec(ssh, cmd, timeout=300):
    """执行远程命令，实时打印输出"""
    print(f"  [CMD] {cmd[:100]}{'...' if len(cmd) > 100 else ''}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    if out.strip():
        print(out.strip())
    if err.strip():
        print(f"  [STDERR] {err.strip()[:500]}")
    return out, err


def main():
    print("=" * 60)
    print("  SageAI 一键部署")
    print(f"  服务器: {SSH_USER}@{SERVER_IP}:{REMOTE_DIR}")
    print("=" * 60)

    # ===== 步骤 1：打包 =====
    print("\n[1/5] 打包项目...")
    tarball = build_package()

    # ===== 步骤 2：连接服务器 =====
    print("\n[2/5] 连接服务器...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(SERVER_IP, username=SSH_USER, password=SSH_PASS, timeout=30)
        print("  [OK] SSH 连接成功")
    except Exception as e:
        print(f"  [FAIL] SSH 连接失败: {e}")
        sys.exit(1)

    # ===== 步骤 3：上传 =====
    print("\n[3/5] 上传部署包...")
    try:
        sftp = ssh.open_sftp()
        # 确保远程目录存在
        try:
            sftp.stat(REMOTE_DIR)
        except FileNotFoundError:
            ssh_exec(ssh, f"mkdir -p {REMOTE_DIR}")

        remote_tarball = f"{REMOTE_DIR}/{TARBALL_NAME}"
        sftp.put(tarball, remote_tarball)
        sftp.close()
        print(f"  [OK] 上传完成")
    except Exception as e:
        print(f"  [FAIL] 上传失败: {e}")
        ssh.close()
        sys.exit(1)

    # ===== 步骤 4：远程部署 =====
    print("\n[4/5] 远程部署...")

    # 4a. 停止旧容器 (兼容 docker-compose v1)
    print("  --- 停止旧容器 ---")
    ssh_exec(ssh, f"cd {REMOTE_DIR} && (docker-compose down 2>&1 || docker compose down 2>&1 || true)", timeout=60)

    # 4b. 解压覆盖
    print("  --- 解压更新文件 ---")
    ssh_exec(ssh, f"cd {REMOTE_DIR} && rm -rf backend frontend && tar -xzf {TARBALL_NAME} 2>&1", timeout=30)

    # 4c. 构建并启动 (兼容 docker-compose v1)
    print("  --- docker-compose build & up (等待最多 8 分钟) ---")
    ssh_exec(ssh, f"cd {REMOTE_DIR} && (docker-compose up -d --build 2>&1 || docker compose up -d --build 2>&1)", timeout=480)

    # ===== 步骤 5：健康检查 =====
    print("\n[5/5] 健康检查...")
    time.sleep(5)

    # 检查容器状态
    out, _ = ssh_exec(ssh, "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep -i sage", timeout=15)
    health_containers = out.strip()

    # 检查后端健康
    out, _ = ssh_exec(ssh, "curl -s -m 10 http://localhost:8000/health 2>&1 || echo 'UNREACHABLE'", timeout=15)
    health_api = out.strip()

    ssh.close()

    # 清理本地打包文件
    if os.path.exists(tarball):
        os.remove(tarball)

    # ===== 结果汇总 =====
    print("\n" + "=" * 60)
    print("  [RESULT] Deployment Result")
    print("=" * 60)
    print(f"\n  Containers:\n{health_containers}")
    print(f"\n  Health Check: {health_api}")

    if "healthy" in health_api.lower() or "ok" in health_api.lower():
        print("\n  [SUCCESS] Deploy OK!")
        print(f"  Visit: http://{SERVER_IP}")
    elif "sageai-backend" in health_containers and "sageai-frontend" in health_containers:
        print("\n  [WARN] Containers are up, service may still be initializing...")
        print(f"  Visit: http://{SERVER_IP}")
        print(f"  Wait 30s and retry")
    else:
        print("\n  [FAIL] Deployment may have issues, check server logs")
        print(f"  SSH: ssh root@{SERVER_IP}")
        print(f"  Cmd: cd {REMOTE_DIR} && docker compose logs")


if __name__ == "__main__":
    main()
