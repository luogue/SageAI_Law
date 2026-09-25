import json
from pathlib import Path
from collections import Counter
p=Path('artifacts/work85/scenario-after.json'); d=json.loads(p.read_text(encoding='utf8'))
print('task',d['contract_review_trace_id'],'counts',Counter(i['coverage_status'] for i in d['items']))
print('gate',d['release_quality_gate']['status'])
for i in d['items']:
 if i['item_id'] in ['COMMON-23-01','W-03-03','W-03-04','W-10-01','W-10-02','W-10-03','W-04-03','W-04-04']:
  print(i['item_id'],i['coverage_status'],str(i.get('applicability'))[:900]);print('keys',list(i) if i['item_id']=='COMMON-23-01' else '')
