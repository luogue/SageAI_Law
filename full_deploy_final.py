"""SageAI 完整部署脚本"""
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
    print("SageAI 完整部署")
    print("=" * 60)
    
    try:
        # 1. 停止所有相关容器
        print("\n[1/6] 清理旧容器...")
        ssh_exec("docker stop $(docker ps -q --filter 'name=sageai') 2>/dev/null || true")
        ssh_exec("docker rm $(docker ps -aq --filter 'name=sageai') 2>/dev/null || true")
        print("  [OK] 旧容器已清理")
        
        # 2. 创建网络和数据卷
        print("\n[2/6] 创建网络和数据卷...")
        ssh_exec("docker network create sageai-network 2>/dev/null || true")
        ssh_exec("docker volume create sageai-db-data 2>/dev/null || true")
        ssh_exec("docker volume create sageai-log-data 2>/dev/null || true")
        print("  [OK] 网络和数据卷创建完成")
        
        # 3. 创建 .env.production
        print("\n[3/6] 创建环境配置...")
        env_content = """
DASHSCOPE_API_KEY=sk-9e6945cb47234bfb95c90ec6860aa862
ADMIN_USERNAME=admin
ADMIN_PASSWORD=%1.qaq556+-aa.
ADMIN_TOKEN=admin_secure_token_change_me
ALIYUN_ACCESS_KEY_ID=
ALIYUN_ACCESS_KEY_SECRET=
ALIYUN_GREEN_ENABLE=false
AUTO_BAN_ENABLE=true
DEBUG_PROMPT=false
ENV=production
LOG_LEVEL=INFO
"""
        import base64
        encoded = base64.b64encode(env_content.strip().encode('utf-8')).decode('utf-8')
        cmd = f"echo '{encoded}' | base64 -d > {PROJECT_DIR}/.env.production"
        ssh_exec(cmd)
        print("  [OK] .env.production 创建完成")
        
        # 4. 构建后端镜像
        print("\n[4/6] 构建后端镜像...")
        cmd = f"cd {PROJECT_DIR} && docker build -t sageai-backend:latest -f Dockerfile.backend ."
        output, error = ssh_exec(cmd)
        if output:
            last_lines = output.strip().split('\n')[-5:]
            result_text = '\n  '.join(last_lines)
        else:
            last_lines = error.strip().split('\n')[-5:]
            result_text = '\n  '.join(last_lines)
        print("  构建结果:", result_text)
        
        # 5. 启动后端容器
        print("\n[5/6] 启动后端容器...")
        cmd = f"""docker run -d --name sageai-backend --network sageai-network \
            -p 8000:8000 \
            -v sageai-db-data:/app/data \
            -v sageai-log-data:/app/logs \
            -v {PROJECT_DIR}/auth:/app/auth \
            -v {PROJECT_DIR}/utils:/app/utils \
            -v {PROJECT_DIR}/storage:/app/storage \
            -v {PROJECT_DIR}/reset_password.py:/app/reset_password.py \
            --env-file {PROJECT_DIR}/.env.production \
            sageai-backend:latest"""
        output, error = ssh_exec(cmd)
        print(f"  容器ID: {output.strip()[:12]}")
        
        # 等待启动
        import time
        print("  等待服务启动 (25秒)...")
        time.sleep(25)
        
        # 6. 测试服务
        print("\n[6/6] 测试服务...")
        
        # 健康检查
        cmd = "curl -s http://localhost:8000/health"
        output, error = ssh_exec(cmd)
        print(f"  健康检查: {output.strip() or error.strip()}")
        
        # 重置密码
        cmd = "docker exec sageai-backend python /app/reset_password.py 15680793860 123456"
        output, error = ssh_exec(cmd)
        print(f"  密码重置: {output.strip() or error.strip()}")
        
        # 测试登录
        cmd = 'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"123456"}\''
        output, error = ssh_exec(cmd)
        print(f"  登录测试: {output.strip()}")
        
        # 检查容器状态
        output, error = ssh_exec("docker ps --filter 'name=sageai-backend'")
        print(f"\n  容器状态:\n{output}")
        
        print("\n" + "=" * 60)
        print("部署完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] 部署失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()