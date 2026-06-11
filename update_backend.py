"""更新后端代码并重启服务"""
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

def upload_file(local_path, remote_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=30)
    try:
        sftp = ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        return True
    finally:
        ssh.close()

def main():
    print("=" * 60)
    print("更新后端代码并重启服务")
    print("=" * 60)
    
    try:
        # 1. 上传更新后的路由文件
        print("\n[1/3] 上传更新后的路由文件...")
        local_file = "f:/ai/Sage/backend/auth/routes.py"
        remote_file = "/opt/sageai/backend/auth/routes.py"
        if upload_file(local_file, remote_file):
            print(f"  [OK] {remote_file}")
        
        # 2. 重启容器
        print("\n[2/3] 重启容器...")
        output, error = ssh_exec("docker restart sageai")
        print(f"  {output.strip()}")
        if error:
            print(f"  警告: {error.strip()}")
        
        # 3. 等待服务启动
        print("\n[3/3] 等待服务启动...")
        import time
        time.sleep(10)
        
        # 测试登录接口
        print("\n[4/4] 测试登录接口...")
        cmd = 'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"wrongpassword"}\''
        output, error = ssh_exec(cmd)
        print(f"  错误密码测试: {output.strip()}")
        
        cmd = 'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"a.144iLil123"}\''
        output, error = ssh_exec(cmd)
        print(f"  正确密码测试: {output.strip()}")
        
        print("\n" + "=" * 60)
        print("后端更新完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()