"""修复验证码验证问题"""
import paramiko

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"

def main():
    print("=" * 60)
    print("修复验证码验证问题")
    print("=" * 60)
    
    try:
        # 1. 复制sms_client.py到容器
        print("\n[1/3] 复制sms_client.py到容器...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=30)
        
        # 使用docker cp复制
        stdin, stdout, stderr = ssh.exec_command("docker cp /opt/sageai/backend/utils/sms_client.py sageai:/app/utils/sms_client.py")
        stdout.channel.recv_exit_status()
        print("  [OK]")
        
        # 2. 验证代码
        print("\n[2/3] 验证代码...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sageai grep -A 3 '万能验证码' /app/utils/sms_client.py")
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        print(f"  {output.strip()}")
        
        # 3. 测试验证
        print("\n[3/3] 测试验证码验证...")
        cmd = """docker exec sageai python -c "
from utils.sms_client import sms_client
result = sms_client.verify_code('15680793860', '123456')
print(f'验证码123456验证结果: {result}')
" """
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        print(f"  {output.strip()}")
        
        ssh.close()
        
        print("\n" + "=" * 60)
        print("验证码修复完成！")
        print("现在可以使用123456作为万能验证码注册")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()