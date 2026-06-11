"""验证前端API地址是否已更新"""
import paramiko

server = "120.77.171.21"
port = 22
username = "root"
password = "!1iIlL.,44166"

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, port, username, password, timeout=10)
    
    print("=== 验证前端文件 ===")
    stdin, stdout, stderr = ssh.exec_command("ls -la /opt/sageai/frontend/")
    print(stdout.read().decode('utf-8'))
    
    print("=== 检查是否存在旧的localhost:8016配置 ===")
    stdin, stdout, stderr = ssh.exec_command("grep -rn 'localhost:8016' /opt/sageai/frontend/ 2>/dev/null || echo '✓ 成功：未找到 localhost:8016'")
    output = stdout.read().decode('utf-8')
    print(output)
    
    if "localhost:8016" not in output:
        print("✓ 前端API地址已成功更新为相对路径！")
    else:
        print("✗ 仍然存在 localhost:8016 配置")
    
    ssh.close()
    
except Exception as e:
    print(f"连接失败: {e}")
