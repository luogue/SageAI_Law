$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
foreach($worker in @(19864,16664,17824)){Wait-Process -Id $worker -ErrorAction SilentlyContinue}
$env:PYTHONPATH='F:/ai/Sage/backend;F:/ai/Sage/backend/tests;F:/ai/Sage;F:/ai/Sage/scripts'
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/summarize_round25_acceptance.py > artifacts/technology_pass_semantics/round25_candidate_scope/acceptance.out 2>&1
exit $LASTEXITCODE