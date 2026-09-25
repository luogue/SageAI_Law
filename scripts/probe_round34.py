import sys,json
from pathlib import Path
sys.path[:0]=['backend','.']
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
out=Path('artifacts/technology_pass_semantics/round34_cooperative_routing')
r=review_contract_v2((out/'input/original.txt').read_text(encoding='utf8'),'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方'))
(out/'probe.json').write_text(json.dumps(r,ensure_ascii=False),encoding='utf8')
print(r['contract_type'],r['release_quality_gate'])
