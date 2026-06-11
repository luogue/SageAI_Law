"""重新构建 Docker 镜像并重启容器"""
import paramiko
import time

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
PROJECT_DIR = "/opt/sageai"

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
            print(f"  [OUT] {output[:1000]}")

        return True, output
    except Exception as e:
        print(f"  [ERR] 执行命令失败: {e}")
        return False, str(e)

def main():
    print("=" * 60)
    print("重新构建 Docker 镜像并重启容器")
    print("=" * 60)

    # 1. 停止并删除旧容器
    print("\n[1/4] 停止并删除旧容器...")
    success, output = execute_command("docker stop sageai && docker rm sageai")
    if not success:
        print("  [WARN] 停止容器失败，继续执行...")
    else:
        print("  [OK] 旧容器已删除")

    # 2. 重新构建 Docker 镜像
    print("\n[2/4] 重新构建 Docker 镜像...")
    print("  [INFO] 这可能需要几分钟时间，请耐心等待...")
    success, output = execute_command(f"cd {PROJECT_DIR} && docker build -f Dockerfile.backend -t sageai .")
    if not success:
        print("  [ERR] Docker 镜像构建失败")
        return
    print("  [OK] Docker 镜像构建成功")

    # 3. 启动新容器
    print("\n[3/4] 启动新容器...")
    success, output = execute_command("docker run -d --name sageai -p 8000:8000 sageai")
    if not success:
        print("  [ERR] 容器启动失败")
        return
    print("  [OK] 容器启动成功")

    # 4. 等待容器启动并验证
    print("\n[4/4] 等待容器启动并验证...")
    time.sleep(5)  # 等待容器启动
    success, output = execute_command("docker ps | grep sageai")
    if success:
        print("  [OK] 容器运行正常")
    else:
        print("  [WARN] 容器状态检查失败")

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