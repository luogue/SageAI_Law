$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
$out='F:/ai/Sage/artifacts/technology_pass_semantics/round32_patent_application_transfer'
$env:PYTHONPATH='F:/ai/Sage/backend;F:/ai/Sage'
$token=& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 -c "from dotenv import load_dotenv; load_dotenv('backend/.env'); from auth.utils import create_access_token; print(create_access_token({'user_id':'1'}))" 2> "$out/protection_auth.err"
if($LASTEXITCODE -ne 0 -or !$token){throw 'Could not create identity'}
$cases=@(
 @('secret_transferee','甲方/受让方','round31_transfer_consistency'),
 @('secret_transferor','乙方/让与方','round31_transfer_consistency'),
 @('secret_licensor','甲方/许可方','round29_secret_license_aggregation'),
 @('secret_licensee','乙方/被许可方','round29_secret_license_aggregation'),
 @('patent_licensor','甲方/许可方','round24_patent_consistency'),
 @('patent_licensee','乙方/被许可方','round24_patent_consistency')
)
foreach($entry in $cases){
 $name,$party,$round=$entry
 $file=Get-Item "F:/ai/Sage/artifacts/technology_pass_semantics/$round/input/original.docx"
 $form=@{contract_type='technology';use_llm='true';include_low_risk='true';profile_json=(@{user_identity=$party}|ConvertTo-Json -Compress);file=$file}
 $response=Invoke-WebRequest 'http://localhost:5173/review-v2/file' -Method Post -Headers @{Authorization="Bearer $token"} -Form $form -TimeoutSec 600
 $dest="$out/protection_$name";[IO.Directory]::CreateDirectory($dest)|Out-Null
 [IO.File]::WriteAllText("$dest/report.json",$response.Content,[Text.UTF8Encoding]::new($false))
 $report=$response.Content|ConvertFrom-Json
 [IO.File]::WriteAllText("$dest/report.md",$report.result,[Text.UTF8Encoding]::new($false))
 Write-Output "$name HTTP=$($response.StatusCode) gate=$($report.release_quality_gate.status) process=$($report.production_path_trace.process_id)"
}
$token=$null
