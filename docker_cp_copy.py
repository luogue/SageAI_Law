"""使用docker cp复制文件到容器"""
import paramiko
import os

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"

def ssh_exec(cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=60)
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')
    finally:
        ssh.close()

def main():
    print("=" * 60)
    print("使用docker cp复制文件到容器")
    print("=" * 60)
    
    try:
        # 1. 清空容器内的前端目录
        print("\n[1/4] 清空容器内的前端目录...")
        output, error = ssh_exec("docker exec sageai rm -rf /app/frontend/* && docker exec sageai mkdir -p /app/frontend/static")
        print("  [OK]")
        
        # 2. 复制到容器
        print("\n[2/4] 复制到容器...")
        output, error = ssh_exec("docker cp /app/frontend/. sageai:/app/frontend/")
        print(f"  {output if output else '[OK]'}")
        if error:
            print(f"  错误: {error}")
        
        # 等待复制完成
        print("\n[3/4] 等待复制完成...")
        import time
        time.sleep(2)
        
        # 3. 验证
        print("\n[4/4] 验证文件...")
        output, error = ssh_exec("docker exec sageai ls /app/frontend/static/*.js | wc -l")
        count = output.strip()
        print(f"  JS文件数量: {count}")
        
        output, error = ssh_exec("docker exec sageai ls /app/frontend/static/*.js 2>/dev/null")
        print(f"  文件列表: {output.strip()}")
        
        output, error = ssh_exec("docker exec sageai grep -c 'user_id' /app/frontend/static/*.js 2>/dev/null || echo '0'")
        print(f"  包含user_id: {output.strip()}")
        
        print("\n" + "=" * 60)
        print("文件复制完成！")
        print("请强制刷新浏览器 (Ctrl+F5)")
        print("然后重新登录！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    main()