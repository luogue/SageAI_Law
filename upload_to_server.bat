@echo off
setlocal enabledelayedexpansion

set "server=120.77.171.21"
set "port=22"
set "username=root"
set "password=!1iIlL.,44166"
set "local_path=f:\ai\Sage\backend"
set "remote_path=/opt/sageai"

echo 连接到服务器 %server%:%port%...

:: 创建远程目录
ssh -p %port% %username%@%server% "mkdir -p %remote_path%"

echo 上传文件...

:: 使用 PowerShell 进行递归复制
powershell -Command "$password = ConvertTo-SecureString '%password%' -AsPlainText -Force; $credential = New-Object System.Management.Automation.PSCredential ('%username%', $password); Get-ChildItem -Path '%local_path%' -Recurse -File | Where-Object { $_.Extension -eq '.py' -and $_.FullName -notmatch '__pycache__' -and $_.Name -ne 'clean_users.py' } | ForEach-Object { $remoteFile = $_.FullName.Replace('%local_path%\', '').Replace('\', '/'); scp -P %port% $_.FullName %username%@%server%:%remote_path%/$remoteFile }"

echo 上传配置文件...
scp -P %port% "%local_path%\.env" %username%@%server%:%remote_path%/.env
scp -P %port% "%local_path%\.env.example" %username%@%server%:%remote_path%/.env.example
scp -P %port% "%local_path%\alembic.ini" %username%@%server%:%remote_path%/alembic.ini
scp -P %port% "%local_path%\MOCK_MODE_GUIDE.md" %username%@%server%:%remote_path%/MOCK_MODE_GUIDE.md
scp -P %port% "%local_path%\contract_review_prompt.txt" %username%@%server%:%remote_path%/contract_review_prompt.txt

echo 上传目录...
scp -P %port% -r "%local_path%\alembic" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\auth" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\layers" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\reasoning" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\routers" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\security" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\storage" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\tests" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\utils" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\docs" %username%@%server%:%remote_path%/
scp -P %port% -r "%local_path%\migrations" %username%@%server%:%remote_path%/

echo 文件上传完成！

echo.
echo 验证上传结果:
ssh -p %port% %username%@%server% "ls -la %remote_path%/"

endlocal