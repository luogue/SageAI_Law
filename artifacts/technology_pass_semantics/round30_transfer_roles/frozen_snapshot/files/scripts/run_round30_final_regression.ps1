param([int]$Batch = 0)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
$env:PYTHONPATH = "$root/backend;$root/backend/tests;$root;$root/scripts"
$destination = "$root/artifacts/technology_pass_semantics/round30_transfer_roles/full83_batch$Batch"
$manifest = Get-Content "$root/artifacts/technology_pass_semantics/round30_transfer_roles/full83_manifest.json" -Raw | ConvertFrom-Json
$modules = @($manifest.modules[$Batch])
$modules | ConvertTo-Json | Set-Content "$destination.modules.json" -Encoding UTF8
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -m pytest @modules -q "--junitxml=$destination.xml" > "$destination.out" 2>&1
exit $LASTEXITCODE
