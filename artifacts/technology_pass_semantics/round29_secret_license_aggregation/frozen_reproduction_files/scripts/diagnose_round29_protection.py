"""Compare frozen prior and current engines with identical deterministic input."""
import sys
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/technology_pass_semantics/round29_secret_license_aggregation'
import review_v2
if sys.argv[1]=='baseline':
    review_v2.__path__.insert(0,str(OUT/'baseline_source'))
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
live = '--llm' in sys.argv
if live:
    from dotenv import load_dotenv
    load_dotenv(ROOT/'backend/.env')
text=(ROOT/'artifacts/technology_pass_semantics/round28_secret_transfer_binding/input/original.txt').read_text(encoding='utf-8')
r=review_contract_v2(text,'technology',use_llm=live,profile=UserRiskProfile(user_identity='乙方/受让方'))
(OUT/('control_'+sys.argv[1]+('_live' if live else '')+'.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(sys.argv[1],r['release_quality_gate']['status'],sorted(f['risk_group'] for f in r['risk_findings']))
