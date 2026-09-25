"""Finance-lease adjudication engine."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from adjudicate.engine_v2 import _extract_number_near, _format_output, _mentions, _parse_date, _years_between
from adjudicate.finance_lease_configs import get_finance_lease_config


@dataclass
class FinanceLeaseFacts:
    raw_text: str
    contract_type: str = "finance_lease"
    contract_type_name: str = "融资租赁合同"
    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    finance_lease_contract: bool = False
    contract_date: Optional[date] = None
    third_party_tort: bool = False
    nature_dispute: bool = False
    real_asset: bool = False
    fake_asset: bool = False
    rent_includes_cost_profit: bool = False
    not_finance_lease: bool = False
    sale_leaseback: bool = False
    admin_license_issue: bool = False
    contract_invalid: bool = False
    invalid_asset_ownership_agreed: bool = False
    seller_non_delivery: bool = False
    serious_nonconform_delivery: bool = False
    lessee_refuses_accept: bool = False
    timely_notify_lessor: bool = False
    unjustified_refusal: bool = False
    quality_defect: bool = False
    lessee_selected_asset: bool = False
    lessor_skill_reliance: bool = False
    lessor_intervened_choice: bool = False
    claim_against_seller: bool = False
    lessor_failed_assist: bool = False
    lessor_wrongfully_repossess: bool = False
    third_party_damage: bool = False
    during_lessee_possession: bool = False
    maintenance_issue: bool = False
    unpaid_rent: bool = False
    lessor_urged: bool = False
    reasonable_period_unpaid: bool = False
    rent_arrears_periods: float = 0.0
    rent_arrears_amount: float = 0.0
    total_rent_amount: float = 0.0
    request_all_rent: bool = False
    request_terminate_repossess: bool = False
    request_both_remedies: bool = False
    termination_loss_claim: bool = False
    all_unpaid_fees: float = 0.0
    repossessed_asset_value: float = 0.0
    asset_loss: bool = False
    lessee_fault_loss: bool = False
    no_fault_loss: bool = False
    cannot_repair_replace: bool = False
    unauthorized_disposition: bool = False
    ownership_registered: bool = False
    ownership_unregistered: bool = False
    good_faith_third_party: bool = False
    end_ownership_agreed: bool = False
    end_ownership_unclear: bool = False
    symbolic_price: bool = False
    paid_most_rent: bool = False
    unable_pay_remaining: bool = False
    asset_value: float = 0.0
    unpaid_fees: float = 0.0
    sale_contract_invalid: bool = False
    asset_chosen_by_lessee: bool = False
    asset_chosen_by_lessor: bool = False
    repurchase_guarantee: bool = False
    repurchase_condition_met: bool = False
    repurchase_resolution: bool = False
    contract_assignment: bool = False
    assignee_requests_termination: bool = False
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "finance_lease_contract": self.finance_lease_contract,
            "contract_date": self.contract_date.isoformat() if self.contract_date else None,
            "third_party_tort": self.third_party_tort,
            "nature_dispute": self.nature_dispute,
            "real_asset": self.real_asset,
            "fake_asset": self.fake_asset,
            "rent_includes_cost_profit": self.rent_includes_cost_profit,
            "not_finance_lease": self.not_finance_lease,
            "sale_leaseback": self.sale_leaseback,
            "admin_license_issue": self.admin_license_issue,
            "contract_invalid": self.contract_invalid,
            "invalid_asset_ownership_agreed": self.invalid_asset_ownership_agreed,
            "seller_non_delivery": self.seller_non_delivery,
            "serious_nonconform_delivery": self.serious_nonconform_delivery,
            "lessee_refuses_accept": self.lessee_refuses_accept,
            "timely_notify_lessor": self.timely_notify_lessor,
            "unjustified_refusal": self.unjustified_refusal,
            "quality_defect": self.quality_defect,
            "lessee_selected_asset": self.lessee_selected_asset,
            "lessor_skill_reliance": self.lessor_skill_reliance,
            "lessor_intervened_choice": self.lessor_intervened_choice,
            "claim_against_seller": self.claim_against_seller,
            "lessor_failed_assist": self.lessor_failed_assist,
            "lessor_wrongfully_repossess": self.lessor_wrongfully_repossess,
            "third_party_damage": self.third_party_damage,
            "during_lessee_possession": self.during_lessee_possession,
            "maintenance_issue": self.maintenance_issue,
            "unpaid_rent": self.unpaid_rent,
            "lessor_urged": self.lessor_urged,
            "reasonable_period_unpaid": self.reasonable_period_unpaid,
            "rent_arrears_periods": self.rent_arrears_periods,
            "rent_arrears_amount": self.rent_arrears_amount,
            "total_rent_amount": self.total_rent_amount,
            "request_all_rent": self.request_all_rent,
            "request_terminate_repossess": self.request_terminate_repossess,
            "request_both_remedies": self.request_both_remedies,
            "termination_loss_claim": self.termination_loss_claim,
            "all_unpaid_fees": self.all_unpaid_fees,
            "repossessed_asset_value": self.repossessed_asset_value,
            "asset_loss": self.asset_loss,
            "lessee_fault_loss": self.lessee_fault_loss,
            "no_fault_loss": self.no_fault_loss,
            "cannot_repair_replace": self.cannot_repair_replace,
            "unauthorized_disposition": self.unauthorized_disposition,
            "ownership_registered": self.ownership_registered,
            "ownership_unregistered": self.ownership_unregistered,
            "good_faith_third_party": self.good_faith_third_party,
            "end_ownership_agreed": self.end_ownership_agreed,
            "end_ownership_unclear": self.end_ownership_unclear,
            "symbolic_price": self.symbolic_price,
            "paid_most_rent": self.paid_most_rent,
            "unable_pay_remaining": self.unable_pay_remaining,
            "asset_value": self.asset_value,
            "unpaid_fees": self.unpaid_fees,
            "sale_contract_invalid": self.sale_contract_invalid,
            "asset_chosen_by_lessee": self.asset_chosen_by_lessee,
            "asset_chosen_by_lessor": self.asset_chosen_by_lessor,
            "repurchase_guarantee": self.repurchase_guarantee,
            "repurchase_condition_met": self.repurchase_condition_met,
            "repurchase_resolution": self.repurchase_resolution,
            "contract_assignment": self.contract_assignment,
            "assignee_requests_termination": self.assignee_requests_termination,
            "notes": self.notes,
        }


def _format_finance_lease_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: FinanceLeaseFacts,
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


def extract_finance_lease_facts(case_text: str) -> FinanceLeaseFacts:
    config = get_finance_lease_config()
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = FinanceLeaseFacts(raw_text=raw_text)

    for field_name in (
        "finance_lease_contract", "third_party_tort", "nature_dispute", "real_asset",
        "fake_asset", "rent_includes_cost_profit", "not_finance_lease", "sale_leaseback",
        "admin_license_issue", "contract_invalid", "invalid_asset_ownership_agreed",
        "seller_non_delivery", "serious_nonconform_delivery", "lessee_refuses_accept",
        "timely_notify_lessor", "unjustified_refusal", "quality_defect", "lessee_selected_asset",
        "lessor_skill_reliance", "lessor_intervened_choice", "claim_against_seller",
        "lessor_failed_assist", "lessor_wrongfully_repossess", "third_party_damage",
        "during_lessee_possession", "maintenance_issue", "unpaid_rent", "lessor_urged",
        "reasonable_period_unpaid", "request_all_rent", "request_terminate_repossess",
        "request_both_remedies", "termination_loss_claim", "asset_loss", "lessee_fault_loss",
        "no_fault_loss", "cannot_repair_replace", "unauthorized_disposition",
        "ownership_registered", "ownership_unregistered", "good_faith_third_party",
        "end_ownership_agreed", "end_ownership_unclear", "symbolic_price", "paid_most_rent",
        "unable_pay_remaining", "sale_contract_invalid", "asset_chosen_by_lessee",
        "asset_chosen_by_lessor", "repurchase_guarantee", "repurchase_condition_met",
        "repurchase_resolution", "contract_assignment", "assignee_requests_termination",
    ):
        setattr(facts, field_name, _mentions(text, config.get_terms(field_name)))

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        ("起诉" in text or "法院" in text) and any(word in text for word in ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.contract_date = _parse_date(text, config.get_terms("contract_date"))
    facts.rent_arrears_periods = _extract_number_near(text, config.get_terms("rent_arrears_periods"), ("期",))
    facts.rent_arrears_amount = _extract_money_near(text, config.get_terms("rent_arrears_amount"))
    facts.total_rent_amount = _extract_money_near(text, config.get_terms("total_rent_amount"))
    facts.all_unpaid_fees = _extract_money_near(text, config.get_terms("all_unpaid_fees"))
    facts.repossessed_asset_value = _extract_money_near(text, config.get_terms("repossessed_asset_value"))
    facts.asset_value = _extract_money_near(text, config.get_terms("asset_value"))
    facts.unpaid_fees = _extract_money_near(text, config.get_terms("unpaid_fees"))

    if any((facts.sale_leaseback, facts.unpaid_rent, facts.asset_loss, facts.unauthorized_disposition, facts.end_ownership_agreed)):
        facts.finance_lease_contract = True
    return facts


def _procedure_findings(facts: FinanceLeaseFacts) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append("融资租赁合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理")
    if facts.asks_defendant:
        findings.append("适格被告应结合争议确定：租金支付争议通常列承租人，交付或质量索赔争议可能涉及出卖人，妨碍占有使用争议可列出租人")
    return findings


def _only_procedure_question(facts: FinanceLeaseFacts) -> bool:
    substantive = _has_substantive_dispute(facts)
    return (facts.asks_jurisdiction or facts.asks_defendant) and not substantive


def _has_substantive_dispute(facts: FinanceLeaseFacts) -> bool:
    return any(
        (
            facts.nature_dispute, facts.sale_leaseback, facts.fake_asset, facts.contract_invalid,
            facts.admin_license_issue, facts.seller_non_delivery, facts.serious_nonconform_delivery,
            facts.lessee_refuses_accept, facts.quality_defect, facts.claim_against_seller,
            facts.lessor_wrongfully_repossess, facts.third_party_damage, facts.maintenance_issue,
            facts.unpaid_rent, facts.request_all_rent, facts.request_terminate_repossess,
            facts.asset_loss, facts.unauthorized_disposition, facts.end_ownership_agreed,
            facts.end_ownership_unclear, facts.symbolic_price, facts.paid_most_rent,
            facts.sale_contract_invalid, facts.repurchase_guarantee, facts.contract_assignment,
        )
    )


def _rent_default_reaches_termination_threshold(facts: FinanceLeaseFacts) -> bool:
    if facts.rent_arrears_periods >= 2:
        return True
    if facts.rent_arrears_amount > 0 and facts.total_rent_amount > 0:
        return facts.rent_arrears_amount >= facts.total_rent_amount * 0.15
    return False


def adjudicate_finance_lease(case_text: str, today: Optional[date] = None) -> Dict[str, Any]:
    config = get_finance_lease_config()
    facts = extract_finance_lease_facts(case_text)
    today = today or date.today()
    procedure_findings = _procedure_findings(facts)
    path = ["入口程序校验"]

    if _only_procedure_question(facts):
        major = "融资租赁合同纠纷适用合同纠纷管辖和适格当事人规则；合同有有效管辖约定的，按约定处理。"
        minor = "本案事实主要询问起诉法院或应列被告，未提出需要实体裁判的租金、租赁物或合同效力争议。"
        conclusion = "按程序事项处理：" + "；".join(procedure_findings)
        return _format_finance_lease_output(major, minor, conclusion, ["管辖程序"] if procedure_findings else [], facts, path, procedure_findings)

    if facts.contract_date and _years_between(facts.contract_date, today) > 3:
        major = "合同纠纷请求权通常适用三年诉讼时效。"
        minor = f"本案可识别的合同或履行日期为 {facts.contract_date.isoformat()}，距今已超过三年，且未识别到中止、中断或延长事由。"
        conclusion = "诉讼时效已过，超过时效部分不予支持。"
        return _format_finance_lease_output(major, minor, conclusion, ["诉讼时效"], facts, [*path, "诉讼时效"], procedure_findings)

    if facts.third_party_tort and not facts.finance_lease_contract:
        major = "第三人侵害财产或人身权益的，按侵权责任规则处理；合同裁判引擎只处理合同相对方之间的履行争议。"
        minor = "本案主要事实指向合同外第三人侵权，未能识别融资租赁合同履行争议。"
        conclusion = "本案涉及侵权责任，非融资租赁合同纠纷，不适用本融资租赁合同裁判引擎。"
        return _format_finance_lease_output(major, minor, conclusion, [], facts, [*path, "侵权第三方分流"], procedure_findings)

    path.append("前置实体判断")

    if facts.sale_leaseback:
        triggered = [config.patch_name("F8", "售后回租认定")]
        major = "售后回租中，承租人与出卖人虽为同一人，但只要存在真实租赁物且租金构成符合融资租赁交易安排，不当然否定融资租赁法律关系。"
        if facts.fake_asset or facts.not_finance_lease:
            minor = "本案虽称售后回租，但事实显示租赁物不存在或交易只有融资没有融物属性。"
            conclusion = "本案不构成融资租赁法律关系，应按实际法律关系处理。"
        else:
            minor = "本案为承租人将自有物出卖给出租人后再租回，未识别到虚构租赁物或仅有资金拆借事实。"
            conclusion = "售后回租构成融资租赁法律关系，后续租金、租赁物和违约责任按融资租赁规则处理。"
        return _format_finance_lease_output(major, minor, conclusion, triggered, facts, [*path, "融资租赁性质认定"], procedure_findings)

    if facts.nature_dispute or facts.not_finance_lease or facts.real_asset or facts.rent_includes_cost_profit:
        triggered = [config.patch_name("F1", "融资租赁法律关系认定")]
        major = "融资租赁合同应结合标的物真实性、价值、租金构成以及当事人权利义务综合认定；名称不决定合同性质。"
        if facts.fake_asset or facts.not_finance_lease:
            minor = "本案存在租赁物虚构、只有融资没有融物属性，或双方实质争议更接近资金借贷。"
            conclusion = "本案不构成融资租赁法律关系，应按实际法律关系处理。"
        else:
            minor = "本案能够识别真实租赁物，且租金安排体现购买成本、合理利润及租赁物使用收益。"
            conclusion = "本案构成融资租赁法律关系，应按融资租赁合同处理。"
        return _format_finance_lease_output(major, minor, conclusion, triggered, facts, [*path, "融资租赁性质认定"], procedure_findings)

    if facts.fake_asset:
        major = "以虚构租赁物方式订立的融资租赁合同无效。"
        minor = "本案事实显示租赁物不存在或为虚构租赁物。"
        conclusion = "融资租赁合同无效，因合同取得的财产应依法返还；损失按过错承担。"
        return _format_finance_lease_output(major, minor, conclusion, [config.patch_name("F2", "虚构租赁物合同无效")], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.contract_invalid and not facts.admin_license_issue:
        major = "融资租赁合同无效时，租赁物归属有约定的按照约定；没有约定或约定不明确的，租赁物应返还出租人。"
        minor = "本案已识别融资租赁合同无效争议。"
        if facts.invalid_asset_ownership_agreed:
            conclusion = "融资租赁合同无效，租赁物归属按双方关于无效后归属的约定处理。"
        else:
            conclusion = "融资租赁合同无效，租赁物应返还出租人；费用返还和损失赔偿另按过错结算。"
        return _format_finance_lease_output(major, minor, conclusion, [config.patch_name("F15", "合同无效时租赁物归属")], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.admin_license_issue:
        major = "租赁物经营使用需要行政许可的，承租人未取得行政许可一般不当然影响融资租赁合同效力，法律另有强制性规定的除外。"
        minor = "本案争议集中在承租人或使用环节未取得行政许可，而非租赁物虚构或合同目的违法。"
        conclusion = "行政许可问题不当然导致融资租赁合同无效；承租人仍应按合同承担租金和使用管理责任。"
        return _format_finance_lease_output(major, minor, conclusion, ["行政许可不影响合同效力"], facts, [*path, "合同效力审查"], procedure_findings)

    if facts.seller_non_delivery or facts.serious_nonconform_delivery or facts.lessee_refuses_accept:
        major = "出卖人迟延交付、拒绝交付或交付标的物严重不符合约定，导致承租人拒绝受领的，应审查拒收理由及是否及时通知出租人。"
        if facts.unjustified_refusal:
            minor = "本案承租人无正当理由拒绝受领，或未按交易安排及时通知出租人。"
            conclusion = "承租人拒绝受领不成立，应赔偿因此给出租人造成的损失，并继续按合同承担相应租金义务。"
        elif facts.timely_notify_lessor or facts.serious_nonconform_delivery or facts.seller_non_delivery:
            minor = "本案存在出卖人未交付、迟延交付或租赁物严重不符合约定，且承租人拒收具有可识别的正当理由。"
            conclusion = "承租人拒绝受领成立，可请求出租人协助向出卖人索赔；是否解除或变更合同按履行障碍程度另行审查。"
        else:
            minor = "本案仅能识别拒绝受领争议，但拒收理由和通知事实仍不完整。"
            conclusion = "需补充交付情况、租赁物是否严重不符合约定以及承租人是否及时通知出租人后，再判断拒收后果。"
        return _format_finance_lease_output(major, minor, conclusion, ["交付与受领审查"], facts, [*path, "交付与受领审查"], procedure_findings)

    if facts.quality_defect or facts.claim_against_seller or facts.lessor_failed_assist:
        triggered = [config.patch_name("F3", "出租人瑕疵担保责任例外")]
        major = "融资租赁中，租赁物由承租人选择时，出租人一般不承担租赁物质量瑕疵担保责任；但承租人依赖出租人技能确定租赁物，或出租人干预、决定选择的，出租人应承担相应责任。"
        if facts.lessor_intervened_choice or facts.lessor_skill_reliance:
            minor = "本案租赁物有质量瑕疵，且出租人对选择租赁物或出卖人具有决定性影响，或承租人依赖出租人的专业技能作出选择。"
            conclusion = "出租人应承担租赁物质量瑕疵担保责任；承租人可据此主张相应赔偿或抗辩。"
        elif facts.lessor_failed_assist:
            minor = "本案承租人需向出卖人索赔，但出租人未提供必要协助或怠于行使索赔权，影响了承租人的索赔。"
            conclusion = "出租人对索赔受阻造成的损失承担相应责任；承租人原则上仍应履行租金义务。"
        else:
            minor = "本案租赁物由承租人自行选择，质量问题主要指向出卖人履约瑕疵。"
            conclusion = "出租人不承担租赁物质量瑕疵担保责任；承租人可直接向出卖人索赔，但不得仅以质量瑕疵当然拒付租金。"
        return _format_finance_lease_output(major, minor, conclusion, triggered, facts, [*path, "租赁物瑕疵责任"], procedure_findings)

    if facts.lessor_wrongfully_repossess:
        major = "出租人应保障承租人对租赁物的占有和使用；无正当理由收回、妨碍或干扰使用造成损失的，应承担赔偿责任。"
        minor = "本案出租人无正当理由收回租赁物或干扰承租人占有使用。"
        conclusion = "出租人构成妨碍承租人占有使用租赁物，应赔偿因此造成的损失。"
        return _format_finance_lease_output(major, minor, conclusion, [config.patch_name("F12", "出租人妨碍占有使用责任")], facts, [*path, "占有使用保障"], procedure_findings)

    if facts.third_party_damage and facts.during_lessee_possession:
        major = "承租人占有租赁物期间，租赁物造成第三人人身或财产损害的，出租人不承担责任。"
        minor = "本案损害发生在承租人占有使用租赁物期间。"
        conclusion = "租赁物致第三人损害发生在承租人占有期间，出租人不承担责任；责任由实际控制、使用或有过错的一方承担。"
        return _format_finance_lease_output(major, minor, conclusion, [config.patch_name("F14", "租赁物致人损害责任")], facts, [*path, "租赁物致人损害"], procedure_findings)

    if facts.maintenance_issue and not facts.asset_loss:
        major = "融资租赁期间，承租人对租赁物负有妥善保管、使用和维修义务，另有约定的按约定。"
        minor = "本案争议指向承租人未妥善保管、使用不当或未履行维修义务。"
        conclusion = "承租人应对保管、使用或维修不当造成的损失承担责任，并按合同继续结算租金。"
        return _format_finance_lease_output(major, minor, conclusion, ["承租人保管维修义务"], facts, [*path, "保管维修义务"], procedure_findings)

    if facts.sale_contract_invalid:
        triggered = [config.patch_name("F10", "买卖合同无效导致解除的处理")]
        major = "买卖合同解除、无效或被撤销导致融资租赁合同无法继续履行的，应审查租赁物或出卖人由谁选择。"
        if facts.asset_chosen_by_lessee:
            minor = "本案租赁物或出卖人由承租人选择，买卖合同障碍导致融资租赁合同解除。"
            conclusion = "出租人有权向承租人主张赔偿损失。"
        elif facts.asset_chosen_by_lessor:
            minor = "本案租赁物或出卖人由出租人选择，买卖合同障碍导致融资租赁合同解除。"
            conclusion = "出租人无权就该障碍向承租人主张赔偿损失。"
        else:
            minor = "本案能够识别买卖合同无效、解除或撤销，但尚不能判断租赁物或出卖人由谁选择。"
            conclusion = "需先查明选择租赁物和出卖人的主体，再确定出租人能否向承租人主张赔偿。"
        return _format_finance_lease_output(major, minor, conclusion, triggered, facts, [*path, "买卖合同障碍"], procedure_findings)

    if facts.repurchase_guarantee:
        triggered = [config.patch_name("F11", "回购担保认定与处理")]
        major = "融资租赁交易中的回购担保，应审查回购合同、回购条件是否成就以及公司决议等程序要求。"
        if facts.repurchase_condition_met and facts.repurchase_resolution:
            minor = "本案存在回购担保，回购条件已经成就，并能识别回购人履行回购所需的内部决议。"
            conclusion = "回购担保有效，回购人应履行回购义务。"
        elif facts.repurchase_condition_met:
            minor = "本案存在回购担保且回购条件已经成就，但未能识别回购人公司决议或授权情况。"
            conclusion = "回购条件已成就，但仍需审查回购人内部决议或授权；程序合规的，回购人应履行回购义务。"
        else:
            minor = "本案存在回购担保，但未能识别回购条件已经成就。"
            conclusion = "回购担保能否履行需补充回购条件是否成就；条件未成就的，暂不支持要求回购人履行。"
        return _format_finance_lease_output(major, minor, conclusion, triggered, facts, [*path, "回购担保"], procedure_findings)

    if facts.contract_assignment:
        major = "出租人转让融资租赁合同项下权利，不影响融资租赁合同继续履行；受让方不得仅以权利转让为由请求解除或变更合同。"
        minor = "本案存在出租人转让融资租赁合同权利，或受让方以转让为由请求解除、变更合同。"
        conclusion = "融资租赁合同权利转让后合同继续有效；受让方不得仅以转让为由解除或变更合同。"
        return _format_finance_lease_output(major, minor, conclusion, [config.patch_name("F13", "融资租赁合同转让影响")], facts, [*path, "合同权利转让"], procedure_findings)

    path.append("租金与租赁物核心争议树")

    if facts.paid_most_rent and (facts.asset_value > 0 or facts.unpaid_fees > 0 or facts.unable_pay_remaining):
        triggered = [config.patch_name("F7", "租赁物收回后的价值清算")]
        major = "租赁物约定归承租人且承租人已支付大部分租金，但因无力支付剩余租金被出租人收回的，出租人收回价值超过欠付租金及其他费用的，承租人可以请求返还差额。"
        difference = facts.asset_value - facts.unpaid_fees
        minor = f"本案承租人已支付大部分租金，租赁物价值为 {_money(facts.asset_value)}，欠付租金及其他费用为 {_money(facts.unpaid_fees)}。"
        if difference > 0:
            conclusion = f"出租人应返还租赁物价值超过欠付费用的差额 {_money(difference)}。"
        else:
            conclusion = "租赁物价值未超过欠付租金及其他费用，出租人不承担返还差额义务。"
        return _format_finance_lease_output(major, minor, conclusion, triggered, facts, [*path, "租赁物价值清算"], procedure_findings)

    if facts.unpaid_rent or facts.request_all_rent or facts.request_terminate_repossess or facts.request_both_remedies:
        triggered = [config.patch_name("F4", "承租人违约时出租人救济方式选择")]
        major = "承租人欠付租金，经催告后在合理期限内仍不支付的，出租人可以请求支付全部租金，也可以解除合同并收回租赁物，但两种主要救济不能同时获得。"
        if not (facts.lessor_urged or facts.reasonable_period_unpaid):
            minor = "本案识别到承租人欠付租金，但尚未识别出租人已经催告并给予合理履行期限。"
            conclusion = "出租人应先催告承租人在合理期限内支付租金；催告后仍不支付的，再选择请求全部租金或解除合同收回租赁物。"
        elif facts.request_both_remedies:
            minor = "本案出租人经催告后主张承租人欠付租金，但同时请求支付全部租金和解除合同收回租赁物。"
            conclusion = "出租人不能同时获得支付全部租金和解除合同收回租赁物两项主要救济，应择一主张。"
        elif facts.request_terminate_repossess:
            minor = "本案承租人经催告后仍欠付租金，出租人选择解除合同并收回租赁物。"
            if _rent_default_reaches_termination_threshold(facts) or facts.reasonable_period_unpaid:
                if facts.termination_loss_claim:
                    loss = max(facts.all_unpaid_fees - facts.repossessed_asset_value, 0)
                    conclusion = f"出租人可以解除合同并收回租赁物；解除后的损失为全部未付租金及其他费用 {_money(facts.all_unpaid_fees)} 减去收回租赁物价值 {_money(facts.repossessed_asset_value)}，差额 {_money(loss)}。"
                    triggered.append(config.patch_name("F9", "解除收回后的损失赔偿计算"))
                else:
                    conclusion = "出租人可以解除合同并收回租赁物；是否另行赔偿损失，应按全部未付租金及其他费用减去收回租赁物价值后计算。"
            else:
                conclusion = "现有事实不足以认定欠租达到解除程度，需补充欠租期数、欠租金额或催告后仍不付款事实。"
        else:
            minor = "本案承租人经催告后仍欠付租金，出租人选择请求支付全部租金或全部剩余租金。"
            conclusion = "出租人可以请求承租人支付全部租金；选择该救济后，不得再同时请求解除合同收回租赁物。"
        return _format_finance_lease_output(major, minor, conclusion, triggered, facts, [*path, "租金违约救济"], procedure_findings)

    if facts.asset_loss:
        triggered = [config.patch_name("F5", "租赁物毁损灭失后租金义务")]
        major = "租赁物在承租人占有期间毁损、灭失的，承租人通常仍应支付租金；不可归责于双方且不能修复或替代的，可以解除合同并按折旧等因素补偿。"
        if facts.lessee_fault_loss:
            minor = "本案租赁物毁损灭失发生在承租人占有期间，且可归责于承租人保管不善或使用不当。"
            conclusion = "承租人应继续支付租金，并对租赁物毁损灭失承担赔偿责任。"
        elif facts.no_fault_loss and facts.cannot_repair_replace:
            minor = "本案租赁物毁损灭失不可归责于双方，且不能修复或确定替代物。"
            conclusion = "当事人可以解除融资租赁合同；承租人应按租赁物折旧和实际使用情况给予合理补偿。"
        else:
            minor = "本案存在租赁物毁损灭失，但归责原因、修复可能性或替代物情况尚不清楚。"
            conclusion = "需补充毁损灭失原因及能否修复、替代；可归责于承租人的，承租人继续支付租金并赔偿。"
        return _format_finance_lease_output(major, minor, conclusion, triggered, facts, [*path, "租赁物风险负担"], procedure_findings)

    if facts.unauthorized_disposition:
        triggered = [config.patch_name("F6", "所有权登记与善意取得")]
        major = "出租人对租赁物享有所有权；未经登记的所有权不得对抗善意第三人，已登记的可以对抗。"
        if facts.ownership_registered:
            minor = "本案承租人擅自处分租赁物，但出租人所有权已经登记。"
            conclusion = "出租人可以对抗第三人，要求返还租赁物，并可向承租人主张违约责任。"
        elif facts.ownership_unregistered and facts.good_faith_third_party:
            minor = "本案承租人擅自处分租赁物，出租人所有权未登记，第三人主张善意取得。"
            conclusion = "出租人不得以未登记的所有权对抗善意第三人；出租人可向承租人主张违约赔偿。"
        else:
            minor = "本案存在擅自处分租赁物，但所有权登记和第三人善意情况仍不完整。"
            conclusion = "需查明租赁物所有权是否登记及第三人是否善意取得，再判断出租人能否追回租赁物。"
        return _format_finance_lease_output(major, minor, conclusion, triggered, facts, [*path, "所有权登记与处分"], procedure_findings)

    if facts.symbolic_price or facts.end_ownership_agreed or facts.end_ownership_unclear:
        major = "融资租赁期满后，租赁物归属有约定的按照约定；约定支付象征性价款后归承租人的，租金履行完毕且支付象征性价款后归承租人；没有约定或约定不明的，归出租人所有。"
        if facts.symbolic_price or facts.end_ownership_agreed:
            minor = "本案约定租赁期满后租赁物归承租人所有，或约定承租人支付象征性价款后取得所有权。"
            conclusion = "承租人按约付清租金并支付象征性价款后，租赁物所有权归承租人。"
        else:
            minor = "本案未约定租赁期满后的所有权归属，或约定不明确。"
            conclusion = "租赁期满后租赁物归出租人所有。"
        return _format_finance_lease_output(major, minor, conclusion, ["期满所有权归属"], facts, [*path, "期满所有权归属"], procedure_findings)

    if facts.finance_lease_contract:
        major = "融资租赁合同中，出租人按承租人选择购买租赁物并交付使用，承租人按约支付租金并妥善保管使用租赁物。"
        minor = "本案能够识别融资租赁合同关系，但未识别足以触发无效、租金违约、瑕疵担保、风险负担或所有权归属的具体事实。"
        conclusion = "融资租赁合同继续有效，各方应按合同履行；如主张违约责任，需进一步补充欠租、租赁物瑕疵、毁损灭失或解除收回等事实。"
    else:
        major = "融资租赁裁判需先识别真实租赁物、融资租赁交易结构和具体争议事实。"
        minor = "现有自然语言事实不足以确认融资租赁合同关系和裁判节点。"
        conclusion = "请补充合同结构、租赁物是否真实、租金支付情况、租赁物交付和权属安排后再裁判。"
    return _format_finance_lease_output(major, minor, conclusion, [], facts, path, procedure_findings)
