"""SageAI 最终部署脚本"""
import paramiko
import os

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
PROJECT_DIR = "/opt/sageai"
LOCAL_BASE = "f:/ai/Sage"

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
    print("SageAI 最终部署")
    print("=" * 60)
    
    try:
        # 1. 上传修复的 docker-compose.yml
        print("\n[1/5] 上传配置文件...")
        with open(os.path.join(LOCAL_BASE, "docker-compose.yml"), 'r', encoding='utf-8') as f:
            content = f.read()
        
        import base64
        encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        cmd = f"echo '{encoded}' | base64 -d > {PROJECT_DIR}/docker-compose.yml"
        ssh_exec(cmd)
        print("  [OK] docker-compose.yml")
        
        # 2. 上传更新的后端文件
        print("\n[2/5] 上传后端文件...")
        files_to_copy = [
            ("backend/auth/routes.py", "auth/routes.py"),
            ("backend/utils/sms_client.py", "utils/sms_client.py"),
            ("backend/storage/crud.py", "storage/crud.py"),
            ("backend/reset_password.py", "reset_password.py"),
        ]
        
        for local, remote in files_to_copy:
            local_full = os.path.join(LOCAL_BASE, local)
            with open(local_full, 'rb') as f:
                content = f.read()
            
            encoded = base64.b64encode(content).decode('utf-8')
            remote_full = f"{PROJECT_DIR}/{remote}"
            cmd = f"echo '{encoded}' | base64 -d > '{remote_full}'"
            ssh_exec(cmd)
            print(f"  [OK] {local}")
        
        # 3. 启动服务
        print("\n[3/5] 启动服务...")
        cmd = f"cd {PROJECT_DIR} && docker-compose up -d"
        output, error = ssh_exec(cmd)
        print(f"  启动结果: {output.strip()[:300] or error.strip()[:300]}")
        
        # 4. 等待启动
        import time
        print("\n[4/5] 等待服务启动 (25秒)...")
        time.sleep(25)
        
        # 5. 测试服务
        print("\n[5/5] 测试服务...")
        cmd = "curl -s http://localhost:8000/health"
        output, error = ssh_exec(cmd)
        print(f"  健康检查: {output.strip() or error.strip()}")
        
        cmd = "docker exec sageai-backend python /app/reset_password.py 15680793860 123456"
        output, error = ssh_exec(cmd)
        print(f"  密码重置: {output.strip() or error.strip()}")
        
        cmd = 'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"123456"}\''
        output, error = ssh_exec(cmd)
        print(f"  登录测试: {output.strip()}")
        
        print("\n" + "=" * 60)
        print("部署完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] 部署失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()