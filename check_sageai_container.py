"""检查 sageai 容器内的代码"""
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
    print("检查 sageai 容器内的代码")
    print("=" * 60)

    # 1. 检查容器内的 Mock 模式代码
    print("\n[1/2] 检查容器内的 Mock 模式代码...")
    success, output = execute_command("docker exec sageai grep -n 'MOCK MODE' /app/reasoning/llm_client.py | head -5")
    if success:
        print("  [INFO] 检查完成")

    # 2. 检查容器内的 Mock 模式代码详情
    print("\n[2/2] 检查容器内的 Mock 模式代码详情...")
    success, output = execute_command("docker exec sageai grep -A 5 'if os.getenv.*LLM_MOCK_MODE' /app/reasoning/llm_client.py")
    if success:
        print("  [INFO] 检查完成")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()