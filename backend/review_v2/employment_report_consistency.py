"""Keep formal coverage separate from linked source-supported adverse legality."""
from decimal import InvalidOperation
from review_v2.fact_validation import FactExtractionError

def overlap(a,b):
 if a.get('clause_id')!=b.get('clause_id'):return False
 x=a.get('quote') or a.get('text') or '';y=b.get('quote') or b.get('text') or ''
 return bool(x and y and (x in y or y in x))

def coordinate(items):
 from review_v2.employment_fact_store import current
 if current() is None:return
 for item in items:
  impact=monetary_impact(item)
  if impact:
   item.economic_impact=impact
   item.economic_impact_detail={**(item.economic_impact_detail or {}),'contractual_exposure':exposure_details(item),'actual_loss':None,'actual_loss_status':'NOT_ESTABLISHED','aggregation':'NO_SUMMATION_ACROSS_OBLIGATIONS'}
 risks=[i for i in items if i.coverage_status=='风险条款']
 for item in items:
  if item.coverage_status!='通过':continue
  related=[r.item_id for r in risks if any(overlap(a,b) for a in item.evidence_clauses for b in r.evidence_clauses)]
  if related:
   text='形式要素已覆盖，但相关约定存在风险，见 '+ '、'.join(related)+'；应结合专项风险修改。'
   item.decision_trace['coverage_legality']={'formal_coverage':'COVERED','legality':'RELATED_ADVERSE','related_rule_ids':related,'message':text}
   item.risk_point_description=item.reasoning_summary=item.action_suggestion=text
   item.legal_consequence_if_missing=text
   item.narrative_state={**(item.narrative_state or {}),'judgment':text,'consequence':text,'recommendation':text}


def exposure_details(item):
 from review_v2.employment_fact_store import current,number
 s=current()
 if not s or item.coverage_status!='风险条款':return []
 ids={r.get('structured_fact_id') for r in item.evidence_clauses}
 result=[]
 for key in sorted(k for k in ids if k):
  f=s.by_id.get(key)
  if f and f['concept']=='social_insurance.cash_replacement' and f['normalized_value'] is True:
   result.extend(insurance_exposure(f))
   continue
  if not f or f['concept'] not in {'worker.security_payment','penalties.obligations'}:continue
  v=f['normalized_value'];security=f['concept']=='worker.security_payment'
  if not (v.get('required') is True if security else v.get('imposed',True) is True):continue
  # Consume only this source-verified obligation's own amount expression;
  # never scan the enclosing clause for another obligation's numbers.
  raw=v.get('amount_text')
  if not isinstance(raw,str) or not raw.strip():continue
  try:
   amount=number(raw)
   if not amount.is_finite() or amount<0:continue
   display=format(amount,'f')+'元';fixed=format(amount,'f')
  except (FactExtractionError,InvalidOperation):
   display=raw.strip();fixed=None
  result.append({'fact_id':key,'scope':v.get('scope'),'concept':f['concept'],'amount_expression':display,
     'fixed_amount_cny':fixed,'calculation_basis':raw,'kind':'SECURITY_PAYMENT' if security else 'CONTRACTUAL_PENALTY',
     'evidence':[{'clause_id':e['clause_id'],'quote':e['quote']} for e in f['evidence']]})
 return result


def monetary_impact(item):
 details=exposure_details(item)
 if not details:return ''
 parts=[]
 for d in details:
  expression=d['amount_expression']
  if d['kind']=='INSURANCE_REPLACEMENT':
   parts.append('合同明确涉及'+d['period_label']+expression+'现金补贴替代社保缴费；该金额不等同依法应缴社保金额，实际补缴情形及金额需另行核算')
  elif d['kind']=='SECURITY_PAYMENT':parts.append('直接涉及收取或从工资扣收'+expression)
  else:parts.append('直接涉及'+expression+('固定赔偿责任' if d['scope']=='PROPERTY_DAMAGE' else '违约金'))
 return '；'.join(parts)+'；同一责任不重复累计；是否实际发生取决于触发条件，不等同已经产生实际损失。'


def message(item):
 return (item.decision_trace or {}).get('coverage_legality',{}).get('message','')

