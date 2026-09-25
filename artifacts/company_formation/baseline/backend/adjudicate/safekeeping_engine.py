"""Safekeeping-contract adjudication engine."""

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
from adjudicate.safekeeping_configs import get_safekeeping_config


@dataclass
class SafekeepingFacts:
    raw_text: str
    contract_type: str = "deposit"
    contract_type_name: str = "保管合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    safekeeping_contract: bool = False
    contract_invalid: bool = False
    delivery_date: Optional[date] = None
    third_party_tort: bool = False
    contract_nature_dispute: bool = False
    purpose_keep_return: bool = False
    transfer_use_right: bool = False
    venue_only: bool = False
    custodian_actual_control: bool = False
    designated_place_activity: bool = False
    item_delivered: bool = False
    item_not_delivered: bool = False
    before_delivery: bool = False
    after_retrieval: bool = False
    during_safekeeping: bool = False
    paid_safekeeping: bool = False
    unpaid_safekeeping: bool = False
    fee_unclear: bool = False
    unpaid_fee: bool = False
    lien_claim: bool = False
    lien_excluded_by_contract: bool = False
    improper_lien: bool = False
    fee_amount: float = 0.0
    item_damage: bool = False
    item_loss: bool = False
    non_return: bool = False
    force_majeure: bool = False
    item_nature_defect: bool = False
    depositor_disclosed: bool = False
    depositor_not_disclosed: bool = False
    depositor_fault: bool = False
    third_party_fault: bool = False
    proper_custody: bool = False
    improper_custody: bool = False
    custodian_general_negligence: bool = False
    custodian_intent_gross: bool = False
    custodian_proves_no_intent_gross: bool = False
    changed_place_method: bool = False
    emergency_or_depositor_interest: bool = False
    transfer_to_third: bool = False
    transfer_agreed: bool = False
    custodian_used_item: bool = False
    third_party_use: bool = False
    use_agreed: bool = False
    third_party_claim: bool = False
    third_party_lawsuit_or_seizure: bool = False
    custodian_notified_depositor: bool = False
    valuable_item: bool = False
    declared_valuable: bool = False
    undeclared_valuable: bool = False
    consumptive_safekeeping: bool = False
    currency_item: bool = False
    fungible_item: bool = False
    depositor_requests_return: bool = False
    custodian_refuses_return: bool = False
    fruits_interest: bool = False
    fixed_period: bool = False
    no_fixed_period: bool = False
    period_expired: bool = False
    depositor_overdue_retrieval: bool = False
    custodian_urged_retrieval: bool = False
    extra_fee: float = 0.0
    actual_loss: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "safekeeping_contract": self.safekeeping_contract,
            "contract_invalid": self.contract_invalid,
            "delivery_date": self.delivery_date.isoformat() if self.delivery_date else None,
            "third_party_tort": self.third_party_tort,
            "contract_nature_dispute": self.contract_nature_dispute,
            "purpose_keep_return": self.purpose_keep_return,
            "transfer_use_right": self.transfer_use_right,
            "venue_only": self.venue_only,
            "custodian_actual_control": self.custodian_actual_control,
            "designated_place_activity": self.designated_place_activity,
            "item_delivered": self.item_delivered,
            "item_not_delivered": self.item_not_delivered,
            "before_delivery": self.before_delivery,
            "after_retrieval": self.after_retrieval,
            "during_safekeeping": self.during_safekeeping,
            "paid_safekeeping": self.paid_safekeeping,
            "unpaid_safekeeping": self.unpaid_safekeeping,
            "fee_unclear": self.fee_unclear,
            "unpaid_fee": self.unpaid_fee,
            "lien_claim": self.lien_claim,
            "lien_excluded_by_contract": self.lien_excluded_by_contract,
            "improper_lien": self.improper_lien,
            "fee_amount": self.fee_amount,
            "item_damage": self.item_damage,
            "item_loss": self.item_loss,
            "non_return": self.non_return,
            "force_majeure": self.force_majeure,
            "item_nature_defect": self.item_nature_defect,
            "depositor_disclosed": self.depositor_disclosed,
            "depositor_not_disclosed": self.depositor_not_disclosed,
            "depositor_fault": self.depositor_fault,
            "third_party_fault": self.third_party_fault,
            "proper_custody": self.proper_custody,
            "improper_custody": self.improper_custody,
            "custodian_general_negligence": self.custodian_general_negligence,
            "custodian_intent_gross": self.custodian_intent_gross,
            "custodian_proves_no_intent_gross": self.custodian_proves_no_intent_gross,
            "changed_place_method": self.changed_place_method,
            "emergency_or_depositor_interest": self.emergency_or_depositor_interest,
            "transfer_to_third": self.transfer_to_third,
            "transfer_agreed": self.transfer_agreed,
            "custodian_used_item": self.custodian_used_item,
            "third_party_use": self.third_party_use,
            "use_agreed": self.use_agreed,
            "third_party_claim": self.third_party_claim,
            "third_party_lawsuit_or_seizure": self.third_party_lawsuit_or_seizure,
            "custodian_notified_depositor": self.custodian_notified_depositor,
            "valuable_item": self.valuable_item,
            "declared_valuable": self.declared_valuable,
            "undeclared_valuable": self.undeclared_valuable,
            "consumptive_safekeeping": self.consumptive_safekeeping,
            "currency_item": self.currency_item,
            "fungible_item": self.fungible_item,
            "depositor_requests_return": self.depositor_requests_return,
            "custodian_refuses_return": self.custodian_refuses_return,
            "fruits_interest": self.fruits_interest,
            "fixed_period": self.fixed_period,
            "no_fixed_period": self.no_fixed_period,
            "period_expired": self.period_expired,
            "depositor_overdue_retrieval": self.depositor_overdue_retrieval,
            "custodian_urged_retrieval": self.custodian_urged_retrieval,
            "extra_fee": self.extra_fee,
            "actual_loss": self.actual_loss,
            "notes": self.notes,
        }


