"""Warehouse-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import _format_output, _mentions, _parse_date, _years_between
from adjudicate.warehouse_configs import get_warehouse_config


@dataclass
class WarehouseFacts:
    raw_text: str
    contract_type: str = "warehouse"
    contract_type_name: str = "仓储合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    warehouse_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    nature_dispute: bool = False
    warehouse_business: bool = False
    general_safekeeping: bool = False
    consensual_contract: bool = False
    contract_invalid: bool = False
    qualification_issue: bool = False
    goods_delivered: bool = False
    receipt_issued: bool = False
    receipt_transfer: bool = False
    receipt_pledge: bool = False
    receipt_endorsed: bool = False
    keeper_signed_receipt: bool = False
    multiple_claimants: bool = False
    receipt_holder: bool = False
    acceptance_dispute: bool = False
    goods_nonconform: bool = False
    timely_notice: bool = False
    no_timely_notice: bool = False
    after_acceptance_nonconform: bool = False
    dangerous_goods: bool = False
    hazard_explained: bool = False
    hazard_not_explained: bool = False
    damage_or_loss: bool = False
    in_storage_period: bool = False
    before_or_after_storage: bool = False
    improper_custody: bool = False
    natural_property: bool = False
    bad_packaging: bool = False
    expired_storage: bool = False
    force_majeure: bool = False
    actual_loss: float = 0.0
    partial_damage: bool = False
    undamaged_return: bool = False
    value_depreciation: bool = False
    inspection_request: bool = False
    deterioration_found: bool = False
    loss_expanded: bool = False
    danger_to_others: bool = False
    emergency: bool = False
    disposed: bool = False
    period_due: bool = False
    retrieved: bool = False
    overdue_retrieval: bool = False
    keeper_urged: bool = False
    deposit_goods: bool = False
    early_retrieval: bool = False
    unclear_storage_period: bool = False
    unpaid_storage_fee: bool = False
    lien_claim: bool = False
    fee_amount: float = 0.0
    termination_request: bool = False
    statutory_termination_reason: bool = False
    depositor_assignment: bool = False
    valid_assignment: bool = False
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "warehouse_contract": self.warehouse_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "nature_dispute": self.nature_dispute,
            "warehouse_business": self.warehouse_business,
            "general_safekeeping": self.general_safekeeping,
            "consensual_contract": self.consensual_contract,
            "contract_invalid": self.contract_invalid,
            "qualification_issue": self.qualification_issue,
            "goods_delivered": self.goods_delivered,
            "receipt_issued": self.receipt_issued,
            "receipt_transfer": self.receipt_transfer,
            "receipt_pledge": self.receipt_pledge,
            "receipt_endorsed": self.receipt_endorsed,
            "keeper_signed_receipt": self.keeper_signed_receipt,
            "multiple_claimants": self.multiple_claimants,
            "receipt_holder": self.receipt_holder,
            "acceptance_dispute": self.acceptance_dispute,
            "goods_nonconform": self.goods_nonconform,
            "timely_notice": self.timely_notice,
            "no_timely_notice": self.no_timely_notice,
            "after_acceptance_nonconform": self.after_acceptance_nonconform,
            "dangerous_goods": self.dangerous_goods,
            "hazard_explained": self.hazard_explained,
            "hazard_not_explained": self.hazard_not_explained,
            "damage_or_loss": self.damage_or_loss,
            "in_storage_period": self.in_storage_period,
            "before_or_after_storage": self.before_or_after_storage,
            "improper_custody": self.improper_custody,
            "natural_property": self.natural_property,
            "bad_packaging": self.bad_packaging,
            "expired_storage": self.expired_storage,
            "force_majeure": self.force_majeure,
            "actual_loss": self.actual_loss,
            "partial_damage": self.partial_damage,
            "undamaged_return": self.undamaged_return,
            "value_depreciation": self.value_depreciation,
            "inspection_request": self.inspection_request,
            "deterioration_found": self.deterioration_found,
            "loss_expanded": self.loss_expanded,
            "danger_to_others": self.danger_to_others,
            "emergency": self.emergency,
            "disposed": self.disposed,
            "period_due": self.period_due,
            "retrieved": self.retrieved,
            "overdue_retrieval": self.overdue_retrieval,
            "keeper_urged": self.keeper_urged,
            "deposit_goods": self.deposit_goods,
            "early_retrieval": self.early_retrieval,
            "unclear_storage_period": self.unclear_storage_period,
            "unpaid_storage_fee": self.unpaid_storage_fee,
            "lien_claim": self.lien_claim,
            "fee_amount": self.fee_amount,
            "termination_request": self.termination_request,
            "statutory_termination_reason": self.statutory_termination_reason,
            "depositor_assignment": self.depositor_assignment,
            "valid_assignment": self.valid_assignment,
            "notes": self.notes,
        }


def _format_warehouse_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: WarehouseFacts,
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


def extract_warehouse_facts(case_text: str) -> WarehouseFacts:
    config = get_warehouse_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = WarehouseFacts(raw_text=raw_text)

    for field_name in (
        "warehouse_contract", "third_party_tort", "nature_dispute", "warehouse_business",
        "general_safekeeping", "consensual_contract", "contract_invalid", "qualification_issue",
        "goods_delivered", "receipt_issued", "receipt_transfer", "receipt_pledge",
        "receipt_endorsed", "keeper_signed_receipt", "multiple_claimants", "receipt_holder",
        "acceptance_dispute", "goods_nonconform", "timely_notice", "no_timely_notice",
        "after_acceptance_nonconform", "dangerous_goods", "hazard_explained",
        "hazard_not_explained", "damage_or_loss", "in_storage_period",
        "before_or_after_storage", "improper_custody", "natural_property", "bad_packaging",
        "expired_storage", "force_majeure", "partial_damage", "undamaged_return",
        "value_depreciation", "inspection_request", "deterioration_found", "loss_expanded",
        "danger_to_others", "emergency", "disposed", "period_due", "retrieved",
        "overdue_retrieval", "keeper_urged", "deposit_goods", "early_retrieval",
        "unclear_storage_period", "unpaid_storage_fee", "lien_claim", "termination_request",
        "statutory_termination_reason", "depositor_assignment", "valid_assignment",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))
    facts.fee_amount = _extract_money_near(text, config.get_terms("fee_amount"))

    if any(
        (
            facts.warehouse_business, facts.receipt_issued, facts.receipt_transfer,
            facts.receipt_pledge, facts.goods_delivered, facts.unpaid_storage_fee,
            facts.damage_or_loss, facts.overdue_retrieval, facts.early_retrieval,
            facts.unclear_storage_period,
        )
    ):
        facts.warehouse_contract = True
    return facts


def _procedure_findings(facts: WarehouseFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("仓储合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告应结合争议确定：仓储物毁损灭失通常列保管人，仓储费欠付通常列存货人或仓单持有人")
    return findings


def _has_substantive_dispute(facts: WarehouseFacts) -> bool:
    return any(
        (
            facts.nature_dispute, facts.contract_invalid, facts.qualification_issue,
            facts.receipt_transfer, facts.receipt_pledge, facts.multiple_claimants,
            facts.acceptance_dispute, facts.goods_nonconform, facts.dangerous_goods,
            facts.damage_or_loss, facts.partial_damage, facts.value_depreciation,
            facts.inspection_request, facts.deterioration_found, facts.danger_to_others,
            facts.overdue_retrieval, facts.early_retrieval, facts.unclear_storage_period,
            facts.unpaid_storage_fee, facts.lien_claim, facts.termination_request,
            facts.depositor_assignment,
        )
    )


def _only_procedure_question(facts: WarehouseFacts) -> bool:
    return (facts.asks_jurisdiction or facts.asks_defendant) and not _has_substantive_dispute(facts)


def adjudicate_warehouse(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_warehouse_config()
    facts = extract_warehouse_facts(case_text)
    today = today or date.today()
    procedure_findings = _procedure_findings(facts)
    path = ["入口程序校验"]

    if _only_procedure_question(facts):
        major = "仓储合同纠纷适用合同纠纷管辖和适格当事人规则；合同有有效管辖约定的，按约定处理。"
        minor = "本案事实主要询问起诉法院或应列被告，未提出需要实体裁判的仓储物、仓单或仓储费争议。"
        conclusion = "按程序事项处理：" + "；".join(procedure_findings)
        return _format_warehouse_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "仓储合同纠纷通常适用三年诉讼时效。"
        minor = f"本案可识别的合同或履行日期为 {facts.contract_date.isoformat()}，距今已超过三年，且未识别到中止、中断或延长事由。"
        conclusion = "诉讼时效已过，超过时效部分不予支持。"
        return _format_warehouse_output(major, minor, conclusion, ["诉讼时效"], facts, [*path, "诉讼时效"], procedure_findings)

    if facts.third_party_tort and not facts.warehouse_contract:
        major = "第三人侵害财产或人身权益的，按侵权责任规则处理；合同裁判引擎处理合同相对方之间的履行争议。"
        minor = "本案主要事实指向合同外第三人侵权，未能识别仓储合同履行争议。"
        conclusion = "本案涉及侵权责任，非仓储合同纠纷，不适用本仓储合同裁判引擎。"
        return _format_warehouse_output(major, minor, conclusion, [], facts, [*path, "侵权第三方分流"], procedure_findings)

    path.append("前置实体判断")

    if facts.qualification_issue and not facts.nature_dispute:
        major = "仓储合同应以合法仓储物和符合法律要求的仓储经营活动为基础；保管人不具备仓储营业资质的，不宜按商事仓储合同规则处理。"
        minor = "本案保管人不具备仓储营业资质或并非仓储营业人。"
        conclusion = "本案不宜按仓储合同处理；已实际保管的，按实际保管关系结算费用和损失。"
        return _format_warehouse_output(major, minor, conclusion, ["合同效力审查"], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.nature_dispute or facts.warehouse_business or facts.general_safekeeping or facts.consensual_contract:
        triggered = [config.patch_name("W1", "仓储合同与保管合同的区分认定")]
        major = "仓储合同是保管人储存存货人交付的仓储物、存货人支付仓储费的合同，自双方意思表示一致时成立；仓储合同通常要求保管人以仓储为业，并可涉及仓单制度。"
        if facts.general_safekeeping and not facts.warehouse_business:
            minor = "本案保管人并非以仓储为业，事实更接近一般物品保管。"
            conclusion = "合同性质认定为保管合同，不适用仓储合同裁判规则，应转入保管合同裁判引擎处理。"
        else:
            minor = "本案能够识别保管人以仓储为业、双方以储存保管仓储物并支付仓储费为交易目的。"
            conclusion = "合同性质认定为仓储合同，适用仓储合同裁判规则。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.contract_invalid or facts.qualification_issue:
        major = "仓储合同应以合法仓储物和符合法律要求的仓储经营活动为基础；合同无效后，应按返还财产和过错赔偿处理。"
        if facts.qualification_issue:
            minor = "本案保管人不具备仓储营业资质或并非仓储营业人。"
            conclusion = "本案不宜按仓储合同处理；已实际保管的，按实际保管关系结算费用和损失。"
        else:
            minor = "本案涉及违禁品储存、非法仓储物或其他导致仓储合同无效的事实。"
            conclusion = "仓储合同无效，因合同取得的财产应依法返还；造成损失的，按双方过错承担赔偿责任。"
        return _format_warehouse_output(major, minor, conclusion, ["合同效力审查"], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.multiple_claimants:
        major = "仓单是提取仓储物的凭证，合法持有仓单的人有权提取仓储物。"
        minor = "本案存在多人主张提取仓储物的争议。"
        if facts.receipt_holder:
            conclusion = "合法仓单持有人有权提取仓储物；非仓单持有人不得要求保管人交付仓储物。"
        else:
            conclusion = "需先查明谁合法持有仓单；不能证明合法持有仓单的，不得要求提取仓储物。"
        return _format_warehouse_output(major, minor, conclusion, [config.patch_name("W11", "仓单持有人身份的认定")], facts, [*path, "仓单持有人身份"], procedure_findings)

    if facts.receipt_transfer or facts.receipt_pledge:
        triggered = [config.patch_name("W2", "仓单的转让与质押效力")]
        major = "仓单是提取仓储物的凭证；存货人或仓单持有人在仓单上背书并经保管人签名或者盖章的，可以转让提取仓储物的权利；仓单也可以作为权利质押标的。"
        if facts.receipt_pledge and not facts.receipt_transfer:
            minor = "本案涉及仓单质押。"
            conclusion = "仓单可以作为权利质押标的；质押是否有效，还需审查质押设立和登记、交付等要件。"
        elif facts.receipt_endorsed and facts.keeper_signed_receipt:
            minor = "本案仓单转让具备背书并经保管人签名或盖章的形式要件。"
            conclusion = "仓单转让有效，受让人取得提货权。"
        else:
            minor = "本案仓单转让未能识别背书以及保管人签名或盖章的完整形式要件。"
            conclusion = "仓单转让无效或效力待定，受让人暂未取得对保管人的提货权。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, [*path, "仓单效力"], procedure_findings)

    if facts.acceptance_dispute or facts.after_acceptance_nonconform or (facts.goods_nonconform and not (facts.bad_packaging or facts.damage_or_loss)):
        triggered = [config.patch_name("W3", "保管人验收义务与责任")]
        major = "保管人应按约定对入库仓储物进行验收；验收时发现不符合约定的，应及时通知存货人；验收后发生品种、数量、质量不符合约定的，保管人应承担赔偿责任。"
        if facts.after_acceptance_nonconform or (facts.goods_nonconform and not facts.timely_notice):
            minor = "本案仓储物品种、数量或质量与约定不符，且保管人未能证明验收时及时提出异议或通知存货人。"
            conclusion = "保管人未充分履行验收和通知义务，应承担相应赔偿责任。"
        else:
            minor = "本案保管人在验收时发现仓储物不符合约定，并已及时通知存货人。"
            conclusion = "保管人已履行验收和通知义务，不因入库时已通知的不符事项承担赔偿责任。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, [*path, "入库验收"], procedure_findings)

    if facts.dangerous_goods:
        triggered = [config.patch_name("W6", "危险物品/易变质物品的说明义务")]
        major = "储存危险物品或易变质物品的，存货人应说明物品性质并提供有关资料；违反说明义务的，保管人可以拒收或采取相应措施避免损失，费用由存货人负担。"
        if facts.hazard_not_explained or not facts.hazard_explained:
            minor = "本案仓储物属于危险物品或易变质物品，未能识别存货人已充分说明性质并提供资料。"
            conclusion = "存货人未履行危险物品说明义务，保管人可以拒收仓储物或采取必要措施，费用由存货人承担。"
        else:
            minor = "本案存货人已说明危险物品或易变质物品性质并提供资料。"
            conclusion = "存货人已履行说明义务，保管人应按约定和专业仓储要求储存。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, [*path, "危险物品说明义务"], procedure_findings)

    if facts.depositor_assignment:
        triggered = [config.patch_name("W14", "存货人变更/转让后的权利义务")]
        major = "存货人转让仓储物且转让有效的，受让人承继与仓储物相关的提货权、检查权以及支付仓储费等义务。"
        if facts.valid_assignment:
            minor = "本案存在有效的仓储物转让事实。"
            conclusion = "仓储物已转让，受让人承继存货人的权利义务。"
        else:
            minor = "本案存在转让主张，但未能识别有效转让手续。"
            conclusion = "受让人暂不承继存货人的权利义务，原存货人仍为仓储合同当事人。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, [*path, "存货人变更"], procedure_findings)

    if facts.deterioration_found and (facts.no_timely_notice or facts.loss_expanded):
        triggered = [config.patch_name("W13", "保管人未尽通知义务的责任")]
        major = "保管人发现入库仓储物有变质或者其他损坏的，应及时通知存货人或者仓单持有人；未及时通知导致损失扩大的，对扩大部分承担赔偿责任。"
        minor = "本案保管人发现仓储物变质或损坏后未及时通知，并造成或可能造成损失扩大。"
        conclusion = "保管人未及时履行通知义务，对扩大损失承担赔偿责任。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, [*path, "检查通知与处置义务"], procedure_findings)

    if facts.danger_to_others:
        triggered = [config.patch_name("W7", "保管人紧急处置权")]
        major = "仓储物变质或损坏危及其他仓储物安全和正常保管的，保管人应催告存货人或仓单持有人处置；情况紧急的，可以作出必要处置，但事后应及时通知。"
        if facts.emergency or facts.disposed:
            minor = "本案仓储物变质或损坏已经危及其他仓储物，且存在紧急处置必要。"
            conclusion = "保管人紧急处置权成立，处置费用由存货人承担，但保管人事后应及时通知。"
        else:
            minor = "本案仓储物变质或损坏危及其他仓储物，但未识别紧急情况。"
            conclusion = "保管人应先催告存货人或仓单持有人作出必要处置；未催告即处置的，应审查处置必要性。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, [*path, "检查通知与处置义务"], procedure_findings)

    path.append("仓储物毁损灭失责任认定")

    if facts.partial_damage:
        triggered = [config.patch_name("W12", "仓储物部分毁损/灭失的处理")]
        major = "仓储物仅部分毁损或灭失的，保管人只对依法应赔的毁损、灭失部分承担赔偿责任，未毁损部分仍应返还。"
        minor = f"本案仓储物发生部分毁损或灭失，可识别损失金额为 {_money(facts.actual_loss)}。"
        conclusion = f"仓储物部分毁损/灭失，保管人应赔偿毁损部分损失 {_money(facts.actual_loss)}，未毁损部分应予返还。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, [*path, "部分毁损灭失"], procedure_findings)

    if facts.value_depreciation:
        triggered = [config.patch_name("W15", "仓储物价值减损的认定")]
        major = "仓储物虽未毁损灭失，但因保管不善导致价值减损的，保管人应赔偿价值减损损失。"
        if facts.improper_custody:
            minor = f"本案仓储物价值减损，且减损原因指向保管人保管不善，可识别减损金额为 {_money(facts.actual_loss)}。"
            conclusion = f"仓储物因保管不善价值减损 {_money(facts.actual_loss)}，保管人应赔偿。"
        else:
            minor = "本案存在价值减损，但尚不能识别减损系保管不善造成。"
            conclusion = "需补充价值减损原因；不能证明保管不善的，保管人不承担赔偿责任。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, [*path, "价值减损"], procedure_findings)

    if facts.damage_or_loss:
        triggered = [config.patch_name("W4", "保管人免责事由")]
        major = "储存期内因保管不善造成仓储物毁损、灭失的，保管人应承担赔偿责任；因仓储物自然性质、包装不符合约定、超过有效储存期或不可抗力造成损失的，保管人不承担赔偿责任。"
        if facts.before_or_after_storage:
            minor = "本案仓储物毁损灭失发生在入库前或出库后，未发生在保管人责任期间。"
            conclusion = "保管人不承担赔偿责任。"
        elif facts.natural_property or facts.bad_packaging or facts.expired_storage or facts.force_majeure:
            minor = "本案仓储物毁损灭失原因属于自然性质、包装不符合约定、超过有效储存期或不可抗力。"
            conclusion = "仓储物毁损灭失属于保管人免责事由，保管人不承担赔偿责任。"
        elif facts.improper_custody or facts.in_storage_period:
            minor = f"本案仓储物在储存期内毁损灭失，且未识别到法定免责事由，损失金额为 {_money(facts.actual_loss)}。"
            conclusion = f"仓储物毁损灭失不属于保管人免责事由，保管人承担赔偿责任，赔偿范围按实际损失 {_money(facts.actual_loss)} 计算。"
        else:
            minor = "本案存在仓储物毁损灭失，但尚不能识别发生时间、损害原因和免责事由。"
            conclusion = "存货人应证明仓储物在储存期内毁损灭失；保管人主张免责的，应证明自然性质、包装不符、超期或不可抗力等事由。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("检查通知与处置义务")

    if facts.inspection_request:
        major = "保管人根据存货人或者仓单持有人的要求，应当同意其检查仓储物或者提取样品。"
        minor = "本案存货人或仓单持有人要求检查仓储物或提取样品。"
        conclusion = "保管人应当配合检查仓储物或提取样品；无正当理由拒绝的，应承担违约责任。"
        return _format_warehouse_output(major, minor, conclusion, ["检查取样权"], facts, path, procedure_findings)

    if facts.deterioration_found and (facts.no_timely_notice or facts.loss_expanded):
        triggered = [config.patch_name("W13", "保管人未尽通知义务的责任")]
        major = "保管人发现入库仓储物有变质或者其他损坏的，应及时通知存货人或者仓单持有人；未及时通知导致损失扩大的，对扩大部分承担赔偿责任。"
        minor = "本案保管人发现仓储物变质或损坏后未及时通知，并造成或可能造成损失扩大。"
        conclusion = "保管人未及时履行通知义务，对扩大损失承担赔偿责任。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.danger_to_others:
        triggered = [config.patch_name("W7", "保管人紧急处置权")]
        major = "仓储物变质或损坏危及其他仓储物安全和正常保管的，保管人应催告存货人或仓单持有人处置；情况紧急的，可以作出必要处置，但事后应及时通知。"
        if facts.emergency or facts.disposed:
            minor = "本案仓储物变质或损坏已经危及其他仓储物，且存在紧急处置必要。"
            conclusion = "保管人紧急处置权成立，处置费用由存货人承担，但保管人事后应及时通知。"
        else:
            minor = "本案仓储物变质或损坏危及其他仓储物，但未识别紧急情况。"
            conclusion = "保管人应先催告存货人或仓单持有人作出必要处置；未催告即处置的，应审查处置必要性。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("仓储物提取")

    if facts.early_retrieval:
        triggered = [config.patch_name("W8", "提前提取不减收仓储费")]
        major = "存货人或者仓单持有人在储存期限届满前提前提取仓储物的，不减收仓储费。"
        minor = f"本案存货人或仓单持有人提前提取仓储物，可识别仓储费金额为 {_money(facts.fee_amount)}。"
        conclusion = f"存货人提前提取仓储物，仓储费不减收，应按原约定支付 {_money(facts.fee_amount)}。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.overdue_retrieval or (facts.period_due and not facts.retrieved):
        triggered = [config.patch_name("W5", "逾期提取的加收费与提存规则")]
        major = "储存期限届满后，存货人或者仓单持有人逾期提取的，应加收仓储费；保管人可以催告其在合理期限内提取，逾期不提取的可以提存仓储物。"
        minor = f"本案储存期限已经届满，存货人或仓单持有人未按期提取，可识别加收仓储费为 {_money(facts.fee_amount)}。"
        if facts.keeper_urged or facts.deposit_goods:
            conclusion = f"存货人逾期未提取，应加收仓储费 {_money(facts.fee_amount)}；保管人催告后仍不提取的，可以提存仓储物。"
        else:
            conclusion = f"存货人逾期未提取，应加收仓储费 {_money(facts.fee_amount)}；保管人可催告提取，逾期不提取的可提存仓储物。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.unclear_storage_period:
        triggered = [config.patch_name("W9", "储存期限约定不明的处理")]
        major = "当事人对储存期限没有约定或者约定不明确的，存货人或仓单持有人可以随时提取，保管人也可以随时请求提取，但应给予必要准备时间。"
        minor = "本案储存期限没有约定或约定不明确。"
        conclusion = "储存期限约定不明，双方均可随时主张提取，但应给予必要的准备时间。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("仓储费与留置权")

    if facts.unpaid_storage_fee or facts.lien_claim:
        major = "存货人未按约支付仓储费且仓储物仍由保管人占有的，保管人依法可以主张留置权，并就仓储物折价、拍卖或变卖价款优先受偿。"
        minor = f"本案存在仓储费欠付或留置权争议，可识别欠付仓储费为 {_money(facts.fee_amount)}。"
        conclusion = f"保管人对其占有的仓储物可以依法行使留置权，并就欠付仓储费 {_money(facts.fee_amount)} 优先受偿；留置范围应与债权相当。"
        return _format_warehouse_output(major, minor, conclusion, ["仓储费留置权"], facts, path, procedure_findings)

    path.append("独立分支")

    if facts.termination_request:
        triggered = [config.patch_name("W10", "仓储合同解除")]
        major = "因不可抗力致使不能实现合同目的、一方明确拒绝履行、迟延履行经催告后仍未履行，或其他违约行为致使合同目的不能实现的，当事人可以解除合同。"
        if facts.statutory_termination_reason:
            minor = "本案存在可识别的法定解除事由。"
            conclusion = "仓储合同解除成立，解除后应返还仓储物、结清已发生仓储费，并由违约方赔偿损失。"
        else:
            minor = "本案虽有解除仓储合同主张，但未识别不可抗力、拒绝履行、催告后仍不履行或合同目的不能实现等法定解除事由。"
            conclusion = "仓储合同解除不成立，各方应继续按合同履行；已有违约的，可另行主张违约责任。"
        return _format_warehouse_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.warehouse_contract:
        major = "仓储合同中，保管人应以专业仓储标准储存保管仓储物，存货人应支付仓储费并依约提取仓储物。"
        minor = "本案能够识别仓储合同关系，但未识别足以触发仓单、验收、危险物品、毁损灭失、提取或仓储费留置的具体争议。"
        conclusion = "仓储合同继续有效，各方应按合同履行；如主张违约责任，需进一步补充仓储物状态、仓单、仓储费或提取期限等事实。"
    else:
        major = "仓储裁判需先识别保管人是否以仓储为业、仓储物是否入库、是否涉及仓单以及具体争议事实。"
        minor = "现有自然语言事实不足以确认仓储合同关系和裁判节点。"
        conclusion = "请补充保管人主体、仓储物入库、仓单、仓储费、毁损灭失或提取期限等事实后再裁判。"
    return _format_warehouse_output(major, minor, conclusion, [], facts, path, procedure_findings)
