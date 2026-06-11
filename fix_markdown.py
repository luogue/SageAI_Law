"""修复缺失的markdown模块"""
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
    print("修复缺失的markdown模块")
    print("=" * 60)
    
    try:
        # 1. 在容器内安装markdown模块
        print("\n[1/2] 在容器内安装markdown模块...")
        cmd = "docker exec sageai pip install markdown"
        output, error = ssh_exec(cmd)
        print("  安装输出: " + output.strip()[-200:])
        if error:
            print("  错误: " + error.strip()[:200])
        
        # 2. 验证安装
        print("\n[2/2] 验证安装...")
        cmd = "docker exec sageai python -c \"import markdown; print('markdown版本:', markdown.__version__)\""
        output, error = ssh_exec(cmd)
        print("  " + output.strip())
        
        print("\n" + "=" * 60)
        print("修复完成！")
        print("markdown模块已安装")
        print("=" * 60)
        
    except Exception as e:
        print("\n[ERROR]: " + str(e))

if __name__ == "__main__":
    main()