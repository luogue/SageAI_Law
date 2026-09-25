"""Repeat the same upload twice; preserve the explicit release hold."""
import asyncio
import hashlib
import io
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/lease_final_children'
sys.path.insert(0, str(ROOT / 'backend'))


def core_projection(result, profiles):
    return {i['node_id']: [i['coverage_status'], sorted(
        (e['element_id'], e['status'], e.get('source_locations', []), e.get('source_spans', []))
        for e in i['coverage_elements'])] for i in result['items'] if i['node_id'] in profiles}


async def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT / 'backend/.env')
    from routers.review_v2 import review_v2_file
    from review_v2.lease_semantics import PROFILES
    path = ROOT / 'test_data/53 租赁合同.docx'
    results = []
    for index in (1, 2):
        upload = type('Upload', (), {'filename': path.name, 'file': io.BytesIO(path.read_bytes())})()
        r = await review_v2_file(file=upload, contract_type='lease', include_low_risk=True,
                                use_llm=True, profile_json='{}', current_user={'id': 1})
        (OUT / f'run-{index}.json').write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding='utf-8')
        results.append(r)
        print(f'Completed run {index}: {r["coverage_summary"]}', flush=True)
    a, r = results
    core_equal = core_projection(a, PROFILES) == core_projection(r, PROFILES)
    all_states_equal = {i['node_id']: i['coverage_status'] for i in a['items']} == {i['node_id']: i['coverage_status'] for i in r['items']}
    (OUT / 'report.json').write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'report.md').write_text(r['result'], encoding='utf-8')
    cases = list(ET.parse(OUT / 'regression.xml').iter('testcase'))
    failed = [c.attrib['name'] for c in cases if c.find('failure') is not None or c.find('error') is not None]
    acceptance = {'release_quality_gate': 'BLOCKED', 'release_hold': r.get('release_hold'),
                  'technical_quality_gate': r.get('technical_quality_gate', r['release_quality_gate']),
                  'tests_passed': len(cases)-len(failed), 'tests_failed': failed,
                  'repeat_core_evidence_and_coverage_equal': core_equal,
                  'repeat_all_rule_states_equal': all_states_equal,
                  'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                  'rule_code_sha256': hashlib.sha256(b''.join((ROOT / 'backend/review_v2' / p).read_bytes() for p in
                       ('engine.py', 'lease_semantics.py', 'clause_parser.py', 'recommendation_children.py'))).hexdigest(),
                  'coverage': r['coverage_summary'], 'overview': r['final_overview_summary'],
                  'child_sets': r['recommendation_children_gate'],
                  'model_sources': [x['judge_source_summary'] for x in results]}
    (OUT / 'acceptance.json').write_text(json.dumps(acceptance, ensure_ascii=False, indent=2), encoding='utf-8')
    old = json.loads((OUT / 'before.json').read_text(encoding='utf-8'))
    old_by = {i['item_id']: i for i in old['items']}
    lines = ['# 房屋租赁期限与建议子项复测', '', '**release_quality_gate=BLOCKED，发布保持阻断。**', '',
             '根因：期限匹配漏掉“期限→将押金→返还”的语序；优先购买权依赖模型召回；建议聚合跳过通用复合要素，并按要素名去重，丢失不同规则的来源。未发现本轮问题由缓存命中造成。', '',
             '修改文件：backend/review_v2/lease_semantics.py、engine.py、recommendation_children.py；backend/tests/test_lease_deadline_and_children.py；scripts/run_lease_children_acceptance.py；本地 backend/.env 的租赁发布阻断配置。', '',
             '期限、优先购买权、入住瑕疵通知、异议和损坏举证均以全文语义要素核验；共享建议保留全部规则来源，聚合后增加明细—主题—正式建议—顶部子项集合检查。', '',
             '原报告统计：' + json.dumps(old['coverage_summary'], ensure_ascii=False),
             '新报告统计：' + json.dumps(r['coverage_summary'], ensure_ascii=False),
             f'自动化回归通过 {len(cases)-len(failed)}，失败 {len(failed)}。两次实际上传核心证据及状态一致：{core_equal}；全部规则状态一致：{all_states_equal}。', '',
             '|规则|原报告|新报告|正向证据与检索|', '|---|---|---|---|']
    for i in r['items']:
        audit = '；'.join(f"{e['element_id']}={e['result']}" for e in i['decision_trace'].get('element_absence_searches', []))
        lines.append(f"|{i['item_id']} {i['title']}|{old_by[i['item_id']]['coverage_status']}|{i['coverage_status']}|{i['evidence_location']} {audit}|")
    lines += ['', '建议子项集合：' + json.dumps(r['recommendation_children_gate'], ensure_ascii=False)]
    (OUT / 'diff.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({k:v for k,v in acceptance.items() if k != 'technical_quality_gate'}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    asyncio.run(main())
