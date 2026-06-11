"""上传代码到服务器"""
import os
import paramiko

def upload_files(local_path, remote_path, ssh_client):
    """上传目录到服务器"""
    sftp = ssh_client.open_sftp()
    
    for root, dirs, files in os.walk(local_path):
        # 排除不需要的目录
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.history', 'logs', 'data']]
        
        for file in files:
            # 排除不需要的文件
            if file.endswith('.pyc') or file == 'clean_users.py' or file == 'app.db' or file == 'sql_app.db':
                continue
            
            local_file = os.path.join(root, file)
            relative_path = os.path.relpath(local_file, local_path)
            remote_file = os.path.join(remote_path, relative_path).replace('\\', '/')
            
            # 确保远程目录存在
            remote_dir = os.path.dirname(remote_file)
            try:
                sftp.stat(remote_dir)
            except FileNotFoundError:
                # 递归创建目录
                current_dir = ''
                for part in remote_dir.split('/'):
                    if part:
                        current_dir += '/' + part
                        try:
                            sftp.stat(current_dir)
                        except FileNotFoundError:
                            sftp.mkdir(current_dir)
            
            print(f"上传: {local_file} -> {remote_file}")
            sftp.put(local_file, remote_file)
    
    sftp.close()

def main():
    server = "120.77.171.21"
    port = 22
    username = "root"
    password = "!1iIlL.,44166"
    local_path = r"f:\ai\Sage\backend"
    remote_path = "/opt/sageai"
    
    print(f"连接到服务器 {server}:{port}...")
    
    try:
        # 创建 SSH 连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port, username, password, timeout=10)
        
        # 创建远程目录
        stdin, stdout, stderr = ssh.exec_command(f"mkdir -p {remote_path}")
        stdout.channel.recv_exit_status()
        
        print(f"上传代码到 {remote_path}...")
        upload_files(local_path, remote_path, ssh)
        
        # 验证上传结果
        print("\n验证上传结果:")
        stdin, stdout, stderr = ssh.exec_command(f"ls -la {remote_path}/")
        print(stdout.read().decode('utf-8'))
        
        ssh.close()
        print("\n上传完成！")
        
    except Exception as e:
        print(f"上传失败: {e}")

if __name__ == "__main__":
    main()