def gate(items,report):
 import re
 from review_v2.employment_fact_store import current
 store=current()
 failures=[]
 for item in items:
  if store:
   for row in item.evidence_clauses or []:
    f=store.by_id.get(row.get('structured_fact_id'))
    if f and f['concept']=='social_insurance.cash_replacement' and f['normalized_value'] is True and not insurance_exposure(f) and any('元' in e['quote'] for e in f['evidence']):
     failures.append({'requirement':'AMBIGUOUS_VERIFIED_MONETARY_BINDING','review_id':item.item_id,'current_status':'FAIL','root_cause':'替代缴费证据包含无法唯一绑定的金额，不借用其他义务金额'})
  expected_impact=monetary_impact(item)
  if expected_impact:
   section=re.search(r'^## [^\n]*[（(]'+re.escape(item.item_id)+r'[）)][^\n]*\n(.*?)(?=^## |\Z)',report,re.M|re.S)
   if item.economic_impact!=expected_impact or not section or expected_impact not in section[1]:
    failures.append({'requirement':'VERIFIED_MONETARY_EXPOSURE_DISPLAY','review_id':item.item_id,
       'current_status':'FAIL','failure_stage':'Economic impact projection',
       'root_cause':'已验证经济责任有金额或公式，但报告经济影响未按同一事实展示。'})
  if item.node_id=='employment_part_time_wage' and item.coverage_status=='通过':
   proof=(item.decision_trace or {}).get('specialized_legality',{})
   if proof.get('status')!='PASS' or not isinstance(proof.get('max_days'),(int,float)) or proof['max_days']>15:
    failures.append({'requirement':'PART_TIME_SETTLEMENT_PASS_PROOF','review_id':item.item_id,
       'current_status':'FAIL','failure_stage':'Settlement proof','root_cause':'缺少逐区间计算或明确等价的最长十五日周期证据。'})
  # Responsibility follows the verified concept, not a title substring or a
  # contract-specific quotation. Only fee/payment rules may consume charges.
  if store and item.coverage_status=='风险条款':
   charge_sources=[r for r in item.evidence_clauses
       if store.by_id.get(r.get('structured_fact_id'),{}).get('concept')=='worker.security_payment']
   if charge_sources and item.node_id not in {'employment_worker_charge','employment_wage','employment_dispatch_charges'}:
    failures.append({'requirement':'RISK_RULE_CONCEPT_OWNERSHIP','review_id':item.item_id,
       'current_status':'FAIL','failure_stage':'Rule/report classification',
       'root_cause':'保证金或工资扣收事实被挂到不负责收费的规则。'})
  linked=message(item)
  if not linked:continue
  match=re.search(r'^## [^\n]*[（(]'+re.escape(item.item_id)+r'[）)][^\n]*\n(.*?)(?=^## |\Z)',report,re.M|re.S)
  if not match or linked not in match[1] or '无需修改' in match[1]:
   failures.append({'requirement':'COVERAGE_LEGALITY_CONSISTENCY','review_id':item.item_id,'current_status':'FAIL',
      'failure_stage':'Report projection','root_cause':'同一原文已参与不利风险，不能以形式覆盖输出无需修改。'})
 return {'status':'BLOCKED' if failures else 'REPORT_READY','failures':failures,'gate_results':{'COVERAGE_LEGALITY_CONSISTENCY':'FAIL' if failures else 'PASS'}}


def decision_evidence_lines(item):
 """Render the decision's own verified evidence, independently of coverage citations."""
 a=(item.decision_trace or {}).get('specialized_legality')
 if not a:return []
 rows=a.get('evidence',[])
 lines=['【规则判断证据】','- 判断：'+a['reason']]
 for row in rows:
  lines.append('- 原文位置：'+str(row.get('location') or row.get('clause_id')))
  lines.append('- 原文证据：'+str(row.get('quote') or row.get('text') or ''))
 return lines+['']


def decision_evidence_gate(items,report):
 import re
 from review_v2.employment_fact_store import current
 failures=[]
 for item in items:
  a=(item.decision_trace or {}).get('specialized_legality')
  if not a:continue
  rows=a.get('evidence',[])
  match=re.search(r'^## [^\n]*[（(]'+re.escape(item.item_id)+r'[）)][^\n]*\n(.*?)(?=^## |\Z)',report,re.M|re.S)
  section=match[1].partition('【规则判断证据】')[2] if match else ''
  store=current()
  expected={f['fact_id'] for c in a['concepts'] for f in store.get(c,positive=False)} if store else set(a.get('input_fact_ids',[]))
  actual={e.get('structured_fact_id') for e in rows}
  if expected!=actual or set(a.get('input_fact_ids',[]))!=actual:
   failures.append({'rule_id':item.item_id,'reason':'DECISION_INPUT_EVIDENCE_SET_MISMATCH'})
  for e in rows:
   quote=e.get('quote') or e.get('text') or ''
   if not quote or quote not in section:
    failures.append({'rule_id':item.item_id,'fact_id':e.get('structured_fact_id'),'reason':'DECISION_FACT_NOT_DISPLAYED'})
  if a['reason'] not in section:
   failures.append({'rule_id':item.item_id,'reason':'DECISION_REASON_NOT_DISPLAYED'})
 return {'status':'BLOCKED' if failures else 'REPORT_READY','failures':[
  {**f,'requirement':'DECISION_EVIDENCE_CLOSURE','root_cause':f['reason'],'current_status':'FAIL','failure_stage':'Final decision evidence'} for f in failures]}


