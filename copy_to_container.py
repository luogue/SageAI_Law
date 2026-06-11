"""将修改后的代码复制到Docker容器内"""
import paramiko

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"

def main():
    print("=" * 60)
    print("将修改后的代码复制到Docker容器内")
    print("=" * 60)
    
    try:
        # 使用docker cp命令复制文件到容器
        print("\n[1/2] 复制auth路由文件到容器...")
        cmd = "docker cp /opt/sageai/backend/auth/routes.py sageai:/app/auth/routes.py"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=30)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        print(f"  输出: {output}")
        if error:
            print(f"  错误: {error}")
        else:
            print("  [OK] 文件复制成功")
        
        # 重启容器
        print("\n[2/2] 重启容器...")
        stdin, stdout, stderr = ssh.exec_command("docker restart sageai")
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        print(f"  {output.strip()}")
        
        # 等待服务启动
        print("\n[3/3] 等待服务启动...")
        import time
        time.sleep(10)
        
        # 测试登录接口
        print("\n[4/4] 测试登录接口...")
        cmd = 'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"wrongpassword"}\''
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        print(f"  错误密码测试: {output.strip()}")
        
        cmd = 'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"a.144iLil123"}\''
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        print(f"  正确密码测试: {output.strip()}")
        
        ssh.close()
        
        print("\n" + "=" * 60)
        print("代码更新完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()