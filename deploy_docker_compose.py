"""SageAI 部署脚本（使用 docker compose）"""
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
    print("SageAI 部署（使用 docker compose）")
    print("=" * 60)
    
    try:
        # 1. 检查 docker compose 命令
        print("\n[1/6] 检查 Docker Compose...")
        output, error = ssh_exec("docker compose version")
        if "version" in output.lower():
            compose_cmd = "docker compose"
            print(f"  [OK] 使用: {compose_cmd}")
        else:
            compose_cmd = "docker-compose"
            print(f"  [WARN] 降级到: {compose_cmd}")
        
        # 2. 创建 .env.production
        print("\n[2/6] 创建 .env.production...")
        output, error = ssh_exec(f"cat {PROJECT_DIR}/.env")
        prod_env = output + "\nENV=production\nLOG_LEVEL=INFO\n"
        import base64
        encoded = base64.b64encode(prod_env.encode('utf-8')).decode('utf-8')
        cmd = f"echo '{encoded}' | base64 -d > {PROJECT_DIR}/.env.production"
        ssh_exec(cmd)
        print("  [OK] .env.production 已创建")
        
        # 3. 上传配置文件
        print("\n[3/6] 上传配置文件...")
        with open(os.path.join(LOCAL_BASE, "docker-compose.yml"), 'r', encoding='utf-8') as f:
            content = f.read()
        encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        cmd = f"echo '{encoded}' | base64 -d > {PROJECT_DIR}/docker-compose.yml"
        ssh_exec(cmd)
        print("  [OK] docker-compose.yml")
        
        # 4. 上传后端文件
        print("\n[4/6] 上传后端文件...")
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
            cmd = f"echo '{encoded}' | base64 -d > '{PROJECT_DIR}/{remote}'"
            ssh_exec(cmd)
            print(f"  [OK] {local}")
        
        # 5. 启动服务
        print("\n[5/6] 启动服务...")
        cmd = f"cd {PROJECT_DIR} && {compose_cmd} up -d"
        output, error = ssh_exec(cmd)
        print(f"  启动结果: {output.strip()[:500] or error.strip()[:500]}")
        
        # 6. 等待并测试
        import time
        print("\n[6/6] 等待服务启动 (35秒)...")
        time.sleep(35)
        
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