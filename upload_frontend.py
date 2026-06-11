"""上传前端文件到服务器"""
import paramiko
import os

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
LOCAL_DIST = "f:/ai/Sage/frontend/dist"
REMOTE_DIR = "/opt/sageai/frontend"

def upload_file(ssh, local_path, remote_path):
    """上传单个文件"""
    sftp = ssh.open_sftp()
    try:
        sftp.put(local_path, remote_path)
        return True
    except Exception as e:
        print(f"  上传失败 {local_path}: {e}")
        return False
    finally:
        sftp.close()

def upload_directory(ssh, local_dir, remote_dir):
    """递归上传目录"""
    sftp = ssh.open_sftp()
    try:
        # 创建远程目录
        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            sftp.mkdir(remote_dir)
        
        for item in os.listdir(local_dir):
            local_item = os.path.join(local_dir, item)
            remote_item = f"{remote_dir}/{item}"
            
            if os.path.isfile(local_item):
                sftp.put(local_item, remote_item)
                print(f"  [OK] {item}")
            elif os.path.isdir(local_item):
                try:
                    sftp.stat(remote_item)
                except FileNotFoundError:
                    sftp.mkdir(remote_item)
                upload_directory(ssh, local_item, remote_item)
    finally:
        sftp.close()

def main():
    print("=" * 60)
    print("上传前端文件到服务器")
    print("=" * 60)
    
    try:
        # 连接服务器
        print(f"\n[1/2] 连接服务器 {SERVER}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=30)
        print("  [OK] 连接成功")
        
        # 清空远程目录
        print("\n[2/2] 清空并上传文件...")
        stdin, stdout, stderr = ssh.exec_command(f"rm -rf {REMOTE_DIR}/*")
        stdout.channel.recv_exit_status()
        
        # 上传目录
        upload_directory(ssh, LOCAL_DIST, REMOTE_DIR)
        
        # 验证上传
        stdin, stdout, stderr = ssh.exec_command(f"ls -la {REMOTE_DIR}/")
        output = stdout.read().decode('utf-8')
        print(f"\n  远程目录内容:\n{output}")
        
        ssh.close()
        
        print("\n" + "=" * 60)
        print("上传完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] 上传失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()