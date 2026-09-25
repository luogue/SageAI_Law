param([string]$Prefix = 'round11_final')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$art = "$root/artifacts/technology_pass_semantics"
$python = 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe'
$cases = @(
    @('cross_article', "$art/round8_close_input_cross_article/original.docx", 'technology', '甲方/被许可方'),
    @('patent', "$art/round6_patent/original.docx", 'sale', '接受方'),
    @('guard', "$root/test_data/122 测试2.docx", 'technology', '甲方'),
    @('consulting', "$art/round8_consulting_final/original.docx", 'technology', '甲方'),
    @('provider', "$art/round8_close_input_provider/original.docx", 'technology', '甲方'),
    @('balanced', "$art/round8_close_input_balanced/original.docx", 'technology', '甲方/被许可方'),
    @('ancillary', "$art/round8_close_input_ancillary/original.docx", 'technology', '甲方/技术秘密受让方')
)
$manifest = @()
foreach ($case in $cases) {
    $running = @(Get-CimInstance Win32_Process | Where-Object {$_.Name -match '^python(w)?\.exe$'})
    if ($running.Count -gt 2) { throw 'No Python process slot available for normal uploader.' }
    $name, $source, $type, $party = $case
    $output = "$art/${Prefix}_${name}_live"
    $started = [DateTime]::UtcNow
    & $python -X utf8 "$root/scripts/run_technology_live_acceptance.py" $source $output --user-id 1 --contract-type $type --use-llm false --user-identity $party > "$art/${Prefix}_${name}_live.out" 2> "$art/${Prefix}_${name}_live.err"
    $exitCode = $LASTEXITCODE
    $resultFile = Get-Item -LiteralPath "$output/report.json" -ErrorAction SilentlyContinue
    if (!$resultFile -or $resultFile.LastWriteTimeUtc -lt $started) {
        throw "No fresh response for $name (exit=$exitCode). Previous reports cannot satisfy acceptance."
    }
    $report = Get-Content -LiteralPath "$output/report.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    $hash = (Get-FileHash "$root/backend/review_v2/engine.py" -Algorithm SHA256).Hash.ToLower()
    $loaded = $report.production_path_trace.runtime_sources.engine.sha256
    $manifest += @{sample=$name; source=$source; exit_code=$exitCode; gate=$report.release_quality_gate;
                   runtime=$report.production_path_trace; report="$output/report.json"; engine_hash_matches=($hash -eq $loaded)}
    $manifest | ConvertTo-Json -Depth 80 | Set-Content "$art/${Prefix}_live_manifest.json" -Encoding UTF8
    Write-Output "$name Gate=$($report.release_quality_gate.status) hash_matches=$($hash -eq $loaded)"
}
