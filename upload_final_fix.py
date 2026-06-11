"""上传修复后的前端文件"""
import paramiko
import os

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
LOCAL_DIST = "f:/ai/Sage/frontend/dist"

def ssh_exec(cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=60)
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')
    finally:
        ssh.close()

def main():
    print("=" * 60)
    print("上传修复后的前端文件")
    print("=" * 60)
    
    try:
        # 1. 清空宿主机的前端目录
        print("\n[1/4] 清空宿主机前端目录...")
        ssh_exec("rm -rf /app/frontend/* && mkdir -p /app/frontend/static")
        print("  [OK]")
        
        # 2. 使用SFTP上传文件到宿主机
        print("\n[2/4] 上传文件到宿主机...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=60)
        sftp = ssh.open_sftp()
        
        for root, dirs, files in os.walk(LOCAL_DIST):
            for file in files:
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, LOCAL_DIST)
                remote_path = f"/app/frontend/{rel_path.replace(chr(92), '/')}"
                remote_dir = os.path.dirname(remote_path)
                
                try:
                    sftp.stat(remote_dir)
                except:
                    ssh.exec_command(f"mkdir -p '{remote_dir}'")
                
                sftp.put(local_path, remote_path)
                print(f"  [OK] {rel_path}")
        
        sftp.close()
        ssh.close()
        
        # 3. 清空容器内的前端目录
        print("\n[3/4] 清空容器内前端目录...")
        ssh_exec("docker exec sageai rm -rf /app/frontend/* && docker exec sageai mkdir -p /app/frontend/static")
        print("  [OK]")
        
        # 4. 使用docker cp复制到容器
        print("\n[4/4] 复制到容器...")
        output, error = ssh_exec("docker cp /app/frontend/. sageai:/app/frontend/")
        print(f"  {output if output else '[OK]'}")
        
        print("\n" + "=" * 60)
        print("前端文件上传完成！")
        print("请强制刷新浏览器 (Ctrl+F5)")
        print("然后重新登录测试邀请链接功能")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()