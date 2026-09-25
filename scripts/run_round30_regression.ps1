param([int]$Batch = 0)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
$env:PYTHONPATH = "$root/backend;$root/backend/tests;$root;$root/scripts"
$manifest = Get-Content "$root/artifacts/technology_pass_semantics/full33_manifest.json" -Raw | ConvertFrom-Json
$modules = @($manifest.modules[$Batch])
if ($Batch -eq 0) {
    $modules += @('backend/tests/test_registered_patent_asset_routing.py',
      'backend/tests/test_transfer_verified_roles_and_conditions.py',
      'backend/tests/test_license_element_ownership.py',
      'backend/tests/test_license_report_evidence_boundaries.py',
      'backend/tests/test_claim_semantic_scope.py',
      'backend/tests/test_requirement_polarity_components.py',
      'backend/tests/test_license_source_scope_regressions.py', 'backend/tests/test_license_boundary_mapping.py', 'backend/tests/test_patent_component_consistency.py', 'backend/tests/test_implementation_candidate_scope.py', 'backend/tests/test_service_final_fact_binding.py', 'backend/tests/test_consulting_final_fact_binding.py', 'backend/tests/test_secret_transfer_final_fact_binding.py', 'backend/tests/test_secret_license_proof_aggregation.py', 'backend/tests/test_secret_transfer_roles_projection.py')
}
$modules = @($modules | Select-Object -Unique)
$destination = "$root/artifacts/technology_pass_semantics/round30_transfer_roles/full82_batch$Batch"
$modules | ConvertTo-Json | Set-Content "$destination.modules.json" -Encoding UTF8
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -m pytest @modules -q "--junitxml=$destination.xml" > "$destination.out" 2>&1
exit $LASTEXITCODE
