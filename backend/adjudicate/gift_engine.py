"""Gift-contract adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import _format_output, _mentions, _parse_date, _years_between
from adjudicate.gift_configs import get_gift_config


@dataclass
class GiftFacts:
    raw_text: str
    contract_type: str = "gift"
    contract_type_name: str = "赠与合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    gift_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    deadline_question: bool = False
    nature_dispute: bool = False
    gratuitous_intent: bool = False
    donee_accepts: bool = False
    no_acceptance: bool = False
    consideration: bool = False
    betrothal_or_romance: bool = False
    equity_incentive: bool = False
    contract_invalid: bool = False
    notarized_gift: bool = False
    public_welfare_gift: bool = False
    moral_obligation_gift: bool = False
    obligation_attached: bool = False
    registration_required: bool = False
    registration_done: bool = False
    right_transferred: bool = False
    not_transferred: bool = False
    arbitrary_revocation_claim: bool = False
    termination_word: bool = False
    waiver_revocation_agreement: bool = False
    statutory_revocation_claim: bool = False
    serious_infringement: bool = False
    support_duty_unfulfilled: bool = False
    agreed_obligation_unfulfilled: bool = False
    within_one_year: bool = False
    over_one_year: bool = False
    heir_or_agent_revocation: bool = False
    donee_illegal_act: bool = False
    donor_dead: bool = False
    donor_incapacitated: bool = False
    within_six_months: bool = False
    over_six_months: bool = False
    delivery_claim: bool = False
    property_not_delivered: bool = False
    property_destroyed: bool = False
    donor_intent_gross: bool = False
    force_majeure: bool = False
    donee_obligation_performed: bool = False
    gift_property_defect: bool = False
    deliberate_non_disclosure: bool = False
    guaranteed_no_defect: bool = False
    poverty_defense: bool = False
    economic_deteriorated: bool = False
    serious_life_impact: bool = False
    revocation_exercised: bool = False
    return_claim: bool = False
    property_unreturnable: bool = False
    donee_predeceased: bool = False
    donor_dead_inheritance_request: bool = False
    actual_loss: float = 0.0
    property_value: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "gift_contract": self.gift_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "deadline_question": self.deadline_question,
            "nature_dispute": self.nature_dispute,
            "gratuitous_intent": self.gratuitous_intent,
            "donee_accepts": self.donee_accepts,
            "no_acceptance": self.no_acceptance,
            "consideration": self.consideration,
            "betrothal_or_romance": self.betrothal_or_romance,
            "equity_incentive": self.equity_incentive,
            "contract_invalid": self.contract_invalid,
            "notarized_gift": self.notarized_gift,
            "public_welfare_gift": self.public_welfare_gift,
            "moral_obligation_gift": self.moral_obligation_gift,
            "obligation_attached": self.obligation_attached,
            "registration_required": self.registration_required,
            "registration_done": self.registration_done,
            "right_transferred": self.right_transferred,
            "not_transferred": self.not_transferred,
            "arbitrary_revocation_claim": self.arbitrary_revocation_claim,
            "termination_word": self.termination_word,
            "waiver_revocation_agreement": self.waiver_revocation_agreement,
            "statutory_revocation_claim": self.statutory_revocation_claim,
            "serious_infringement": self.serious_infringement,
            "support_duty_unfulfilled": self.support_duty_unfulfilled,
            "agreed_obligation_unfulfilled": self.agreed_obligation_unfulfilled,
            "within_one_year": self.within_one_year,
            "over_one_year": self.over_one_year,
            "heir_or_agent_revocation": self.heir_or_agent_revocation,
            "donee_illegal_act": self.donee_illegal_act,
            "donor_dead": self.donor_dead,
            "donor_incapacitated": self.donor_incapacitated,
            "within_six_months": self.within_six_months,
            "over_six_months": self.over_six_months,
            "delivery_claim": self.delivery_claim,
            "property_not_delivered": self.property_not_delivered,
            "property_destroyed": self.property_destroyed,
            "donor_intent_gross": self.donor_intent_gross,
            "force_majeure": self.force_majeure,
            "donee_obligation_performed": self.donee_obligation_performed,
            "gift_property_defect": self.gift_property_defect,
            "deliberate_non_disclosure": self.deliberate_non_disclosure,
            "guaranteed_no_defect": self.guaranteed_no_defect,
            "poverty_defense": self.poverty_defense,
            "economic_deteriorated": self.economic_deteriorated,
            "serious_life_impact": self.serious_life_impact,
            "revocation_exercised": self.revocation_exercised,
            "return_claim": self.return_claim,
            "property_unreturnable": self.property_unreturnable,
            "donee_predeceased": self.donee_predeceased,
            "donor_dead_inheritance_request": self.donor_dead_inheritance_request,
            "actual_loss": self.actual_loss,
            "property_value": self.property_value,
            "notes": self.notes,
        }


def _format_gift_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: GiftFacts,
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


def extract_gift_facts(case_text: str) -> GiftFacts:
    config = get_gift_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = GiftFacts(raw_text=raw_text)

    for field_name in (
        "gift_contract", "third_party_tort", "deadline_question", "nature_dispute",
        "gratuitous_intent", "donee_accepts", "no_acceptance", "consideration",
        "betrothal_or_romance", "equity_incentive", "contract_invalid", "notarized_gift",
        "public_welfare_gift", "moral_obligation_gift", "obligation_attached",
        "registration_required", "registration_done", "right_transferred",
        "not_transferred", "arbitrary_revocation_claim", "termination_word",
        "waiver_revocation_agreement", "statutory_revocation_claim", "serious_infringement",
        "support_duty_unfulfilled", "agreed_obligation_unfulfilled", "within_one_year",
        "over_one_year", "heir_or_agent_revocation", "donee_illegal_act", "donor_dead",
        "donor_incapacitated", "within_six_months", "over_six_months", "delivery_claim",
        "property_not_delivered", "property_destroyed", "donor_intent_gross",
        "force_majeure", "donee_obligation_performed", "gift_property_defect",
        "deliberate_non_disclosure", "guaranteed_no_defect", "poverty_defense",
        "economic_deteriorated", "serious_life_impact", "revocation_exercised",
        "return_claim", "property_unreturnable", "donee_predeceased",
        "donor_dead_inheritance_request",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.actual_loss = _extract_money_near(text, config.get_terms("actual_loss"))
    facts.property_value = _extract_money_near(text, config.get_terms("property_value"))

    if any(
        (
            facts.gratuitous_intent, facts.donee_accepts, facts.notarized_gift,
            facts.public_welfare_gift, facts.moral_obligation_gift, facts.obligation_attached,
            facts.arbitrary_revocation_claim, facts.statutory_revocation_claim,
            facts.delivery_claim, facts.gift_property_defect,
        )
    ):
        facts.gift_contract = True
    if facts.registration_done:
        facts.right_transferred = True
    if facts.not_transferred:
        facts.right_transferred = False
    return facts


def _procedure_findings(facts: GiftFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("赠与合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理。")
    if facts.asks_defendant:
        findings.append("适格被告按请求确定：请求交付或赔偿的，通常列赠与人或其继承人为被告；请求返还赠与财产的，通常列受赠人为被告。")
    return findings


def _only_procedure_question(facts: GiftFacts) -> bool:
    substantive = any(
        (
            facts.deadline_question, facts.nature_dispute, facts.no_acceptance,
            facts.arbitrary_revocation_claim, facts.termination_word, facts.statutory_revocation_claim,
            facts.heir_or_agent_revocation, facts.delivery_claim, facts.obligation_attached,
            facts.gift_property_defect, facts.poverty_defense, facts.donee_predeceased,
            facts.donor_dead_inheritance_request,
        )
    )
    return (facts.asks_jurisdiction or facts.asks_defendant) and not substantive


def _non_revocable_exception(facts: GiftFacts) -> bool:
    return facts.notarized_gift or facts.public_welfare_gift or facts.moral_obligation_gift or facts.waiver_revocation_agreement


def adjudicate_gift(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_gift_config()
    facts = extract_gift_facts(case_text)
    today = today or date.today()
    triggered: List[str] = []
    path: List[str] = ["入口程序校验"]
    procedure_findings = _procedure_findings(facts)

    if _only_procedure_question(facts):
        major = "赠与合同纠纷的程序事项应先确认管辖法院和适格被告。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出赠与成立、撤销、交付、返还、瑕疵或穷困抗辩等实体争议事实。"
        conclusion = "；".join(procedure_findings)
        return _format_gift_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    concrete_revocation_dispute = any(
        (
            facts.statutory_revocation_claim, facts.heir_or_agent_revocation,
            facts.serious_infringement, facts.support_duty_unfulfilled,
            facts.agreed_obligation_unfulfilled, facts.donee_illegal_act,
            facts.revocation_exercised, facts.return_claim,
        )
    )
    if facts.deadline_question and not concrete_revocation_dispute:
        triggered.append(config.patch_name("G15", "赠与合同纠纷的诉讼时效与除斥期间区分"))
        major = "赠与合同中，法定撤销权行使期间属于除斥期间：赠与人撤销权为知道或者应当知道撤销事由之日起一年内，继承人或者法定代理人撤销权为知道或者应当知道撤销事由之日起六个月内；交付、赔偿等其他请求权适用三年诉讼时效。"
        minor = "识别到用户要求判断赠与合同权利行使期限。"
        if facts.heir_or_agent_revocation:
            status = "已超过" if facts.over_six_months else "未超过"
            conclusion = f"继承人/法定代理人撤销权行使期限为六个月除斥期间，{status}；其他请求权适用三年诉讼时效。"
        else:
            status = "已超过" if facts.over_one_year else "未超过"
            conclusion = f"赠与人撤销权行使期限为一年除斥期间，{status}；其他请求权适用三年诉讼时效。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, [*path, "诉讼时效与除斥期间"], procedure_findings)

    if facts.third_party_tort and not facts.gift_contract:
        major = "赠与合同裁判引擎处理赠与人与受赠人之间因无偿给予财产产生的合同争议；单纯合同外第三人侵权应按侵权责任处理。"
        minor = "识别到争议核心是合同外第三人侵权，未识别到赠与合同履行争议。"
        conclusion = "本案涉及侵权责任，非赠与合同纠纷，不适用本赠与合同裁判引擎。"
        return _format_gift_output(major, minor, conclusion, [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "赠与合同的交付、赔偿等请求权适用三年一般诉讼时效；撤销权另适用除斥期间。"
        minor = f"识别到相关合同签订、请求交付或撤销日期为{facts.contract_date.isoformat()}，截至{today.isoformat()}已经超过三年。"
        conclusion = "诉讼时效已过，驳回请求；如系撤销权，还应另行审查一年的除斥期间或六个月的除斥期间是否已过。"
        return _format_gift_output(major, minor, conclusion, [], facts, [*path, "诉讼时效"], procedure_findings)

    path.append("前置实体判断")
    if facts.nature_dispute:
        triggered.append(config.patch_name("G1", "赠与合同的性质认定"))
        major = "《民法典》第657条规定，赠与合同是赠与人将自己的财产无偿给予受赠人，受赠人表示接受赠与的合同。合同性质应按实质内容认定。"
        if facts.gratuitous_intent and facts.donee_accepts and not facts.consideration:
            minor = "识别到赠与人具有无偿给予财产的意思表示，受赠人也表示接受，且未识别金钱对价。"
            conclusion = "合同性质认定为赠与合同，适用赠与合同裁判规则。"
        elif facts.consideration:
            minor = "识别到财产转让存在价款、对价或付款购买安排。"
            conclusion = "合同性质更接近买卖合同或其他有偿合同，不适用赠与合同裁判规则。"
        elif facts.betrothal_or_romance:
            minor = "识别到争议发生在彩礼或恋爱期间大额给付场景。"
            conclusion = "该给付可能构成附条件赠与，应结合结婚目的、金额、双方关系和给付背景继续审查。"
        elif facts.equity_incentive:
            minor = "识别到合同虽使用赠与表述，但发生在股权激励协议背景下。"
            conclusion = "股权激励中的赠与表述需综合合同整体约定、合同目的及订立背景审查，不能仅按赠与合同处理。"
        else:
            minor = "现有事实不足以确认是否存在无偿给予和接受赠与的合意。"
            conclusion = "合同性质暂不能稳定认定，需要补充是否无偿给予、受赠人是否接受以及是否存在对价。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, [*path, "合同性质认定"], procedure_findings)

    if facts.contract_invalid:
        major = "赠与合同违反法律、行政法规强制性规定或者损害公共利益的，应认定无效；无效后已取得财产应返还，有过错的赔偿损失。"
        minor = "识别到赠与合同无效或违法无效事实。"
        conclusion = "按无效合同处理，已经取得的赠与财产应返还；不能返还的折价补偿，有过错的一方赔偿对方损失。"
        return _format_gift_output(major, minor, conclusion, [], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.no_acceptance:
        major = "《民法典》第657条规定，赠与合同须赠与人无偿给予财产、受赠人表示接受，双方意思表示一致时成立。"
        minor = "识别到受赠人未表示接受或者拒绝接受赠与。"
        conclusion = "赠与合同不成立，赠与人无需交付赠与财产。"
        return _format_gift_output(major, minor, conclusion, [], facts, [*path, "合同成立审查"], procedure_findings)

    if facts.donee_predeceased:
        triggered.append(config.patch_name("G12", "受赠人先于赠与人死亡的处理"))
        major = "赠与合同具有人身属性。受赠人在赠与人交付财产前死亡的，赠与合同终止。"
        minor = "识别到受赠人在赠与财产交付前先于赠与人死亡。"
        conclusion = "受赠人先于赠与人死亡，赠与合同终止，赠与人无需再履行赠与义务。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, [*path, "合同成立与终止"], procedure_findings)

    if facts.registration_required:
        triggered.append(config.patch_name("G10", "赠与财产需办理登记手续的处理"))
        major = "《民法典》第659条规定，赠与的财产依法需要办理登记或者其他手续的，应当办理有关手续。"
        minor = "识别到赠与财产为不动产、车辆、股权等依法需要办理登记或过户手续的财产。"
        if facts.registration_done:
            conclusion = "赠与财产已办理登记手续，财产权利已转移，赠与人不得再主张任意撤销。"
        else:
            conclusion = "赠与财产未办理登记手续，财产权利尚未转移；除公证、公益或道德义务等不可撤销赠与外，赠与人可主张任意撤销。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, [*path, "赠与类型识别"], procedure_findings)

    if facts.poverty_defense:
        triggered.append(config.patch_name("G8", "穷困抗辩权"))
        major = "《民法典》第666条规定，赠与人的经济状况显著恶化，严重影响其生产经营或者家庭生活的，可以不再履行赠与义务。"
        minor = "识别到赠与人主张因经济状况恶化不再履行赠与义务。"
        if facts.economic_deteriorated and facts.serious_life_impact:
            conclusion = "穷困抗辩权成立，赠与人可以不再履行赠与义务。"
        else:
            conclusion = "穷困抗辩权不成立，赠与人仍应继续履行赠与义务。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, [*path, "穷困抗辩"], procedure_findings)

    if facts.donor_dead_inheritance_request:
        triggered.append(config.patch_name("G14", "赠与人的继承人是否应继续履行赠与义务"))
        major = "一般赠与具有人身属性，赠与人死亡后继承人通常无需继续履行赠与义务；但公证赠与或者公益、道德义务性质赠与除外。"
        minor = "识别到赠与人死亡后，受赠人请求继承人继续履行赠与义务。"
        if facts.notarized_gift or facts.public_welfare_gift or facts.moral_obligation_gift:
            conclusion = "继承人应在遗产范围内继续履行赠与义务。"
        else:
            conclusion = "继承人不应继续履行一般赠与义务。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, [*path, "继承人履行义务"], procedure_findings)

    path.append("任意撤销权")
    if facts.termination_word:
        triggered.append(config.patch_name("G11", "赠与合同的任意解除 vs 撤销"))
        major = "赠与合同适用撤销权制度。赠与人的反悔在法律上应定性为撤销，而非合同解除。"
        minor = "识别到赠与人使用‘解除赠与合同’或‘解除合同’的表述。"
        conclusion = "赠与人主张的‘解除’应定性为‘撤销’，适用赠与合同任意撤销权或法定撤销权的相关规定。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.arbitrary_revocation_claim and not concrete_revocation_dispute:
        triggered.append(config.patch_name("G2", "任意撤销权的行使条件"))
        major = "《民法典》第658条规定，赠与人在赠与财产的权利转移之前可以撤销赠与；经过公证的赠与合同，或者依法不得撤销的公益、道德义务性质赠与合同，不适用任意撤销权。"
        minor = "识别到赠与人主张在赠与财产权利转移前后反悔、收回或撤销赠与。"
        if facts.waiver_revocation_agreement:
            triggered.append(config.patch_name("G13", "赠与人与受赠人约定不得撤销的效力"))
            conclusion = "赠与人已放弃任意撤销权，不得行使任意撤销权；但不影响法定撤销权的行使。"
        elif facts.right_transferred:
            conclusion = "赠与财产权利已经转移，赠与人任意撤销权不成立，不可以撤销赠与。"
        elif facts.notarized_gift or facts.public_welfare_gift or facts.moral_obligation_gift:
            conclusion = "本案属于公证赠与、公益赠与或道德义务性质赠与，赠与人任意撤销权不成立，受赠人可以请求交付。"
        else:
            conclusion = "赠与财产权利尚未转移，且不属于不可撤销的例外情形，赠与人任意撤销权成立，可以撤销赠与。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("法定撤销权")
    if facts.obligation_attached and not facts.statutory_revocation_claim:
        triggered.append(config.patch_name("G6", "附义务赠与的履行与责任"))
        major = "《民法典》第661条规定，赠与可以附义务；赠与附义务的，受赠人应当按照约定履行义务。《民法典》第662条规定，附义务赠与中财产有瑕疵的，赠与人在附义务限度内承担与出卖人相同的责任。"
        minor = "识别到赠与附有约定义务。"
        if facts.agreed_obligation_unfulfilled:
            conclusion = "受赠人未履行约定义务，赠与人可依法主张法定撤销权。"
        elif facts.gift_property_defect:
            conclusion = "受赠人已履行或未识别不履行约定义务；赠与财产有瑕疵的，赠与人在附义务限度内承担与出卖人相同的瑕疵担保责任。"
        else:
            conclusion = "受赠人应按约定履行义务；未识别违约或瑕疵事实，暂不支持撤销或瑕疵赔偿。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, [*path, "附义务赠与"], procedure_findings)

    if facts.heir_or_agent_revocation:
        triggered.append(config.patch_name("G4", "继承人/法定代理人的撤销权"))
        major = "《民法典》第664条规定，因受赠人的违法行为致使赠与人死亡或者丧失民事行为能力的，赠与人的继承人或者法定代理人可以撤销赠与；撤销权自知道或者应当知道撤销事由之日起六个月内行使。"
        minor = "识别到赠与人的继承人或法定代理人主张撤销赠与。"
        if not (facts.donee_illegal_act and (facts.donor_dead or facts.donor_incapacitated)):
            conclusion = "继承人/法定代理人撤销权不成立，未能证明受赠人违法行为导致赠与人死亡或丧失民事行为能力。"
        elif facts.over_six_months:
            conclusion = "继承人/法定代理人撤销权不成立，六个月除斥期间已超过。"
        else:
            triggered.append(config.patch_name("G9", "赠与合同撤销后的财产返还"))
            conclusion = "继承人/法定代理人撤销权成立，可以撤销赠与并请求返还财产；财产无法返还的，可请求折价赔偿。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.statutory_revocation_claim or facts.serious_infringement or facts.support_duty_unfulfilled or facts.agreed_obligation_unfulfilled:
        triggered.append(config.patch_name("G3", "法定撤销权的行使条件"))
        major = "《民法典》第663条规定，受赠人严重侵害赠与人或其近亲属合法权益、对赠与人有扶养义务而不履行，或者不履行赠与合同约定义务的，赠与人可以撤销赠与；撤销权自知道或者应当知道撤销事由之日起一年内行使。"
        minor = "识别到赠与人主张基于受赠人行为行使法定撤销权。"
        has_reason = facts.serious_infringement or facts.support_duty_unfulfilled or facts.agreed_obligation_unfulfilled
        if not has_reason:
            conclusion = "法定撤销权不成立，未识别到严重侵害、不履行扶养义务或不履行约定义务等法定撤销事由。"
        elif facts.over_one_year:
            conclusion = "法定撤销权不成立，一年除斥期间已超过。"
        else:
            triggered.append(config.patch_name("G9", "赠与合同撤销后的财产返还"))
            conclusion = "法定撤销权成立，赠与人可以撤销赠与并请求返还财产；财产无法返还的，可请求折价赔偿。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("公证/公益赠与履行")
    if (facts.delivery_claim or facts.property_not_delivered) and (facts.notarized_gift or facts.public_welfare_gift or facts.moral_obligation_gift):
        triggered.append(config.patch_name("G5", "公证/公益赠与的强制履行与赔偿责任"))
        major = "《民法典》第660条规定，经过公证的赠与合同或者依法不得撤销的公益、道德义务性质赠与合同，赠与人不交付赠与财产的，受赠人可以请求交付；因赠与人故意或者重大过失致使应交付财产毁损、灭失的，赠与人应承担赔偿责任。"
        minor = "识别到公证赠与、公益赠与或道德义务性质赠与中，受赠人请求交付赠与财产。"
        if facts.property_destroyed:
            if facts.donor_intent_gross:
                conclusion = f"赠与人应承担赔偿责任，已识别损失为 {_money(facts.actual_loss or facts.property_value)}。"
            else:
                conclusion = "赠与财产毁损、灭失，但未识别赠与人故意或重大过失，赠与人不承担赔偿责任。"
        else:
            conclusion = "赠与人应交付赠与财产，不能以任意撤销权拒绝交付。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("附义务赠与")
    if facts.obligation_attached:
        triggered.append(config.patch_name("G6", "附义务赠与的履行与责任"))
        major = "《民法典》第661条规定，赠与可以附义务；赠与附义务的，受赠人应当按照约定履行义务。《民法典》第662条规定，附义务赠与中财产有瑕疵的，赠与人在附义务限度内承担与出卖人相同的责任。"
        minor = "识别到赠与附有约定义务。"
        if facts.agreed_obligation_unfulfilled:
            conclusion = "受赠人未履行约定义务，赠与人可依法主张法定撤销权。"
        elif facts.gift_property_defect:
            conclusion = "受赠人已履行或未识别不履行约定义务；赠与财产有瑕疵的，赠与人在附义务限度内承担与出卖人相同的瑕疵担保责任。"
        else:
            conclusion = "受赠人应按约定履行义务；未识别违约或瑕疵事实，暂不支持撤销或瑕疵赔偿。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("瑕疵担保责任")
    if facts.gift_property_defect:
        triggered.append(config.patch_name("G7", "赠与人瑕疵担保责任的免除与例外"))
        major = "《民法典》第662条规定，赠与的财产有瑕疵的，赠与人原则上不承担责任；附义务赠与在附义务限度内承担与出卖人相同的责任；赠与人故意不告知瑕疵或者保证无瑕疵造成损失的，应承担赔偿责任。"
        minor = "识别到受赠人主张赠与财产存在瑕疵并要求赠与人承担责任。"
        if facts.deliberate_non_disclosure or facts.guaranteed_no_defect:
            conclusion = f"赠与人承担赔偿责任，已识别损失为 {_money(facts.actual_loss)}。"
        else:
            conclusion = "赠与人不承担瑕疵担保责任，也不承担赔偿责任。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.revocation_exercised or facts.return_claim:
        triggered.append(config.patch_name("G9", "赠与合同撤销后的财产返还"))
        major = "《民法典》第665条规定，撤销权人撤销赠与的，可以向受赠人请求返还赠与的财产。"
        minor = "识别到撤销权人已撤销赠与并请求返还赠与财产。"
        if facts.property_unreturnable:
            conclusion = f"撤销权成立，赠与财产无法返还的，受赠人应折价赔偿；已识别金额为 {_money(facts.property_value or facts.actual_loss)}。"
        else:
            conclusion = "撤销权成立，受赠人应返还赠与财产。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, [*path, "撤销后返还"], procedure_findings)

    if facts.gift_contract:
        major = "《民法典》第657条至第666条规定，赠与合同裁判应围绕无偿给予和接受、财产权利是否转移、赠与类型、撤销权、交付请求、瑕疵担保和穷困抗辩进行审查。"
        minor = "已识别赠与合同关系，但未稳定识别撤销、交付、登记、附义务、瑕疵、继承人履行或穷困抗辩等具体争议事实。"
        conclusion = "事实要素不足，需要补充赠与是否已交付或登记、是否公证或公益、是否主张撤销、受赠人是否有法定撤销事由、是否存在瑕疵或穷困抗辩后再裁判。"
        return _format_gift_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    major = "赠与合同纠纷应围绕赠与人无偿给予财产、受赠人接受、撤销权是否成立、是否应交付或返还、瑕疵责任和穷困抗辩进行审查。"
    minor = "自然语言事实未能稳定识别出赠与合同关系和关键争议节点。"
    conclusion = "事实要素不足，需要补充是否存在无偿给予和接受、是否已交付或过户、是否公证或公益、是否主张撤销、是否存在法定撤销事由或瑕疵后再裁判。"
    return _format_gift_output(major, minor, conclusion, triggered, facts, path, procedure_findings)
