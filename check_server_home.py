"""检查服务器容器内的Home文件"""
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
    print("检查服务器容器内的Home文件")
    print("=" * 60)
    
    try:
        # 列出容器内的static文件
        print("\n[1/2] 容器内的static文件...")
        cmd = "docker exec sageai ls -la /app/frontend/static/"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 检查Home文件中是否有localStorage.getItem user_id
        print("\n[2/2] 检查Home文件中的user_id...")
        cmd = "docker exec sageai grep 'user_id' /app/frontend/static/*.js"
        output, error = ssh_exec(cmd)
        print(output if output else "未找到")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()