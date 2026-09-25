"""Utility-supply-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import _format_output, _mentions, _parse_date, _years_between
from adjudicate.utility_supply_configs import get_utility_supply_config


@dataclass
class UtilitySupplyFacts:
    raw_text: str
    contract_type: str = "utility_supply"
    contract_type_name: str = "供用电、水、气、热力合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    utility_supply_contract: bool = False
    electricity_contract: bool = False
    water_contract: bool = False
    gas_contract: bool = False
    heat_contract: bool = False
    contract_type_dispute: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    no_written_contract: bool = False
    actual_supply: bool = False
    user_used: bool = False
    paid_fee: bool = False
    refuse_contract: bool = False
    public_supplier: bool = False
    reasonable_request: bool = False
    format_clause: bool = False
    unreasonable_clause: bool = False
    supply_quality_dispute: bool = False
    supply_quality_conform: bool = False
    supply_quality_nonconform: bool = False
    supply_interruption: bool = False
    supplier_fault: bool = False
    maintenance_interruption: bool = False
    legal_power_limit: bool = False
    prior_notice: bool = False
    natural_disaster: bool = False
    timely_repair: bool = False
    user_cause: bool = False
    unpaid_fee: bool = False
    liquidated_damage_claim: bool = False
    urged: bool = False
    reasonable_period_given: bool = False
    supply_suspended: bool = False
    statutory_procedure: bool = False
    property_company_cutoff: bool = False
    property_fee_unpaid: bool = False
    illegal_use: bool = False
    supplier_loss: bool = False
    sub_supply: bool = False
    supplier_consent: bool = False
    metering_dispute: bool = False
    meter_error: bool = False
    meter_fault: bool = False
    user_modified_meter: bool = False
    supplier_install_fault: bool = False
    overcharged: bool = False
    undercharged: bool = False
    maintenance_dispute: bool = False
    boundary_supplier_side: bool = False
    boundary_user_side: bool = False
    boundary_unclear: bool = False
    fault_damage: bool = False
    heating_temp_dispute: bool = False
    heating_temp_not_standard: bool = False
    heating_evidence: bool = False
    no_heating_evidence: bool = False
    commitment_restore_time: bool = False
    commitment_breached: bool = False
    actual_loss: float = 0.0
    fee_amount: float = 0.0
    liquidated_damage_amount: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "utility_supply_contract": self.utility_supply_contract,
            "electricity_contract": self.electricity_contract,
            "water_contract": self.water_contract,
            "gas_contract": self.gas_contract,
            "heat_contract": self.heat_contract,
            "contract_type_dispute": self.contract_type_dispute,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "no_written_contract": self.no_written_contract,
            "actual_supply": self.actual_supply,
            "user_used": self.user_used,
            "paid_fee": self.paid_fee,
            "refuse_contract": self.refuse_contract,
            "public_supplier": self.public_supplier,
            "reasonable_request": self.reasonable_request,
            "format_clause": self.format_clause,
            "unreasonable_clause": self.unreasonable_clause,
            "supply_quality_dispute": self.supply_quality_dispute,
            "supply_quality_conform": self.supply_quality_conform,
            "supply_quality_nonconform": self.supply_quality_nonconform,
            "supply_interruption": self.supply_interruption,
            "supplier_fault": self.supplier_fault,
            "maintenance_interruption": self.maintenance_interruption,
            "legal_power_limit": self.legal_power_limit,
            "prior_notice": self.prior_notice,
            "natural_disaster": self.natural_disaster,
            "timely_repair": self.timely_repair,
            "user_cause": self.user_cause,
            "unpaid_fee": self.unpaid_fee,
            "liquidated_damage_claim": self.liquidated_damage_claim,
            "urged": self.urged,
            "reasonable_period_given": self.reasonable_period_given,
            "supply_suspended": self.supply_suspended,
            "statutory_procedure": self.statutory_procedure,
            "property_company_cutoff": self.property_company_cutoff,
            "property_fee_unpaid": self.property_fee_unpaid,
            "illegal_use": self.illegal_use,
            "supplier_loss": self.supplier_loss,
            "sub_supply": self.sub_supply,
            "supplier_consent": self.supplier_consent,
            "metering_dispute": self.metering_dispute,
            "meter_error": self.meter_error,
            "meter_fault": self.meter_fault,
            "user_modified_meter": self.user_modified_meter,
            "supplier_install_fault": self.supplier_install_fault,
            "overcharged": self.overcharged,
            "undercharged": self.undercharged,
            "maintenance_dispute": self.maintenance_dispute,
            "boundary_supplier_side": self.boundary_supplier_side,
            "boundary_user_side": self.boundary_user_side,
            "boundary_unclear": self.boundary_unclear,
            "fault_damage": self.fault_damage,
            "heating_temp_dispute": self.heating_temp_dispute,
            "heating_temp_not_standard": self.heating_temp_not_standard,
            "heating_evidence": self.heating_evidence,
            "no_heating_evidence": self.no_heating_evidence,
            "commitment_restore_time": self.commitment_restore_time,
            "commitment_breached": self.commitment_breached,
            "actual_loss": self.actual_loss,
            "fee_amount": self.fee_amount,
            "liquidated_damage_amount": self.liquidated_damage_amount,
            "notes": self.notes,
        }


def _format_utility_supply_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: UtilitySupplyFacts,
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


def extract_utility_supply_facts(case_text: str) -> UtilitySupplyFacts:
    config = get_utility_supply_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = UtilitySupplyFacts(raw_text=raw_text)

    for field_name in (
        "utility_supply_contract", "electricity_contract", "water_contract", "gas_contract",
        "heat_contract", "third_party_tort", "no_written_contract", "actual_supply",
        "user_used", "paid_fee", "refuse_contract", "public_supplier", "reasonable_request",
        "format_clause", "unreasonable_clause", "supply_quality_dispute",
        "supply_quality_conform", "supply_quality_nonconform", "supply_interruption",
        "supplier_fault", "maintenance_interruption", "legal_power_limit", "prior_notice",
        "natural_disaster", "timely_repair", "user_cause", "unpaid_fee",
        "liquidated_damage_claim", "urged", "reasonable_period_given", "supply_suspended",
        "statutory_procedure", "property_company_cutoff", "property_fee_unpaid",
        "illegal_use", "supplier_loss", "sub_supply", "supplier_consent",
        "metering_dispute", "meter_error", "meter_fault", "user_modified_meter",
        "supplier_install_fault", "overcharged", "undercharged", "maintenance_dispute",
        "boundary_supplier_side", "boundary_user_side", "boundary_unclear", "fault_damage",
        "heating_temp_dispute", "heating_temp_not_standard", "heating_evidence",
        "no_heating_evidence", "commitment_restore_time", "commitment_breached",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_type_dispute = any(word in text for word in ("什么合同", "哪类合同", "适用什么规则", "参照适用", "合同类型"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))
    facts.fee_amount = _extract_money_near(text, config.get_terms("fee_amount"))
    facts.liquidated_damage_amount = _extract_money_near(text, config.get_terms("liquidated_damage_amount"))

    if any((facts.electricity_contract, facts.water_contract, facts.gas_contract, facts.heat_contract, facts.actual_supply)):
        facts.utility_supply_contract = True
    return facts


def _procedure_findings(facts: UtilitySupplyFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("供用电、水、气、热力合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理。")
    if facts.asks_defendant:
        findings.append("适格被告按争议请求确定：用户请求恢复供应、赔偿损失的，通常列供应企业为被告；供应企业追缴费用、违约金的，通常列用户为被告。")
    return findings


def _only_procedure_question(facts: UtilitySupplyFacts) -> bool:
    substantive = any(
        (
            facts.contract_type_dispute, facts.no_written_contract, facts.refuse_contract,
            facts.supply_quality_dispute, facts.supply_interruption, facts.unpaid_fee,
            facts.supply_suspended, facts.property_company_cutoff, facts.illegal_use,
            facts.sub_supply, facts.metering_dispute, facts.maintenance_dispute,
            facts.heating_temp_dispute, facts.commitment_restore_time,
        )
    )
    return (facts.asks_jurisdiction or facts.asks_defendant) and not substantive


def _supply_type_sentence(facts: UtilitySupplyFacts) -> tuple[str, str]:
    if facts.water_contract:
        return "供用水", "参照适用"
    if facts.gas_contract:
        return "供用气", "参照适用"
    if facts.heat_contract:
        return "供用热力", "参照适用"
    return "供用电", "直接适用"


def adjudicate_utility_supply(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_utility_supply_config()
    facts = extract_utility_supply_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "供用合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出供应质量、费用支付、中止供应、计量或设施维护等实体争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_utility_supply_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.third_party_tort and not facts.utility_supply_contract:
        major = "供用合同裁判引擎处理供应企业与用户之间因持续供应和费用支付产生的合同争议；单纯合同外第三人侵权应按侵权责任处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到供用合同履行争议。"
        conclusion = "本案涉及侵权责任，非供用合同纠纷，不适用本供用合同裁判引擎。"
        return _format_utility_supply_output(major, minor, conclusion, [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "供用合同纠纷适用三年一般诉讼时效。"
        minor = f"识别到相关合同签订、履行、催告或中止供应日期为{facts.contract_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求。"
        return _format_utility_supply_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    path.append("前置实体判断")
    if facts.contract_type_dispute:
        triggered.append(config.patch_name("U1", "合同类型的识别与参照适用"))
        supply_type, apply_mode = _supply_type_sentence(facts)
        major = "《民法典》第648条规定供用电合同的基本规则；第656条规定，供用水、供用气、供用热力合同参照适用供用电合同的有关规定。"
        minor = f"识别到本案争议属于{supply_type}合同或需要确认供用合同适用规则。"
        conclusion = f"本案为{supply_type}合同，{apply_mode}供用电合同的有关规定。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, [*path, "合同类型识别"], procedure_findings)

    if facts.no_written_contract:
        triggered.append(config.patch_name("U11", "未签订书面合同的供用关系认定"))
        major = "供用合同不以书面形式为成立的唯一条件。供应方已实际供应，用户已实际使用并支付费用的，可以认定供用合同关系成立。"
        minor = "识别到双方未签订书面供用合同。"
        if facts.actual_supply and facts.user_used and facts.paid_fee:
            conclusion = "供用合同关系成立，双方应按实际供用关系和交易习惯履行供应、使用和付费义务。"
        else:
            conclusion = "现有事实不足以证明已经形成事实供应关系，供用合同关系暂不能认定成立。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, [*path, "合同成立与效力审查"], procedure_findings)

    if facts.refuse_contract:
        triggered.append(config.patch_name("U2", "强制缔约义务"))
        major = "《民法典》第648条规定，向社会公众供电的供电人不得拒绝用电人合理的订立合同要求。"
        minor = "识别到用户主张供应方拒绝订立供用合同、拒绝开户或拒绝接入。"
        if facts.public_supplier and facts.reasonable_request:
            conclusion = "供应方违反强制缔约义务，应承担相应责任。"
        else:
            conclusion = "尚不能证明用户属于合理订立合同要求或供应方属于面向社会公众的供应主体，暂不认定供应方违反强制缔约义务。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, [*path, "强制缔约义务"], procedure_findings)

    if facts.format_clause:
        major = "《民法典》第496条、第497条规定，提供格式条款的一方应履行提示说明义务；不合理免除自身责任、加重对方责任、排除对方主要权利的格式条款无效。"
        minor = "识别到供用合同中存在预先拟定、不能协商的格式条款。"
        conclusion = "该格式条款不合理免除供应方责任、加重用户责任或排除用户主要权利的，相关条款无效。" if facts.unreasonable_clause else "未识别到不合理免除或加重责任内容，格式条款效力需结合提示说明情况继续审查。"
        return _format_utility_supply_output(major, minor, conclusion, [], facts, [*path, "格式条款审查"], procedure_findings)

    if facts.illegal_use:
        triggered.append(config.patch_name("U7", "用户违规使用的责任"))
        major = "《民法典》第655条规定，用电人应当按照国家有关规定和当事人的约定安全、节约和计划用电；未按规定和约定用电造成供电人损失的，应承担赔偿责任。"
        minor = "识别到用户存在违规使用、窃能或擅自改变使用类别等行为。"
        conclusion = f"用户存在违规使用行为，造成供应方损失的，应承担赔偿责任，已识别损失为 {_money(facts.actual_loss)}。" if facts.supplier_loss else "用户存在违规使用行为；是否承担赔偿责任，还需证明该行为造成供应方损失。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, [*path, "用户义务审查"], procedure_findings)

    if facts.sub_supply:
        triggered.append(config.patch_name("U8", "转供的处理"))
        major = "供用合同具有公共安全和持续供应属性。用户未经供应方同意向第三方转供的，供应方可以要求停止转供；造成损失的，用户承担违约责任。"
        minor = "识别到用户向第三方转供水、电、气或热力。"
        conclusion = "转供已经供应方同意，暂不认定用户违约。" if facts.supplier_consent else "用户存在违规转供行为，应停止转供；造成损失的，应承担违约责任。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, [*path, "用户义务审查"], procedure_findings)

    path.append("供应质量不达标/供应中断")
    if facts.heating_temp_dispute:
        triggered.append(config.patch_name("U13", "供暖温度不达标的举证责任"))
        major = "用户主张供暖温度不达标的，应及时保留投诉、维修、测温或第三方检测记录；有有效证据的，可按不达标期间主张相应减免供暖费。"
        minor = "识别到用户以供暖温度不达标为由拒交或要求减免供暖费。"
        if facts.heating_evidence and not facts.no_heating_evidence:
            conclusion = "供暖温度不达标主张成立，用户可以按不达标期间主张减免供暖费。"
        else:
            conclusion = "供暖温度不达标主张不成立，用户缺少有效测温、投诉、维修或检测证据，不能仅以体感不热拒交供暖费。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, [*path, "供暖温度举证"], procedure_findings)

    if facts.commitment_restore_time:
        triggered.append(config.patch_name("U15", "供应方的承诺效力"))
        major = "供应方在停供公告中明确恢复供应时间的，该明确恢复时间可作为对用户的承诺；违反承诺造成损失的，应承担违约责任。"
        minor = "识别到供应方在停供公告或通知中明确了承诺恢复供应时间。"
        conclusion = f"供应方已作出承诺且违反承诺，应承担违约责任，已识别损失为 {_money(facts.actual_loss)}。" if facts.commitment_breached else "供应方已作出恢复供应时间承诺；未识别到违反承诺，暂不承担违约责任。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.supply_quality_dispute or facts.supply_quality_nonconform:
        triggered.append(config.patch_name("U3", "供应质量不达标的处理"))
        major = "《民法典》第651条规定，供电人应按照国家规定的供电质量标准和约定安全供电；未按质量标准和约定安全供电造成用户损失的，应承担赔偿责任。供用水、气、热力合同参照适用。"
        minor = "识别到用户主张供应质量不符合国家标准或合同约定。"
        if facts.supply_quality_conform and not facts.supply_quality_nonconform:
            conclusion = "供应方已达到国家规定的供应质量标准，不承担赔偿责任，用户不可以据此主张减免使用费。"
        else:
            conclusion = f"供应方未达到国家规定的供应质量标准，应承担赔偿责任，用户可以主张相应减免使用费；已识别损失为 {_money(facts.actual_loss)}。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.supply_interruption:
        if facts.natural_disaster:
            triggered.append(config.patch_name("U5", "自然灾害断电后的抢修义务"))
            major = "《民法典》第653条规定，因自然灾害等原因断电的，供电人应按照国家有关规定及时抢修；未及时抢修造成用户损失的，应承担赔偿责任。供用水、气、热力合同参照适用。"
            minor = "识别到供应中断系自然灾害等原因引起。"
            conclusion = "供应方已及时抢修，不承担赔偿责任。" if facts.timely_repair else f"供应方未及时抢修，应承担赔偿责任，已识别损失为 {_money(facts.actual_loss)}。"
            return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.maintenance_interruption or facts.legal_power_limit or facts.user_cause:
            triggered.append(config.patch_name("U4", "中断供应的通知义务"))
            major = "《民法典》第652条规定，因计划检修、临时检修、依法限供或者用户违法使用等原因需要中断供应的，应按照国家有关规定事先通知用户；未事先通知造成损失的，应承担赔偿责任。"
            minor = "识别到供应方因检修、依法限供或用户原因中断供应。"
            conclusion = "供应方已履行中断供应的事先通知义务，不承担赔偿责任。" if facts.prior_notice else f"供应方未履行中断供应的事先通知义务，应承担赔偿责任，已识别损失为 {_money(facts.actual_loss)}。"
            return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.supplier_fault:
            triggered.append(config.patch_name("U3", "供应质量不达标的处理"))
            major = "供应方因设备故障、管理不善等自身原因导致供应中断，属于未按约安全、持续供应。"
            minor = "识别到供应中断由供应方原因造成。"
            conclusion = f"供应方承担违约责任，用户可主张赔偿损失并相应减免使用费；已识别损失为 {_money(facts.actual_loss)}。"
            return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("使用费支付争议")
    if facts.property_company_cutoff:
        triggered.append(config.patch_name("U12", "物业公司无权对用户断水断电"))
        major = "供水、供电合同的当事人是用户和自来水公司、供电公司等供应企业。物业公司不是供用合同供应方，无权以催缴物业费为由断水断电。"
        minor = "识别到物业公司以用户拖欠物业费为由实施断水断电。"
        conclusion = f"物业公司断水断电不合法，应恢复供应并赔偿损失；已识别损失为 {_money(facts.actual_loss)}。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.liquidated_damage_claim and facts.liquidated_damage_amount > 0:
        triggered.append(config.patch_name("U14", "违约金过高的调整"))
        major = "《民法典》第585条规定，约定的违约金过分高于造成的损失的，人民法院可以根据当事人的请求予以适当减少。"
        minor = f"识别到供应方主张违约金 {_money(facts.liquidated_damage_amount)}，用户请求调整；实际损失识别为 {_money(facts.actual_loss)}。"
        if facts.actual_loss > 0 and facts.liquidated_damage_amount > facts.actual_loss * 1.3:
            conclusion = "违约金过高，应予以调减。"
        else:
            conclusion = "现有事实不足以认定违约金过分高于实际损失，暂不予调减。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.unpaid_fee or facts.supply_suspended:
        triggered.append(config.patch_name("U6", "欠费中止供应的法定程序"))
        major = "《民法典》第654条规定，用户应及时支付使用费；逾期不支付的，应按约定支付违约金。经催告后在合理期限内仍不支付使用费和违约金的，供应方可以按照国家规定的程序中止供应。"
        minor = "识别到用户欠付使用费或供应方因欠费中止供应。"
        if facts.supply_suspended:
            if facts.urged and facts.reasonable_period_given and facts.statutory_procedure:
                conclusion = "供应方中止供应程序合法，不承担违约责任；用户仍应支付欠费及约定违约金。"
            else:
                conclusion = "供应方中止供应程序不合法，应承担违约责任；中止供应前应履行催告、给予合理期限并按国家规定程序处理。"
        else:
            conclusion = f"用户逾期未支付使用费，应支付欠费及约定违约金；已识别欠费为 {_money(facts.fee_amount)}。供应方中止供应前仍应依法催告。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("计量争议")
    if facts.metering_dispute or facts.meter_error:
        triggered.append(config.patch_name("U9", "计量误差的处理"))
        major = "计量装置存在误差导致多计或少计的，应按实际用量重新计算使用费；实际用量可参照历史用量或同类用户平均用量推算，差额多退少补。"
        minor = "识别到计量装置误差或双方对使用量、读数存在争议。"
        if facts.user_modified_meter:
            conclusion = f"计量误差由用户私自改动计量装置造成，用户承担违约责任并补足费用；已识别金额为 {_money(facts.fee_amount)}。"
        elif facts.supplier_install_fault:
            conclusion = f"计量误差由供应方安装或维护不当造成，供应方承担责任，应按实际用量重新计算并多退少补；已识别差额为 {_money(facts.fee_amount)}。"
        else:
            direction = "多退" if facts.overcharged else "少补" if facts.undercharged else "多退少补"
            conclusion = f"计量装置存在误差，应按实际用量重新计算，差额{direction}；已识别金额为 {_money(facts.fee_amount)}。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("设施维护责任")
    if facts.maintenance_dispute:
        triggered.append(config.patch_name("U10", "设施维护责任的认定"))
        major = "《民法典》第650条规定，供用电合同履行地点有约定的按约定；没有约定或约定不明确的，供电设施的产权分界处为履行地点。设施维护责任通常以产权分界处为界确定，供用水、气、热力合同参照适用。"
        minor = "识别到供用设施损坏，双方对维修责任有争议。"
        if facts.boundary_supplier_side:
            conclusion = "设施损坏发生在产权分界处供应方侧，设施维护责任由供应方承担。"
        elif facts.boundary_user_side:
            conclusion = "设施损坏发生在产权分界处用户侧，设施维护责任由用户承担。"
        else:
            conclusion = "产权分界处不明确的，应先按合同约定、设施产权归属和行业规则确定分界处，再按分界处确定维护责任。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.utility_supply_contract:
        major = "《民法典》第648条至第656条规定，供用合同裁判应围绕供应方是否安全、持续、达标供应，用户是否及时付费并安全使用，以及中止供应、计量和设施维护责任是否合法进行审查。"
        minor = "已识别供用合同关系，但未稳定识别供应质量、费用支付、中止供应、计量误差或设施维护等具体争议事实。"
        conclusion = "事实要素不足，需要补充供应类型、是否中断或不达标、欠费和催告情况、计量误差原因、设施产权分界处及损失金额后再裁判。"
        return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "供用电、水、气、热力合同纠纷应围绕持续安全供应、使用费支付、中止供应程序、计量误差和设施维护责任进行审查。"
    minor = "自然语言事实未能稳定识别出供用合同关系和关键争议节点。"
    conclusion = "事实要素不足，需要补充是否存在供用合同关系、供应类型、使用费支付、供应中断或质量不达标、计量或设施维护争议后再裁判。"
    return _format_utility_supply_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