def _format_safekeeping_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: SafekeepingFacts,
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


def extract_safekeeping_facts(case_text: str) -> SafekeepingFacts:
    config = get_safekeeping_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = SafekeepingFacts(raw_text=raw_text)

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.safekeeping_contract = _mentions(text, config.get_terms("safekeeping_contract"))
    facts.contract_invalid = _mentions(text, config.get_terms("contract_invalid"))
    facts.delivery_date = _parse_date(text, config.get_terms("delivery_date"))
    facts.third_party_tort = _mentions(text, config.get_terms("third_party_tort"))

    facts.contract_nature_dispute = _mentions(text, config.get_terms("contract_nature_dispute"))
    facts.purpose_keep_return = _mentions(text, config.get_terms("purpose_keep_return"))
    facts.transfer_use_right = _mentions(text, config.get_terms("transfer_use_right"))
    facts.venue_only = _mentions(text, config.get_terms("venue_only"))
    facts.custodian_actual_control = _mentions(text, config.get_terms("custodian_actual_control"))
    facts.designated_place_activity = _mentions(text, config.get_terms("designated_place_activity"))

    facts.item_delivered = _mentions(text, config.get_terms("item_delivered"))
    facts.item_not_delivered = _mentions(text, config.get_terms("item_not_delivered"))
    facts.before_delivery = _mentions(text, config.get_terms("before_delivery"))
    facts.after_retrieval = _mentions(text, config.get_terms("after_retrieval"))
    facts.during_safekeeping = _mentions(text, config.get_terms("during_safekeeping"))

    facts.paid_safekeeping = _mentions(text, config.get_terms("paid_safekeeping"))
    facts.unpaid_safekeeping = _mentions(text, config.get_terms("unpaid_safekeeping"))
    facts.fee_unclear = _mentions(text, config.get_terms("fee_unclear"))
    facts.unpaid_fee = _mentions(text, config.get_terms("unpaid_fee"))
    facts.lien_claim = _mentions(text, config.get_terms("lien"))
    facts.lien_excluded_by_contract = _mentions(text, config.get_terms("lien_excluded_by_contract"))
    facts.improper_lien = _mentions(text, config.get_terms("improper_lien"))
    facts.fee_amount = _extract_money_near(text, config.get_terms("fee_amount"))

    facts.item_damage = _mentions(text, config.get_terms("item_damage"))
    facts.item_loss = _mentions(text, config.get_terms("item_loss"))
    facts.non_return = _mentions(text, config.get_terms("non_return"))
    facts.force_majeure = _mentions(text, config.get_terms("force_majeure"))
    facts.item_nature_defect = _mentions(text, config.get_terms("item_nature_defect"))
    facts.depositor_disclosed = _mentions(text, config.get_terms("depositor_disclosed"))
    facts.depositor_not_disclosed = _mentions(text, config.get_terms("depositor_not_disclosed"))
    facts.depositor_fault = _mentions(text, config.get_terms("depositor_fault"))
    facts.third_party_fault = _mentions(text, config.get_terms("third_party_fault"))
    facts.proper_custody = _mentions(text, config.get_terms("proper_custody"))
    facts.improper_custody = _mentions(text, config.get_terms("improper_custody"))
    facts.custodian_general_negligence = _mentions(text, config.get_terms("custodian_general_negligence"))
    facts.custodian_intent_gross = _mentions(text, config.get_terms("custodian_intent_gross"))
    facts.custodian_proves_no_intent_gross = _mentions(text, config.get_terms("custodian_proves_no_intent_gross"))
    facts.changed_place_method = _mentions(text, config.get_terms("changed_place_method"))
    facts.emergency_or_depositor_interest = _mentions(text, config.get_terms("emergency_or_depositor_interest"))

    facts.transfer_to_third = _mentions(text, config.get_terms("transfer_to_third"))
    facts.transfer_agreed = _mentions(text, config.get_terms("transfer_agreed"))
    facts.custodian_used_item = _mentions(text, config.get_terms("custodian_used_item"))
    facts.third_party_use = _mentions(text, config.get_terms("third_party_use"))
    facts.use_agreed = _mentions(text, config.get_terms("use_agreed"))
    facts.third_party_claim = _mentions(text, config.get_terms("third_party_claim"))
    facts.third_party_lawsuit_or_seizure = _mentions(text, config.get_terms("third_party_lawsuit_or_seizure"))
    facts.custodian_notified_depositor = _mentions(text, config.get_terms("custodian_notified_depositor"))

    facts.valuable_item = _mentions(text, config.get_terms("valuable_item"))
    facts.declared_valuable = _mentions(text, config.get_terms("declared_valuable"))
    facts.undeclared_valuable = _mentions(text, config.get_terms("undeclared_valuable"))
    if facts.valuable_item and not facts.declared_valuable and _mentions(text, ("未声明", "没有声明", "未验收", "未封存")):
        facts.undeclared_valuable = True

    facts.consumptive_safekeeping = _mentions(text, config.get_terms("consumptive_safekeeping"))
    facts.currency_item = _mentions(text, config.get_terms("currency_item"))
    facts.fungible_item = _mentions(text, config.get_terms("fungible_item"))
    facts.consumptive_safekeeping = facts.consumptive_safekeeping or (
        (facts.currency_item or facts.fungible_item) and _mentions(text, ("同种类", "同数量", "同品质", "可替代"))
    )

    facts.depositor_requests_return = _mentions(text, config.get_terms("depositor_requests_return"))
    facts.custodian_refuses_return = _mentions(text, config.get_terms("custodian_refuses_return"))
    facts.fruits_interest = _mentions(text, config.get_terms("fruits_interest"))
    facts.fixed_period = _mentions(text, config.get_terms("fixed_period"))
    facts.no_fixed_period = _mentions(text, config.get_terms("no_fixed_period"))
    facts.period_expired = _mentions(text, config.get_terms("period_expired"))
    facts.depositor_overdue_retrieval = _mentions(text, config.get_terms("depositor_overdue_retrieval"))
    facts.custodian_urged_retrieval = _mentions(text, config.get_terms("custodian_urged_retrieval"))
    facts.extra_fee = _extract_money_near(text, config.get_terms("extra_fee"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))

    if (facts.item_damage or facts.item_loss or facts.non_return) and not (facts.before_delivery or facts.after_retrieval):
        facts.during_safekeeping = facts.during_safekeeping or facts.item_delivered or facts.safekeeping_contract

    if facts.paid_safekeeping:
        facts.unpaid_safekeeping = False
    elif facts.fee_unclear:
        facts.unpaid_safekeeping = True

    return facts


