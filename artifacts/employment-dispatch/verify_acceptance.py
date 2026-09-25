"""Assert the actual live business response and independent semantic regressions."""
import hashlib
import json
from pathlib import Path

root=Path('artifacts/employment-dispatch')
path=max(root.glob('result-*.json'),key=lambda p:p.stat().st_mtime)
live=json.loads(path.read_text(encoding='utf8'))
assert live['filename']=='107 劳动合同.docx'
assert live['contract_type_name']=='劳务派遣劳动合同'
assert live['employment_classification']['subtype']=='LABOR_DISPATCH'
assert live['report_context']['contract_subtype']=='LABOR_DISPATCH'
assert live['release_quality_gate']['status']=='REPORT_READY',live['release_quality_gate']['failures']
items={r['item_id']:r for r in live['items']}
assert len(items)==28
targets=('DSP-02-01','DSP-03-01','DSP-04-01','DSP-06-01')
for rule in targets:
    row=items[rule]
    assert row['coverage_status']=='风险条款'
    assert row['evidence_clauses']
    assert all(e.get('verified_original') and e.get('structured_fact_id') for e in row['evidence_clauses'])
assert items['EMP-IP-01']['coverage_status']=='通过'
assert items['EMP-14-01']['coverage_status']=='通过'
assert items['EMP-15-01']['coverage_status']=='通过'
for token in ('DUTY_OR_RESOURCES','LOWER_ALLOWED','REGULAR_CORE','{scope:'):
    assert token not in live['result']
regressions=[]
for folder,expected in [('protective',set()),('adverse-variants',set(targets)),('ordinary-106-verified',set())]:
    result=json.loads((root/folder/'result.json').read_text(encoding='utf8'))
    dsp=[r for r in result['items'] if r['item_id'].startswith('DSP-')]
    actual={r['item_id'] for r in dsp if r['coverage_status']=='风险条款'}
    assert actual==expected,(folder,actual)
    assert result['release_quality_gate']['status']=='REPORT_READY'
    if folder=='protective':
        assert len(dsp)==8 and all(r['coverage_status']=='通过' for r in dsp)
    if folder=='ordinary-106-verified':
        assert not dsp
        baseline=json.loads(next(Path('artifacts/employment-ip-report').glob('result-*.json')).read_text(encoding='utf8'))
        assert {r['item_id']:r['coverage_status'] for r in result['items']}=={r['item_id']:r['coverage_status'] for r in baseline['items']}
    regressions.append({'fixture':folder,'fresh_deepseek':True,'gate':result['release_quality_gate']['status'],
                        'dispatch_rule_count':len(dsp),'dispatch_risks':sorted(actual)})
first=json.loads(next(root.glob('result-22936-*.json')).read_text(encoding='utf8'))
assert live['structured_fact_debug']['source_sha256']==first['structured_fact_debug']['source_sha256']
summary={'live_response':path.name,'filename':live['filename'],
    'source_file_sha256':hashlib.sha256(Path('test_data/107 劳动合同.docx').read_bytes()).hexdigest(),
    'source_text_sha256':live['structured_fact_debug']['source_sha256'],
    'classification':{k:live['employment_classification'][k] for k in ('subtype','label','employment_form','term_types')},
    'rule_count':len(items),'gate':live['release_quality_gate']['status'],
    'rules':[{'rule_id':r['item_id'],'status':r['coverage_status'],'location':r['evidence_location'],
        'quotes':[e['quote'] for e in r['evidence_clauses']]} for r in items.values() if r['item_id'].startswith('DSP-')],
    'manual_reviews':[{'rule_id':r['item_id'],'reason':r['reasoning_summary']} for r in items.values() if r['coverage_status']=='待核验'],
    'regressions':regressions}
(root/'acceptance.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
(root/'report.md').write_text(live['result'],encoding='utf8')
print(json.dumps({'gate':summary['gate'],'rules':summary['rule_count'],'subtype':summary['classification']['subtype'],
    'manual_reviews':summary['manual_reviews'],'regressions':regressions},ensure_ascii=False))
