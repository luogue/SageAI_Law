"""Audit a saved live /review-v2/file response without rewriting its result."""
import collections
import hashlib
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
result = json.loads(path.read_text(encoding='utf-8'))
out = path.parent
items = {i['item_id']: i for i in result['items']}
expected = {'D-04-04':'不适用','D-08-03':'部分覆盖','D-07-02':'通过',
            'D-01-03':'通过','D-02-03':'通过','D-07-01':'通过',
            'D-09-03':'不适用','D-12-04':'部分覆盖','COMMON-20-01':'通过'}
for key, state in expected.items():
    assert items[key]['coverage_status'] == state, (key, items[key]['coverage_status'])
assert len(items) == 49
assert '未经甲方同意' in str(items['D-08-03']['evidence_clauses'])
assert '故意或者重大过失' in str(items['D-07-02']['evidence_clauses'])
assert all('违约金' not in e['quote'] for e in items['D-04-04']['applicability']['premise_evidence'])
assert result['release_quality_gate']['status'] == 'REPORT_READY'
assert not result['release_quality_gate']['failures']
conflicts = []
for item in items.values():
    trace = item.get('decision_trace', {})
    for element in item.get('coverage_elements', []):
        if element['status'] == 'COVERED':
            if not element['evidence_ids']:
                conflicts.append((item['item_id'], element['element_id'], 'missing binding'))
            for audit in trace.get('element_absence_searches', []):
                if audit.get('element_id') == element['element_id'] and audit.get('result') == 'NOT_FOUND':
                    conflicts.append((item['item_id'], element['element_id'], 'negative audit'))
    if item['coverage_status'] == '缺失' and any(e['status']=='COVERED' for e in item.get('coverage_elements', [])):
        conflicts.append((item['item_id'], 'covered atom in missing rule'))
assert not conflicts, conflicts
audit = {'source_result':path.name,'source_sha256':hashlib.sha256(Path('test_data/82 保管合同.docx').read_bytes()).hexdigest(),
         'counts':dict(collections.Counter(i['coverage_status'] for i in items.values())),
         'overview':result['final_overview_summary'],'conflicts':conflicts,
         'release_quality_gate':result['release_quality_gate'],
         'production_path_trace':result['production_path_trace']}
(out/'report.md').write_text(result['result'],encoding='utf-8')
(out/'consistency-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'element-audit.json').write_text(json.dumps([items[k] for k in expected],ensure_ascii=False,indent=2),encoding='utf-8')
(out/'applicability-audit.json').write_text(json.dumps([
    {'rule_id':i['item_id'],'title':i.get('title',i.get('review_point')),
     'applicability':i.get('applicability'),'coverage':i['coverage_status']}
    for i in items.values()],ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'counts':audit['counts'],'overview':audit['overview'],'conflicts':conflicts},ensure_ascii=False))
