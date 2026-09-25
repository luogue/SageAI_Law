param([string]$Prefix = 'round12_final')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$art = "$root/artifacts/technology_pass_semantics"
$python = 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe'
$cases = @(
    @('cooperative', "$art/round12_cooperative_input/original.docx", 'technology', '甲方'),
    @('cross_article', "$art/round8_close_input_cross_article/original.docx", 'technology', '甲方/被许可方'),
    @('patent', "$art/round6_patent/original.docx", 'sale', '接受方'),
    @('consulting', "$art/round8_consulting_final/original.docx", 'technology', '甲方'),
    @('provider', "$art/round8_close_input_provider/original.docx", 'technology', '甲方'),
    @('balanced', "$art/round8_close_input_balanced/original.docx", 'technology', '甲方/被许可方'),
    @('ancillary', "$art/round8_close_input_ancillary/original.docx", 'technology', '甲方/技术秘密受让方')
)
$manifest = @(@{sample='guard'; status='NOT_VERIFIED'; reason='Original 122 source replaced by cooperative input; original SHA256 e5463c90d88b68b07544d560894b0d0487b67aa4e163bb96e817c50206283ef5 not found.'})
foreach ($case in $cases) {
    if (@(Get-CimInstance Win32_Process | Where-Object {$_.Name -match '^python(w)?\.exe$'}).Count -gt 2) {
        throw 'No Python slot for uploader'
    }
    $name,$source,$type,$party = $case
    $output = "$art/${Prefix}_${name}_live"
    $started = [DateTime]::UtcNow
    & $python -X utf8 "$root/scripts/run_technology_live_acceptance.py" $source $output --user-id 1 --contract-type $type --use-llm false --user-identity $party > "$output.out" 2> "$output.err"
    $code=$LASTEXITCODE
    $file=Get-Item -LiteralPath "$output/report.json" -ErrorAction SilentlyContinue
    if (!$file -or $file.LastWriteTimeUtc -lt $started) { throw "No fresh report: $name exit=$code" }
    $r=Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8|ConvertFrom-Json
    $hash=(Get-FileHash "$root/backend/review_v2/engine.py" -Algorithm SHA256).Hash.ToLower()
    $manifest += @{sample=$name; gate=$r.release_quality_gate; report=$file.FullName;
        process_id=$r.production_path_trace.process_id; engine_hash=$r.production_path_trace.runtime_sources.engine.sha256;
        engine_hash_matches=($hash -eq $r.production_path_trace.runtime_sources.engine.sha256)}
    $manifest|ConvertTo-Json -Depth 80|Set-Content "$art/${Prefix}_live_manifest.json" -Encoding UTF8
    Write-Output "$name $($r.release_quality_gate.status) failures=$(@($r.release_quality_gate.failures).Count) hash_matches=$($hash -eq $r.production_path_trace.runtime_sources.engine.sha256)"
}
