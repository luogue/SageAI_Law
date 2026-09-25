"""Final construction-only acceptance; preserve prior rounds and engine protocol."""
import asyncio
import io
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
OUT = ROOT / 'artifacts/construction_final'


async def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT / 'backend/.env')
    from routers.review_v2 import review_v2_file, ReviewV2Result
    from review_v2.report_statistics import statistics_gate
    from review_v2.construction_coverage import coverage_failures
    from review_v2.construction_evidence import EXTERNAL_NODES, evidence_failures

    path = ROOT / 'test_data/50 建设工程.docx'
    upload = type('Upload', (), {'filename': path.name, 'file': io.BytesIO(path.read_bytes())})()
    result = await review_v2_file(file=upload, contract_type='construction', include_low_risk=True,
                                 use_llm=True, profile_json='{}', current_user={'id': 1})
    api = ReviewV2Result(**result).model_dump()
    (OUT / 'after.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    rows = {r['item_id']: r for r in result['items']}
    items = [SimpleNamespace(**r) for r in result['items']]
    permit = rows['CE-13-03']
    external = [r for r in rows.values() if r['node_id'] in EXTERNAL_NODES]
    checks = {
        '52_statuses_closed': len(rows) == sum(result['coverage_summary'].values()) == 52,
        'summary_recalculable': statistics_gate(result)['status'] == 'REPORT_READY',
        'external_fact_consistency': len(external) == 6 and all(r['coverage_status'] == '待核验' and r['needs_manual_review'] for r in external),
        'permit_optional_only': permit['risk_severity'] == 'LOW' and permit['action_priority'] == 'C_OPTIMIZATION' and result['final_overview_summary']['recommended_action'] == 0,
        'pass_evidence_semantics_and_location': not coverage_failures(items),
        'completion_direct_location': all(e['location'] == '第二部分 通用条款 / 10.4' for e in rows['CE-07-02']['evidence_clauses']) and bool(rows['CE-07-02']['evidence_clauses']),
        'risk_direct_evidence': not evidence_failures(items),
        'previous_cross_clause_regressions': all(rows[k]['coverage_status'] == '通过' for k in ('CE-12-02', 'CE-12-03', 'CE-12-04', 'CE-13-01', 'CE-11-03', 'CE-13-04')),
        'previous_negation_regressions': all(rows[k]['coverage_status'] == '通过' and not rows[k]['evidence_clauses'] for k in ('CE-05-01', 'CE-06-01', 'CE-10-03')),
        'engine_release_gate': result['release_quality_gate']['status'] == 'REPORT_READY',
        'api_audit_preserved': api['statistics_consistency_gate'] == result['statistics_consistency_gate'],
    }
    cases = list(ET.parse(OUT / 'regression.xml').iter('testcase'))
    failed = [c.attrib['name'] for c in cases if c.find('failure') is not None or c.find('error') is not None]
    checks['construction_regression_tests'] = bool(cases) and not failed
    acceptance = {'release_quality_gate': 'PASSED' if all(checks.values()) else 'BLOCKED',
                  'scope': '建设工程本轮验收及既有建设工程回归；不代表其他合同域的全项目发布验收',
                  'engine_protocol_status': result['release_quality_gate']['status'],
                  'checks': checks, 'tests_passed': len(cases) - len(failed), 'tests_failed': failed,
                  'coverage_summary': result['coverage_summary'], 'manual_review_count': len(result['manual_review_items']),
                  'model_sources': result['judge_source_summary']}
    (OUT / 'acceptance.json').write_text(json.dumps(acceptance, ensure_ascii=False, indent=2), encoding='utf-8')
    before = json.loads((OUT / 'before.json').read_text(encoding='utf-8'))
    old = {r['item_id']: r for r in before['items']}
    lines = ['# 建设工程最终收尾验收', '', f"release_quality_gate={acceptance['release_quality_gate']}", '',
             '验收限定本轮建设工程及既有建设工程回归。引擎既有成功协议值 REPORT_READY 保持兼容，验收状态使用 PASSED/BLOCKED。', '',
             f"回归测试：{acceptance['tests_passed']} 通过，{len(failed)} 失败。", '',
             '修复前：' + json.dumps(before['coverage_summary'], ensure_ascii=False),
             '修复后：' + json.dumps(result['coverage_summary'], ensure_ascii=False),
             f"人工复核：{len(before['manual_review_items'])} → {len(result['manual_review_items'])}。", '',
             'CE-13-03 保留附件部分覆盖事实，风险改为 LOW / C_OPTIMIZATION；不再推动建议修改后签署。真实许可异常、责任或开工条件缺失不享受此豁免。', '',
             'CE-02-03、CE-03-03 从文本未命中通过改为待核验。直接不利约定仍保留风险条款与原文证据，并要求核验。CE-03-02 明确命名为“中标文件纳入合同”，不宣称实际中标有效。', '',
             'CE-07-02 使用通用条款 10.4 实际竣工日期认定；同时清理其他 PASS 项的标题、相邻引用、主体错配和非同类行为证据。', '',
             '| 校验 | 结果 |', '|---|---|', *[f"| {k} | {'PASS' if v else 'FAIL'} |" for k,v in checks.items()], '',
             '| 规则 | 原状态 | 现状态 | 风险/处理 | 当前证据位置 |', '|---|---|---|---|---|']
    for key, row in rows.items():
        locations = '；'.join(dict.fromkeys(e.get('location', '') for e in row['evidence_clauses']))
        lines.append(f"| {key} {row['title']} | {old[key]['coverage_status']} | {row['coverage_status']} | {row['risk_severity']} / {row['action_priority']} | {locations or '不引用无关条款'} |")
    (OUT / 'diff.md').write_text('\n'.join(lines), encoding='utf-8')
    (OUT / 'report.md').write_text(result['result'], encoding='utf-8')
    print(json.dumps(acceptance, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
