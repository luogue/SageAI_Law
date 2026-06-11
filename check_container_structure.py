"""检查容器内的实际路径结构"""
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
    print("检查容器内的实际路径结构")
    print("=" * 60)

    # 1. 检查容器内的根目录
    print("\n[1/4] 检查容器内的根目录...")
    success, output = execute_command("docker exec sageai ls -la /")
    if success:
        print("  [INFO] 检查完成")

    # 2. 检查容器内的 app 目录
    print("\n[2/4] 检查容器内的 app 目录...")
    success, output = execute_command("docker exec sageai ls -la /app")
    if success:
        print("  [INFO] 检查完成")

    # 3. 查找 llm_client.py 文件
    print("\n[3/4] 查找 llm_client.py 文件...")
    success, output = execute_command("docker exec sageai find / -name 'llm_client.py' 2>/dev/null")
    if success:
        print("  [INFO] 查找完成")

    # 4. 检查 docker-compose.yml 配置
    print("\n[4/4] 检查 docker-compose.yml 配置...")
    success, output = execute_command("cat /opt/sageai/docker-compose.yml")
    if success:
        print("  [INFO] 检查完成")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()