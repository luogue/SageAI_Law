from pathlib import Path
import json
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
t=Path('backend/tests/fixtures/round40_service.txt').read_text(encoding='utf8')
r=review_contract_v2(t,'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方'))
Path('artifacts/technology_pass_semantics/round40_service_components/local_debug.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print(r['release_quality_gate']['status'])
