from pathlib import Path
import json
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
out=Path('artifacts/technology_pass_semantics/round30_transfer_roles')
p=review_contract_v2((out/'input/original.txt').read_text(encoding='utf8'),'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方/受让方'))
(out/'local_transferee.json').write_text(json.dumps(p,ensure_ascii=False),encoding='utf8')
print(p['release_quality_gate']['status'],p['release_quality_gate'].get('blocking_requirements'))
for i in p['items']:
 if i['item_id'] in ['TC-01-03','TC-02-01','TC-06-01','TC-06-03','TC-09-01','TC-09-02','TC-09-03','TC-09-04','TC-10-01','TC-10-02','TC-10-03','TC-10-04','TC-11-03','TC-12-01','TC-12-03','TC-13-01','COMMON-20-01']:
  print(i['item_id'],i['coverage_status'],[(e['element_id'],e['status']) for e in i.get('coverage_elements',[])])
print('groups',len(p['risk_themes']))
