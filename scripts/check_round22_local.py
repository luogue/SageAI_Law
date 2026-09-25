import json
import logging
import sys
from pathlib import Path
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile

logging.disable(logging.CRITICAL)
root = Path('artifacts/technology_pass_semantics/round22_routing')
report = review_contract_v2((root/'input/original.txt').read_text(encoding='utf-8'), 'technology', use_llm=False, profile=UserRiskProfile(user_identity='乙方/被许可方'))
(root/(sys.argv[1]+'.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(report.get('release_quality_gate'))
