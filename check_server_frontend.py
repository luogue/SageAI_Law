"""检查服务器上容器内的前端代码"""
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
    print("检查服务器上容器内的前端代码")
    print("=" * 60)
    
    try:
        # 检查容器内的前端代码
        print("\n[1/3] 检查容器内前端目录...")
        cmd = "docker exec sageai ls -la /app/frontend/"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 检查邀请链接相关代码
        print("\n[2/3] 检查邀请链接代码...")
        cmd = "docker exec sageai grep -r 'handleInvite' /app/frontend/ 2>/dev/null || echo '未找到'"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 检查容器内的前端文件挂载情况
        print("\n[3/3] 检查前端文件来源...")
        cmd = "docker exec sageai cat /app/frontend/static/index-CQ_afnkE.js 2>/dev/null | grep -A 10 'handleInvite' | head -n 20 || echo '文件不存在或未找到'"
        output, error = ssh_exec(cmd)
        print(output[:1000] if output else "未找到")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()