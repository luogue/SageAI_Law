"""更新远程服务器上的 llm_client.py 文件并重启服务"""
import paramiko
import sys

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
PROJECT_DIR = "/opt/sageai"
LOCAL_BACKEND = "f:/ai/Sage/backend"
REMOTE_BACKEND = "/opt/sageai/backend"

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
            return None
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
    print("更新远程服务器 - 禁用 Mock 模式")
    print("=" * 60)

    # 1. 检查 SSH 连接
    print("\n[1/4] 检查 SSH 连接...")
    ssh = ssh_connect()
    if not ssh:
        print("  [ERR] 无法连接到服务器")
        return
    ssh.close()
    print("  [OK] SSH 连接成功")

    # 2. 上传更新后的 llm_client.py 文件
    print("\n[2/4] 上传更新后的 llm_client.py 文件...")
    local_file = f"{LOCAL_BACKEND}/reasoning/llm_client.py"
    remote_file = f"{REMOTE_BACKEND}/reasoning/llm_client.py"

    if not upload_file(local_file, remote_file):
        print("  [ERR] 文件上传失败")
        return
    print("  [OK] 文件上传成功")

    # 3. 验证文件已更新
    print("\n[3/4] 验证文件已更新...")
    success, output = execute_command(f"grep -n 'MOCK MODE' {remote_file} | head -5")
    if success:
        print("  [INFO] 文件内容预览：")
        print(output)

    # 4. 重启后端服务
    print("\n[4/4] 重启后端服务...")
    success, output = execute_command(f"cd {PROJECT_DIR} && docker-compose restart backend")
    if not success:
        print("  [WARN] docker-compose 重启失败，尝试手动重启...")
        success, output = execute_command(f"docker restart sageai-backend")
        if not success:
            print("  [ERR] 重启失败，请手动重启服务")
            return
    print("  [OK] 服务重启成功")

    print("\n" + "=" * 60)
    print("更新完成！Mock 模式已在远程服务器上禁用")
    print("=" * 60)

if __name__ == "__main__":
    main()