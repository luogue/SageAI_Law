"""Rerun the lease upload path and write an auditable before/after report."""
import asyncio
import io
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
OUT = ROOT / 'artifacts/lease_consistency'


async def main():
    from dotenv import load_dotenv
    load_dotenv(ROOT / 'backend/.env')
    from routers.review_v2 import review_v2_file
    path = ROOT / 'test_data/53 租赁合同.docx'
    upload = type('Upload', (), {'filename': path.name, 'file': io.BytesIO(path.read_bytes())})()
    result = await review_v2_file(file=upload, contract_type='lease', include_low_risk=True, use_llm=True,
                                 profile_json='{}', current_user={'id': 1})
    (OUT / 'after_llm.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'report.md').write_text(result['result'], encoding='utf-8')
    before = json.loads((OUT / 'before.json').read_text(encoding='utf-8'))
    old = {r['node_id']: r for r in before['items']}
    cases = list(ET.parse(OUT / 'regression.xml').iter('testcase'))
    failed = [c.attrib['name'] for c in cases if c.find('failure') is not None or c.find('error') is not None]
    acceptance = {'release_quality_gate': 'PASSED' if not failed and result['release_quality_gate']['status'] == 'REPORT_READY' else 'BLOCKED',
                  'report_quality_gate': result['release_quality_gate']['status'], 'test_passed': len(cases)-len(failed),
                  'test_failed': failed, 'coverage': result['coverage_summary'], 'overview': result['final_overview_summary'],
                  'model_sources': result['judge_source_summary']}
    (OUT / 'acceptance.json').write_text(json.dumps(acceptance, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# 租赁合同通用语义一致性修复', '', '修复前为同一 Word 的规则路径快照；修复后为实际上传入口的大模型重跑。', '',
             '根因：旧 PARTIAL 回填与状态单调性保护可绕过要素证据校验；多个规则独立召回相同事实；自然人和无约定补位规则缺少结构化适用条件；经济风险及建议沿用旧判断和模板；风险证据包未完整投影正向要素；N/A 仍进入旧规则风险计数。', '',
             '修改文件：', '- backend/review_v2/engine.py：证据约束、状态保护、风险上限、统一证据投影。',
             '- backend/review_v2/lease_semantics.py：通用关系谓词、全文共享事实、主体与条件适用性、经济暴露证据和一致性门。',
             '- backend/review_v2/clause_parser.py：避免把含逗号的叙述句识别成字段标题。',
             '- backend/review_v2/report_statistics.py：N/A 不计入规则风险数量。',
             '- backend/tests/test_lease_semantic_consistency.py：新增 18 个测试案例，覆盖七类验收要求及改编号、换条款位置、跨事件干扰。',
             '- backend/tests/test_review_v2_house_lease.py：将旧错误 PARTIAL/高风险预期改为证据和要素断言，移除对内部叙述字符串的依赖。',
             '- scripts/run_lease_consistency_acceptance.py：完整文件上传重跑、统计和前后对照。', '',
             '范围：未增加法人注销、合并或分立规则，不以自然人死亡规则代替这些独立法律问题。未知主体类型不会直接判不适用。', '',
             '修复前覆盖：' + json.dumps(before['coverage_summary'], ensure_ascii=False),
             '修复后覆盖：' + json.dumps(result['coverage_summary'], ensure_ascii=False),
             '修复后统计：' + json.dumps(result['final_overview_summary'], ensure_ascii=False), '',
             '原文明确提前退出违约金为两个月租金 76,000 元；该事实不能等同于无金额证据，也不能直接推定重大风险。', '',
             '| 规则 | 修复前 | 修复后 | 证据位置 |', '|---|---|---|---|']
    for row in result['items']:
        locations = '；'.join(dict.fromkeys(e.get('location', '') for e in row['evidence_clauses']))
        lines.append(f"| {row['item_id']} {row['title']} | {old[row['node_id']]['coverage_status']} | {row['coverage_status']} | {locations or '无正向引文/不适用'} |")
    lines += ['', f"回归通过 {acceptance['test_passed']}，失败 {len(failed)}。发布验收：{acceptance['release_quality_gate']}；报告质量门：{acceptance['report_quality_gate']}。", *['- '+f for f in failed]]
    (OUT / 'diff.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(acceptance, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
