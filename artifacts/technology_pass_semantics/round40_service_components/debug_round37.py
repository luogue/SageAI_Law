from pathlib import Path
import json
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
text=Path('backend/tests/fixtures/round37_service.txt').read_text(encoding='utf8')
r=review_contract_v2(text,'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方'))
print(json.dumps(r['release_quality_gate']['failures'],ensure_ascii=False,indent=2))
