"""Scope-owned cooperative arrangements feeding the shared canonical projector."""
import re
from review_v2.obligation_detail_elements import _element
from review_v2.technology_service_elements import sources
from review_v2.proposition_scope import listed_arrangement_matches

RULE_FAMILIES={'TC-05-02':'joint_patent_procedure','TC-05-03':'joint_secret_disposition',
 'TC-10-01':'cooperative_improvement_ownership','TC-10-02':'cooperative_improvement_sharing',
 'TC-10-03':'cooperative_improvement_notice', 'TC-12-01':'cooperative_background_liability', 'TC-12-02':'cooperative_claims'}
FAMILIES=tuple(RULE_FAMILIES.values())+('cooperative_exit','background_license',)

def scoped(clauses,pattern):
 return [c for c in clauses if re.search(pattern,c.title+' '+c.text)]

def transaction_layers(clauses):
 layers=[]
 for party,tag in [('甲方','PARTY_A'),('乙方','PARTY_B')]:
  rows=scoped(clauses,party+'背景技术')
  proof=sources(rows,r'(?:授予|提供)[^。；]{0,45}许可|免费实施许可|项目内部免费许可',inherit_lists=True)
  if proof:layers.append(dict(type=tag+'_BACKGROUND_PATENT_LICENSE',sources=proof,actor=party))
 for kind,pat in [('JOINT_PATENT_APPLICATION',r'双方应共同申请专利|共同作为专利申请人'),
                  ('JOINT_TECHNICAL_SECRET',r'共同技术秘密由双方共同控制'),
                  ('JOINT_IP_LICENSE',r'(?:许可共同专利|许可共同技术秘密)[^。；]{0,35}(?:同意|许可)'),
                  ('POST_PROJECT_IMPROVEMENT',r'改进成果[^。；]{0,30}归[^。；]{0,20}所有')]:
  proof=sources(clauses,pat)
  if proof:layers.append(dict(type=kind,sources=proof))
 return layers

