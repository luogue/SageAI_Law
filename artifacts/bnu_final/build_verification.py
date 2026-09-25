import json
from pathlib import Path

p = Path(__file__).parent
r = json.loads((p/'result.json').read_text(encoding='utf-8'))
chunks = json.loads((p/'actual_rule_chunks.json').read_text(encoding='utf-8'))
states = {'通过':'PASS', '部分覆盖':'PARTIAL', '缺失':'MISSING', '风险条款':'RISK', '不适用':'N/A'}
labels = {'PROTECTIVE':'保护性条款（不作为风险）', 'STATUTORY':'法定解除事由', 'DISCIPLINARY_VERIFICATION':'可能由合法制度支撑的严重违纪（核验）', 'EXPANDED_RIGHT':'扩张法定解除权', 'MANUAL_VERIFICATION':'需人工核验'}
lines = ['# 北京师范大学固定期限劳动合同复验', '',
         '本轮修改：backend/review_v2/employment_contract_checklist.py、employment_facts.py、employment_exit.py（新增）、priority_contract_review.py、engine.py、lease_semantics.py；backend/routers/review_v2.py；scripts/run_employment_file_acceptance.py；backend/tests/test_employment_complex_prose.py（新增）。', '',
         '输入：63 劳动合同.docx；normalized 3426 字；正文及附件共 64 个 chunks。',
         'release_quality_gate: '+r['release_quality_gate']['status'],
         '实际服务页面保留同份合同；无文件替换、无样本名称或日期特判。', '',
         '## 全部规则', '', '|规则|状态|理由|', '|---|---|---|']
for row in r['items']:
    lines.append(f"|{row['item_id']}|{states[row['coverage_status']]}|{row['reasoning_summary']}|")
lines += ['', '## 解除条款逐款分类', '', '|位置|原文|分类|理由|', '|---|---|---|---|']
exit_row = next(x for x in r['items'] if x['item_id']=='EMP-10-01')
for row in exit_row['decision_trace']['employment_exit_classification']:
    lines.append(f"|{row['location']}|{row['text']}|{labels[row['classification']]}|{row['reason']}|")
lines += ['', '## 指定规则的要素、原文证据与 SEARCH_AUDIT', '']
targets = {'EMP-%02d-01'%n for n in [1,3,4,5,6,7,9,10,11]}
for row in r['items']:
    if row['item_id'] not in targets:
        continue
    corpus_note = f"实际接收 {len(chunks[row['item_id']])} 个 chunks，完整内容见 actual_rule_chunks.json。" if row['item_id'] in chunks else '全文适用性门禁判 N/A，未进入实体要素检索；实际全文见 actual_applicability_inputs.json。'
    lines += ['### '+row['item_id'], '', corpus_note, '', '|要素|状态|证据|', '|---|---|---|']
    for e in row['coverage_elements']:
        quotes = '<br>'.join(e.get('source_spans', [] )).replace('\n','<br>').replace('|','／')
        lines.append(f"|{e['proposition']}|{e['status']}|{quotes}|")
    audits = [{k: a[k] for k in ('element_id', 'result', 'search_targets', 'candidate_count', 'searched_document_hash') if k in a}
              for a in row['decision_trace'].get('element_absence_searches', [])]
    lines += ['', '```json', json.dumps(audits, ensure_ascii=False, indent=2), '```', '']
missing = [{k: a[k] for k in ('rule_id', 'element_id', 'result', 'search_targets') if k in a}
           for a in json.loads((p/'not_found.json').read_text(encoding='utf-8'))]
lines += ['## 所有 NOT FOUND', '', '```json', json.dumps(missing, ensure_ascii=False, indent=2), '```', '',
          '## 仍需保留的边界', '',
          '用人单位住所未见于实际输入；劳动者家庭地址不能替代单位住所。',
          '具体工时、加班安排及社保个人部分代扣代缴未明确；经济补偿交接后支付已识别，法定依据/计算口径未明确。',
          '劳动防护/安全培训未见原文；职业危害情况为待核验，不作为已触发专项义务。',
          '解除分类为文本风险筛查，制度制定、公示、行为严重程度、事实和法定前置条件仍需人工核验。', '',
          '法律依据：[劳动合同法第39、40、42条](https://rsj.gz.gov.cn/zcfg/flfg/content/post_7993969.html)。', '',
          '## 测试', '',
          '相关组合回归 393 项通过；最终劳动专项 92 项通过（含本轮新增 21 项），结果见 ../bnu_employment_final.log。',
          '全量后端回归在 145 项通过后遇到原有技术开发合同 test_current47_production_review_keeps_explicitly_shared_acceptance_and_reference_provenance 的 NARRATIVE_TRUTH_GATE 失败，未宣称全量通过。']
(p/'verification.md').write_text('\n'.join(lines), encoding='utf-8')
print('\n'.join(f"{x['item_id']} {states[x['coverage_status']]}" for x in r['items']))
print('termination rows:', len(exit_row['decision_trace']['employment_exit_classification']))
print('gate:', r['release_quality_gate']['status'])
