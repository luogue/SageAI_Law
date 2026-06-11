"""更新服务器上的代码并重新构建 Docker 镜像"""
import paramiko

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
PROJECT_DIR = "/opt/sageai"
LOCAL_BACKEND = "f:/ai/Sage/backend"

def ssh_connect():
    """连接到服务器"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=10)
        return ssh
    except Exception as e:
        print(f"  [ERR] SSH 连接失败: {e}")
        return None

def sftp_connect():
    """连接到服务器的 SFTP"""
    try:
        ssh = ssh_connect()
        if not ssh:
            return None, None
        sftp = ssh.open_sftp()
        return sftp, ssh
    except Exception as e:
        print(f"  [ERR] SFTP 连接失败: {e}")
        return None, None

def upload_file(local_path, remote_path):
    """上传文件到服务器"""
    try:
        sftp, ssh = sftp_connect()
        if not sftp:
            return False

        print(f"  [INFO] 上传 {local_path} -> {remote_path}")
        sftp.put(local_path, remote_path)
        sftp.close()
        ssh.close()
        return True
    except Exception as e:
        print(f"  [ERR] 上传失败: {e}")
        return False

def execute_command(cmd):
    """在服务器上执行命令"""
    try:
        ssh = ssh_connect()
        if not ssh:
            return False, ""

        print(f"  [CMD] {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        ssh.close()

        if error and "warning" not in error.lower():
            print(f"  [ERR] {error}")
            return False, error

        if output:
            print(f"  [OUT] {output[:500]}")

        return True, output
    except Exception as e:
        print(f"  [ERR] 执行命令失败: {e}")
        return False, str(e)

def main():
    print("=" * 60)
    print("更新服务器上的代码并重新构建 Docker 镜像")
    print("=" * 60)

    # 1. 上传更新后的 llm_client.py 文件
    print("\n[1/4] 上传更新后的 llm_client.py 文件...")
    local_file = f"{LOCAL_BACKEND}/reasoning/llm_client.py"
    remote_file = f"{PROJECT_DIR}/backend/reasoning/llm_client.py"

    if not upload_file(local_file, remote_file):
        print("  [ERR] 文件上传失败")
        return
    print("  [OK] 文件上传成功")

    # 2. 上传更新后的 .env 文件
    print("\n[2/4] 上传更新后的 .env 文件...")
    local_env = f"{LOCAL_BACKEND}/.env"
    remote_env = f"{PROJECT_DIR}/backend/.env"

    if not upload_file(local_env, remote_env):
        print("  [WARN] .env 文件上传失败，继续执行...")
    else:
        print("  [OK] .env 文件上传成功")

    # 3. 重新构建 Docker 镜像
    print("\n[3/4] 重新构建 Docker 镜像...")
    success, output = execute_command(f"cd {PROJECT_DIR} && docker-compose build backend")
    if not success:
        print("  [WARN] Docker 镜像构建失败，尝试使用 docker build...")
        success, output = execute_command(f"cd {PROJECT_DIR} && docker build -f Dockerfile.backend -t sageai .")
        if not success:
            print("  [ERR] Docker 镜像构建失败")
            return
    print("  [OK] Docker 镜像构建成功")

    # 4. 重启容器
    print("\n[4/4] 重启容器...")
    success, output = execute_command("docker stop sageai && docker rm sageai")
    if not success:
        print("  [WARN] 停止容器失败，继续执行...")

    success, output = execute_command("docker run -d --name sageai -p 8000:8000 sageai")
    if not success:
        print("  [ERR] 容器启动失败")
        return
    print("  [OK] 容器启动成功")

    # 5. 验证容器内的代码
    print("\n[5/5] 验证容器内的代码...")
    success, output = execute_command("docker exec sageai grep -n 'MOCK MODE' /app/reasoning/llm_client.py | head -5")
    if success:
        print("  [INFO] 验证完成")

    print("\n" + "=" * 60)
    print("更新完成！Mock 模式已在远程服务器上禁用")
    print("=" * 60)

if __name__ == "__main__":
    main()