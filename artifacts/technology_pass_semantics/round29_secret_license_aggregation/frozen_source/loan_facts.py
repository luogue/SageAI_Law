"""Evidence-bound loan facts shared by applicability, coverage and risk assessment.

Only operative text/annexes and party declarations establish facts.  A bank
account, a remedy-cost list or generic statutory wording is not a transaction.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from review_v2.clause_parser import formal_evidence_clauses
from review_v2.loan_semantics import concept_facts


def compact(text):
    return re.sub(r"\s+", "", text or "")


def atom(key, proposition, *patterns):
    return {"element_id": key, "proposition": proposition,
            "terms": [proposition], "loan_patterns": list(patterns)}


DEADLINE = atom("loan_maturity", "借款到期日或可确定的还款期限", r"借款期限|还款期限|到期日|偿还日期|还款日|借款自|借期", r"(?:至|到|于).{0,8}\d{4}年\d{1,2}月\d{1,2}日|(?:之日起|起|为)\d+(?:个)?[年月日天]")
RATE = atom("loan_agreed_rate", "明确的借期利率或无息安排", r"(?:年利率|月利率|日利率|月息|年息|利率).{0,8}\d+(?:\.\d+)?[%％‰]|(?:本借款|本合同|借期内|双方约定).{0,8}(?:无息|不计息|不支付利息)")
PROFILES = {
    "loan_notice_service_method": [
        atom("loan_service_address", "指定送达地址", r"送达地址|地址.{0,12}(?:用于|作为).{0,8}送达"),
        atom("loan_address_change_notice", "地址变更通知", r"住址|地址|住所|联系方式", r"变化|变更", r"通知(?:对方|贷款人|出借人|另一方|甲方|乙方)"),
        dict(atom("loan_collection_channel", "催收通知方式或渠道", r"催收|催告|通知|送达", r"邮寄|快递|短信|电子信息|电子邮件|邮箱|微信"),
             alternative_patterns=[[r'催收|催告',r'书面|电话']])],
    "loan_financial_private_distinction": [atom("loan_lender_identity", "贷款人主体身份可用于区分金融借款与民间借贷", r"贷款人|出借人|出借方|贷款方|甲方|乙方", r"身份证|自然人|银行|信用社|公司|企业")],
    "loan_note_receipt_attachment": [atom("loan_receipt_document", "实际借据、收据或欠条", r"收据|借据|借条|欠条", r"收到|借到|借款金额|欠款金额")],
    "loan_actual_disbursement_evidence": [atom("loan_disbursement_record", "实际放款或到账凭证及确认", r"放款|借款|贷款|本金|到账", r"转账凭证|放款凭证|到账确认|收款收据|银行回单|收据|借据|电子借据|银行系统.{0,8}(?:放款记录|贷款记录)|电子放款记录", r"作为|证明|确认|保存|出具|提供|记录")],
    "loan_voucher_creditor_identification": [atom("loan_voucher_creditor", "债权凭证载明债权人身份", r"借据|借条|欠条|收据|债权凭证", r"载明|注明|记载|列明", r"出借人|债权人|贷款人")],
    "loan_interest_calculation_base": [
        atom("loan_interest_base", "利息计算基数", r"利息|计息", r"本金余额|未偿还本金|实际收到|实际占用|以.{0,15}本金.{0,8}(?:基数|计算)"),
        atom("loan_interest_period", "利息起止期间", r"利息|计息", r"自.{0,30}(?:至|止)|起算|计息期间")],
    "loan_repayment_method_account": [
        atom("loan_repayment_method", "还款支付方式", r"还款|偿还|归还借款", r"转账|现金|汇款|划扣|自动扣收|自动扣款|等额本息|等额本金"),
        atom("loan_repayment_account", "还款收款账户或指定机制", r"还款|偿还|归还借款", r"账户|账号|户名|开户行")],
    "loan_guarantee_attachment": [atom("loan_security_document", "具体担保文件及附件安排", r"保证合同|抵押合同|质押合同|担保合同|担保人授权书|抵押登记证明", r"附件|附具|提供|提交|编号|签署")],
    "loan_collection_record_attachment": [atom("loan_collection_records", "催收或还款记录的保存安排", r"催收函|催收记录|还款回单|还款记录|还款承诺书|对账单", r"保存|留存|附件|保留|提供|提交")],
    "loan_repayment_deadline": [DEADLINE],
    "loan_limitation_start": [DEADLINE],
    "loan_interest_rate_agreed": [RATE],
    "loan_repayment_offset_order": [atom("loan_offset_order", "部分还款的抵充顺序", r"抵充|冲抵|清偿顺序|偿还顺序|扣款顺序", r"先|依次|顺序")],
    "loan_repayment_receipt_confirmation": [atom("loan_repayment_receipt", "还款到账确认或结清凭证", r"还款|偿还|清偿|结清", r"收据|回单|到账确认|结清证明|出具.{0,8}确认|确认收到")],
    "loan_collection_ack_limitation_interruption": [atom("loan_interruption_record", "催收或债务确认的留痕安排", r"催收|催告|还款承诺|对账|债务确认", r"保存|留存|保留|签收|书面|记录")],
    "loan_guarantor_collection_within_period": [atom("loan_guarantee_claim_record", "保证期间内向保证人行权并保存证据", r"保证期间|保证期限", r"保证人|担保人", r"主张|催收|催告|起诉", r"保存|留存|保留|签收|书面|记录")],
    "loan_interest_no_agreement_rule": [atom("loan_no_interest_default", "未约定利息时的处理", r"未约定利息|利息约定不明", r"视为|不支付|处理|执行")],
    "loan_natural_person_formation": [atom("loan_delivery_formation", "借款以实际交付或收到款项为依据", r"实际收到|实际交付|实际提供|到账|收到.{0,10}借款", r"成立|生效|确认|为准|已")],
    "loan_old_for_new_guarantor_notice": [atom("loan_refinancing_guarantor_knowledge", "保证人知悉借新还旧并确认相应保证责任", r"保证人|担保人", r"借新还旧|(?:新贷|本贷款|本借款).{0,15}(?:偿还|归还).{0,8}(?:旧贷|原贷|旧借款)", r"知悉|知情|已知|确认|同意")],
    "loan_extension_request": [
        atom("loan_extension_application", "展期申请程序", r"展期|延期还款", r"申请|提出"),
        atom("loan_extension_lender_consent", "展期须贷款人同意", r"展期|延期还款", r"贷款人|出借人|甲方", r"同意|批准"),
    ],
    "loan_extension_interest_rate": [atom("loan_extension_rate", "展期期间的利率或计息安排", r"展期|延期", r"利率|利息", r"按原|原利率|执行|计收|计算|为.{0,10}[%％]")],
    "loan_extension_guarantor_consent": [atom("loan_extension_guarantee", "展期须保证人书面同意", r"展期|延期", r"保证人|担保人", r"书面同意|书面确认")],
    "loan_extension_original_due_no_consent": [atom("loan_extension_not_approved", "展期未经同意仍按原期限履行", r"展期|延期", r"未经|未获|不同意|未同意", r"原期限|原还款|原到期|原合同.{0,10}履行")],
    "loan_enterprise_business_need": [atom("loan_enterprise_purpose", "企业借款用于生产经营", r"借款|贷款|资金", r"用于|用途|为|因", r"生产经营|经营周转|资金周转")],
    "loan_financial_interest_compliance": [atom("loan_financial_rate_compliance", "金融贷款利率及费用符合监管要求", r"利率|融资成本|贷款费用", r"符合|不超过|遵守|按照", r"监管|法律|规定")],
}


# Payment collection priorities do not establish allocation of insufficient debt payment.
PROFILES['loan_repayment_offset_order']=[atom('loan_offset_order','部分还款的抵充顺序',
 r'部分还款|还款[^。；]{0,12}不足|不足[^。；]{0,12}(?:清偿|偿还)|抵充|冲抵',r'先|依次|顺序',r'本金|利息')]
PROFILES['loan_overdue_interest']=[atom('loan_overdue_rate','逾期利率或可计算的加收标准',
 r'逾期',r'利息|利率|罚息',r'\d+(?:\.\d+)?[%％‰]|按[^。；]{0,12}(?:原|合同|执行)利率'),
 atom('loan_overdue_base','逾期利息计算基数',r'逾期|罚息',r'本金|未偿借款|未还借款'),
 atom('loan_overdue_period','逾期利息起止期间',r'逾期',r'自逾期|逾期之日起|到期次日',r'清偿|付清|还清|实际偿还|实际归还')]
PROFILES['loan_early_repayment_interest']=[atom('loan_early_interest_period','提前还款按实际占用期间计息',
 r'(?:提前(?:还款|偿还|清偿)|已归还本金|实际还款)',r'利息|计息',r'(?:实际[^。；]{0,20}(?:天数|期间)|计算至[^。；]{0,12}还款日|到账日起不再计息)')]

# Conjunctive requirements retain separate source ownership.  Either an
# explicit actual-occupancy clause or the two complementary temporal facts
# establishes the complete interest period; one half alone is only PARTIAL.
_actual_period = PROFILES['loan_early_repayment_interest'][0]['loan_patterns']
PROFILES['loan_early_repayment_interest'] = [
    dict(atom('loan_early_interest_period', '已归还本金到账后停止后续计息', *_actual_period),
         alternative_patterns=[[r'提前(?:归还|还款|偿还)', r'本金', r'到账', r'不再(?:计算|计收|产生).{0,8}(?:利息|计息)']]),
    dict(atom('loan_early_accrued_settlement', '提前还款结清截至实际还款日的已产生利息', *_actual_period),
         alternative_patterns=[[r'提前还款', r'结清|支付', r'截至实际还款日', r'(?:已|已经)产生.{0,5}利息']]),
]

# Distinct operative propositions; list mentions are not calculation limits.
PROFILES['loan_compound_interest_limit'] = [
 atom('loan_compound_scope','复利计算对象及条件',r'复利|利息计息',r'(?:对|就)[^。；]{0,20}(?:未付|未支付|逾期|拖欠)利息[^。；]{0,20}(?:计收|计算)|不(?:得|再)?[^。；]{0,12}(?:计收|计算)复利|禁止[^。；]{0,8}复利'),
 atom('loan_compound_standard','复利标准或限制',r'复利',r'按[^。；]{0,20}(?:利率|标准)[^。；]{0,10}(?:计收|计算)|不得超过|不计收|不计算|禁止[^。；]{0,8}复利')]
PROFILES['loan_early_repayment_notice'] = [
 dict(atom('loan_early_application','提前还款申请或通知程序',r'提前(?:还款|偿还|清偿)',r'申请|通知',r'贷款人|出借人|甲方|乙方',r'同意|批准|确认'),
      alternative_patterns=[[r'提前(?:还款|偿还|归还)',r'通知(?:甲方|乙方|出借人|贷款人|对方)',r'书面|提前[一二三四五六七八九十百\d]+(?:个工作)?[日天]']]),
 atom('loan_early_channel','提前还款通知渠道或明确提前期限',r'(?:提前(?:还款|偿还|清偿)|提前)',r'书面|电子|线上|柜台|手机银行|提前[一二三四五六七八九十百\d]+(?:个工作)?[日天]|[一二三四五六七八九十百\d]+个工作日(?:前|内).*通知')]

# Payment evidence is shared across the substantive and document-check rules.
# Cash receipts and bank vouchers are alternatives, not cumulative requirements.
PROFILES['loan_transfer_voucher_attachment'] = PROFILES['loan_actual_disbursement_evidence']

PROFILES['loan_enterprise_business_need'][0]['loan_concept'] = 'business_purpose'
PROFILES['loan_repayment_offset_order'][0]['loan_concept'] = 'payment_allocation'
PROFILES['loan_overdue_interest'][0]['loan_concept'] = 'overdue_rate'
PROFILES['loan_overdue_interest'][1]['loan_concept'] = 'overdue_base'
PROFILES['loan_overdue_interest'][2]['loan_concept'] = 'overdue_period'

# Grading metadata only: existing address protections mitigate a residual
# collection-channel gap; they do not establish the missing channel itself.
for _element in PROFILES['loan_notice_service_method']:
    _element['residual_risk_kind'] = 'procedural_channel'
    _element['protective_mechanism'] = _element['element_id'] != 'loan_collection_channel'

RECEIPT_ACKNOWLEDGEMENT = r'(?:今|已)收到(?:贷款人|出借人).{1,20}(?:现金|转账|借款|人民币)[\d,，.]+元'

def supports(element, text):
    from review_v2.unified_facts.store import CURRENT
    store = CURRENT.get()
    if store is not None:
        from review_v2.unified_facts.loan import element_concept
        rows = store.get(element_concept(element['element_id']), consumer='loan_facts.supports')
        supported = any(f.get('normalized_value') is True and any(e['quote'] == text for e in f['evidence']) for f in rows)
        store.record_decision(element['element_id'], 'EVIDENCE_SUPPORT', {'supported': supported},
                              [element_concept(element['element_id'])])
        return supported
    if element.get('loan_concept'):
        return bool(concept_facts(element['loan_concept'], text))
    if element.get('element_id') in {'loan_disbursement_record','loan_voucher_creditor','loan_receipt_document'} and re.search(RECEIPT_ACKNOWLEDGEMENT,compact(text)):
        return True
    if element.get('element_id') == 'loan_early_application' and re.search(r'无需[^。；]{0,10}(?:申请|同意)|不得申请',compact(text)):
        # Waiving consent is not a positive approval procedure, but it does
        # not negate a separately stated notification procedure.
        return any(all(re.search(p, compact(text)) for p in path)
                   for path in element.get('alternative_patterns', []))
    if element.get("element_id") == "loan_agreed_rate":
        # A penalty/overdue rate does not establish interest during the loan.
        text = re.sub(r"(?:逾期|罚息|违约)[^。；;]*", "", text)
    paths = [element.get('loan_patterns', [])] + element.get('alternative_patterns', [])
    return any(path and all(re.search(p, compact(text)) for p in path) for path in paths)


def units(clauses):
    from review_v2.unified_facts.store import CURRENT, fail
    if CURRENT.get() is not None:
        fail('RAW_FACT_REEXTRACTION_FORBIDDEN', 'loan_facts.units')
    for clause in formal_evidence_clauses(list(clauses)):
        if clause.block_type not in {"OPERATIVE_CLAUSE", "ANNEX", "PARTY_INFORMATION"}:
            continue
        for quote in re.split(r"(?<=[。；;])|\n", clause.text):
            if quote.strip():
                yield clause, quote.strip()

def _context_units(clauses):
    """Yield clause-level context so facts split across lines can be joined."""
    for clause in formal_evidence_clauses(list(clauses)):
        if clause.block_type in {"OPERATIVE_CLAUSE", "ANNEX", "PARTY_INFORMATION"}:
            text = clause.text.strip()
            if text:
                yield clause, text


def financing_charge(text):
    """Positive financing charges, not enforcement costs or a prohibition."""
    for part in re.split(r"[。；;]", compact(text)):
        for hit in re.finditer(r"服务费|管理费|咨询费|手续费|综合费率|融资费|账户维护费", part):
            before_full = part[max(0, hit.start()-40):hit.start()]
            # Adversative clauses reset scope; the morpheme 另 in 不另行 does
            # not. Coordinated fee nouns inherit the governing negation.
            before = re.split(r"[，,]|但是|但", part[:hit.start()])[-1]
            if re.search(r"(?:不收取|不另行收取|免收|无需支付|不存在)\s*$", before_full):
                continue
            if re.search(r"不得|不收取|不另(?:行)?收取|免收|无须|无需|不支付|不存在|不承担", before):
                continue
            # Debt collection counsel/service costs are enforcement expenses.
            if re.search(r"诉讼|执行|催收|维权|实现债权", before):
                continue
            if re.search(r"收取|支付|扣除|扣收|预扣|承担|计收|按.{0,8}[%％]|为.{0,8}[%％元]", part):
                return True
    return False


def extract(node, clauses):
    from review_v2.unified_facts.store import CURRENT
    if CURRENT.get() is not None:
        from review_v2.unified_facts.loan import evidence_for
        return evidence_for(CURRENT.get(), node)
    rows = []
    if node=='loan_financial_private_distinction':
        kind, ids=_party_kind(clauses,'lender')
        source=((c,c.text) for c in formal_evidence_clauses(list(clauses)) if kind!='unknown' and c.clause_id in ids)
    else:
        # Clause context is the retrieval unit.  Article titles and adjacent
        # sentences commonly carry the missing half of a loan fact.
        source=_context_units(clauses)
    for clause, quote in source:
        specs = PROFILES.get(node, [])
        # Retrieval and acceptance use the same typed proposition. Keep its
        # operative span, never the surrounding prohibition as primary proof.
        for element in specs:
            if not element.get('loan_concept'):
                continue
            for fact in concept_facts(element['loan_concept'], quote):
                rows.append({'clause_id':clause.clause_id, 'text':fact['quote'], 'quote':fact['quote'],
                             'location':clause.location,'section_type':clause.section_type,
                             'block_type':clause.block_type,'source_type':'CONTRACT_TEXT',
                             'evidence_id':f'{clause.clause_id}-LOAN-{len(rows)+1}',
                             'entailment_status':'SUPPORTS','semantic_score':1.0,
                             'supports_element_ids':[element['element_id']],
                             'semantic_normalization':fact})
        keys = [e["element_id"] for e in specs if not e.get('loan_concept') and supports(e, quote)]
        if node == "loan_hidden_fee_over_cap" and financing_charge(quote):
            keys = ["loan_financing_charge"]
        if keys:
            location=clause.location
            # A receipt may be embedded after the last numbered article.
            headings=list(re.finditer(r'(?:^|\n)\s*(收款收据|借款收据|借据|借条|收条)\s*(?:\n|$)',clause.text))
            if headings and clause.text.find(quote)>headings[-1].start():
                location=headings[-1].group(1)
            rows.append({"clause_id": clause.clause_id, "text": quote, "quote": quote,
                         "location": location, "section_type": clause.section_type,
                         "block_type": clause.block_type, "source_type": "CONTRACT_TEXT",
                         "evidence_id": f"{clause.clause_id}-LOAN-{len(rows)+1}",
                         "entailment_status": "SUPPORTS", "semantic_score": 1.0,
                         "supports_element_ids": keys})
    merged = {}
    for r in rows:
        key = (r['clause_id'], r['quote'])
        target = merged.setdefault(key, r)
        target['supports_element_ids'] = list(dict.fromkeys(target['supports_element_ids'] + r['supports_element_ids']))
        if r.get('semantic_normalization'):
            target.setdefault('normalization_by_element', {}).update(
                {element: r['semantic_normalization'] for element in r['supports_element_ids']})
    rows = list(merged.values())
    rows.sort(key=lambda r: r.get('semantic_normalization',{}).get('directness',0),reverse=True)
    return rows


def _positive(text, pattern, *, actual=False):
    for part in re.split(r"[。；;\n]", text):
        for hit in re.finditer(pattern, part):
            prefix = part[max(0, hit.start()-12):hit.end()]
            if re.search(r"不涉及|不存在|不用于|不得用于|禁止|并非|不采用|无须|无需|不得办理|不办理|不允许|不予办理", prefix):
                continue
            if actual and re.search(r"如|若|假如|可能|不得", part[:hit.start()]):
                continue
            return True
    return False


def _party_kind(clauses, role):
    marker = r"(?:出借人|出借方|贷款人|贷款方|贷方)" if role == "lender" else r"(?:借款人|借款方|借方)"
    all_text = '\n'.join(c.text for c in formal_evidence_clauses(list(clauses)))
    sides = set(re.findall(r'([甲乙丙丁]方)[（(]'+marker+r'[）)]',all_text))
    for m in re.finditer(r'([甲乙丙丁]方)(?:应|同意)?向([甲乙丙丁]方)(?:提供|支付|发放|出借)借款',compact(all_text)):
        sides.add(m[1] if role=='lender' else m[2])
    declaration = '(?:'+marker+'|'+ '|'.join(map(re.escape, sorted(sides)))+')' if sides else marker
    found = []
    for clause in formal_evidence_clauses(list(clauses)):
        if clause.block_type not in {"OPERATIVE_CLAUSE", "ANNEX", "PARTY_INFORMATION"}:
            continue
        text = compact(clause.text)
        # Role-bound declarations only, never references to a receiving bank.
        m = re.search(declaration + r"(?:[（(][^）)]{0,12}[）)])?[）)]?[：:]([^。；;]{1,160})", text)
        if not m and sides:
            # Only an account explicitly owned by the resolved side may
            # establish that party's identity; its开户行 is never the party.
            owner='(?:'+'|'.join(map(re.escape,sorted(sides)))+')'
            m=re.search(owner+r'[^。；]{0,35}账户[^。；]{0,15}(?:账户名称|户名|开户名)[：:]([^。；;]{1,100})',text)
        if not m:
            continue
        value = re.split(r"[甲乙丙丁]方[（(:：]|(?:借款人|出借人|贷款人|保证人|担保人|配偶)(?:[（(]|[：:])", m.group(1))[0]
        value = re.split(r'住所|住址|联系地址|联系电话|开户银行|开户行|法定代表人|统一社会信用代码',value)[0]
        if re.match(r"[_＿\s]+$", value):
            continue
        if re.search(r"银行|信用合作|信用社|持牌金融机构|消费金融公司|信托公司|财务公司", value[:40]):
            kind = "financial"
        elif re.search(r"公司|企业|法人|合伙|合作社|统一社会信用代码", value):
            kind = "enterprise"
        elif re.search(r"身份证|自然人", value):
            kind = "natural"
        else:
            # Link a role-bound name to its separate identity declaration;
            # never infer a natural person solely from a short Chinese name.
            name=re.split(r'，|,|地址|联系电话|签署日期|联系地址|\n',value)[0]
            identity=[c for c in clauses if name and re.search(
                r'(?:姓名[：:]?\s*)?'+re.escape(name)+r'\s*(?:证件类型[：:]?)?(?:居民身份证|身份证|证件号码)', compact(c.text))]
            # Identity belongs to this declared party, never another person
            # elsewhere in the document (e.g. guarantor or contact).
            if not name or not identity:
                continue
            kind='natural'
            found.extend((kind,c.clause_id) for c in identity)
        found.append((kind, clause.clause_id))
    kinds = {k for k, _ in found}
    return (next(iter(kinds)) if len(kinds) == 1 else "unknown", [i for _, i in found])


@dataclass
class LoanFacts:
    values: dict
    evidence: dict
    searched_clause_ids: list

    @classmethod
    def from_clauses(cls, clauses):
        from review_v2.unified_facts.store import CURRENT
        if CURRENT.get() is not None:
            from review_v2.unified_facts.loan import project_shared
            return project_shared(CURRENT.get())
        source = list(units(clauses))
        text = "\n".join(compact(q) for _, q in source)
        lender, lender_ids = _party_kind(clauses, "lender")
        borrower, borrower_ids = _party_kind(clauses, "borrower")
        patterns = {
            "guarantee": r"连带责任保证|保证人|保证期间|一般保证|保证担保",
            "security": r"抵押|质押|保证人|连带责任保证",
            "refinancing": r"借新还旧|新贷.{0,15}(?:偿还|归还|结清).{0,12}旧贷|(?:借款|贷款).{0,15}(?:偿还|归还|结清).{0,12}(?:旧贷|旧借款|原借款|原贷款)",
            "sale_security": r"买卖担保|让与担保|(?:买卖|过户|回购).{0,30}(?:担保|借款)|(?:担保|借款).{0,30}(?:买卖|过户|回购)",
            "extension": r"展期|延期还款|延长还款期限",
            "early_repayment": r"提前还款|提前偿还|提前清偿|提前归还",
            "household": r"家庭日常生活|家庭生活开支|日常家用",
            "joint_business": r"夫妻共同经营|共同生产经营",
            "spouse": r"配偶|夫妻|丈夫|妻子",
            "compound": r"复利|利滚利|利息计息|利息计入本金",
            "limitation_risk": r"诉讼时效.{0,12}(?:届满|已过|临近|不足)|保证期间.{0,12}(?:届满未|已过|临近|不足)|已逾期.{0,6}(?:三|四|五|[3-9])年|未在保证期间.{0,12}主张",
        }
        values = {"lender_kind": lender, "borrower_kind": borrower}
        values["party_type"] = "natural_person" if lender == borrower == "natural" else "mixed" if lender != borrower else lender
        values["lender_party_type"] = lender
        values["borrower_party_type"] = borrower
        evidence = {"lender_kind": lender_ids, "borrower_kind": borrower_ids}
        for key, pattern in patterns.items():
            hits = [c.clause_id for c, q in source if _positive(compact(q), pattern, actual=key in {"refinancing", "limitation_risk", "security", "guarantee"})
                    and not (key in {'security','guarantee'} and re.search(r'费用|公证费|评估费',q) and not re.search(r'提供.{0,15}担保|承担.{0,15}保证责任|以.{0,30}(?:抵押|质押)',q))
                    and not (key in {'security','guarantee'} and re.search(r'无抵押|无保证|无需担保|不设担保',q))]
            values[key], evidence[key] = bool(hits), hits
        excluded=[c.clause_id for c,q in source if re.search(r'(?:本贷款|本借款|贷款)[^。；]{0,8}(?:不得|不予|不允许|不能|不)[^。；]{0,5}(?:办理)?展期',compact(q))]
        vouchers=[c.clause_id for c,q in source if re.search(r'借据|欠条|借条|收据|放款凭证|银行回单|系统放款记录',q)]
        values['voucher_mechanism'],evidence['voucher_mechanism']=bool(vouchers),vouchers
        instruments=[c.clause_id for c,q in source if re.search(r'(?:出具|签署|签发|另附|提供|附件)[^。；]{0,12}(?:借据|借条|欠条|收据)|(?:借据|借条|欠条|收据)[^。；]{0,15}(?:载明|记载|注明|收到|借款金额|组成部分)|^(?:收款)?(?:借据|借条|欠条|收据)[：:]?',compact(q))
                     and not re.search(r'无需|不另行|不出具',q)]
        # An embedded receipt declaration is itself an instrument even without
        # a separate title or file. Use the same fact as evidence satisfaction.
        instruments=list(dict.fromkeys(instruments+[c.clause_id for c,q in source
                         if re.search(RECEIPT_ACKNOWLEDGEMENT,compact(q))]))
        values['debt_instrument'],evidence['debt_instrument']=bool(instruments),instruments
        values['extension_excluded'],evidence['extension_excluded']=bool(excluded),excluded
        if excluded:
            values['extension']=False
        for key, node in {"maturity": "loan_repayment_deadline", "agreed_rate": "loan_interest_rate_agreed"}.items():
            rows = extract(node, clauses)
            values[key], evidence[key] = bool(rows), rows
        return cls(values, evidence, list(dict.fromkeys(c.clause_id for c, _ in source)))

    def applicability(self, node):
        v = self.values
        tests = {
            "loan_financial_interest_compliance": (("lender_kind",), None if v["lender_kind"] == "unknown" else v["lender_kind"] == "financial"),
            "loan_interest_lpr_cap": (("lender_kind",), None if v["lender_kind"] == "unknown" else v["lender_kind"] != "financial"),
            "loan_enterprise_business_need": (("lender_kind", "borrower_kind"), False if any(k in {"natural","financial"} for k in (v["lender_kind"], v["borrower_kind"])) else None if "unknown" in (v["lender_kind"], v["borrower_kind"]) else v["lender_kind"] == v["borrower_kind"] == "enterprise"),
            "loan_natural_person_formation": (("lender_kind", "borrower_kind"), False if any(v[k] in {"enterprise", "financial"} for k in ("lender_kind", "borrower_kind")) else None if "unknown" in (v["lender_kind"], v["borrower_kind"]) else True),
            "loan_sale_security_distinction": (("sale_security",), v["sale_security"]),
            "loan_interest_no_agreement_rule": (("agreed_rate",), not v["agreed_rate"]),
            "loan_compound_interest_limit": (("compound",), v["compound"]),
        }
        if node.startswith("loan_extension_"):
            keys = ("extension", "guarantee") if "guarantor" in node else ("extension",)
            tests[node] = (keys, all(v[k] for k in keys))
        if node in {'loan_relending_bank_loan_invalid','loan_professional_lender_invalid'}:
            tests[node]=(('lender_kind',),v['lender_kind']!='financial')
        if node in {'loan_voucher_creditor_identification','loan_note_receipt_attachment'}:
            tests[node]=(('debt_instrument',),v['debt_instrument'])
        if node.startswith("loan_early_repayment_") or node == "loan_unreasonable_early_repayment_penalty":
            tests[node] = (("early_repayment",), v["early_repayment"])
        if node in GUARANTEE_NODES:
            tests[node] = (("guarantee",), v["guarantee"])
        if node == "loan_old_for_new_guarantor_notice":
            tests[node] = (("refinancing", "guarantee"), v["refinancing"] and v["guarantee"])
        if node == "loan_guarantee_attachment":
            tests[node] = (("security",), v["security"])
        if node in HOUSEHOLD_NODES:
            tests[node] = (("household",), v["household"])
        if node in JOINT_BUSINESS_NODES:
            tests[node] = (("joint_business",), v["joint_business"])
        if node in SPOUSE_NODES:
            tests[node] = (("spouse",), v["spouse"])
        if node == "loan_beyond_family_need_evidence":
            tests[node] = (("spouse", "household", "joint_business"), v["spouse"] and (v["joint_business"] or not v["household"]))
        keys, applicable = tests.get(node, ((), True))
        if any(getattr(self, 'verified_states', {}).get(k) in {'UNCERTAIN', 'UNKNOWN', 'CONFLICT', 'DEFERRED'} for k in keys):
            applicable = None
        state = "UNCERTAIN" if applicable is None else "APPLICABLE" if applicable else "NOT_APPLICABLE"
        reason = ("主体信息不足，无法确认专项规则的适用前提。" if applicable is None else
                  "已确认规则适用前提。" if applicable else "合同未触发该专项规则的适用场景，不要求补写该场景条款。")
        if node.startswith('loan_extension_') and v.get('extension_excluded'):
            keys=(*keys,'extension_excluded')
            reason='合同明确排除办理展期，不要求补充展期申请、利率或批准后安排。'
        if node=='loan_note_receipt_attachment' and v['lender_kind']=='financial':
            reason='金融借款不强制采用民间借贷纸质借据；放款记录与电子凭证由实际放款证据规则核验。'
        result = {"status": state, "applicable": applicable, "reason": reason, "user_reason": reason,
                "machine_reason": reason, "depends_on": list(keys),
                "trigger_facts": {k: v[k] for k in keys},
                "source_evidence": {k: self.evidence[k] for k in keys},
                "searched_clause_ids": self.searched_clause_ids,
                "confidence": "low" if applicable is None else "high"}
        if hasattr(self, 'verified_store'):
            concepts = [self.verified_concept_keys[k] for k in keys]
            self.verified_store.record_decision(node, 'APPLICABILITY', result, concepts)
        return result


# Semantic node IDs are the stable rule interface; no document identifiers.
GUARANTEE_NODES = {"loan_guarantee_type_joint_or_general", "loan_guarantee_period", "loan_guarantee_scope", "loan_guarantor_collection_within_period"}
HOUSEHOLD_NODES = {"loan_daily_family_need"}
JOINT_BUSINESS_NODES = {"loan_joint_business_need"}
SPOUSE_NODES = {"loan_spousal_joint_intent", "loan_beyond_family_need_evidence"}
OPTIONAL_NODES = {"loan_repayment_offset_order", "loan_repayment_receipt_confirmation", "loan_collection_ack_limitation_interruption", "loan_guarantor_collection_within_period", "loan_collection_record_attachment"}


def consistency_gate(items, facts):
    """Fail closed if a downstream stage contradicts the shared loan facts."""
    failures = []
    by_node = {i.node_id: i for i in items}
    def fail(item, reason):
        failures.append({"requirement": "LOAN_SHARED_FACT_CONSISTENCY", "review_id": item.item_id,
                         "failure_stage": "Final Loan Fact Validation", "root_cause": reason,
                         "current_status": "FAIL"})
    for item in items:
        specs=item.decision_trace.get("loan_cost_elements") or PROFILES.get(item.node_id,[])
        supported = {e['element_id'] for e in specs if any(
            supports(e, row.get('quote') or row.get('text',''))
            for row in item.evidence_clauses) and not e.get('loan_cost_element')}
        missing = {e.get('element_id') for e in item.decision_trace.get('coverage_elements', [])
                   if e.get('status') == 'MISSING'}
        missing.update(item.decision_trace.get('final_missing_element_ids', []))
        if supported & missing and item.coverage_status != '不适用':
            fail(item, '已验证证据与缺失要素冲突：'+','.join(sorted(supported & missing)))
        if specs and item.coverage_status=='通过':
            for element in specs:
                if item.decision_trace.get('loan_cost_elements'):
                    from review_v2.engine import _element_supported_by_evidence
                    if not any(_element_supported_by_evidence(element,e)[0]=='COVERED' for e in item.evidence_clauses):
                        fail(item,'融资组合要素缺少绑定原文：'+element['element_id'])
                    continue
                if not any(element['element_id'] in e.get('supports_element_ids',[]) and supports(element,e.get('quote') or e.get('text','')) for e in item.evidence_clauses):
                    fail(item,'已覆盖要素缺少直接蕴含该事实的绑定原文：'+element['element_id'])
        expected = facts.applicability(item.node_id)
        costs = item.decision_trace.get("loan_cost_assessment")
        if costs:
            protection = costs.get('judicial_protection', {})
            expected_status = {'PENDING': {'待核验','法律提示'}, 'RISK': {'风险条款'}, 'PASS': {'通过'}}
            if item.coverage_status not in expected_status.get(protection.get('status'), set()):
                fail(item, '司法保护范围评估与最终状态不一致，不得将外部待核验转为合同缺失或已确认合法。')
            if protection.get('status') == 'PENDING' and missing:
                fail(item, '外部司法保护范围待核验不得制造合同文本缺失要素。')
        external = item.decision_trace.get("external_fact_assessment")
        if external and external.get("external_fact_status") != "NOT_VERIFIED":
            fail(item, "仅凭合同文本不得确认合同外风险事实不存在。")
        if expected["applicable"] is False and item.coverage_status != "不适用":
            fail(item, "下游结论违背适用性前置门控。")
        if item.node_id == "loan_hidden_fee_over_cap" and item.coverage_status == "风险条款":
            if not item.evidence_clauses or any(not financing_charge(e.get("quote") or e.get("text", "")) for e in item.evidence_clauses):
                fail(item, "融资收费风险缺少与收费事实直接绑定的证据。")
        if item.decision_trace.get("optional_without_specific_exposure") and item.coverage_status in {"缺失", "部分覆盖"}:
            if item.risk_severity not in {"LOW", "NONE"} or item.action_priority not in {"C_OPTIMIZATION", "NONE"}:
                fail(item, "无具体风险事实的法定默认或证据管理事项被错误升级。")
    producer = by_node.get("loan_repayment_deadline")
    consumer = by_node.get("loan_limitation_start")
    if producer and consumer and producer.coverage_status == "通过":
        if consumer.coverage_status != "通过":
            fail(consumer, "已确认的还款期限未被下游时效规则复用。")
        elif producer.decision_trace.get("shared_fact_consumption") != consumer.decision_trace.get("shared_fact_consumption"):
            fail(consumer, "时效起算与还款期限未引用同一事实证据。")
    return {"status": "BLOCKED" if failures else "REPORT_READY", "failures": failures,
            "gate_results": {"LOAN_SHARED_FACT_CONSISTENCY": "FAIL" if failures else "PASS"}}


NEGATIVE_SCANS = {
 'loan_deducted_interest_forbidden': (r'(?:预扣|先扣|预先扣除)[^。；]{0,12}(?:利息|服务费)|从[^。；]{0,8}本金[^。；]{0,8}扣除[^。；]{0,8}利息',),
 'loan_unreasonable_early_repayment_penalty': (r'提前(?:还款|偿还|清偿)',r'违约金|罚金|补偿金|手续费|禁止提前还款'),
 'loan_hidden_fee_over_cap': (),
}

def negative_scan(node, clauses):
    from review_v2.unified_facts.store import CURRENT, fail
    if CURRENT.get() is not None:
        fail('RAW_FACT_REEXTRACTION_FORBIDDEN', 'loan_facts.negative_scan:' + node)
    """Reproducible adverse-fact search, not proof of legal/external safety."""
    import hashlib
    if node not in NEGATIVE_SCANS:
        return None
    source=list(_context_units(clauses) if node == 'loan_hidden_fee_over_cap' else units(clauses)); hits=[]
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
