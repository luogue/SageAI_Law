"""检查服务器部署状态"""
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
    print("检查服务器部署状态")
    print("=" * 60)
    
    try:
        # 1. 检查容器状态
        print("\n[1/4] 容器状态...")
        output, error = ssh_exec("docker ps -a")
        print(output)
        
        # 2. 检查服务健康状态
        print("\n[2/4] 服务健康检查...")
        output, error = ssh_exec("curl -s http://localhost:8000/health 2>/dev/null || echo '服务未响应'")
        print(f"  后端健康检查: {output.strip()}")
        
        # 3. 测试登录
        print("\n[3/4] 测试登录...")
        cmd = 'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"123456"}\''
        output, error = ssh_exec(cmd)
        print(f"  登录测试: {output.strip()}")
        
        # 4. 查看日志
        print("\n[4/4] 后端日志...")
        output, error = ssh_exec("docker logs sageai-backend 2>&1 | tail -30")
        print(output)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()