"""给服务器上的用户增加额度"""
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
    print("给用户15680793860增加100个额度")
    print("=" * 60)
    
    try:
        # 在服务器容器中增加额度
        print("\n[1/2] 在容器中增加额度...")
        cmd = """docker exec sageai python -c "
from storage.crud import get_user_by_mobile, add_user_bonus_credits
u = get_user_by_mobile('15680793860')
if u:
    before = u.bonus_credits
    new_credits = add_user_bonus_credits(u.id, 100)
    print(f'用户 {u.mobile} 额度变更: {before} -> {new_credits} (+100)')
else:
    print('用户不存在')
" """
        output, error = ssh_exec(cmd)
        print(output.strip())
        if error:
            print(f"错误: {error.strip()}")
        
        # 验证额度
        print("\n[2/2] 验证额度...")
        cmd = """docker exec sageai python -c "
from storage.crud import get_user_by_mobile
u = get_user_by_mobile('15680793860')
if u:
    print(f'用户 {u.mobile} 当前额度: {u.bonus_credits}')
else:
    print('用户不存在')
" """
        output, error = ssh_exec(cmd)
        print(output.strip())
        
        print("\n" + "=" * 60)
        print("额度增加完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()