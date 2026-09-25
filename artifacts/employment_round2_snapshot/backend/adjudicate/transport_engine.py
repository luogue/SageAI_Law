"""Transportation-contract adjudication engine."""

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
from adjudicate.transport_configs import get_transport_config


@dataclass
class TransportFacts:
    raw_text: str
    contract_type: str = "transportation"
    contract_type_name: str = "运输合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    transport_contract: bool = False
    contract_invalid: bool = False
    delivery_date: Optional[date] = None
    cargo_delivered_to_carrier: bool = False
    cargo_damage: bool = False
    cargo_loss: bool = False
    cargo_delay: bool = False
    in_transit: bool = False
    before_loading: bool = False
    after_unloading: bool = False
    force_majeure: bool = False
    natural_property: bool = False
    reasonable_wear: bool = False
    shipper_fault: bool = False
    consignee_fault: bool = False
    carrier_proves_exemption: bool = False
    causation_proven: bool = False
    valuation_clause: bool = False
    carrier_explained_clause: bool = False
    carrier_no_explanation: bool = False
    carrier_intent_gross_negligence: bool = False
    agreed_compensation: float = 0.0
    market_price: float = 0.0
    delay_loss: float = 0.0
    shipper_info_accurate: bool = False
    shipper_info_inaccurate: bool = False
    change_request: bool = False
    before_delivery: bool = False
    after_delivery: bool = False
    carrier_loss: float = 0.0
    unpaid_freight: bool = False
    lien_claim: bool = False
    improper_lien: bool = False
    prior_freight_debt: bool = False
    current_cargo_lien: bool = False
    same_legal_relationship: bool = False
    different_legal_relationship: bool = False
    lien_excluded_by_contract: bool = False
    mitigation_failure: bool = False
    freight_amount: float = 0.0
    continuous_transport: bool = False
    unknown_transport_segment: bool = False
    sea_segment: bool = False
    land_segment: bool = False
    third_party_tort: bool = False
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "transport_contract": self.transport_contract,
            "contract_invalid": self.contract_invalid,
            "delivery_date": self.delivery_date.isoformat() if self.delivery_date else None,
            "cargo_delivered_to_carrier": self.cargo_delivered_to_carrier,
            "cargo_damage": self.cargo_damage,
            "cargo_loss": self.cargo_loss,
            "cargo_delay": self.cargo_delay,
            "in_transit": self.in_transit,
            "before_loading": self.before_loading,
            "after_unloading": self.after_unloading,
            "force_majeure": self.force_majeure,
            "natural_property": self.natural_property,
            "reasonable_wear": self.reasonable_wear,
            "shipper_fault": self.shipper_fault,
            "consignee_fault": self.consignee_fault,
            "carrier_proves_exemption": self.carrier_proves_exemption,
            "causation_proven": self.causation_proven,
            "valuation_clause": self.valuation_clause,
            "carrier_explained_clause": self.carrier_explained_clause,
            "carrier_no_explanation": self.carrier_no_explanation,
            "carrier_intent_gross_negligence": self.carrier_intent_gross_negligence,
            "agreed_compensation": self.agreed_compensation,
            "market_price": self.market_price,
            "delay_loss": self.delay_loss,
            "shipper_info_accurate": self.shipper_info_accurate,
            "shipper_info_inaccurate": self.shipper_info_inaccurate,
            "change_request": self.change_request,
            "before_delivery": self.before_delivery,
            "after_delivery": self.after_delivery,
            "carrier_loss": self.carrier_loss,
            "unpaid_freight": self.unpaid_freight,
            "lien_claim": self.lien_claim,
            "improper_lien": self.improper_lien,
            "prior_freight_debt": self.prior_freight_debt,
            "current_cargo_lien": self.current_cargo_lien,
            "same_legal_relationship": self.same_legal_relationship,
            "different_legal_relationship": self.different_legal_relationship,
            "lien_excluded_by_contract": self.lien_excluded_by_contract,
            "mitigation_failure": self.mitigation_failure,
            "freight_amount": self.freight_amount,
            "continuous_transport": self.continuous_transport,
            "unknown_transport_segment": self.unknown_transport_segment,
            "sea_segment": self.sea_segment,
            "land_segment": self.land_segment,
            "third_party_tort": self.third_party_tort,
            "notes": self.notes,
        }


