# deploy.ps1
$REMOTE = "root@120.77.171.21"
$REMOTE_DIR = "/opt/sageai"

Write-Host "打包中..."
tar --exclude='.env' --exclude='node_modules' --exclude='.git' --exclude='__pycache__' -czf deploy.tar.gz .

Write-Host "上传中..."
scp deploy.tar.gz ${REMOTE}:${REMOTE_DIR}/

Write-Host "触发远程部署..."
ssh $REMOTE "tmux new-session -d -s sageai 'cd $REMOTE_DIR && tar -xzf deploy.tar.gz --overwrite && docker-compose up -d --build && rm deploy.tar.gz'"

Remove-Item deploy.tar.gz
Write-Host "部署已触发，请稍后访问网站。"