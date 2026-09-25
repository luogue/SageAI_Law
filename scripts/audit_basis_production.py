"""Compare captured real responses; preserve report bytes and original legal metadata."""
import json,re,hashlib,sys,subprocess
from pathlib import Path
from collections import Counter
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'backend'))
from review_v2.legal_basis_selection import select
out=ROOT/'artifacts/basis-production-after'
b=json.loads((ROOT/'artifacts/basis-production-before/result-20908-e17cf8580ba442be88e27a24d6a196ad.json').read_text(encoding='utf8'))
a=json.loads((out/'report.json').read_text(encoding='utf8'))
integration=json.loads((ROOT/'artifacts/safekeeping-basis-after/report.json').read_text(encoding='utf8'))
ids=['D-04-02','D-04-03','D-09-02','D-09-04']
bm={i['item_id']:i for i in b['items']};am={i['item_id']:i for i in a['items']};im={i['item_id']:i for i in integration['items']}
def md_basis(report,rid):
    section=re.search(r'^## [^\n]*[（(]'+re.escape(rid)+r'[）)][^\n]*\n(.*?)(?=^## |\Z)',report,re.M|re.S)
    match=re.search(r'^- .*?法律依据.*?：([^\n]*)',section[1],re.M) if section else None
    return match[1] if match else ''
trace={}
for rid in ids:
    bt=bm[rid]['decision_trace']['legal_basis_runtime_trace'];at=am[rid]['decision_trace']['legal_basis_runtime_trace']
    unit=SimpleNamespace(legal_basis_index='',decision_trace={'legal_basis_runtime_trace':{'stages':[]}})
    select(unit,SimpleNamespace(**at['runtime_rule_metadata']))
    assert unit.legal_basis_index==im[rid]['legal_basis_index']==am[rid]['legal_basis_index']==md_basis(a['result'],rid)
    trace[rid]={'before':bt,'after':at,'before_actual_markdown':md_basis(b['result'],rid),
                'unit_integration_production_equal':True,
                'before_candidate_score':'NOT_COMPUTED: old path performed authority existence/support filtering, not proposition ranking'}
changes=[rid for rid in am if rid not in bm or am[rid]['coverage_status']!=bm[rid]['coverage_status']]
assert not changes,changes
fact_changes=[(rid,field) for rid in am for field in ('coverage_elements','evidence','covered_elements','missing_elements') if am[rid].get(field)!=bm[rid].get(field)]
assert not fact_changes,fact_changes
assert a['release_quality_gate']['status']=='REPORT_READY',a['release_quality_gate']['failures']
sha=lambda text:hashlib.sha256(text.encode()).hexdigest()
assert sha(b['result'])!=sha(a['result'])
runtime=a['production_path_trace']
verification={'source_sha256':hashlib.sha256((ROOT/'test_data/82 保管合同.docx').read_bytes()).hexdigest(),
    'report_before_sha256':sha(b['result']),'report_after_sha256':sha(a['result']),
    'coverage_counts':dict(Counter(i['coverage_status'] for i in a['items'])),'coverage_changes':changes,'fact_field_changes':fact_changes,
    'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'production_path_trace':runtime,'release_quality_gate':a['release_quality_gate'],
    'request_profile':b['profile'],'normalized_response_profile':a['profile'],
    'notes':'Same file and original request profile. Current runtime normalizes the profile to deposit roles; this concurrent change is outside this legal-basis patch.'}
