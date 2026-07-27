"""Property-management contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import (
    _extract_money_near,
    _format_output,
    _mentions,
)
from adjudicate.property_configs import PropertyManagementConfig, get_property_config


@dataclass(frozen=True)
class FeePeriod:
    start_year: int
    start_month: int
    end_year: int
    end_month: int

    def to_public_dict(self) -> Dict[str, int]:
        return {
            "start_year": self.start_year,
            "start_month": self.start_month,
            "end_year": self.end_year,
            "end_month": self.end_month,
        }


@dataclass
class PropertyFacts:
    raw_text: str
    contract_type: str = "property_management"
    contract_type_name: str = "物业服务合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    property_fee_dispute: bool = False
    fee_periods: List[FeePeriod] = field(default_factory=list)
    developer_contract: bool = False
    owners_committee_contract: bool = False
    owner_not_signed_defense: bool = False
    illegal_collection: bool = False
    dismissal_dispute: bool = False
    owners_meeting_valid: bool = False
    owners_meeting_invalid: bool = False
    notice_60_days: bool = False
    service_provided: bool = False
    service_defect: bool = False
    minor_defect: bool = False
    general_defect: bool = False
    serious_defect: bool = False
    property_responsibility: bool = False
    building_structure_issue: bool = False
    third_party_tort: bool = False
    owner_no_living_defense: bool = False
    owner_no_accept_defense: bool = False
    public_income_dispute: bool = False
    public_income_amount: float = 0.0
    management_cost: float = 0.0
    property_fee_amount: float = 0.0
    no_written_contract: bool = False
    actual_property_service: bool = False
    long_accept_no_objection: bool = False
    contract_terminated: bool = False
    original_property_refuses_exit: bool = False
    original_property_refuses_handover: bool = False
    original_property_exited: bool = False
    post_termination_fee: bool = False
    property_company_challenges_dismissal: bool = False
    has_intrusive_third_party: bool = False
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "property_fee_dispute": self.property_fee_dispute,
            "fee_periods": [period.to_public_dict() for period in self.fee_periods],
            "developer_contract": self.developer_contract,
            "owners_committee_contract": self.owners_committee_contract,
            "owner_not_signed_defense": self.owner_not_signed_defense,
            "illegal_collection": self.illegal_collection,
            "dismissal_dispute": self.dismissal_dispute,
            "owners_meeting_valid": self.owners_meeting_valid,
            "owners_meeting_invalid": self.owners_meeting_invalid,
            "notice_60_days": self.notice_60_days,
            "service_provided": self.service_provided,
            "service_defect": self.service_defect,
            "minor_defect": self.minor_defect,
            "general_defect": self.general_defect,
            "serious_defect": self.serious_defect,
            "property_responsibility": self.property_responsibility,
            "building_structure_issue": self.building_structure_issue,
            "third_party_tort": self.third_party_tort,
            "owner_no_living_defense": self.owner_no_living_defense,
            "owner_no_accept_defense": self.owner_no_accept_defense,
            "public_income_dispute": self.public_income_dispute,
            "public_income_amount": self.public_income_amount,
            "management_cost": self.management_cost,
            "property_fee_amount": self.property_fee_amount,
            "no_written_contract": self.no_written_contract,
            "actual_property_service": self.actual_property_service,
            "long_accept_no_objection": self.long_accept_no_objection,
            "contract_terminated": self.contract_terminated,
            "original_property_refuses_exit": self.original_property_refuses_exit,
            "original_property_refuses_handover": self.original_property_refuses_handover,
            "original_property_exited": self.original_property_exited,
            "post_termination_fee": self.post_termination_fee,
            "property_company_challenges_dismissal": self.property_company_challenges_dismissal,
            "has_intrusive_third_party": self.has_intrusive_third_party,
            "notes": self.notes,
        }


def _format_property_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: PropertyFacts,
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


def _month_index(year: int, month: int) -> int:
    return year * 12 + month


def _month_text(index: int) -> str:
    year = index // 12
    month = index % 12
    if month == 0:
        year -= 1
        month = 12
    return f"{year}年{month}月"


def _period_text(start_index: int, end_index: int) -> str:
    return f"{_month_text(start_index)}—{_month_text(end_index)}"


def _extract_fee_periods(text: str) -> List[FeePeriod]:
    pattern = re.compile(
        r"(?P<sy>20\d{2})年(?P<sm>\d{1,2})月"
        r"(?:至|到|—|-)"
        r"(?:(?P<ey>20\d{2})年)?(?P<em>\d{1,2})月"
    )
    periods: List[FeePeriod] = []
    for match in pattern.finditer(text):
        sy = int(match.group("sy"))
        sm = int(match.group("sm"))
        ey = int(match.group("ey") or sy)
        em = int(match.group("em"))
        if 1 <= sm <= 12 and 1 <= em <= 12 and _month_index(sy, sm) <= _month_index(ey, em):
            periods.append(FeePeriod(sy, sm, ey, em))
    return periods


def _limitation_segments(periods: List[FeePeriod], today: date) -> tuple[List[str], List[str]]:
    cutoff = _month_index(today.year - 3, today.month)
    expired: List[str] = []
    active: List[str] = []
    for period in periods:
        start = _month_index(period.start_year, period.start_month)
        end = _month_index(period.end_year, period.end_month)
        if end < cutoff:
            expired.append(_period_text(start, end))
        elif start >= cutoff:
            active.append(_period_text(start, end))
        else:
            expired.append(_period_text(start, cutoff - 1))
            active.append(_period_text(cutoff, end))
    return expired, active


def _limitation_text(periods: List[FeePeriod], today: date) -> str:
    if not periods:
        return "物业费诉讼时效应逐期计算，需补充欠费起止月份及催缴情形。"

    expired, active = _limitation_segments(periods, today)
    parts: List[str] = []
    if expired:
        parts.append(f"{'、'.join(expired)}已超时效，不支持")
    if active:
        parts.append(f"{'、'.join(active)}未超时效，支持")
    return "物业费诉讼时效逐期计算：" + "；".join(parts) + "。"


def _all_fee_periods_expired(periods: List[FeePeriod], today: date) -> bool:
    if not periods:
        return False
    _, active = _limitation_segments(periods, today)
    return not active


def extract_property_facts(case_text: str) -> PropertyFacts:
    config = get_property_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = PropertyFacts(raw_text=raw_text)

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.property_fee_dispute = _mentions(text, config.get_terms("property_fee_dispute"))
    facts.fee_periods = _extract_fee_periods(text)

    facts.developer_contract = _mentions(text, config.get_terms("developer_contract"))
    facts.owners_committee_contract = _mentions(text, config.get_terms("owners_committee_contract"))
    facts.owner_not_signed_defense = _mentions(text, config.get_terms("owner_not_signed_defense"))
    facts.illegal_collection = _mentions(text, config.get_terms("illegal_collection"))
    facts.dismissal_dispute = _mentions(text, config.get_terms("dismissal_dispute"))
    facts.owners_meeting_valid = _mentions(text, config.get_terms("owners_meeting_valid"))
    facts.owners_meeting_invalid = _mentions(text, config.get_terms("owners_meeting_invalid"))
    facts.notice_60_days = _mentions(text, config.get_terms("notice_60_days"))

    facts.service_provided = _mentions(text, config.get_terms("service_provided"))
    facts.minor_defect = _mentions(text, config.get_terms("minor_defect"))
    facts.general_defect = _mentions(text, config.get_terms("general_defect"))
    facts.serious_defect = _mentions(text, config.get_terms("serious_defect"))
    facts.building_structure_issue = _mentions(text, config.get_terms("building_structure_issue"))
    facts.third_party_tort = _mentions(text, config.get_terms("third_party_tort"))
    facts.service_defect = (
        _mentions(text, config.get_terms("service_defect"))
        or facts.minor_defect
        or facts.general_defect
        or facts.serious_defect
        or facts.building_structure_issue
        or facts.third_party_tort
    )
    facts.property_responsibility = _mentions(text, config.get_terms("property_responsibility")) or (
        facts.service_defect and not (facts.building_structure_issue or facts.third_party_tort)
    )

    facts.owner_no_living_defense = _mentions(text, config.get_terms("owner_no_living_defense"))
    facts.owner_no_accept_defense = _mentions(text, config.get_terms("owner_no_accept_defense"))
    facts.public_income_dispute = _mentions(text, config.get_terms("public_income"))
    facts.public_income_amount = _extract_money_near(text, config.get_terms("public_income") + ("收益",))
    facts.management_cost = _extract_money_near(text, config.get_terms("management_cost"))
    facts.property_fee_amount = _extract_money_near(text, ("物业费", "欠费", "追缴", "物业欠费"))
    facts.no_written_contract = _mentions(text, config.get_terms("no_written_contract"))
    facts.actual_property_service = _mentions(text, config.get_terms("actual_property_service"))
    facts.long_accept_no_objection = _mentions(text, config.get_terms("long_accept_no_objection"))
    facts.contract_terminated = _mentions(text, config.get_terms("contract_terminated"))
    facts.original_property_refuses_exit = _mentions(text, config.get_terms("original_property_refuses_exit"))
    facts.original_property_refuses_handover = _mentions(text, config.get_terms("original_property_refuses_handover"))
    facts.original_property_exited = _mentions(text, config.get_terms("original_property_exited"))
    facts.post_termination_fee = _mentions(text, config.get_terms("post_termination_fee"))
    facts.property_company_challenges_dismissal = _mentions(text, config.get_terms("property_company_challenges_dismissal"))
    facts.has_intrusive_third_party = facts.third_party_tort and not (
        facts.property_fee_dispute or facts.service_defect or facts.public_income_dispute
    )
    return facts


def _procedure_findings(facts: PropertyFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("物业服务合同纠纷由不动产所在地人民法院处理，即房屋所在地人民法院")
    if facts.asks_defendant:
        findings.append("适格被告为业主本人；物业服务合同虽可由建设单位或业主委员会签订，但依法约束全体业主")
    return findings


def _only_procedure_question(facts: PropertyFacts) -> bool:
    return (
        (facts.asks_jurisdiction or facts.asks_defendant)
        and not facts.property_fee_dispute
        and not facts.owner_not_signed_defense
        and not facts.illegal_collection
        and not facts.dismissal_dispute
        and not facts.service_defect
        and not facts.public_income_dispute
        and not facts.no_written_contract
        and not facts.contract_terminated
        and not facts.property_company_challenges_dismissal
        and not facts.has_intrusive_third_party
    )


def _with_limitation(conclusion: str, limitation: str | None) -> str:
    return f"{conclusion}；{limitation}" if limitation else conclusion


def _public_income_output(
    facts: PropertyFacts,
    triggered: List[str],
    path: List[str],
    procedure_findings: List[str],
) -> Dict[str, Any]:
    triggered = [*triggered, "公共收益归属"]
    path = [*path, "公共收益归属"]
    major = "小区公共区域经营收益由全体业主共有，物业公司仅可在能够举证的范围内扣除合理管理成本，不得擅自占有。"
    minor = "识别到争议涉及电梯广告、地面停车费、公共场地出租等公共区域经营收益。"
    if facts.public_income_amount > 0:
        amount = max(facts.public_income_amount - facts.management_cost, 0)
        if facts.management_cost > 0:
            minor += f"识别到公共收益{facts.public_income_amount:.2f}元，物业主张或事实中出现管理成本{facts.management_cost:.2f}元。"
        conclusion = f"公共收益归全体业主共有，物业应返还 {amount:.2f} 元或抵扣物业费。"
    else:
        conclusion = "公共收益归全体业主共有，物业应返还相应金额或抵扣物业费；具体金额需补充收益账目和合理管理成本证据。"
    return _format_property_output(major, minor, conclusion, triggered, facts, path, procedure_findings)


def adjudicate_property_management(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    facts = extract_property_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "物业服务合同纠纷的程序事项应先审查管辖法院和适格被告；物业服务合同依法约束业主。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出需要继续审查物业费、服务瑕疵、催收方式、解聘或公共收益的事实。"
        conclusion = "；".join(procedure_findings)
        return _format_property_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.has_intrusive_third_party:
        major = "物业服务合同裁判引擎处理物业服务合同项下的服务、收费和合同效力争议；单纯第三方侵权应按侵权责任另行处理。"
        minor = "识别到争议核心是邻居、外人等第三方侵权，未识别到物业费、物业服务瑕疵或公共收益争议。"
        conclusion = "本案涉及侵权责任，非物业服务合同纠纷，不适用本物业服务合同裁判引擎"
        return _format_property_output(major, minor, conclusion, [], facts, path, procedure_findings)

    limitation: str | None = None
    if facts.property_fee_dispute:
        triggered.append("诉讼时效逐期计算")
        limitation = _limitation_text(facts.fee_periods, today)
        if _all_fee_periods_expired(facts.fee_periods, today):
            major = "物业费属于定期缴纳的独立债务，每一期物业费分别适用三年诉讼时效。"
            minor = "识别到物业公司起诉或催缴多期物业费，且欠费期次均已超过三年诉讼时效。"
            conclusion = limitation
            return _format_property_output(major, minor, conclusion, triggered, facts, [*path, "诉讼时效"], procedure_findings)

    path.append("前置实体判断")
    if facts.owner_not_signed_defense or facts.developer_contract or facts.owners_committee_contract:
        major = "《民法典》第939条规定，建设单位依法订立的前期物业服务合同，以及业主委员会依法与物业服务人订立的物业服务合同，对业主具有法律约束力。"
        minor = "识别到物业服务合同由建设单位或业主委员会签订，或业主以合同不是本人签署为由抗辩。"
        if facts.owner_not_signed_defense and not facts.service_defect and not facts.illegal_collection and not facts.dismissal_dispute:
            conclusion = _with_limitation("业主以“不是我签的合同”为由拒交物业费的抗辩不成立，物业服务合同对业主具有法律约束力", limitation)
            return _format_property_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查"], procedure_findings)

    if facts.no_written_contract:
        triggered.append("事实物业服务关系")
        major = "物业公司虽未与业主签订书面物业服务合同，但已实际提供主要物业服务，业主长期接受服务且未提出异议的，可以认定双方形成事实上的物业服务合同关系。"
        if facts.actual_property_service and facts.long_accept_no_objection:
            minor = "识别到未签书面物业服务合同，但物业公司已实际提供保洁、安保、设施维护等主要服务，业主长期接受且未提出异议。"
            conclusion = _with_limitation("双方形成事实上的物业服务合同关系，业主仍应支付物业费", limitation)
        else:
            minor = "识别到未签书面物业服务合同，但未同时稳定识别物业公司实际履行主要服务义务以及业主长期接受且未提出异议。"
            conclusion = "事实物业服务合同关系不成立，物业费无依据，无需缴纳。"
        return _format_property_output(major, minor, conclusion, triggered, facts, [*path, "合同效力审查", "事实物业服务关系"], procedure_findings)

    if facts.illegal_collection:
        triggered.append("催收方式合法性审查")
        major = "物业服务人不得以停止供水、供电、停用门禁卡、停用电梯等方式催交物业费；业主欠费应通过书面催缴、诉讼等合法方式处理。"
        minor = "识别到物业采取或被业主主张采取停水、停电、停门禁、停电梯等方式催收物业费。"
        conclusion = "催收方式违法，物业不得以该方式催费，但物业费本体仍需缴纳。"
        return _format_property_output(major, minor, conclusion, triggered, facts, [*path, "物业费催收方式合法性"], procedure_findings)

    if facts.dismissal_dispute:
        if facts.property_company_challenges_dismissal and facts.owners_meeting_valid:
            triggered.append("物业公司对业主大会解聘决定无诉权")
            major = "业主大会依法作出的解聘物业公司决定属于业主共同管理事项；物业服务人并非小区业主，无权请求人民法院就业主大会解聘决定效力作出裁判。"
            minor = "识别到业主大会已经依法作出解聘物业公司的决定，物业公司起诉要求撤销该解聘决定。"
            conclusion = "物业公司无权起诉要求撤销业主大会解聘决定，法院驳回起诉。"
            return _format_property_output(major, minor, conclusion, triggered, facts, [*path, "合同解除/解聘"], procedure_findings)

        triggered.append("解聘程序合法性审查")
        major = "《民法典》第278条规定，选聘和解聘物业服务企业应由业主共同决定；第946条规定，业主依法定程序共同决定解聘物业服务人的，可以解除物业服务合同，并应提前六十日书面通知。"
        minor = "识别到业主主张已解聘物业，或物业主张解聘无效。"
        if facts.contract_terminated and (facts.original_property_refuses_exit or facts.original_property_refuses_handover or facts.post_termination_fee):
            triggered.append("合同终止后交接僵局")
            major = "《民法典》第949条规定，物业服务合同终止的，原物业服务人应当在约定期限或者合理期限内退出物业服务区域，将物业服务用房、相关设施、物业服务所必需的相关资料等交还业主委员会、决定自行管理的业主或者其指定的人。"
            if facts.original_property_refuses_exit:
                minor = "识别到物业服务合同已经依法终止，但原物业公司拒不退场，并主张合同终止后的物业费。"
                conclusion = "原物业公司拒不退场，合同终止后的物业费不予支持；拒不移交资料造成业主损失的，原物业公司应承担赔偿责任。"
            elif facts.original_property_refuses_handover:
                minor = "识别到物业服务合同已经依法终止，原物业公司拒绝移交相关设施、档案或服务资料。"
                conclusion = "原物业公司应退出物业服务区域并移交相关设施和资料；拒不移交造成业主损失的，应承担赔偿责任。"
            else:
                minor = "识别到物业服务合同已经依法终止，原物业公司主张合同终止后的物业费。"
                conclusion = "原物业公司只能主张合同终止前依法产生的物业费；合同终止后的物业费是否支持，取决于其是否依法退场并完成交接。"
            return _format_property_output(major, minor, conclusion, triggered, facts, [*path, "合同解除/解聘", "合同终止后交接"], procedure_findings)
        if facts.owners_meeting_valid:
            conclusion = "解聘程序合法，解聘有效；业主大会应提前60日书面通知物业。物业公司无权起诉挑战业主大会依法选聘新物业决定的效力。"
        elif facts.owners_meeting_invalid:
            conclusion = "解聘程序不合法，解聘无效。未经业主大会依法表决或程序违法的，不能产生解聘物业公司的效力。"
        else:
            conclusion = "需审查是否经业主大会依法定程序共同决定；程序合法的，解聘有效并须提前60日书面通知，程序不合法的，解聘无效。"
        return _format_property_output(major, minor, conclusion, triggered, facts, [*path, "合同解除/解聘"], procedure_findings)

    if facts.contract_terminated and (facts.original_property_refuses_exit or facts.original_property_refuses_handover or facts.post_termination_fee):
        triggered.append("合同终止后交接僵局")
        major = "《民法典》第949条规定，物业服务合同终止后，原物业服务人应当退出物业服务区域，并移交相关设施和资料。"
        if facts.original_property_refuses_exit:
            minor = "识别到物业服务合同已经到期或依法终止，但原物业公司拒不退出物业服务区域。"
            conclusion = "原物业公司拒不退场，合同终止后的物业费不予支持；拒不移交资料造成业主损失的，原物业公司应承担赔偿责任。"
        elif facts.original_property_refuses_handover:
            minor = "识别到物业服务合同已经到期或依法终止，但原物业公司拒绝移交相关资料。"
            conclusion = "原物业公司应退出并移交相关设施和资料；拒不移交资料造成业主损失的，应承担赔偿责任。"
        else:
            minor = "识别到物业服务合同已经终止，原物业公司主张合同终止后的物业费。"
            conclusion = "合同终止后的物业费原则上不予支持；原物业公司可主张合同终止前已经产生且未超过诉讼时效的物业费。"
        return _format_property_output(major, minor, conclusion, triggered, facts, [*path, "合同解除/解聘", "合同终止后交接"], procedure_findings)

    path.append("物业费应缴金额")
    fee_major = "《民法典》第944条规定，业主应按约定向物业服务人支付物业费；物业已按约定和有关规定提供服务的，业主不得以未接受或者无需接受相关物业服务为由拒绝支付物业费。"

    if facts.owner_no_living_defense or facts.owner_no_accept_defense:
        minor = "识别到业主以未入住、房屋空置、未接受服务或无需接受服务为由拒交物业费。"
        conclusion = _with_limitation("该抗辩不成立；物业已面向小区公共区域和全体业主提供服务的，业主应缴纳物业费", limitation)
        return _format_property_output(fee_major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.service_defect:
        path.append("瑕疵程度判断")
        defect_major = "《民法典》第942条规定，物业服务人应按约定和物业使用性质，妥善维修、养护、清洁、绿化和经营管理物业服务区域内的共有部分，维护基本秩序。"
        if facts.building_structure_issue or facts.third_party_tort:
            minor = "识别到业主主张的瑕疵属于房屋主体结构问题或第三方侵权，并非物业服务职责范围内的服务不达标。"
            conclusion = _with_limitation("该瑕疵不属于物业责任，不支持以此减免物业费", limitation)
            return _format_property_output(defect_major, minor, conclusion, triggered, facts, [*path, "瑕疵责任归属"], procedure_findings)

        if facts.minor_defect:
            minor = "识别到瑕疵属于个别角落清洁不到位、维修响应稍慢等局部轻微问题，未实质影响正常居住生活。"
            conclusion = _with_limitation("轻微瑕疵不影响物业费缴纳，业主不能据此拒交或减免物业费", limitation)
        elif facts.general_defect:
            minor = "识别到多处物业服务不达标，但尚未严重影响业主正常生活。"
            conclusion = _with_limitation("一般瑕疵可酌情减免部分物业费，通常可在10%-30%范围内由法院结合证据裁量", limitation)
        elif facts.serious_defect:
            minor = "识别到物业服务严重缺失，已经严重影响业主正常生活。"
            conclusion = _with_limitation("严重瑕疵可主张减免相应物业费，具体比例需结合服务缺失范围、持续时间和影响程度确定", limitation)
        else:
            minor = "识别到物业服务存在不到位或不达标事实，但现有事实不足以稳定区分轻微、一般或严重瑕疵。"
            conclusion = _with_limitation("可按瑕疵程度酌情审查是否减免物业费；需补充服务缺失范围、持续时间和影响程度", limitation)
        return _format_property_output(defect_major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.public_income_dispute:
        return _public_income_output(facts, triggered, [*path, "独立分支"], procedure_findings)

    if facts.service_provided or facts.property_fee_dispute:
        minor = "未识别到物业服务存在可归责于物业公司的实质性瑕疵，或业主仅提出未接受、无需接受服务等抗辩。"
        conclusion = _with_limitation("业主应全额缴纳未超过诉讼时效期间的物业费", limitation)
        return _format_property_output(fee_major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "物业服务合同纠纷应围绕合同效力、催收方式、解聘程序、物业服务是否达标、瑕疵程度和物业费金额进行审查。"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的关键事实。"
    conclusion = "事实要素不足，需补充物业费期间、物业服务是否达标、瑕疵程度、催收方式、解聘程序或公共收益金额后再裁判"
    return _format_property_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
