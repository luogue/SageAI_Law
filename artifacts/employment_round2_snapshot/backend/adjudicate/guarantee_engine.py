"""Guarantee-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import _format_output, _mentions, _parse_date, _years_between
from adjudicate.guarantee_configs import get_guarantee_config


@dataclass
class GuaranteeFacts:
    raw_text: str
    contract_type: str = "guarantee"
    contract_type_name: str = "保证合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    guarantee_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    main_contract_invalid: bool = False
    guarantee_invalid: bool = False
    independent_guarantee_clause: bool = False
    state_org_guarantor: bool = False
    public_nonprofit_guarantor: bool = False
    company_guarantor: bool = False
    company_resolution: bool = False
    creditor_good_faith: bool = False
    creditor_bad_faith: bool = False
    written_guarantee: bool = False
    main_debt_exists: bool = False
    guarantee_scope_agreed: bool = False
    unclear_guarantee_type: bool = False
    general_guarantee: bool = False
    joint_guarantee_type: bool = False
    guarantee_period_agreed: bool = False
    guarantee_period_unclear: bool = False
    period_same_or_earlier: bool = False
    main_debt_due_unclear: bool = False
    within_period_action: bool = False
    action_against_debtor: bool = False
    action_against_guarantor: bool = False
    period_expired: bool = False
    only_sue_general_guarantor: bool = False
    debtor_enforced_unsatisfied: bool = False
    debtor_missing_no_property: bool = False
    debtor_bankrupt: bool = False
    debtor_insolvent: bool = False
    waived_prior_lawsuit: bool = False
    main_contract_changed: bool = False
    guarantor_written_consent: bool = False
    debt_aggravated: bool = False
    debt_reduced: bool = False
    credit_assignment: bool = False
    assignment_notified: bool = False
    assignment_prohibited: bool = False
    debt_transfer: bool = False
    third_party_debt_join: bool = False
    multiple_guarantors: bool = False
    guarantee_share_agreed: bool = False
    maximum_guarantee: bool = False
    maximum_period_unclear: bool = False
    guarantee_terminated: bool = False
    guarantor_paid: bool = False
    paid_amount: float = 0.0
    recourse_claim: bool = False
    post_period_signature: bool = False
    new_guarantee_contract: bool = False
    main_debt_limitation_expired: bool = False
    guarantor_knows_limitation: bool = False
    guarantor_not_knows_limitation: bool = False
    debtor_defense: bool = False
    setoff_or_revocation: bool = False
    actual_loss: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "guarantee_contract": self.guarantee_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "main_contract_invalid": self.main_contract_invalid,
            "guarantee_invalid": self.guarantee_invalid,
            "independent_guarantee_clause": self.independent_guarantee_clause,
            "state_org_guarantor": self.state_org_guarantor,
            "public_nonprofit_guarantor": self.public_nonprofit_guarantor,
            "company_guarantor": self.company_guarantor,
            "company_resolution": self.company_resolution,
            "creditor_good_faith": self.creditor_good_faith,
            "creditor_bad_faith": self.creditor_bad_faith,
            "written_guarantee": self.written_guarantee,
            "main_debt_exists": self.main_debt_exists,
            "guarantee_scope_agreed": self.guarantee_scope_agreed,
            "unclear_guarantee_type": self.unclear_guarantee_type,
            "general_guarantee": self.general_guarantee,
            "joint_guarantee_type": self.joint_guarantee_type,
            "guarantee_period_agreed": self.guarantee_period_agreed,
            "guarantee_period_unclear": self.guarantee_period_unclear,
            "period_same_or_earlier": self.period_same_or_earlier,
            "main_debt_due_unclear": self.main_debt_due_unclear,
            "within_period_action": self.within_period_action,
            "action_against_debtor": self.action_against_debtor,
            "action_against_guarantor": self.action_against_guarantor,
            "period_expired": self.period_expired,
            "only_sue_general_guarantor": self.only_sue_general_guarantor,
            "debtor_enforced_unsatisfied": self.debtor_enforced_unsatisfied,
            "debtor_missing_no_property": self.debtor_missing_no_property,
            "debtor_bankrupt": self.debtor_bankrupt,
            "debtor_insolvent": self.debtor_insolvent,
            "waived_prior_lawsuit": self.waived_prior_lawsuit,
            "main_contract_changed": self.main_contract_changed,
            "guarantor_written_consent": self.guarantor_written_consent,
            "debt_aggravated": self.debt_aggravated,
            "debt_reduced": self.debt_reduced,
            "credit_assignment": self.credit_assignment,
            "assignment_notified": self.assignment_notified,
            "assignment_prohibited": self.assignment_prohibited,
            "debt_transfer": self.debt_transfer,
            "third_party_debt_join": self.third_party_debt_join,
            "multiple_guarantors": self.multiple_guarantors,
            "guarantee_share_agreed": self.guarantee_share_agreed,
            "maximum_guarantee": self.maximum_guarantee,
            "maximum_period_unclear": self.maximum_period_unclear,
            "guarantee_terminated": self.guarantee_terminated,
            "guarantor_paid": self.guarantor_paid,
            "paid_amount": self.paid_amount,
            "recourse_claim": self.recourse_claim,
            "post_period_signature": self.post_period_signature,
            "new_guarantee_contract": self.new_guarantee_contract,
            "main_debt_limitation_expired": self.main_debt_limitation_expired,
            "guarantor_knows_limitation": self.guarantor_knows_limitation,
            "guarantor_not_knows_limitation": self.guarantor_not_knows_limitation,
            "debtor_defense": self.debtor_defense,
            "setoff_or_revocation": self.setoff_or_revocation,
            "actual_loss": self.actual_loss,
            "notes": self.notes,
        }


def _format_guarantee_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: GuaranteeFacts,
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


def extract_guarantee_facts(case_text: str) -> GuaranteeFacts:
    config = get_guarantee_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = GuaranteeFacts(raw_text=raw_text)

    for field_name in (
        "guarantee_contract", "third_party_tort", "main_contract_invalid", "guarantee_invalid",
        "independent_guarantee_clause", "state_org_guarantor", "public_nonprofit_guarantor",
        "company_guarantor", "company_resolution", "creditor_good_faith", "creditor_bad_faith",
        "written_guarantee", "main_debt_exists", "guarantee_scope_agreed",
        "unclear_guarantee_type", "general_guarantee", "joint_guarantee_type",
        "guarantee_period_agreed", "guarantee_period_unclear", "period_same_or_earlier",
        "main_debt_due_unclear", "within_period_action", "action_against_debtor",
        "action_against_guarantor", "period_expired", "only_sue_general_guarantor",
        "debtor_enforced_unsatisfied", "debtor_missing_no_property", "debtor_bankrupt",
        "debtor_insolvent", "waived_prior_lawsuit", "main_contract_changed",
        "guarantor_written_consent", "debt_aggravated", "debt_reduced", "credit_assignment",
        "assignment_notified", "assignment_prohibited", "debt_transfer", "third_party_debt_join",
        "multiple_guarantors", "guarantee_share_agreed", "maximum_guarantee",
        "maximum_period_unclear", "guarantee_terminated", "guarantor_paid", "recourse_claim",
        "post_period_signature", "new_guarantee_contract", "main_debt_limitation_expired",
        "guarantor_knows_limitation", "guarantor_not_knows_limitation", "debtor_defense",
        "setoff_or_revocation",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.paid_amount = _extract_money_near(text, config.get_terms("paid_amount"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))

    if any(
        (
            facts.general_guarantee, facts.joint_guarantee_type, facts.unclear_guarantee_type,
            facts.company_guarantor, facts.maximum_guarantee, facts.guarantor_paid,
        )
    ):
        facts.guarantee_contract = True
    return facts


def _procedure_findings(facts: GuaranteeFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("保证合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告通常为保证人和债务人；一般保证中，债权人未就主合同纠纷起诉或仲裁债务人而仅起诉一般保证人的，应驳回起诉")
    return findings


def _only_procedure_question(facts: GuaranteeFacts) -> bool:
    substantive = any(
        (
            facts.main_contract_invalid, facts.guarantee_invalid, facts.state_org_guarantor,
            facts.public_nonprofit_guarantor, facts.company_guarantor, facts.unclear_guarantee_type,
            facts.general_guarantee, facts.joint_guarantee_type, facts.guarantee_period_unclear,
            facts.period_expired, facts.only_sue_general_guarantor, facts.main_contract_changed,
            facts.credit_assignment, facts.debt_transfer, facts.multiple_guarantors,
            facts.maximum_guarantee, facts.guarantor_paid, facts.post_period_signature,
            facts.main_debt_limitation_expired,
        )
    )
    return (facts.asks_jurisdiction or facts.asks_defendant) and not substantive


def adjudicate_guarantee(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_guarantee_config()
    facts = extract_guarantee_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "保证合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出保证方式、保证期间、保证责任、主合同变更或追偿争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_guarantee_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "保证债务诉讼时效应结合保证方式和债权人在保证期间内行使权利的时间确定；一般保证和连带责任保证的起算规则不同。"
        minor = f"识别到相关保证请求、起诉或应履行日期为{facts.contract_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "保证债务诉讼时效可能已过；仍需结合保证期间内是否依法行使权利及保证债务诉讼时效起算点核定。"
        return _format_guarantee_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    if facts.third_party_tort and not facts.guarantee_contract:
        major = "保证合同裁判引擎处理债权人、债务人与保证人之间围绕保证责任产生的合同争议；单纯合同外第三人侵权应按侵权责任处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到保证合同履行争议。"
        conclusion = "本案涉及侵权责任，非保证合同纠纷，不适用本保证合同裁判引擎。"
        return _format_guarantee_output(major, minor, conclusion, [], facts, path, procedure_findings)

    path.append("前置实体判断")
    if facts.state_org_guarantor or facts.public_nonprofit_guarantor:
        triggered.append(config.patch_name("G12", "保证人主体资格特殊规定"))
        major = "《民法典》第683条规定，机关法人不得为保证人，经国务院批准为使用外国政府或者国际经济组织贷款进行转贷的除外；以公益为目的的非营利法人、非法人组织不得为保证人。"
        minor = "识别到保证人为机关法人、公益非营利法人、公益组织、居委会或村委会等特殊主体。"
        conclusion = "保证人不具备保证人资格，保证合同无效。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "保证人主体资格审查"], procedure_findings)

    if facts.company_guarantor:
        triggered.append(config.patch_name("G11", "公司对外担保效力"))
        major = "公司对外担保应审查法定代表人是否超越权限以及相对人是否善意。相对人已对公司决议进行合理审查的，通常认定善意；非善意的，担保合同对公司不发生效力。"
        minor = "识别到保证人为公司或公司法定代表人代表公司对外担保。"
        if facts.company_resolution or facts.creditor_good_faith:
            conclusion = "公司对外担保，相对人善意，担保合同对公司发生效力。"
        else:
            conclusion = "公司对外担保，相对人非善意或未合理审查公司决议，担保合同对公司不发生效力。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "保证人主体资格审查"], procedure_findings)

    if facts.main_contract_invalid or facts.guarantee_invalid or facts.independent_guarantee_clause:
        triggered.append(config.patch_name("G9", "保证合同无效后责任承担"))
        major = "《民法典》第682条规定，保证合同是主债权债务合同的从合同，主债权债务合同无效的，保证合同无效；保证合同确认无效后，各方有过错的，按过错承担相应民事责任。担保独立性约定无效。"
        minor = "识别到主合同无效、保证合同无效或合同约定保证效力独立于主合同。"
        conclusion = "保证合同无效，各方按过错承担责任。一般保证人仍享有先诉抗辩权。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "保证合同效力审查"], procedure_findings)

    if facts.unclear_guarantee_type:
        triggered.append(config.patch_name("G1", "保证方式约定不明推定"))
        major = "《民法典》第686条规定，保证方式包括一般保证和连带责任保证；当事人对保证方式没有约定或者约定不明确的，按照一般保证承担保证责任。"
        minor = "识别到保证合同仅写保证人、担保人，或未明确一般保证、连带责任保证。"
        conclusion = "保证方式约定不明，依法推定为一般保证。一般保证人享有先诉抗辩权，债权人须先向债务人主张权利。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "保证方式认定"], procedure_findings)

    if facts.guarantee_period_agreed or facts.guarantee_period_unclear or facts.period_same_or_earlier or facts.main_debt_due_unclear:
        triggered.append(config.patch_name("G2", "保证期间确定规则"))
        major = "《民法典》第692条规定，保证期间不发生中止、中断和延长；没有约定或者约定不明的，保证期间为主债务履行期限届满之日起六个月；约定早于主债务履行期限或者与其同时届满的，视为没有约定。"
        if facts.guarantee_period_agreed and not facts.period_same_or_earlier:
            minor = "识别到保证合同对保证期间有明确约定，且未识别到约定无效情形。"
            conclusion = "保证期间按合同有效约定确定。保证期间不发生中止、中断和延长。"
        elif facts.main_debt_due_unclear:
            minor = "识别到主债务履行期限没有约定或约定不明。"
            conclusion = "保证期间自债权人请求债务人履行债务的宽限期届满之日起计算六个月。保证期间不发生中止、中断和延长。"
        else:
            minor = "识别到保证期间没有约定、约定不明，或约定早于主债务履行期限、与其同时届满。"
            conclusion = "保证期间为主债务履行期限届满之日起六个月。保证期间不发生中止、中断和延长。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "保证期间确定"], procedure_findings)

    if facts.maximum_guarantee:
        triggered.append(config.patch_name("G8", "最高额保证特殊规则"))
        major = "《民法典》第690条规定，最高额保证是在最高债权额限度内，就一定期间连续发生的债权提供保证。担保制度解释第30条规定，保证期间没有约定或约定不明的，自最高额保证终止之日或保证人终止保证合同的书面通知到达之日起六个月。"
        minor = "识别到保证合同为最高额保证。"
        conclusion = "最高额保证，保证期间为最高额保证终止之日或收到终止通知之日起六个月。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "最高额保证"], procedure_findings)

    if facts.debtor_defense or facts.setoff_or_revocation:
        major = "《民法典》第701条、第702条规定，保证人可以主张债务人对债权人的抗辩；债务人对债权人享有抵销权或者撤销权的，保证人可以在相应范围内拒绝承担保证责任。"
        minor = "识别到保证人主张债务人对债权人的抗辩、抵销权或撤销权。"
        conclusion = "保证人可以在债务人可抗辩、可抵销或可撤销的范围内拒绝承担保证责任。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "保证人抗辩权"], procedure_findings)

    if facts.post_period_signature:
        triggered.append(config.patch_name("G14", "保证期间届满后签字效力"))
        major = "担保制度解释第34条规定，保证责任消灭后，保证人在债权人要求承担保证责任的通知书上签字、盖章或者按指印，债权人请求继续承担保证责任的，人民法院不予支持，但有证据证明成立新的保证合同的除外。"
        minor = "识别到保证期间届满后，保证人在催收通知或类似文件上签字。"
        if facts.new_guarantee_contract:
            conclusion = "保证期间已过，保证人签字构成新的保证合同，保证责任按新合同处理。"
        else:
            conclusion = "保证期间已过，保证人签字不构成新的保证合同，保证责任不恢复。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "保证期间审查"], procedure_findings)

    if facts.main_debt_limitation_expired:
        triggered.append(config.patch_name("G15", "主债务诉讼时效届满影响"))
        major = "担保制度解释第35条规定，保证人知道或者应当知道主债权诉讼时效期间届满仍然提供保证，又以主债权诉讼时效届满为由拒绝承担保证责任的，人民法院不予支持。"
        minor = "识别到主债务诉讼时效期间已经届满。"
        if facts.guarantor_knows_limitation:
            conclusion = "保证人知道主债务诉讼时效已届满，不得以时效届满为由拒绝承担保证责任。"
        else:
            conclusion = "保证人不知道主债务诉讼时效已届满，可以以时效届满为由拒绝承担保证责任。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "主债务诉讼时效"], procedure_findings)

    path.append("一般保证责任")
    if facts.general_guarantee or facts.only_sue_general_guarantor or facts.waived_prior_lawsuit:
        if facts.only_sue_general_guarantor:
            major = "担保制度解释第26条规定，一般保证中债权人未就主合同纠纷提起诉讼或者申请仲裁，仅起诉一般保证人的，人民法院应当驳回起诉。"
            minor = "识别到债权人仅起诉一般保证人，未同时或先行向债务人主张主合同责任。"
            conclusion = "债权人仅起诉一般保证人的，应当驳回起诉。"
            return _format_guarantee_output(major, minor, conclusion, [], facts, path, procedure_findings)
        if facts.period_expired or (facts.within_period_action and not facts.action_against_debtor):
            triggered.append(config.patch_name("G4", "保证期间内行使权利认定"))
            major = "《民法典》第693条规定，一般保证的债权人未在保证期间内对债务人提起诉讼或者申请仲裁的，保证人不再承担保证责任。"
            minor = "识别到保证方式为一般保证，但债权人未在保证期间内对债务人提起诉讼或申请仲裁，或保证期间已经届满。"
            conclusion = "债权人未在保证期间内依法行使权利，保证责任消灭。"
            return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "保证期间内行权"], procedure_findings)
        if facts.waived_prior_lawsuit:
            triggered.append(config.patch_name("G13", "放弃先诉抗辩权效力"))
            major = "《民法典》第687条规定，一般保证人书面表示放弃先诉抗辩权的，债权人可以不经先诉程序直接向保证人主张权利。"
            minor = "识别到保证人书面表示放弃先诉抗辩权。"
            conclusion = "保证人已书面放弃先诉抗辩权，债权人可以直接向保证人主张权利。"
            return _format_guarantee_output(major, minor, conclusion, triggered, facts, [*path, "先诉抗辩权"], procedure_findings)
        triggered.append(config.patch_name("G3", "一般保证人先诉抗辩权"))
        major = "《民法典》第687条规定，一般保证人在主合同纠纷未经审判或者仲裁，并就债务人财产依法强制执行仍不能履行债务前，有权拒绝向债权人承担保证责任；债务人下落不明且无财产、破产、明显资不抵债或保证人书面放弃的除外。"
        minor = "识别到保证方式为一般保证，保证人主张先诉抗辩或责任顺位。"
        if facts.debtor_enforced_unsatisfied or facts.debtor_missing_no_property or facts.debtor_bankrupt or facts.debtor_insolvent:
            conclusion = "一般保证人的先诉抗辩权因法定例外或债务人财产执行仍不能履行而消灭，债权人可以向保证人主张保证责任。"
        else:
            conclusion = "一般保证人享有先诉抗辩权，债权人应先就债务人财产强制执行。如存在例外情形，先诉抗辩权消灭。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("连带责任保证")
    if facts.joint_guarantee_type:
        triggered.append(config.patch_name("G4", "保证期间内行使权利认定"))
        major = "《民法典》第688条、第693条规定，连带责任保证中，债务人不履行到期债务时，债权人可以请求债务人履行，也可以请求保证人在保证范围内承担责任；债权人未在保证期间内请求保证人承担责任的，保证人不再承担保证责任。"
        if facts.period_expired or not (facts.within_period_action or facts.action_against_guarantor):
            minor = "识别到保证方式为连带责任保证，但未识别到债权人在保证期间内请求保证人承担保证责任，或保证期间已过。"
            conclusion = "债权人未在保证期间内依法行使权利，保证责任消灭。"
        else:
            minor = "识别到保证方式为连带责任保证，且债权人在保证期间内请求保证人承担责任。"
            conclusion = "债权人已在保证期间内依法行使权利，保证责任不消灭；债权人可以请求债务人履行，也可以请求保证人在保证范围内承担责任。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("主合同变更")
    if facts.main_contract_changed:
        triggered.append(config.patch_name("G5", "主合同变更未经保证人同意"))
        major = "《民法典》第695条规定，债权人和债务人未经保证人书面同意协商变更主债权债务合同，减轻债务的，保证人仍对变更后的债务承担责任；加重债务的，保证人对加重部分不承担责任。"
        minor = "识别到主合同内容发生变更。"
        if facts.guarantor_written_consent:
            conclusion = "主合同变更已经保证人书面同意，保证人对变更后的债务承担保证责任。"
        elif facts.debt_aggravated:
            conclusion = "主合同变更未经保证人书面同意，保证人对加重部分不承担保证责任。"
        elif facts.debt_reduced:
            conclusion = "主合同变更未经保证人书面同意，但变更减轻债务，保证人仍对变更后的债务承担保证责任。"
        else:
            conclusion = "主合同变更是否影响保证责任，需查明是否经保证人书面同意以及变更是否加重债务。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.credit_assignment or facts.debt_transfer or facts.third_party_debt_join:
        triggered.append(config.patch_name("G6", "债权转让与债务转移影响"))
        major = "《民法典》第696条、第697条规定，债权转让未通知保证人的，对保证人不发生效力；债务转移未经保证人书面同意的，保证人对未经同意转移的债务不再承担责任；第三人加入债务的，保证责任不受影响。"
        if facts.debt_transfer and not facts.guarantor_written_consent:
            minor = "识别到债务转移未经保证人书面同意。"
            conclusion = "债务转移未经保证人书面同意，保证责任对转移债务部分消灭。"
        elif facts.credit_assignment and not facts.assignment_notified:
            minor = "识别到债权转让未通知保证人。"
            conclusion = "债权转让未通知保证人，该转让对保证人不发生效力，保证人对受让人不承担保证责任。"
        elif facts.third_party_debt_join:
            minor = "识别到第三人加入债务。"
            conclusion = "第三人加入债务不影响原保证责任，保证责任不变。"
        else:
            minor = "识别到债权转让或债务转移，并已通知保证人或取得书面同意。"
            conclusion = "债权转让或债务转移已经履行通知或书面同意要求，保证责任按有效变更后的关系处理。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("保证人追偿")
    if facts.guarantor_paid or facts.recourse_claim:
        triggered.append(config.patch_name("G10", "保证人追偿权与代位权"))
        major = "《民法典》第700条规定，保证人承担保证责任后，除当事人另有约定外，有权在其承担保证责任范围内向债务人追偿，并享有债权人对债务人的权利，但不得损害债权人的利益。"
        minor = "识别到保证人已经承担保证责任或向债务人主张追偿。"
        conclusion = f"保证人已承担保证责任 {_money(facts.paid_amount)}，有权向债务人追偿，并代位行使债权人对债务人的权利。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("独立分支")
    if facts.multiple_guarantors:
        triggered.append(config.patch_name("G7", "共同保证责任承担"))
        major = "《民法典》第699条规定，同一债务有两个以上保证人的，保证人按保证合同约定份额承担责任；没有约定保证份额的，债权人可以请求任何一个保证人在其保证范围内承担责任。"
        minor = "识别到同一债务存在两个以上保证人。"
        if facts.guarantee_share_agreed:
            conclusion = "共同保证，有约定保证份额，保证人按份额承担保证责任。"
        else:
            conclusion = "共同保证，无约定保证份额，债权人可以请求任何一个保证人在其保证范围内承担保证责任；向部分保证人行权的效力不当然及于其他保证人。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.guarantee_contract:
        major = "保证合同是为保障债权实现而由保证人为他人债务提供担保的从合同。裁判应依次审查保证人资格、保证合同效力、保证方式、保证期间、债权人是否在保证期间内行使权利，以及主合同变更和追偿问题。"
        minor = "已识别保证合同关系，但未稳定识别足以输出最终结论的保证方式、保证期间、行权事实、主合同变更、主体资格或追偿事实。"
        conclusion = "事实要素不足，需补充保证方式、主债务到期日、保证期间、债权人行权对象和时间、保证人资格、是否存在主合同变更或是否已代偿后再裁判。"
        return _format_guarantee_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "保证合同纠纷应围绕保证方式、保证期间、债权人是否在保证期间内行使权利、先诉抗辩权、主合同变更和保证人追偿权进行审查。"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的保证合同关键事实。"
    conclusion = "事实要素不足，需补充是否存在保证合同、保证方式、保证期间、债权人是否行使权利、保证人主体资格和主合同状态后再裁判。"
    return _format_guarantee_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
