"""Summarize the two captured production uploads, without changing outcomes."""
import json
from pathlib import Path

base=Path('artifacts/property_before')
after=Path('artifacts/property_final')
old=json.loads((base/'report.json').read_text(encoding='utf-8'))
new=json.loads((after/'report.json').read_text(encoding='utf-8'))
old_items={r['item_id']:r for r in old['items']}
new_items={r['item_id']:r for r in new['items']}
lines=['# 物业服务合同生产入口回归对照','',
 '输入：test_data/87 物业服务合同.docx；两次均使用 /review-v2/file 的同一解析、审查、聚合、质量门和报告生成链路。',
 '',f"旧分类：{old['report_context']['contract_type_label']}；新分类：{new['report_context']['contract_type_label']}。",'',
 f"旧覆盖统计：{old['coverage_summary']}",f"新覆盖统计：{new['coverage_summary']}",
 f"风险主题：{len(old['risk_findings'])} → {len(new['risk_findings'])}；审查项：{len(old_items)} → {len(new_items)}。",
 f"质量门：{new['release_quality_gate']['status']}；失败项：{new['release_quality_gate']['failures']}",
 '', '原48项逐项对照（新增的共用法律效果检查另列，不将旧数量写死为新统计）：','',
 '| 审查项 | 名称 | 修复前 | 修复后 | 当前证据位置 |','|---|---|---|---|---|']
for key,a in old_items.items():
    b=new_items.get(key,{})
    loc=str(b.get('evidence_location','')).replace('\n',' ').replace('|','／')
    lines.append(f"| {key} | {a.get('title','')} | {a['coverage_status']} | {b.get('coverage_status','未纳入')} | {loc} |")
lines+=['','## 新增法律效果审查','']
for key,b in new_items.items():
    if key in old_items: continue
    lines += [f"### {key} {b.get('title','')}",'',b['coverage_status'],b.get('reasoning_summary',''),'',str(b.get('legal_basis_index','')),'']
lines+=['## 实际检索和逐要素证据','', '完整记录见同目录 rule_audit.json 与 report.json；以下为关键要素：','']
for key in ['SVC-03-01','SVC-03-02','SVC-06-04','SVC-08-01','SVC-08-02','SVC-11-04','SVC-12-02','COMMON-20-01']:
    b=new_items[key]
    lines += [f'### {key}','',b.get('reasoning_summary',''),'']
    for ev in b.get('evidence_clauses',[]):
        quote=ev.get('quote') or ev.get('text') or ''
        lines += [f"- {ev.get('location','')}：{quote.replace(chr(10),' ')}"]
    lines+=['']
(after/'comparison.md').write_text('\n'.join(lines),encoding='utf-8')
print('\n'.join(lines[:12]))
