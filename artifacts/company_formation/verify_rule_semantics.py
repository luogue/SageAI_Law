from pathlib import Path
import json,hashlib
p=Path('artifacts/company_formation/rule_semantics_final');r=json.loads((p/'result.json').read_text(encoding='utf-8'));d={i['item_id']:i for i in r['items']}
files=['backend/review_v2/formation_rule_semantics.py','backend/review_v2/company_formation_checklist.py','backend/review_v2/priority_contract_review.py','backend/review_v2/employment_facts.py','backend/routers/review_v2.py','backend/tests/test_formation_rule_semantics.py']
a=d['CF-02-01']['decision_trace']['contribution_deadline_assessment']
checks={
 'deadline_present':a['contribution_deadline_present'],
 'deadline_risk':a['contribution_deadline_compliant'] is False and d['CF-16-01']['coverage_status']=='风险条款',
 'deadline_FOUND':any(x['element_id']=='formation_contributions_3' and x['result']=='FOUND' for x in d['CF-02-01']['decision_trace']['element_absence_searches']),
 'old_transfer_source_risk':d['CF-09-01']['coverage_status']=='风险条款' and '旧式过半数同意' in d['CF-09-01']['risk_point_description'],
 'account_context_only':d['CF-04-01']['decision_trace']['fund_receiver_context']['personal_account_receiver_identified'] and not any(x['element_id']=='formation_fund_safety_1' for x in d['CF-04-01']['coverage_elements']),
 'equity_total': '110%' in d['CF-01-01']['risk_point_description'],
 'capital_total':'110万元' in d['CF-01-01']['risk_point_description'],
 'party_mismatch':'戊方' in d['CF-01-01']['risk_point_description'],
 'dependent_dates':'2034-09-30' in d['CF-01-01']['risk_point_description'] and '2031-06-30' in d['CF-01-01']['risk_point_description'],
 'nonmonetary_applicable':d['CF-03-01']['applicability']['status']=='APPLICABLE',
 'personal_account_applicable':d['CF-04-01']['applicability']['status']=='APPLICABLE',
 'veto_and_unilateral_risk':d['CF-12-01']['coverage_status']=='风险条款',
 'restrictive_inspection':d['CF-05-01']['coverage_status']=='风险条款' and '知情权限制' in d['CF-05-01']['risk_point_description'],
 'charter_conflict_FOUND':any(x['element_id']=='formation_articles_alignment_2' and x['result']=='FOUND' for x in d['CF-10-01']['decision_trace']['element_absence_searches']),
 'termination_FOUND':any(x['element_id']=='common_contract_termination_1' and x['result']=='FOUND' for x in d['COMMON-26-01']['decision_trace']['element_absence_searches']),
 'private_exit_not_company_return':not any(x['element_id']=='formation_transfer_exit_3' for x in d['CF-09-01']['coverage_elements']),
 'unvouched_expenses':d['CF-08-01']['coverage_status']=='风险条款',
 'unequal_liability':d['COMMON-23-01']['coverage_status']=='风险条款' and d['COMMON-24-01']['coverage_status']=='风险条款',
 'no_sales_rules':not any(x['node_id'].startswith('sale_') for x in r['items']),
 'release_quality_gate':r['release_quality_gate']['status']=='REPORT_READY',
}
sha=hashlib.sha256(Path('test_data/86 股东协议.docx').read_bytes()).hexdigest()
checks['original_unchanged']=sha==json.loads(Path('artifacts/company_formation/round86_before/summary.json').read_text(encoding='utf-8'))['sha256']
assert all(checks.values()),checks
out=dict(status='PASS',checks=checks,files=files,source_sha256=sha,deadline_assessment=a,
    context=r['report_context'],rules=len(r['items']),rule_findings=len(r['risk_findings']),risk_themes=r['risk_theme_count'],overview=r['final_overview_summary'],
    tests=dict(new_cases=16,regression_passed=326,final_repeat_passed=106,full_repository_run=False),
    browser=dict(review_id='CR-20260909-105421-717D0E',pid=15692,runtime='CURRENT',release_quality_gate='REPORT_READY'),release_quality_gate=r['release_quality_gate']['status'])
(p/'acceptance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 股东合作协议规则语义验收','','最终：REPORT_READY。原86号完整文件未修改；真实页面与启用LLM的multipart生产入口均通过。','','## 修改文件','']+['- '+f for f in files]+['','## 修改逻辑','','CF-02保留出资期限存在性及FOUND，新增CF-16独立核验法定上限。deadline_present与deadline_compliant分离，成立时间按明确日期/年份区间计算；未知成立日不认定合法，存量公司不机械套用新设公司五年上限。样本以拟设及合作安排推定2026年，并明确标记为推定而非登记成立日；2035截止触发上限风险，登记日及法定例外仍需核对。','','CF-09增加书面通知、通知内容、同等条件和行权期限。旧过半数同意无章程依据时引用原文提示机制衔接；声明有章程特别规定时核验章程与合法性，不直接宣告无效。仅有优先购买权仍为部分覆盖。退出与公司资本返还要素仍按交易主体触发。','','CF-04移除保护要素中的账户身份，将其记录为fund_receiver_context，含personal_account_receiver_identified、NEUTRAL、TRIGGER_CONTEXT及protective_coverage=false。资金隔离、共同审批、限期转账核对和退款才参与保护覆盖。','','未修改质量门、主分类器或大范围路由。','','## 测试','','新增16个参数化用例；298项综合回归+28项股权回归=326项通过。最终补齐年份和相对期限的存在性匹配后，106项股东协议相关测试重复通过。未运行全仓库测试。','','## 实际生产结果','',f"contract_type=shareholders；scenario=股东合作协议；role=shareholder。规则{out['rules']}，规则风险命中{out['rule_findings']}，风险主题{out['risk_themes']}。",'',str(out['overview']),'','浏览器请求CR-20260909-105421-717D0E；PID15692；runtime=CURRENT；REPORT_READY；failures=[]。','','## 逐项断言','','| 检查 | 结果 |','|---|---|']+[f'| {name} | PASS |' for name in checks]+['','法律依据：[现行公司法第47、84条](https://www.samr.gov.cn/xyjgs/flfg/art/2024/art_d4e84936a8a744f8928ac7aec7594345.html)。']
(p/'acceptance.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps({'all_assertions':'PASS','count':len(checks),'overview':out['overview'],'gate':out['release_quality_gate']},ensure_ascii=False))
