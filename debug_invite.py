"""调试邀请链接功能"""
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
    print("调试邀请链接功能")
    print("=" * 60)
    
    try:
        # 检查容器内的代码
        print("\n[1/2] 检查容器内的邀请链接代码...")
        cmd = "docker exec sageai cat /app/frontend/static/*.js 2>/dev/null | grep -A 5 'handleInvite' | head -n 20"
        output, error = ssh_exec(cmd)
        print(output[:500] if output else "未找到")
        
        # 检查前端HTML中的配置
        print("\n[2/2] 检查前端HTML...")
        cmd = "cat /opt/sageai/frontend/index.html"
        output, error = ssh_exec(cmd)
        print(output)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()