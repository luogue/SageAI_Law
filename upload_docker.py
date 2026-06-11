"""上传 Docker 配置文件到服务器"""
import paramiko

def main():
    server = "120.77.171.21"
    port = 22
    username = "root"
    password = "!1iIlL.,44166"
    remote_path = "/opt/sageai"
    
    # 需要上传的 Docker 文件
    docker_files = [
        "docker-compose.yml",
        "Dockerfile.backend", 
        "Dockerfile.frontend",
        "nginx.conf"
    ]
    
    print(f"连接到服务器 {server}:{port}...")
    
    try:
        # 创建 SSH 连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port, username, password, timeout=10)
        
        sftp = ssh.open_sftp()
        
        for file_name in docker_files:
            local_path = f"f:/ai/Sage/{file_name}"
            remote_file = f"{remote_path}/{file_name}"
            
            print(f"上传: {file_name}")
            sftp.put(local_path, remote_file)
        
        sftp.close()
        
        # 验证上传结果
        print("\n验证 Docker 文件:")
        stdin, stdout, stderr = ssh.exec_command(f"ls -la {remote_path}/*.yml {remote_path}/*.backend {remote_path}/*.frontend {remote_path}/nginx.conf")
        print(stdout.read().decode('utf-8'))
        
        ssh.close()
        print("\nDocker 配置文件上传完成！")
        
    except Exception as e:
        print(f"上传失败: {e}")

if __name__ == "__main__":
    main()
