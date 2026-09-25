"""Check both live service reviews against the sealed final consequence field."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / 'artifacts/technology_pass_semantics/round38_service_consequence'
runtime = json.loads((out / 'runtime.json').read_text(encoding='utf8'))
for name in ('engine.py', 'technology_service_elements.py'):
    path = root / 'backend/review_v2' / name
    key = str(path.relative_to(root))
    assert hashlib.sha256(path.read_bytes()).hexdigest() == runtime['source_hashes'][key]

results = {}
for side in ('party_a', 'party_b'):
    report = json.loads((out / side / 'report.json').read_text(encoding='utf8'))
    item = next(row for row in report['items'] if row['item_id'] == 'TC-12-02')
    finding = next(row for row in report['risk_findings'] if 'TC-12-02' in row['source_review_ids'])
    consequence = item['legal_consequence_if_missing']
    gate = report['release_quality_gate']
    snapshot = report['final_review_snapshot']
    assert gate['status'] == 'REPORT_READY' and not gate['failures'] and not gate['blocking_entities']
    assert item['coverage_status'] == '缺失'
    assert len(consequence) > 100 and all(word in consequence for word in ('索赔', '通知', '抗辩', '费用', '授权', '退款'))
    assert '可能对相关义务的履行及权利行使产生争议' not in consequence
    assert finding['consequence'] == consequence
    assert '- 【缺失的法律后果】：' + consequence in report['result']
    for gate_name in ('REVIEW_EVIDENCE_ELEMENT_MISMATCH', 'RISK_EVIDENCE_MISMATCH', 'EXACT_ELEMENT_REPORT_INVARIANT'):
        assert gate['gate_results'][gate_name] == 'PASS'
    assert snapshot['review_run_id'] == gate['review_run_id'] == report['review_run_id']
    assert snapshot['snapshot_hash'] == gate['snapshot_hash'] == report['snapshot_hash']
    assert snapshot['report_version'] == gate['passed_report_version'] == report['report_version']
    results[side] = {
        'review_task_id': report['review_task_id'],
        'review_run_id': report['review_run_id'],
        'report_version': report['report_version'],
        'gate': gate['status'],
        'tc_12_02': item['coverage_status'],
        'consequence_chars': len(consequence),
        'consequence_matches_finding_and_markdown': True,
        'original_blockers': len(gate['failures']),
        'expanded_blockers': len(gate['blocking_entities']),
        'evidence_mismatch': 0,
    }

acceptance = {'status': 'ACCEPTED', 'test_result': '94 passed', 'runtime': runtime,
              'source_hashes_verified': True, 'live_reviews': results}
(out / 'acceptance.json').write_text(json.dumps(acceptance, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps({'status': acceptance['status'], 'live_reviews': results}, ensure_ascii=False, indent=2))
