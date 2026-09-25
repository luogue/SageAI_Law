"""Work-contract adjudication engine."""

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
from adjudicate.work_contract_configs import get_work_contract_config


@dataclass
class WorkContractFacts:
    raw_text: str
    contract_type: str = "work_contract"
    contract_type_name: str = "承揽合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    work_contract: bool = False
    contract_nature_dispute: bool = False
    named_sale_contract: bool = False
    named_work_contract: bool = False
    customized_order: bool = False
    specific_work: bool = False
    standard_product: bool = False
    ownership_transfer: bool = False
    contract_invalid: bool = False
    completion_date: Optional[date] = None
    third_party_tort: bool = False
    main_work_subcontract: bool = False
    total_subcontract: bool = False
    disassembled_subcontract: bool = False
    auxiliary_subcontract: bool = False
    customer_consent: bool = False
    customer_assistance_missing: bool = False
    urged_assistance: bool = False
    assistance_overdue: bool = False
    customer_change_request: bool = False
    workload_increased: bool = False
    contractor_loss: float = 0.0
    unpaid_remuneration: bool = False
    lien_claim: bool = False
    improper_lien: bool = False
    customer_material_defect: bool = False
    contractor_inspected_notice: bool = False
    contractor_no_inspection_notice: bool = False
    defect_caused_by_customer_material: bool = False
    custody_damage: bool = False
    proper_custody: bool = False
    improper_custody: bool = False
    result_delivered: bool = False
    not_delivered: bool = False
    customer_termination: bool = False
    termination_after_completion: bool = False
    near_completion: bool = False
    substantial_cost_invested: bool = False
    delay_delivery: bool = False
    quality_defect: bool = False
    quality_conform: bool = False
    contract_quality_standard: bool = False
    sample_drawing: bool = False
    industry_standard: bool = False
    customer_knew_and_accepted: bool = False
    minor_defect: bool = False
    serious_defect: bool = False
    worthless_defect: bool = False
    repair_requested: bool = False
    remake_requested: bool = False
    reduce_pay_requested: bool = False
    compensation_requested: bool = False
    contractor_refuses_repair: bool = False
    remuneration_amount: float = 0.0
    actual_loss: float = 0.0
    delay_loss: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "work_contract": self.work_contract,
            "contract_nature_dispute": self.contract_nature_dispute,
            "named_sale_contract": self.named_sale_contract,
            "named_work_contract": self.named_work_contract,
            "customized_order": self.customized_order,
            "specific_work": self.specific_work,
            "standard_product": self.standard_product,
            "ownership_transfer": self.ownership_transfer,
            "contract_invalid": self.contract_invalid,
            "completion_date": self.completion_date.isoformat() if self.completion_date else None,
            "third_party_tort": self.third_party_tort,
            "main_work_subcontract": self.main_work_subcontract,
            "total_subcontract": self.total_subcontract,
            "disassembled_subcontract": self.disassembled_subcontract,
            "auxiliary_subcontract": self.auxiliary_subcontract,
            "customer_consent": self.customer_consent,
            "customer_assistance_missing": self.customer_assistance_missing,
            "urged_assistance": self.urged_assistance,
            "assistance_overdue": self.assistance_overdue,
            "customer_change_request": self.customer_change_request,
            "workload_increased": self.workload_increased,
            "contractor_loss": self.contractor_loss,
            "unpaid_remuneration": self.unpaid_remuneration,
            "lien_claim": self.lien_claim,
            "improper_lien": self.improper_lien,
            "customer_material_defect": self.customer_material_defect,
            "contractor_inspected_notice": self.contractor_inspected_notice,
            "contractor_no_inspection_notice": self.contractor_no_inspection_notice,
            "defect_caused_by_customer_material": self.defect_caused_by_customer_material,
            "custody_damage": self.custody_damage,
            "proper_custody": self.proper_custody,
            "improper_custody": self.improper_custody,
            "result_delivered": self.result_delivered,
            "not_delivered": self.not_delivered,
            "customer_termination": self.customer_termination,
            "termination_after_completion": self.termination_after_completion,
            "near_completion": self.near_completion,
            "substantial_cost_invested": self.substantial_cost_invested,
            "delay_delivery": self.delay_delivery,
            "quality_defect": self.quality_defect,
            "quality_conform": self.quality_conform,
            "contract_quality_standard": self.contract_quality_standard,
            "sample_drawing": self.sample_drawing,
            "industry_standard": self.industry_standard,
            "customer_knew_and_accepted": self.customer_knew_and_accepted,
            "minor_defect": self.minor_defect,
            "serious_defect": self.serious_defect,
            "worthless_defect": self.worthless_defect,
            "repair_requested": self.repair_requested,
            "remake_requested": self.remake_requested,
            "reduce_pay_requested": self.reduce_pay_requested,
            "compensation_requested": self.compensation_requested,
            "contractor_refuses_repair": self.contractor_refuses_repair,
            "remuneration_amount": self.remuneration_amount,
            "actual_loss": self.actual_loss,
            "delay_loss": self.delay_loss,
            "notes": self.notes,
        }