def _procedure_findings(facts: SafekeepingFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("保管合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告为保管人；可结合签约保管人和实际保管人的履行情况确定")
    return findings


def _only_procedure_question(facts: SafekeepingFacts) -> bool:
    return (
        (facts.asks_jurisdiction or facts.asks_defendant)
        and not facts.contract_nature_dispute
        and not facts.contract_invalid
        and not facts.item_damage
        and not facts.item_loss
        and not facts.non_return
        and not facts.transfer_to_third
        and not facts.custodian_used_item
        and not facts.third_party_use
        and not facts.third_party_claim
        and not facts.unpaid_fee
        and not facts.lien_claim
        and not facts.depositor_requests_return
        and not facts.depositor_overdue_retrieval
    )


def _has_safekeeping_dispute(facts: SafekeepingFacts) -> bool:
    return any(
        (
            facts.safekeeping_contract,
            facts.contract_nature_dispute,
            facts.item_damage,
            facts.item_loss,
            facts.non_return,
            facts.transfer_to_third,
            facts.custodian_used_item,
            facts.third_party_use,
            facts.third_party_claim,
            facts.unpaid_fee,
            facts.lien_claim,
            facts.depositor_requests_return,
            facts.depositor_overdue_retrieval,
            facts.consumptive_safekeeping,
        )
    )


def _amount_text(facts: SafekeepingFacts) -> str:
    return f" {facts.actual_loss:.2f} 元" if facts.actual_loss > 0 else ""


def _fee_text(facts: SafekeepingFacts) -> str:
    return f" {facts.fee_amount:.2f} 元" if facts.fee_amount > 0 else ""


def _extra_fee_text(facts: SafekeepingFacts) -> str:
    return f" {facts.extra_fee:.2f} 元" if facts.extra_fee > 0 else ""


def _compensation_amount_conclusion(facts: SafekeepingFacts, triggered: List[str]) -> tuple[str, List[str]]:
    config = get_safekeeping_config()
    if facts.consumptive_safekeeping:
        triggered = [*triggered, config.patch_name("S6", "消费保管")]
        if facts.currency_item:
            return "属于消费保管，保管人应返还相同种类和数量的货币，而非必须返还原货币。", triggered
        return "属于消费保管，保管人应返还相同种类、品质、数量的可替代物，而非必须返还原物。", triggered

    if facts.valuable_item:
        triggered = [*triggered, config.patch_name("S5", "贵重物品未声明")]
        if facts.declared_valuable:
            amount = _amount_text(facts)
            return f"寄存人已声明贵重物品并由保管人验收或封存，赔偿按实际价值计算{amount}。", triggered
        return "寄存人未声明贵重物品，毁损灭失后按一般物品价值赔偿，具体一般物品价值由法院结合证据酌定。", triggered

    amount = _amount_text(facts)
    if amount:
        return f"赔偿金额按保管物实际损失或市场价值计算，为{amount.strip()}。", triggered
    return "赔偿金额按保管物实际损失或市场价值计算；现有事实未能识别具体金额，需补充价值证据。", triggered


def adjudicate_safekeeping(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_safekeeping_config()
    facts = extract_safekeeping_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "保管合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出保管物毁损、灭失、未返还、费用、留置或保管义务争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_safekeeping_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.third_party_tort and not _has_safekeeping_dispute(facts):
        major = "保管合同裁判引擎处理保管人与寄存人之间的保管、返还、费用和赔偿争议；单纯第三人侵权应按侵权责任另行处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到保管合同履行争议。"
        conclusion = "本案涉及侵权责任，非保管合同纠纷，不适用本保管合同裁判引擎。"
        return _format_safekeeping_output(major, minor, conclusion, [], facts, path, procedure_findings)

    if facts.delivery_date and _years_between(facts.delivery_date, today) > 3:
        major = "保管合同纠纷适用三年一般诉讼时效。"
        minor = f"识别到相关交付、返还或应返还日期为{facts.delivery_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求。"
        return _format_safekeeping_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    path.append("前置实体判断")
    if facts.contract_nature_dispute or facts.transfer_use_right or facts.venue_only or facts.designated_place_activity:
        triggered.append(config.patch_name("S1", "保管合同与租赁合同/场地租赁合同的定性"))
        major = "《民法典》第888条规定，保管合同以保管人保管寄存人交付的保管物并返还该物为核心；购物、就餐、住宿等活动中将物品存放在指定场所的，视为保管。合同性质应根据实质内容认定。"
        if facts.designated_place_activity and facts.custodian_actual_control:
            minor = "识别到寄存人在购物、就餐或住宿活动中，将物品存放在指定场所，且保管人对物品具有实际控制或看管义务。"
            conclusion = "合同性质认定为保管合同，适用保管合同裁判规则。"
        elif facts.venue_only and not facts.custodian_actual_control:
            minor = "识别到合同实质是提供仓位、柜位或场地，由存放人自行控制物品，保管人不承担实质看管义务。"
            conclusion = "合同性质认定为场地租赁合同，不适用本保管合同裁判引擎。"
        elif facts.transfer_use_right and not facts.purpose_keep_return:
            minor = "识别到合同实质是转移物或场地的使用权，而非由保管人保管并返还原物。"
            conclusion = "合同性质认定为租赁合同，不适用本保管合同裁判引擎。"
        elif facts.purpose_keep_return or facts.custodian_actual_control:
            minor = "识别到合同目的为保管并返还原物，且保管人对保管物具有实际控制或看管义务。"
            conclusion = "合同性质认定为保管合同，适用保管合同裁判规则。"
        else:
            minor = "识别到双方对合同性质存在争议，但现有事实不足以判断保管人是否实际控制保管物、是否只提供场地或是否转移使用权。"
            conclusion = "合同性质尚需补充事实；应先查明合同目的和保管人是否承担实际看管义务。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.contract_invalid:
        major = "《民法典》第888条、第890条规定，保管合同以保管和返还保管物为核心，通常自保管物交付时成立；合同无效的，按无效合同后果处理。"
        minor = "识别到保管合同无效或合同不成立事实。"
        conclusion = "保管合同无效，已取得的保管费或保管物应依法返还；因此造成损失的，按过错承担赔偿责任。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.item_not_delivered and not facts.item_damage and not facts.item_loss:
        major = "《民法典》第890条规定，保管合同自保管物交付时成立，但当事人另有约定的除外。"
        minor = "识别到保管物尚未实际交付给保管人，且未识别到双方另有成立时间约定。"
        conclusion = "保管合同尚未成立，保管人不承担保管合同项下的保管责任。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "合同成立审查"], procedure_findings)

    if facts.transfer_to_third:
        triggered.append(config.patch_name("S3", "保管人擅自转保管"))
        major = "《民法典》第894条规定，保管人不得将保管物转交第三人保管，但当事人另有约定的除外；违反规定造成损失的，应当承担赔偿责任。"
        if facts.transfer_agreed:
            minor = "识别到保管人将保管物转交第三人保管，但该转保管经过约定或寄存人同意。"
            conclusion = "转保管经约定，有效；保管人仍应对第三人保管行为造成的后果向寄存人负责。"
        else:
            amount = _amount_text(facts)
            minor = "识别到保管人未经约定或寄存人同意，擅自将保管物转交第三人保管。"
            conclusion = f"保管人擅自转保管构成违约；造成损失的，应承担赔偿责任{amount}。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "保管人义务审查"], procedure_findings)

    if facts.custodian_used_item or facts.third_party_use:
        triggered.append(config.patch_name("S4", "保管人擅自使用保管物"))
        major = "《民法典》第895条规定，保管人不得使用或者许可第三人使用保管物，但当事人另有约定的除外。"
        if facts.use_agreed:
            minor = "识别到保管人或第三人使用保管物，但该使用经过约定或寄存人同意。"
            conclusion = "保管人经约定使用保管物，不因使用本身承担赔偿责任；若另有损坏，仍按保管义务和损失原因审查。"
        else:
            amount = _amount_text(facts)
            minor = "识别到保管人未经约定擅自使用保管物，或许可第三人使用保管物。"
            conclusion = f"保管人擅自使用保管物构成违约；造成保管物损耗或损坏的，应承担赔偿责任{amount}。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "保管人义务审查"], procedure_findings)

    if facts.third_party_claim:
        major = "《民法典》第896条规定，第三人对保管物主张权利的，除依法保全或者执行外，保管人应向寄存人返还保管物；第三人起诉或者申请扣押的，保管人应及时通知寄存人。"
        minor = "识别到第三人对保管物主张权利、起诉或申请扣押。"
        if facts.third_party_lawsuit_or_seizure:
            conclusion = "保管人应及时通知寄存人；保管物被依法保全或执行的，按司法程序处理。"
        else:
            conclusion = "保管人仍应向寄存人返还保管物，不得仅因第三人主张权利而拒绝返还。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "第三人权利主张"], procedure_findings)

    if facts.unpaid_fee or facts.lien_claim or facts.lien_excluded_by_contract:
        triggered.append(config.patch_name("S7", "保管人留置权"))
        major = "《民法典》第903条规定，寄存人未按照约定支付保管费或者其他费用的，保管人对保管物享有留置权，但当事人另有约定的除外。"
        if facts.lien_excluded_by_contract:
            minor = "识别到合同明确约定排除保管人留置权，或约定保管人不得留置保管物。"
            conclusion = "保管人留置权不成立；保管人仍扣留保管物的，构成违约，造成损失的应赔偿。"
        elif facts.improper_lien:
            minor = "识别到寄存人未支付到期保管费或其他费用，但保管人存在超额留置或留置明显不相当财产的事实。"
            conclusion = "保管人留置权成立但行使不当；因不当留置造成寄存人损失的，应承担赔偿责任。"
        elif facts.unpaid_fee:
            minor = "识别到寄存人未按照约定支付到期保管费或其他费用。"
            conclusion = f"保管人留置权成立，保管人可以留置与欠费相当的保管物；欠付费用为{_fee_text(facts).strip() or '待核定'}。"
        else:
            minor = "识别到保管人主张留置保管物，但现有事实未能确认寄存人存在到期未付费用。"
            conclusion = "保管人留置权是否成立需补充保管费或其他费用已到期且未支付的事实。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "保管人留置权"], procedure_findings)

    path.append("核心争议树")
    if facts.before_delivery or facts.after_retrieval:
        major = "保管人的责任期间通常从保管物交付时开始，到保管物返还或寄存人领取后结束。"
        if facts.before_delivery:
            minor = "识别到保管物毁损、灭失发生在交付保管人之前。"
        else:
            minor = "识别到保管物毁损、灭失发生在寄存人领取或保管人返还之后。"
        conclusion = "损失未发生在保管期间，保管人不承担保管合同项下的赔偿责任。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "责任期间"], procedure_findings)

    if facts.period_expired and facts.depositor_overdue_retrieval:
        triggered.append(config.patch_name("S10", "保管合同终止后的逾期领取"))
        major = "《民法典》第899条、第900条、第902条规定，保管期限届满后寄存人应领取保管物；无保管期限的，保管人也可随时请求领取；逾期产生的合理费用应由寄存人承担。"
        minor = "识别到保管期限已经届满，寄存人逾期未领取，保管人已催告或存在继续保管费用。"
        conclusion = f"保管期限已届满，寄存人应在合理期限内领取；逾期产生的额外保管费用由寄存人承担{_extra_fee_text(facts)}。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "保管物返还"], procedure_findings)

    if facts.depositor_requests_return or (facts.custodian_refuses_return and not (facts.item_damage or facts.item_loss)):
        triggered.append(config.patch_name("S8", "寄存人随时领取权"))
        major = "《民法典》第899条、第900条规定，寄存人可以随时领取保管物；保管期限届满或者寄存人提前领取的，保管人应返还原物及其孳息。"
        minor = "识别到寄存人要求领取或提前取回保管物，保管人拒绝返还或未返还。"
        conclusion = "寄存人有权随时领取，保管人应返还保管物及孳息；有偿保管费按实际保管期间结算。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "保管物返还"], procedure_findings)

    if facts.consumptive_safekeeping and not (facts.item_damage or facts.item_loss):
        triggered.append(config.patch_name("S6", "消费保管"))
        major = "《民法典》第901条规定，保管货币或者其他可替代物的，可以按照约定返还相同种类、品质、数量的货币或物品。"
        minor = "识别到保管物为货币或其他可替代物，争议核心为返还对象。"
        conclusion = "属于消费保管，保管人应返还相同种类、数量、品质的货币或物品，而非必须返还原物。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "赔偿金额计算"], procedure_findings)

    if facts.item_damage or facts.item_loss or facts.non_return:
        path.append("毁损灭失原因")
        if facts.force_majeure:
            major = "保管物在保管期间因不可抗力毁损、灭失，且保管人能够证明不可抗力与损失之间存在因果关系的，保管人不承担赔偿责任。"
            minor = "识别到保管物毁损或灭失与不可抗力有关。"
            conclusion = "保管人如能证明损失由不可抗力造成，不承担赔偿责任；不能证明因果关系的，仍需按保管责任审查。"
            return _format_safekeeping_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

        if facts.item_nature_defect:
            triggered.append(config.patch_name("S9", "保管物自身性质导致的损失"))
            major = "《民法典》第893条规定，寄存人交付有瑕疵或者需要采取特殊保管措施的保管物，应当告知保管人；未告知导致损失的，保管人不承担赔偿责任。"
            if facts.depositor_not_disclosed:
                minor = "识别到保管物因自身性质、瑕疵或特殊保管需求发生损失，寄存人未履行告知义务。"
                conclusion = "保管物自身性质导致损失，寄存人未履行告知义务，保管人不承担赔偿责任；保管人因此受损的，寄存人还应承担赔偿责任。"
            elif facts.depositor_disclosed and (facts.improper_custody or facts.changed_place_method):
                minor = "识别到寄存人已告知保管物自身性质或特殊保管需求，但保管人未采取相应保管措施或擅自改变保管方法。"
                amount_conclusion, triggered = _compensation_amount_conclusion(facts, triggered)
                conclusion = f"寄存人已履行告知义务，保管人未妥善保管，应承担赔偿责任。{amount_conclusion}"
            else:
                minor = "识别到保管物自身性质或特殊保管需求可能导致损失，但告知情况和保管措施尚不完整。"
                conclusion = "应先查明寄存人是否履行告知义务；未告知的，保管人原则上不赔，已告知而保管人未妥善处理的，保管人应承担相应责任。"
            return _format_safekeeping_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

        if facts.depositor_fault or facts.third_party_fault:
            major = "保管人能够证明损失由寄存人或第三人过错造成，且与损失存在因果关系的，保管人不承担赔偿责任。"
            minor = "识别到保管物毁损、灭失或未返还与寄存人过错或第三人过错有关。"
            conclusion = "如保管人能够证明该过错事实及因果关系，保管人不承担赔偿责任；相关损失由过错方承担。"
            return _format_safekeeping_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

        if facts.valuable_item and facts.undeclared_valuable and not (
            facts.paid_safekeeping
            or facts.unpaid_safekeeping
            or facts.fee_unclear
            or facts.improper_custody
            or facts.custodian_general_negligence
            or facts.custodian_intent_gross
            or facts.custodian_proves_no_intent_gross
        ):
            triggered.append(config.patch_name("S5", "贵重物品未声明"))
            major = "《民法典》第898条规定，寄存货币、有价证券或者其他贵重物品的，应当向保管人声明并由保管人验收或者封存；未声明的，毁损、灭失后按照一般物品予以赔偿。"
            minor = "识别到寄存人寄存贵重物品，但未向保管人声明，也未由保管人验收或封存，保管期间发生毁损或灭失。"
            conclusion = "寄存人未声明贵重物品，若保管人赔偿责任成立，赔偿范围按一般物品价值计算；保管人是否承担责任仍需结合有偿、无偿及保管过错审查。"
            return _format_safekeeping_output(major, minor, conclusion, triggered, facts, [*path, "赔偿金额计算"], procedure_findings)

        triggered.append(config.patch_name("S2", "有偿保管与无偿保管的责任标准"))
        path.append("保管人责任标准")
        major = "《民法典》第889条、第897条规定，有偿保管中保管人因保管不善造成保管物毁损、灭失的，应承担赔偿责任；无偿保管人证明自己没有故意或者重大过失的，不承担赔偿责任。"
        if facts.unpaid_safekeeping or facts.fee_unclear:
            minor = "识别到本案为无偿保管或保管费约定不明，责任标准为故意或者重大过失。"
            if facts.custodian_proves_no_intent_gross:
                conclusion = "保管合同为无偿保管，保管人已证明自己没有故意或重大过失，不承担赔偿责任。"
                return _format_safekeeping_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
            if facts.custodian_intent_gross or facts.improper_custody:
                amount_conclusion, triggered = _compensation_amount_conclusion(facts, triggered)
                conclusion = f"保管合同为无偿保管，但保管人存在故意或重大过失，应承担赔偿责任。{amount_conclusion}"
                return _format_safekeeping_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
            conclusion = "保管合同为无偿保管，需进一步查明保管人是否存在故意或重大过失；保管人能证明无故意或重大过失的，不承担赔偿责任。"
            return _format_safekeeping_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

        minor = "识别到本案为有偿保管或保管人收取保管费，责任标准为一般过失。"
        if facts.improper_custody or facts.custodian_general_negligence or facts.changed_place_method:
            amount_conclusion, triggered = _compensation_amount_conclusion(facts, triggered)
            conclusion = f"保管合同为有偿保管，保管人未尽妥善保管义务，赔偿责任成立。{amount_conclusion}"
        elif facts.proper_custody:
            conclusion = "保管合同为有偿保管，但现有事实显示保管人已尽妥善保管义务，赔偿责任不成立。"
        else:
            conclusion = "保管合同为有偿保管，需进一步查明保管人是否存在未尽妥善保管义务的一般过失。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.safekeeping_contract:
        major = "《民法典》第888条规定，保管合同的核心义务是保管人保管寄存人交付的保管物并返还该物；保管费、保管方法、返还和赔偿责任需结合具体事实审查。"
        minor = "已识别保管合同关系，但未稳定识别保管物毁损、灭失、未返还、保管费、留置、转保管、擅自使用或领取争议事实。"
        conclusion = "事实要素不足，需补充保管物是否交付、是否毁损灭失或未返还、保管是否有偿、损失原因和金额后再裁判。"
        return _format_safekeeping_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "保管合同纠纷应围绕保管物是否交付、是否在保管期间毁损灭失或未返还、损失原因、保管有偿或无偿以及赔偿金额进行审查。"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的保管合同关键事实。"
    conclusion = "事实要素不足，需补充保管合同关系、保管物交付、毁损灭失或返还争议、责任原因和损失金额后再裁判。"
    return _format_safekeeping_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
