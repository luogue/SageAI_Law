from pathlib import Path
p=Path('backend/review_v2/loan_facts.py');s=p.read_text(encoding='utf8')
s=s.replace('r"转账|现金|汇款|划扣"','r"转账|现金|汇款|划扣|自动扣收|自动扣款|等额本息|等额本金"')
needle='# Payment evidence is shared'
pos=s.index(needle)
s=s[:pos]+'''# Distinct operative propositions; list mentions are not calculation limits.
PROFILES['loan_compound_interest_limit'] = [
 atom('loan_compound_scope','复利计算对象及条件',r'复利|利息计息',r'(?:对|就)[^。；]{0,20}(?:未付|未支付|逾期|拖欠)利息[^。；]{0,20}(?:计收|计算)|不(?:得|再)?[^。；]{0,12}(?:计收|计算)复利|禁止[^。；]{0,8}复利'),
 atom('loan_compound_standard','复利标准或限制',r'复利',r'按[^。；]{0,20}(?:利率|标准)[^。；]{0,10}(?:计收|计算)|不得超过|不计收|不计算|禁止[^。；]{0,8}复利')]
PROFILES['loan_early_repayment_notice'] = [
 atom('loan_early_application','提前还款申请及同意程序',r'提前(?:还款|偿还|清偿)',r'申请|通知',r'贷款人|出借人',r'同意|批准|确认'),
 atom('loan_early_channel','提前还款通知渠道或明确提前期限',r'提前(?:还款|偿还|清偿)',r'书面|电子|线上|柜台|手机银行|提前[一二三四五六七八九十百\\d]+(?:个工作)?[日天]')]

''' +s[pos:]
s=s.replace('if re.search(r"不涉及|不存在|不用于|不得用于|禁止|并非|不采用|无须|无需", prefix):','if re.search(r"不涉及|不存在|不用于|不得用于|禁止|并非|不采用|无须|无需|不得办理|不办理|不允许|不予办理", prefix):')
s=s.replace('else:\n            continue\n        found.append((kind, clause.clause_id))', '''else:
            # Link a role-bound name to its separate identity declaration;
            # never infer a natural person solely from a short Chinese name.
            name=re.split(r'[，,地址联系电话\\n]',value)[0]
            identity=[c for c in clauses if re.search(r'姓名[：:]'+re.escape(name)+r'(?:\\s|证件|$)',c.text) and re.search(r'居民身份证|身份证',c.text)]
            if not name or not identity:
                continue
            kind='natural'
        found.append((kind, clause.clause_id))''')
s=s.replace('False if "natural" in (v["lender_kind"], v["borrower_kind"])','False if any(k in {"natural","financial"} for k in (v["lender_kind"], v["borrower_kind"]))')
s=s.replace('        for key, node in {"maturity":', '''        excluded=[c.clause_id for c,q in source if re.search(r'(?:本贷款|本借款|贷款)[^。；]{0,8}(?:不得|不予|不允许|不能|不)[^。；]{0,5}(?:办理)?展期',compact(q))]
        values['extension_excluded'],evidence['extension_excluded']=bool(excluded),excluded
        if excluded:
            values['extension']=False
        for key, node in {"maturity":''')
s=s.replace('keys = ("extension", "guarantee") if "guarantor" in node else ("extension",)','keys = ("extension", "guarantee") if "guarantor" in node else ("extension",)')
s=s.replace('        if node.startswith("loan_early_repayment_")', '''        if node == 'loan_note_receipt_attachment':
            tests[node]=(('lender_kind',), v['lender_kind'] != 'financial')
        if node.startswith("loan_early_repayment_")''')
s=s.replace('        return {"status": state,', '''        if node.startswith('loan_extension_') and v.get('extension_excluded'):
            keys=(*keys,'extension_excluded')
            reason='合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。'
        if node=='loan_note_receipt_attachment' and v['lender_kind']=='financial':
            reason='金融借款不强制采用民间借贷纸质借据；放款记录与电子凭证由实际放款证据规则核验。'
        return {"status": state,''')
s=s.replace('银行回单|收据|借据", r"作为','银行回单|收据|借据|电子借据|银行系统.{0,8}(?:放款记录|贷款记录)|电子放款记录", r"作为')
p.write_text(s,encoding='utf8')
