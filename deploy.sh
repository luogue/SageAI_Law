# 1. 本地打包（在项目目录 Git Bash 中）：
tar --exclude='.env' --exclude='node_modules' --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='Qwen3-4B-Thinking-2507' --exclude='.history' -czf deploy.tar.gz .

# 2. 上传到服务器：
scp deploy.tar.gz root@120.77.171.21:/opt/sageai/

# 3. 登录服务器并部署（可合并为一条 SSH 命令）：
ssh root@120.77.171.21 "cd /opt/sageai && sudo tar -xzf deploy.tar.gz --overwrite && sudo docker-compose up -d --build"