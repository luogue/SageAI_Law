$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
$out='F:/ai/Sage/artifacts/technology_pass_semantics/round41_consulting_components'
$listeners=Get-NetTCPConnection -LocalPort 8016 -State Listen -ErrorAction SilentlyContinue
foreach($listener in $listeners){
 $service=Get-CimInstance Win32_Process -Filter "ProcessId = $($listener.OwningProcess)"
 if($service.CommandLine -notmatch 'uvicorn main:app' -or $service.CommandLine -notmatch 'run_round33_low_load.py'){
  throw 'Port 8016 is not owned by the verified Sage acceptance server'
 }
 Stop-Process -Id $service.ProcessId
}
$env:PYTHONPATH='F:/ai/Sage/backend;F:/ai/Sage'
$server=Start-Process -FilePath 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -ArgumentList @('-X','utf8','F:/ai/Sage/scripts/run_round33_low_load.py','--module','uvicorn','main:app','--host','127.0.0.1','--port','8016') -WorkingDirectory 'F:/ai/Sage/backend' -WindowStyle Hidden -RedirectStandardOutput "$out/backend.stdout.log" -RedirectStandardError "$out/backend.stderr.log" -PassThru
$ready=$false
for($attempt=0;$attempt -lt 30;$attempt++){
 Start-Sleep -Seconds 1
 $listening=Get-NetTCPConnection -LocalPort 8016 -State Listen -ErrorAction SilentlyContinue
 if($listening.OwningProcess -contains $server.Id){$ready=$true;break}
 if($server.HasExited){throw 'Sage backend exited during startup'}
}
if(!$ready){throw 'Sage backend did not become ready'}
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/record_round41_runtime.py $server.Id
Get-Process -Id $server.Id | Select-Object Id,PriorityClass,ProcessorAffinity





