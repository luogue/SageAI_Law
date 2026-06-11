@echo off
chcp 65001 >nul
cd /d f:\ai\Sage

echo ============================================
echo  SageAI 一键部署脚本
echo ============================================

echo.
echo [1/4] 打包项目...
python deploy_package.py
if %errorlevel% neq 0 (
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo [2/4] 上传到服务器 120.77.171.21 ...
C:\Windows\System32\OpenSSH\scp.exe -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL sageai-deploy.tar.gz root@120.77.171.21:/opt/sageai/
if %errorlevel% neq 0 (
    echo 上传失败！请检查网络和SSH连接。
    pause
    exit /b 1
)
echo 上传完成！

echo.
echo [3/4] 停止旧容器并解压...
C:\Windows\System32\OpenSSH\ssh.exe -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL root@120.77.171.21 "cd /opt/sageai && docker compose down 2>&1 || true"
C:\Windows\System32\OpenSSH\ssh.exe -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL root@120.77.171.21 "cd /opt/sageai && rm -rf backend frontend && tar -xzf sageai-deploy.tar.gz && echo === 解压完成 ==="

echo.
echo [4/4] 构建并启动容器（等待约3-5分钟）...
C:\Windows\System32\OpenSSH\ssh.exe -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL root@120.77.171.21 "cd /opt/sageai && docker compose up -d --build 2>&1"

echo.
echo ============================================
echo  健康检查...
C:\Windows\System32\OpenSSH\ssh.exe -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL root@120.77.171.21 "curl -s localhost:8000/health 2>/dev/null || echo '后端启动中...'"
C:\Windows\System32\OpenSSH\ssh.exe -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL root@120.77.171.21 "curl -s -o /dev/null -w '%%{http_code}' localhost:80/ 2>/dev/null || echo '前端启动中...'"

echo.
echo ============================================
echo  部署完成！请访问 http://120.77.171.21/
echo ============================================
pause
