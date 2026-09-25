from pathlib import Path
p=Path('backend/review_v2/loan_facts.py');s=p.read_text(encoding='utf8');pos=s.index('# Distinct operative propositions')
s=s[:pos]+'''# Payment collection priorities do not establish allocation of insufficient debt payment.
PROFILES['loan_repayment_offset_order']=[atom('loan_offset_order','部分还款的抵充顺序',
 r'部分还款|还款[^。；]{0,12}不足|不足[^。；]{0,12}(?:清偿|偿还)|抵充|冲抵',r'先|依次|顺序',r'本金|利息')]
PROFILES['loan_overdue_interest']=[atom('loan_overdue_rate','逾期利率或可计算的加收标准',
 r'逾期',r'利息|利率|罚息',r'\\d+(?:\\.\\d+)?[%％‰]|按[^。；]{0,12}(?:原|合同|执行)利率')]
PROFILES['loan_early_repayment_interest']=[atom('loan_early_interest_period','提前还款按实际占用期间计息',
 r'提前(?:还款|偿还|清偿)',r'利息',r'实际[^。；]{0,12}(?:天数|期间)|计算至[^。；]{0,8}还款日')]

''' +s[pos:]
s+='''

NEGATIVE_SCANS = {
 'loan_deducted_interest_forbidden': (r'(?:预扣|先扣|预先扣除)[^。；]{0,12}(?:利息|服务费)|从[^。；]{0,8}本金[^。；]{0,8}扣除[^。；]{0,8}利息',),
 'loan_unreasonable_early_repayment_penalty': (r'提前(?:还款|偿还|清偿)',r'违约金|罚金|补偿金|手续费|禁止提前还款'),
 'loan_hidden_fee_over_cap': (),
}

def negative_scan(node, clauses):
    """Reproducible adverse-fact search, not proof of legal/external safety."""
    import hashlib
    if node not in NEGATIVE_SCANS:
        return None
    source=list(units(clauses)); hits=[]
    for c,q in source:
        if node=='loan_hidden_fee_over_cap':
            adverse=financing_charge(q)
        else:
            adverse=all(re.search(p,compact(q)) for p in NEGATIVE_SCANS[node])
            if re.search(r'不得[^。；]{0,15}(?:预扣|扣除|收取)|不收取|无需支付|免收',q):
                adverse=False
        if adverse:
            hits.append({'clause_id':c.clause_id,'quote':q,'location':c.location})
    return {'kind':'ADVERSE_FACT_SCAN','node':node,'scope':'CONTRACT_TEXT_ONLY',
      'corpus_hash':hashlib.sha256(repr([(c.clause_id,q) for c,q in source]).encode()).hexdigest(),
      'searched_clause_ids':list(dict.fromkeys(c.clause_id for c,q in source)),
      'unit_count':len(source),'adverse_evidence':hits,
      'status':'FOUND' if hits else 'NOT_FOUND' if source else 'EMPTY_CORPUS'}
'''
p.write_text(s,encoding='utf8')
p=Path('backend/review_v2/engine.py');s=p.read_text(encoding='utf8')
needle='        claim=_coverage_claim_for_item(item)'
s=s.replace(needle,'''        audit=item.decision_trace.get('negative_rule_scan')
        if audit:
            from review_v2.loan_facts import negative_scan
            verified=negative_scan(item.node_id,clauses)
            if verified == audit and verified['status']=='NOT_FOUND' and verified['unit_count']:
                item.decision_trace['verified_pass_source_gate']={'status':'PASS','assessment':'TEXT_NO_ADVERSE_FACT','absence_audit':verified,'failures':[]}
                continue
'''+needle,1)
needle='        if item.node_id in COLLECTION_NODES:'
s=s.replace(needle,'''        from review_v2.loan_facts import negative_scan
        audit=negative_scan(item.node_id,clauses)
        if audit:
            item.decision_trace['negative_rule_scan']=audit
        if item.node_id in {'loan_actual_disbursement_evidence','loan_transfer_voucher_attachment'}:
            item.decision_trace['finding_parent_group']='loan_disbursement_proof'
            item.decision_trace['risk_category']='实际放款到账证明'
            item.decision_trace['underlying_risk_identity']={'fact':'disbursement_record','scope':'loan_principal','remedy':'retain_actual_disbursement_evidence'}
'''+needle,1)
s=s.replace('if item.node_id in LOAN_ELEMENT_PROFILES or item.node_id == "loan_hidden_fee_over_cap":','if (item.node_id in LOAN_ELEMENT_PROFILES or item.node_id == "loan_hidden_fee_over_cap") and not item.decision_trace.get("loan_cost_elements"):')
p.write_text(s,encoding='utf8')
