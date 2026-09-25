from pathlib import Path
p=Path('backend/review_v2/work_evidence.py')
s=p.read_text(encoding='utf8')
a=s.index('def applicability(node, clauses):')
b=s.index("    if node != 'work_professional_license':",a)
s=s[:a]+'''def transaction_facts(clauses):
    """Shared role-bound transfer and mutually exclusive lien scenarios."""
    profiles = {
      'transfer': [atom('transfer', '承揽工作交第三人', r'承揽[人方]', TRANSFER)],
      'auxiliary': [atom('auxiliary', '承揽人辅助工作外交', r'承揽[人方][^。；]{0,30}(?:将|把|可|负责)', r'辅助工作', TRANSFER+r'|外协')],
      'customer_assistance': [atom('customer_assistance', '定作人协助', r'定作[人方][^。；]{0,90}完成[^。；]{0,10}辅助工作')],
      'lien_excluded': [atom('lien_excluded', '排除留置', r'不得留置|排除留置|禁止扣留|无条件交付')],
      'lien_reserved': [atom('lien_reserved', '保留留置', r'有权[^。；]{0,8}留置|可以[^。；]{0,8}留置|保留留置权')],
    }
    return {key: extract(key,clauses,profiles) for key in profiles}


def applicability(node, clauses):
    facts = transaction_facts(clauses)
    def gate(active, condition, reason, evidence):
        return {'status':'APPLICABLE' if active else 'NOT_APPLICABLE',
                'applicable':active,'triggered':active,'condition':condition,
                'reason':reason,'trigger_evidence':evidence,'shared_transaction_facts':facts}
    if node == 'work_main_subcontract_consent':
        evidence=extract(node,clauses,PROFILES)
        if evidence or facts['transfer']:
            return gate(True,'MAIN_WORK_TRANSFER','正文存在承揽工作转交安排，检查主要工作同意要求。',evidence or facts['transfer'])
    if node == 'work_auxiliary_subcontract_liability':
        active=bool(facts['auxiliary'])
        return gate(active,'CONTRACTOR_AUXILIARY_TRANSFER',
          '承揽人将辅助工作交第三人完成，审查其责任。' if active else '未发现承揽人辅助工作交第三人完成；定作人完成辅助工作属于协助义务，不触发辅助分包责任。',facts['auxiliary'])
    if node == 'work_illegal_total_subcontract':
        active=bool(facts['transfer'])
        return gate(active,'CONTRACTOR_WORK_TRANSFER',
          '已识别承揽工作转交第三人，进一步检查是否允许未经同意全部或肢解转包。' if active else '未发现承揽工作交第三人完成的事实。',facts['transfer'])
    if node in {'work_contractor_lien_condition','work_lien_notice_scope','work_lien_exclusion'}:
        excluded=bool(facts['lien_excluded'])
        # Neutral silence keeps the statutory retention option, never recommends
        # adding both retention and its exclusion. Express exclusion wins routing.
        active=excluded if node=='work_lien_exclusion' else not excluded
        return gate(active,'LIEN_EXCLUSION' if node=='work_lien_exclusion' else 'LIEN_RETENTION',
          ('已选择排除留置方案，不再建议增加留置权。' if excluded else '未选择排除留置方案；仅审查留置条件及范围，不建议同时补充排除留置。'),
          facts['lien_excluded'] or facts['lien_reserved'])
''' + s[b:]
p.write_text(s,encoding='utf8')
p=Path('backend/review_v2/settlement_formula.py');s=p.read_text(encoding='utf8');s=s.replace("        base=re.search", "        if not re.search(r'最低(?:业绩|采购|销售|收入|收益)|保底|业绩承诺|业务(?:额|基数)|销售额|收入额|收益额|年度基数|采购额',quote):\n            continue\n        base=re.search",1)
s=s.replace('if analyze(text) and not any','if re.search(r\'补足|保底|最低收益\',text) and not any')
s+='''\n\ndef applicability(text):
    facts=analyze(text)
    return {'status':'APPLICABLE' if facts else 'NOT_APPLICABLE',
      'applicable':bool(facts),'triggered':bool(facts),'condition':'BUSINESS_PERFORMANCE_SHORTFALL',
      'trigger_evidence':facts,
      'reason':'存在业务金额承诺及补差机制。' if facts else '未发现最低业绩或业务金额补差机制；普通清偿不足的债务余额不适用业务额补差规则。'}
'''
p.write_text(s,encoding='utf8')
p=Path('backend/review_v2/engine.py');s=p.read_text(encoding='utf8');needle='        predicate_gate = resolve_prerequisites(checkpoint, prerequisite_facts)';s=s.replace(needle,"        if checkpoint.node_id == 'common_shortfall_formula':\n            from review_v2.settlement_formula import applicability as shortfall_gate\n            fact_applicability = shortfall_gate(contract_text)\n            is_applicable = fact_applicability['applicable']\n            applicability_reason = fact_applicability['reason']\n"+needle);p.write_text(s,encoding='utf8')
