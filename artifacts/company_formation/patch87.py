from pathlib import Path
p=Path('backend/review_v2/company_formation_checklist.py');s=p.read_text(encoding='utf-8');s += '''
# Presence and legal compliance are separate checks.
COMPANY_FORMATION_CHECKLIST += (replace(F('CF',16,'formation_deadline_legality','认缴期限法定上限及成立日核验',('认缴','缴足','成立'),C+'第47条',(),
    '保留已经约定的缴付日期，核对公司成立日及法定特别规定；原则上将认缴期限限制在成立起五年内，不能把明确日期等同于合法。'),
    applicable_if='存在明确认缴截止日期且需核对成立日及法定期限时适用；未明确日期由出资条款完整性规则审查。'),)
from review_v2.lease_semantics import requirement
PROFILES['formation_transfer_exit'] += [
    requirement('formation_transfer_notice','对外转让书面通知其他股东',r'(?:书面通知其他股东|向其他股东[^。\\n]{0,20}书面通知)'),
    requirement('formation_transfer_notice_content','通知股权数量、价格、支付方式和期限',r'数量[^。\\n]{0,25}价格[^。\\n]{0,25}支付方式[^。\\n]{0,15}期限'),
    requirement('formation_transfer_equal_terms','其他股东同等条件下优先购买',r'同等条件[^。\\n]{0,40}优先(?:购买|受让)权'),
    requirement('formation_transfer_exercise_period','接到通知后的优先购买行权期限',r'(?:通知|接到)[^。\\n]{0,40}(?:三十|30)日[^。\\n]{0,50}(?:答复|行使|优先购买|放弃)'),
]
''';p.write_text(s,encoding='utf-8')
p=Path('backend/review_v2/employment_facts.py');s=p.read_text(encoding='utf-8');marker="    if node == 'formation_transfer_exit':";s=s.replace(marker,"    if node == 'formation_fund_safety':\n        return [r for r in requirements if r['element_id']!='formation_fund_safety_1'], []\n"+marker,1);p.write_text(s,encoding='utf-8')
p=Path('backend/review_v2/priority_contract_review.py');s=p.read_text(encoding='utf-8');s=s.replace("def adverse_evidence(node, clauses):", "def adverse_evidence(node, clauses):\n    if node == 'formation_deadline_legality':\n        from review_v2.formation_rule_semantics import deadline_evidence\n        return deadline_evidence(clauses)")
s=s.replace("def positive_rule_adverse_evidence(node, clauses):", "def positive_rule_adverse_evidence(node, clauses):\n    if node == 'formation_transfer_exit':\n        from review_v2.formation_rule_semantics import transfer_evidence\n        return transfer_evidence(clauses)")
s=s.replace("        if checkpoint.node_id == 'employment_general_penalty' and evidence:","        if checkpoint.node_id == 'formation_deadline_legality' and evidence:\n            reason = '；'.join(dict.fromkeys(r['reason'] for r in evidence))\n        if checkpoint.node_id == 'employment_general_penalty' and evidence:")
s=s.replace('    return ReviewJudgment(\n        coverage_status=state, risk_level="低"',"    if checkpoint.node_id == 'formation_fund_safety':\n        from review_v2.formation_rule_semantics import account_context\n        reason = account_context('\\n'.join(c.text for c in clauses))['conclusion'] + reason\n    return ReviewJudgment(\n        coverage_status=state, risk_level=\"低\"")
s=s.replace('    attach_source_assertions(items, clauses)', '''    attach_source_assertions(items, clauses)
    from review_v2.formation_rule_semantics import deadline_assessment, transfer_assessment, account_context
    formation_text = '\\n'.join(c.text for c in clauses)
    for review in items:
        if review.node_id in {'formation_contributions','formation_deadline_legality'}:
            review.decision_trace['contribution_deadline_assessment'] = deadline_assessment(formation_text)
        if review.node_id == 'formation_transfer_exit':
            review.decision_trace['transfer_mechanism_assessment'] = transfer_assessment(formation_text)
        if review.node_id == 'formation_fund_safety':
            review.decision_trace['fund_receiver_context'] = account_context(formation_text)''',1)
p.write_text(s,encoding='utf-8')
p=Path('backend/routers/review_v2.py');s=p.read_text(encoding='utf-8').replace('adverse_theme_projection, report_statistics, shareholder_transaction_facts','adverse_theme_projection, report_statistics, shareholder_transaction_facts, formation_rule_semantics');p.write_text(s,encoding='utf-8')
