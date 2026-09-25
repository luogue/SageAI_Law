param([string]$Prefix = 'full29', [string]$Baseline = 'full28',
      [string]$AdditionalModule = 'backend/tests/test_cross_article_upload_closure.py')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$python = 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe'
$running = @(Get-CimInstance Win32_Process | Where-Object {$_.Name -match '^python(w)?\.exe$'})
if ($running.Count -gt 1) { throw 'Only the backend may be running before the two serial pytest workers start.' }
$costs = @{}
foreach ($path in (Get-ChildItem "$root/artifacts/technology_pass_semantics/${Baseline}_batch*.xml")) {
    [xml]$doc = Get-Content -LiteralPath $path.FullName -Raw
    foreach ($case in $doc.SelectNodes('//testcase')) {
        $module = $case.classname.Replace('.', '/') + '.py'
        if (!(Test-Path -LiteralPath "$root/$module")) { throw "Missing original module: $module" }
        $costs[$module] += [double]$case.time
    }
}
if (!(Test-Path -LiteralPath "$root/$AdditionalModule")) { throw 'Additional test module does not exist' }
$costs[$AdditionalModule] = 55
$batches = @([System.Collections.Generic.List[string]]::new(), [System.Collections.Generic.List[string]]::new())
$weights = @(0.0, 0.0)
foreach ($module in ($costs.Keys | Sort-Object -Property @{Expression = {$costs[$_]}; Descending = $true})) {
    $index = if ($weights[0] -le $weights[1]) { 0 } else { 1 }
    $batches[$index].Add($module)
    $weights[$index] += $costs[$module]
}
$env:PYTHONPATH = "$root/backend;$root"
$processes = @()
for ($i = 0; $i -lt 2; $i++) {
    $output = "$root/artifacts/technology_pass_semantics/${Prefix}_batch$i"
    $arguments = @('-X', 'utf8', '-m', 'pytest') + $batches[$i].ToArray() + @('-q', '--tb=short', "--junitxml=$output.xml")
    $processes += Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -PassThru -RedirectStandardOutput "$output.out" -RedirectStandardError "$output.err"
}
@{ modules = @($batches[0].ToArray(), $batches[1].ToArray()); pids = @($processes.Id); baseline = $Baseline; estimated_seconds = $weights } |
    ConvertTo-Json -Depth 5 | Set-Content "$root/artifacts/technology_pass_semantics/${Prefix}_manifest.json" -Encoding UTF8
Write-Output "Started two pytest processes: $($processes.Id -join ', '); modules=$($costs.Count). Backend reserved."
foreach ($process in $processes) { $process.WaitForExit() }
Write-Output "Finished: $($processes.ExitCode -join ', ')"
