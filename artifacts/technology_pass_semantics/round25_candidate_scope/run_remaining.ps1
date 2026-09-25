$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
Wait-Process -Id 19500 -ErrorAction SilentlyContinue
& F:/ai/Sage/scripts/run_round25_regression.ps1 -Batch 1
$env:PYTHONPATH='F:/ai/Sage/backend;F:/ai/Sage/backend/tests;F:/ai/Sage;F:/ai/Sage/scripts'
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -m pytest backend/tests/test_foreign_secret_license_evidence_consistency.py backend/tests/test_secret_license_production_closure.py -q --junitxml=artifacts/technology_pass_semantics/round25_candidate_scope/supplemental.xml > artifacts/technology_pass_semantics/round25_candidate_scope/supplemental.out 2>&1
Wait-Process -Id 22448 -ErrorAction SilentlyContinue
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/summarize_round25_acceptance.py > artifacts/technology_pass_semantics/round25_candidate_scope/acceptance.out 2>&1
exit $LASTEXITCODE