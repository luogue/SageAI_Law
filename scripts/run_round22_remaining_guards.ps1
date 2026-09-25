$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
$art = "$root/artifacts/technology_pass_semantics"
$python = 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe'
$cases = @(
    @('patent_closed', 'round17_license_input/original.docx', '乙方/被许可方'),
    @('entrusted', 'round14_entrusted_input/original.docx', '甲方/委托方'),
    @('prior_patent', 'round15_patent_input/original.docx', '乙方/专利权受让方'),
    @('transfer', 'round16_patent_input/original.docx', '乙方/专利权受让方'),
    @('prior_secret_licensor', 'round19_secret_diagnosis/candidate_input/original.docx', '甲方/许可方'),
    @('prior_secret_licensee', 'round19_secret_diagnosis/candidate_input/original.docx', '乙方/被许可方')
)
foreach ($case in $cases) {
    $name,$source,$party = $case
    $output = "$art/round22_accepted_$name"
    $llm = if ($name.StartsWith('prior_secret_')) { 'true' } else { 'false' }
    & $python -X utf8 "$root/scripts/run_technology_live_acceptance.py" "$art/$source" $output --user-id 1 --contract-type technology --use-llm $llm --user-identity $party > "$output.out" 2> "$output.err"
    if ($LASTEXITCODE -ne 0) { throw "Protection sample failed: $name" }
    $r = Get-Content "$output/report.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    Write-Output "$name $($r.release_quality_gate.status) failures=$(@($r.release_quality_gate.failures).Count)"
}
