"""Loan-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import _format_output, _mentions, _parse_date, _years_between
from adjudicate.loan_configs import get_loan_config


@dataclass
class LoanFacts:
    raw_text: str
    contract_type: str = "loan"
    contract_type_name: str = "借款合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    loan_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    financial_institution_lender: bool = False
    private_lender: bool = False
    sale_security: bool = False
    natural_person_loan: bool = False
    loan_provided: bool = False
    loan_not_provided: bool = False
    contract_invalid: bool = False
    relending_bank_loan: bool = False
    illegal_fund_source: bool = False
    illegal_purpose_known: bool = False
    public_order_violation: bool = False
    professional_lender_claim: bool = False
    professional_lender_proved: bool = False
    enterprise_loan: bool = False
    business_need: bool = False
    loan_voucher: bool = False
    voucher_no_creditor: bool = False
    only_transfer_record: bool = False
    other_purpose_defense: bool = False
    other_purpose_proved: bool = False
    nominal_principal: float = 0.0
    actual_received: float = 0.0
    deducted_interest: bool = False
    repaid: bool = False
    partial_repayment: bool = False
    repayment_amount: float = 0.0
    cost_amount: float = 0.0
    interest_amount: float = 0.0
    principal_amount: float = 0.0
    interest_agreed: bool = False
    no_interest_agreed: bool = False
    annual_rate: float = 0.0
    monthly_rate: float = 0.0
    lpr_rate: float = 0.0
    overdue_interest: bool = False
    no_overdue_rate: bool = False
    compound_interest: bool = False
    compound_agreed: bool = False
    liquidated_damage_or_fee: bool = False
    early_repayment: bool = False
    early_repayment_forbidden: bool = False
    extension_request: bool = False
    extension_before_due: bool = False
    lender_agreed_extension: bool = False
    guarantee_contract: bool = False
    joint_guarantee: bool = False
    general_guarantee: bool = False
    guarantee_period_expired: bool = False
    loan_old_for_new: bool = False
    same_guarantor: bool = False
    guarantor_knows: bool = False
    guarantor_not_knows: bool = False
    spousal_debt: bool = False
    daily_family_need: bool = False
    joint_business_or_intent: bool = False
    beyond_family_need: bool = False
    misuse_loan: bool = False
    lender_not_provide: bool = False
    lender_late_provide: bool = False
    limitation_defense: bool = False
    collection_or_ack: bool = False
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "loan_contract": self.loan_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "financial_institution_lender": self.financial_institution_lender,
            "private_lender": self.private_lender,
            "sale_security": self.sale_security,
            "natural_person_loan": self.natural_person_loan,
            "loan_provided": self.loan_provided,
            "loan_not_provided": self.loan_not_provided,
            "contract_invalid": self.contract_invalid,
            "relending_bank_loan": self.relending_bank_loan,
            "illegal_fund_source": self.illegal_fund_source,
            "illegal_purpose_known": self.illegal_purpose_known,
            "public_order_violation": self.public_order_violation,
            "professional_lender_claim": self.professional_lender_claim,
            "professional_lender_proved": self.professional_lender_proved,
            "enterprise_loan": self.enterprise_loan,
            "business_need": self.business_need,
            "loan_voucher": self.loan_voucher,
            "voucher_no_creditor": self.voucher_no_creditor,
            "only_transfer_record": self.only_transfer_record,
            "other_purpose_defense": self.other_purpose_defense,
            "other_purpose_proved": self.other_purpose_proved,
            "nominal_principal": self.nominal_principal,
            "actual_received": self.actual_received,
            "deducted_interest": self.deducted_interest,
            "repaid": self.repaid,
            "partial_repayment": self.partial_repayment,
            "repayment_amount": self.repayment_amount,
            "cost_amount": self.cost_amount,
            "interest_amount": self.interest_amount,
            "principal_amount": self.principal_amount,
            "interest_agreed": self.interest_agreed,
            "no_interest_agreed": self.no_interest_agreed,
            "annual_rate": self.annual_rate,
            "monthly_rate": self.monthly_rate,
            "lpr_rate": self.lpr_rate,
            "overdue_interest": self.overdue_interest,
            "no_overdue_rate": self.no_overdue_rate,
            "compound_interest": self.compound_interest,
            "compound_agreed": self.compound_agreed,
            "liquidated_damage_or_fee": self.liquidated_damage_or_fee,
            "early_repayment": self.early_repayment,
            "early_repayment_forbidden": self.early_repayment_forbidden,
            "extension_request": self.extension_request,
            "extension_before_due": self.extension_before_due,
            "lender_agreed_extension": self.lender_agreed_extension,
            "guarantee_contract": self.guarantee_contract,
            "joint_guarantee": self.joint_guarantee,
            "general_guarantee": self.general_guarantee,
            "guarantee_period_expired": self.guarantee_period_expired,
            "loan_old_for_new": self.loan_old_for_new,
            "same_guarantor": self.same_guarantor,
            "guarantor_knows": self.guarantor_knows,
            "guarantor_not_knows": self.guarantor_not_knows,
            "spousal_debt": self.spousal_debt,
            "daily_family_need": self.daily_family_need,
            "joint_business_or_intent": self.joint_business_or_intent,
            "beyond_family_need": self.beyond_family_need,
            "misuse_loan": self.misuse_loan,
            "lender_not_provide": self.lender_not_provide,
            "lender_late_provide": self.lender_late_provide,
            "limitation_defense": self.limitation_defense,
            "collection_or_ack": self.collection_or_ack,
            "notes": self.notes,
        }


def _format_loan_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: LoanFacts,
    path: List[str],
    procedure_findings: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return _format_output(
        major=major,
        minor=minor,
        conclusion=conclusion,
        triggered_items=triggered_items,
        facts=facts,
        path=path,
        procedure_findings=procedure_findings,
        footer_label="触发补丁清单",
    )


def _money(value: float) -> str:
    return f"{value:.2f} 元" if value > 0 else "待核定"


def _extract_money_near(text: str, labels: tuple[str, ...]) -> float:
    money_pattern = r"(\d+(?:\.\d+)?)\s*(万|万元|元|块|人民币)?"

    def normalize(match: re.Match[str]) -> float:
        value = float(match.group(1))
        unit = match.group(2) or ""
        if unit in {"万", "万元"}:
            value *= 10000
        return value

    for label in labels:
        for match in re.finditer(re.escape(label), text):
            after = text[match.end():min(len(text), match.end() + 18)]
            after_match = re.search(money_pattern, after)
            if after_match:
                value = normalize(after_match)
                if value > 0:
                    return value
            before = text[max(0, match.start() - 12):match.start()]
            before_matches = list(re.finditer(money_pattern, before))
            if before_matches:
                value = normalize(before_matches[-1])
                if value > 0:
                    return value
    return 0.0


def _extract_rate_near(text: str, labels: tuple[str, ...]) -> float:
    for label in labels:
        for match in re.finditer(re.escape(label), text):
            windows = (
                text[match.end():min(len(text), match.end() + 14)],
                text[max(0, match.start() - 8):match.start()],
            )
            for window in windows:
                rate_match = re.search(r"(\d+(?:\.\d+)?)\s*%", window)
                if rate_match:
                    return float(rate_match.group(1))
    return 0.0


def extract_loan_facts(case_text: str) -> LoanFacts:
    config = get_loan_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = LoanFacts(raw_text=raw_text)

    for field_name in (
        "loan_contract", "third_party_tort", "financial_institution_lender", "private_lender",
        "sale_security", "natural_person_loan", "loan_provided", "loan_not_provided",
        "contract_invalid", "relending_bank_loan", "illegal_fund_source", "illegal_purpose_known",
        "public_order_violation", "professional_lender_claim", "professional_lender_proved",
        "enterprise_loan", "business_need", "loan_voucher", "voucher_no_creditor",
        "only_transfer_record", "other_purpose_defense", "other_purpose_proved", "deducted_interest",
        "repaid", "partial_repayment", "interest_agreed", "no_interest_agreed", "overdue_interest",
        "no_overdue_rate", "compound_interest", "compound_agreed", "liquidated_damage_or_fee",
        "early_repayment", "early_repayment_forbidden", "extension_request", "extension_before_due",
        "lender_agreed_extension", "guarantee_contract", "joint_guarantee", "general_guarantee",
        "guarantee_period_expired", "loan_old_for_new", "same_guarantor", "guarantor_knows",
        "guarantor_not_knows", "spousal_debt", "daily_family_need", "joint_business_or_intent",
        "beyond_family_need", "misuse_loan", "lender_not_provide", "lender_late_provide",
        "limitation_defense", "collection_or_ack",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.nominal_principal = _extract_money_near(text, config.get_terms("nominal_principal"))
    facts.actual_received = _extract_money_near(text, config.get_terms("actual_received"))
    facts.repayment_amount = _extract_money_near(text, config.get_terms("repayment_amount"))
    facts.cost_amount = _extract_money_near(text, config.get_terms("cost_amount"))
    facts.interest_amount = _extract_money_near(text, config.get_terms("interest_amount"))
    facts.principal_amount = _extract_money_near(text, config.get_terms("principal_amount"))
    facts.annual_rate = _extract_rate_near(text, config.get_terms("annual_rate"))
    facts.monthly_rate = _extract_rate_near(text, config.get_terms("monthly_rate"))
    facts.lpr_rate = _extract_rate_near(text, config.get_terms("lpr_rate"))

    if facts.monthly_rate > 0 and facts.annual_rate <= 0:
        facts.annual_rate = facts.monthly_rate * 12
    if any(phrase in text for phrase in ("借款人提前还款", "借款人提前偿还", "提前偿还借款", "提前归还借款")):
        facts.early_repayment = True
    if any(phrase in text for phrase in ("不能证明其他用途", "无法证明其他用途", "未证明其他用途", "不能证明转账系其他用途")):
        facts.other_purpose_proved = False
    if facts.deducted_interest and facts.nominal_principal > facts.actual_received > 0:
        facts.loan_contract = True
    if any((facts.interest_agreed, facts.no_interest_agreed, facts.guarantee_contract, facts.repaid, facts.early_repayment)):
        facts.loan_contract = True
    return facts


def _procedure_findings(facts: LoanFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("借款合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同履行地未约定或约定不明的，以接受货币一方所在地为合同履行地")
    if facts.asks_defendant:
        findings.append("适格被告通常为借款人；同时主张保证责任且保证期间未过的，可以一并列保证人为被告")
    return findings


def _only_procedure_question(facts: LoanFacts) -> bool:
    substantive = any(
        (
            facts.sale_security, facts.natural_person_loan, facts.loan_not_provided, facts.contract_invalid,
            facts.relending_bank_loan, facts.professional_lender_claim, facts.enterprise_loan,
            facts.only_transfer_record, facts.voucher_no_creditor, facts.deducted_interest,
            facts.repaid, facts.interest_agreed, facts.no_interest_agreed, facts.early_repayment,
            facts.extension_request, facts.guarantee_contract, facts.spousal_debt, facts.misuse_loan,
            facts.lender_not_provide, facts.limitation_defense,
        )
    )
    return (facts.asks_jurisdiction or facts.asks_defendant) and not substantive


def _effective_interest_cap(facts: LoanFacts) -> float:
    return facts.lpr_rate * 4 if facts.lpr_rate > 0 else 0.0


def adjudicate_loan(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_loan_config()
    facts = extract_loan_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "借款合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出本金、利率、还款、效力、担保或时效争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_loan_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.limitation_defense or (facts.contract_date and _years_between(facts.contract_date, today) > 3):
        triggered.append(config.patch_name("L9", "诉讼时效中断"))
        major = "借款合同纠纷适用三年一般诉讼时效。诉讼时效可以因提起诉讼、出借人催收、借款人承诺还款或部分还款而中断，中断后重新计算三年。"
        if facts.collection_or_ack:
            minor = "识别到借款人提出时效抗辩或借款时间较早，但存在催收、还款承诺、部分还款或起诉等时效中断事实。"
            conclusion = "诉讼时效已中断，应从中断事由发生之日起重新计算；是否超过三年需结合中断日期核定。"
        elif facts.contract_date and _years_between(facts.contract_date, today) > 3:
            minor = f"识别到相关借款、到期或应履行日期为{facts.contract_date.isoformat()}，截至{today.isoformat()}已经超过三年，且未识别到时效中断事实。"
            conclusion = "诉讼时效未中断，已经超过三年诉讼时效，驳回超过时效部分请求。"
        else:
            minor = "识别到借款人提出诉讼时效抗辩，但具体到期日和催收情况尚不完整。"
            conclusion = "应先核定还款期限届满日、催收或承诺还款日期，再判断是否超过三年诉讼时效。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "诉讼时效"], procedure_findings)

    if facts.third_party_tort and not facts.loan_contract:
        major = "借款合同裁判引擎处理贷款人、借款人和保证人之间围绕借款本金、利息、还款、担保产生的合同争议；单纯合同外第三人侵权应按侵权责任处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到借款合同履行争议。"
        conclusion = "本案涉及侵权责任，非借款合同纠纷，不适用本借款合同裁判引擎。"
        return _format_loan_output(major, minor, conclusion, [], facts, path, procedure_findings)

    path.append("前置实体判断")
    if facts.financial_institution_lender or facts.private_lender:
        triggered.append(config.patch_name("L1", "金融借款与民间借贷区分"))
        major = "《民法典》第667条规定，借款合同是借款人向贷款人借款，到期返还借款并支付利息的合同；民间借贷司法解释第1条规定，金融机构发放贷款纠纷不适用民间借贷司法解释。"
        if facts.financial_institution_lender:
            minor = "识别到出借人为银行、消费金融公司、信托公司等持牌金融机构。"
            conclusion = "本案为金融借款，适用民法典借款合同章和金融监管规定，不适用民间借贷司法解释的LPR四倍规则。"
        else:
            minor = "识别到出借人为自然人或非持牌主体之间的资金融通。"
            conclusion = "本案为民间借贷，适用民法典借款合同章和民间借贷司法解释。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "合同类型识别"], procedure_findings)

    if facts.sale_security:
        triggered.append(config.patch_name("L11", "以买卖担保借款"))
        major = "当事人以签订买卖合同作为民间借贷合同担保，借款到期后借款人不能还款，出借人请求履行买卖合同的，应按民间借贷法律关系审理。"
        minor = "识别到当事人以买卖合同形式担保借款，出借人请求按买卖合同直接取得标的物或办理过户。"
        conclusion = "本案实质为民间借贷，应按民间借贷法律关系审理；出借人可就担保财产依法申请拍卖、变卖受偿，不能直接请求过户。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "合同类型识别"], procedure_findings)

    if facts.natural_person_loan:
        triggered.append(config.patch_name("L14", "自然人间借款成立时间"))
        major = "《民法典》第679条规定，自然人之间的借款合同，自贷款人提供借款时成立。民间借贷司法解释第9条规定，现金支付自收到借款时成立，转账支付自资金到达借款人账户时成立。"
        minor = "识别到本案为自然人之间借款。"
        if facts.loan_not_provided:
            conclusion = "自然人间借款合同，贷款人未提供借款，合同未成立；借款人无返还本金和支付利息义务。"
        else:
            conclusion = "自然人间借款合同，贷款人已提供借款，合同成立；借款人应按约返还借款并支付依法成立的利息。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "合同成立认定"], procedure_findings)

    if any((facts.contract_invalid, facts.relending_bank_loan, facts.illegal_fund_source, facts.illegal_purpose_known, facts.public_order_violation, facts.professional_lender_claim, facts.enterprise_loan)):
        if facts.professional_lender_claim:
            triggered.append(config.patch_name("L7", "职业放贷人认定"))
        if facts.enterprise_loan:
            triggered.append(config.patch_name("L15", "企业间借贷效力"))
        major = "民间借贷司法解释第11条、第13条规定，为生产经营需要订立的企业间借贷原则上有效；但套取金融机构贷款转贷、非法集资转贷、职业放贷、明知违法犯罪用途、违反强制性规定或违背公序良俗的，借款合同无效。"
        if facts.relending_bank_loan or facts.illegal_fund_source or facts.illegal_purpose_known or facts.public_order_violation or (facts.professional_lender_claim and facts.professional_lender_proved):
            minor = "识别到存在套取贷款转贷、非法资金来源、明知违法用途、公序良俗违反，或职业放贷已经达到反复性、经常性、营业性标准。"
            conclusion = "借款合同无效，借款人应返还实际取得的本金；约定高息不予支持，资金占用损失可按LPR标准核定。"
        elif facts.enterprise_loan and facts.business_need:
            minor = "识别到企业之间为生产经营需要进行资金融通，未识别到法定无效情形。"
            conclusion = "企业间借贷有效，应按合同约定和法定利率上限处理本金、利息及违约责任。"
        elif facts.professional_lender_claim:
            minor = "识别到借款人主张出借人为职业放贷人，但未识别到足以证明反复性、经常性、营业性的事实。"
            conclusion = "出借人暂不构成职业放贷人，借款合同不因该抗辩当然无效。"
        else:
            minor = "识别到合同效力争议，但无效事实尚不完整。"
            conclusion = "需进一步查明资金来源、出借对象、出借频率、借款用途和是否违反强制性规定后认定效力。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.lender_not_provide:
        triggered.append(config.patch_name("L13", "贷款人未按约定提供借款"))
        major = "《民法典》第671条规定，贷款人未按照约定日期、数额提供借款，造成借款人损失的，应当赔偿损失。"
        minor = "识别到贷款人未按约定日期或约定数额提供借款。"
        if facts.loan_not_provided:
            conclusion = f"贷款人未按约定提供借款，造成损失 {_money(facts.principal_amount)}，应赔偿借款人因此受到的损失；借款本金不按未提供金额认定。"
        else:
            conclusion = "贷款人未足额提供借款的，应按实际提供金额认定本金；造成借款人损失的，应承担赔偿责任。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "借贷事实认定"], procedure_findings)

    if facts.only_transfer_record or facts.voucher_no_creditor or facts.deducted_interest:
        path.append("借贷事实认定")
        if facts.only_transfer_record:
            triggered.append(config.patch_name("L5", "仅有转账凭证的借贷关系认定"))
            major = "民间借贷司法解释第17条规定，原告仅依据金融机构转账凭证起诉，被告抗辩转账系偿还双方之前借款或其他债务的，被告应对其主张提供证据证明。"
            minor = "识别到原告只有银行转账凭证，没有借据、欠条等债权凭证。"
            if facts.other_purpose_proved:
                conclusion = "仅有转账凭证，被告能够证明转账系其他用途，借贷关系不成立。"
            else:
                conclusion = "仅有转账凭证，被告不能证明转账系其他用途，借贷关系成立。"
            return _format_loan_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.voucher_no_creditor:
            triggered.append(config.patch_name("L10", "债权凭证未载明债权人"))
            major = "民间借贷司法解释第2条规定，持有债权凭证的当事人可以提起民间借贷诉讼；被告对原告债权人资格提出有事实依据抗辩的，人民法院应审查。"
            minor = "识别到借据、收据或欠条未载明债权人。"
            if facts.other_purpose_proved:
                conclusion = "债权凭证未载明债权人，被告已提出并证明原告不具有债权人资格，原告债权人资格不成立。"
            else:
                conclusion = "债权凭证未载明债权人，持有人可初步证明债权人资格；被告不能提出充分反证的，原告债权人资格成立。"
            return _format_loan_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.deducted_interest:
            triggered.append(config.patch_name("L2", "砍头息认定"))
            major = "《民法典》第670条规定，借款的利息不得预先在本金中扣除；利息预先在本金中扣除的，应当按照实际借款数额返还借款并计算利息。"
            deducted = facts.nominal_principal - facts.actual_received if facts.nominal_principal > facts.actual_received > 0 else 0.0
            minor = f"识别到借条或合同载明本金为 {_money(facts.nominal_principal)}，借款人实际收到 {_money(facts.actual_received)}，存在预扣利息或费用争议。"
            conclusion = f"存在砍头息 {_money(deducted)}，本金应认定为实际借款数额 {_money(facts.actual_received)}，利息也应以该实际借款数额为基数计算。"
            return _format_loan_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.partial_repayment:
        triggered.append(config.patch_name("L4", "还款冲抵顺序"))
        major = "《民法典》第561条规定，债务人在履行主债务外还应支付利息和实现债权费用，其给付不足以清偿全部债务的，除另有约定外，按实现债权费用、利息、主债务顺序履行。"
        minor = f"识别到借款人部分还款 {_money(facts.repayment_amount)}，不足以清偿全部债务。"
        remaining = facts.principal_amount
        if facts.repayment_amount > 0:
            remaining_payment = facts.repayment_amount
            remaining_payment = max(0.0, remaining_payment - facts.cost_amount)
            remaining_payment = max(0.0, remaining_payment - facts.interest_amount)
            remaining = max(0.0, facts.principal_amount - remaining_payment) if facts.principal_amount > 0 else 0.0
        conclusion = f"部分还款 {_money(facts.repayment_amount)}，按费用、利息、本金顺序冲抵，尚欠本金 {_money(remaining)}。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "还款事实审查"], procedure_findings)

    if facts.spousal_debt:
        triggered.append(config.patch_name("L8", "夫妻共同债务认定"))
        major = "夫妻共同债务规则要求，夫妻一方以个人名义所负债务，属于家庭日常生活需要的为夫妻共同债务；超出日常生活需要的，债权人需证明用于共同生活、共同生产经营或基于夫妻共同意思表示。"
        minor = "识别到出借人主张借款由夫妻双方共同偿还。"
        if facts.daily_family_need or facts.joint_business_or_intent:
            conclusion = "本案借款属于夫妻共同债务，应由夫妻双方共同偿还。"
        elif facts.beyond_family_need:
            conclusion = "本案借款超出家庭日常生活需要，且未识别到共同生活、共同经营或共同意思表示，不属于夫妻共同债务，不应由夫妻双方共同偿还。"
        else:
            conclusion = "是否属于夫妻共同债务需查明借款用途、金额大小、配偶是否签字追认以及是否用于共同生活或共同经营。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "夫妻共同债务"], procedure_findings)

    if facts.misuse_loan:
        triggered.append(config.patch_name("L12", "未按约定用途使用借款"))
        major = "《民法典》第673条规定，借款人未按照约定的借款用途使用借款的，贷款人可以停止发放借款、提前收回借款或者解除合同。"
        minor = "识别到借款人未按约定用途使用借款。"
        conclusion = "借款人未按约定用途使用借款，贷款人可以停止发放借款、提前收回借款或解除合同。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "借款用途审查"], procedure_findings)

    path.append("利息计算")
    if facts.no_interest_agreed:
        major = "《民法典》第680条规定，借款合同对支付利息没有约定的，视为没有利息；自然人之间借款利息约定不明确的，视为没有利息。"
        minor = "识别到双方没有约定利息。"
        conclusion = "出借人主张借期内利息的，不予支持；逾期后的资金占用损失可依法另行审查。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.interest_agreed or facts.annual_rate > 0:
        triggered.append(config.patch_name("L3", "利率上限审查"))
        cap = _effective_interest_cap(facts)
        rate = facts.annual_rate
        major = "民间借贷司法解释第26条、第29条规定，约定利率不得超过合同成立时一年期LPR四倍；逾期利息、违约金和其他费用一并主张的，总计也不得超过该上限。"
        if cap > 0:
            supported_rate = min(rate, cap) if rate > 0 else cap
            comparison = "超过" if rate > cap else "未超过"
            minor = f"识别到合同约定年利率为 {rate:.2f}%，一年期LPR为 {facts.lpr_rate:.2f}%，四倍为 {cap:.2f}%。"
            conclusion = f"合同成立时一年期LPR为 {facts.lpr_rate:.2f}%，四倍为 {cap:.2f}%。约定利率 {rate:.2f}% {comparison}上限，应按 {supported_rate:.2f}% 计算。"
        else:
            minor = f"识别到合同约定年利率为 {rate:.2f}%，但未识别到合同成立时一年期LPR。"
            conclusion = "应以合同成立时一年期LPR四倍为司法保护上限；超过上限的利息、逾期利息、违约金和其他费用部分不予支持。"
        if facts.compound_interest and not facts.compound_agreed:
            conclusion += " 合同未明确约定复利的，对利息再计息不予支持。"
        if facts.overdue_interest and facts.no_overdue_rate and rate > 0:
            conclusion += " 未约定逾期利率但约定借期内利率的，逾期资金占用期间可按借期内利率计算，但仍受上限限制。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, [*path, "利率上限审查"], procedure_findings)

    if facts.early_repayment:
        major = "《民法典》第677条规定，借款人提前返还借款的，除当事人另有约定外，应当按照实际借款期间计算利息。民间借贷司法解释第30条亦支持提前偿还并按实际期间计算利息。"
        minor = "识别到借款人提前偿还借款。"
        if facts.early_repayment_forbidden:
            conclusion = "合同明确约定提前还款构成违约或需支付费用的，可按约处理；但违约金、费用及利息总额仍不得超过法定利率上限。"
        else:
            conclusion = "提前还款不构成违约，除另有约定外，应按实际借款期间计算利息。"
        return _format_loan_output(major, minor, conclusion, [], facts, [*path, "提前还款"], procedure_findings)

    if facts.extension_request:
        major = "《民法典》第678条规定，借款人可以在还款期限届满前向贷款人申请展期；贷款人同意的，可以展期。"
        minor = "识别到借款人申请借款展期。"
        if facts.extension_before_due and facts.lender_agreed_extension:
            conclusion = "借款展期成立，应按展期协议履行；展期利率有约定按约定，无约定参照原合同利率，但不得超过法定上限。"
        else:
            conclusion = "展期需在还款期限届满前申请并经贷款人同意；贷款人不同意的，借款人仍应按原还款期限履行。"
        return _format_loan_output(major, minor, conclusion, [], facts, [*path, "借款展期"], procedure_findings)

    if facts.guarantee_contract:
        path.append("保证责任")
        if facts.loan_old_for_new:
            triggered.append(config.patch_name("L6", "借新还旧中保证人责任"))
            major = "借新还旧中，除保证人知道或者应当知道借新还旧外，保证人原则上不承担保证责任；新贷与旧贷系同一保证人的，保证人应承担保证责任。"
            minor = "识别到新贷款用于偿还旧贷款，并涉及保证人责任。"
            if facts.same_guarantor or facts.guarantor_knows:
                conclusion = "借新还旧，保证人知道或新贷与旧贷为同一保证人，保证人应承担保证责任。"
            else:
                conclusion = "借新还旧，新贷与旧贷不同一保证人且保证人不知道也不应当知道的，保证人不应承担保证责任。"
            return _format_loan_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        major = "《民法典》第681条至第687条规定，保证合同有效且保证期间未过的，保证人按约定保证方式承担责任；未约定或约定不明的，按一般保证承担责任。"
        minor = "识别到存在保证合同或保证人。"
        if facts.guarantee_period_expired:
            conclusion = "保证期间已经届满，债权人未依法主张保证责任的，保证人不再承担保证责任。"
        elif facts.joint_guarantee:
            conclusion = "保证方式明确为连带责任保证，债权人可要求保证人在保证范围内承担连带责任。"
        else:
            conclusion = "保证方式为一般保证，或未约定、约定不明而依法按一般保证处理；保证人享有先诉抗辩权。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.loan_contract:
        major = "《民法典》第667条规定，借款合同的核心是贷款人提供借款，借款人到期返还借款并支付依法成立的利息。裁判应依次审查本金、利率、还款、逾期责任和保证责任。"
        minor = "已识别借款合同关系，但未稳定识别足以输出最终结论的本金、利率、还款、效力、提前还款、展期或保证事实。"
        conclusion = "事实要素不足，需补充实际放款金额、约定利率、LPR、还款情况、是否逾期、是否存在担保或合同无效事实后再裁判。"
        return _format_loan_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "借款合同纠纷应围绕货币所有权转移、到期返还同种类货币、利息计算、还款事实和担保责任进行审查。"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的借款合同关键事实。"
    conclusion = "事实要素不足，需补充是否存在借款关系、实际放款、本金金额、利率、还款期限、还款情况和保证事实后再裁判。"
    return _format_loan_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
