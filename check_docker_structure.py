"""检查Docker容器内的文件结构"""
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
    print("检查Docker容器内的文件结构")
    print("=" * 60)
    
    try:
        # 检查容器内的目录结构
        print("\n[1/2] 检查容器内的目录结构...")
        cmd = "docker exec sageai ls -la /"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 查找auth目录
        print("\n[2/2] 查找auth目录...")
        cmd = "docker exec sageai find / -name 'auth' -type d 2>/dev/null"
        output, error = ssh_exec(cmd)
        print(output)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()