"""检查并修复部署问题"""
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
    print("检查并修复部署问题")
    print("=" * 60)
    
    try:
        # 1. 检查容器当前的sms_client.py是否有万能验证码
        print("\n[1/5] 检查容器内当前代码...")
        cmd = "docker exec sageai cat /app/utils/sms_client.py | grep -A3 '123456'"
        output, error = ssh_exec(cmd)
        if output:
            print("  ✅ 容器内有万能验证码逻辑")
            print(f"  {output.strip()}")
        else:
            print("  ❌ 容器内没有万能验证码逻辑")
            
        # 2. 检查容器的挂载方式
        print("\n[2/5] 检查容器挂载方式...")
        cmd = "docker inspect sageai | grep -A5 'Mounts'"
        output, error = ssh_exec(cmd)
        print(f"  {output.strip()[:300]}")
        
        # 3. 检查docker-compose.yml
        print("\n[3/5] 检查docker-compose.yml...")
        cmd = "cat /opt/sageai/docker-compose.yml 2>/dev/null || echo 'docker-compose.yml不存在'"
        output, error = ssh_exec(cmd)
        print(f"  {output.strip()[:500]}")
        
        # 4. 检查Dockerfile
        print("\n[4/5] 检查Dockerfile...")
        cmd = "cat /opt/sageai/Dockerfile 2>/dev/null || cat /opt/sageai/backend/Dockerfile 2>/dev/null || echo 'Dockerfile不存在'"
        output, error = ssh_exec(cmd)
        print(f"  {output.strip()[:500]}")
        
        # 5. 修复：重新构建镜像并启动
        print("\n[5/5] 重新构建镜像并启动...")
        cmd = "cd /opt/sageai && docker-compose build sageai && docker-compose up -d sageai"
        output, error = ssh_exec(cmd)
        print(f"  构建输出: {output.strip()[-500:]}")
        if error:
            print(f"  错误: {error.strip()[:300]}")
        
        # 等待启动
        print("\n[等待] 等待服务启动...")
        import time
        time.sleep(15)
        
        # 测试
        print("\n[测试] 测试注册接口...")
        cmd = '''curl -s -X POST http://localhost:8000/auth/register \
            -H "Content-Type: application/json" \
            -d '{"phone":"15680793860","sms_code":"123456","password":"test1234","confirm_password":"test1234"}' '''
        output, error = ssh_exec(cmd)
        print(f"  响应: {output.strip()}")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()