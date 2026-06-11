"""重启远程服务器上的 sageai 容器"""
import paramiko

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"

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
            print(f"  [OUT] {output}")

        return True, output
    except Exception as e:
        print(f"  [ERR] 执行命令失败: {e}")
        return False, str(e)

def main():
    print("=" * 60)
    print("重启 sageai 容器")
    print("=" * 60)

    # 1. 重启容器
    print("\n[1/2] 重启 sageai 容器...")
    success, output = execute_command("docker restart sageai")
    if success:
        print("  [OK] 容器重启成功")

    # 2. 检查容器状态
    print("\n[2/2] 检查容器状态...")
    success, output = execute_command("docker ps | grep sageai")
    if success:
        print("  [OK] 容器运行状态检查成功")

    # 3. 查看最新日志
    print("\n[3/3] 查看最新日志（最后10行）...")
    success, output = execute_command("docker logs --tail 10 sageai")
    if success:
        print("  [OK] 日志获取成功")

    print("\n" + "=" * 60)
    print("容器重启完成！Mock 模式已禁用")
    print("=" * 60)

if __name__ == "__main__":
    main()