"""检查Docker容器中实际运行的代码"""
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
    print("检查Docker容器中实际运行的代码")
    print("=" * 60)
    
    try:
        # 检查容器内的auth路由文件
        print("\n[1/2] 检查容器内的auth路由文件...")
        cmd = "docker exec sageai cat /app/backend/auth/routes.py | grep -n 'HTTPException.*422'"
        output, error = ssh_exec(cmd)
        print(output)
        if error:
            print(f"错误: {error}")
        
        # 检查容器内的文件内容
        print("\n[2/2] 检查登录函数代码...")
        cmd = "docker exec sageai cat /app/backend/auth/routes.py | head -n 240 | tail -n 50"
        output, error = ssh_exec(cmd)
        print(output)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()