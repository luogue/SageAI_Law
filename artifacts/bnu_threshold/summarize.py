import hashlib
import json
from pathlib import Path

p = Path(__file__).parent
r = json.loads((p/'result.json').read_text(encoding='utf-8'))
prior = json.loads((p.parent/'bnu_final/result.json').read_text(encoding='utf-8'))
old = {i['item_id']:i for i in prior['items']}
current = {i['item_id']:i for i in r['items']}
normalized = (p/'normalized_input.txt').read_bytes()
assert normalized == (p.parent/'bnu_final/normalized_input.txt').read_bytes()
changed_rules = {'EMP-07-01','EMP-08-01','EMP-11-01'}
unchanged = []
for key, row in current.items():
    if key in changed_rules:
        continue
    for field in ('coverage_status','risk_severity','action_priority'):
        assert row[field] == old[key][field], (key, field)
    assert [(e['element_id'], e['status'], e.get('source_spans')) for e in row['coverage_elements']] == [(e['element_id'], e['status'], e.get('source_spans')) for e in old[key]['coverage_elements']], key
    unchanged.append(key)
assert current['EMP-10-01']['decision_trace']['employment_exit_classification'] == old['EMP-10-01']['decision_trace']['employment_exit_classification']
states = {'通过':'PASS','缺失':'MISSING','部分覆盖':'PARTIAL','风险条款':'RISK','不适用':'N/A'}
lines = ['# 当前复杂劳动合同：三项风险门槛复验', '',
         '输入仍为 63 劳动合同.docx，normalized 与上轮逐字相同。',
         'normalized SHA256：'+hashlib.sha256(normalized).hexdigest(),
         'release_quality_gate：'+r['release_quality_gate']['status'], '',
         '本轮生产代码修改：employment_contract_checklist.py、priority_contract_review.py、engine.py。没有修改全文检索、附件绑定、日期计算、培训/竞业适用性及解除条款分类器。', '',
         '## 指定六项规则', '', '|规则|覆盖|严重度|处理优先级|', '|---|---|---|---|']
for n in [1,5,7,8,10,11]:
    i = current[f'EMP-{n:02}-01']
    lines.append(f"|{i['item_id']}|{states[i['coverage_status']]}|{i['risk_severity']}|{i['action_priority']}|")
for n in [1,5,7,8,10,11]:
    i = current[f'EMP-{n:02}-01']
    lines += ['', '## '+i['item_id'], '', i['reasoning_summary'], '', '|要素|状态|原文证据|', '|---|---|---|']
    for e in i['coverage_elements']:
        quotes = '<br>'.join(e.get('source_spans') or []).replace('\n','<br>').replace('|','／')
        lines.append(f"|{e['proposition']}|{e['status']}|{quotes or '无直接证据；未补造原文'}|")
    audit = [{k:a[k] for k in ('element_id','result','search_targets') if k in a} for a in i['decision_trace'].get('element_absence_searches', [])]
    lines += ['', 'SEARCH_AUDIT：', '', '```json', json.dumps(audit,ensure_ascii=False,indent=2), '```']
lines += ['', '## 回归不变性', '', '以下16项的覆盖、严重度、处理优先级及要素原文均与上轮一致：', ', '.join(unchanged), '',
          'EMP-10 的逐款分类与上轮完全一致，第二十二条不进入不利证据。', '',
          '## 聚合统计', '', '```json', json.dumps(r['final_disposition_summary'],ensure_ascii=False,indent=2), '```', '',
          '完整证据与诊断见同目录 diagnostics.md、result.json、actual_rule_chunks.json。']
(p/'verification.md').write_text('\n'.join(lines), encoding='utf-8')
print('unchanged rules:',len(unchanged))
print('gate:',r['release_quality_gate']['status'])
