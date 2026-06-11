"""检查Docker容器的挂载情况"""
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
    print("检查Docker容器的挂载情况")
    print("=" * 60)
    
    try:
        # 检查容器的挂载情况
        print("\n[1/2] 检查容器挂载...")
        cmd = "docker inspect sageai | grep -A 10 'Mounts'"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 检查容器内的auth路由文件
        print("\n[2/2] 检查容器内的auth路由文件...")
        cmd = "docker exec sageai cat /app/auth/routes.py | grep -n 'HTTPException.*422'"
        output, error = ssh_exec(cmd)
        print(output)
        if error:
            print(f"错误: {error}")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()