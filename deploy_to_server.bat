@echo off
chcp 65001 >nul
REM ============================================================
REM SageAI 一键部署脚本
REM 使用前请确保: 1) Node.js已安装 2) Docker已安装并运行
REM ============================================================
set SERVER_IP=120.77.171.21
set SERVER_USER=root
set SERVER_PASS=!1iIlL.,44166
set SERVER_DIR=/opt/sageai/
set PACKAGE=sageai-deploy.tar.gz

echo.
echo ============================================================
echo   SageAI 一键部署到阿里云服务器
echo   服务器: %SERVER_IP%:%SERVER_DIR%
echo ============================================================
echo.

REM ---- 步骤1: 构建前端 ----
echo [1/5] 构建前端...
cd /d "%~dp0frontend"
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 前端构建失败！
    pause
    exit /b 1
)
cd /d "%~dp0"
echo [完成] 前端构建成功

REM ---- 步骤2: 打包项目 ----
echo [2/5] 打包项目文件...
if exist %PACKAGE% del /f %PACKAGE%

tar --exclude=frontend/node_modules --exclude=__pycache__ --exclude=*.pyc --exclude=Qwen3-4B-Thinking-2507 --exclude=.codebuddy --exclude=.git --exclude=*.log --exclude=*.tar.gz -czf %PACKAGE% backend frontend/dist docker-compose.yml Dockerfile.backend Dockerfile.frontend nginx.conf .dockerignore

if not exist %PACKAGE% (
    echo [错误] 打包失败！
    pause
    exit /b 1
)
echo [完成] 打包成功 (%PACKAGE%)

REM ---- 步骤3: 上传到服务器 ----
echo [3/5] 上传到服务器 (需要输入SSH密码)...

REM 方法: 使用内置 scp 命令
echo 正在上传，请在弹出的窗口中输入密码: %SERVER_PASS%
scp -o StrictHostKeyChecking=no %PACKAGE% %SERVER_USER%@%SERVER_IP%:%SERVER_DIR%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 上传失败！
    echo.
    echo 可能的原因:
    echo   1. 网络连接问题 - 请检查能否 ping %SERVER_IP%
    echo   2. SSH 需要密码认证 - 请在弹出的窗口中输入密码
    echo.
    echo 手动上传方法:
    echo   使用 WinSCP/FileZilla 将 %PACKAGE% 上传到 %SERVER_IP%:%SERVER_DIR%
    echo   然后 SSH 登录服务器执行以下命令:
    echo     cd %SERVER_DIR%
    echo     tar -xzf %PACKAGE%
    echo     docker-compose down
    echo     docker-compose build --no-cache
    echo     docker-compose up -d
    pause
    exit /b 1
)
echo [完成] 上传成功

REM ---- 步骤4: 远程部署 ----
echo [4/5] 在服务器上部署 (需要输入SSH密码)...

ssh -o StrictHostKeyChecking=no %SERVER_USER%@%SERVER_IP% "cd %SERVER_DIR% && tar -xzf %PACKAGE% && rm -f %PACKAGE% && docker-compose down && docker-compose build --no-cache && docker-compose up -d && docker-compose ps"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 远程部署失败！
    echo.
    echo 请手动 SSH 登录服务器执行:
    echo   ssh %SERVER_USER%@%SERVER_IP%
    echo   cd %SERVER_DIR%
    echo   tar -xzf %PACKAGE%
    echo   rm -f %PACKAGE%
    echo   docker-compose down
    echo   docker-compose build --no-cache
    echo   docker-compose up -d
    pause
    exit /b 1
)
echo [完成] 远程部署成功

REM ---- 步骤5: 验证 ----
echo [5/5] 验证服务状态...

ssh -o StrictHostKeyChecking=no %SERVER_USER%@%SERVER_IP% "curl -s http://localhost:8000/health && echo. && docker-compose ps"

if %ERRORLEVEL% NEQ 0 (
    echo [警告] 验证失败，请手动检查服务器
) else (
    echo [完成] 服务运行正常
)

REM ---- 清理 ----
echo.
echo [清理] 删除本地打包文件...
del /f %PACKAGE%

echo.
echo ============================================================
echo   部署完成！
echo   Web 地址: http://%SERVER_IP%
echo   API 地址: http://%SERVER_IP%:8000
echo ============================================================
echo.
pause
