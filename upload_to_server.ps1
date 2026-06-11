# 上传代码到服务器
$server = "120.77.171.21"
$port = "22"
$username = "root"
$password = "!1iIlL.,44166"
$localPath = "f:\ai\Sage\backend"
$remotePath = "/opt/sageai/"

# 创建期望的目录结构
$sshCommand = @"
ssh -p $port $username@$server "mkdir -p /opt/sageai"
"@

Write-Host "创建远程目录..."
Invoke-Expression $sshCommand

# 使用 pscp 上传文件（排除不需要的文件）
$pscpPath = "C:\Program Files\PuTTY\pscp.exe"
if (-not (Test-Path $pscpPath)) {
    $pscpPath = "C:\Program Files (x86)\PuTTY\pscp.exe"
}

if (-not (Test-Path $pscpPath)) {
    Write-Error "pscp not found! Please install PuTTY or use another method."
    exit 1
}

Write-Host "开始上传文件..."

# 上传所有 .py 文件
Get-ChildItem -Path $localPath -Recurse -Filter "*.py" | ForEach-Object {
    $relativePath = $_.FullName.Substring($localPath.Length + 1)
    $remoteFilePath = $remotePath + $relativePath.Replace("\", "/")
    
    # 排除 __pycache__ 目录和 clean_users.py
    if ($_.FullName -notlike "*__pycache__*" -and $_.Name -ne "clean_users.py") {
        Write-Host "Uploading: $($_.FullName)"
        & $pscpPath -scp -P $port -pw $password "$($_.FullName)" "$username@$server`:$remoteFilePath"
    }
}

# 上传配置文件
Get-ChildItem -Path $localPath -Filter ".env*" | ForEach-Object {
    Write-Host "Uploading: $($_.FullName)"
    & $pscpPath -scp -P $port -pw $password "$($_.FullName)" "$username@$server`:$remotePath$($_.Name)"
}

# 上传其他重要文件
$otherFiles = @("alembic.ini", "MOCK_MODE_GUIDE.md", "contract_review_prompt.txt")
foreach ($file in $otherFiles) {
    $localFile = Join-Path $localPath $file
    if (Test-Path $localFile) {
        Write-Host "Uploading: $localFile"
        & $pscpPath -scp -P $port -pw $password "$localFile" "$username@$server`:$remotePath$file"
    }
}

# 上传 docs 目录
$docsPath = Join-Path $localPath "docs"
if (Test-Path $docsPath) {
    Write-Host "Uploading docs directory..."
    & $pscpPath -scp -P $port -pw $password -r "$docsPath" "$username@$server`:$remotePath"
}

# 上传 alembic 目录（排除 __pycache__）
$alembicPath = Join-Path $localPath "alembic"
if (Test-Path $alembicPath) {
    Write-Host "Uploading alembic directory..."
    & $pscpPath -scp -P $port -pw $password -r "$alembicPath" "$username@$server`:$remotePath"
}

Write-Host "文件上传完成！"

# 验证上传结果
Write-Host "`n验证上传结果..."
ssh -p $port $username@$server "ls -la /opt/sageai/"