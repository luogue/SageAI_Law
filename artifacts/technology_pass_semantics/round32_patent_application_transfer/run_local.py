from pathlib import Path
import json
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
p=Path('artifacts/technology_pass_semantics/round32_patent_application_transfer')
r=review_contract_v2((p/'input/original.txt').read_text(encoding='utf8'),'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方/受让方'))
(p/'local.json').write_text(json.dumps(r,ensure_ascii=False),encoding='utf8')
print(r['release_quality_gate']['status'])
for i in r['items']:
 if i['item_id'].startswith(('TC-01','TC-03','TC-06','TC-12','TC-13','COMMON-20','TECH-GEN')):print(i['item_id'],i['coverage_status'],i['risk_point_description'])
