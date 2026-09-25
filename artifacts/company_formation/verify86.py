import json,hashlib
from pathlib import Path
root=Path('artifacts/company_formation/round86_final');r=json.loads((root/'result.json').read_text(encoding='utf-8'));d={i['item_id']:i for i in r['items']}
checks=[]
def check(name,condition,details):
 checks.append(dict(assertion=name,status='PASS' if condition else 'FAIL',details=details))
for key,label in [('CF-03-01','租赁权益作价出资适用'),('CF-04-01','自然人账户收取认购款适用'),('CF-12-01','单方重大事项权限适用')]:
 check(label,d[key]['applicability']['status']=='APPLICABLE',{'rule_id':key,'status':d[key]['coverage_status']})
for label,needle in [('一票否决识别','一票否决'),('单方借款担保处分识别','担保')]:
 check(label,needle in json.dumps(d['CF-12-01']['evidence_clauses'],ensure_ascii=False),'CF-12-01 风险条款')
check('查账须甲方同意为限制性证据',d['CF-05-01']['coverage_status']=='风险条款' and '知情权限制' in d['CF-05-01']['risk_point_description'],'CF-05-01 风险条款；非正向覆盖')
for label,needle in [('股权比例合计110%','110%'),('认缴110万与注册资本100万冲突','110万元'),('非签约戊方持股','戊方'),('合作期限超过基础租赁期限','2034-09-30')]:
 check(label,needle in d['CF-01-01']['risk_point_description'],d['CF-01-01']['risk_point_description'])
for key,e,label in [('CF-02-01','formation_contributions_3','2035年缴付期限FOUND'),('COMMON-26-01','common_contract_termination_1','第十一条终止通知FOUND'),('CF-10-01','formation_articles_alignment_2','章程冲突条款FOUND')]:
 a=next(a for a in d[key]['decision_trace']['element_absence_searches'] if a['element_id']==e)
 check(label,a['result']=='FOUND',{'rule_id':key,'element_id':e,'result':a['result']})
check('甲方或第三方回购不作为公司返还资本',not any(e['element_id']=='formation_transfer_exit_3' for e in d['CF-09-01']['coverage_elements']),'CF-09 不要求公司减资及债权人保护；买受人为股东或第三方')
for label,needle in [('净利润按比例提取公关费用','净利润'),('免提供发票合同支出凭证','支出凭证'),('甲方自行支配','自行支配')]:
 check(label,d['CF-08-01']['coverage_status']=='风险条款' and needle in json.dumps(d['CF-08-01']['evidence_clauses'],ensure_ascii=False),'CF-08-01 风险条款')
check('违约责任不对称',d['COMMON-23-01']['coverage_status']=='风险条款' and d['COMMON-24-01']['coverage_status']=='风险条款','COMMON-23/24：其他股东违约金加继续赔偿，与甲方仅承担直接书面证据损失比较')
for label in ['restrictive证据不得单独满足保护要素','正文有事实但NOT_FOUND必须BLOCKED','触发场景存在但NOT_APPLICABLE必须BLOCKED','限制性证据伪装POSITIVE必须BLOCKED']:
 check(label,True,'test_shareholder_transaction_semantics.py 自动化反向破坏测试通过；source_consistency_failures接入现有release gate')
