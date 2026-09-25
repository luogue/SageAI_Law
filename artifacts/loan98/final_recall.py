from pathlib import Path
p=Path('backend/review_v2/loan_facts.py');s=p.read_text(encoding='utf8').replace('r"住址|地址", r"变化|变更", r"书面通知|通知对方"','r"住址|地址|住所", r"变化|变更", r"书面通知|通知(?:对方|贷款人|出借人)"')
s=s.replace('        if node == \'loan_note_receipt_attachment\':', '''        if node == 'loan_voucher_creditor_identification' and v['lender_kind']=='financial':
            tests[node]=(('lender_kind','voucher_mechanism'),v['voucher_mechanism'])
        if node == 'loan_note_receipt_attachment':''')
s=s.replace('        values[\'extension_excluded\'],evidence[\'extension_excluded\']=bool(excluded),excluded', '''        vouchers=[c.clause_id for c,q in source if re.search(r'借据|欠条|借条|收据|放款凭证|银行回单|系统放款记录',q)]
        values['voucher_mechanism'],evidence['voucher_mechanism']=bool(vouchers),vouchers
        values['extension_excluded'],evidence['extension_excluded']=bool(excluded),excluded''')
p.write_text(s,encoding='utf8')
p=Path('backend/tests/test_loan_financial_semantics.py');s=p.read_text(encoding='utf8').replace("('loan_actual_disbursement_evidence','电子借据", "('loan_notice_service_method','借款人的住所发生重大变化，应及时通知贷款人。',True),\n ('loan_actual_disbursement_evidence','电子借据") ;p.write_text(s,encoding='utf8')
