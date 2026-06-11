# ============================================================
# SageAI 部署脚本 - 上传到阿里云服务器并重启服务
# ============================================================
param(
    [string]$ServerIP = "120.77.171.21",
    [string]$ServerUser = "root",
    [string]$ServerPassword = "!1iIlL.,44166",
    [string]$ServerDir = "/opt/sageai/",
    [string]$PackageName = "sageai-deploy.tar.gz"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  SageAI 部署脚本" -ForegroundColor Cyan
Write-Host "  目标服务器: ${ServerIP}:${ServerDir}" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ========== 步骤1: 构建前端 ==========
Write-Host "[1/5] 构建前端..." -ForegroundColor Yellow
Set-Location "$ScriptDir/frontend"
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] 前端构建失败" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] 前端构建完成" -ForegroundColor Green
Set-Location $ScriptDir

# ========== 步骤2: 打包项目 ==========
Write-Host "[2/5] 打包项目文件..." -ForegroundColor Yellow

# 删除旧的打包文件
if (Test-Path $PackageName) {
    Remove-Item $PackageName -Force
}

# 使用 tar 打包（排除不需要的文件和目录）
$tarExcludes = @(
    "--exclude=frontend/node_modules",
    "--exclude=frontend/.git",
    "--exclude=__pycache__",
    "--exclude=backend/__pycache__",
    "--exclude=*.pyc",
    "--exclude=*.tar.gz",
    "--exclude=Qwen3-4B-Thinking-2507",
    "--exclude=.codebuddy",
    "--exclude=.git",
    "--exclude=*.log"
)

# 需要打包的文件和目录
$includeItems = @(
    "backend",
    "frontend/dist",
    "frontend/package.json",
    "frontend/package-lock.json",
    "docker-compose.yml",
    "Dockerfile.backend",
    "Dockerfile.frontend",
    "nginx.conf",
    ".env.production.example"
)

# 使用7z或tar打包
$tarCmd = "tar -czf $PackageName $($tarExcludes -join ' ') $($includeItems -join ' ')"
Write-Host "  执行: $tarCmd"
Invoke-Expression $tarCmd
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $PackageName)) {
    Write-Host "[ERROR] 打包失败" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] 打包完成: $PackageName ($([math]::Round((Get-Item $PackageName).Length / 1MB, 2)) MB)" -ForegroundColor Green

# ========== 步骤3: 上传到服务器 ==========
Write-Host "[3/5] 上传到服务器 ${ServerIP}..." -ForegroundColor Yellow

# 使用 SCP 上传（通过 SSH 密码方式）
# Windows 下使用 sshpass 或 plink，这里使用内置的 scp
# 注意：需要通过 sshpass 或密钥认证方式

# 检查是否有 sshpass
$sshpassExists = Get-Command sshpass -ErrorAction SilentlyContinue
if ($sshpassExists) {
    $scpCmd = "sshpass -p '$ServerPassword' scp -o StrictHostKeyChecking=no $PackageName ${ServerUser}@${ServerIP}:${ServerDir}"
} else {
    # 使用 OpenSSH (Windows 10+ 内置)
    # 需要先配置免密登录或使用 sshpass
    Write-Host "[WARN] sshpass 未安装，尝试使用 SSH..." -ForegroundColor Yellow
    $scpCmd = "scp -o StrictHostKeyChecking=no $PackageName ${ServerUser}@${ServerIP}:${ServerDir}"
}

Write-Host "  执行: scp $PackageName ${ServerUser}@${ServerIP}:${ServerDir}"
Invoke-Expression $scpCmd
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] 上传失败" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] 上传完成" -ForegroundColor Green

# ========== 步骤4: 在服务器上解压并部署 ==========
Write-Host "[4/5] 在服务器上解压并重新部署..." -ForegroundColor Yellow

# 构建远程命令
$remoteCmd = @"
cd ${ServerDir} &&
tar -xzf ${PackageName} &&
rm -f ${PackageName} &&
docker-compose down &&
docker-compose build --no-cache &&
docker-compose up -d &&
docker-compose ps
"@

if ($sshpassExists) {
    $sshCmd = "sshpass -p '$ServerPassword' ssh -o StrictHostKeyChecking=no ${ServerUser}@${ServerIP} `"$remoteCmd`""
} else {
    $sshCmd = "ssh -o StrictHostKeyChecking=no ${ServerUser}@${ServerIP} `"$remoteCmd`""
}

Write-Host "  正在远程部署..."
Invoke-Expression $sshCmd
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] 远程部署失败" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] 远程部署完成" -ForegroundColor Green

# ========== 步骤5: 验证部署 ==========
Write-Host "[5/5] 验证部署状态..." -ForegroundColor Yellow

$healthCheckCmd = "curl -s -o /dev/null -w '%{http_code}' http://${ServerIP}:8000/health"
if ($sshpassExists) {
    $healthResult = Invoke-Expression "sshpass -p '$ServerPassword' ssh -o StrictHostKeyChecking=no ${ServerUser}@${ServerIP} `"$healthCheckCmd`""
} else {
    $healthResult = Invoke-Expression "ssh -o StrictHostKeyChecking=no ${ServerUser}@${ServerIP} `"$healthCheckCmd`""
}

if ($healthResult -eq "200") {
    Write-Host "[OK] 服务运行正常！" -ForegroundColor Green
} else {
    Write-Host "[WARN] 健康检查返回: $healthResult，请手动检查" -ForegroundColor Yellow
}

# ========== 清理本地打包文件 ==========
Write-Host ""
Write-Host "[清理] 删除本地打包文件..." -ForegroundColor Yellow
Remove-Item $PackageName -Force -ErrorAction SilentlyContinue
Write-Host "[OK] 本地清理完成" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  部署完成！" -ForegroundColor Cyan
Write-Host "  Web 地址: http://${ServerIP}" -ForegroundColor Cyan
Write-Host "  API 地址: http://${ServerIP}:8000" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
