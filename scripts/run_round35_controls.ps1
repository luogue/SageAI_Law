$ErrorActionPreference='Stop'
Set-Location F:/ai/Sage
$cases=@(
 @('cooperative_a','round34_cooperative_routing','甲方'),
 @('secret_licensor','round29_secret_license_aggregation','甲方/许可方'),
 @('secret_transferee','round31_transfer_consistency','甲方/受让方')
)
foreach($case in $cases){
 $name,$round,$role=$case
 foreach($mode in @('baseline','final')){
  & 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/run_round33_low_load.py scripts/check_round35_fixed_protection.py $mode $name $round $role
  if($LASTEXITCODE -ne 0){throw "Fixed-output control failed: $name $mode"}
 }
}
& 'C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe' -X utf8 scripts/run_round33_low_load.py scripts/summarize_round35.py
if($LASTEXITCODE -ne 0){throw 'Fixed-output acceptance checks need attention'}
