"""Evidence-bound loan facts shared by applicability, coverage and risk assessment.

Only operative text/annexes and party declarations establish facts.  A bank
account, a remedy-cost list or generic statutory wording is not a transaction.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from review_v2.clause_parser import formal_evidence_clauses


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
        atom("loan_address_change_notice", "地址变更通知", r"住址|地址", r"变化|变更", r"书面通知|通知对方"),
        atom("loan_collection_channel", "催收通知方式或渠道", r"催收|催告", r"书面|邮寄|短信|电子邮件|邮箱|微信|电话|送达")],
    "loan_financial_private_distinction": [atom("loan_lender_identity", "贷款人主体身份可用于区分金融借款与民间借贷", r"贷款人|出借人", r"身份证|自然人|银行|信用社|公司|企业")],
    "loan_note_receipt_attachment": [atom("loan_receipt_document", "实际借据、收据或欠条", r"收据|借据|借条|欠条", r"收到|借到|借款金额|欠款金额")],
    "loan_actual_disbursement_evidence": [atom("loan_disbursement_record", "实际放款或到账凭证及确认", r"放款|借款|贷款|本金|到账", r"转账凭证|放款凭证|到账确认|收款收据|银行回单|收据|借据", r"作为|证明|确认|保存|出具|提供|记录")],
    "loan_voucher_creditor_identification": [atom("loan_voucher_creditor", "债权凭证载明债权人身份", r"借据|借条|欠条|收据|债权凭证", r"载明|注明|记载|列明", r"出借人|债权人|贷款人")],
    "loan_interest_calculation_base": [
        atom("loan_interest_base", "利息计算基数", r"利息|计息", r"本金余额|未偿还本金|实际收到|实际占用|以.{0,15}本金.{0,8}(?:基数|计算)"),
        atom("loan_interest_period", "利息起止期间", r"利息|计息", r"自.{0,30}(?:至|止)|起算|计息期间")],
    "loan_repayment_method_account": [
        atom("loan_repayment_method", "还款支付方式", r"还款|偿还|归还借款", r"转账|现金|汇款|划扣"),
        atom("loan_repayment_account", "还款收款账户或指定机制", r"还款|偿还|归还借款", r"账户|账号|户名|开户行")],
    "loan_guarantee_attachment": [atom("loan_security_document", "具体担保文件及附件安排", r"保证合同|抵押合同|质押合同|担保合同|担保人授权书|抵押登记证明", r"附件|附具|提供|提交|编号|签署")],
    "loan_collection_record_attachment": [atom("loan_collection_records", "催收或还款记录的保存安排", r"催收函|催收记录|还款回单|还款记录|还款承诺书|对账单", r"保存|留存|附件|保留|提供|提交")],
    "loan_repayment_deadline": [DEADLINE],
    "loan_limitation_start": [DEADLINE],
    "loan_interest_rate_agreed": [RATE],
    "loan_repayment_offset_order": [atom("loan_offset_order", "部分还款的抵充顺序", r"抵充|冲抵|清偿顺序|偿还顺序", r"先|依次|顺序")],
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


# Payment evidence is shared across the substantive and document-check rules.
# Cash receipts and bank vouchers are alternatives, not cumulative requirements.
PROFILES['loan_transfer_voucher_attachment'] = PROFILES['loan_actual_disbursement_evidence']

# Grading metadata only: existing address protections mitigate a residual
# collection-channel gap; they do not establish the missing channel itself.
for _element in PROFILES['loan_notice_service_method']:
    _element['residual_risk_kind'] = 'procedural_channel'
    _element['protective_mechanism'] = _element['element_id'] != 'loan_collection_channel'

def supports(element, text):
    if element.get('element_id') in {'loan_disbursement_record','loan_voucher_creditor','loan_receipt_document'} and re.search(r'(?:今|已)收到(?:贷款人|出借人).{1,20}(?:现金|转账|借款|人民币)[\d,，.]+元',compact(text)):
        return True
    if element.get("element_id") == "loan_agreed_rate":
        # A penalty/overdue rate does not establish interest during the loan.
        text = re.sub(r"(?:逾期|罚息|违约)[^。；;]*", "", text)
    return all(re.search(p, compact(text)) for p in element.get("loan_patterns", []))


def units(clauses):
    for clause in formal_evidence_clauses(list(clauses)):
        if clause.block_type not in {"OPERATIVE_CLAUSE", "ANNEX", "PARTY_INFORMATION"}:
            continue
        for quote in re.split(r"(?<=[。；;])|\n", clause.text):
            if quote.strip():
                yield clause, quote.strip()


def financing_charge(text):
    """Positive financing charges, not enforcement costs or a prohibition."""
    for part in re.split(r"[。；;]", compact(text)):
        for hit in re.finditer(r"服务费|管理费|咨询费|手续费|综合费率|融资费|账户维护费", part):
            before = re.split(r"[，,]|但是|但|另", part[:hit.start()])[-1][-22:]
            if re.search(r"不得|不收取|不另收|免收|无须|无需|不支付|不存在|不承担", before):
                continue
            # Debt collection counsel/service costs are enforcement expenses.
            if re.search(r"诉讼|执行|催收|维权|实现债权", before):
                continue
            if re.search(r"收取|支付|扣除|扣收|预扣|承担|计收|按.{0,8}[%％]|为.{0,8}[%％元]", part):
                return True
    return False


def extract(node, clauses):
    rows = []
    if node=='loan_financial_private_distinction':
        kind, ids=_party_kind(clauses,'lender')
        source=((c,c.text) for c in formal_evidence_clauses(list(clauses)) if kind!='unknown' and c.clause_id in ids)
    else:
        source=units(clauses)
    for clause, quote in source:
        keys = [e["element_id"] for e in PROFILES.get(node, []) if supports(e, quote)]
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
    return rows


def _positive(text, pattern, *, actual=False):
    for part in re.split(r"[。；;\n]", text):
        for hit in re.finditer(pattern, part):
            prefix = part[max(0, hit.start()-12):hit.end()]
            if re.search(r"不涉及|不存在|不用于|不得用于|禁止|并非|不采用|无须|无需", prefix):
                continue
            if actual and re.search(r"如|若|假如|可能|不得", part[:hit.start()]):
                continue
            return True
    return False


def _party_kind(clauses, role):
    marker = r"(?:出借人|贷款人|贷方)" if role == "lender" else r"(?:借款人|借方)"
    found = []
    for clause in formal_evidence_clauses(list(clauses)):
        if clause.block_type not in {"OPERATIVE_CLAUSE", "ANNEX", "PARTY_INFORMATION"}:
            continue
        text = compact(clause.text)
        # Role-bound declarations only, never references to a receiving bank.
        m = re.search(marker + r"(?:[（(][^）)]{0,12}[）)])?[：:]([^。；;]{1,90})", text)
        if not m:
            continue
        value = re.split(r"(?:借款人|出借人|贷款人|保证人|担保人|配偶)(?:[（(]|[：:])", m.group(1))[0]
        if re.match(r"[_＿\s]+$", value):
            continue
        if re.search(r"银行|信用合作|信用社|持牌金融机构|消费金融公司|信托公司|财务公司", value[:40]):
            kind = "financial"
        elif re.search(r"公司|企业|法人|合伙|合作社|统一社会信用代码", value):
            kind = "enterprise"
        elif re.search(r"身份证|自然人", value):
            kind = "natural"
        else:
            continue
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
        evidence = {"lender_kind": lender_ids, "borrower_kind": borrower_ids}
        for key, pattern in patterns.items():
            hits = [c.clause_id for c, q in source if _positive(compact(q), pattern, actual=key in {"refinancing", "limitation_risk", "security", "guarantee"})
                    and not (key in {'security','guarantee'} and re.search(r'费用|公证费|评估费',q) and not re.search(r'提供.{0,15}担保|承担.{0,15}保证责任|以.{0,30}(?:抵押|质押)',q))
                    and not (key in {'security','guarantee'} and re.search(r'无抵押|无保证|无需担保|不设担保',q))]
            values[key], evidence[key] = bool(hits), hits
        for key, node in {"maturity": "loan_repayment_deadline", "agreed_rate": "loan_interest_rate_agreed"}.items():
            rows = extract(node, clauses)
            values[key], evidence[key] = bool(rows), rows
        return cls(values, evidence, list(dict.fromkeys(c.clause_id for c, _ in source)))

    def applicability(self, node):
        v = self.values
        tests = {
            "loan_financial_interest_compliance": (("lender_kind",), None if v["lender_kind"] == "unknown" else v["lender_kind"] == "financial"),
            "loan_interest_lpr_cap": (("lender_kind",), None if v["lender_kind"] == "unknown" else v["lender_kind"] != "financial"),
            "loan_enterprise_business_need": (("lender_kind", "borrower_kind"), False if "natural" in (v["lender_kind"], v["borrower_kind"]) else None if "unknown" in (v["lender_kind"], v["borrower_kind"]) else v["lender_kind"] == v["borrower_kind"] == "enterprise"),
            "loan_natural_person_formation": (("lender_kind", "borrower_kind"), False if any(v[k] in {"enterprise", "financial"} for k in ("lender_kind", "borrower_kind")) else None if "unknown" in (v["lender_kind"], v["borrower_kind"]) else True),
            "loan_sale_security_distinction": (("sale_security",), v["sale_security"]),
            "loan_interest_no_agreement_rule": (("agreed_rate",), not v["agreed_rate"]),
            "loan_compound_interest_limit": (("compound",), v["compound"]),
        }
        if node.startswith("loan_extension_"):
            keys = ("extension", "guarantee") if "guarantor" in node else ("extension",)
            tests[node] = (keys, all(v[k] for k in keys))
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
        state = "UNCERTAIN" if applicable is None else "APPLICABLE" if applicable else "NOT_APPLICABLE"
        reason = ("主体信息不足，无法确认专项规则的适用前提。" if applicable is None else
                  "已确认规则适用前提。" if applicable else "合同未触发该专项规则的适用场景，不要求补写该场景条款。")
        return {"status": state, "applicable": applicable, "reason": reason, "user_reason": reason,
                "machine_reason": reason, "depends_on": list(keys),
                "trigger_facts": {k: v[k] for k in keys},
                "source_evidence": {k: self.evidence[k] for k in keys},
                "searched_clause_ids": self.searched_clause_ids,
                "confidence": "low" if applicable is None else "high"}


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
        specs=PROFILES.get(item.node_id,[])
        if specs and item.coverage_status=='通过':
            for element in specs:
                if not any(element['element_id'] in e.get('supports_element_ids',[]) and supports(element,e.get('quote') or e.get('text','')) for e in item.evidence_clauses):
                    fail(item,'已覆盖要素缺少直接蕴含该事实的绑定原文：'+element['element_id'])
        expected = facts.applicability(item.node_id)
        costs = item.decision_trace.get("loan_cost_assessment")
        if costs and costs["needs_check"] and item.coverage_status not in {"部分覆盖", "风险条款"}:
            fail(item, "逾期融资成本组合校验尚未完成，禁止被下游改为通过。")
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
