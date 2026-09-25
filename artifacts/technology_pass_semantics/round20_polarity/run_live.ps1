$ErrorActionPreference = 'Stop'
$root = 'F:/ai/Sage'
$art = "$root/artifacts/technology_pass_semantics"
$python = 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe'
& "$root/scripts/run_round12_live.ps1" -Prefix round20_complete
$cases = @(
    @('patent_closed', 'round17_license_input', '乙方', 'false'),
    @('entrusted', 'round14_entrusted_input', '甲方', 'false'),
    @('prior_patent', 'round15_patent_input', '乙方', 'false'),
    @('transfer', 'round16_patent_input', '乙方', 'false'),
    @('current_licensee', 'round19_secret_diagnosis/candidate_input', '乙方/被许可方', 'true'),
    @('current_licensor', 'round19_secret_diagnosis/candidate_input', '甲方/许可方', 'true')
)
foreach ($case in $cases) {
    if (@(Get-CimInstance Win32_Process -Filter "name='python.exe'").Count -gt 2) {
        throw 'No free Python process slot'
    }
    $name,$inputFolder,$party,$llm = $case
    & $python -X utf8 "$root/scripts/run_technology_live_acceptance.py" "$art/$inputFolder/original.docx" "$art/round20_complete_$name" --user-id 1 --contract-type technology --use-llm $llm --user-identity $party *> "$art/round20_polarity/complete_$name.out"
    if ($LASTEXITCODE -ne 0) { throw "Live acceptance failed: $name" }
    Write-Output "$name REPORT_READY"
}
