"""检查运行中的容器"""
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
    print("检查运行中的容器")
    print("=" * 60)
    
    try:
        # 1. 查看运行中的容器
        print("\n[1/3] 查看运行中的容器...")
        cmd = "docker ps"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 2. 检查sageai容器内的sms_client.py
        print("\n[2/3] 检查sageai容器内的验证逻辑...")
        cmd = "docker exec sageai cat /app/utils/sms_client.py | grep -A2 '测试/开发模式'"
        output, error = ssh_exec(cmd)
        print("  " + output.strip())
        
        # 3. 在容器内直接测试验证函数
        print("\n[3/3] 在容器内测试验证函数...")
        cmd = "docker exec sageai python -c \"from utils.sms_client import sms_client; print(sms_client.verify_code('15680793860', '123456'))\""
        output, error = ssh_exec(cmd)
        print("  验证结果: " + output.strip())
        
    except Exception as e:
        print("\n[ERROR]: " + str(e))

if __name__ == "__main__":
    main()