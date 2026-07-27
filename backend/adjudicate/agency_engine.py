"""Agency-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.agency_configs import get_agency_config
from adjudicate.engine_v2 import _extract_money_near, _format_output, _mentions, _parse_date, _years_between


@dataclass
class AgencyFacts:
    raw_text: str
    contract_type: str = "agency"
    contract_type_name: str = "委托合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    agency_contract: bool = False
    contract_invalid: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    nature_dispute: bool = False
    process_affairs: bool = False
    complete_work: bool = False
    intermediary_service: bool = False
    commission_trade: bool = False
    paid_agency: bool = False
    unpaid_agency: bool = False
    general_mandate: bool = False
    special_mandate: bool = False
    expense_advance: bool = False
    nonnecessary_expense: bool = False
    remuneration_unpaid: bool = False
    matter_completed: bool = False
    matter_unfinished_no_trustee_fault: bool = False
    matter_unfinished_trustee_fault: bool = False
    trustee_loss_no_fault: bool = False
    instruction_changed_without_consent: bool = False
    emergency_handling: bool = False
    timely_report: bool = False
    sub_entrustment: bool = False
    principal_consent: bool = False
    ratification: bool = False
    emergency_sub_entrustment: bool = False
    selection_instruction_fault: bool = False
    self_agency: bool = False
    both_side_agency: bool = False
    consent_or_ratification: bool = False
    unfair_price: bool = False
    report_failure: bool = False
    false_report: bool = False
    property_obtained: bool = False
    property_not_transferred: bool = False
    trustee_loss: bool = False
    trustee_fault: bool = False
    trustee_no_fault: bool = False
    trustee_intent_gross: bool = False
    trustee_proves_no_intent_gross: bool = False
    over_authority: bool = False
    actual_loss: float = 0.0
    expected_profit: float = 0.0
    third_party_cause: bool = False
    principal_fault: bool = False
    force_majeure: bool = False
    trustee_own_name: bool = False
    third_party_knows_agency: bool = False
    third_party_unknown_agency: bool = False
    third_party_fault_nonperformance: bool = False
    principal_fault_nonperformance: bool = False
    trustee_disclosed_third_party: bool = False
    trustee_disclosed_principal: bool = False
    third_party_would_not_contract: bool = False
    third_party_selected_principal: bool = False
    third_party_selected_trustee: bool = False
    defense_continuation: bool = False
    arbitrary_termination: bool = False
    principal_terminates: bool = False
    trustee_terminates: bool = False
    termination_loss: bool = False
    not_attributable_termination: bool = False
    direct_loss: bool = False
    liquidated_damage: bool = False
    separate_entrustment: bool = False
    trustee_consented_separate: bool = False
    separate_caused_loss: bool = False
    joint_trustees: bool = False
    principal_dead_or_terminated: bool = False
    trustee_dead_or_incapable: bool = False
    no_termination_agreement: bool = False
    continuing_needed: bool = False
    format_clause: bool = False
    prompt_explain: bool = False
    unreasonable_clause: bool = False
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "agency_contract": self.agency_contract,
            "contract_invalid": self.contract_invalid,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "nature_dispute": self.nature_dispute,
            "process_affairs": self.process_affairs,
            "complete_work": self.complete_work,
            "intermediary_service": self.intermediary_service,
            "commission_trade": self.commission_trade,
            "paid_agency": self.paid_agency,
            "unpaid_agency": self.unpaid_agency,
            "general_mandate": self.general_mandate,
            "special_mandate": self.special_mandate,
            "expense_advance": self.expense_advance,
            "nonnecessary_expense": self.nonnecessary_expense,
            "remuneration_unpaid": self.remuneration_unpaid,
            "matter_completed": self.matter_completed,
            "matter_unfinished_no_trustee_fault": self.matter_unfinished_no_trustee_fault,
            "matter_unfinished_trustee_fault": self.matter_unfinished_trustee_fault,
            "trustee_loss_no_fault": self.trustee_loss_no_fault,
            "instruction_changed_without_consent": self.instruction_changed_without_consent,
            "emergency_handling": self.emergency_handling,
            "timely_report": self.timely_report,
            "sub_entrustment": self.sub_entrustment,
            "principal_consent": self.principal_consent,
            "ratification": self.ratification,
            "emergency_sub_entrustment": self.emergency_sub_entrustment,
            "selection_instruction_fault": self.selection_instruction_fault,
            "self_agency": self.self_agency,
            "both_side_agency": self.both_side_agency,
            "consent_or_ratification": self.consent_or_ratification,
            "unfair_price": self.unfair_price,
            "report_failure": self.report_failure,
            "false_report": self.false_report,
            "property_obtained": self.property_obtained,
            "property_not_transferred": self.property_not_transferred,
            "trustee_loss": self.trustee_loss,
            "trustee_fault": self.trustee_fault,
            "trustee_no_fault": self.trustee_no_fault,
            "trustee_intent_gross": self.trustee_intent_gross,
            "trustee_proves_no_intent_gross": self.trustee_proves_no_intent_gross,
            "over_authority": self.over_authority,
            "actual_loss": self.actual_loss,
            "expected_profit": self.expected_profit,
            "third_party_cause": self.third_party_cause,
            "principal_fault": self.principal_fault,
            "force_majeure": self.force_majeure,
            "trustee_own_name": self.trustee_own_name,
            "third_party_knows_agency": self.third_party_knows_agency,
            "third_party_unknown_agency": self.third_party_unknown_agency,
            "third_party_fault_nonperformance": self.third_party_fault_nonperformance,
            "principal_fault_nonperformance": self.principal_fault_nonperformance,
            "trustee_disclosed_third_party": self.trustee_disclosed_third_party,
            "trustee_disclosed_principal": self.trustee_disclosed_principal,
            "third_party_would_not_contract": self.third_party_would_not_contract,
            "third_party_selected_principal": self.third_party_selected_principal,
            "third_party_selected_trustee": self.third_party_selected_trustee,
            "defense_continuation": self.defense_continuation,
            "arbitrary_termination": self.arbitrary_termination,
            "principal_terminates": self.principal_terminates,
            "trustee_terminates": self.trustee_terminates,
            "termination_loss": self.termination_loss,
            "not_attributable_termination": self.not_attributable_termination,
            "direct_loss": self.direct_loss,
            "liquidated_damage": self.liquidated_damage,
            "separate_entrustment": self.separate_entrustment,
            "trustee_consented_separate": self.trustee_consented_separate,
            "separate_caused_loss": self.separate_caused_loss,
            "joint_trustees": self.joint_trustees,
            "principal_dead_or_terminated": self.principal_dead_or_terminated,
            "trustee_dead_or_incapable": self.trustee_dead_or_incapable,
            "no_termination_agreement": self.no_termination_agreement,
            "continuing_needed": self.continuing_needed,
            "format_clause": self.format_clause,
            "prompt_explain": self.prompt_explain,
            "unreasonable_clause": self.unreasonable_clause,
            "notes": self.notes,
        }


def _format_agency_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: AgencyFacts,
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


def extract_agency_facts(case_text: str) -> AgencyFacts:
    config = get_agency_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = AgencyFacts(raw_text=raw_text)

    for field_name in (
        "agency_contract", "contract_invalid", "third_party_tort", "nature_dispute",
        "process_affairs", "complete_work", "intermediary_service", "commission_trade",
        "paid_agency", "unpaid_agency", "general_mandate", "special_mandate",
        "expense_advance", "nonnecessary_expense", "remuneration_unpaid", "matter_completed",
        "matter_unfinished_no_trustee_fault", "matter_unfinished_trustee_fault",
        "trustee_loss_no_fault", "instruction_changed_without_consent", "emergency_handling",
        "timely_report", "sub_entrustment", "principal_consent", "ratification",
        "emergency_sub_entrustment", "selection_instruction_fault", "self_agency",
        "both_side_agency", "consent_or_ratification", "unfair_price", "report_failure",
        "false_report", "property_obtained", "property_not_transferred", "trustee_loss",
        "trustee_fault", "trustee_no_fault", "trustee_intent_gross", "trustee_proves_no_intent_gross",
        "over_authority", "third_party_cause", "principal_fault", "force_majeure",
        "trustee_own_name", "third_party_knows_agency", "third_party_unknown_agency",
        "third_party_fault_nonperformance", "principal_fault_nonperformance",
        "trustee_disclosed_third_party", "trustee_disclosed_principal", "third_party_would_not_contract",
        "third_party_selected_principal", "third_party_selected_trustee", "defense_continuation",
        "arbitrary_termination", "principal_terminates", "trustee_terminates", "termination_loss",
        "not_attributable_termination", "direct_loss", "liquidated_damage", "separate_entrustment",
        "trustee_consented_separate", "separate_caused_loss", "joint_trustees",
        "principal_dead_or_terminated", "trustee_dead_or_incapable", "no_termination_agreement",
        "continuing_needed", "format_clause", "prompt_explain", "unreasonable_clause",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.actual_loss = max(
        _extract_money_near(text, config.get_terms("actual_loss")),
        _extract_money_near(text, config.get_terms("property_obtained")),
    )
    facts.expected_profit = _extract_money_near(text, config.get_terms("expected_profit"))

    if any((facts.process_affairs, facts.paid_agency, facts.unpaid_agency, facts.sub_entrustment, facts.over_authority)):
        facts.agency_contract = True
    if facts.third_party_fault_nonperformance or facts.principal_fault_nonperformance:
        facts.trustee_own_name = facts.trustee_own_name or facts.third_party_unknown_agency
    return facts


def _procedure_findings(facts: AgencyFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("委托合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告应按请求内容确定：委托人请求赔偿或返还财产的，通常列受托人为被告；受托人请求报酬、费用或损失补偿的，通常列委托人为被告")
    return findings


def _only_procedure_question(facts: AgencyFacts) -> bool:
    substantive = any(
        (
            facts.contract_invalid, facts.nature_dispute, facts.complete_work, facts.intermediary_service,
            facts.commission_trade, facts.expense_advance, facts.remuneration_unpaid,
            facts.instruction_changed_without_consent, facts.sub_entrustment, facts.self_agency,
            facts.both_side_agency, facts.report_failure, facts.property_not_transferred,
            facts.trustee_loss, facts.over_authority, facts.trustee_own_name, facts.arbitrary_termination,
            facts.separate_entrustment, facts.joint_trustees, facts.principal_dead_or_terminated,
            facts.trustee_dead_or_incapable, facts.format_clause,
        )
    )
    return (facts.asks_jurisdiction or facts.asks_defendant) and not substantive


def _money(value: float) -> str:
    return f"{value:.2f} 元" if value > 0 else "待核定"


def adjudicate_agency(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_agency_config()
    facts = extract_agency_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "委托合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出委托事务处理、费用报酬、受托人责任、转委托、间接代理或合同解除争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_agency_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.third_party_tort and not facts.agency_contract:
        major = "委托合同裁判引擎处理委托人与受托人之间因处理委托事务产生的合同争议；单纯合同外第三人侵权应按侵权责任处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到委托合同履行争议。"
        conclusion = "本案涉及侵权责任，非委托合同纠纷，不适用本委托合同裁判引擎。"
        return _format_agency_output(major, minor, conclusion, [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "委托合同纠纷适用三年一般诉讼时效。"
        minor = f"识别到相关合同签订、解除或应履行日期为{facts.contract_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求。"
        return _format_agency_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    path.append("前置实体判断")
    if facts.nature_dispute or facts.complete_work or facts.intermediary_service or facts.commission_trade:
        triggered.append(config.patch_name("A1", "委托合同性质认定"))
        major = "《民法典》第919条规定，委托合同是委托人和受托人约定，由受托人处理委托人事务的合同。合同性质应按实质内容认定，不能只看合同名称。"
        if facts.process_affairs and not (facts.complete_work or facts.intermediary_service or facts.commission_trade):
            minor = "识别到合同核心是由受托人按照委托人意思处理事务，而非交付固定工作成果、报告订约机会或以自己名义从事交易。"
            conclusion = "按实质内容认定为委托合同，继续适用委托合同裁判规则。"
        elif facts.complete_work:
            minor = "识别到合同核心是完成特定工作成果并交付成果。"
            conclusion = "本案更接近承揽合同，应适用承揽合同裁判规则。"
        elif facts.intermediary_service:
            minor = "识别到合同核心是报告订约机会或提供媒介服务。"
            conclusion = "本案更接近中介合同，应适用中介合同规则。"
        else:
            minor = "识别到受托人以自己名义为委托人进行交易。"
            conclusion = "本案更接近行纪合同，应适用行纪合同规则。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, [*path, "合同性质识别"], procedure_findings)

    if facts.contract_invalid:
        major = "委托合同违反法律、行政法规强制性规定或损害公共利益的，应认定无效；无效后应返还取得的财产并按过错赔偿。"
        minor = "识别到委托合同无效或不成立事实。"
        conclusion = "按无效合同处理，已经取得的财产应返还；有过错的一方赔偿对方因此受到的损失。"
        return _format_agency_output(major, minor, conclusion, [], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.format_clause:
        triggered.append(config.patch_name("A14", "格式条款效力审查"))
        major = "《民法典》第496条、第497条规定，提供格式条款的一方应合理提示并说明；不合理免除自身责任、加重对方责任、排除对方主要权利的格式条款无效。"
        minor = "识别到委托合同中存在预先拟定、不能协商的格式条款。"
        if facts.unreasonable_clause and not facts.prompt_explain:
            conclusion = "格式条款无效，不能作为免除主要义务、免除重大过错责任或不合理加重对方责任的依据。"
        elif facts.unreasonable_clause:
            conclusion = "即使已作提示说明，不合理免除责任、加重责任或排除主要权利的格式条款仍无效。"
        else:
            conclusion = "格式条款本身不当然无效；需继续审查是否已提示说明，以及条款内容是否公平合理。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.special_mandate or facts.general_mandate:
        major = "《民法典》第920条规定，委托人可以特别委托受托人处理一项或者数项事务，也可以概括委托受托人处理一切事务。"
        minor = "识别到双方对委托权限范围存在特别委托或概括委托安排。"
        conclusion = "特别委托按明确授权事项处理，概括委托按授权范围内的一切事务处理；受托人不得超越授权范围。"
        return _format_agency_output(major, minor, conclusion, [], facts, [*path, "委托权限范围"], procedure_findings)

    if facts.expense_advance or facts.remuneration_unpaid or facts.matter_unfinished_no_trustee_fault or facts.trustee_loss_no_fault or facts.separate_entrustment:
        path.append("委托人义务")
        if facts.expense_advance:
            major = "《民法典》第921条规定，委托人应当预付处理委托事务的费用；受托人为处理委托事务垫付必要费用的，委托人应当偿还并支付利息。"
            minor = "识别到受托人为处理委托事务垫付或请求预付必要费用。"
            conclusion = "委托人应偿还必要费用并支付相应利息；非必要或不合理扩大支出的费用不予支持。" if not facts.nonnecessary_expense else "非必要或不合理扩大支出的费用不予支持，必要费用部分可另行核定。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.remuneration_unpaid and facts.matter_completed:
            major = "《民法典》第928条规定，受托人完成委托事务的，委托人应当按照约定向其支付报酬。"
            minor = "识别到受托人已经完成委托事务，但委托人尚未支付报酬。"
            conclusion = f"委托人应向受托人支付报酬，已识别金额为 {_money(facts.actual_loss)}。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.matter_unfinished_no_trustee_fault:
            triggered.append(config.patch_name("A15", "不可归责受托人的报酬请求"))
            major = "《民法典》第928条规定，因不可归责于受托人的事由，委托合同解除或者委托事务不能完成的，委托人应当向受托人支付相应报酬；另有约定的除外。"
            minor = "识别到委托事务未完成，但原因不可归责于受托人。"
            conclusion = "委托人应向受托人支付相应报酬；具体数额按已完成事务比例、约定报酬和实际履行情况核定。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.trustee_loss_no_fault:
            major = "《民法典》第930条规定，受托人处理委托事务时，因不可归责于自己的事由受到损失的，可以向委托人请求赔偿损失。"
            minor = "识别到受托人在处理委托事务过程中无过错受损。"
            conclusion = f"委托人应赔偿受托人损失，已识别损失为 {_money(facts.actual_loss)}。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.separate_entrustment:
            triggered.append(config.patch_name("A8", "委托人另行委托"))
            major = "《民法典》第931条规定，委托人经受托人同意，可以在受托人之外委托第三人处理委托事务；因此造成受托人损失的，受托人可以请求赔偿。"
            minor = "识别到委托人将同一事务另行委托第三人处理。"
            if facts.trustee_consented_separate and not facts.separate_caused_loss:
                conclusion = "委托人另行委托不当然违约，原受托人仍可就已处理事务请求费用和报酬。"
            else:
                conclusion = "另行委托造成原受托人损失的，委托人应赔偿相应损失。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if any((facts.instruction_changed_without_consent, facts.self_agency, facts.both_side_agency, facts.report_failure, facts.false_report, facts.property_not_transferred, facts.joint_trustees)):
        path.append("受托人义务")
        if facts.instruction_changed_without_consent:
            triggered.append(config.patch_name("A11", "受托人指示遵守义务"))
            major = "《民法典》第922条规定，受托人应当按照委托人的指示处理委托事务；需要变更指示的，应经委托人同意，情况紧急难以联系的，受托人应妥善处理并及时报告。"
            minor = "识别到受托人未按委托人指示处理事务或擅自变更指示。"
            if facts.emergency_handling and facts.timely_report:
                conclusion = "受托人在紧急情况下为维护委托人利益变更处理方式并及时报告的，不构成违反指示义务。"
            else:
                conclusion = f"受托人违反指示义务，应赔偿因此造成的损失，已识别损失为 {_money(facts.actual_loss)}。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.self_agency or facts.both_side_agency:
            triggered.append(config.patch_name("A4", "自己代理与双方代理"))
            major = "《民法典》第168条规定，代理人不得以被代理人的名义与自己实施民事法律行为，也不得同时代理双方实施民事法律行为；被代理人同意或者追认的除外。"
            minor = "识别到受托人存在自己代理或双方代理情形。"
            if facts.consent_or_ratification and not facts.unfair_price:
                conclusion = "自己代理或双方代理已经委托人同意或追认，且未识别到显失公平，交易效力可予认可。"
            else:
                conclusion = "自己代理或双方代理未经同意或追认的，对委托人不发生效力；造成损失的，受托人应赔偿。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.report_failure or facts.false_report:
            triggered.append(config.patch_name("A12", "受托人报告义务"))
            major = "《民法典》第924条规定，受托人应当按照委托人的要求报告委托事务处理情况；委托合同终止时，应报告委托事务结果。"
            minor = "识别到受托人未报告、拒绝报告或虚假报告事务处理情况。"
            conclusion = "受托人违反报告义务；因此造成委托人损失的，应承担赔偿责任。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.property_not_transferred:
            triggered.append(config.patch_name("A13", "取得财产转交义务"))
            major = "《民法典》第927条规定，受托人处理委托事务取得的财产，应当转交给委托人。"
            minor = "识别到受托人处理委托事务取得财产后未转交委托人。"
            conclusion = f"受托人应返还取得财产并赔偿损失，已识别金额为 {_money(facts.actual_loss)}。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
        if facts.joint_trustees:
            triggered.append(config.patch_name("A9", "共同受托人连带责任"))
            major = "《民法典》第932条规定，两个以上受托人共同处理委托事务的，对委托人承担连带责任。"
            minor = "识别到两个以上受托人共同处理委托事务并发生责任争议。"
            conclusion = "共同受托人对委托人承担连带责任；内部责任可按各自过错和约定另行分担。"
            return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("受托人责任")
    if facts.over_authority:
        triggered.append(config.patch_name("A2", "有偿/无偿委托责任标准"))
        major = "《民法典》第929条规定，受托人超越权限造成委托人损失的，应当赔偿损失。"
        minor = "识别到受托人超越授权范围处理委托事务并造成损失。"
        conclusion = f"受托人越权造成损失的，应直接向委托人赔偿，已识别损失为 {_money(facts.actual_loss)}。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.trustee_loss and not facts.arbitrary_termination:
        triggered.append(config.patch_name("A2", "有偿/无偿委托责任标准"))
        major = "《民法典》第929条规定，有偿委托中受托人有过错造成委托人损失的，应赔偿损失；无偿委托中受托人故意或者重大过失造成损失的，才承担赔偿责任。"
        if facts.force_majeure or facts.principal_fault:
            minor = "识别到损失由不可抗力或委托人自身原因造成。"
            conclusion = "受托人不承担赔偿责任；相应损失按不可抗力或委托人过错规则处理。"
        elif facts.third_party_cause:
            minor = "识别到损失直接由第三人原因造成。"
            conclusion = "受托人一般不直接承担第三人违约或侵权责任；但未及时报告、未按指示追偿或处理不当扩大的损失，应由受托人承担相应责任。"
        elif facts.unpaid_agency:
            minor = "识别到委托为无偿委托。"
            if facts.trustee_intent_gross:
                conclusion = f"无偿委托中受托人存在故意或重大过失，应赔偿损失，已识别损失为 {_money(facts.actual_loss)}。"
            else:
                conclusion = "无偿委托中未能识别受托人故意或重大过失，委托人要求受托人赔偿的请求不予支持。"
        else:
            minor = "识别到委托为有偿委托或存在报酬约定。"
            if facts.trustee_fault:
                conclusion = f"有偿委托中受托人有过错造成损失，应赔偿损失，已识别损失为 {_money(facts.actual_loss)}。"
            else:
                conclusion = "有偿委托仍需证明受托人有过错及该过错与损失之间存在因果关系；现有事实不足以直接支持赔偿。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("间接代理")
    if facts.trustee_own_name and facts.third_party_knows_agency:
        major = "《民法典》第925条规定，受托人以自己的名义在委托人授权范围内与第三人订立合同，第三人在订立合同时知道受托人与委托人之间代理关系的，该合同直接约束委托人和第三人。"
        minor = "识别到受托人以自己名义订约，但第三人在订立合同时知道委托人与受托人的代理关系。"
        conclusion = "该合同直接约束委托人和第三人；受托人不因形式上以自己名义签约而当然成为最终责任主体。"
        return _format_agency_output(major, minor, conclusion, [], facts, path, procedure_findings)

    if facts.trustee_own_name and facts.third_party_fault_nonperformance:
        triggered.append(config.patch_name("A5", "委托人介入权"))
        if facts.defense_continuation:
            triggered.append(config.patch_name("A16", "介入权/选择权后的抗辩延续"))
        major = "《民法典》第926条规定，受托人以自己的名义与第三人订立合同，第三人不履行义务导致委托人受损的，受托人向委托人披露第三人后，委托人可以行使受托人对第三人的权利；但第三人知道委托人就不会订约的除外。"
        minor = "识别到受托人以自己名义与第三人订约，第三人原因导致不履行，受托人已披露或需要披露第三人。"
        if facts.third_party_would_not_contract:
            conclusion = "第三人能够证明其知道委托人身份就不会订立合同的，委托人介入权不成立。"
        else:
            conclusion = "委托人介入权成立，可以向第三人主张受托人原本享有的合同权利；第三人原可向受托人主张的抗辩继续存在。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.trustee_own_name and facts.principal_fault_nonperformance:
        triggered.append(config.patch_name("A6", "第三人选择权"))
        if facts.defense_continuation:
            triggered.append(config.patch_name("A16", "介入权/选择权后的抗辩延续"))
        major = "《民法典》第926条规定，受托人以自己的名义与第三人订立合同，委托人原因导致受托人不能履行对第三人的义务的，受托人应向第三人披露委托人；第三人可以选择受托人或者委托人作为相对人主张权利，选定后不得变更。"
        minor = "识别到受托人以自己名义与第三人订约，因委托人原因导致不能履行。"
        selected = "委托人" if facts.third_party_selected_principal else "受托人" if facts.third_party_selected_trustee else "委托人或受托人"
        conclusion = f"第三人选择权成立，可以选择{selected}主张权利；一经选定不得变更，原合同抗辩继续存在。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("任意解除")
    if facts.arbitrary_termination:
        triggered.append(config.patch_name("A7", "任意解除权及赔偿范围"))
        major = "《民法典》第933条规定，委托人或者受托人可以随时解除委托合同。因解除合同造成对方损失的，除不可归责于该当事人的事由外，无偿委托赔偿直接损失，有偿委托赔偿直接损失和合同履行后可以获得的利益。"
        minor = "识别到委托人或受托人行使任意解除权并发生损失争议。"
        if not facts.termination_loss:
            conclusion = "委托合同可以解除；未识别到解除造成损失，暂不支持赔偿。"
        elif facts.not_attributable_termination:
            conclusion = "解除事由不可归责于解除方，解除方不承担损失赔偿责任。"
        elif facts.unpaid_agency:
            conclusion = f"无偿委托解除造成损失的，解除方赔偿直接损失，已识别损失为 {_money(facts.actual_loss)}。"
        else:
            total = facts.actual_loss + facts.expected_profit
            conclusion = f"有偿委托解除造成损失的，解除方赔偿直接损失和可得利益，已识别金额为 {_money(total)}。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("转委托")
    if facts.sub_entrustment:
        triggered.append(config.patch_name("A3", "转委托责任"))
        major = "《民法典》第923条规定，受托人应当亲自处理委托事务；经委托人同意或者追认的，可以转委托。转委托经同意或追认的，受托人仅就第三人的选任及其对第三人的指示承担责任；未经同意或追认的，受托人应当对第三人的行为承担责任，但紧急情况下为维护委托人利益需要转委托的除外。"
        minor = "识别到受托人将委托事务转交第三人处理。"
        if facts.principal_consent or facts.ratification:
            conclusion = "转委托有效；受托人仅对第三人的选任和指示承担责任，第三人处理事务造成损失的，按具体过错另行判断。"
        elif facts.emergency_sub_entrustment:
            conclusion = "虽未经同意，但属于紧急情况下为维护委托人利益所作转委托，受托人不因转委托本身承担全部责任。"
        else:
            conclusion = "未经委托人同意或追认的转委托不符合规则，受托人应对第三人的行为向委托人承担责任。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("合同终止")
    if facts.principal_dead_or_terminated or facts.trustee_dead_or_incapable:
        triggered.append(config.patch_name("A10", "终止后的继续处理义务"))
        major = "《民法典》第934条、第935条规定，委托人死亡、终止或者受托人死亡、丧失民事行为能力、终止的，委托合同原则上终止；但当事人另有约定、根据委托事务性质不宜终止，或者因委托人死亡、终止而终止将损害委托人利益的，受托人在继承人、遗产管理人或清算人承受事务前应继续处理。"
        minor = "识别到委托人或受托人死亡、终止或丧失行为能力。"
        if facts.continuing_needed:
            conclusion = "委托合同虽发生终止事由，但立即停止会损害委托人利益，受托人应继续处理至继承人、遗产管理人或清算人接手。"
        else:
            conclusion = "委托合同原则上终止；已产生的费用、报酬、财产返还和损失赔偿仍按实际履行情况结算。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.agency_contract:
        major = "《民法典》第919条规定，委托合同以受托人处理委托人事务为核心；裁判应围绕授权范围、费用报酬、受托人义务、责任标准、间接代理、转委托和终止后义务进行审查。"
        minor = "已识别委托合同关系，但未稳定识别费用报酬、受托人过错、转委托、间接代理、任意解除或终止后义务等足以输出最终裁判的事实。"
        conclusion = "事实要素不足，需补充委托事务内容、是否有偿、授权范围、损失原因、受托人过错、第三人关系或解除终止情况后再裁判。"
        return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "委托合同纠纷应围绕受托人是否按授权和指示处理事务、委托人是否支付费用报酬、损失原因及有偿或无偿责任标准进行审查。"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的委托合同关键事实。"
    conclusion = "事实要素不足，需补充是否存在委托合同关系、委托事务、授权范围、费用报酬、损失原因或第三人交易事实后再裁判。"
    return _format_agency_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
