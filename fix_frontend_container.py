"""将前端文件复制到容器内"""
import paramiko
import os

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
LOCAL_DIST = "f:/ai/Sage/frontend/dist"

def main():
    print("=" * 60)
    print("将前端文件复制到容器内")
    print("=" * 60)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=30)
    
    try:
        # 1. 清空容器内的前端目录
        print("\n[1/3] 清空容器内的前端目录...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai rm -rf /app/frontend/*")
        stdout.channel.recv_exit_status()
        print("  [OK] 已清空")
        
        # 2. 上传本地dist目录到服务器临时位置
        print("\n[2/3] 上传前端文件到服务器临时位置...")
        sftp = ssh.open_sftp()
        # 先清空服务器临时目录
        ssh.exec_command("rm -rf /tmp/frontend_dist && mkdir -p /tmp/frontend_dist")
        
        # 遍历上传
        for root, dirs, files in os.walk(LOCAL_DIST):
            for file in files:
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, LOCAL_DIST)
                remote_path = f"/tmp/frontend_dist/{rel_path.replace(chr(92), '/')}"
                
                # 确保目录存在
                remote_dir = os.path.dirname(remote_path)
                try:
                    sftp.stat(remote_dir)
                except:
                    # 创建目录
                    ssh.exec_command(f"mkdir -p '{remote_dir}'")
                
                sftp.put(local_path, remote_path)
                print(f"  [OK] {rel_path}")
        
        sftp.close()
        
        # 3. 复制到容器内
        print("\n[3/3] 复制到容器内...")
        stdin, stdout, stderr = ssh.exec_command("docker cp /tmp/frontend_dist/. sageai:/app/frontend/")
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        print(f"  {output if output else '[OK] 复制完成'}")
        
        # 验证
        print("\n[4/4] 验证文件...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai ls -la /app/frontend/")
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        print(output)
        
        print("\n" + "=" * 60)
        print("前端文件已复制到容器内！")
        print("请刷新浏览器页面（强制刷新 Ctrl+F5）")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    main()