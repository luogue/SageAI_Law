"""SageAI 部署脚本（直接使用 Docker 命令）"""
import paramiko
import os

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
PROJECT_DIR = "/opt/sageai"

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
    print("SageAI 部署（直接 Docker 命令）")
    print("=" * 60)
    
    try:
        # 1. 停止旧容器
        print("\n[1/5] 停止旧容器...")
        ssh_exec("docker stop sageai-backend sageai-frontend 2>/dev/null || true")
        ssh_exec("docker rm sageai-backend sageai-frontend 2>/dev/null || true")
        print("  [OK] 旧容器已停止")
        
        # 2. 创建网络和数据卷
        print("\n[2/5] 准备环境...")
        ssh_exec("docker network create sageai-network 2>/dev/null || true")
        ssh_exec("docker volume create sageai-db-data 2>/dev/null || true")
        ssh_exec("docker volume create sageai-log-data 2>/dev/null || true")
        print("  [OK] 环境准备完成")
        
        # 3. 构建并启动后端容器
        print("\n[3/5] 构建后端...")
        cmd = f"cd {PROJECT_DIR} && docker build -t sageai-backend -f Dockerfile.backend ."
        output, error = ssh_exec(cmd)
        print(f"  构建日志: {output[-300:] if output else error[-300:]}")
        
        print("\n[4/5] 启动后端...")
        cmd = f"""docker run -d --name sageai-backend --network sageai-network \
            -p 8000:8000 \
            -v sageai-db-data:/app/data \
            -v sageai-log-data:/app/logs \
            --env-file {PROJECT_DIR}/.env.production \
            -e ENV=production -e LOG_LEVEL=INFO -e DATABASE_URL=sqlite:////app/data/app.db \
            sageai-backend"""
        output, error = ssh_exec(cmd)
        print(f"  容器ID: {output.strip()[:12]}")
        
        # 等待启动
        import time
        print("  等待后端启动 (20秒)...")
        time.sleep(20)
        
        # 4. 构建并启动前端
        print("\n[5/5] 构建前端...")
        cmd = f"cd {PROJECT_DIR} && docker build -t sageai-frontend -f Dockerfile.frontend ."
        output, error = ssh_exec(cmd)
        print(f"  构建日志: {output[-200:] if output else error[-200:]}")
        
        print("\n启动前端...")
        cmd = """docker run -d --name sageai-frontend --network sageai-network \
            -p 80:80 \
            sageai-frontend"""
        output, error = ssh_exec(cmd)
        print(f"  容器ID: {output.strip()[:12]}")
        
        # 等待启动
        print("  等待前端启动 (10秒)...")
        time.sleep(10)
        
        # 5. 测试服务
        print("\n测试服务...")
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