def _format_transport_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: TransportFacts,
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


def extract_transport_facts(case_text: str) -> TransportFacts:
    config = get_transport_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = TransportFacts(raw_text=raw_text)

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.transport_contract = _mentions(text, config.get_terms("transport_contract"))
    facts.contract_invalid = _mentions(text, config.get_terms("contract_invalid"))
    facts.delivery_date = _parse_date(text, config.get_terms("delivery_date"))

    facts.cargo_delivered_to_carrier = _mentions(text, config.get_terms("cargo_delivered_to_carrier"))
    facts.cargo_damage = _mentions(text, config.get_terms("cargo_damage"))
    facts.cargo_loss = _mentions(text, config.get_terms("cargo_loss"))
    facts.cargo_delay = _mentions(text, config.get_terms("cargo_delay"))
    facts.in_transit = _mentions(text, config.get_terms("in_transit"))
    facts.before_loading = _mentions(text, config.get_terms("before_loading"))
    facts.after_unloading = _mentions(text, config.get_terms("after_unloading"))
    if (facts.cargo_damage or facts.cargo_loss) and not (facts.before_loading or facts.after_unloading):
        facts.in_transit = facts.in_transit or facts.cargo_delivered_to_carrier

    facts.force_majeure = _mentions(text, config.get_terms("force_majeure"))
    facts.natural_property = _mentions(text, config.get_terms("natural_property"))
    facts.reasonable_wear = _mentions(text, config.get_terms("reasonable_wear"))
    facts.shipper_fault = _mentions(text, config.get_terms("shipper_fault"))
    facts.consignee_fault = _mentions(text, config.get_terms("consignee_fault"))
    facts.carrier_proves_exemption = _mentions(text, config.get_terms("carrier_proves"))
    facts.causation_proven = _mentions(text, config.get_terms("causation"))

    facts.valuation_clause = _mentions(text, config.get_terms("valuation_clause"))
    facts.carrier_explained_clause = _mentions(text, config.get_terms("carrier_explained_clause"))
    facts.carrier_no_explanation = _mentions(text, config.get_terms("carrier_no_explanation"))
    facts.carrier_intent_gross_negligence = _mentions(text, config.get_terms("carrier_intent_gross_negligence"))
    facts.agreed_compensation = _extract_money_near(text, config.get_terms("agreed_compensation"))
    facts.market_price = _extract_money_near(text, config.get_terms("market_price"))
    facts.delay_loss = _extract_money_near(text, config.get_terms("delay_loss"))

    facts.shipper_info_accurate = _mentions(text, config.get_terms("shipper_info_accurate"))
    facts.shipper_info_inaccurate = _mentions(text, config.get_terms("shipper_info_inaccurate"))
    facts.change_request = _mentions(text, config.get_terms("change_request"))
    facts.before_delivery = _mentions(text, config.get_terms("before_delivery"))
    facts.after_delivery = _mentions(text, config.get_terms("after_delivery"))
    facts.carrier_loss = _extract_money_near(text, config.get_terms("carrier_loss"))
    facts.unpaid_freight = _mentions(text, config.get_terms("unpaid_freight"))
    facts.lien_claim = _mentions(text, config.get_terms("lien"))
    facts.improper_lien = _mentions(text, config.get_terms("improper_lien"))
    facts.prior_freight_debt = _mentions(text, config.get_terms("prior_freight_debt"))
    facts.current_cargo_lien = _mentions(text, config.get_terms("current_cargo_lien"))
    facts.same_legal_relationship = _mentions(text, config.get_terms("same_legal_relationship"))
    facts.different_legal_relationship = _mentions(text, config.get_terms("different_legal_relationship"))
    facts.lien_excluded_by_contract = _mentions(text, config.get_terms("lien_excluded_by_contract"))
    facts.mitigation_failure = _mentions(text, config.get_terms("mitigation_failure"))
    facts.freight_amount = _extract_money_near(text, config.get_terms("freight_amount"))
    facts.continuous_transport = _mentions(text, config.get_terms("continuous_transport"))
    facts.unknown_transport_segment = _mentions(text, config.get_terms("unknown_transport_segment"))
    facts.sea_segment = _mentions(text, config.get_terms("sea_segment"))
    facts.land_segment = _mentions(text, config.get_terms("land_segment"))
    facts.third_party_tort = _mentions(text, config.get_terms("third_party_tort"))
    return facts


