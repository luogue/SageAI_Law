"""检查服务器上的后端代码"""
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
    print("检查服务器上的后端代码")
    print("=" * 60)
    
    try:
        # 检查登录路由
        print("\n[1/2] 检查登录路由代码...")
        cmd = "cat /opt/sageai/backend/auth/routes.py | head -n 240 | tail -n 50"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 检查main.py中的异常处理
        print("\n[2/2] 检查main.py中的异常处理...")
        cmd = "grep -n 'exception_handler\|HTTPException.*400\|HTTPException.*422' /opt/sageai/backend/main.py | head -n 20"
        output, error = ssh_exec(cmd)
        print(output)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()