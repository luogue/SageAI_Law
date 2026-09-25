param([string]$Phase='before')
$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
$out='F:/ai/Sage/artifacts/technology_pass_semantics/round31_transfer_consistency'
$env:PYTHONPATH='F:/ai/Sage/backend;F:/ai/Sage'
$token=& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -c "from dotenv import load_dotenv; load_dotenv('backend/.env'); from auth.utils import create_access_token; print(create_access_token({'user_id':'1'}))" 2> "$out/auth.err"
if($LASTEXITCODE -ne 0 -or !$token){throw 'Could not create identity'}
foreach($entry in @(@('transferee','甲方/受让方'),@('transferor','乙方/让与方'))){
 $name,$party=$entry
 $form=@{contract_type='technology';use_llm='true';include_low_risk='true';profile_json=(@{user_identity=$party}|ConvertTo-Json -Compress);file=Get-Item "$out/input/original.docx"}
 $response=Invoke-WebRequest 'http://localhost:5173/review-v2/file' -Method Post -Headers @{Authorization="Bearer $token"} -Form $form -TimeoutSec 600
 $dest="$out/${Phase}_$name";[IO.Directory]::CreateDirectory($dest)|Out-Null
 [IO.File]::WriteAllText("$dest/report.json",$response.Content,[Text.UTF8Encoding]::new($false))
 $report=$response.Content|ConvertFrom-Json
 [IO.File]::WriteAllText("$dest/report.md",$report.result,[Text.UTF8Encoding]::new($false))
 Write-Output "$name HTTP=$($response.StatusCode) gate=$($report.release_quality_gate.status) process=$($report.production_path_trace.process_id)"
}
$token=$null
