"""Sale-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import (
    _extract_money_near,
    _format_output,
    _mentions,
    _parse_date,
    _years_between,
)
from adjudicate.sale_configs import get_sale_config


@dataclass
class SaleFacts:
    raw_text: str
    contract_type: str = "sale"
    contract_type_name: str = "买卖合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    sale_contract: bool = False
    written_contract: bool = False
    no_written_contract: bool = False
    delivery_note: bool = False
    invoice_only: bool = False
    vat_invoice: bool = False
    ordinary_invoice: bool = False
    contract_invalid: bool = False
    no_disposition_right: bool = False
    delivery_date: Optional[date] = None
    third_party_tort: bool = False
    installment_sale: bool = False
    total_price: float = 0.0
    unpaid_price: float = 0.0
    seller_urged: bool = False
    reasonable_period_unpaid: bool = False
    trial_sale: bool = False
    trial_period_expired: bool = False
    buyer_accepts_purchase: bool = False
    buyer_refuses_purchase: bool = False
    trial_damage: bool = False
    title_retention: bool = False
    registered: bool = False
    not_registered: bool = False
    seller_retake: bool = False
    redemption: bool = False
    sample_sale: bool = False
    sample_conform: bool = False
    sample_nonconform: bool = False
    tender_auction: bool = False
    delivered: bool = False
    not_delivered: bool = False
    delivery_to_carrier: bool = False
    electronic_product: bool = False
    electronic_received: bool = False
    over_delivery: bool = False
    buyer_accepts_extra: bool = False
    buyer_rejects_extra: bool = False
    custody_extra_fee: float = 0.0
    unpaid_payment: bool = False
    suspend_payment_right: bool = False
    seller_security: bool = False
    risk_loss: bool = False
    before_delivery: bool = False
    after_delivery: bool = False
    buyer_delay_caused_non_delivery: bool = False
    in_transit_sale: bool = False
    buyer_refuses_collect: bool = False
    quality_nonconform: bool = False
    quality_conform: bool = False
    quality_standard: bool = False
    inspection_period_agreed: bool = False
    timely_notice: bool = False
    late_notice: bool = False
    signed_document: bool = False
    hidden_defect: bool = False
    short_inspection_period: bool = False
    seller_knew_defect: bool = False
    minor_defect: bool = False
    general_defect: bool = False
    serious_defect: bool = False
    repair_requested: bool = False
    replace_requested: bool = False
    return_requested: bool = False
    reduce_price_requested: bool = False
    compensation_requested: bool = False
    actual_loss: float = 0.0
    expected_profit: float = 0.0
    foreseeable_amount: float = 0.0
    deposit_penalty: bool = False
    liquidated_damage: bool = False
    third_party_right: bool = False
    buyer_knew_right: bool = False
    buyer_not_knew_right: bool = False
    multi_sale: bool = False
    first_delivery: bool = False
    first_payment: bool = False
    first_contract: bool = False
    exemption_clause: bool = False
    seller_intent_gross_no_notice: bool = False
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "sale_contract": self.sale_contract,
            "written_contract": self.written_contract,
            "no_written_contract": self.no_written_contract,
            "delivery_note": self.delivery_note,
            "invoice_only": self.invoice_only,
            "vat_invoice": self.vat_invoice,
            "ordinary_invoice": self.ordinary_invoice,
            "contract_invalid": self.contract_invalid,
            "no_disposition_right": self.no_disposition_right,
            "delivery_date": self.delivery_date.isoformat() if self.delivery_date else None,
            "third_party_tort": self.third_party_tort,
            "installment_sale": self.installment_sale,
            "total_price": self.total_price,
            "unpaid_price": self.unpaid_price,
            "seller_urged": self.seller_urged,
            "reasonable_period_unpaid": self.reasonable_period_unpaid,
            "trial_sale": self.trial_sale,
            "trial_period_expired": self.trial_period_expired,
            "buyer_accepts_purchase": self.buyer_accepts_purchase,
            "buyer_refuses_purchase": self.buyer_refuses_purchase,
            "trial_damage": self.trial_damage,
            "title_retention": self.title_retention,
            "registered": self.registered,
            "not_registered": self.not_registered,
            "seller_retake": self.seller_retake,
            "redemption": self.redemption,
            "sample_sale": self.sample_sale,
            "sample_conform": self.sample_conform,
            "sample_nonconform": self.sample_nonconform,
            "tender_auction": self.tender_auction,
            "delivered": self.delivered,
            "not_delivered": self.not_delivered,
            "delivery_to_carrier": self.delivery_to_carrier,
            "electronic_product": self.electronic_product,
            "electronic_received": self.electronic_received,
            "over_delivery": self.over_delivery,
            "buyer_accepts_extra": self.buyer_accepts_extra,
            "buyer_rejects_extra": self.buyer_rejects_extra,
            "custody_extra_fee": self.custody_extra_fee,
            "unpaid_payment": self.unpaid_payment,
            "suspend_payment_right": self.suspend_payment_right,
            "seller_security": self.seller_security,
            "risk_loss": self.risk_loss,
            "before_delivery": self.before_delivery,
            "after_delivery": self.after_delivery,
            "buyer_delay_caused_non_delivery": self.buyer_delay_caused_non_delivery,
            "in_transit_sale": self.in_transit_sale,
            "buyer_refuses_collect": self.buyer_refuses_collect,
            "quality_nonconform": self.quality_nonconform,
            "quality_conform": self.quality_conform,
            "quality_standard": self.quality_standard,
            "inspection_period_agreed": self.inspection_period_agreed,
            "timely_notice": self.timely_notice,
            "late_notice": self.late_notice,
            "signed_document": self.signed_document,
            "hidden_defect": self.hidden_defect,
            "short_inspection_period": self.short_inspection_period,
            "seller_knew_defect": self.seller_knew_defect,
            "minor_defect": self.minor_defect,
            "general_defect": self.general_defect,
            "serious_defect": self.serious_defect,
            "repair_requested": self.repair_requested,
            "replace_requested": self.replace_requested,
            "return_requested": self.return_requested,
            "reduce_price_requested": self.reduce_price_requested,
            "compensation_requested": self.compensation_requested,
            "actual_loss": self.actual_loss,
            "expected_profit": self.expected_profit,
            "foreseeable_amount": self.foreseeable_amount,
            "deposit_penalty": self.deposit_penalty,
            "liquidated_damage": self.liquidated_damage,
            "third_party_right": self.third_party_right,
            "buyer_knew_right": self.buyer_knew_right,
            "buyer_not_knew_right": self.buyer_not_knew_right,
            "multi_sale": self.multi_sale,
            "first_delivery": self.first_delivery,
            "first_payment": self.first_payment,
            "first_contract": self.first_contract,
            "exemption_clause": self.exemption_clause,
            "seller_intent_gross_no_notice": self.seller_intent_gross_no_notice,
            "notes": self.notes,
        }


def _format_sale_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: SaleFacts,
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


def extract_sale_facts(case_text: str) -> SaleFacts:
    config = get_sale_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = SaleFacts(raw_text=raw_text)

    for field_name in (
        "sale_contract", "written_contract", "no_written_contract", "delivery_note", "invoice_only",
        "vat_invoice", "ordinary_invoice", "contract_invalid", "no_disposition_right", "third_party_tort",
        "installment_sale", "seller_urged", "reasonable_period_unpaid", "trial_sale",
        "trial_period_expired", "buyer_accepts_purchase", "buyer_refuses_purchase", "trial_damage",
        "title_retention", "registered", "not_registered", "seller_retake", "redemption",
        "sample_sale", "sample_conform", "sample_nonconform", "tender_auction", "delivered",
        "not_delivered", "delivery_to_carrier", "electronic_product", "electronic_received",
        "over_delivery", "buyer_accepts_extra", "buyer_rejects_extra", "unpaid_payment",
        "suspend_payment_right", "seller_security", "risk_loss", "before_delivery", "after_delivery",
        "buyer_delay_caused_non_delivery", "in_transit_sale", "buyer_refuses_collect",
        "quality_nonconform", "quality_conform", "quality_standard", "inspection_period_agreed",
        "timely_notice", "late_notice", "signed_document", "hidden_defect", "short_inspection_period",
        "seller_knew_defect", "minor_defect", "general_defect", "serious_defect", "repair_requested",
        "replace_requested", "return_requested", "reduce_price_requested", "compensation_requested",
        "deposit_penalty", "liquidated_damage", "third_party_right", "buyer_knew_right",
        "buyer_not_knew_right", "multi_sale", "first_delivery", "first_payment", "first_contract",
        "exemption_clause", "seller_intent_gross_no_notice",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.delivery_date = _parse_date(text, config.get_terms("delivery_date"))
    facts.total_price = _extract_money_near(text, config.get_terms("total_price"))
    facts.unpaid_price = _extract_money_near(text, config.get_terms("unpaid_price"))
    facts.custody_extra_fee = _extract_money_near(text, config.get_terms("custody_extra_fee"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))
    facts.expected_profit = _extract_money_near(text, config.get_terms("expected_profit"))
    facts.foreseeable_amount = _extract_money_near(text, config.get_terms("foreseeable_amount"))

    if facts.quality_nonconform and not (facts.minor_defect or facts.general_defect or facts.serious_defect):
        facts.general_defect = True
    if facts.risk_loss and not facts.before_delivery:
        facts.after_delivery = facts.after_delivery or facts.delivered
    if facts.trial_damage:
        facts.trial_sale = True
        facts.risk_loss = True
    if facts.title_retention and (facts.seller_retake or facts.unpaid_payment):
        facts.sale_contract = True
    if facts.installment_sale:
        facts.sale_contract = True
    return facts


def _procedure_findings(facts: SaleFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("买卖合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告通常为出卖人或买受人；应结合请求内容确定是向卖方主张交付、质量责任，还是向买方主张付款责任")
    return findings


def _only_procedure_question(facts: SaleFacts) -> bool:
    return (
        (facts.asks_jurisdiction or facts.asks_defendant)
        and not facts.contract_invalid
        and not facts.no_written_contract
        and not facts.invoice_only
        and not facts.installment_sale
        and not facts.trial_sale
        and not facts.title_retention
        and not facts.sample_sale
        and not facts.tender_auction
        and not facts.not_delivered
        and not facts.unpaid_payment
        and not facts.risk_loss
        and not facts.quality_nonconform
        and not facts.third_party_right
        and not facts.multi_sale
    )


def _has_sale_dispute(facts: SaleFacts) -> bool:
    return any(
        (
            facts.sale_contract, facts.no_written_contract, facts.invoice_only, facts.installment_sale,
            facts.trial_sale, facts.title_retention, facts.sample_sale, facts.not_delivered,
            facts.unpaid_payment, facts.risk_loss, facts.quality_nonconform, facts.third_party_right,
            facts.multi_sale,
        )
    )


def _money(value: float) -> str:
    return f"{value:.2f} 元" if value > 0 else "待核定"


def _installment_ratio(facts: SaleFacts) -> float:
    if facts.total_price <= 0 or facts.unpaid_price <= 0:
        return 0.0
    return facts.unpaid_price / facts.total_price


def _quality_remedy(facts: SaleFacts, triggered: List[str]) -> tuple[str, List[str]]:
    config = get_sale_config()
    remedies: List[str] = []
    if facts.repair_requested or facts.minor_defect:
        remedies.append("修理")
    if facts.replace_requested:
        remedies.append("更换")
    if facts.reduce_price_requested:
        remedies.append("减少价款")
    if facts.compensation_requested:
        remedies.append("赔偿损失")
    if facts.return_requested or facts.serious_defect:
        remedies.append("退货或解除合同")
    if not remedies:
        remedies = ["修理", "更换", "减少价款", "赔偿损失"]

    conclusion = f"买受人可以合理选择{'、'.join(dict.fromkeys(remedies))}；修理、更换费用由出卖人承担。"
    if facts.expected_profit > 0:
        triggered = [*triggered, config.patch_name("B6", "可得利益损失")]
        total = facts.actual_loss + facts.expected_profit
        if facts.foreseeable_amount > 0 and total > facts.foreseeable_amount:
            conclusion += f" 可得利益损失成立，但赔偿总额不得超过订约时可预见范围 {_money(facts.foreseeable_amount)}。"
        else:
            conclusion += f" 可得利益损失成立，赔偿金额为实际损失与可得利益合计 {_money(total)}。"
    elif facts.actual_loss > 0:
        conclusion += f" 已识别实际损失为 {_money(facts.actual_loss)}。"

    if facts.deposit_penalty and facts.liquidated_damage:
        triggered = [*triggered, config.patch_name("B8", "定金与违约金、赔偿损失的关系")]
        conclusion += " 定金与违约金不可以并用，守约方应择一主张；定金不足以弥补实际损失的，可以请求赔偿超过定金数额的损失。"
    return conclusion, triggered


def adjudicate_sale(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_sale_config()
    facts = extract_sale_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "买卖合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出合同成立、交付、付款、风险、质量、权利瑕疵或所有权转移争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_sale_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.third_party_tort and not _has_sale_dispute(facts):
        major = "买卖合同裁判引擎处理出卖人与买受人之间的交付、付款、所有权转移、风险负担和瑕疵担保争议；单纯第三人侵权应按侵权责任处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到买卖合同履行争议。"
        conclusion = "本案涉及侵权责任，非买卖合同纠纷，不适用本买卖合同裁判引擎。"
        return _format_sale_output(major, minor, conclusion, [], facts, path, procedure_findings)

    if facts.delivery_date and _years_between(facts.delivery_date, today) > 3:
        major = "买卖合同纠纷适用三年一般诉讼时效。"
        minor = f"识别到相关交付、付款或应履行日期为{facts.delivery_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求。"
        return _format_sale_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    path.append("前置实体判断")
    if facts.invoice_only:
        triggered.append(config.patch_name("B13", "发票的证明效力"))
        major = "买卖合同司法解释第5条规定，出卖人仅以增值税专用发票及税款抵扣资料证明已交付，买受人不认可的，出卖人还应提供其他证据；合同约定或交易习惯以普通发票作为付款凭证的，买受人以普通发票证明已付款的，可以支持。"
        if facts.vat_invoice:
            minor = "识别到出卖人仅以增值税专用发票或抵扣资料证明交付事实，买受人不认可。"
            conclusion = "发票不足以单独证明交付事实；出卖人应补充送货单、签收单、物流记录、对账单等其他证据。"
        elif facts.ordinary_invoice:
            minor = "识别到买受人以普通发票证明付款，且存在以发票作为付款凭证的约定或交易习惯。"
            conclusion = "发票可以证明付款事实；但若对方提出相反证据，仍应结合交易习惯和收付款记录综合判断。"
        else:
            minor = "识别到当事人仅以发票证明交付或付款事实。"
            conclusion = "发票证明力需区分交付还是付款；仅凭发票通常不足以证明交付，但可结合约定和交易习惯证明付款。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同成立认定"], procedure_findings)

    if facts.no_written_contract:
        major = "买卖合同司法解释第1条规定，没有书面合同，当事人以送货单、收货单、结算单、发票等主张存在买卖合同关系的，应结合交易方式、交易习惯等综合认定。"
        minor = "识别到双方未签书面买卖合同。"
        if facts.delivery_note:
            conclusion = "虽无书面合同，但存在送货单、收货单、结算单、发票或交易习惯等证据，可以综合认定买卖合同关系成立。"
        else:
            conclusion = "仅凭现有事实不足以认定买卖合同关系成立，需补充送货、收货、结算、发票、付款或交易习惯证据。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同成立认定"], procedure_findings)

    if facts.contract_invalid:
        major = "《民法典》第595条规定，买卖合同以出卖人转移标的物所有权、买受人支付价款为核心；合同无效的，按无效合同后果处理。"
        minor = "识别到买卖合同无效或合同不成立事实。"
        conclusion = "买卖合同无效，已取得的标的物或价款应依法返还；因此造成损失的，按过错承担赔偿责任。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.no_disposition_right:
        major = "出卖人未取得处分权导致标的物所有权不能转移的，买受人可以解除合同并请求出卖人承担违约责任。"
        minor = "识别到出卖人无处分权或标的物所有权不能转移。"
        conclusion = "买受人可以解除合同，并请求出卖人承担返还价款、赔偿损失等违约责任。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.exemption_clause:
        triggered.append(config.patch_name("B7", "免责条款效力审查"))
        major = "《民法典》第618条规定，当事人约定减轻或者免除出卖人对标的物瑕疵承担责任的，因出卖人故意或者重大过失不告知买受人标的物瑕疵的，出卖人无权主张减轻或者免除责任。"
        if facts.seller_intent_gross_no_notice:
            minor = "识别到合同存在减轻或免除出卖人瑕疵担保责任的条款，且出卖人故意或重大过失不告知瑕疵。"
            conclusion = "免责条款无效，出卖人仍应承担瑕疵担保责任。"
        else:
            minor = "识别到合同存在减轻或免除出卖人瑕疵担保责任的条款，但未识别到出卖人故意或重大过失不告知瑕疵。"
            conclusion = "免责条款原则上可以作为责任范围约定，但仍需审查格式条款提示说明、公平性和出卖人是否知情隐瞒。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.installment_sale:
        triggered.append(config.patch_name("B1", "分期付款买卖"))
        major = "《民法典》第634条规定，分期付款买卖中，买受人未支付到期价款的数额达到全部价款五分之一，经催告后在合理期限内仍未支付的，出卖人可以请求买受人支付全部价款或者解除合同。"
        ratio = _installment_ratio(facts)
        minor = f"识别到买受人分期付款；未付价款为{_money(facts.unpaid_price)}，总价款为{_money(facts.total_price)}。"
        if ratio >= 0.2 and facts.seller_urged and facts.reasonable_period_unpaid:
            conclusion = f"分期付款买卖，未付价款达总价款的 {ratio:.0%}，经催告后仍未在合理期限内支付，出卖人可以请求支付全部价款或解除合同；解除时可请求支付标的物使用费。"
        else:
            conclusion = "分期付款买卖，尚需满足未付价款达到总价款五分之一、出卖人已催告、催告后合理期限内仍未支付三个条件，出卖人才可以请求全部价款或解除合同。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.trial_sale:
        triggered.append(config.patch_name("B2", "试用买卖"))
        major = "《民法典》第637条至第640条规定，试用买卖中买受人在试用期内可以购买或拒绝购买；试用期限届满未作表示或实施支付部分价款、出卖、出租、设立担保等行为的，视为同意购买；试用期内标的物毁损灭失风险由出卖人承担。"
        if facts.trial_damage:
            triggered.append(config.patch_name("B14", "试用买卖中标的物风险负担"))
            minor = "识别到标的物在试用期内毁损或灭失。"
            conclusion = "试用期内标的物毁损灭失，风险由出卖人承担，买受人不因该风险负担付款义务。"
        elif facts.buyer_refuses_purchase and not facts.trial_period_expired:
            minor = "识别到买受人在试用期限内明确拒绝购买。"
            conclusion = "试用买卖，试用期限未届满，买受人未表示购买且明确拒绝购买，买卖合同不成立。"
        elif facts.trial_period_expired or facts.buyer_accepts_purchase:
            minor = "识别到试用期限届满未作拒绝表示，或买受人已明示、默示同意购买。"
            conclusion = "试用买卖，试用期限已届满或买受人已表示购买，视为同意购买，买卖合同成立。"
        else:
            minor = "识别到试用买卖，但试用期限是否届满和买受人是否表示购买尚不明确。"
            conclusion = "试用买卖需查明试用期限和买受人意思表示；试用期内买受人可以购买或拒绝购买。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.title_retention:
        triggered.append(config.patch_name("B3", "所有权保留买卖"))
        major = "《民法典》第641条至第643条规定，买卖合同可以约定所有权保留；未经登记不得对抗善意第三人。买受人未按约定支付价款经催告后仍未支付等情形下，出卖人有权取回标的物，买受人可依法回赎。"
        minor = "识别到合同约定买受人未履行支付价款或其他义务时，标的物所有权属于出卖人。"
        if facts.seller_retake and facts.seller_urged and facts.reasonable_period_unpaid:
            registration = "已登记" if facts.registered else "未登记"
            conclusion = f"所有权保留{registration}，买受人已触发取回权情形，出卖人有权取回标的物；但未登记的，不得对抗善意第三人，取回后应依法给予买受人回赎机会。"
        else:
            conclusion = "所有权保留买卖中，出卖人是否有权取回需审查买受人是否违约、出卖人是否催告、是否给予合理期限以及所有权保留是否登记。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.sample_sale:
        triggered.append(config.patch_name("B4", "凭样品买卖"))
        major = "凭样品买卖中，出卖人交付的标的物应当与样品及其说明的质量相同；不一致的，按质量瑕疵承担违约责任。"
        if facts.sample_nonconform:
            minor = "识别到买卖双方凭样品确定质量，交付标的物与样品不一致。"
            conclusion = "凭样品买卖，交付标的物不符合样品质量，出卖人应承担相应违约责任。"
        elif facts.sample_conform:
            minor = "识别到交付标的物与样品质量一致。"
            conclusion = "凭样品买卖，交付标的物符合样品质量，买受人不能仅以样品质量不符为由拒付价款。"
        else:
            minor = "识别到凭样品买卖，但交付标的物是否符合样品质量尚不明确。"
            conclusion = "应先比对封存样品、样品说明与实际交付标的物，再判断出卖人是否承担质量违约责任。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.tender_auction:
        triggered.append(config.patch_name("B15", "招标投标买卖与拍卖"))
        major = "《民法典》第644条、第645条规定，招标投标买卖和拍卖的当事人权利义务及程序依照有关法律、行政法规规定。"
        minor = "识别到买卖合同通过招标投标、拍卖或竞拍方式订立。"
        conclusion = "招标投标买卖/拍卖，优先适用招标投标法、拍卖法等特别法规定；特别法未规定的，适用民法典买卖合同一般规则。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.electronic_product:
        triggered.append(config.patch_name("B11", "电子信息产品的交付"))
        major = "买卖合同司法解释第2条规定，电子信息产品交付方式约定不明确且无法确定的，买受人收到约定的电子信息产品或者权利凭证即为交付。"
        minor = "识别到标的物为无需有形载体交付的电子信息产品。"
        if facts.electronic_received:
            conclusion = "电子信息产品，交付方式约定不明，自买受人收到电子信息产品或权利凭证时完成交付。"
        else:
            conclusion = "电子信息产品是否交付，应以买受人是否收到电子信息产品或权利凭证为判断核心。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "标的物交付审查"], procedure_findings)

    if facts.over_delivery:
        triggered.append(config.patch_name("B12", "多交标的物的处理"))
        major = "买卖合同司法解释第3条规定，出卖人多交标的物的，买受人可以接收或者拒绝接收多交部分；拒绝接收而代为保管的，合理费用由出卖人承担。"
        if facts.buyer_rejects_extra:
            minor = "识别到出卖人多交标的物，买受人拒绝接收多交部分并代为保管。"
            conclusion = f"多交标的物，买受人拒绝接收多交部分的，可以代为保管，合理保管费用由出卖人承担；已识别费用为 {_money(facts.custody_extra_fee)}。"
        elif facts.buyer_accepts_extra:
            minor = "识别到出卖人多交标的物，买受人接收多交部分。"
            conclusion = "多交标的物，买受人接收多交部分的，应按合同约定或交易习惯支付相应价款。"
        else:
            minor = "识别到出卖人多交标的物，但买受人是否接收尚不明确。"
            conclusion = "多交标的物，买受人可以接收或拒绝接收；拒绝接收并代为保管的，合理费用由出卖人承担。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "标的物交付审查"], procedure_findings)

    if facts.not_delivered:
        major = "《民法典》第598条规定，出卖人应当向买受人交付标的物或者交付提取标的物的单证，并转移标的物所有权。未按期交付的，应承担违约责任。"
        minor = "识别到出卖人未按约定时间或地点交付标的物。"
        conclusion = "出卖人构成迟延交付，买受人可以请求继续交付、赔偿损失；迟延导致合同目的不能实现的，买受人可以解除合同。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "标的物交付审查"], procedure_findings)

    if facts.unpaid_payment:
        major = "买受人应当按照约定支付价款；迟延付款构成违约。存在确切证据证明第三人对标的物享有权利的，买受人可以中止支付相应价款，但出卖人提供适当担保的除外。"
        if facts.suspend_payment_right and not facts.seller_security:
            minor = "识别到买受人未支付价款，但有确切证据证明第三人对标的物享有权利，且出卖人未提供适当担保。"
            conclusion = "买受人可以中止支付相应价款，直至出卖人消除权利瑕疵或提供适当担保。"
        else:
            minor = "识别到买受人拖欠、迟延或未按约定支付货款。"
            conclusion = f"买受人构成迟延付款，应支付货款 {_money(facts.unpaid_price)} 并承担逾期付款违约责任。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "价款支付审查"], procedure_findings)

    path.append("风险负担")
    if facts.risk_loss:
        major = "《民法典》第604条至第611条规定，标的物毁损、灭失风险一般在交付前由出卖人承担，交付后由买受人承担；但风险转移不影响买受人因质量不符合约定请求出卖人承担违约责任。"
        if facts.buyer_delay_caused_non_delivery or facts.buyer_refuses_collect:
            minor = "识别到因买受人原因导致未按期交付，或买受人违反约定未收取标的物。"
            conclusion = "买受人自违反约定时起承担标的物毁损、灭失风险。"
        elif facts.in_transit_sale:
            minor = "识别到出卖人出卖交由承运人运输的在途标的物。"
            conclusion = "路货买卖中，除另有约定外，标的物毁损、灭失风险自合同成立时起由买受人承担。"
        elif facts.delivery_to_carrier:
            minor = "识别到出卖人已按约定将标的物交付给承运人运输。"
            conclusion = "货交承运人后，标的物毁损、灭失风险由买受人承担；但质量瑕疵责任不因此免除。"
        elif facts.quality_nonconform and facts.serious_defect and facts.return_requested:
            minor = "识别到标的物质量不符合要求，导致合同目的不能实现，买受人拒绝接受或解除合同。"
            conclusion = "因质量不符导致合同目的不能实现，买受人拒绝接受或解除合同的，标的物毁损、灭失风险由出卖人承担。"
        elif facts.before_delivery:
            minor = "识别到标的物在交付前毁损、灭失。"
            conclusion = "标的物交付前毁损、灭失的风险由出卖人承担。"
        elif facts.after_delivery:
            minor = "识别到标的物在交付后毁损、灭失。"
            conclusion = "标的物交付后毁损、灭失的风险由买受人承担；但若同时存在质量瑕疵，买受人仍可请求出卖人承担违约责任。"
        else:
            minor = "识别到标的物毁损、灭失争议，但交付状态和法定例外情形尚不明确。"
            conclusion = "风险负担需先查明毁损灭失发生时间、交付是否完成、是否货交承运人、是否路货买卖以及买受人是否迟延受领。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("质量瑕疵")
    if facts.quality_conform:
        major = "《民法典》第615条规定，出卖人应当按照约定的质量要求交付标的物。标的物符合质量要求的，买受人应按约支付价款。"
        minor = "识别到交付标的物质量符合约定或验收合格。"
        conclusion = "买受人应全额支付价款，不能以质量瑕疵为由拒付或减少价款。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.quality_nonconform:
        major = "《民法典》第615条、第617条、第621条规定，出卖人应按约定质量交付标的物；质量不符合约定的，买受人可以请求承担违约责任，但应在约定或合理检验期限内通知出卖人。"
        if facts.signed_document and not facts.hidden_defect:
            triggered.append(config.patch_name("B10", "买受人检验期限的推定"))
            minor = "识别到买受人签收了载明数量、型号、规格的送货单或确认单，且争议属于数量或外观瑕疵。"
            conclusion = "买受人已签收载明数量/型号/规格的单据，推定已完成数量和外观瑕疵检验；买受人可提供相反证据推翻，该推定不适用于隐蔽瑕疵。"
            return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "异议期限"], procedure_findings)
        if facts.late_notice and not facts.seller_knew_defect:
            minor = "识别到买受人未在约定检验期限、合理期限或质量保证期内通知质量不符合约定，且未识别到出卖人知道或应当知道瑕疵。"
            conclusion = "买受人怠于通知的，视为标的物质量符合约定，质量瑕疵抗辩或索赔不予支持。"
            return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "异议期限"], procedure_findings)
        if facts.short_inspection_period:
            triggered.append(config.patch_name("B10", "买受人检验期限的推定"))
            minor = "识别到约定检验期限过短，依标的物性质和交易习惯难以完成全面检验。"
            conclusion = "过短检验期限仅视为买受人对外观瑕疵提出异议的期限，不限制买受人就隐蔽瑕疵在合理期限内主张权利。"
            return _format_sale_output(major, minor, triggered and conclusion, triggered, facts, [*path, "异议期限"], procedure_findings)
        if facts.serious_defect:
            triggered.append(config.patch_name("B9", "合同目的不能实现的认定标准"))
            minor = "识别到标的物质量瑕疵严重，导致无法正常使用、使用价值严重减损或合同主要目的落空。"
            conclusion = "合同目的已落空，买受人可以拒绝接受标的物或解除合同，并请求返还价款、赔偿损失。"
            return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "瑕疵严重程度"], procedure_findings)
        minor = "识别到标的物不符合质量要求，买受人已主张相应救济或现有事实未显示异议逾期。"
        conclusion, triggered = _quality_remedy(facts, triggered)
        return _format_sale_output(major, minor, conclusion, triggered, facts, [*path, "救济方式执行"], procedure_findings)

    path.append("权利瑕疵")
    if facts.third_party_right:
        major = "《民法典》第612条至第614条规定，出卖人就交付的标的物负有保证第三人不享有任何权利的义务；买受人知道或应当知道第三人权利的除外。买受人有确切证据证明第三人享有权利的，可以中止支付相应价款。"
        if facts.buyer_knew_right:
            minor = "识别到买受人在订立合同时知道或应当知道第三人对标的物享有权利。"
            conclusion = "买受人知道或应当知道权利瑕疵的，出卖人不承担权利瑕疵担保责任。"
        elif facts.seller_security:
            minor = "识别到第三人对标的物享有权利，但出卖人已提供适当担保。"
            conclusion = "出卖人提供适当担保的，买受人应继续支付相应价款；权利瑕疵造成损失的，可另行按违约责任处理。"
        else:
            minor = "识别到第三人对标的物享有抵押、租赁、查封等权利，买受人订约时不知情。"
            conclusion = "买受人可以中止支付相应价款；第三人权利导致买受人无法取得所有权的，买受人可以解除合同并请求赔偿。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("一物数卖")
    if facts.multi_sale:
        triggered.append(config.patch_name("B5", "一物数卖"))
        major = "买卖合同司法解释第6条规定，一物数卖时，先行受领交付的买受人优先；均未受领交付的，先行支付价款的买受人优先；均未受领交付也未支付价款的，合同成立在先的买受人优先。"
        if facts.first_delivery:
            minor = "识别到多个买受人中已有买受人先行受领交付。"
            conclusion = "一物数卖，按先行受领交付规则，应向先受领交付的买受人履行交付或确认履行效果；其他买受人可向出卖人主张违约责任。"
        elif facts.first_payment:
            minor = "识别到多个买受人均未受领交付，但其中一方先行支付价款。"
            conclusion = "一物数卖，按先行支付价款规则，应向先付款买受人履行交付义务；其他买受人可向出卖人主张违约责任。"
        elif facts.first_contract:
            minor = "识别到多个买受人均未受领交付也未支付价款，但其中一份合同成立在先。"
            conclusion = "一物数卖，按合同成立在先规则，应向合同成立在先的买受人履行交付义务；其他买受人可向出卖人主张违约责任。"
        else:
            minor = "识别到出卖人就同一标的物订立多重买卖合同，但交付、付款和合同成立先后尚不明确。"
            conclusion = "一物数卖应依次查明谁先受领交付、谁先支付价款、哪份合同成立在先，再确定履行对象。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.sale_contract:
        major = "《民法典》第595条、第598条规定，买卖合同的核心是出卖人转移标的物所有权并交付符合质量要求的标的物，买受人支付价款。"
        minor = "已识别买卖合同关系，但未稳定识别交付、付款、风险负担、质量瑕疵、权利瑕疵或所有权转移争议事实。"
        conclusion = "事实要素不足，需补充标的物是否交付、是否毁损灭失、质量是否符合约定、价款是否支付、是否存在第三人权利后再裁判。"
        return _format_sale_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "买卖合同纠纷应围绕标的物是否交付、所有权是否转移、风险谁承担、质量是否符合要求以及买受人如何救济进行审查。"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的买卖合同关键事实。"
    conclusion = "事实要素不足，需补充买卖合同关系、标的物交付、价款支付、质量瑕疵、风险损失或权利瑕疵事实后再裁判。"
    return _format_sale_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
