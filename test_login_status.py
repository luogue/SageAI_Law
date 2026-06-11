"""测试登录接口状态码"""
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
    print("测试登录接口状态码")
    print("=" * 60)
    
    try:
        # 使用详细的curl命令测试
        print("\n[1/2] 测试错误密码（期望422）...")
        cmd = '''curl -v -X POST http://localhost:8000/auth/login \
            -H "Content-Type: application/json" \
            -d '{"phone":"+8615680793860","password":"wrongpassword"}' 2>&1 | grep -E "(HTTP/1.1|HTTP/2|status|400|422|detail)"'''
        output, error = ssh_exec(cmd)
        print(output)
        
        print("\n[2/2] 测试正确密码（期望200）...")
        cmd = '''curl -v -X POST http://localhost:8000/auth/login \
            -H "Content-Type: application/json" \
            -d '{"phone":"+8615680793860","password":"a.144iLil123"}' 2>&1 | grep -E "(HTTP/1.1|HTTP/2|status|200|access_token)"'''
        output, error = ssh_exec(cmd)
        print(output)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()