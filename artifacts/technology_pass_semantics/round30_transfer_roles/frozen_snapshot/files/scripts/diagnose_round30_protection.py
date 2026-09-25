"""Same-input comparison against the frozen pre-change engine."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/technology_pass_semantics/round30_transfer_roles'
import review_v2
if sys.argv[1]=='baseline':review_v2.__path__.insert(0,str(OUT/'baseline_source'))
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
kind=sys.argv[2]
location={'license':'round29_secret_license_aggregation','transfer':'round28_secret_transfer_binding','current':'round30_transfer_roles'}[kind]
party={'license':'乙方/被许可方','transfer':'乙方/受让方','current':'甲方/受让方'}[kind]
text=(ROOT/'artifacts/technology_pass_semantics'/location/'input/original.txt').read_text(encoding='utf8')
llm='--llm' in sys.argv
if llm:
 from dotenv import load_dotenv
 load_dotenv(ROOT/'backend/.env')
r=review_contract_v2(text,'technology',use_llm=llm,profile=UserRiskProfile(user_identity=party))
name='control_'+sys.argv[1]+'_'+kind+('_live' if llm else '')
(OUT/(name+'.json')).write_text(json.dumps(r,ensure_ascii=False),encoding='utf8')
print(name,r['release_quality_gate']['status'],sorted(f['risk_group'] for f in r['risk_themes']))
