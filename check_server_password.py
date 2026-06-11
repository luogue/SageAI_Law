"""检查服务器上的用户密码"""
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
    print("检查服务器用户密码")
    print("=" * 60)
    
    try:
        # 1. 检查运行中的容器
        print("\n[1/3] 检查容器...")
        output, error = ssh_exec("docker ps --filter 'name=sageai'")
        print(output)
        
        # 2. 检查数据库中的用户
        print("\n[2/3] 检查数据库用户...")
        cmd = """docker exec sageai-backend python -c "
from storage.crud import get_user_by_mobile
u = get_user_by_mobile('15680793860')
if u:
    print(f'用户存在: {u.mobile}')
    print(f'密码哈希: {u.password_hash[:50]}')
else:
    print('用户不存在')
" """
        output, error = ssh_exec(cmd)
        print(output.strip())
        if error:
            print(f"错误: {error.strip()}")
        
        # 3. 如果容器不存在，直接检查服务器上的数据库
        print("\n[3/3] 直接检查服务器数据库...")
        cmd = """cd /opt/sageai && python -c "
import sys
sys.path.insert(0, 'backend')
from storage.crud import get_user_by_mobile
u = get_user_by_mobile('15680793860')
if u:
    print(f'用户存在: {u.mobile}')
    print(f'密码哈希: {u.password_hash[:50]}')
else:
    print('用户不存在')
" """
        output, error = ssh_exec(cmd)
        print(output.strip())
        if error:
            print(f"错误: {error.strip()[:200]}")
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()