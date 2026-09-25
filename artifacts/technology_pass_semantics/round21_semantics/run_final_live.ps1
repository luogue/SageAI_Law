$ErrorActionPreference = 'Stop'
$root = 'F:/ai/Sage'
$art = "$root/artifacts/technology_pass_semantics"
$python = 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe'
$cases = @(
    @('current_licensee', "$art/round19_secret_diagnosis/candidate_input/original.docx", '乙方/被许可方', 'true'),
    @('current_licensor', "$art/round19_secret_diagnosis/candidate_input/original.docx", '甲方/许可方', 'true'),
    @('patent_closed', "$art/round17_license_input/original.docx", '乙方 / 被许可方', 'false'),
    @('entrusted', "$art/round14_entrusted_input/original.docx", '甲方 / 委托方', 'false'),
    @('prior_patent', "$art/round15_patent_input/original.docx", '乙方 / 专利权受让方', 'false'),
    @('transfer', "$art/round16_patent_input/original.docx", '乙方 / 专利权受让方', 'false')
)
foreach ($case in $cases) {
    if (@(Get-CimInstance Win32_Process | Where-Object {$_.Name -match '^python(w)?\.exe$'}).Count -gt 2) { throw 'No Python slot for uploader' }
    $name,$source,$party,$llm = $case
    $output = "$art/round21_accepted_$name"
    & $python -X utf8 "$root/scripts/run_technology_live_acceptance.py" $source $output --user-id 1 --contract-type technology --use-llm $llm --user-identity $party > "$output.out" 2> "$output.err"
    if ($LASTEXITCODE -ne 0) { throw "Upload failed: $name" }
    $r = Get-Content "$output/report.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    Write-Output "$name $($r.release_quality_gate.status) failures=$(@($r.release_quality_gate.failures).Count)"
}
& "$root/scripts/run_round12_live.ps1" -Prefix round21_accepted
