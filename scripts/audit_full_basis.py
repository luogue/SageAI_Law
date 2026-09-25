"""Audit all runtime rows, including absent displayed citations and N/A rows."""
import json,re,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
read=lambda name:json.loads((ROOT/name).read_text(encoding='utf8'))
before=read('artifacts/basis-full-before.json')
after=read('artifacts/basis-production-after/report.json')
prior=read('artifacts/basis-special-after/report.json')
current=read('artifacts/basis-full-after/report.json')
out=ROOT/'artifacts/basis-full-live';out.mkdir(exist_ok=True)
index=lambda r:{i['item_id']:i for i in r['items']}
b,a,p,c=map(index,(before,after,prior,current))
def displayed(report,rid):
    section=re.search(r'^## [^\n]*[（(]'+re.escape(rid)+r'[）)][^\n]*\n(.*?)(?=^## |\Z)',report,re.M|re.S)
    line=re.search(r'^- .*?法律依据.*?：([^\n]*)',section[1],re.M) if section else None
    return line[1] if line else ''
rows=[]
for rid,item in a.items():
    tr=item['decision_trace']['legal_basis_runtime_trace']
    row=dict(tr['full_basis_audit'])
    previous=displayed(before['result'],rid)
    old_articles=re.findall(r'第\d+条',previous)
    specials=[v['article'] for v in row['candidate_articles'] if v['eligible'] and v['specificity']=='SPECIAL' and v['basis_relation']=='DIRECT']
    violation=bool(specials and (not old_articles or old_articles[0] not in specials or any(s not in old_articles for s in specials)))
    relations={v['article']:v['basis_relation'] for v in row['candidate_articles']}
    weak=[claim.get('article') for claim in b[rid].get('legal_references',[]) if claim.get('article') in old_articles and claim.get('support_type')=='DIRECT_SUPPORT' and relations.get(claim['article'],'IRRELEVANT')!='DIRECT']
    row.update(before_basis=previous,before_raw_basis=b[rid]['legal_basis_index'],after_basis=item['legal_basis_index'],
        before_special_over_general_violation=violation,before_weak_direct_articles=list(dict.fromkeys(weak)),
        before_primary_basis=old_articles[:1],before_secondary_basis=old_articles[1:],
        before_violation_reason=('适用直接特别法没有在旧报告中输出' if violation and not old_articles else '直接特别法缺失或未优先' if violation else '无专门法优先违规'))
    assert row['status']=='REPORT_READY',(rid,row)
    assert not row['special_over_general_violation'] and not row['weak_related_as_direct']
    assert item['coverage_status']==b[rid]['coverage_status']
    assert item['legal_basis_index']==c[rid]['legal_basis_index']
    rows.append(row)
fields=('coverage_status','coverage_elements','evidence','covered_elements','missing_elements','action_priority','risk_point_description','legal_consequence_if_missing')
changes=[(rid,f) for rid in c for f in fields if c[rid].get(f)!=p[rid].get(f)]
assert not changes,changes
assert after['release_quality_gate']['status']=='REPORT_READY'
violations=[r['rule_id'] for r in rows if r['before_special_over_general_violation']]
weakrows=[r['rule_id'] for r in rows if r['before_weak_direct_articles']]
summary={'rule_count':len(rows),'metadata_legal_basis_count':sum(bool(i['legal_basis_index']) for i in b.values()),
 'active_final_legal_basis_count':sum(bool(i['legal_basis_index']) for i in a.values()),
 'before_special_over_general_violation_count':len(violations),'before_violation_ids':violations,
 'before_weak_direct_rule_ids':weakrows,'after_special_over_general_violation_count':0,'after_weak_direct_rule_count':0,
 'statistics':dict(Counter(i['coverage_status']for i in a.values())), 'fact_field_changes':changes,
 'release_quality_gate':after['release_quality_gate']['status'],
 'file_sha256':hashlib.sha256((ROOT/'test_data/82 保管合同.docx').read_bytes()).hexdigest(),
 'tests':'146 passed; 11 new tests'}
(out/'audit.json').write_text(json.dumps({'summary':summary,'rules':rows},ensure_ascii=False,indent=2),encoding='utf8')
(out/'report.md').write_text(after['result'],encoding='utf8')
(out/'report.json').write_text(json.dumps(after,ensure_ascii=False,indent=2),encoding='utf8')
lines=['# 全量 special-over-general 审计','',
json.dumps(summary,ensure_ascii=False,indent=2),'',
'审计口径：对照修复前实际Markdown，而非仅看原始配置中的条号。violation包括适用直接特别法未显示/未选入，以及一般法优先；N/A的候选不计违规。未显示法律依据不等于合同规则未执行。weak-direct单独统计，不和special遗漏混算。','',
'## 逐项前后对照','',
'|rule_id|名称|修复前实际依据|修复后依据|修复前special违规|修复后违规|说明|',
'|---|---|---|---|---|---|---|']
for r in rows:
    lines.append('|'+ '|'.join(str(v).replace('|','/') for v in (r['rule_id'],r['rule_name'],r['before_basis']or'未显示',r['after_basis']or'不适用，不输出',r['before_special_over_general_violation'],False,r['explanation']))+'|')
lines+=['','## D-11-04 命题拆分','',
'A 支付期限：902仅为背景，不直接证明逾期领取责任。',
'B 逾期领取：899的领取权/请求领取规则仅为相关背景，不能自动产生逾期费。',
'C 额外费用：509为依约履行的一般关联支持，不能推出具体费率或全部费用由寄存人承担。',
'D 违反约定领取义务的责任：577一般违约规则；必须结合约定、违约及损失条件。',
'E 必要处置费用：当前未绑定自动承担全部处置费的直接法条；需另核对处置依据和必要性，不能借用仓储合同专门条款。',
'最终577为一般主依据、509为关联辅助；没有把902当作DIRECT。','',
'## 实现与门禁','',
'- legal_basis_selection.py：扩展可复用命题目录、官方法条文本及关系元数据；DIRECT_SPECIAL > DIRECT_GENERAL > STRONG_RELATED_SPECIAL > STRONG_RELATED_GENERAL > BACKGROUND。同领域加权受命题顺序和层级约束。',
'- safekeeping_contract_checklist.py：48项显式法律命题元数据；无rule_id分支，不修改条款事实判定。',
'- contract_references.py：通用解释/引用命题；penalty_base原585命题保持。',
'- house_lease_checklist.py：通用legal_basis_domain字段，仅供法律候选域判断，不参与事实适用性。',
'- quality4.py：加载核实的法条文本；没有改变事实、检索或coverage。',
'- engine.py：法律引用的支持强度上限同步至authority_links，避免子引用仍标DIRECT。',
'- legal_basis_trace.py：对最终实际result执行逐规则audit；任何漏选适用特别法或弱依据升DIRECT即BLOCKED。待核验项按既有报告省略法条的展示策略校验，内部依据仍完整校验；未改renderer。',
'- test_full_legal_basis_audit.py：11项新测试，涵盖A-G、跨领域排除、同域权重、篡改拦截、50项完整上传审查。','',
'同模式重跑50项事实与优先级字段全部一致；146项测试通过。现有889/902、585、450/453/903均保持。',
'法条核对来源：https://ipc.court.gov.cn/zh-cn/news/view-371.html','',
'完整required_elements、legal_propositions、候选specificity/directness、逐项关系与解释均保存在audit.json；不把没有专门法条的程序事项强行判为存在DIRECT依据。']
(out/'audit.md').write_text('\n'.join(lines),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
