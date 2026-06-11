"""检查容器内的验证码验证代码"""
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
    print("检查容器内的验证码验证代码")
    print("=" * 60)
    
    try:
        # 检查容器内的sms_client.py
        print("\n[1/2] 检查容器内的sms_client.py...")
        cmd = "docker exec sageai cat /app/utils/sms_client.py | grep -A 5 '万能验证码'"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 检查容器内的代码是否包含万能验证码逻辑
        print("\n[2/2] 检查万能验证码逻辑...")
        cmd = "docker exec sageai grep -c '123456' /app/utils/sms_client.py"
        output, error = ssh_exec(cmd)
        print(f"123456出现次数: {output.strip()}")
        
        # 直接检查代码内容
        cmd = "docker exec sageai sed -n '123,127p' /app/utils/sms_client.py"
        output, error = ssh_exec(cmd)
        print(f"第123-127行内容:\n{output}")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()