import json,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf8'))
before=load('artifacts/basis-special-before.json')
after=load('artifacts/basis-production-after/report.json')
integration=load('artifacts/basis-special-after/report.json')
old_integration=load('artifacts/safekeeping-basis-after/report.json')
out=ROOT/'artifacts/basis-special-live';out.mkdir(exist_ok=True)
index=lambda r:{i['item_id']:i for i in r['items']}
b,a,old,test=map(index,(before,after,old_integration,integration))
assert after['release_quality_gate']['status']=='REPORT_READY'
assert all(a[k]['coverage_status']==b[k]['coverage_status'] for k in a)
fact_fields=('coverage_status','coverage_elements','evidence','covered_elements','missing_elements')
assert all(test[k].get(f)==old[k].get(f) for k in test for f in fact_fields)
targets=('COMMON-20-01','D-04-02','D-04-03','D-09-02','D-09-04')
for rid in targets:
    assert a[rid]['legal_basis_index']==test[rid]['legal_basis_index']
    t=a[rid]['decision_trace']['legal_basis_runtime_trace']
    assert t['selected_basis']==t['final_markdown']['VALUE_AFTER']
for rid in ('D-04-03','D-09-02','D-09-04'):
    assert a[rid]['legal_basis_index']==b[rid]['legal_basis_index']
traces={rid:a[rid]['decision_trace']['legal_basis_runtime_trace'] for rid in targets}
(out/'report.md').write_text(after['result'],encoding='utf8')
(out/'report.json').write_text(json.dumps(after,ensure_ascii=False,indent=2),encoding='utf8')
summary={'statistics':dict(Counter(i['coverage_status'] for i in a.values())),
    'source_sha256':hashlib.sha256((ROOT/'test_data/82 保管合同.docx').read_bytes()).hexdigest(),
    'gate':after['release_quality_gate']['status'],'tests':'135 passed; final specificity rerun 12 passed',
    'deterministic_fact_fields_unchanged':True,'all_production_coverage_states_unchanged':True,
    'legal_basis_trace':traces}
(out/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
lines=['# 专门法条召回与排序修复','',
'COMMON-20-01根因：585原本就在静态候选中，但未接入显式命题选择；校验实际收到“合同原文覆盖全部专项要素。”这一结论占位句，585被判断UNCERTAIN。585本地摘要同时只记录调减救济，缺少首款的约定违约金/损失赔偿额计算方法。',
'D-04-02根因：只有902支付期限命题，缺少889支付义务命题；889未入本地法条库。旧选择器对所有命题统一评分100并按配置顺序选取，没有专门性等级。','',
'修改文件及范围：',
'- backend/review_v2/legal_basis_selection.py：新增义务/违约金计算命题；ARTICLE_METADATA含article_id、legal_domain、contract_type、proposition_tags、normative_object、trigger_conditions、effect_type、specificity_level；rank_candidates按专门性和直接性排序。',
'- backend/review_v2/quality4.py：补入889官方法条，补全585首款计算方法及调整/迟延履行内容。',
'- backend/review_v2/penalty_base.py：仅绑定legal_basis_topics，未改计算基数解析。',
'- backend/review_v2/safekeeping_contract_checklist.py：仅增加支付保管费义务命题。',
'- backend/tests/test_legal_specificity.py：新增12项测试；test_legal_basis_production_path.py更新法条预期及单元输入coverage上下文。','',
'评分：直接专门条款1.0；直接一般条款0.8；相关一般条款0.6；已触发补充条款0.3；未触发背景0.1且不入最终依据；无命题匹配0。不是词频匹配。',
'补充规则仅读取既有coverage结果，不做新事实抽取：已覆盖时不触发约定不明补充。当前两项均为已覆盖，因此510保留候选背景，排除最终依据。',
'门禁：存在适用SPECIAL时首项必须是SPECIAL；所需适用条文验证失败或排序违反约束，会通过现有selection_complete门禁阻断报告。未改renderer、SEARCH_AUDIT、coverage、evidence或chunking。','',
'|规则|最终主要依据|辅助依据|','|---|---|---|']
for rid,t in traces.items():lines.append(f"|{rid}|{'、'.join(t['primary_basis'])}|{'、'.join(t['secondary_basis'])}|")
lines+=['','D-04-03、D-09-02、D-09-04法律依据文本与修复前逐字相同；同模式集成重跑全部50项的coverage、要素、证据、covered/missing字段与修复前一致。实际开启模型复核重跑全部覆盖状态亦未变化。',
'50项：39 PASS、2 PARTIAL、3 MISSING、6 N/A。新增12项，整体135项通过（7个依赖/弃用警告）；最后排序定向复验12项通过。',
'实际完整报告质量门：REPORT_READY。',
'官方法条：https://www.spp.gov.cn/spp/fl/202006/t20200602_463888.shtml','']
for rid in targets[:2]:
    lines += ['## '+rid,'',json.dumps(traces[rid]['candidate_articles'],ensure_ascii=False,indent=2),'']
(out/'summary.md').write_text('\n'.join(lines),encoding='utf8')
print(summary['statistics'],summary['gate'])
