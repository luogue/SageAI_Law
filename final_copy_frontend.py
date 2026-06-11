"""最终修复：强制复制前端文件到容器"""
import paramiko
import os

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
LOCAL_DIST = "f:/ai/Sage/frontend/dist"

def main():
    print("=" * 60)
    print("最终修复：强制复制前端文件到容器")
    print("=" * 60)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=60)
    
    try:
        # 1. 清空容器内的前端目录
        print("\n[1/6] 清空容器内的前端目录...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai rm -rf /app/frontend/*")
        stdout.channel.recv_exit_status()
        print("  [OK]")
        
        # 2. 验证目录已清空
        print("\n[2/6] 验证目录已清空...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai ls /app/frontend/")
        stdout.channel.recv_exit_status()
        print(f"  {stdout.read().decode('utf-8').strip()}")
        
        # 3. 上传本地dist目录到服务器临时位置
        print("\n[3/6] 上传前端文件到服务器临时位置...")
        sftp = ssh.open_sftp()
        
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
                    ssh.exec_command(f"mkdir -p '{remote_dir}'")
                
                sftp.put(local_path, remote_path)
        
        sftp.close()
        print(f"  [OK] 上传完成")
        
        # 4. 复制到容器内
        print("\n[4/6] 复制到容器内...")
        stdin, stdout, stderr = ssh.exec_command("docker cp /tmp/frontend_dist/. sageai:/app/frontend/")
        stdout.channel.recv_exit_status()
        print("  [OK]")
        
        # 5. 验证文件
        print("\n[5/6] 验证文件...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai ls /app/frontend/static/*.js | wc -l")
        stdout.channel.recv_exit_status()
        count = stdout.read().decode('utf-8').strip()
        print(f"  JS文件数量: {count}")
        
        # 6. 检查user_id
        print("\n[6/6] 检查user_id...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai grep -c 'user_id' /app/frontend/static/*.js 2>/dev/null || echo '0'")
        stdout.channel.recv_exit_status()
        result = stdout.read().decode('utf-8').strip()
        print(f"  包含user_id的文件: {result}")
        
        print("\n" + "=" * 60)
        print("前端文件已复制完成！")
        print("请强制刷新浏览器 (Ctrl+F5) 或清除浏览器缓存")
        print("然后重新登录！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()

if __name__ == "__main__":
    main()