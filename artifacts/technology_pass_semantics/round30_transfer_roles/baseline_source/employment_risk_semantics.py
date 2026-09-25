"""Source-bound risk atoms shared by rule views, themes and release checks."""
import hashlib
import json

# Legal exposures are independent of rule IDs and of contract wording.
CATALOG = {
 'dispatch.onward_assignment':('onward_dispatch','用工单位再次派遣至其他用人单位','删除用工单位直接再次派遣的授权，依法核实新实际用工主体及派遣安排'),
 'dispatch.return_terms':('dispatch_return_basis','用工单位退回条件约定过宽','按法定事由和程序限制退回，不以普通绩效、主观匹配或单纯组织调整直接退回'),
 'worker.security_payment':('worker_charge','违法向劳动者收取保证金或从工资扣收费用','取消押金保证金收费及工资扣收，返还已收款项并结清工资'),
 'job.change_terms': ('employment_conditions_change','单方变更岗位或薪酬权限过宽','明确协商变更及合理调岗边界，删除任意降薪和拒绝任意调岗即违纪的安排'),
 'discipline.dismissal_terms': ('disciplinary_proportionality','违纪认定与直接解除条件过宽','结合行为情节、影响及合法制度判断严重程度，删除机械认定并直接解除的安排'),
 'contract.term_limit_mode': ('termination_discretion','用人单位单方认定任务完成并终止','明确客观任务完成标准、验收和确认程序，删除任意终止授权'),
 'termination.employer_unrestricted': ('termination_discretion','用人单位任意解除或终止','限定法定解除终止事由及程序'),
 'economic_compensation.waived': ('compensation_exclusion','排除法定经济补偿','删除排除法定经济补偿的约定，按法定情形计算并结算'),
 'economic_compensation.reduced': ('compensation_reduction','降低法定经济补偿','按法定标准计算经济补偿'),
 'capability.ground': ('capability_ground','仅凭绩效排名认定不能胜任','以实质工作能力认定不能胜任，不以排名末位直接替代'),
 'capability.training': ('capability_remediation','排除不能胜任解除的培训或调岗程序','保留培训或调岗及再次不能胜任的法定前提'),
 'capability.reassignment': ('capability_remediation','排除不能胜任解除的培训或调岗程序','保留培训或调岗及再次不能胜任的法定前提'),
 'capability.reassessment': ('capability_reassessment','跳过再次不能胜任条件','保留培训或调岗后仍不能胜任的条件'),
 'capability.notice': ('capability_notice','排除不能胜任解除的通知保障','依法提前书面通知或支付代通知金'),
 'capability.compensation': ('compensation_exclusion','不能胜任解除排除经济补偿','不能胜任解除依法支付经济补偿'),
}


def semantic_policy(store, fact):
 concept=fact['concept'];value=fact['normalized_value']
 task='TASK' in store.values('contract.type')
 if task and concept in {'contract.type','probation.arrangement','probation.duration_months','probation.start_date','probation.end_date'}:
  return ('task_probation_prohibited','以完成一定工作任务为期限劳动合同不得约定试用期','删除试用期约定，不以缩短试用期或调整试用工资使其合法化')
 if concept=='economic_compensation.statutory':
  if value['kind'] not in {'WAIVED','EXCLUDED'}:return None
  concept='economic_compensation.waived'
 if concept=='economic_compensation.waived' and task and store.get('contract.task_end'):
  return ('compensation_exclusion','排除法定经济补偿','删除免除经济补偿的约定，并按法律规定在工作任务完成导致合同终止时依法处理经济补偿')
 return CATALOG.get(concept)

def annotate(store, rows):
 for row in rows:
  fact=store.by_id.get(row.get('structured_fact_id'))
  policy=semantic_policy(store,fact) if fact else None
  if not policy:continue
  exposure,title,remedy=policy
  value=fact['normalized_value']
  # Only adverse usages of the multivalent deadline concept have this meaning.
  if fact['concept']=='contract.term_limit_mode' and value!='EMPLOYER_DETERMINED_COMPLETION': continue
  identity=hashlib.sha256(json.dumps([fact['concept'],value],sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:20]
  row['adverse_fact_atom']={'fact':identity,'scope':store.hash,'actor':'EMPLOYER','object':'EMPLOYMENT_RELATION',
   'legal_exposure':exposure,'remedy':remedy,'title':title,'summary':title,'recommendation':remedy,
   'evidence_ids':[fact['fact_id']], 'fact_concept':fact['concept']}
 return rows

def project_item(item):
 rows=item.evidence_clauses or []
 atoms=[r.get('adverse_fact_atom') for r in rows]
 if item.coverage_status!='风险条款' or not atoms or not all(atoms): return
 titles=list(dict.fromkeys(a['title'] for a in atoms))
 from review_v2.employment_fact_store import current
 store=current()
 exposures={a['legal_exposure'] for a in atoms}
 if 'task_probation_prohibited' in exposures or ('compensation_exclusion' in exposures and store and 'TASK' in store.values('contract.type') and store.get('contract.task_end')):
  item.risk_level='高'
 item.title='；'.join(titles)
 item.risk_point_description='；'.join(dict.fromkeys(a['summary'] for a in atoms))+'。'
 item.reasoning_summary=item.risk_point_description
 item.suggested_clause_example='建议'+'；'.join(dict.fromkeys(a['recommendation'] for a in atoms))+'。'
 item.action_suggestion=item.suggested_clause_example
 item.decision_trace['risk_semantic_contract']={'title':item.title,'conclusion':item.risk_point_description,'recommendation_action':'；'.join(dict.fromkeys(a['recommendation'] for a in atoms)),
   'required_exposures':list(dict.fromkeys(a['legal_exposure'] for a in atoms))}

def consistency_failures(items):
 from review_v2.employment_fact_store import current
 store=current()
 failures=[]
 for item in items:
  contract=(item.decision_trace or {}).get('risk_semantic_contract')
  if not contract: continue
  supported=set()
  for row in item.evidence_clauses or []:
   atom=row.get('adverse_fact_atom') or {}
   fact=store.by_id.get(row.get('structured_fact_id')) if store else None
   if fact and row.get('verified_original') and any(e['quote']==row.get('quote') and e['clause_id']==row.get('clause_id') for e in fact['evidence']):
    expected=semantic_policy(store,fact)
    if expected and atom.get('legal_exposure')==expected[0]: supported.add(expected[0])
  if item.title!=contract['title'] or item.risk_point_description!=contract['conclusion'] or not set(contract['required_exposures'])<=supported:
   failures.append({'requirement':'RISK_TITLE_EVIDENCE_CONSISTENCY','review_id':item.item_id,
     'failure_stage':'Risk semantic projection','current_status':'FAIL','root_cause':'风险标题或结论超出已验证原文支持的法律事实。'})
 return failures
