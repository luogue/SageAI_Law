"""检查验证码验证逻辑"""
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
    print("检查验证码验证逻辑")
    print("=" * 60)
    
    try:
        # 测试验证码验证
        print("\n[1/2] 测试验证码验证...")
        cmd = """docker exec sageai python -c "
from utils.sms_client import sms_client
result = sms_client.verify_code('15680793860', '123456')
print(f'验证码123456验证结果: {result}')
result2 = sms_client.verify_code('15680793860', '111111')
print(f'验证码111111验证结果: {result2}')
" """
        output, error = ssh_exec(cmd)
        print(output)
        if error:
            print(f"错误: {error}")
        
        # 检查日志
        print("\n[2/2] 检查最近的注册日志...")
        cmd = "docker exec sageai tail -n 20 /app/logs/app_*.log 2>/dev/null | grep -i '验证码\\|register\\|sms'"
        output, error = ssh_exec(cmd)
        print(output[:1000] if output else "无相关日志")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()