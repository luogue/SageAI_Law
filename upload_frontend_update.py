"""上传更新后的前端构建文件到服务器"""
import os
import paramiko

def upload_directory(local_path, remote_path, ssh_client):
    """上传目录到服务器"""
    sftp = ssh_client.open_sftp()
    
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file = os.path.join(root, file)
            relative_path = os.path.relpath(local_file, local_path)
            remote_file = os.path.join(remote_path, relative_path).replace('\\', '/')
            
            # 确保远程目录存在
            remote_dir = os.path.dirname(remote_file)
            try:
                sftp.stat(remote_dir)
            except FileNotFoundError:
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
    local_path = r"f:\ai\Sage\frontend\dist"
    remote_path = "/opt/sageai/frontend"
    
    print(f"连接到服务器 {server}:{port}...")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port, username, password, timeout=10)
        
        print(f"上传更新后的前端构建文件到 {remote_path}...")
        upload_directory(local_path, remote_path, ssh)
        
        # 验证上传结果
        print("\n验证上传结果:")
        stdin, stdout, stderr = ssh.exec_command(f"ls -la {remote_path}/")
        print(stdout.read().decode('utf-8'))
        
        # 验证 API 地址是否已改为相对路径
        print("\n验证 API 地址配置:")
        stdin, stdout, stderr = ssh.exec_command(f"grep -E 'localhost:8016' {remote_path}/static/*.js || echo '✓ 未找到 localhost:8016，配置已更新'")
        print(stdout.read().decode('utf-8'))
        
        ssh.close()
        print("\n前端文件更新上传完成！")
        
    except Exception as e:
        print(f"上传失败: {e}")

if __name__ == "__main__":
    main()