def _format_work_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: WorkContractFacts,
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


def extract_work_contract_facts(case_text: str) -> WorkContractFacts:
    config = get_work_contract_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = WorkContractFacts(raw_text=raw_text)

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.work_contract = _mentions(text, config.get_terms("work_contract"))
    facts.contract_nature_dispute = _mentions(text, config.get_terms("contract_nature_dispute"))
    facts.named_sale_contract = _mentions(text, config.get_terms("named_sale_contract"))
    facts.named_work_contract = _mentions(text, config.get_terms("named_work_contract"))
    facts.customized_order = _mentions(text, config.get_terms("customized_order"))
    facts.specific_work = _mentions(text, config.get_terms("specific_work"))
    facts.standard_product = _mentions(text, config.get_terms("standard_product"))
    facts.ownership_transfer = _mentions(text, config.get_terms("ownership_transfer"))
    facts.contract_invalid = _mentions(text, config.get_terms("contract_invalid"))
    facts.completion_date = _parse_date(text, config.get_terms("completion_date"))
    facts.third_party_tort = _mentions(text, config.get_terms("third_party_tort"))

    facts.main_work_subcontract = _mentions(text, config.get_terms("main_work_subcontract"))
    facts.total_subcontract = _mentions(text, config.get_terms("total_subcontract"))
    facts.disassembled_subcontract = _mentions(text, config.get_terms("disassembled_subcontract"))
    facts.main_work_subcontract = facts.main_work_subcontract or facts.total_subcontract or facts.disassembled_subcontract
    facts.auxiliary_subcontract = _mentions(text, config.get_terms("auxiliary_subcontract"))
    facts.customer_consent = _mentions(text, config.get_terms("customer_consent"))
    facts.customer_assistance_missing = _mentions(text, config.get_terms("customer_assistance_missing"))
    facts.urged_assistance = _mentions(text, config.get_terms("urged_assistance"))
    facts.assistance_overdue = _mentions(text, config.get_terms("assistance_overdue"))
    facts.customer_change_request = _mentions(text, config.get_terms("customer_change_request"))
    facts.workload_increased = _mentions(text, config.get_terms("workload_increased"))
    facts.contractor_loss = _extract_money_near(text, config.get_terms("contractor_loss"))

    facts.unpaid_remuneration = _mentions(text, config.get_terms("unpaid_remuneration"))
    facts.lien_claim = _mentions(text, config.get_terms("lien"))
    facts.improper_lien = _mentions(text, config.get_terms("improper_lien"))
    facts.customer_material_defect = _mentions(text, config.get_terms("customer_material_defect"))
    facts.contractor_inspected_notice = _mentions(text, config.get_terms("contractor_inspected_notice"))
    facts.contractor_no_inspection_notice = _mentions(text, config.get_terms("contractor_no_inspection_notice"))
    facts.defect_caused_by_customer_material = _mentions(text, config.get_terms("defect_caused_by_customer_material"))
    facts.custody_damage = _mentions(text, config.get_terms("custody_damage"))
    facts.proper_custody = _mentions(text, config.get_terms("proper_custody"))
    facts.improper_custody = _mentions(text, config.get_terms("improper_custody"))

    facts.result_delivered = _mentions(text, config.get_terms("result_delivered"))
    facts.not_delivered = _mentions(text, config.get_terms("not_delivered"))
    facts.customer_termination = _mentions(text, config.get_terms("customer_termination"))
    facts.termination_after_completion = _mentions(text, config.get_terms("termination_after_completion"))
    facts.near_completion = _mentions(text, config.get_terms("near_completion"))
    facts.substantial_cost_invested = _mentions(text, config.get_terms("substantial_cost_invested"))
    facts.delay_delivery = _mentions(text, config.get_terms("delay_delivery"))
    facts.quality_defect = _mentions(text, config.get_terms("quality_defect"))
    facts.quality_conform = _mentions(text, config.get_terms("quality_conform"))
    facts.contract_quality_standard = _mentions(text, config.get_terms("contract_quality_standard"))
    facts.sample_drawing = _mentions(text, config.get_terms("sample_drawing"))
    facts.industry_standard = _mentions(text, config.get_terms("industry_standard"))
    facts.customer_knew_and_accepted = _mentions(text, config.get_terms("customer_knew_and_accepted"))
    facts.minor_defect = _mentions(text, config.get_terms("minor_defect"))
    facts.serious_defect = _mentions(text, config.get_terms("serious_defect"))
    facts.worthless_defect = _mentions(text, config.get_terms("worthless_defect"))
    facts.repair_requested = _mentions(text, config.get_terms("repair_requested"))
    facts.remake_requested = _mentions(text, config.get_terms("remake_requested"))
    facts.reduce_pay_requested = _mentions(text, config.get_terms("reduce_pay_requested"))
    facts.compensation_requested = _mentions(text, config.get_terms("compensation_requested"))
    facts.contractor_refuses_repair = _mentions(text, config.get_terms("contractor_refuses_repair"))
    facts.remuneration_amount = _extract_money_near(text, config.get_terms("remuneration_amount"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))
    facts.delay_loss = _extract_money_near(text, config.get_terms("delay_loss"))
    return facts


