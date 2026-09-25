$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
foreach($mode in @('technical','frozen','adjacent')){
 & 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/run_round33_low_load.py scripts/run_round36_tests.py $mode
 if($mode -eq 'adjacent' -and (Test-Path 'artifacts/technology_pass_semantics/round36_consulting_snapshot/adjacent_baseline.xml')){
  & 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/compare_round36_adjacent.py
  if($LASTEXITCODE -ne 0){throw 'Adjacent regression changed against the pre-change baseline'}
 }elseif($LASTEXITCODE -ne 0){throw "$mode regression failed; inspect log before continuing"}
 Write-Output "$mode completed"
}
