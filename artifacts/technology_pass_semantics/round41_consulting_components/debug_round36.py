from pathlib import Path
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
r=review_contract_v2(Path('backend/tests/fixtures/round36_consulting.txt').read_text(encoding='utf8'),'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方'))
i={x['item_id']:x for x in r['items']}
print([(k,i[k]['coverage_status'],[(e['element_id'],e['status']) for e in i[k]['coverage_elements']]) for k in ('TC-01-03','TC-01-04','TC-08-01','TC-08-02','TC-08-05')])