def _procedure_findings(facts: WorkContractFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("承揽合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告为承揽人；可结合签约承揽人和实际完成人的履行情况确定")
    return findings


def _only_procedure_question(facts: WorkContractFacts) -> bool:
    return (
        (facts.asks_jurisdiction or facts.asks_defendant)
        and not facts.contract_nature_dispute
        and not facts.contract_invalid
        and not facts.main_work_subcontract
        and not facts.auxiliary_subcontract
        and not facts.customer_assistance_missing
        and not facts.customer_change_request
        and not facts.unpaid_remuneration
        and not facts.lien_claim
        and not facts.customer_material_defect
        and not facts.custody_damage
        and not facts.customer_termination
        and not facts.delay_delivery
        and not facts.quality_defect
        and not facts.quality_conform
    )


def _has_work_performance_dispute(facts: WorkContractFacts) -> bool:
    return any(
        (
            facts.contract_nature_dispute,
            facts.contract_invalid,
            facts.main_work_subcontract,
            facts.auxiliary_subcontract,
            facts.customer_assistance_missing,
            facts.customer_change_request,
            facts.unpaid_remuneration,
            facts.lien_claim,
            facts.customer_material_defect,
            facts.custody_damage,
            facts.result_delivered,
            facts.not_delivered,
            facts.customer_termination,
            facts.delay_delivery,
            facts.quality_defect,
            facts.quality_conform,
        )
    )


def _quality_standard(facts: WorkContractFacts) -> str:
    if facts.contract_quality_standard:
        return "合同约定标准"
    if facts.sample_drawing:
        return "样品或图纸标准"
    if facts.industry_standard:
        return "行业或通常标准"
    return "符合合同目的的通常标准"


def _selected_remedy(facts: WorkContractFacts) -> str:
    if facts.repair_requested:
        return "修理"
    if facts.remake_requested:
        return "重作"
    if facts.reduce_pay_requested:
        return "减少报酬"
    if facts.compensation_requested:
        return "赔偿损失"
    if facts.worthless_defect:
        return "解除合同并赔偿损失"
    if facts.serious_defect:
        return "重作或赔偿损失"
    return "修理"


def _quality_remedy_conclusion(facts: WorkContractFacts) -> str:
    if facts.customer_knew_and_accepted:
        return "工作成果质量视为定作人认可，瑕疵抗辩不成立；定作人应支付相应报酬。"

    if facts.contractor_refuses_repair:
        if facts.actual_loss > 0:
            return f"承揽人明确拒绝修理或重作，定作人可以直接请求减少报酬或赔偿损失；已识别损失为 {facts.actual_loss:.2f} 元。"
        return "承揽人明确拒绝修理或重作，定作人可以直接请求减少报酬或赔偿损失。"

    if facts.worthless_defect:
        if facts.actual_loss > 0:
            return f"工作成果完全无价值，定作人可以解除合同，并要求承揽人赔偿全部损失 {facts.actual_loss:.2f} 元。"
        return "工作成果完全无价值，定作人可以解除合同，并要求承揽人赔偿全部损失。"

    remedy = _selected_remedy(facts)
    if remedy == "修理":
        return "定作人合理选择修理，承揽人应负责修复瑕疵并承担修复费用；修理仍不合格的，定作人可再要求减少报酬或赔偿损失。"
    if remedy == "重作":
        return "定作人合理选择重作，承揽人应重新完成工作，原不合格成果按实际情况处理，重作费用由承揽人承担。"
    if remedy == "减少报酬":
        amount_text = f"；涉及报酬 {facts.remuneration_amount:.2f} 元的，应按瑕疵程度相应扣减" if facts.remuneration_amount > 0 else ""
        return f"定作人合理选择减少报酬，承揽人应按瑕疵程度承担报酬扣减责任{amount_text}。"
    if remedy == "赔偿损失":
        amount_text = f" {facts.actual_loss:.2f} 元" if facts.actual_loss > 0 else ""
        return f"定作人合理选择赔偿损失，承揽人应赔偿因质量瑕疵造成的损失{amount_text}。"
    return "定作人可在重作、减少报酬、赔偿损失之间合理选择，承揽人应承担相应违约责任。"


def adjudicate_work_contract(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_work_contract_config()
    facts = extract_work_contract_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "承揽合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出质量瑕疵、报酬、交付、材料、保管、转包或解除事实。"
        conclusion = "；".join(procedure_findings)
        return _format_work_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.contract_nature_dispute or (
        (facts.named_sale_contract or facts.named_work_contract)
        and (facts.customized_order or facts.specific_work or facts.standard_product or facts.ownership_transfer)
    ):
        triggered.append(config.patch_name("C7", "承揽/买卖合同定性争议"))
        major = "合同性质应根据实质内容认定，而不是只看合同名称。买卖合同以转移标的物所有权为主要目的，承揽合同以按照定作人要求完成特定工作并交付工作成果为主要目的。"
        if facts.standard_product and facts.ownership_transfer and not facts.specific_work:
            minor = "识别到合同虽存在定作或加工表述，但交易核心是交付标准化产品并转移所有权，未稳定识别承揽人完成特定工作的内容。"
            conclusion = "根据合同实质内容，倾向认定为买卖合同；不适用本承揽合同裁判引擎，应按买卖合同规则审查违约责任、解除权和赔偿范围。"
        elif facts.specific_work or (facts.customized_order and not facts.standard_product):
            minor = "识别到合同名称与实质内容存在争议，但交易核心是承揽人按照定作人要求完成特定工作并交付工作成果。"
            conclusion = "根据合同实质内容，倾向认定为承揽合同；应继续按工作成果质量、交付、报酬、材料和解除规则审查。"
        else:
            minor = "识别到合同名称与实质内容可能不一致，但现有事实不足以判断交易目的究竟是转移所有权还是完成特定工作。"
            conclusion = "需根据合同实质内容进一步定性：以转移标准化产品所有权为主的，按买卖合同处理；以完成特定工作为主的，按承揽合同处理。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "合同类型识别"], procedure_findings)

    if facts.third_party_tort and not _has_work_performance_dispute(facts):
        major = "承揽合同裁判引擎处理承揽合同项下工作成果、报酬、材料、保管、转包和解除争议；单纯第三方侵权应按侵权责任另行处理。"
        minor = "识别到争议核心是第三方侵权，未识别到承揽合同履行争议。"
        conclusion = "本案涉及侵权责任，非承揽合同纠纷，不适用本承揽合同裁判引擎"
        return _format_work_output(major, minor, conclusion, [], facts, path, procedure_findings)

    if facts.completion_date and _years_between(facts.completion_date, today) > 3:
        major = "承揽合同纠纷适用三年一般诉讼时效；法律另有规定的，从其规定。"
        minor = f"识别到交付、完工或验收日期为{facts.completion_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求"
        return _format_work_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    path.append("前置实体判断")
    if facts.contract_invalid:
        major = "《民法典》第770条规定，承揽合同是承揽人按照定作人要求完成工作、交付工作成果，定作人支付报酬的合同；合同无效的，按无效合同后果处理。"
        minor = "识别到承揽合同无效或合同未成立事实。"
        conclusion = "承揽合同无效，已取得的报酬、材料或工作成果应依法返还；因此造成损失的，按过错承担赔偿责任。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.main_work_subcontract or facts.auxiliary_subcontract:
        triggered.append(config.patch_name("C6", "转包/分包的效力"))
        major = "《民法典》第772条、第773条规定，承揽人应以自己的设备、技术和劳力完成主要工作；主要工作交由第三人完成的，应经定作人同意，辅助工作可由第三人完成，但承揽人仍对工作成果负责。"
        if facts.total_subcontract or facts.disassembled_subcontract:
            triggered.append(config.patch_name("C9", "违法分包/转包"))
            major = "《民法典》第772条规定，承揽人将其承揽的主要工作交由第三人完成的，应当就第三人完成的工作成果向定作人负责；未经定作人同意的，定作人可以解除合同。"
            if facts.customer_consent:
                minor = "识别到承揽人将全部工作或主要工作拆分后交由第三人完成，但已经定作人同意。"
                conclusion = "经定作人同意的转包有效，但承揽人仍应对第三人完成的工作成果向定作人负责。"
            elif facts.quality_defect:
                minor = "识别到承揽人未经定作人同意，将全部工作转包或将主要工作肢解后分别转包，并导致工作成果出现质量问题。"
                conclusion = "未经同意违法转包，定作人可以解除合同；违法转包导致工作成果质量问题的，承揽人承担全部责任。"
            else:
                minor = "识别到承揽人未经定作人同意，将全部工作转包或将主要工作肢解后分别转包。"
                conclusion = "未经同意违法转包，定作人可以解除合同；承揽人仍应对第三人完成的工作成果向定作人负责。"
        elif facts.main_work_subcontract and facts.customer_consent:
            minor = "识别到承揽人将主要工作交由第三人完成，且已经定作人同意。"
            conclusion = "主要工作转包有效，但承揽人仍应对第三人完成的工作成果向定作人负责。"
        elif facts.main_work_subcontract:
            minor = "识别到承揽人未经定作人同意，将主要工作交由第三人完成。"
            conclusion = "主要工作未经定作人同意转包，定作人可以解除合同；承揽人仍应对已完成成果及因此造成的损失承担责任。"
        else:
            minor = "识别到承揽人将辅助工作交由第三人完成。"
            conclusion = "辅助工作转包有效，但承揽人应对第三人完成的工作成果向定作人负责。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "承揽人亲自完成义务审查"], procedure_findings)

    if facts.customer_assistance_missing:
        major = "《民法典》第778条规定，定作人不履行协助义务致使承揽工作不能完成的，承揽人可以催告定作人在合理期限内履行，并可以顺延履行期限；定作人逾期不履行的，承揽人可以解除合同。"
        if facts.urged_assistance and facts.assistance_overdue:
            minor = "识别到定作人未履行协助义务，承揽人已经催告，定作人逾期仍未履行。"
            conclusion = "定作人逾期不履行协助义务，承揽人可以解除合同，并可主张因此受到的损失。"
        elif facts.urged_assistance:
            minor = "识别到定作人未履行协助义务，承揽人已经催告。"
            conclusion = "承揽人可以顺延履行期限；定作人仍不履行的，承揽人可以解除合同。"
        else:
            minor = "识别到定作人未提供图纸、资料、场地或其他必要协助。"
            conclusion = "承揽人应催告定作人在合理期限内履行协助义务，并可以顺延履行期限。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "定作人协助义务审查"], procedure_findings)

    if facts.customer_change_request:
        major = "《民法典》第777条规定，定作人中途变更承揽工作的要求，造成承揽人损失的，应当赔偿损失。"
        minor = "识别到定作人中途变更设计、规格、图纸、尺寸或其他承揽要求。"
        if facts.contractor_loss > 0:
            conclusion = f"定作人中途变更承揽要求有效，但应赔偿承揽人损失 {facts.contractor_loss:.2f} 元。"
        elif facts.workload_increased:
            conclusion = "定作人中途变更导致工作量或成本增加的，应相应增加报酬或赔偿承揽人实际损失。"
        else:
            conclusion = "定作人可以中途变更承揽要求，但因此造成承揽人损失的，应当赔偿。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "定作人变更要求审查"], procedure_findings)

    if facts.customer_material_defect:
        triggered.append(config.patch_name("C4", "定作人提供的材料瑕疵"))
        major = "《民法典》第775条规定，定作人提供材料的，应按约定提供；承揽人对定作人提供的材料应及时检验，发现不符合约定时，应及时通知定作人更换、补齐或采取其他补救措施。"
        if facts.contractor_no_inspection_notice:
            minor = "识别到定作人提供的材料不符合约定，但承揽人未及时检验或未及时通知。"
            conclusion = "材料瑕疵责任由承揽人承担相应责任。"
        elif facts.contractor_inspected_notice:
            minor = "识别到定作人提供的材料不符合约定，承揽人已经及时检验并通知定作人更换或补齐。"
            conclusion = "材料瑕疵责任由定作人承担；定作人应更换、补齐或采取补救措施。"
        elif facts.defect_caused_by_customer_material:
            minor = "识别到工作成果瑕疵由定作人提供材料瑕疵导致。"
            conclusion = "材料瑕疵责任由定作人承担；承揽人不承担由材料瑕疵造成的工作成果质量责任。"
        else:
            minor = "识别到定作人提供的材料存在瑕疵，但未稳定识别承揽人是否及时检验并通知。"
            conclusion = "需审查承揽人是否及时检验并通知；已检验并通知的由定作人承担，未检验或未通知的由承揽人承担相应责任。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "定作人提供材料瑕疵"], procedure_findings)

    if facts.custody_damage:
        triggered.append(config.patch_name("C5", "承揽人保管义务"))
        major = "《民法典》第784条规定，承揽人应当妥善保管定作人提供的材料以及完成的工作成果，因保管不善造成毁损、灭失的，应当承担赔偿责任。"
        amount_text = f" {facts.actual_loss:.2f} 元" if facts.actual_loss > 0 else ""
        if facts.improper_custody:
            minor = "识别到定作人提供的材料或已完成工作成果在承揽人保管期间毁损、灭失，且承揽人存在保管不善事实。"
            conclusion = f"承揽人保管未尽到妥善保管义务，承担赔偿责任{amount_text}。"
        elif facts.proper_custody:
            minor = "识别到材料或工作成果在承揽人保管期间毁损、灭失，但承揽人已尽到合理保管义务。"
            conclusion = "承揽人保管已尽到妥善保管义务，不承担赔偿责任。"
        else:
            minor = "识别到材料或工作成果在承揽人保管期间毁损、灭失，但未稳定识别保管是否妥善。"
            conclusion = "需审查承揽人是否尽到妥善保管义务；保管不善的，承揽人承担赔偿责任。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "承揽人保管义务"], procedure_findings)

    if facts.lien_claim:
        major = "《民法典》第783条规定，定作人未向承揽人支付报酬或者材料费等价款的，承揽人对完成的工作成果享有留置权或者有权拒绝交付。"
        if facts.improper_lien:
            minor = "识别到定作人未支付报酬或材料费，但承揽人存在超额留置、扣留全部成果或其他不当行使留置权的事实。"
            conclusion = "承揽人享有留置权但行使不当；因不当留置造成定作人损失的，承揽人应承担赔偿责任。"
        elif facts.unpaid_remuneration:
            minor = "识别到定作人未支付报酬、加工费或材料费等价款。"
            conclusion = "承揽人对完成的工作成果享有留置权或者有权拒绝交付。"
        else:
            minor = "识别到承揽人主张留置或拒绝交付，但未稳定识别到定作人未支付报酬或材料费。"
            conclusion = "承揽人留置权是否成立需补充定作人是否到期未支付报酬、加工费或材料费等事实。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "承揽人留置权"], procedure_findings)

    path.append("核心争议树")
    if facts.customer_termination and facts.termination_after_completion:
        triggered.append(config.patch_name("C3", "定作人任意解除权"))
        triggered.append(config.patch_name("C8", "定作人任意解除权的行使边界"))
        major = "《民法典》第787条规定，定作人在承揽人完成工作前可以随时解除合同；该解除权必须在工作完成前行使，工作完成后不再适用任意解除权。"
        minor = "识别到定作人在承揽人已经完成工作或交付工作成果后主张任意解除。"
        conclusion = "定作人任意解除权不成立；工作完成后不得再按第787条随时解除合同。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "工作成果交付状态"], procedure_findings)

    if facts.not_delivered:
        if facts.customer_termination:
            triggered.append(config.patch_name("C3", "定作人任意解除权"))
            major = "《民法典》第787条规定，定作人在承揽人完成工作前可以随时解除合同，造成承揽人损失的，应当赔偿损失。"
            if facts.termination_after_completion:
                minor = "识别到定作人在工作完成或交付后主张任意解除。"
                conclusion = "定作人任意解除权不成立；工作完成后不得再按第787条随时解除合同。"
            elif facts.near_completion or facts.substantial_cost_invested:
                triggered.append(config.patch_name("C8", "定作人任意解除权的行使边界"))
                major = "《民法典》第787条规定，定作人在承揽人完成工作前可以随时解除合同；但解除权行使应受诚信原则限制，不能造成明显不公平或权利滥用。"
                minor = "识别到工作虽尚未完成，但已经接近完成，或承揽人已投入绝大部分成本。"
                if facts.contractor_loss > 0:
                    conclusion = f"定作人任意解除权行使可能受限；如解除被支持，定作人仍应赔偿承揽人实际损失 {facts.contractor_loss:.2f} 元。"
                else:
                    conclusion = "定作人任意解除权行使可能受诚信原则限制；如解除被支持，仍应赔偿承揽人已投入成本、人工费和合理利润等实际损失。"
            else:
                minor = "识别到承揽人尚未完成或尚未交付工作成果，定作人要求解除合同。"
                if facts.contractor_loss > 0:
                    conclusion = f"定作人任意解除权成立，解除有效，应赔偿承揽人损失 {facts.contractor_loss:.2f} 元。"
                else:
                    conclusion = "定作人任意解除权成立，解除有效；定作人应赔偿承揽人已投入材料费、人工费、合理利润等实际损失。"
            return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "工作成果交付状态"], procedure_findings)

        if facts.delay_delivery:
            major = "承揽人应按照约定或合理期限完成工作并交付工作成果；逾期交付造成损失的，应承担违约责任。"
            minor = "识别到承揽人尚未交付或逾期交付工作成果。"
            if facts.delay_loss > 0:
                conclusion = f"承揽人构成迟延交付，应赔偿因此造成的损失 {facts.delay_loss:.2f} 元。"
            else:
                conclusion = "承揽人构成迟延交付；定作人需证明因迟延遭受的具体损失后主张赔偿。"
            return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "迟延交付"], procedure_findings)

        major = "承揽合同以承揽人完成工作并交付工作成果为核心；尚未交付的，应先审查履行期限、任意解除和迟延责任。"
        minor = "识别到工作成果尚未交付，但未稳定识别定作人解除或迟延损失事实。"
        conclusion = "事实要素不足，需补充工作是否完成、是否逾期、定作人是否解除以及承揽人损失后再裁判。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "工作成果交付状态"], procedure_findings)

    if facts.quality_defect:
        triggered.append(config.patch_name("C1", "质量瑕疵认定标准"))
        standard = _quality_standard(facts)
        major = "《民法典》第781条规定，承揽人交付的工作成果不符合质量要求的，定作人可以合理选择请求承揽人承担修理、重作、减少报酬、赔偿损失等违约责任。"
        minor = f"识别到承揽人已交付或应交付工作成果，定作人主张工作成果存在质量瑕疵；质量标准按{standard}判断。"
        if facts.customer_knew_and_accepted:
            conclusion = "工作成果质量视为定作人认可，瑕疵抗辩不成立；定作人应支付相应报酬。"
            return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "质量是否符合要求"], procedure_findings)

        triggered.append(config.patch_name("C2", "定作人救济方式的选择权"))
        if facts.worthless_defect:
            minor += "瑕疵导致工作成果完全无价值。"
        elif facts.serious_defect:
            minor += "瑕疵严重，无法修复或修复成本过高。"
        elif facts.minor_defect:
            minor += "瑕疵轻微且可以修复。"
        else:
            minor += "瑕疵程度需结合是否可修复、修复成本和对合同目的的影响判断。"
        conclusion = _quality_remedy_conclusion(facts)
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "质量是否符合要求", "救济方式选择"], procedure_findings)

    if facts.result_delivered and (facts.quality_conform or facts.unpaid_remuneration):
        major = "《民法典》第782条规定，定作人应当向承揽人支付报酬；对支付期限没有约定或约定不明确的，定作人应当在承揽人交付工作成果时支付，工作成果部分交付的，应相应支付。"
        minor = "识别到承揽人已经交付工作成果，且未识别到成立的质量瑕疵抗辩。"
        if facts.remuneration_amount > 0:
            conclusion = f"定作人应支付报酬 {facts.remuneration_amount:.2f} 元。"
        else:
            conclusion = "定作人应全额支付报酬。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "报酬支付"], procedure_findings)

    if facts.delay_delivery:
        major = "承揽人应按照约定或合理期限完成工作并交付工作成果；逾期交付造成损失的，应承担违约责任。"
        minor = "识别到承揽人迟延交付、逾期完工或未按期交付工作成果。"
        if facts.delay_loss > 0:
            conclusion = f"承揽人构成迟延交付，应赔偿因此造成的损失 {facts.delay_loss:.2f} 元。"
        else:
            conclusion = "承揽人构成迟延交付；定作人需证明因迟延遭受的具体损失后主张赔偿。"
        return _format_work_output(major, minor, conclusion, triggered, facts, [*path, "迟延交付"], procedure_findings)

    if facts.work_contract:
        major = "《民法典》第770条规定，承揽合同的核心是承揽人完成工作、交付工作成果，定作人支付报酬。"
        minor = "已识别承揽合同关系，但未稳定识别质量瑕疵、交付状态、报酬、材料、保管、转包或解除等具体争议事实。"
        conclusion = "事实要素不足，需补充工作成果是否交付、质量是否合格、瑕疵程度、救济方式、报酬支付或材料保管事实后再裁判"
        return _format_work_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "承揽合同纠纷应围绕工作成果是否符合质量要求、定作人可选择何种救济方式、报酬是否应支付以及材料保管责任进行审查。"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的承揽合同关键事实。"
    conclusion = "事实要素不足，需补充承揽合同关系、工作成果、质量标准、瑕疵程度和损失金额后再裁判"
    return _format_work_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
