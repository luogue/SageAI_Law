"""在服务器上创建用户并设置密码"""
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
    print("在服务器上创建用户")
    print("=" * 60)
    
    try:
        # 创建用户并设置密码
        print("\n[1/2] 创建用户并设置密码...")
        cmd = """docker exec sageai python -c "
from storage.crud import create_user
from auth.utils import hash_password
user = create_user('15680793860', hash_password('a.144iLil123'))
print(f'用户创建成功: {user.mobile}')
" """
        output, error = ssh_exec(cmd)
        print(output.strip())
        if error:
            print(f"错误: {error.strip()}")
        
        # 验证用户创建成功
        print("\n[2/2] 验证用户并测试登录...")
        cmd = """docker exec sageai python -c "
from storage.crud import get_user_by_mobile
u = get_user_by_mobile('15680793860')
if u:
    print(f'用户存在: {u.mobile}')
else:
    print('用户不存在')
" """
        output, error = ssh_exec(cmd)
        print(output.strip())
        
        # 测试登录
        cmd = 'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"a.144iLil123"}\''
        output, error = ssh_exec(cmd)
        print(f"登录测试: {output.strip()}")
        
        print("\n" + "=" * 60)
        print("用户创建完成！")
        print("密码: a.144iLil123")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()