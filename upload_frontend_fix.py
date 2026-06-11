"""强制上传新的前端构建文件到服务器"""
import os
import paramiko

def main():
    server = "120.77.171.21"
    port = 22
    username = "root"
    password = "!1iIlL.,44166"
    local_path = r"f:\ai\Sage\frontend\dist"
    remote_path = "/opt/sageai/frontend"
    
    print("连接到服务器...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port, username, password, timeout=10)
    
    print("清理旧文件...")
    stdin, stdout, stderr = ssh.exec_command(f"rm -rf {remote_path}/*")
    stdout.channel.recv_exit_status()
    
    sftp = ssh.open_sftp()
    
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            relative_path = os.path.relpath(local_file, local_path)
            remote_file = os.path.join(remote_path, relative_path).replace('\\', '/')
            
            remote_dir = os.path.dirname(remote_file)
            try:
                sftp.stat(remote_dir)
            except FileNotFoundError:
                ssh.exec_command(f"mkdir -p {remote_dir}")
            
            print(f"上传: {file}")
            sftp.put(local_file, remote_file)
    
    sftp.close()
    
    print("\n验证:")
    stdin, stdout, stderr = ssh.exec_command(f"grep -rn 'localhost:8016' {remote_path}/static/*.js 2>/dev/null || echo 'SUCCESS: No localhost:8016 found'")
    print(stdout.read().decode('utf-8'))
    
    ssh.close()
    print("\nDone!")

if __name__ == "__main__":
    main()