def _procedure_findings(facts: TransportFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("运输合同纠纷可由运输始发地、目的地或者被告住所地人民法院处理")
    if facts.asks_defendant:
        findings.append("适格被告为承运人；可结合签约承运人和实际承运人的运输参与情况确定")
    return findings


def _only_procedure_question(facts: TransportFacts) -> bool:
    return (
        (facts.asks_jurisdiction or facts.asks_defendant)
        and not facts.cargo_damage
        and not facts.cargo_loss
        and not facts.cargo_delay
        and not facts.shipper_info_inaccurate
        and not facts.change_request
        and not facts.unpaid_freight
        and not facts.lien_claim
        and not facts.continuous_transport
        and not facts.lien_excluded_by_contract
        and not facts.prior_freight_debt
    )


def _exemption_reason(facts: TransportFacts) -> str:
    if facts.force_majeure:
        return "不可抗力"
    if facts.natural_property or facts.reasonable_wear:
        return "货物本身的自然性质或合理损耗"
    if facts.shipper_fault:
        return "托运人过错"
    if facts.consignee_fault:
        return "收货人过错"
    return ""


def _compensation_conclusion(facts: TransportFacts, triggered: List[str]) -> tuple[str, List[str]]:
    config = get_transport_config()
    if facts.valuation_clause:
        triggered = [*triggered, config.patch_name("T2", "保价条款效力审查")]
        if facts.carrier_intent_gross_negligence:
            amount = facts.market_price or facts.agreed_compensation
            if amount > 0:
                return f"承运人存在故意或重大过失，保价或限额赔偿条款不适用，赔偿金额为 {amount:.2f} 元。", triggered
            return "承运人存在故意或重大过失，保价或限额赔偿条款不适用，应按实际损失赔偿。", triggered
        if facts.carrier_no_explanation:
            amount = facts.market_price
            if amount > 0:
                return f"保价条款无效，赔偿金额为 {amount:.2f} 元，按交付或应当交付时货物到达地市场价格计算。", triggered
            return "保价条款无效，赔偿金额应按交付或应当交付时货物到达地市场价格计算。", triggered
        if facts.carrier_explained_clause:
            amount = facts.agreed_compensation or facts.market_price
            if amount > 0:
                return f"保价条款有效，赔偿金额为 {amount:.2f} 元。", triggered
            return "保价条款有效，赔偿金额按保价或限额赔偿约定确定。", triggered
        return "需审查承运人是否就保价或限额赔偿条款尽到提示说明义务；未尽提示说明义务的，按第833条市场价格计算。", triggered

    amount = facts.market_price
    if amount > 0:
        return f"无有效保价或赔偿约定，赔偿金额按到达地市场价格计算，为 {amount:.2f} 元。", triggered
    return "无有效保价或赔偿约定，赔偿金额应按交付或应当交付时货物到达地市场价格计算。", triggered


def adjudicate_transportation(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_transport_config()
    facts = extract_transport_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "运输合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出货损、灭失、延迟、运费、留置或多式联运事实。"
        conclusion = "；".join(procedure_findings)
        return _format_transport_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.third_party_tort and not facts.transport_contract:
        major = "运输合同裁判引擎处理运输合同项下的安全、按时运输和费用争议；单纯第三方侵权应按侵权责任另行处理。"
        minor = "识别到争议核心是第三方侵权，未识别到运输合同履行争议。"
        conclusion = "本案涉及侵权责任，非运输合同纠纷，不适用本运输合同裁判引擎"
        return _format_transport_output(major, minor, conclusion, [], facts, path, procedure_findings)

    if facts.delivery_date and _years_between(facts.delivery_date, today) > 3:
        major = "普通货运合同纠纷适用三年一般诉讼时效；法律、行政法规或特别法另有规定的，从其规定。"
        minor = f"识别到交付或应交付日期为{facts.delivery_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求"
        return _format_transport_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    path.append("前置实体判断")
    if facts.contract_invalid:
        major = "《民法典》第809条规定，运输合同是承运人将旅客或者货物从起运地点运输到约定地点，托运人或者收货人支付运输费用的合同。合同无效的，按无效合同后果处理。"
        minor = "识别到运输合同无效或合同未成立事实。"
        conclusion = "运输合同无效，已取得的运输费用或货物应依法返还；因此造成损失的，按过错承担赔偿责任。"
        return _format_transport_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.shipper_info_inaccurate:
        major = "《民法典》第825条规定，托运人办理货物运输，应当向承运人准确表明收货人、货物名称、性质、重量、数量、收货地点等必要情况。"
        minor = "识别到托运人存在瞒报、错报、未如实告知货物性质、重量、数量或危险属性的事实。"
        conclusion = "托运人未准确告知货物运输必要信息，应对因此造成的损失承担相应责任。"
        return _format_transport_output(major, minor, conclusion, triggered, facts, [*path, "托运人义务审查"], procedure_findings)

    if facts.change_request:
        triggered.append(config.patch_name("T4", "托运人变更/解除的赔偿"))
        major = "《民法典》第829条规定，在承运人将货物交付收货人之前，托运人可以要求中止运输、返还货物、变更到达地或者将货物交给其他收货人，但是应当赔偿承运人因此受到的损失。"
        if facts.after_delivery:
            minor = "识别到托运人在货物已交付收货人之后要求中止、返还、变更到达地或变更收货人。"
            conclusion = "货物已交付收货人之后，托运人不得再行使变更或解除运输合同的权利。"
        else:
            minor = "识别到托运人在货物交付收货人之前要求中止运输、返还货物、变更到达地或变更收货人。"
            if facts.carrier_loss > 0:
                conclusion = f"托运人变更/解除有效，应赔偿承运人损失 {facts.carrier_loss:.2f} 元。"
            else:
                conclusion = "托运人变更/解除有效，应赔偿承运人因此受到的空驶费、仓储费、改派费等实际损失。"
        return _format_transport_output(major, minor, conclusion, triggered, facts, [*path, "托运人变更/解除权"], procedure_findings)

    if facts.unpaid_freight or facts.lien_claim or facts.lien_excluded_by_contract or facts.prior_freight_debt:
        triggered.append(config.patch_name("T5", "承运人留置权"))
        major = "托运人、收货人未支付运费、保管费以及其他运输费用的，承运人对相应运输货物依法享有留置权；留置权应在相应范围内合理行使。"
        if facts.lien_excluded_by_contract:
            triggered.append(config.patch_name("T7", "合同排除留置权的效力"))
            major = "《民法典》第836条规定，托运人或者收货人不支付运费、保管费或者其他费用的，承运人对相应的运输货物享有留置权，但是当事人另有约定的除外。"
            minor = "识别到运输合同明确约定承运人不得留置货物，但承运人仍以欠付运费为由扣押货物。"
            if facts.mitigation_failure:
                conclusion = "合同明确排除留置权，承运人扣货构成违约；承运人应赔偿因此造成的损失，但托运人未及时采取措施防止损失扩大的，就扩大部分自行承担。"
            else:
                conclusion = "合同明确排除留置权，承运人扣货构成违约；造成托运人损失的，承运人应承担赔偿责任。"
        elif facts.prior_freight_debt and (facts.current_cargo_lien or facts.lien_claim):
            triggered.append(config.patch_name("T6", "留置权的同一法律关系限制"))
            major = "《民法典》第448条规定，债权人留置的动产，应当与债权属于同一法律关系；企业之间留置的除外，但仍应结合交易关系和合同约定审查。"
            if facts.same_legal_relationship:
                minor = "识别到承运人因此前运费扣押当前货物，但欠付运费与当前承运货物属于同一合同项下连续履行或同一法律关系。"
                conclusion = "欠付运费与当前货物属于同一法律关系，承运人留置权成立。"
            elif facts.different_legal_relationship:
                minor = "识别到承运人因此前其他业务的运费欠款，扣押当前批次货物，且欠款与当前货物属于多笔独立业务。"
                conclusion = "欠付运费与当前货物不属于同一法律关系，承运人留置权不成立；承运人擅自扣货构成违约，造成损失的应承担赔偿责任。"
            else:
                minor = "识别到承运人因此前运费扣押当前货物，但现有事实不足以判断欠款与当前货物是否属于同一法律关系。"
                conclusion = "承运人留置权是否成立，需先审查欠付运费与当前货物是否属于同一法律关系；不属于同一法律关系的，扣货构成违约。"
        elif facts.improper_lien:
            minor = "识别到托运人或收货人未支付运输费用，但承运人存在超额留置、留置全部货物或其他不当行使留置权的事实。"
            conclusion = "承运人留置权成立但行使不当；因不当留置造成损失的，承运人应承担赔偿责任。"
        elif facts.unpaid_freight:
            minor = "识别到托运人或收货人到期未支付运费、保管费或其他运输费用。"
            conclusion = "承运人留置权成立，承运人可留置与欠费相应的运输货物。"
        else:
            minor = "识别到承运人主张留置货物，但未稳定识别到到期未支付的运输费用。"
            conclusion = "承运人留置权是否成立需补充运费、保管费或其他运输费用已到期且未支付的事实。"
        return _format_transport_output(major, minor, conclusion, triggered, facts, [*path, "承运人留置权"], procedure_findings)

    if facts.continuous_transport and not ((facts.cargo_damage or facts.cargo_loss) and (facts.unknown_transport_segment or facts.sea_segment or facts.land_segment)):
        triggered.append(config.patch_name("T3", "连续运输/多式联运责任划分"))
        major = "连续运输、多式联运或转包运输中，与托运人订立合同的承运人对全程运输承担责任；损失发生在某一区段的，该区段承运人承担相应责任。"
        minor = "识别到运输涉及多个承运人、转包、分段运输或多式联运。"
        conclusion = "签约承运人承担全程责任，可向区段承运人追偿。"
        return _format_transport_output(major, minor, conclusion, triggered, facts, [*path, "连续运输/多式联运"], procedure_findings)

    path.append("核心争议树")
    if facts.before_loading or facts.after_unloading:
        major = "承运人承担运输责任的期间通常以接收货物后至交付货物前为核心；货损发生在承运人责任期间外的，承运人不承担运输合同项下货损赔偿责任。"
        minor = "识别到货物毁损、灭失发生在装货前、承运人接收前、卸货后或收货人签收后。"
        conclusion = "货损未发生在承运人责任期间内，承运人不承担赔偿责任。"
        return _format_transport_output(major, minor, conclusion, triggered, facts, [*path, "责任期间"], procedure_findings)

    if facts.cargo_damage or facts.cargo_loss:
        path.append("承运人免责事由")
        if facts.continuous_transport and (facts.unknown_transport_segment or facts.sea_segment or facts.land_segment):
            triggered.append(config.patch_name("T8", "多式联运区段不明时的责任"))
            major = "多式联运或连续运输中，不同运输区段可能适用不同赔偿规则；货损发生在海运区段或运输区段不能确定的，适用海商法责任限额，能查明为陆运区段的，适用《民法典》运输合同规则。"
            if facts.land_segment:
                minor = "识别到货物在多式联运过程中毁损或灭失，且能够查明货损发生在陆运区段。"
                amount_text = f"；已识别实际损失为 {facts.market_price:.2f} 元" if facts.market_price > 0 else ""
                conclusion = f"货损发生在陆运区段，适用《民法典》运输合同规定，赔偿以实际损失为准{amount_text}。"
            elif facts.sea_segment:
                minor = "识别到货物在多式联运过程中毁损或灭失，且能够查明货损发生在海运区段。"
                conclusion = "货损发生在海运区段，适用《海商法》赔偿责任限额；具体限额需结合运输单证、货物件数、重量和特别声明价值确定。"
            else:
                minor = "识别到货物在多式联运过程中毁损或灭失，但无法查明发生在哪一个运输区段。"
                conclusion = "货损区段无法查明，适用《海商法》赔偿责任限额；不同运输方式赔偿标准差异较大，需补充运输单证、货物件数和重量。"
            return _format_transport_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        triggered.append(config.patch_name("T1", "承运人严格责任"))
        major = "《民法典》第832条规定，承运人对运输过程中货物的毁损、灭失承担赔偿责任；承运人证明毁损、灭失因不可抗力、货物自然性质或者合理损耗以及托运人、收货人过错造成的，不承担赔偿责任。"
        minor = "识别到货物已交给承运人，且在运输过程中发生毁损或灭失。"
        exemption = _exemption_reason(facts)
        if exemption and facts.carrier_proves_exemption and facts.causation_proven:
            conclusion = f"承运人已证明货损系{exemption}造成，且该事由与货损之间存在因果关系，承运人免责。"
            return _format_transport_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if exemption and facts.carrier_proves_exemption and not facts.causation_proven:
            conclusion = "承运人虽主张存在免责事由，但未证明该事由与货损之间存在因果关系，仍应承担赔偿责任。"
            return _format_transport_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

        amount_conclusion, triggered = _compensation_conclusion(facts, triggered)
        if facts.valuation_clause:
            path.append("赔偿金额计算")
        conclusion = f"承运人未能证明免责事由（或因果关系不成立），应承担赔偿责任。{amount_conclusion}"
        return _format_transport_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.cargo_delay:
        major = "《民法典》第811条规定，承运人应当在约定期限或者合理期限内将货物安全运输到约定地点；延迟交付适用一般违约责任规则。"
        minor = "识别到承运人未在约定期限或合理期限内送达货物。"
        if facts.delay_loss > 0:
            conclusion = f"承运人构成延迟交付违约，应赔偿因此造成的损失 {facts.delay_loss:.2f} 元。"
        else:
            conclusion = "承运人构成延迟交付违约；托运人或收货人需证明因延迟遭受的具体损失后主张赔偿。"
        return _format_transport_output(major, minor, conclusion, triggered, facts, [*path, "延迟交付"], procedure_findings)

    if facts.transport_contract:
        major = "《民法典》第809条规定，运输合同的核心义务是承运人将货物从起运地点运输到约定地点，托运人或收货人支付运输费用。"
        minor = "已识别运输合同关系，但未稳定识别货损、灭失、延迟、运费留置或变更解除等具体争议事实。"
        conclusion = "事实要素不足，需补充货物是否毁损、灭失、延迟，货损是否发生在运输过程中，承运人是否存在免责事由以及损失金额后再裁判"
        return _format_transport_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "运输合同纠纷应围绕货物是否安全、按时到达，货损是否发生在承运人责任期间，承运人能否证明免责事由以及赔偿金额进行审查。"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的运输合同关键事实。"
    conclusion = "事实要素不足，需补充运输合同关系、货损或延迟事实、责任期间、免责事由和损失金额后再裁判"
    return _format_transport_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
