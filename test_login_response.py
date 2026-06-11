"""测试登录返回的数据格式"""
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
    print("测试登录返回的数据格式")
    print("=" * 60)
    
    try:
        # 测试登录接口返回的数据
        print("\n[1/1] 测试登录接口...")
        cmd = 'curl -s -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"a.144iLil123"}\''
        output, error = ssh_exec(cmd)
        print(f"登录响应: {output.strip()}")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()