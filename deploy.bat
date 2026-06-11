@echo off
echo 正在部署...
tar --exclude='.env' --exclude='node_modules' --exclude='.git' --exclude='__pycache__' -czf - . | ssh -o ServerAliveInterval=60 root@120.77.171.21 "cd /opt/sageai && tar -xzf - --overwrite && docker-compose up -d --build"
echo 部署完成
pause