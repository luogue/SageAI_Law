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
            print("  OK: 容器内有万能验证码逻辑")
            print("  " + output.strip())
        else:
            print("  ERROR: 容器内没有万能验证码逻辑")
            
        # 2. 检查docker-compose.yml
        print("\n[2/5] 检查docker-compose.yml...")
        cmd = "cat /opt/sageai/docker-compose.yml 2>/dev/null || echo 'docker-compose.yml不存在'"
        output, error = ssh_exec(cmd)
        print("  " + output.strip()[:500])
        
        # 3. 确保宿主机的sms_client.py是正确的
        print("\n[3/5] 确保宿主机的sms_client.py是正确的...")
        cmd = "grep -A3 '123456' /opt/sageai/backend/utils/sms_client.py"
        output, error = ssh_exec(cmd)
        print("  " + output.strip())
        
        # 4. 重新构建镜像并启动
        print("\n[4/5] 重新构建镜像并启动...")
        cmd = "cd /opt/sageai && docker-compose build sageai 2>&1"
        output, error = ssh_exec(cmd)
        print("  构建输出: " + output.strip()[-300:])
        if error:
            print("  错误: " + error.strip()[:300])
        
        cmd = "cd /opt/sageai && docker-compose up -d sageai"
        output, error = ssh_exec(cmd)
        print("  启动输出: " + output.strip())
        
        # 等待启动
        print("\n[5/5] 等待服务启动...")
        import time
        time.sleep(15)
        
        # 测试
        print("\n[TEST] 测试注册接口...")
        cmd = 'curl -s -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d "{\\\"phone\\\":\\\"15680793860\\\",\\\"sms_code\\\":\\\"123456\\\",\\\"password\\\":\\\"test1234\\\",\\\"confirm_password\\\":\\\"test1234\\\"}"'
        output, error = ssh_exec(cmd)
        print("  响应: " + output.strip())
        
        print("\n" + "=" * 60)
        print("修复完成")
        print("=" * 60)
        
    except Exception as e:
        print("\n[ERROR]: " + str(e))

if __name__ == "__main__":
    main()