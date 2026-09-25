$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
& ./scripts/run_round29_regression.ps1 -Batch 1
$env:PYTHONPATH='backend;backend/tests;.;scripts'
$out='F:/ai/Sage/artifacts/technology_pass_semantics/round29_secret_license_aggregation'
foreach($suite in @('focused','supplemental')){
    $manifest = if ($suite -eq 'focused') { "$out/focused.nodeids.json" } else { "$out/supplemental.modules.json" }
    & 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/run_round26_manifest.py $manifest "$out/$suite.xml" *> "$out/$suite.out"
}
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -m pytest backend/tests/test_secret_license_proof_aggregation.py -q "--junitxml=$out/targeted.xml" *> "$out/targeted.out"
