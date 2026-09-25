"""Technology-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import _format_output, _mentions, _parse_date, _years_between
from adjudicate.technology_configs import get_technology_config


@dataclass
class TechnologyFacts:
    raw_text: str
    contract_type: str = "technology"
    contract_type_name: str = "技术合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    technology_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    nature_dispute: bool = False
    development_contract: bool = False
    commissioned_development: bool = False
    cooperative_development: bool = False
    transfer_contract: bool = False
    license_contract: bool = False
    consulting_contract: bool = False
    service_contract: bool = False
    work_or_construction: bool = False
    illegal_monopoly: bool = False
    infringe_achievement: bool = False
    trade_secret_invalid: bool = False
    good_faith_acquirer: bool = False
    reasonable_use_fee: float = 0.0
    fraud_contract: bool = False
    duty_achievement: bool = False
    non_duty_achievement: bool = False
    ownership_dispute: bool = False
    termination_request: bool = False
    delayed_main_obligation: bool = False
    urged: bool = False
    over_30_days: bool = False
    technology_import_export: bool = False
    development_failed: bool = False
    risk_agreed: bool = False
    no_risk_agreement: bool = False
    developer_breach: bool = False
    client_breach: bool = False
    stagnation_delay_failure: bool = False
    invention_creation: bool = False
    patent_agreed: bool = False
    technical_secret_result: bool = False
    result_agreed: bool = False
    licensor_not_owner: bool = False
    technology_defective: bool = False
    license_not_provided: bool = False
    license_over_scope: bool = False
    fee_unpaid: bool = False
    licensee_over_scope: bool = False
    licensee_as_agreed: bool = False
    third_party_infringement: bool = False
    followup_improvement: bool = False
    share_agreed: bool = False
    consulting_report_conform: bool = False
    consulting_report_nonconform: bool = False
    decision_loss: bool = False
    new_result: bool = False
    trustee_uses_client_material: bool = False
    client_uses_trustee_result: bool = False
    research_org_no_capacity: bool = False
    authorized_or_ratified: bool = False
    unauthorized_org: bool = False
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "technology_contract": self.technology_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "nature_dispute": self.nature_dispute,
            "development_contract": self.development_contract,
            "commissioned_development": self.commissioned_development,
            "cooperative_development": self.cooperative_development,
            "transfer_contract": self.transfer_contract,
            "license_contract": self.license_contract,
            "consulting_contract": self.consulting_contract,
            "service_contract": self.service_contract,
            "work_or_construction": self.work_or_construction,
            "illegal_monopoly": self.illegal_monopoly,
            "infringe_achievement": self.infringe_achievement,
            "trade_secret_invalid": self.trade_secret_invalid,
            "good_faith_acquirer": self.good_faith_acquirer,
            "reasonable_use_fee": self.reasonable_use_fee,
            "fraud_contract": self.fraud_contract,
            "duty_achievement": self.duty_achievement,
            "non_duty_achievement": self.non_duty_achievement,
            "ownership_dispute": self.ownership_dispute,
            "termination_request": self.termination_request,
            "delayed_main_obligation": self.delayed_main_obligation,
            "urged": self.urged,
            "over_30_days": self.over_30_days,
            "technology_import_export": self.technology_import_export,
            "development_failed": self.development_failed,
            "risk_agreed": self.risk_agreed,
            "no_risk_agreement": self.no_risk_agreement,
            "developer_breach": self.developer_breach,
            "client_breach": self.client_breach,
            "stagnation_delay_failure": self.stagnation_delay_failure,
            "invention_creation": self.invention_creation,
            "patent_agreed": self.patent_agreed,
            "technical_secret_result": self.technical_secret_result,
            "result_agreed": self.result_agreed,
            "licensor_not_owner": self.licensor_not_owner,
            "technology_defective": self.technology_defective,
            "license_not_provided": self.license_not_provided,
            "license_over_scope": self.license_over_scope,
            "fee_unpaid": self.fee_unpaid,
            "licensee_over_scope": self.licensee_over_scope,
            "licensee_as_agreed": self.licensee_as_agreed,
            "third_party_infringement": self.third_party_infringement,
            "followup_improvement": self.followup_improvement,
            "share_agreed": self.share_agreed,
            "consulting_report_conform": self.consulting_report_conform,
            "consulting_report_nonconform": self.consulting_report_nonconform,
            "decision_loss": self.decision_loss,
            "new_result": self.new_result,
            "trustee_uses_client_material": self.trustee_uses_client_material,
            "client_uses_trustee_result": self.client_uses_trustee_result,
            "research_org_no_capacity": self.research_org_no_capacity,
            "authorized_or_ratified": self.authorized_or_ratified,
            "unauthorized_org": self.unauthorized_org,
            "notes": self.notes,
        }


def _format_technology_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: TechnologyFacts,
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


def extract_technology_facts(case_text: str) -> TechnologyFacts:
    config = get_technology_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = TechnologyFacts(raw_text=raw_text)

    for field_name in (
        "technology_contract", "third_party_tort", "nature_dispute", "development_contract",
        "commissioned_development", "cooperative_development", "transfer_contract",
        "license_contract", "consulting_contract", "service_contract", "work_or_construction",
        "illegal_monopoly", "infringe_achievement", "trade_secret_invalid",
        "good_faith_acquirer", "fraud_contract", "duty_achievement", "non_duty_achievement",
        "ownership_dispute", "termination_request", "delayed_main_obligation", "urged",
        "over_30_days", "technology_import_export", "development_failed", "risk_agreed",
        "no_risk_agreement", "developer_breach", "client_breach", "stagnation_delay_failure",
        "invention_creation", "patent_agreed", "technical_secret_result", "result_agreed",
        "licensor_not_owner", "technology_defective", "license_not_provided",
        "license_over_scope", "fee_unpaid", "licensee_over_scope", "licensee_as_agreed",
        "third_party_infringement", "followup_improvement", "share_agreed",
        "consulting_report_conform", "consulting_report_nonconform", "decision_loss",
        "new_result", "trustee_uses_client_material", "client_uses_trustee_result",
        "research_org_no_capacity", "authorized_or_ratified", "unauthorized_org",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.reasonable_use_fee = _extract_money_near(text, config.get_terms("reasonable_use_fee"))

    if any(
        (
            facts.development_contract, facts.transfer_contract, facts.license_contract,
            facts.consulting_contract, facts.service_contract, facts.ownership_dispute,
            facts.illegal_monopoly, facts.infringe_achievement, facts.technology_import_export,
            facts.followup_improvement, facts.new_result,
        )
    ):
        facts.technology_contract = True
    return facts


def _procedure_findings(facts: TechnologyFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("技术合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告通常为技术合同当事人，包括委托人、研究开发人、让与人、许可人、受让人、被许可人、咨询人或服务人")
    return findings


def _has_substantive_dispute(facts: TechnologyFacts) -> bool:
    return any(
        (
            facts.nature_dispute, facts.development_contract, facts.transfer_contract,
            facts.license_contract, facts.consulting_contract, facts.service_contract,
            facts.illegal_monopoly, facts.infringe_achievement, facts.fraud_contract,
            facts.ownership_dispute, facts.termination_request, facts.technology_import_export,
            facts.development_failed, facts.invention_creation, facts.technical_secret_result,
            facts.followup_improvement, facts.new_result, facts.research_org_no_capacity,
        )
    )


def _only_procedure_question(facts: TechnologyFacts) -> bool:
    return (facts.asks_jurisdiction or facts.asks_defendant) and not _has_substantive_dispute(facts)


def _type_conclusion(facts: TechnologyFacts) -> str:
    if facts.development_contract or facts.commissioned_development or facts.cooperative_development:
        return "技术开发合同"
    if facts.transfer_contract:
        return "技术转让合同"
    if facts.license_contract:
        return "技术许可合同"
    if facts.consulting_contract:
        return "技术咨询合同"
    if facts.service_contract:
        return "技术服务合同"
    return "技术合同"


def adjudicate_technology(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_technology_config()
    facts = extract_technology_facts(case_text)
    today = today or date.today()
    procedure_findings = _procedure_findings(facts)
    path = ["入口程序校验"]

    if _only_procedure_question(facts):
        major = "技术合同纠纷适用合同纠纷管辖和适格当事人规则；合同有有效管辖约定的，按约定处理。"
        minor = "本案主要询问起诉法院或应列被告，未提出需要实体裁判的技术成果、合同效力或违约争议。"
        conclusion = "按程序事项处理：" + "；".join(procedure_findings)
        return _format_technology_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "技术合同纠纷通常适用三年诉讼时效。"
        minor = f"本案可识别的合同或履行日期为 {facts.contract_date.isoformat()}，距今已超过三年，且未识别到中止、中断或延长事由。"
        conclusion = "诉讼时效已过，超过时效部分不予支持。"
        return _format_technology_output(major, minor, conclusion, ["诉讼时效"], facts, [*path, "诉讼时效"], procedure_findings)

    if facts.research_org_no_capacity:
        triggered = [config.patch_name("T14", "不具有民事主体资格的科研组织订立合同的责任承担")]
        major = "不具有民事主体资格的科研组织订立技术合同，经法人或非法人组织授权或认可的，由该组织承担责任；未经授权或认可的，由科研组织成员共同承担责任，受益组织在受益范围内承担相应责任。"
        if facts.authorized_or_ratified:
            minor = "本案由不具有民事主体资格的科研组织订立技术合同，但已经法人或非法人组织授权或认可。"
            conclusion = "科研组织订立合同，责任由授权组织承担。"
        else:
            minor = "本案由不具有民事主体资格的科研组织订立技术合同，未识别授权或认可事实。"
            conclusion = "科研组织订立合同，责任由成员共同承担；受益组织在受益范围内承担相应责任。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, [*path, "适格被告"], procedure_findings)

    if facts.third_party_tort and not facts.technology_contract:
        major = "第三人侵害技术成果或其他民事权益的，按侵权责任规则处理；技术合同引擎处理合同相对方之间的履行争议。"
        minor = "本案主要事实指向合同外第三人侵权，未能识别技术合同履行争议。"
        conclusion = "本案涉及侵权责任，非技术合同纠纷，不适用本技术合同裁判引擎。"
        return _format_technology_output(major, minor, conclusion, [], facts, [*path, "侵权第三方分流"], procedure_findings)

    path.append("前置实体判断")

    if facts.nature_dispute or facts.work_or_construction:
        triggered = [config.patch_name("T1", "技术合同类型认定")]
        major = "技术合同应根据实质内容认定类型：研究开发新技术为技术开发，现有技术权利让与为技术转让，许可实施使用为技术许可，可行性论证等为技术咨询，以技术知识解决特定技术问题为技术服务；技术服务不包括承揽合同和建设工程合同。"
        if facts.work_or_construction:
            minor = "本案实质更接近承揽或建设工程合同，并非以技术开发、转让、许可、咨询或服务为核心。"
            conclusion = "本案不宜按技术合同处理，应按实际法律关系适用相应裁判规则。"
        else:
            contract_kind = _type_conclusion(facts)
            minor = f"本案争议需按合同标的和履行内容识别技术合同类型，现有事实指向{contract_kind}。"
            conclusion = f"合同性质认定为{contract_kind}，适用相应裁判规则。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, [*path, "合同类型识别"], procedure_findings)

    if facts.technology_import_export:
        major = "技术进出口合同，法律、行政法规另有规定的，依照其规定。"
        minor = "本案技术合同涉及技术进出口。"
        conclusion = "本案涉及技术进出口，优先适用技术进出口相关法律法规。"
        return _format_technology_output(major, minor, conclusion, [config.patch_name("T15", "技术进出口合同的特殊规定")], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.fraud_contract:
        major = "一方以现有技术成果冒充研究开发标的订立委托开发合同收取费用，或就同一研究开发课题重复订立合同收费，使对方违背真实意思订立合同的，受损害方可以请求撤销合同。"
        minor = "本案存在以现有技术冒充委托开发、同一课题重复收费等欺诈订立技术合同情形。"
        conclusion = "存在欺诈订立情形，受损害方可以请求撤销合同。"
        return _format_technology_output(major, minor, conclusion, [config.patch_name("T13", "欺诈订立技术合同的撤销")], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.trade_secret_invalid or (facts.infringe_achievement and facts.good_faith_acquirer):
        triggered = [config.patch_name("T11", "侵害技术秘密合同被确认无效后的善意使用")]
        major = "侵害他人技术秘密的技术合同被确认无效后，善意取得该技术秘密的一方可以在取得时的范围内继续使用，但应支付合理使用费并承担保密义务；非善意取得的，不得继续使用。"
        if facts.good_faith_acquirer:
            minor = f"本案侵害技术秘密的合同被确认无效，取得方为善意，可识别合理使用费为 {_money(facts.reasonable_use_fee)}。"
            conclusion = f"善意取得方可以继续在原范围内使用技术秘密，应支付合理使用费 {_money(facts.reasonable_use_fee)} 并承担保密义务。"
        else:
            minor = "本案侵害技术秘密的合同被确认无效，未能识别取得方为善意。"
            conclusion = "取得方不可以继续使用技术秘密，并应停止使用、承担相应责任。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.illegal_monopoly:
        major = "非法垄断技术或者侵害他人技术成果的技术合同无效。限制对方在合同标的技术基础上进行新研究开发、限制从其他渠道吸收技术、阻碍合理实施专利和使用技术秘密等，属于非法垄断技术的重要表现。"
        minor = "本案技术合同存在限制技术竞争或技术发展的条款。"
        conclusion = "合同构成非法垄断技术，无效。"
        return _format_technology_output(major, minor, conclusion, [config.patch_name("T3", "非法垄断技术的认定")], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.infringe_achievement:
        major = "非法垄断技术或者侵害他人技术成果的技术合同无效。"
        minor = "本案合同标的侵害他人专利、技术秘密或其他技术成果。"
        conclusion = "技术合同无效；因无效取得的财产应依法返还，造成损失的按过错承担责任。"
        return _format_technology_output(major, minor, conclusion, ["侵害他人技术成果"], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.ownership_dispute or facts.duty_achievement or facts.non_duty_achievement:
        triggered = [config.patch_name("T2", "职务技术成果 vs 非职务技术成果的认定")]
        major = "执行单位工作任务，或主要利用单位资金、设备、器材等物质技术条件并对成果有实质影响完成的技术成果，属于职务技术成果，使用权、转让权归单位；非职务技术成果的使用权、转让权归完成技术成果的个人。"
        if facts.duty_achievement and not facts.non_duty_achievement:
            minor = "本案技术成果系执行单位工作任务或主要利用单位物质技术条件完成。"
            conclusion = "该技术成果属于职务技术成果，权属归单位。"
        elif facts.non_duty_achievement:
            minor = "本案技术成果由个人完成，未识别执行单位任务或主要利用单位物质技术条件。"
            conclusion = "该技术成果不属于职务技术成果，权属归个人。"
        else:
            minor = "本案存在技术成果权属争议，但工作任务、单位物质条件利用情况仍不完整。"
            conclusion = "需补充是否执行单位工作任务、是否主要利用单位物质技术条件后，再认定权属归单位或个人。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, [*path, "技术成果权属"], procedure_findings)

    if facts.termination_request:
        triggered = [config.patch_name("T10", "技术合同解除的催告期限")]
        major = "技术合同一方迟延履行主要债务，经催告后在30日内仍未履行的，另一方可以主张解除合同。"
        if facts.delayed_main_obligation and facts.urged and facts.over_30_days:
            minor = "本案一方迟延履行主要债务，另一方已经催告，超过30日仍未履行。"
            conclusion = "一方迟延履行主要债务，经催告后超过30日仍未履行，另一方可以解除合同。"
        else:
            minor = "本案存在解除技术合同主张，但迟延履行主要债务、催告和30日未履行事实仍不完整。"
            conclusion = "现有事实不足以支持解除；需证明迟延履行主要债务、已经催告且30日内仍未履行。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, [*path, "合同解除审查"], procedure_findings)

    path.append("技术开发合同")

    if facts.development_failed:
        triggered = [config.patch_name("T4", "技术开发合同的风险分担")]
        major = "技术开发未能成功的风险，有约定的按约定；没有约定或者约定不明的，根据各方投入、过错和公平原则合理分担。"
        if facts.risk_agreed:
            minor = "本案技术开发失败，但合同已有风险分担约定。"
            conclusion = "技术开发失败，风险按约定分担。"
        else:
            minor = "本案技术开发失败，未识别明确风险分担约定。"
            conclusion = "技术开发失败，风险由各方根据投入、过错等因素合理分担。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.invention_creation or (facts.commissioned_development and facts.patent_agreed):
        triggered = [config.patch_name("T5", "委托开发成果的专利申请权归属")]
        major = "委托开发完成的发明创造，除当事人另有约定外，申请专利的权利属于研究开发人；研究开发人取得专利权的，委托人可以依法实施该专利。"
        if facts.patent_agreed:
            minor = "本案委托开发成果专利申请权已有约定。"
            conclusion = "委托开发成果的专利申请权按约定归属，委托人是否可以实施该专利按约定处理。"
        else:
            minor = "本案为委托开发完成的发明创造，未识别专利申请权特别约定。"
            conclusion = "委托开发成果的专利申请权归研究开发人，委托人可以依法实施该专利。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.technical_secret_result:
        triggered = [config.patch_name("T6", "技术秘密成果的使用权/转让权归属")]
        major = "委托开发或合作开发完成的技术秘密成果，使用权、转让权和收益分配有约定的按约定；没有约定或约定不明的，双方均有使用和转让的权利。"
        if facts.result_agreed:
            minor = "本案技术秘密成果的使用权、转让权或收益分配已有约定。"
            conclusion = "技术秘密成果的使用权/转让权按约定处理。"
        else:
            minor = "本案为委托开发或合作开发完成的技术秘密成果，未识别明确权属约定。"
            conclusion = "技术秘密成果的使用权/转让权归双方共有，双方均有使用和转让的权利。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.developer_breach or facts.client_breach:
        major = "委托开发或合作开发合同中，一方违反约定造成研究开发工作停滞、延误或者失败的，应承担违约责任。"
        if facts.developer_breach:
            minor = "本案研究开发人未按期完成、未交付成果或未合理使用经费。"
            conclusion = "研究开发人应承担违约责任；造成停滞、延误或失败的，应赔偿相应损失。"
        else:
            minor = "本案委托人未支付经费、未提供资料、未完成协作或不接受成果。"
            conclusion = "委托人应承担违约责任；已影响研发工作的，应赔偿相应损失。"
        return _format_technology_output(major, minor, conclusion, ["技术开发违约责任"], facts, path, procedure_findings)

    path.append("技术转让与许可合同")

    if facts.third_party_infringement and (facts.license_contract or facts.licensee_as_agreed):
        triggered = [config.patch_name("T7", "技术许可合同侵权责任的承担")]
        major = "受让人或被许可人按约定实施专利、使用技术秘密侵害他人合法权益的，由让与人或许可人承担责任；但当事人另有约定或被许可人超范围使用的除外。"
        if facts.licensee_over_scope:
            minor = "本案被许可人超越约定范围使用技术并侵害他人合法权益。"
            conclusion = "被许可人超出约定范围使用，侵权责任由被许可人自行承担。"
        else:
            minor = "本案被许可人按约定实施专利或使用技术秘密，但侵害他人合法权益。"
            conclusion = "被许可人按约定实施/使用，侵权责任由让与人或许可人承担。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.followup_improvement:
        triggered = [config.patch_name("T12", "后续改进成果的归属")]
        major = "一方后续改进的技术成果，有约定的按约定；没有约定或者约定不明的，其他各方无权分享。"
        if facts.share_agreed:
            minor = "本案后续改进成果已有分享约定。"
            conclusion = "后续改进成果按约定分享，他方有权按约定分享。"
        else:
            minor = "本案一方完成后续改进成果，未识别分享约定。"
            conclusion = "后续改进成果归改进方，他方无权分享。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.licensor_not_owner or facts.technology_defective or facts.license_not_provided or facts.license_over_scope:
        major = "技术转让合同的让与人和技术许可合同的许可人，应保证自己是所提供技术的合法拥有者，并保证技术完整、无误、有效，能够达到约定目标；未按约定许可技术或超范围许可的，应返还部分或全部使用费并承担违约责任。"
        minor = "本案让与人或许可人未能保证技术权利、技术有效性，或未按约定许可技术。"
        conclusion = "让与人或许可人构成违约，应返还部分或全部使用费，并承担违约责任。"
        return _format_technology_output(major, minor, conclusion, ["让与人/许可人违约"], facts, path, procedure_findings)

    if facts.fee_unpaid or facts.licensee_over_scope:
        major = "被许可人未按约定支付使用费的，应补交使用费并支付违约金；超越约定范围使用或擅自许可第三人的，应停止违约行为并承担违约责任。"
        if facts.fee_unpaid:
            minor = "本案被许可人未按约定支付使用费。"
            conclusion = "被许可人应补交使用费并支付违约金。"
        else:
            minor = "本案被许可人超越约定范围使用或擅自许可第三人。"
            conclusion = "被许可人应停止违约行为并承担违约责任。"
        return _format_technology_output(major, minor, conclusion, ["被许可人违约"], facts, path, procedure_findings)

    path.append("技术咨询与服务合同")

    if facts.decision_loss:
        triggered = [config.patch_name("T8", "技术咨询合同决策风险承担")]
        major = "技术咨询合同中，委托人按受托人符合要求的咨询报告作出决策造成损失的，由委托人承担；报告不符合约定的，受托人承担减收或免收报酬等违约责任。"
        if facts.consulting_report_nonconform:
            minor = "本案咨询报告不符合约定要求，委托人据此决策造成损失。"
            conclusion = "受托人应承担违约责任，可减收或免收报酬；决策损失按报告不合格与损失之间的因果关系处理。"
        else:
            minor = "本案委托人按符合要求的咨询报告作出决策后发生损失。"
            conclusion = "委托人按符合要求的咨询报告作出决策造成损失，由委托人承担。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.new_result:
        triggered = [config.patch_name("T9", "技术咨询/服务合同的新技术成果归属")]
        major = "技术咨询合同、技术服务合同履行过程中，受托人利用委托人提供的技术资料和工作条件完成的新技术成果，属于受托人；委托人利用受托人的工作成果完成的新技术成果，属于委托人；另有约定的除外。"
        if facts.client_uses_trustee_result:
            minor = "本案新技术成果由委托人利用受托人的工作成果完成。"
            conclusion = "新技术成果归委托人所有。"
        else:
            minor = "本案新技术成果由受托人利用委托人提供的技术资料和工作条件完成。"
            conclusion = "新技术成果归受托人所有。"
        return _format_technology_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.consulting_report_nonconform:
        major = "技术咨询合同中，受托人未按期提出咨询报告或者报告不符合约定的，应承担减收或免收报酬等违约责任。"
        minor = "本案咨询报告不符合约定要求。"
        conclusion = "受托人应承担违约责任，减收或免收报酬。"
        return _format_technology_output(major, minor, conclusion, ["技术咨询违约责任"], facts, path, procedure_findings)

    if facts.service_contract:
        major = "技术服务合同是以技术知识为对方解决特定技术问题的合同，不包括承揽合同和建设工程合同。受托人未按约完成服务工作的，应承担免收报酬等违约责任；委托人不履行义务的，已付报酬不得追回，未付报酬应支付。"
        minor = "本案事实指向技术服务合同。"
        conclusion = "应按技术服务合同规则处理服务质量、报酬支付和新技术成果归属等争议。"
        return _format_technology_output(major, minor, conclusion, [config.patch_name("T1", "技术合同类型认定")], facts, path, procedure_findings)

    if facts.technology_contract:
        major = "技术合同是当事人就技术开发、转让、许可、咨询或者服务订立的确立相互权利义务的合同，应保护知识产权并促进技术进步。"
        minor = "本案能够识别技术合同关系，但未识别足以触发效力、权属、开发失败、转让许可违约、咨询服务风险或解除的具体争议。"
        conclusion = "技术合同继续有效，各方应按合同履行；如主张违约或权属确认，需进一步补充合同类型、技术成果、交付、使用费、保密或履行迟延等事实。"
    else:
        major = "技术合同裁判需先识别合同标的是技术开发、转让、许可、咨询还是技术服务。"
        minor = "现有自然语言事实不足以确认技术合同关系和裁判节点。"
        conclusion = "请补充合同类型、技术成果内容、权属约定、交付使用、使用费和违约事实后再裁判。"
    return _format_technology_output(major, minor, conclusion, [], facts, path, procedure_findings)
