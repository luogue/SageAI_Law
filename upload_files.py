"""手动上传文件到服务器"""
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

def main():
    print("=" * 60)
    print("手动上传文件到服务器")
    print("=" * 60)

    # 1. 上传更新后的 llm_client.py 文件
    print("\n[1/2] 上传更新后的 llm_client.py 文件...")
    local_file = f"{LOCAL_BACKEND}/reasoning/llm_client.py"
    remote_file = f"{PROJECT_DIR}/backend/reasoning/llm_client.py"

    if upload_file(local_file, remote_file):
        print("  [OK] 文件上传成功")
    else:
        print("  [ERR] 文件上传失败")
        return

    # 2. 上传更新后的 .env 文件
    print("\n[2/2] 上传更新后的 .env 文件...")
    local_env = f"{LOCAL_BACKEND}/.env"
    remote_env = f"{PROJECT_DIR}/backend/.env"

    if upload_file(local_env, remote_env):
        print("  [OK] .env 文件上传成功")
    else:
        print("  [WARN] .env 文件上传失败，继续执行...")

    print("\n" + "=" * 60)
    print("文件上传完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()