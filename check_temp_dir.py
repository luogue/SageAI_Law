"""检查服务器临时目录"""
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
    print("检查服务器临时目录")
    print("=" * 60)
    
    try:
        # 检查临时目录
        print("\n[1/3] 检查临时目录...")
        output, error = ssh_exec("ls -la /tmp/frontend_dist/static/ 2>/dev/null | head -n 20")
        print(output)
        
        # 检查Home文件
        print("\n[2/3] 检查Home文件...")
        output, error = ssh_exec("ls /tmp/frontend_dist/static/Home*.js 2>/dev/null")
        print(output)
        
        # 检查user_id
        print("\n[3/3] 检查user_id...")
        output, error = ssh_exec("grep -c 'user_id' /tmp/frontend_dist/static/*.js 2>/dev/null || echo '0'")
        print(output)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()