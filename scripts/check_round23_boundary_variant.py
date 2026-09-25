"""Exercise alternate consent wording through the complete consumer chain."""
import json
import logging
from pathlib import Path
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile

logging.disable(logging.CRITICAL)
root = Path(__file__).resolve().parents[1]
text = (root / 'backend/tests/fixtures/technical_secret_scoped_license.txt').read_text(encoding='utf-8')
original = '未经甲方书面同意，乙方不得将本合同项下许可权整体转让或者再许可给第三方。'
assert original in text
text = text.replace(original, '乙方向第三方转让或者再许可本合同许可权，须取得甲方书面同意。')
report = review_contract_v2(text, 'technology', use_llm=False, profile=UserRiskProfile(user_identity='乙方/被许可方'))
item = next(i for i in report['items'] if i['item_id'] == 'TC-07-01')
result = dict(gate=report['release_quality_gate'], elements={e['element_id']: e['status'] for e in item['coverage_elements']})
(root / 'artifacts/technology_pass_semantics/round23_boundaries/consent_variant.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
assert report['release_quality_gate']['status'] == 'REPORT_READY'
assert all(e['status'] == 'COVERED' for e in item['coverage_elements'])
print('Consent word-order variant: REPORT_READY; all seven elements COVERED')
