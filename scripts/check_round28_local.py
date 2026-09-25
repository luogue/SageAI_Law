from pathlib import Path
import json
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile

out=Path('artifacts/technology_pass_semantics/round28_secret_transfer_binding')
report=review_contract_v2(out.joinpath('input/original.txt').read_text(encoding='utf-8'), 'technology', use_llm=False,
                          profile=UserRiskProfile(user_identity='乙方/受让方'))
out.joinpath('current_local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(report['report_context']['contract_type_label'])
print(json.dumps(report['release_quality_gate']['failures'],ensure_ascii=False))
for item in report['items']:
    if item['item_id'] in ['TC-01-03','TC-03-04','TC-06-01','TC-06-03','TC-11-01','TC-11-02','TC-11-04','TC-12-02','TC-12-03','TC-13-02']:
        print(item['item_id'],item['coverage_status'],[(e['element_id'],e['status']) for e in item['coverage_elements']])
