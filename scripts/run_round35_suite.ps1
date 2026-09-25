$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
foreach($phase in @('targeted','technical','frozen')) {
 & 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/run_round33_low_load.py scripts/run_round35_tests.py $phase
 if($LASTEXITCODE -ne 0){ throw "Round35 $phase failed; inspect saved diagnostics" }
 Write-Output "$phase complete"
}