(out/'legal-basis-trace.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf8')
(out/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf8')
lines=['# Legal basis 生产路径诊断','',
'实际入口：`http://localhost:5173/review-v2/file` → Vite代理8016 → `routers.review_v2.review_v2_file` → `engine.review_contract_v2`。',
f"PID：{runtime['process_id']}；工作目录：{runtime['working_directory']}；commit：{verification['commit']}。工作区含未提交变更，具体版本以 runtime_sources 的逐文件 SHA256 为准。",'',
'根因：原始 Python checklist 四项均预置903；结果初始化复制静态 legal_basis；旧引用校验本地库缺少889/902/448/453，903存在并被默认直接支持；展示阶段只保留通过校验的引用，导致903被留下。未发现这四项在生产路径上已有命题选择后被旧 mapping 覆盖。此前的 proposition 检索仅覆盖其他事项。',
'不是旧缓存：修复前已为 CURRENT，原始配置和运行时值一致。当前入口不复用审查/证据/报告结果缓存，cache=MISS；这四项读取 Python checklist 与本地法条库，未发现其读取 compiled JSON、SQLite registry、snapshot 或生成代码。重启清除进程内旧模块；没有删除结果文件。','',
'修复：为原规则绑定明确法律命题，校验对应条文后先写入 result.legal_basis_index，再生成引用。renderer 读取已选结果，不再对这四项静态索引二次选择；最终门禁逐项比对 selected/result/Markdown。新增模块纳入运行时源码漂移门禁。未修改事实抽取、检索、coverage 或相关 required elements。',
'relevance_score 是透明的离散绑定值（100=明确命题对应；0=无目标命题），不是模型相似度。旧路径没有数值评分，不能补造旧 relevance score。','',
'|规则|修复前实际Markdown|修复后实际Markdown|','|---|---|---|']
for rid,t in trace.items():lines.append(f"|{rid}|{t['before_actual_markdown']}|{md_basis(a['result'],rid)}|")
lines+=['','法律边界：450只直接规定可分物留置价值与债务金额相当；448为同一法律关系要求；453为留置后的履行期限及实现程序，不能宣称它规定了一律事前通知义务；903仅支持保管人留置权来源，不能直接支持费用金额/计费/凭证。509、510在额外费用事项中属于一般履行/补充解释支持，未宣称其直接规定所有费用凭证程序。',
'官方原文：https://www.court.gov.cn/zixun/xiangqing/233181.html','']
for rid,t in trace.items():
    at=t['after'];bt=t['before'];meta=at['runtime_rule_metadata']
    lines += [f'## {rid}', '', '原配置来源：'+json.dumps(at['rule_source'],ensure_ascii=False),
        '实际 requirement：'+meta['semantic_question'],
        '实际 required elements（保持原定义；部分旧规则为单一复合描述，未伪造已拆分的A/B/C）：'+json.dumps(at['required_elements'],ensure_ascii=False),
        'legal propositions：'+json.dumps(at['legal_propositions'],ensure_ascii=False),
        'candidate articles / score / validation：'+json.dumps(at['candidate_articles'],ensure_ascii=False),
        'primary_basis：'+str(at['primary_basis'])+'；secondary_basis：'+str(at['secondary_basis']), '',
        '|阶段|SOURCE_FILE|SOURCE_FIELD|VALUE_BEFORE|VALUE_AFTER|','|---|---|---|---|---|']
    for label,tr in [('before',bt),('after',at)]:
        for s in tr['stages']:
            lines.append('|'+ '|'.join(str(x).replace('|','/') for x in [label+':'+s['STAGE'],s['SOURCE_FILE'],s['SOURCE_FIELD'],s['VALUE_BEFORE'],s['VALUE_AFTER']])+'|')
    lines += [f"|actual Markdown|engine.py::_format_markdown_v2|法律依据|{t['before_actual_markdown']}|{md_basis(a['result'],rid)}|",'']
lines += ['## 修改文件','',
'- backend/review_v2/legal_basis_selection.py：明确命题选择及候选追踪。',
'- backend/review_v2/legal_basis_trace.py：生产阶段快照与最终投影门禁。',
'- backend/review_v2/engine.py：接入选择、引用支持强度上限及renderer读取结果。',
'- backend/review_v2/house_lease_checklist.py：通用checkpoint增加legal_basis_topics字段。',
'- backend/review_v2/safekeeping_contract_checklist.py：仅四项法律命题metadata，原始依据保留用于追踪。',
'- backend/review_v2/quality4.py：补全官方450/448/453/902/510法条记录。',
'- backend/routers/review_v2.py：新法律模块纳入源码漂移检测。',
'- backend/tests/test_legal_basis_production_path.py：14项路径回归。',
'- scripts/run_basis_live.py、scripts/audit_basis_production.py：真实代理重放及前后审计。','',
'## 验证','',
'新增14项回归（包含真实上传路由、四项最终Markdown、unit与integration一致、动态metadata消费、renderer旧引用不覆盖、覆盖篡改阻断、源码漂移阻断、903费用词负例）；连同历史回归123项通过，7个依赖/弃用警告。',
'实际HTTP重跑与单元/集成的四项法律依据完全一致；当前50项：39 PASS、2 PARTIAL、3 MISSING、6 N/A。全部50项 coverage、coverage_elements、evidence、covered_elements、missing_elements 与修复前一致。',
'release_quality_gate=REPORT_READY；完整原始响应见 report.json，未编辑报告正文见 report.md，完整机器追踪见 legal-basis-trace.json，运行时源码指纹见 verification.json。',
'请求仍发送原始画像；当前工作区另有并发画像归一化变更，响应画像被规范为寄存人/保管，此项已单独记录，不冒称由本补丁修复。']
(out/'diagnosis.md').write_text('\n'.join(lines),encoding='utf8')
print(json.dumps({k:v for k,v in verification.items() if k in ['report_before_sha256','report_after_sha256','coverage_counts','coverage_changes']},ensure_ascii=False))
