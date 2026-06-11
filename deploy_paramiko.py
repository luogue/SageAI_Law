"""SageAI 一键部署脚本（使用 paramiko）"""
import paramiko
import os
import time

SERVER = "120.77.171.21"
USERNAME = "root"
PASSWORD = "!1iIlL.,44166"
PROJECT_DIR = "/opt/sageai"
BACKEND_CONTAINER = "sageai-backend"
LOCAL_BASE = "f:/ai/Sage"

FILES_TO_UPLOAD = [
    ("backend/auth/routes.py", "backend/auth/routes.py"),
    ("backend/utils/sms_client.py", "backend/utils/sms_client.py"),
    ("backend/storage/crud.py", "backend/storage/crud.py"),
    ("backend/reset_password.py", "backend/reset_password.py"),
]

def reconnect_ssh():
    """重新连接 SSH"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD, timeout=30)
    return ssh

def main():
    print("=" * 60)
    print("SageAI 部署脚本（使用 paramiko）")
    print("=" * 60)
    
    ssh = None
    try:
        # 1. 连接服务器并创建目录
        print("\n[1/5] 连接服务器并创建目录...")
        ssh = reconnect_ssh()
        cmd = f"mkdir -p {PROJECT_DIR}/backend/auth {PROJECT_DIR}/backend/utils {PROJECT_DIR}/backend/storage {PROJECT_DIR}/frontend/dist"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        print("  [OK] 目录创建完成")
        ssh.close()
        
        # 2. 上传后端文件（逐个上传，每次重新连接）
        print("\n[2/5] 上传后端文件...")
        for local, remote in FILES_TO_UPLOAD:
            ssh = reconnect_ssh()
            local_full = os.path.join(LOCAL_BASE, local)
            remote_full = f"{PROJECT_DIR}/{remote}"  # 修复路径拼接
            
            print(f"  上传 {local}")
            # 使用 base64 编码上传，避免特殊字符问题
            with open(local_full, 'rb') as f:
                content = f.read()
            
            import base64
            encoded = base64.b64encode(content).decode('utf-8')
            cmd = f"echo '{encoded}' | base64 -d > '{remote_full}'"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            
            if exit_status == 0:
                print(f"  [OK] {local}")
            else:
                error = stderr.read().decode('utf-8')
                print(f"  [FAIL] {local}: {error[:100]}")
            ssh.close()
            time.sleep(1)
        
        # 3. 上传前端 dist（打包成 tar.gz）
        print("\n[3/5] 上传前端构建产物...")
        local_dist = os.path.join(LOCAL_BASE, "frontend", "dist")
        
        # 打包前端文件
        import tarfile
        import io
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar:
            tar.add(local_dist, arcname='.')
        tar_buffer.seek(0)
        tar_content = tar_buffer.read()
        
        # 上传并解压
        ssh = reconnect_ssh()
        import base64
        encoded = base64.b64encode(tar_content).decode('utf-8')
        
        # 分块上传（避免命令过长）
        chunk_size = 4096
        chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
        
        # 先创建临时文件
        cmd = "rm -f /tmp/dist.tar.gz.base64"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        
        # 逐块写入
        for i, chunk in enumerate(chunks):
            cmd = f"echo '{chunk}' >> /tmp/dist.tar.gz.base64"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()
        
        # 解码并解压
        cmd = f"base64 -d /tmp/dist.tar.gz.base64 | tar -xzf - -C {PROJECT_DIR}/frontend/dist"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        
        print("  [OK] 前端文件上传完成")
        ssh.close()
        time.sleep(2)
        
        # 4. 重建 Docker
        print("\n[4/5] 重建 Docker 容器...")
        ssh = reconnect_ssh()
        cmd = f"cd {PROJECT_DIR} && docker-compose down && docker-compose build --no-cache backend frontend 2>&1 | tail -30"
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        stdout.channel.set_combine_stderr(True)
        output = ""
        start_time = time.time()
        while not stdout.channel.closed:
            if stdout.channel.recv_ready():
                output += stdout.channel.recv(4096).decode('utf-8', errors='ignore')
            if time.time() - start_time > 300:  # 5分钟超时
                print("  [WARN] Docker构建超时，继续...")
                break
            time.sleep(1)
        print(f"  构建输出: {output[-1000:]}")
        ssh.close()
        
        # 启动容器
        ssh = reconnect_ssh()
        cmd = f"cd {PROJECT_DIR} && docker-compose up -d"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        print("  [OK] Docker 容器启动")
        ssh.close()
        
        # 等待服务启动
        print("  等待服务启动 (20秒)...")
        time.sleep(20)
        
        # 5. 重置密码和测试
        print("\n[5/5] 重置密码并测试...")
        ssh = reconnect_ssh()
        
        # 重置密码
        cmd = f"docker exec {BACKEND_CONTAINER} python /app/reset_password.py 15680793860 123456"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8').strip() + stderr.read().decode('utf-8').strip()
        print(f"  密码重置: {output}")
        
        # 测试登录
        cmd = 'curl -s -w " HTTP:%{http_code}" -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d \'{"phone":"+8615680793860","password":"123456"}\''
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8').strip() + stderr.read().decode('utf-8').strip()
        print(f"  登录测试: {output}")
        
        ssh.close()
        
        print("\n" + "=" * 60)
        print("部署完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] 部署失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if ssh:
            try:
                ssh.close()
            except:
                pass

if __name__ == "__main__":
    main()