def insurance_exposure(fact):
 """Read monetary notation only inside a verified replacement obligation quote."""
 import re
 from review_v2.employment_fact_store import number
 rows=[];seen=set()
 for e in fact['evidence']:
  quote=e['quote']
  monetary_tokens=re.findall(r'(?:人民币\s*)?([0-9０-９,，.]+|[零〇一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬]+)\s*元',quote)
  if len(monetary_tokens)!=1:continue
  # Do not borrow amounts from other sentences or enclosing section metadata.
  for sentence in re.split(r'[。；;\n]',quote):
   matches=list(re.finditer(r'(?:人民币\s*)?([0-9０-９,，.]+|[零〇一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬]+)\s*元',sentence))
   if len(matches)!=1:continue
   m=matches[0];amount=number(m[1]);period='每月' if re.search(r'每月|按月|元[/／]月',sentence) else ''
   identity=(e['clause_id'],sentence,format(amount,'f'),period)
   if identity in seen:continue
   seen.add(identity)
   rows.append({'fact_id':fact['fact_id'],'concept':fact['concept'],'scope':'SOCIAL_INSURANCE','kind':'INSURANCE_REPLACEMENT',
    'amount_expression':format(amount,'f')+'元','fixed_amount_cny':format(amount,'f'),'calculation_basis':m[0],'period_label':period,
    'evidence':[{'clause_id':e['clause_id'],'quote':e['quote']}],'actual_loss':None})
 return rows


def source_counts(items):
 risky=[i for i in items if i.coverage_status=='风险条款']
 clauses=set()
 for i in risky:
  for e in i.evidence_clauses or []:
   if not (e.get('verified_original') or e.get('quote')):continue
   doc=e.get('document_id') or 'main'
   if e.get('clause_id'):clauses.add((doc,'clause',e['clause_id']))
   elif e.get('document_span'):clauses.add((doc,'span',str(e['document_span'])))
 return {'rule_risk_hit_count':len({i.item_id for i in risky}),'risk_clause_count':len(clauses)}


def project_theme_levels(items,findings,themes):
 """Use existing semantic groups, never infer grouping from titles or clause IDs."""
 from review_v2.employment_fact_store import current
 if current() is None:return
 byid={i.item_id:i for i in items}
 for theme in themes:
  ids=set(theme.get('source_review_ids',[]))
  severity=theme['severity'];level={'HIGH':'高','MEDIUM':'中','LOW':'低'}[severity]
  for key in ids:
   i=byid.get(key)
   if not i or i.coverage_status!='风险条款':continue
   i.decision_trace['theme_display_projection']={'theme_id':theme['theme_id'],'severity':severity,'priority':theme['priority'],'original_risk_level':i.risk_level}
   i.risk_level=level
   i.action_priority=i.review_priority=theme['priority']
  for f in findings:
   if set(f.source_review_ids)&ids:
    f.severity=severity;f.priority=theme['priority']
    texts=list(dict.fromkeys(byid[k].economic_impact for k in f.source_review_ids if k in byid and exposure_details(byid[k])))
    if texts:f.aggregation_signals['verified_economic_impact_text']='；'.join(texts)


def theme_display_gate(items,themes,report):
 from review_v2.employment_fact_store import current
 if current() is None:return {'status':'REPORT_READY','failures':[]}
 byid={i.item_id:i for i in items};failures=[]
 for t in themes:
  expected_texts={monetary_impact(byid[k]) for k in t.get('source_review_ids',[]) if k in byid and monetary_impact(byid[k])}
  if any(text not in t.get('economic_impact','') for text in expected_texts):
   failures.append({'requirement':'THEME_VERIFIED_MONETARY_DISPLAY','current_status':'FAIL','root_cause':'聚合主题未保留已验证金额影响'})
  for key in t.get('source_review_ids',[]):
   i=byid.get(key)
   if i and i.coverage_status=='风险条款' and (i.risk_level!={'HIGH':'高','MEDIUM':'中','LOW':'低'}[t['severity']] or i.action_priority!=t['priority']):
    failures.append({'requirement':'THEME_CHILD_DISPLAY_CONSISTENCY','review_id':key,'current_status':'FAIL','root_cause':'主题与子规则分级不一致'})
 counts=source_counts(items)
 if ('风险原文条款数：'+str(counts['risk_clause_count'])) not in report or '风险条款：' in report:
  failures.append({'requirement':'RISK_SOURCE_COUNT_SEMANTICS','current_status':'FAIL','root_cause':'原文条款统计未按证据去重或被误标为规则命中数'})
 return {'status':'BLOCKED' if failures else 'REPORT_READY','failures':failures}