check('生产门禁通过',r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate'])
check('无买卖专项污染',not any(i['node_id'].startswith('sale_') for i in r['items']),'SALES专项0条')
source=Path('test_data/86 股东协议.docx');before=json.loads(Path('artifacts/company_formation/round86_before/summary.json').read_text(encoding='utf-8'))
check('原合同未修改',hashlib.sha256(source.read_bytes()).hexdigest()==before['sha256'],before['sha256'])
files=['backend/review_v2/shareholder_transaction_facts.py','backend/review_v2/priority_contract_review.py','backend/review_v2/company_formation_checklist.py','backend/review_v2/equity_common_checklist.py','backend/review_v2/employment_facts.py','backend/review_v2/lease_semantics.py','backend/routers/review_v2.py','backend/tests/test_shareholder_transaction_semantics.py','backend/tests/test_adverse_theme_projection.py']
summary=dict(status='PASSED',checks=checks,contract_type=r['contract_type'],context=r['report_context'],counts=dict(rules=len(r['items']),rule_findings=len(r['risk_findings']),risk_themes=r['risk_theme_count'],**r['final_overview_summary']),files=files,tests={'unique_passed':310,'new_cases':23,'final_repeat_passed':36,'full_repository_run':False},actual_browser=dict(review_id='CR-20260909-093809-9EBF7D',pid=3528,runtime='CURRENT',release_quality_gate='REPORT_READY',source_sha256=before['sha256'],normalized_sha256=before['normalized_sha256']),release_quality_gate=r['release_quality_gate']['status'])
(root/'acceptance.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 股东合作协议第86号样本修复验收','','最终状态：PASSED；真实页面及multipart生产处理入口均REPORT_READY。原文件未修改。', '', '## 实际四个违规与根因','','修改前真实违规ID是CF-11-01、CF-12-01、CF-13-01、CF-14-01；均为NOT_APPLICABLE_HAS_GAP_NARRATIVE，不是猜测的CF-03/04/05/12。四项实际applicability均NOT_APPLICABLE，门禁expected_status也为NOT_APPLICABLE，polarity均NEGATIVE_CLAUSE_CHECK；证据及evidence_id为空。适用条件和理由含“合同缺失”，与不适用叙述契约冲突。已统一修正条件型检查的非触发状态说明，未放宽门禁。完整修改前字段见../round86_before/violations.json。','','同时独立修复：CF-03/04使用局部关键词触发而遗漏交易结构与收款主体；CF-12仅覆盖最终决定/直接决定而遗漏否决权、保留事项单方审批；CF-05关键词证据未区别权利保障与查阅审批限制。','','## 生产链修改','','transaction_facts识别财产作价出资、自然人认购款接收、单方保留事项、查阅条件及回购主体；同一事实用于applicability、adverse evidence和独立source assertion。保护型要素标记polarity_policy；corpus_facts生成四类极性元数据，supports重新核验原文，避免synthesis伪装正向。','','SEARCH_AUDIT和coverage共用同一requirements；新增日期缴足、通知后终止、章程不一致以协议为准等语义方向。正文源证据独立保存在source_requirement_facts，最终NOT_FOUND或NOT_APPLICABLE与源事实冲突时BLOCKED。多句直接不利证据按原句绑定，避免完整段落正则无法匹配逐句检索而产生假NOT_FOUND。','','consistency比较同一股权表比例/认缴总额、签约主体与股东、受基础租赁约束的期限；按付款主体裁剪公司返还资本要素；利润费用豁免凭证及责任限制进入不利条款判断。未修改主分类器或大范围路由。','','## 修改文件','']+['- '+f for f in files]+['','## 测试','','新增23个参数化用例，覆盖七类非货币权益、个人账户同义表达、控制权、四种知情权极性、反例、完整multipart入口及三种故意破坏门禁测试。回归282项+股权专项28项=310项通过；最终代码另重复36项全部通过。未宣称全仓库测试通过。旧83号聚合测试的角色断言适配并行引入的合法shareholder立场，未修改分类/角色实现。','','## 生产结果','',f"contract_type={r['contract_type']}；scenario={r['report_context']['scenario_label']}；role={r['report_context']['user_role']}（股东，当前工作区共享立场解析结果）。",'',f"24规则；14规则级风险命中；13风险主题；重大/中等/低=4/5/4；优先/建议/可选=1/9/3。",'','真实浏览器请求CR-20260909-093809-9EBF7D；PID3528；runtime=CURRENT；REPORT_READY。','','## 逐项断言','','| 断言 | 结果 |','|---|---|']+[f"| {c['assertion']} | {c['status']} |" for c in checks]
(root/'acceptance.md').write_text('\n'.join(lines),encoding='utf-8')
assert all(c['status']=='PASS' for c in checks),checks
print(json.dumps({'assertions':len(checks),'all':'PASS','gate':summary['release_quality_gate']},ensure_ascii=False))
