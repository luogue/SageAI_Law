"""Produce the current upload-path report and a machine-checkable comparison."""
import asyncio
import io
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
OUT = ROOT / 'artifacts/lease_evidence_consistency'


async def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT / 'backend/.env')
    from routers.review_v2 import review_v2_file
    from review_v2.report_statistics import statistics_gate
    path = ROOT / 'test_data/53 租赁合同.docx'
    upload = type('Upload', (), {'filename': path.name, 'file': io.BytesIO(path.read_bytes())})()
    result = await review_v2_file(file=upload, contract_type='lease', include_low_risk=True,
                                 use_llm=True, profile_json='{}', current_user={'id': 1})
    (OUT / 'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'report.md').write_text(result['result'], encoding='utf-8')
    old = json.loads((OUT / 'before.json').read_text(encoding='utf-8'))
    cases = list(ET.parse(OUT / 'regression.xml').iter('testcase'))
    failures = [c.attrib['name'] for c in cases if c.find('failure') is not None or c.find('error') is not None]
    contamination = [t for t in ('停用、下架', '替换成本', '对出卖人', '出卖人追偿') if t in result['result']]
    ready = (not failures and not contamination and result['release_quality_gate']['status'] == 'REPORT_READY'
             and statistics_gate(result)['status'] == 'REPORT_READY')
    acceptance = dict(release_quality_gate='PASSED' if ready else 'BLOCKED',
                      tests_passed=len(cases)-len(failures), tests_failed=failures,
                      domain_contamination=contamination, coverage=result['coverage_summary'],
                      overview=result['final_overview_summary'], report_gate=result['release_quality_gate'])
    (OUT / 'acceptance.json').write_text(json.dumps(acceptance, ensure_ascii=False, indent=2), encoding='utf-8')
    old_items = {i['node_id']: i for i in old['items']}
    lines = ['# 房屋租赁证据—状态一致性修复复测', '',
             '根因：旧 PASS 未受最终要素真值约束；缺失检索另用字面词，未共享正向关系谓词；维修事实使用同主题词共现，误召回转租违约；侵权后果模板未区分合同类型。', '',
             '修复：统一正向事实召回与搜索审计，按必要要素聚合状态；维修费用拆分必要、合理、实际发生、凭证义务；事实图谱使用相同因果谓词；租赁后果模板按合同域选择。未按 HL 编号或本合同专属文本特判。', '',
             '修改文件：backend/review_v2/engine.py、lease_semantics.py、lease_contract_facts.py；backend/tests/test_lease_evidence_alignment.py、test_review_v2_house_lease.py；scripts/run_lease_evidence_acceptance.py。', '',
             '新增回归覆盖：无正向证据不允许 PASS、无关同主题证据不支持任何要素、supports 与目标要素对齐、搜索审计与正向谓词一致、维修成本原子要素、改编号后仍选择租赁模板、事实图谱来源、明细摘要统计一致。', '',
             '修复前统计：' + json.dumps(old['coverage_summary'], ensure_ascii=False),
             '修复后统计：' + json.dumps(result['coverage_summary'], ensure_ascii=False),
             '修复后风险与建议：' + json.dumps(result['final_overview_summary'], ensure_ascii=False), '',
             '|规则|修复前|修复后|已验证要素及直接引文位置|', '|---|---|---|---|']
    for r in result['items']:
        positive = ['%s：%s' % (e['element_id'], '、'.join(e.get('source_locations', [])))
                    for e in r['coverage_elements'] if e['status'] == 'COVERED']
        lines.append('|%s %s|%s|%s|%s|' % (r['item_id'], r['title'], old_items[r['node_id']]['coverage_status'], r['coverage_status'], '；'.join(positive) or '无已验证正向要素/不适用'))
    lines += ['', '回归通过 %s；失败 %s。release_quality_gate=%s。' % (acceptance['tests_passed'], len(failures), acceptance['release_quality_gate'])]
    (OUT / 'diff.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({k:v for k,v in acceptance.items() if k != 'report_gate'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
