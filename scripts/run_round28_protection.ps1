param([switch]$StartRegressions)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
$art = "$root/artifacts/technology_pass_semantics"
$env:PYTHONPATH = "$root/backend;$root"
# Keep the normal development identity token only in this process's memory.
$token = & 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -c "from dotenv import load_dotenv; load_dotenv('backend/.env'); from auth.utils import create_access_token; print(create_access_token({'user_id':'1'}))" 2> "$art/round28_secret_transfer_binding/auth-validation.err"
if ($LASTEXITCODE -ne 0 -or !$token) { throw 'Could not create upload identity' }
if ($StartRegressions) {
    foreach ($batch in 0,1) {
        $worker = Start-Process -FilePath (Get-Process -Id $PID).Path -ArgumentList @('-NoProfile','-File',"$root/scripts/run_round28_regression.ps1",'-Batch',"$batch") -WorkingDirectory $root -WindowStyle Hidden -PassThru
        Write-Output "Regression batch $batch launched in process $($worker.Id)"
    }
}
$cases = @(
    @('round28_accepted_consulting_client','round27_consulting_binding/input/original.docx','甲方/委托方','technology','true'),
    @('round28_accepted_consulting_provider','round27_consulting_binding/input/original.docx','乙方/咨询方','technology','true'),
    @('round28_accepted_service_client','round26_service_binding/input/original.docx','甲方/委托方','technology','true'),
    @('round28_accepted_service_provider','round26_service_binding/input/original.docx','乙方/服务方','technology','true'),
    @('round28_accepted_current_patent_licensor','round25_candidate_scope/input/original.docx','甲方/许可方','technology','true'),
    @('round28_accepted_current_patent_licensee','round25_candidate_scope/input/original.docx','乙方/被许可方','technology','true'),
    @('round28_accepted_recent_secret_licensor','round22_routing/input/original.docx','甲方/许可方','technology','true'),
    @('round28_accepted_recent_secret_licensee','round22_routing/input/original.docx','乙方/被许可方','technology','true'),
    @('round28_accepted_cooperative_live','round12_cooperative_input/original.docx','甲方','technology','false'),
    @('round28_accepted_cross_article_live','round8_close_input_cross_article/original.docx','甲方/被许可方','technology','false'),
    @('round28_accepted_patent_live','round6_patent/original.docx','接受方','sale','false'),
    @('round28_accepted_consulting_live','round8_consulting_final/original.docx','甲方','technology','false'),
    @('round28_accepted_provider_live','round8_close_input_provider/original.docx','甲方','technology','false'),
    @('round28_accepted_balanced_live','round8_close_input_balanced/original.docx','甲方/被许可方','technology','false'),
    @('round28_accepted_ancillary_live','round8_close_input_ancillary/original.docx','甲方/技术秘密受让方','technology','false'),
    @('round28_accepted_patent_closed','round17_license_input/original.docx','乙方/被许可方','technology','false'),
    @('round28_accepted_entrusted','round14_entrusted_input/original.docx','甲方/委托方','technology','false'),
    @('round28_accepted_prior_patent','round15_patent_input/original.docx','乙方/专利权受让方','technology','false'),
    @('round28_accepted_transfer','round16_patent_input/original.docx','乙方/专利权受让方','technology','false'),
    @('round28_accepted_prior_secret_licensor','round19_secret_diagnosis/candidate_input/original.docx','甲方/许可方','technology','true'),
    @('round28_accepted_prior_secret_licensee','round19_secret_diagnosis/candidate_input/original.docx','乙方/被许可方','technology','true')
)
foreach ($case in $cases) {
    $name,$source,$party,$type,$llm = $case
    $form = @{contract_type=$type; use_llm=$llm; include_low_risk='true'; profile_json=(@{user_identity=$party}|ConvertTo-Json -Compress); file=(Get-Item "$art/$source")}
    $response = Invoke-WebRequest 'http://localhost:5173/review-v2/file' -Method Post -Headers @{Authorization="Bearer $token"} -Form $form -TimeoutSec 600
    $output = "$art/$name"
    [IO.Directory]::CreateDirectory($output) | Out-Null
    [IO.File]::WriteAllText("$output/report.json",$response.Content,[Text.UTF8Encoding]::new($false))
    $report = $response.Content | ConvertFrom-Json
    [IO.File]::WriteAllText("$output/report.md",$report.result,[Text.UTF8Encoding]::new($false))
    if ($report.release_quality_gate.status -ne 'REPORT_READY' -or @($report.release_quality_gate.failures).Count) { Write-Output "Gate failed for $name" }
    Write-Output "$name HTTP=$($response.StatusCode) gate=$($report.release_quality_gate.status) blockers=$(@($report.release_quality_gate.failures).Count) process=$($report.production_path_trace.process_id)"
}
$token = $null
