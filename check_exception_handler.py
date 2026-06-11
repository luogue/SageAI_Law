"""检查服务器上的异常处理器配置"""
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
    print("检查异常处理器配置")
    print("=" * 60)
    
    try:
        # 检查main.py中的异常处理器
        print("\n[1/3] 搜索异常处理器...")
        cmd = "grep -rn 'exception_handler\|@app.exception' /opt/sageai/backend/"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 检查是否有自定义的异常处理
        print("\n[2/3] 检查FastAPI应用配置...")
        cmd = "grep -n 'app = FastAPI\|app.add_exception_handler' /opt/sageai/backend/main.py"
        output, error = ssh_exec(cmd)
        print(output)
        
        # 检查服务器上的auth路由是否正确
        print("\n[3/3] 检查auth路由中的HTTPException状态码...")
        cmd = "grep -n 'HTTPException.*422' /opt/sageai/backend/auth/routes.py"
        output, error = ssh_exec(cmd)
        print(output)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()