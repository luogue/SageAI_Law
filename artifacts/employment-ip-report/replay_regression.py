import json
from pathlib import Path
from unittest.mock import patch
from review_v2.engine import review_contract_v2
from review_v2 import employment_fact_pipeline as pipeline

directory = Path('artifacts/employment-ip-report')
records=[]
for path in Path('artifacts/employment-105-verified-closure').glob('result-*.json'):
    old=json.loads(path.read_text(encoding='utf-8'))
    debug=old['structured_fact_debug']
    with patch.object(pipeline,'extract',return_value=debug['deepseek_raw_results']), patch.object(pipeline,'verify',return_value=debug['semantic_verification']):
        new=review_contract_v2(debug['input']['text'],'labor',include_low_risk=True)
    before={r['item_id']:r['coverage_status'] for r in old['items']}
    after={r['item_id']:r['coverage_status'] for r in new['items']}
    changes={k:[v,after[k]] for k,v in before.items() if k!='EMP-IP-01' and after[k]!=v}
    assert not changes, changes
    assert new['release_quality_gate']['status']=='REPORT_READY',new['release_quality_gate']['failures']
    assert 'DUTY_OR_RESOURCES' not in new['result']
    records.append({'baseline':path.name,'filename':old['filename'],'other_rule_changes':changes,
                    'ip_status':after['EMP-IP-01'],'gate':new['release_quality_gate']['status']})
(directory/'replay-regression.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=True))
