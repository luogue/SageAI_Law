"""检查index.html引用的文件"""
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
    print("检查index.html引用的文件")
    print("=" * 60)
    
    try:
        # 检查index.html
        print("\n[1/2] 检查index.html...")
        output, error = ssh_exec("docker exec sageai cat /app/frontend/index.html")
        print(output)
        
        # 检查Home文件内容
        print("\n[2/2] 检查Home-CWdjUCM-.js内容...")
        output, error = ssh_exec("docker exec sageai grep 'user_id' /app/frontend/static/Home-CWdjUCM-.js 2>/dev/null || echo '未找到user_id'")
        print(output)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()