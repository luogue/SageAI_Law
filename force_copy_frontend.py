"""强制删除并重新复制前端文件"""
import paramiko
import os

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
LOCAL_DIST = "f:/ai/Sage/frontend/dist"

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
    print("强制删除并重新复制前端文件")
    print("=" * 60)
    
    try:
        # 1. 强制删除容器内的前端目录
        print("\n[1/5] 强制删除容器内的前端目录...")
        output = ssh_exec("docker exec rm -rf /app/frontend")
        print(f"  {output}")
        
        # 2. 重新创建目录
        print("\n[2/5] 重新创建目录...")
        output = ssh_exec("docker exec sageai mkdir -p /app/frontend/static")
        print(f"  {output}")
        
        # 3. 复制文件到容器
        print("\n[3/5] 复制文件到容器...")
        output = ssh_exec("docker cp /tmp/frontend_dist/. sageai:/app/frontend/")
        print(f"  {output}")
        
        # 4. 验证
        print("\n[4/5] 验证文件...")
        output = ssh_exec("docker exec sageai ls /app/frontend/")
        print(f"  目录: {output}")
        
        output = ssh_exec("docker exec sageai ls /app/frontend/static/ | head -n 10")
        print(f"  文件: {output}")
        
        # 5. 检查 Home 文件内容
        print("\n[5/5] 检查 Home 文件内容...")
        output = ssh_exec("docker exec sageai grep -l 'user_id' /app/frontend/static/*.js 2>/dev/null || echo '未找到'")
        print(f"  {output}")
        
        print("\n" + "=" * 60)
        print("前端文件已重新复制！")
        print("请强制刷新浏览器 (Ctrl+F5)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()