def elements(family,clauses):
 def find(pattern,scope=None,intro=None):
  subset=scoped(clauses,scope) if scope else clauses
  rows=sources(subset,pattern,inherit_lists=True)
  if intro:
   rows=[]
   for c in subset:
    for r in listed_arrangement_matches(pattern,c.text,introduction_pattern=intro):
     rows.append(dict(clause_id=c.clause_id,quote=r['quote']))
  return rows
 def atom(key,label,pattern,scope=None,intro=None):
  return _element(key,label,find(pattern,scope,intro),source_fact_key='technology.cooperative.'+key)
 if family=='joint_patent_procedure':
  rows=[atom('patent_application_right','共同专利申请人及申请权',r'双方应共同申请专利|共同作为专利申请人'),
   atom('application_costs','共同专利申请费用分配',r'申请费用[^。；]{0,30}(?:各承担|分担|承担比例)'),
   atom('application_document_cooperation','申请材料准备及配合',r'专利申请材料[^。；]{0,50}(?:准备|配合)'),
   atom('unilateral_application_prohibition','禁止单方申请共同成果',r'单独申请[^。；]{0,25}共同成果',intro=r'不得[^。；]{0,25}同意'),
   atom('withdrawal_prohibition','禁止单方撤回共同申请',r'撤回共同专利申请',intro=r'不得[^。；]{0,25}同意'),
   atom('abandonment_prohibition','禁止单方放弃共同申请或专利',r'放弃[^。；]{0,20}共同专利',intro=r'不得[^。；]{0,25}同意'),
   atom('office_action_notice','审查文件通知及期限',r'收到审查意见[^。；]{0,90}发送[^。；]{0,15}审查文件'),
   atom('patent_decision_deadlock','答复、复审及缩限分歧的最终决策机制',r'(?:无法达成一致|分歧|僵局)[^。；]{0,50}(?:由[^。；]{0,20}决定|仲裁|专家裁定|最终决定)',r'专利申请程序|审查意见')]
  if scoped(clauses,r'不愿继续承担[^。；]{0,30}专利|停止[^。；]{0,20}申请费用'):
   for key,label,pat in [('nonpayer_retained_share','停止付费一方是否保留原申请权份额',r'不承担费用的一方[^。；]{0,20}(?:仍保留|不再享有)'),
    ('nonpayer_share_change','停止付费后的申请权份额变化',r'(?:承担后续费用|不承担费用)[^。；]{0,40}(?:份额调整为|份额不变|取得全部申请权)'),
    ('nonpayer_license_revenue','停止付费后的许可收益分配',r'许可收益[^。；]{0,20}(?:按|各占|归)'),
    ('nonpayer_abandonment_effect','停止付费与放弃申请权的关系',r'(?:停止|不承担|放弃)费用[^。；]{0,20}(?:不视为|视为|不等于|等于)放弃申请权')]:
    rows.append(atom(key,label,pat,r'不愿继续承担[^。；]{0,30}专利|停止[^。；]{0,20}申请费用'))
  return rows
 if family=='joint_secret_disposition':
  scope=r'共同技术秘密'
  return [atom('joint_secret_control','共同技术秘密控制权',r'共同技术秘密由双方共同控制',scope),
   atom('independent_use_right','合作方内部生产经营使用权',r'双方均可[^。；]{0,30}内部生产经营[^。；]{0,15}使用',scope),
   atom('external_license_consent','对外许可书面同意机制',r'许可共同技术秘密[^。；]{0,35}应取得[^。；]{0,15}书面同意',scope),
   atom('external_revenue_allocation','对外许可收益分配',r'(?:双方|甲乙双方)[^。；]{0,15}(?:各分配|各占|按[^。；]{0,12}分配)',scope),
   atom('consent_reply_deadline','对外许可同意答复期限',r'(?:同意|答复)[^。；]{0,20}\d+[^。；]{0,8}日|\d+[^。；]{0,8}日内[^。；]{0,15}答复',scope),
   atom('consent_silence_remedy','长期不回复的处理',r'(?:不回复|未回复)[^。；]{0,25}(?:视为同意|可[^。；]{0,15}许可)',scope),
   atom('consent_refusal_remedy','无正当理由拒绝许可的处理',r'无正当理由[^。；]{0,20}(?:不得拒绝|拒绝[^。；]{0,15}赔偿)',scope),
   atom('undervalue_license_control','明显低价许可的处理',r'(?:低于市场|低价)[^。；]{0,30}(?:不得|评估|赔偿)',scope)]
 if family.startswith('cooperative_improvement'):
  scope=r'改进成果'
  ownership=atom('actual_improver_ownership','独立改进成果归实际改进方',r'改进成果归[^。；]{0,25}(?:该方|完成改进的一方|改进方)所有',scope)
  priority=atom('priority_license_right','同等条件优先许可权',r'另一方[^。；]{0,25}同等条件[^。；]{0,15}优先许可权',scope)
  notice=atom('improvement_notice_required','改进成果书面通知义务',r'改进方应[^。；]{0,60}书面通知另一方',scope)
  deadline=atom('improvement_notice_deadline','改进成果通知期限',r'改进成果形成后\d+(?:个工作)?日内书面通知',scope)
  exercise=atom('priority_license_exercise_deadline','优先许可权行使期限',r'优先许可权[^。；]{0,20}(?:应|须)[^。；]{0,15}\d+(?:个工作)?日内[^。；]{0,10}行使',scope)
  return [ownership] if family.endswith('ownership') else [ownership,priority] if family.endswith('sharing') else [notice,deadline,exercise]
 if family=='cooperative_background_liability':
  return [atom('background_rights_guarantee','背景技术合法来源及使用权保证',r'双方分别保证[^。；]{0,50}合法来源和使用权'),
   atom('background_infringement_liability','背景技术提供方承担侵权责任',r'由提供该背景技术的一方承担责任')]
 if family=='cooperative_claims':
  scope=r'第三方权利|第三方[^。；]{0,20}侵权主张'
  return [atom('joint_claim_response','共同成果第三方主张配合处理',r'双方应共同配合处理',scope),
   atom('claim_notice','第三方主张通知期限',r'(?:收到|获悉)[^。；]{0,20}(?:索赔|主张)[^。；]{0,30}(?:日内|立即)[^。；]{0,15}通知',scope),
   atom('defense_control','第三方索赔抗辩控制权',r'(?:甲方|乙方|双方)[^。；]{0,15}(?:负责|控制)[^。；]{0,15}(?:抗辩|诉讼)',scope),
   atom('lawyer_selection','第三方索赔律师选择机制',r'(?:双方|甲方|乙方)[^。；]{0,15}(?:选定|选择|聘请)[^。；]{0,15}律师',scope),
   atom('settlement_authority','第三方索赔和解决策机制',r'和解[^。；]{0,15}(?:应当|应|须)[^。；]{0,15}(?:同意|批准)',scope),
   atom('claim_cost_allocation','第三方索赔程序费用分担',r'(?:诉讼费|律师费)[^。；]{0,20}由[^。；]{0,15}承担',scope),
   atom('claim_compensation_allocation','共同成果侵权赔偿分配',r'赔偿责任[^。；]{0,30}(?:按[^。；]{0,15}承担|各承担)',scope)]
 if family=='cooperative_exit':
  from review_v2.development_exit import development_exit_elements
  rows=development_exit_elements(clauses)
  scope=r'退出项目|一方退出'
  rows.extend([atom('exit_notice_deadline','提前退出通知期限',r'应[^。；]{0,20}提前\d+日书面通知',scope),
   atom('exit_pending_patent_cost','退出后未完成共同专利申请费用承担',r'退出后[^。；]{0,50}(?:应|仍须|无需)[^。；]{0,20}承担[^。；]{0,20}专利申请费用',scope)])
  replacements=[atom('exit_source_code_handover','提前退出时源代码交接',r'交付[^。；]{0,25}(?:代码|源程序)',scope),
   atom('exit_development_cost_settlement','退出日前共同费用承担',r'继续承担退出日前[^。；]{0,20}共同费用',scope)]
  for replacement in replacements:
   if replacement['supporting_evidence']:
    rows=[replacement if e['element_id']==replacement['element_id'] else e for e in rows]
  return rows
 if family=='background_license':
  rows=[]
  for party,tag in [('甲方','party_a'),('乙方','party_b')]:
   scope=party+'背景技术'
   rows.append(atom(tag+'_background_grant',party+'背景技术项目内许可',r'免费实施许可|项目内部免费许可',scope))
  return rows
 return []
