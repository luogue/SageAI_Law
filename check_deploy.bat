@echo off
echo === SageAI Deploy Checker ===
echo.
:loop
python -c "import paramiko; s=paramiko.SSHClient(); s.set_missing_host_key_policy(paramiko.AutoAddPolicy()); s.connect('120.77.171.21',22,'root','!1iIlL.,44166',timeout=15,banner_timeout=15); i,o,e=s.exec_command('curl -s http://localhost:8000/health 2>&1'); h=o.read().decode().strip(); i2,o2,e2=s.exec_command('docker ps --format \"{{.Names}} {{.Status}}\" ^| grep sage 2^>^&1'); c=o2.read().decode().strip(); print(f'Health: {h[:100]}'); print(f'Containers: {c}'); s.close(); exit(0 if 'healthy' in h.lower() and 'sageai-frontend' in c else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo *** DEPLOY SUCCESS! ***
    echo Visit: http://120.77.171.21
    pause
    exit /b 0
)
echo Waiting for build... (%time%)
timeout /t 30 /nobreak >nul
goto loop
