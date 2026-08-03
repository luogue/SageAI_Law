"""Construction-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import _format_output, _mentions, _parse_date, _years_between
from adjudicate.construction_configs import get_construction_config


@dataclass
class ConstructionFacts:
    raw_text: str
    contract_type: str = "construction"
    contract_type_name: str = "建设工程合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    construction_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    survey_contract: bool = False
    design_contract: bool = False
    construction_work_contract: bool = False
    contract_invalid: bool = False
    qualification_defect: bool = False
    qualification_before_completion: bool = False
    affiliation: bool = False
    tender_illegal: bool = False
    planning_missing: bool = False
    planning_obtained_before_suit: bool = False
    illegal_subcontract: bool = False
    black_white_contract: bool = False
    substantive_inconsistency: bool = False
    labor_subcontract: bool = False
    labor_qualification: bool = False
    project_accepted: bool = False
    project_unaccepted: bool = False
    repairable: bool = False
    unrepairable: bool = False
    developer_fault: bool = False
    project_price: float = 0.0
    repair_cost: float = 0.0
    period_dispute: bool = False
    start_notice: bool = False
    conditions_missing: bool = False
    actual_entry: bool = False
    completion_accepted: bool = False
    delay_acceptance: bool = False
    report_submitted: bool = False
    unauthorized_use: bool = False
    quality_defect: bool = False
    quality_deposit_return: bool = False
    deposit_period_due: bool = False
    no_deposit_period: bool = False
    hidden_work: bool = False
    contractor_notified_inspection: bool = False
    developer_no_inspection: bool = False
    unpaid_project_price: bool = False
    payment_urged: bool = False
    priority_claim: bool = False
    within_18_months: bool = False
    beyond_18_months: bool = False
    mortgage_conflict: bool = False
    worker_interest_harmed: bool = False
    actual_constructor: bool = False
    direct_sue_employer: bool = False
    subrogation_claim: bool = False
    amount_owed_by_employer: float = 0.0
    termination_request: bool = False
    employer_termination: bool = False
    contractor_termination: bool = False
    employer_assistance_breach: bool = False
    urged_unperformed: bool = False
    completed_quality_ok: bool = False
    completed_quality_bad: bool = False
    stoppage_loss: bool = False
    employer_material_delay: bool = False
    actual_loss: float = 0.0
    interest_claim: bool = False
    agreed_interest: bool = False
    lpr_interest: bool = False
    project_delivered: bool = False
    settlement_submitted: bool = False
    lawsuit_filed: bool = False
    interest_amount: float = 0.0
    quality_deposit_amount: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "construction_contract": self.construction_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "survey_contract": self.survey_contract,
            "design_contract": self.design_contract,
            "construction_work_contract": self.construction_work_contract,
            "contract_invalid": self.contract_invalid,
            "qualification_defect": self.qualification_defect,
            "qualification_before_completion": self.qualification_before_completion,
            "affiliation": self.affiliation,
            "tender_illegal": self.tender_illegal,
            "planning_missing": self.planning_missing,
            "planning_obtained_before_suit": self.planning_obtained_before_suit,
            "illegal_subcontract": self.illegal_subcontract,
            "black_white_contract": self.black_white_contract,
            "substantive_inconsistency": self.substantive_inconsistency,
            "labor_subcontract": self.labor_subcontract,
            "labor_qualification": self.labor_qualification,
            "project_accepted": self.project_accepted,
            "project_unaccepted": self.project_unaccepted,
            "repairable": self.repairable,
            "unrepairable": self.unrepairable,
            "developer_fault": self.developer_fault,
            "project_price": self.project_price,
            "repair_cost": self.repair_cost,
            "period_dispute": self.period_dispute,
            "start_notice": self.start_notice,
            "conditions_missing": self.conditions_missing,
            "actual_entry": self.actual_entry,
            "completion_accepted": self.completion_accepted,
            "delay_acceptance": self.delay_acceptance,
            "report_submitted": self.report_submitted,
            "unauthorized_use": self.unauthorized_use,
            "quality_defect": self.quality_defect,
            "quality_deposit_return": self.quality_deposit_return,
            "deposit_period_due": self.deposit_period_due,
            "no_deposit_period": self.no_deposit_period,
            "hidden_work": self.hidden_work,
            "contractor_notified_inspection": self.contractor_notified_inspection,
            "developer_no_inspection": self.developer_no_inspection,
            "unpaid_project_price": self.unpaid_project_price,
            "payment_urged": self.payment_urged,
            "priority_claim": self.priority_claim,
            "within_18_months": self.within_18_months,
            "beyond_18_months": self.beyond_18_months,
            "mortgage_conflict": self.mortgage_conflict,
            "worker_interest_harmed": self.worker_interest_harmed,
            "actual_constructor": self.actual_constructor,
            "direct_sue_employer": self.direct_sue_employer,
            "subrogation_claim": self.subrogation_claim,
            "amount_owed_by_employer": self.amount_owed_by_employer,
            "termination_request": self.termination_request,
            "employer_termination": self.employer_termination,
            "contractor_termination": self.contractor_termination,
            "employer_assistance_breach": self.employer_assistance_breach,
            "urged_unperformed": self.urged_unperformed,
            "completed_quality_ok": self.completed_quality_ok,
            "completed_quality_bad": self.completed_quality_bad,
            "stoppage_loss": self.stoppage_loss,
            "employer_material_delay": self.employer_material_delay,
            "actual_loss": self.actual_loss,
            "interest_claim": self.interest_claim,
            "agreed_interest": self.agreed_interest,
            "lpr_interest": self.lpr_interest,
            "project_delivered": self.project_delivered,
            "settlement_submitted": self.settlement_submitted,
            "lawsuit_filed": self.lawsuit_filed,
            "interest_amount": self.interest_amount,
            "quality_deposit_amount": self.quality_deposit_amount,
            "notes": self.notes,
        }


def _format_construction_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: ConstructionFacts,
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
            after = text[match.end():min(len(text), match.end() + 20)]
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


def extract_construction_facts(case_text: str) -> ConstructionFacts:
    config = get_construction_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = ConstructionFacts(raw_text=raw_text)

    for field_name in (
        "construction_contract", "third_party_tort", "survey_contract", "design_contract",
        "construction_work_contract", "contract_invalid", "qualification_defect",
        "qualification_before_completion", "affiliation", "tender_illegal",
        "planning_missing", "planning_obtained_before_suit", "illegal_subcontract",
        "black_white_contract", "substantive_inconsistency", "labor_subcontract",
        "labor_qualification", "project_accepted", "project_unaccepted", "repairable",
        "unrepairable", "developer_fault", "period_dispute", "start_notice",
        "conditions_missing", "actual_entry", "completion_accepted", "delay_acceptance",
        "report_submitted", "unauthorized_use", "quality_defect", "quality_deposit_return",
        "deposit_period_due", "no_deposit_period", "hidden_work",
        "contractor_notified_inspection", "developer_no_inspection", "unpaid_project_price",
        "payment_urged", "priority_claim", "within_18_months", "beyond_18_months",
        "mortgage_conflict", "worker_interest_harmed", "actual_constructor",
        "direct_sue_employer", "subrogation_claim", "termination_request",
        "employer_termination", "contractor_termination", "employer_assistance_breach",
        "urged_unperformed", "completed_quality_ok", "completed_quality_bad",
        "stoppage_loss", "employer_material_delay", "interest_claim", "agreed_interest",
        "lpr_interest", "project_delivered", "settlement_submitted", "lawsuit_filed",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.project_price = _extract_money_near(text, config.get_terms("project_price"))
    facts.repair_cost = _extract_money_near(text, config.get_terms("repair_cost"))
    facts.amount_owed_by_employer = _extract_money_near(text, config.get_terms("amount_owed_by_employer"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))
    facts.interest_amount = _extract_money_near(text, config.get_terms("interest_amount"))
    facts.quality_deposit_amount = _extract_money_near(text, config.get_terms("quality_deposit_amount"))

    if any(term in text for term in ("验收不合格", "工程验收不合格", "工程质量不合格", "竣工验收不合格")):
        facts.project_unaccepted = True
    if any(term in text for term in ("修复后仍不合格", "不可修复", "无法修复")):
        facts.unrepairable = True
    if "无资质" in text or "没有施工资质" in text:
        facts.qualification_defect = True

    if any(
        (
            facts.survey_contract, facts.design_contract, facts.construction_work_contract,
            facts.qualification_defect, facts.affiliation, facts.tender_illegal,
            facts.planning_missing, facts.illegal_subcontract, facts.black_white_contract,
            facts.project_accepted, facts.project_unaccepted, facts.unpaid_project_price,
            facts.priority_claim, facts.actual_constructor, facts.termination_request,
        )
    ):
        facts.construction_contract = True
    if facts.qualification_defect or facts.affiliation or facts.tender_illegal or facts.planning_missing or facts.illegal_subcontract:
        facts.contract_invalid = True
    return facts


def _procedure_findings(facts: ConstructionFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("建设工程合同纠纷一般由被告住所地或者合同履行地人民法院处理，合同履行地通常与建设工程所在地密切相关；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告应结合争议确定：工程款争议通常列发包人，质量争议可列承包人，实际施工人案件可列转包人、违法分包人并追加发包人")
    return findings


def _has_substantive_dispute(facts: ConstructionFacts) -> bool:
    return any(
        (
            facts.survey_contract, facts.design_contract, facts.contract_invalid,
            facts.qualification_defect, facts.affiliation, facts.tender_illegal,
            facts.planning_missing, facts.illegal_subcontract, facts.black_white_contract,
            facts.labor_subcontract, facts.project_accepted, facts.project_unaccepted,
            facts.period_dispute, facts.unauthorized_use, facts.quality_defect,
            facts.quality_deposit_return, facts.hidden_work, facts.unpaid_project_price,
            facts.priority_claim, facts.actual_constructor, facts.termination_request,
            facts.stoppage_loss, facts.employer_material_delay, facts.interest_claim,
        )
    )


def _only_procedure_question(facts: ConstructionFacts) -> bool:
    return (facts.asks_jurisdiction or facts.asks_defendant) and not _has_substantive_dispute(facts)


def adjudicate_construction(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_construction_config()
    facts = extract_construction_facts(case_text)
    today = today or date.today()
    procedure_findings = _procedure_findings(facts)
    path = ["入口程序校验"]

    if _only_procedure_question(facts):
        major = "建设工程合同纠纷适用合同纠纷管辖和适格当事人规则；合同有有效管辖约定的，按约定处理。"
        minor = "本案主要询问起诉法院或应列被告，未提出需要实体裁判的工程效力、质量、价款或工期争议。"
        conclusion = "按程序事项处理：" + "；".join(procedure_findings)
        return _format_construction_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "建设工程合同纠纷通常适用三年诉讼时效。"
        minor = f"本案可识别的合同或履行日期为 {facts.contract_date.isoformat()}，距今已超过三年，且未识别到中止、中断或延长事由。"
        conclusion = "诉讼时效已过，超过时效部分不予支持。"
        return _format_construction_output(major, minor, conclusion, ["诉讼时效"], facts, [*path, "诉讼时效"], procedure_findings)

    if facts.third_party_tort and not facts.construction_contract:
        major = "第三人侵害财产或人身权益的，按侵权责任规则处理；建设工程合同引擎处理合同相对方之间的履行争议。"
        minor = "本案主要事实指向合同外第三人侵权，未能识别建设工程合同履行争议。"
        conclusion = "本案涉及侵权责任，非建设工程合同纠纷，不适用本建设工程合同裁判引擎。"
        return _format_construction_output(major, minor, conclusion, [], facts, [*path, "侵权第三方分流"], procedure_findings)

    path.append("前置实体判断")

    if facts.survey_contract or facts.design_contract:
        triggered = [config.patch_name("C11", "勘察、设计合同纠纷的特殊处理")]
        kind = "勘察" if facts.survey_contract else "设计"
        major = "建设工程合同包括工程勘察、设计、施工合同；勘察、设计合同没有特别规定的，适用承揽合同有关规定。"
        minor = f"本案合同类型指向工程{kind}合同。"
        conclusion = f"本案为{kind}合同，适用建设工程合同章有关规定；没有特别规定的，适用承揽合同相关规定。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "合同类型识别"], procedure_findings)

    if facts.affiliation:
        triggered = [config.patch_name("C4", "出借资质（挂靠）的连带责任")]
        major = "没有资质的实际施工人借用有资质建筑施工企业名义签订合同的，施工合同无效；出借方与借用方对因出借资质造成的损失承担连带赔偿责任。"
        minor = f"本案存在借用资质或挂靠事实，可识别损失金额为 {_money(facts.actual_loss)}。"
        conclusion = f"出借资质成立，出借方与借用方对损失承担连带赔偿责任，损失金额按 {_money(facts.actual_loss)} 核定。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.actual_constructor or facts.direct_sue_employer or facts.subrogation_claim:
        triggered = [config.patch_name("C6", "实际施工人直接起诉发包人")]
        major = "实际施工人以发包人为被告主张权利的，法院应追加转包人或违法分包人为第三人；查明发包人欠付转包人或违法分包人工程款后，发包人在欠付范围内对实际施工人承担责任。转包人或违法分包人怠于行使到期债权的，实际施工人可以提起代位权诉讼。"
        if facts.subrogation_claim:
            minor = "本案实际施工人主张代位权，理由是转包人或违法分包人怠于向发包人行使到期债权。"
            conclusion = "实际施工人可以提起代位权诉讼；是否支持取决于转包人或违法分包人是否怠于行使到期债权并影响实际施工人债权实现。"
        else:
            minor = f"本案实际施工人直接向发包人主张权利，可识别发包人欠付工程款为 {_money(facts.amount_owed_by_employer)}。"
            conclusion = f"实际施工人可向发包人主张权利，发包人在欠付工程款 {_money(facts.amount_owed_by_employer)} 范围内承担责任，并应追加转包人或违法分包人为第三人。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "实际施工人保护"], procedure_findings)

    if facts.termination_request:
        triggered = [config.patch_name("C15", "建设工程合同解除后的处理")]
        major = "承包人转包、违法分包的，发包人可以解除合同；发包人提供材料设备不合强制性标准或不履行协助义务，经催告仍不履行的，承包人可以解除合同。合同解除后，已完工程质量合格的，按约定支付工程价款；质量不合格的，参照无效合同质量规则处理。"
        if facts.employer_termination and facts.illegal_subcontract:
            minor = "本案发包人因承包人转包或违法分包主张解除合同。"
            conclusion = "发包人解除权成立；合同解除后，已完工程质量合格的，应按约定支付相应工程价款。"
        elif facts.contractor_termination and facts.employer_assistance_breach and facts.urged_unperformed:
            minor = "本案发包人不履行协助义务或提供材料设备不合格，经催告后仍未履行。"
            conclusion = "承包人解除权成立；合同解除后，已完工程质量合格的，发包人应按约定支付相应工程价款。"
        elif facts.completed_quality_bad:
            minor = "本案建设工程合同解除，已完工程质量不合格。"
            conclusion = "合同解除，已完工程质量不合格，不应直接支付工程价款，应参照第793条按修复可能性和过错处理。"
        else:
            minor = "本案存在解除建设工程合同主张，但解除事由或已完工程质量事实仍不完整。"
            conclusion = "需补充转包、违法分包、发包人协助义务违约及已完工程质量情况；质量合格的，解除后仍应支付相应工程价款。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "合同解除"], procedure_findings)

    if facts.black_white_contract:
        triggered = [config.patch_name("C3", "黑白合同的认定")]
        major = "招标人和中标人另行签订的合同与中标合同在工程范围、建设工期、工程质量、工程价款等实质性内容不一致的，应按照中标合同确定权利义务。"
        if facts.substantive_inconsistency:
            minor = "本案存在中标合同外另行签订的合同，且实质性内容不一致。"
            conclusion = "黑白合同成立，应按中标合同确定权利义务。"
        else:
            minor = "本案存在另行合同或黑白合同争议，但尚不能识别工程范围、工期、质量或价款等实质性内容不一致。"
            conclusion = "需先查明另行合同是否改变实质性内容；如改变，应按中标合同确定权利义务。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.labor_subcontract:
        triggered = [config.patch_name("C12", "劳务分包合同的效力")]
        major = "具有劳务作业法定资质的承包人与总承包人、分包人签订的劳务分包合同有效。"
        if facts.labor_qualification:
            minor = "本案为劳务分包合同，劳务承包人具有劳务作业法定资质。"
            conclusion = "劳务分包合同有效。"
        else:
            minor = "本案为劳务分包合同，但未能识别劳务作业法定资质。"
            conclusion = "需补充劳务承包人是否具备法定资质；具备的，劳务分包合同有效。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.affiliation:
        triggered = [config.patch_name("C4", "出借资质（挂靠）的连带责任")]
        major = "没有资质的实际施工人借用有资质建筑施工企业名义签订合同的，施工合同无效；出借方与借用方对因出借资质造成的损失承担连带赔偿责任。"
        minor = f"本案存在借用资质或挂靠事实，可识别损失金额为 {_money(facts.actual_loss)}。"
        conclusion = f"出借资质成立，出借方与借用方对损失承担连带赔偿责任，损失金额按 {_money(facts.actual_loss)} 核定。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.contract_invalid:
        invalid_reasons = []
        if facts.qualification_defect and not facts.qualification_before_completion:
            invalid_reasons.append("承包人资质缺陷")
        if facts.tender_illegal:
            invalid_reasons.append("招投标违法")
        if facts.planning_missing and not facts.planning_obtained_before_suit:
            invalid_reasons.append("规划许可缺失")
        if facts.illegal_subcontract:
            invalid_reasons.append("转包或违法分包")
        reason_text = "、".join(invalid_reasons) or "合同无效事由"
        if facts.project_accepted:
            triggered = [config.patch_name("C1", "合同无效但工程合格的处理")]
            major = "建设工程施工合同无效，但建设工程经验收合格的，可以参照合同关于工程价款的约定折价补偿承包人。"
            minor = f"本案施工合同存在{reason_text}，但工程验收合格，可识别工程价款为 {_money(facts.project_price)}。"
            conclusion = f"合同无效但工程验收合格，应参照合同约定折价补偿承包人 {_money(facts.project_price)}。"
        elif facts.project_unaccepted:
            triggered = [config.patch_name("C2", "合同无效且工程不合格的处理")]
            major = "建设工程施工合同无效且工程验收不合格的，可修复并修复合格的，承包人承担修复费用后可主张折价补偿；修复后仍不合格或不可修复的，承包人无权请求折价补偿。"
            minor = f"本案施工合同存在{reason_text}，且工程验收不合格，可识别修复费用为 {_money(facts.repair_cost)}。"
            if facts.unrepairable:
                conclusion = "合同无效且工程不合格，不可修复，承包人不可主张折价补偿；发包人有过错的，按过错比例承担相应责任。"
            else:
                conclusion = f"合同无效且工程不合格，可修复的，承包人承担修复费用 {_money(facts.repair_cost)}；修复合格后可再参照合同约定主张折价补偿。"
        else:
            triggered = ["合同效力审查"]
            major = "承包人资质缺陷、招投标违法、规划许可缺失、转包或违法分包等情形可能导致建设工程施工合同无效。"
            minor = f"本案识别到{reason_text}，但尚未识别工程是否验收合格。"
            conclusion = "施工合同无效后，应先查明工程质量是否合格；合格的参照合同约定折价补偿，不合格的按修复可能性和过错处理。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.period_dispute or facts.start_notice or facts.actual_entry or facts.delay_acceptance or facts.report_submitted:
        triggered = [config.patch_name("C7", "开工日期与竣工日期的认定")]
        major = "开工日期有开工通知的以通知载明日期为准；通知后不具备开工条件的，以条件具备之日为准；已实际进场施工的，以实际进场时间为准。竣工日期验收合格的以合格之日为准；发包人拖延验收的，以承包人提交验收报告之日为准。"
        start = "开工通知载明日期"
        if facts.conditions_missing:
            start = "开工条件具备之日"
        elif facts.actual_entry:
            start = "实际进场施工之日"
        completion = "竣工验收合格之日"
        if facts.delay_acceptance or facts.report_submitted:
            completion = "承包人提交竣工验收报告之日"
        minor = "本案存在开工日期或竣工日期争议。"
        conclusion = f"开工日期认定为{start}，竣工日期认定为{completion}。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "工期认定"], procedure_findings)

    if facts.unauthorized_use:
        triggered = [config.patch_name("C13", "发包人擅自使用未验收工程的法律后果")]
        major = "建设工程未经竣工验收，发包人擅自使用的，以转移占有建设工程之日为竣工日期；发包人擅自使用后，又以使用部分质量不符合约定为由主张权利的，不予支持。"
        minor = "本案建设工程未经竣工验收，发包人已经擅自使用或转移占有。"
        conclusion = "发包人擅自使用未验收工程，竣工日期认定为转移占有之日；其再以使用部分质量不符合约定为由抗辩的，不予支持。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "竣工日期认定"], procedure_findings)

    if facts.hidden_work:
        triggered = [config.patch_name("C14", "隐蔽工程检查")]
        major = "隐蔽工程在隐蔽以前，承包人应通知发包人检查；发包人没有及时检查的，承包人可以顺延工程日期，并有权请求赔偿停工、窝工等损失。"
        if facts.contractor_notified_inspection and facts.developer_no_inspection:
            minor = "本案隐蔽工程隐蔽前，承包人已通知发包人检查，但发包人未及时检查。"
            conclusion = "发包人未及时检查隐蔽工程，承包人可顺延工期并索赔损失。"
        else:
            minor = "本案涉及隐蔽工程检查，但通知检查和未及时检查事实仍不完整。"
            conclusion = "需补充承包人是否通知检查以及发包人是否未及时检查，再判断工期顺延和损失赔偿。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "工程质量审查"], procedure_findings)

    if facts.quality_deposit_return:
        triggered = [config.patch_name("C8", "工程质量保证金返还")]
        major = "承包人请求返还工程质量保证金的，有约定返还期限按约定；未约定返还期限的，自建设工程通过竣工验收之日起满二年；因发包人原因未验收的，自提交竣工验收报告九十日后起算。"
        if facts.deposit_period_due or facts.no_deposit_period:
            minor = f"本案承包人主张返还工程质量保证金，可识别金额为 {_money(facts.quality_deposit_amount)}，且返还期限届满或未约定期限但已满足法定起算条件。"
            conclusion = f"工程质量保证金应返还，金额按 {_money(facts.quality_deposit_amount)} 核定。"
        else:
            minor = "本案承包人主张返还工程质量保证金，但未识别返还期限已经届满。"
            conclusion = "工程质量保证金暂不支持立即返还；应按约定期限或竣工验收合格满二年的规则判断。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "工程质量审查"], procedure_findings)

    if facts.interest_claim:
        triggered = [config.patch_name("C10", "工程款利息的计算")]
        major = "欠付工程价款利息有约定的按约定处理；没有约定的，按同期贷款市场报价利率计算。工程已实际交付的，自交付之日起算；未交付但提交结算文件的，自提交竣工结算文件之日起算；未交付也未结算的，自起诉之日起算。"
        if facts.agreed_interest:
            standard = "约定利率"
        else:
            standard = "LPR"
        if facts.project_delivered:
            start = "工程实际交付之日"
        elif facts.settlement_submitted:
            start = "提交竣工结算文件之日"
        else:
            start = "起诉之日"
        minor = f"本案发包人拖欠工程款，承包人主张利息，可识别利息金额为 {_money(facts.interest_amount)}。"
        conclusion = f"工程款利息按{standard}计算，起算时间为{start}，利息金额为 {_money(facts.interest_amount)}。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "工程价款结算"], procedure_findings)

    if facts.stoppage_loss or facts.employer_material_delay:
        triggered = [config.patch_name("C9", "发包人违约造成停工/窝工损失")]
        major = "发包人未按约提供原材料、设备、场地、资金、技术资料，或因发包人原因中途停建、缓建的，承包人可以顺延工程日期，并请求赔偿停工、窝工等损失和实际费用。"
        minor = f"本案停工、窝工或缓建原因指向发包人违约，可识别损失金额为 {_money(facts.actual_loss)}。"
        conclusion = f"发包人违约造成停工/窝工，应赔偿承包人损失 {_money(facts.actual_loss)}，并相应顺延工期。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, [*path, "停工窝工损失"], procedure_findings)

    path.append("工程价款优先受偿权")

    if facts.priority_claim or facts.unpaid_project_price:
        triggered = [config.patch_name("C5", "工程价款优先受偿权的行使")]
        major = "发包人未按约支付工程价款，经催告后仍不支付的，承包人可协议折价或请求人民法院拍卖建设工程，并就折价或拍卖价款优先受偿；建设工程价款优先受偿权优于抵押权和其他债权，最长应在应付工程价款之日起十八个月内行使，且以工程质量合格为前提。"
        if facts.beyond_18_months:
            minor = "本案承包人主张工程价款优先受偿权，但已超过十八个月行使期限。"
            conclusion = "承包人不再享有建设工程价款优先受偿权；工程款债权可按普通债权主张。"
        elif facts.worker_interest_harmed:
            minor = "本案存在放弃或限制优先受偿权并损害建筑工人利益的情形。"
            conclusion = "放弃或限制优先受偿权的约定损害建筑工人利益的，不予支持；承包人仍可依法主张优先受偿权。"
        elif facts.project_accepted or facts.within_18_months or facts.payment_urged:
            minor = f"本案发包人欠付工程价款，工程质量合格或未识别质量不合格，且承包人已催告或在十八个月内主张权利，工程价款为 {_money(facts.project_price)}。"
            conclusion = "承包人享有建设工程价款优先受偿权，优先于抵押权和其他债权，行使期限为应付工程价款之日起18个月内。"
        else:
            minor = "本案存在欠付工程款或优先受偿权主张，但催告、工程质量合格及十八个月期限事实仍不完整。"
            conclusion = "需补充工程质量是否合格、是否已催告以及是否在十八个月内行使；满足条件的，承包人享有优先受偿权。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("实际施工人保护")

    if facts.actual_constructor or facts.direct_sue_employer or facts.subrogation_claim:
        triggered = [config.patch_name("C6", "实际施工人直接起诉发包人")]
        major = "实际施工人以发包人为被告主张权利的，法院应追加转包人或违法分包人为第三人；查明发包人欠付转包人或违法分包人工程款后，发包人在欠付范围内对实际施工人承担责任。转包人或违法分包人怠于行使到期债权的，实际施工人可以提起代位权诉讼。"
        if facts.subrogation_claim:
            minor = "本案实际施工人主张代位权，理由是转包人或违法分包人怠于向发包人行使到期债权。"
            conclusion = "实际施工人可以提起代位权诉讼；是否支持取决于转包人或违法分包人是否怠于行使到期债权并影响实际施工人债权实现。"
        else:
            minor = f"本案实际施工人直接向发包人主张权利，可识别发包人欠付工程款为 {_money(facts.amount_owed_by_employer)}。"
            conclusion = f"实际施工人可向发包人主张权利，发包人在欠付工程款 {_money(facts.amount_owed_by_employer)} 范围内承担责任，并应追加转包人或违法分包人为第三人。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("合同解除")

    if facts.termination_request:
        triggered = [config.patch_name("C15", "建设工程合同解除后的处理")]
        major = "承包人转包、违法分包的，发包人可以解除合同；发包人提供材料设备不合强制性标准或不履行协助义务，经催告仍不履行的，承包人可以解除合同。合同解除后，已完工程质量合格的，按约定支付工程价款；质量不合格的，参照无效合同质量规则处理。"
        if facts.employer_termination and facts.illegal_subcontract:
            minor = "本案发包人因承包人转包或违法分包主张解除合同。"
            conclusion = "发包人解除权成立；合同解除后，已完工程质量合格的，应按约定支付相应工程价款。"
        elif facts.contractor_termination and facts.employer_assistance_breach and facts.urged_unperformed:
            minor = "本案发包人不履行协助义务或提供材料设备不合格，经催告后仍未履行。"
            conclusion = "承包人解除权成立；合同解除后，已完工程质量合格的，发包人应按约定支付相应工程价款。"
        elif facts.completed_quality_bad:
            minor = "本案建设工程合同解除，已完工程质量不合格。"
            conclusion = "合同解除，已完工程质量不合格，不应直接支付工程价款，应参照第793条按修复可能性和过错处理。"
        else:
            minor = "本案存在解除建设工程合同主张，但解除事由或已完工程质量事实仍不完整。"
            conclusion = "需补充转包、违法分包、发包人协助义务违约及已完工程质量情况；质量合格的，解除后仍应支付相应工程价款。"
        return _format_construction_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.quality_defect:
        major = "因施工人原因致使建设工程质量不符合约定的，发包人有权请求施工人在合理期限内无偿修理、返工或者改建；修理、返工、改建造成逾期交付的，施工人承担违约责任。"
        minor = "本案存在工程质量不符合约定或质量瑕疵争议。"
        conclusion = "发包人可以请求承包人在合理期限内无偿修理、返工或者改建；造成逾期交付的，承包人承担违约责任。"
        return _format_construction_output(major, minor, conclusion, ["工程质量审查"], facts, [*path, "工程质量审查"], procedure_findings)

    if facts.construction_contract:
        major = "建设工程合同中，承包人进行工程建设，发包人支付价款；施工合同应重点审查合同效力、工期、质量、价款结算、优先受偿权和实际施工人保护。"
        minor = "本案能够识别建设工程合同关系，但未识别足以触发效力、工期、质量、工程款、优先受偿权、实际施工人或解除的具体争议。"
        conclusion = "建设工程合同继续有效，各方应按合同履行；如主张违约责任，需进一步补充资质、招投标、规划许可、工程质量、工程款或工期事实。"
    else:
        major = "建设工程裁判需先识别合同类型、工程内容、资质和许可、工程质量以及工程价款争议。"
        minor = "现有自然语言事实不足以确认建设工程合同关系和裁判节点。"
        conclusion = "请补充合同类型、工程项目、发包人与承包人、资质许可、工程质量和价款结算等事实后再裁判。"
    return _format_construction_output(major, minor, conclusion, [], facts, path, procedure_findings)
