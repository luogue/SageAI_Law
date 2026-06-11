"""完整部署脚本"""
import paramiko
import os

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
LOCAL_PROJECT = "f:/ai/Sage"
REMOTE_DIR = "/opt/sageai"

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

def upload_directory(local_dir, remote_dir):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=60)
    sftp = ssh.open_sftp()
    
    try:
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, local_dir)
                remote_path = f"{remote_dir}/{rel_path.replace(chr(92), '/')}"
                remote_file_dir = os.path.dirname(remote_path)
                
                try:
                    sftp.stat(remote_file_dir)
                except:
                    ssh.exec_command(f"mkdir -p '{remote_file_dir}'")
                
                sftp.put(local_path, remote_path)
                print(f"  [OK] {rel_path}")
    finally:
        sftp.close()
        ssh.close()

def main():
    print("=" * 60)
    print("完整部署到服务器")
    print("=" * 60)
    
    try:
        # 1. 创建远程目录
        print("\n[1/4] 创建远程目录...")
        ssh_exec(f"mkdir -p {REMOTE_DIR}")
        print("  [OK]")
        
        # 2. 上传后端代码
        print("\n[2/4] 上传后端代码...")
        upload_directory(f"{LOCAL_PROJECT}/backend", f"{REMOTE_DIR}/backend")
        
        # 3. 上传前端代码（dist目录）
        print("\n[3/4] 上传前端代码...")
        upload_directory(f"{LOCAL_PROJECT}/frontend/dist", f"{REMOTE_DIR}/frontend")
        
        # 4. 重启容器
        print("\n[4/4] 重启容器...")
        output, error = ssh_exec("docker restart sageai")
        print(f"  {output.strip()}")
        
        # 等待服务启动
        print("\n[等待] 等待服务启动...")
        import time
        time.sleep(10)
        
        # 测试服务
        print("\n[验证] 测试服务...")
        cmd = 'curl -s -w " HTTP:%{http_code}" http://localhost:8000/health'
        output, error = ssh_exec(cmd)
        print(f"  健康检查: {output.strip()}")
        
        print("\n" + "=" * 60)
        print("部署完成！")
        print(f"  服务器地址: http://{SERVER}")
        print(f"  项目目录: {REMOTE_DIR}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()