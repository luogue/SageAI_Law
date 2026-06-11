"""调试部署脚本"""
import paramiko

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"

def ssh_exec(cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=30)
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')
    finally:
        ssh.close()

def main():
    print("=" * 60)
    print("调试部署问题")
    print("=" * 60)
    
    # 1. 检查项目目录
    print("\n[1/5] 项目目录结构...")
    output, error = ssh_exec("ls -la /opt/sageai/")
    print(output)
    
    # 2. 检查 Dockerfile
    print("\n[2/5] Dockerfile.backend 内容...")
    output, error = ssh_exec("cat /opt/sageai/Dockerfile.backend")
    print(output[:500])
    
    # 3. 检查构建日志
    print("\n[3/5] 构建后端镜像...")
    cmd = "cd /opt/sageai && docker build -t sageai-backend:test -f Dockerfile.backend . 2>&1"
    output, error = ssh_exec(cmd)
    print(output)
    
    # 4. 查看镜像列表
    print("\n[4/5] 镜像列表...")
    output, error = ssh_exec("docker images | head -20")
    print(output)
    
    # 5. 启动容器并查看日志
    print("\n[5/5] 启动测试容器...")
    cmd = "docker run -d --name sageai-test -p 8001:8000 sageai-backend:test"
    output, error = ssh_exec(cmd)
    print(f"  容器ID: {output.strip()}")
    
    import time
    time.sleep(10)
    
    output, error = ssh_exec("docker logs sageai-test 2>&1 | tail -50")
    print(f"\n  容器日志:\n{output}")
    
    output, error = ssh_exec("docker inspect sageai-test --format '{{.State.Status}}'")
    print(f"\n  容器状态: {output.strip()}")

if __name__ == "__main__":
    main()