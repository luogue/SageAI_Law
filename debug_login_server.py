"""在服务器上调试登录函数"""
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
    print("在服务器上调试登录函数")
    print("=" * 60)
    
    try:
        # 直接调用登录函数测试
        print("\n[1/2] 直接调用登录函数...")
        cmd = """docker exec sageai python -c "
import sys
sys.path.insert(0, '/app/backend')

from fastapi import HTTPException
from auth.routes import login
from pydantic import BaseModel

class MockRequest:
    phone = '+8615680793860'
    password = 'wrongpassword'

class MockReq:
    class Client:
        host = '127.0.0.1'
    client = Client()

try:
    result = login(MockRequest(), MockReq())
    print(f'成功: {result}')
except HTTPException as e:
    print(f'HTTPException: status_code={e.status_code}, detail={e.detail}')
except Exception as e:
    print(f'其他异常: {type(e).__name__}: {e}')
" """
        output, error = ssh_exec(cmd)
        print(output)
        if error:
            print(f"错误: {error}")
        
        # 检查路由是否正确注册
        print("\n[2/2] 检查路由注册...")
        cmd = "docker exec sageai python -c \"from auth.routes import router; print([r.path for r in router.routes])\""
        output, error = ssh_exec(cmd)
        print(output)
        if error:
            print(f"错误: {error}")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()