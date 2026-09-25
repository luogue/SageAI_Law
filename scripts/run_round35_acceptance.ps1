$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
./scripts/run_round35_suite.ps1
./scripts/run_round35_current.ps1 -Phase final
$out='F:/ai/Sage/artifacts/technology_pass_semantics/round35_development_consumers'
foreach($side in @('party_a','party_b')){
 $report=Get-Content "$out/final_$side/report.json" -Raw -Encoding UTF8 | ConvertFrom-Json
 if($report.release_quality_gate.status -ne 'REPORT_READY'){throw "$side real interface is blocked"}
}
./scripts/run_round35_protection.ps1
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/run_round33_low_load.py scripts/audit_round35_artifacts.py
if($LASTEXITCODE -ne 0){throw 'Source audit failed'}
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/run_round33_low_load.py scripts/summarize_round35.py
if($LASTEXITCODE -ne 0){throw 'Acceptance checks need attention'}
