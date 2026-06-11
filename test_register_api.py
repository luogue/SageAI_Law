"""测试注册接口"""
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
    print("测试注册接口")
    print("=" * 60)
    
    try:
        # 1. 测试不同格式的手机号
        print("\n[1/3] 测试不带区号的手机号...")
        cmd = 'curl -s -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d "{\\\"phone\\\":\\\"15680793860\\\",\\\"sms_code\\\":\\\"123456\\\",\\\"password\\\":\\\"test1234\\\",\\\"confirm_password\\\":\\\"test1234\\\"}"'
        output, error = ssh_exec(cmd)
        print("  响应: " + output.strip())
        
        print("\n[2/3] 测试带+86区号的手机号...")
        cmd = 'curl -s -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d "{\\\"phone\\\":\\\"+8615680793860\\\",\\\"sms_code\\\":\\\"123456\\\",\\\"password\\\":\\\"test1234\\\",\\\"confirm_password\\\":\\\"test1234\\\"}"'
        output, error = ssh_exec(cmd)
        print("  响应: " + output.strip())
        
        # 2. 检查uvicorn进程是否需要重启
        print("\n[3/3] 检查uvicorn进程...")
        cmd = "docker exec sageai ps aux | grep uvicorn"
        output, error = ssh_exec(cmd)
        print("  " + output.strip())
        
        # 3. 重启容器
        print("\n[4/3] 重启容器以加载新代码...")
        cmd = "docker restart sageai"
        output, error = ssh_exec(cmd)
        print("  " + output.strip())
        
        # 等待启动
        print("\n[等待] 等待服务启动...")
        import time
        time.sleep(15)
        
        # 再次测试
        print("\n[重新测试] 测试注册接口...")
        cmd = 'curl -s -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d "{\\\"phone\\\":\\\"15680793860\\\",\\\"sms_code\\\":\\\"123456\\\",\\\"password\\\":\\\"test1234\\\",\\\"confirm_password\\\":\\\"test1234\\\"}"'
        output, error = ssh_exec(cmd)
        print("  响应: " + output.strip())
        
    except Exception as e:
        print("\n[ERROR]: " + str(e))

if __name__ == "__main__":
    main()