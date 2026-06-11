#!/bin/bash
REMOTE="root@120.77.171.21"
REMOTE_DIR="/opt/sageai"

tar --exclude='.env' --exclude='node_modules' --exclude='.git' --exclude='__pycache__' -czf deploy.tar.gz .

scp deploy.tar.gz $REMOTE:$REMOTE_DIR/

ssh $REMOTE "cd $REMOTE_DIR && tar -xzf deploy.tar.gz --overwrite && nohup docker-compose up -d --build > /tmp/deploy.log 2>&1 &"

rm deploy.tar.gz
echo "部署已触发，稍后访问网站"