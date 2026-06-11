"""使用SFTP复制文件"""
import paramiko
import os
import time

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
LOCAL_DIST = "f:/ai/Sage/frontend/dist"

def create_ssh():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=60)
    return ssh

def main():
    print("=" * 60)
    print("使用SFTP复制文件")
    print("=" * 60)
    
    try:
        # 清空容器内的前端目录
        print("\n[1/4] 清空容器内的前端目录...")
        ssh = create_ssh()
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai rm -rf /app/frontend/*")
        stdout.channel.recv_exit_status()
        ssh.close()
        print("  [OK]")
        
        # 上传文件
        print("\n[2/4] 上传前端文件...")
        ssh = create_ssh()
        sftp = ssh.open_sftp()
        
        for root, dirs, files in os.walk(LOCAL_DIST):
            for file in files:
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, LOCAL_DIST)
                remote_path = f"/app/frontend/{rel_path.replace(chr(92), '/')}"
                remote_dir = os.path.dirname(remote_path)
                
                # 确保目录存在
                try:
                    sftp.stat(remote_dir)
                except:
                    ssh.exec_command(f"mkdir -p '{remote_dir}'")
                
                # 上传文件
                try:
                    sftp.put(local_path, remote_path)
                    print(f"  [OK] {rel_path}")
                except Exception as e:
                    print(f"  [FAIL] {rel_path}: {e}")
        
        sftp.close()
        ssh.close()
        print("  上传完成")
        
        # 验证
        print("\n[3/4] 验证文件...")
        ssh = create_ssh()
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai ls /app/frontend/static/*.js | wc -l")
        stdout.channel.recv_exit_status()
        count = stdout.read().decode('utf-8').strip()
        print(f"  JS文件数量: {count}")
        
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai grep -c 'user_id' /app/frontend/static/*.js 2>/dev/null || echo '0'")
        stdout.channel.recv_exit_status()
        result = stdout.read().decode('utf-8').strip()
        print(f"  包含user_id的文件: {result}")
        ssh.close()
        
        print("\n" + "=" * 60)
        print("文件复制完成！")
        print("请强制刷新浏览器 (Ctrl+F5)")
        print("然后重新登录！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()