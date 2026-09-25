"""Second-version housing lease adjudication engine.

This engine is independent from the contract review flow and the legacy
structured deposit endpoint. It accepts natural-language facts, extracts
decision facts conservatively, then adjudicates in this order:

1. procedure review;
2. pre-deposit entity review;
3. deposit settlement.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from adjudicate.lease_configs import MOUNT_POST, MOUNT_PRE, MOUNT_REPLACE, LeaseTypeConfig, get_lease_config

NEGATION_WORDS = ("无", "没有", "未", "不存在", "未涉及", "不涉及", "并非", "不是")


@dataclass
class ExtractedFacts:
    raw_text: str
    contract_type: str = "house"
    contract_type_name: str = "房屋租赁"
    tenant_dead: bool = False
    cohabitant_or_cooperator: bool = False
    successor_willing_continue: bool = False
    successor_requests_termination: bool = False
    changed_circumstances: bool = False
    unforeseeable_change: bool = False
    non_commercial_risk: bool = False
    unfair_to_continue: bool = False
    illegal_building: bool = False
    sublease_chain_dispute: bool = False
    landlord_dead: bool = False
    heir_refuses_performance: bool = False
    fixed_term_expired: bool = False
    tenant_continues_use_after_expiry: bool = False
    landlord_collects_rent_or_no_objection: bool = False
    no_new_lease_contract: bool = False
    indefinite_lease: bool = False

    asks_jurisdiction: bool = False
    asks_defendant: bool = False
    house_location_known: bool = False
    signer_not_landlord: bool = False
    signer_description: Optional[str] = None

    termination_requested: bool = False
    force_majeure: bool = False
    fundamental_breach: bool = False
    unauthorized_sublease: bool = False
    rent_arrears_periods: float = 0.0
    rent_arrears_months: float = 0.0
    agreed_termination: bool = False
    landlord_knowledge_date: Optional[date] = None

    house_sold: bool = False
    lease_before_sale: bool = False
    sale_before_lease: bool = False
    sale_without_notice: bool = False

    pre_delivery_defect: bool = False
    third_party_defect: bool = False
    expropriation_or_demolition: bool = False
    serious_safety_risk: bool = False

    has_third_party: bool = False
    contract_end_date: Optional[date] = None
    contract_valid: Optional[bool] = None
    is_early_termination: bool = False
    has_early_termination_clause: bool = False
    has_damage: Optional[bool] = None
    damage_reason: Optional[str] = None
    evidence_can_prove_cause: Optional[bool] = None
    traffic_accident: bool = False
    traffic_accident_tenant_responsible: bool = False
    traffic_accident_other_responsible: bool = False
    traffic_accident_unknown_liability: bool = False
    financing_lease: bool = False
    vehicle_no_driving_qualification: bool = False
    lessor_checked_qualification: bool = False
    lessor_failed_qualification_check: bool = False
    actual_user_third_party: bool = False
    tenant_denies_actual_use_liability: bool = False
    vehicle_under_repair: bool = False
    stoppage_loss_claimed: bool = False
    vehicle_over_repair: bool = False
    replacement_vehicle_provided: bool = False
    repair_days: float = 0.0
    daily_rent: float = 0.0
    equipment_fault_abnormal: bool = False
    tenant_timely_notice: bool = False
    tenant_failed_notice_or_measures: bool = False
    loss_expanded: bool = False
    equipment_scrapped: bool = False
    equipment_total_loss: bool = False
    loss_during_lease: bool = False
    loss_tenant_fault: bool = False
    loss_no_fault: bool = False
    unpaid_rent: float = 0.0
    equipment_actual_user_damage: bool = False
    overbroad_damage_liability_clause: bool = False
    notified_defect_at_check_in: bool = False
    landlord_knew_no_objection: bool = False
    agreed_deduction: float = 0.0
    actual_loss: float = 0.0
    deposit_amount: float = 0.0
    notes: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type,
            "contract_type_name": self.contract_type_name,
            "tenant_dead": self.tenant_dead,
            "cohabitant_or_cooperator": self.cohabitant_or_cooperator,
            "successor_willing_continue": self.successor_willing_continue,
            "successor_requests_termination": self.successor_requests_termination,
            "changed_circumstances": self.changed_circumstances,
            "unforeseeable_change": self.unforeseeable_change,
            "non_commercial_risk": self.non_commercial_risk,
            "unfair_to_continue": self.unfair_to_continue,
            "illegal_building": self.illegal_building,
            "sublease_chain_dispute": self.sublease_chain_dispute,
            "landlord_dead": self.landlord_dead,
            "heir_refuses_performance": self.heir_refuses_performance,
            "fixed_term_expired": self.fixed_term_expired,
            "tenant_continues_use_after_expiry": self.tenant_continues_use_after_expiry,
            "landlord_collects_rent_or_no_objection": self.landlord_collects_rent_or_no_objection,
            "no_new_lease_contract": self.no_new_lease_contract,
            "indefinite_lease": self.indefinite_lease,
            "asks_jurisdiction": self.asks_jurisdiction,
            "asks_defendant": self.asks_defendant,
            "house_location_known": self.house_location_known,
            "signer_not_landlord": self.signer_not_landlord,
            "signer_description": self.signer_description,
            "termination_requested": self.termination_requested,
            "force_majeure": self.force_majeure,
            "fundamental_breach": self.fundamental_breach,
            "unauthorized_sublease": self.unauthorized_sublease,
            "rent_arrears_periods": self.rent_arrears_periods,
            "rent_arrears_months": self.rent_arrears_months,
            "agreed_termination": self.agreed_termination,
            "landlord_knowledge_date": self.landlord_knowledge_date.isoformat() if self.landlord_knowledge_date else None,
            "house_sold": self.house_sold,
            "lease_before_sale": self.lease_before_sale,
            "sale_before_lease": self.sale_before_lease,
            "sale_without_notice": self.sale_without_notice,
            "pre_delivery_defect": self.pre_delivery_defect,
            "third_party_defect": self.third_party_defect,
            "expropriation_or_demolition": self.expropriation_or_demolition,
            "serious_safety_risk": self.serious_safety_risk,
            "has_third_party": self.has_third_party,
            "contract_end_date": self.contract_end_date.isoformat() if self.contract_end_date else None,
            "contract_valid": self.contract_valid,
            "is_early_termination": self.is_early_termination,
            "has_early_termination_clause": self.has_early_termination_clause,
            "has_damage": self.has_damage,
            "damage_reason": self.damage_reason,
            "evidence_can_prove_cause": self.evidence_can_prove_cause,
            "traffic_accident": self.traffic_accident,
            "traffic_accident_tenant_responsible": self.traffic_accident_tenant_responsible,
            "traffic_accident_other_responsible": self.traffic_accident_other_responsible,
            "traffic_accident_unknown_liability": self.traffic_accident_unknown_liability,
            "financing_lease": self.financing_lease,
            "vehicle_no_driving_qualification": self.vehicle_no_driving_qualification,
            "lessor_checked_qualification": self.lessor_checked_qualification,
            "lessor_failed_qualification_check": self.lessor_failed_qualification_check,
            "actual_user_third_party": self.actual_user_third_party,
            "tenant_denies_actual_use_liability": self.tenant_denies_actual_use_liability,
            "vehicle_under_repair": self.vehicle_under_repair,
            "stoppage_loss_claimed": self.stoppage_loss_claimed,
            "vehicle_over_repair": self.vehicle_over_repair,
            "replacement_vehicle_provided": self.replacement_vehicle_provided,
            "repair_days": self.repair_days,
            "daily_rent": self.daily_rent,
            "equipment_fault_abnormal": self.equipment_fault_abnormal,
            "tenant_timely_notice": self.tenant_timely_notice,
            "tenant_failed_notice_or_measures": self.tenant_failed_notice_or_measures,
            "loss_expanded": self.loss_expanded,
            "equipment_scrapped": self.equipment_scrapped,
            "equipment_total_loss": self.equipment_total_loss,
            "loss_during_lease": self.loss_during_lease,
            "loss_tenant_fault": self.loss_tenant_fault,
            "loss_no_fault": self.loss_no_fault,
            "unpaid_rent": self.unpaid_rent,
            "equipment_actual_user_damage": self.equipment_actual_user_damage,
            "overbroad_damage_liability_clause": self.overbroad_damage_liability_clause,
            "notified_defect_at_check_in": self.notified_defect_at_check_in,
            "landlord_knew_no_objection": self.landlord_knew_no_objection,
            "agreed_deduction": self.agreed_deduction,
            "actual_loss": self.actual_loss,
            "deposit_amount": self.deposit_amount,
            "notes": self.notes,
        }


def _has_negated_word(text: str, word: str, window: int = 5) -> bool:
    for match in re.finditer(re.escape(word), text):
        prefix = text[max(0, match.start() - window):match.start()]
        if any(negation in prefix for negation in NEGATION_WORDS):
            return True
    return False


def _mentions(text: str, words: tuple[str, ...]) -> bool:
    return any(word in text and not _has_negated_word(text, word) for word in words)


def _has_any(text: str, words: tuple[str, ...]) -> bool:
    return any(word in text for word in words)


def _parse_date(text: str, context_words: tuple[str, ...] = ()) -> Optional[date]:
    patterns = [
        r"(?P<y>20\d{2})[-/.年](?P<m>\d{1,2})[-/.月](?P<d>\d{1,2})日?",
        r"(?P<y>19\d{2})[-/.年](?P<m>\d{1,2})[-/.月](?P<d>\d{1,2})日?",
    ]
    candidates: List[tuple[int, date]] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            try:
                parsed = date(int(match.group("y")), int(match.group("m")), int(match.group("d")))
            except ValueError:
                continue
            start = max(0, match.start() - 14)
            end = min(len(text), match.end() + 14)
            context = text[start:end]
            score = 0 if context_words and any(word in context for word in context_words) else 1
            candidates.append((score, parsed))
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: item[0])[0][1]


def _extract_number_near(text: str, labels: tuple[str, ...], unit_words: tuple[str, ...]) -> float:
    for label in labels:
        for match in re.finditer(re.escape(label), text):
            after = text[match.end():min(len(text), match.end() + 12)]
            unit_group = "|".join(re.escape(unit) for unit in unit_words)
            number_match = re.search(rf"(\d+(?:\.\d+)?)\s*(?:{unit_group})", after)
            if number_match:
                return float(number_match.group(1))
            before = text[max(0, match.start() - 12):match.start()]
            number_match = re.search(rf"(\d+(?:\.\d+)?)\s*(?:{unit_group})", before)
            if number_match:
                return float(number_match.group(1))
    return 0.0


def _extract_money_near(text: str, labels: tuple[str, ...]) -> float:
    amounts: List[float] = []
    money_pattern = r"(\d+(?:\.\d+)?)\s*(?:元|块|人民币)?"
    for label in labels:
        for match in re.finditer(re.escape(label), text):
            after = text[match.end():min(len(text), match.end() + 18)]
            after_match = re.search(money_pattern, after)
            if after_match:
                value = float(after_match.group(1))
                if value > 0:
                    amounts.append(value)
                    continue

            before = text[max(0, match.start() - 8):match.start()]
            for amount_match in re.finditer(money_pattern, before):
                value = float(amount_match.group(1))
                if value > 0:
                    amounts.append(value)
    return max(amounts) if amounts else 0.0


def _years_between(start: date, end: date) -> float:
    return (end - start).days / 365.25


def _sentences(text: str) -> List[str]:
    parts = re.split(r"[。！？；;，,\n]", text)
    return [part.strip() for part in parts if part.strip()]


def _role_event_before(case_text: str, role_words: tuple[str, ...], event_words: tuple[str, ...], excluded_roles: tuple[str, ...]) -> bool:
    for sentence in _sentences(case_text):
        compact = re.sub(r"\s+", "", sentence)
        for event_word in event_words:
            for match in re.finditer(re.escape(event_word), compact):
                prefix = compact[max(0, match.start() - 14):match.start()]
                if any(role in prefix for role in role_words) and not any(role in prefix for role in excluded_roles):
                    return True
    return False


def _is_overbroad_tenant_damage_liability_clause(case_text: str, config: LeaseTypeConfig) -> bool:
    """Classify a clause that shifts all damage risk to the tenant.

    This does not depend on one fixed phrase. It looks for a sentence that is
    described as a contract term and semantically assigns no-fault, whole-scope
    damage liability to the tenant.
    """
    clause_markers = config.get_terms("overbroad_clause_clause")
    tenant_markers = config.get_terms("overbroad_clause_tenant")
    damage_markers = config.get_terms("overbroad_clause_damage")
    liability_markers = config.get_terms("overbroad_clause_liability")
    whole_scope_markers = config.get_terms("overbroad_clause_scope")

    for sentence in _sentences(case_text):
        compact = re.sub(r"\s+", "", sentence)
        if any(negation in compact for negation in ("该条款无效", "不能一概", "并非全部")):
            continue
        score = 0
        score += 1 if any(marker in compact for marker in clause_markers) else 0
        score += 1 if any(marker in compact for marker in tenant_markers) else 0
        score += 1 if any(marker in compact for marker in damage_markers) else 0
        score += 1 if any(marker in compact for marker in liability_markers) else 0
        score += 1 if any(marker in compact for marker in whole_scope_markers) else 0
        if score >= 5:
            return True
    return False


def extract_facts(case_text: str, contract_type: Optional[str] = None) -> ExtractedFacts:
    config = get_lease_config(contract_type)
    raw_text = case_text or ""
    text = re.sub(r"\s+", "", raw_text)
    facts = ExtractedFacts(raw_text=raw_text, contract_type=config.key, contract_type_name=config.display_name)

    facts.contract_end_date = _parse_date(text, ("终止", "到期", "结束", "退租", "搬离", "解除"))
    facts.landlord_knowledge_date = _parse_date(text, ("知道", "应当知道", "知情", "解除事由"))

    facts.tenant_dead = _mentions(
        text,
        config.get_terms("tenant_dead"),
    ) or _role_event_before(raw_text, config.get_terms("tenant"), ("死亡", "去世", "身故"), config.get_terms("lessor"))
    if not facts.tenant_dead and _has_any(text, config.get_terms("tenant")) and _has_any(text, ("死亡", "去世", "身故")) and not _has_any(text, config.get_terms("lessor")):
        facts.tenant_dead = True
    no_cohabitant_or_cooperator = any(
        phrase in text
        for phrase in config.get_terms("no_cohabitant_or_cooperator")
    )
    facts.cohabitant_or_cooperator = not no_cohabitant_or_cooperator and _mentions(
        text,
        config.get_terms("cohabitant_or_cooperator"),
    )
    facts.successor_willing_continue = _mentions(
        text,
        config.get_terms("successor_continue"),
    )
    facts.successor_requests_termination = _mentions(
        text,
        config.get_terms("successor_terminate"),
    )

    facts.unforeseeable_change = _mentions(
        text,
        config.get_terms("changed_unforeseeable"),
    )
    facts.non_commercial_risk = _mentions(text, config.get_terms("changed_non_commercial"))
    facts.unfair_to_continue = _mentions(
        text,
        config.get_terms("changed_unfair"),
    )
    facts.changed_circumstances = facts.unforeseeable_change and facts.non_commercial_risk and facts.unfair_to_continue

    facts.illegal_building = _mentions(
        text,
        config.get_terms("illegal_asset"),
    )

    facts.sublease_chain_dispute = (
        _mentions(text, config.get_terms("sublease_chain"))
        or (_mentions(text, ("转租",)) and _mentions(text, ("次承租", "二房东", "C", "第三人造成租赁物损失")))
    )

    facts.landlord_dead = _mentions(
        text,
        config.get_terms("lessor_dead"),
    ) or _role_event_before(raw_text, config.get_terms("lessor"), ("死亡", "去世", "身故"), config.get_terms("tenant"))
    if not facts.landlord_dead and _has_any(text, config.get_terms("lessor")) and _has_any(text, ("死亡", "去世", "身故")) and not _has_any(text, config.get_terms("tenant")):
        facts.landlord_dead = True
    facts.heir_refuses_performance = _mentions(
        text,
        config.get_terms("lessor_heir_refuse"),
    )

    facts.fixed_term_expired = _mentions(text, config.get_terms("term_expired"))
    facts.tenant_continues_use_after_expiry = _mentions(
        text,
        config.get_terms("continue_use"),
    )
    facts.landlord_collects_rent_or_no_objection = _mentions(
        text,
        config.get_terms("collect_rent_or_no_objection"),
    )
    facts.no_new_lease_contract = _mentions(
        text,
        config.get_terms("no_new_contract"),
    )
    facts.indefinite_lease = (
        facts.fixed_term_expired
        and facts.tenant_continues_use_after_expiry
        and facts.landlord_collects_rent_or_no_objection
        and facts.no_new_lease_contract
    )

    facts.asks_jurisdiction = _mentions(text, config.get_terms("jurisdiction_question")) or (
        _has_any(text, ("起诉", "法院")) and _has_any(text, ("哪里", "去哪", "哪个", "管辖", "地点"))
    )
    facts.asks_defendant = _mentions(text, config.get_terms("defendant_question"))
    facts.house_location_known = _mentions(text, ("房屋所在地", "房子所在地", "租赁房屋位于", "房屋位于", "车辆所在地", "设备所在地", "租赁物所在地"))

    signer_patterns = config.get_terms("non_lessor_signer")
    facts.signer_not_landlord = _mentions(text, signer_patterns)
    if facts.signer_not_landlord:
        facts.signer_description = next((word for word in signer_patterns if word in text), "非出租人本人签署")

    facts.termination_requested = _mentions(text, config.get_terms("termination_request"))
    facts.force_majeure = _mentions(text, config.get_terms("force_majeure"))
    facts.unauthorized_sublease = _mentions(text, config.get_terms("sublease_unauthorized"))
    facts.rent_arrears_periods = _extract_number_near(text, ("欠租", "拖欠租金"), ("期",))
    facts.rent_arrears_months = _extract_number_near(text, ("欠租", "拖欠租金", "累计"), ("个月", "月"))
    if _mentions(text, ("欠租超过两期", "欠租超过2期", "长期欠租")):
        facts.rent_arrears_periods = max(facts.rent_arrears_periods, 3)
    facts.fundamental_breach = (
        facts.unauthorized_sublease
        or facts.rent_arrears_periods > 2
        or facts.rent_arrears_months >= 6
        or _mentions(text, config.get_terms("fundamental_breach"))
    )
    facts.agreed_termination = facts.termination_requested and _mentions(text, config.get_terms("agreed_termination"))

    facts.house_sold = _mentions(text, config.get_terms("asset_transfer"))
    facts.lease_before_sale = _mentions(text, config.get_terms("lease_before_transfer"))
    facts.sale_before_lease = _mentions(text, config.get_terms("transfer_before_lease"))
    facts.sale_without_notice = facts.house_sold and _mentions(text, config.get_terms("transfer_without_notice"))

    facts.pre_delivery_defect = _mentions(text, config.get_terms("pre_delivery_defect"))
    facts.third_party_defect = _mentions(text, config.get_terms("third_party_defect"))
    facts.expropriation_or_demolition = _mentions(text, config.get_terms("expropriation"))
    facts.serious_safety_risk = _mentions(text, config.get_terms("serious_safety_risk"))

    facts.has_third_party = any(
        word in text and not _has_negated_word(text, word)
        for word in config.get_terms("third_party")
    )

    if _mentions(text, config.get_terms("contract_invalid")):
        facts.contract_valid = False
    elif _mentions(text, config.get_terms("contract_valid")):
        facts.contract_valid = True

    facts.is_early_termination = _mentions(text, config.get_terms("early_return"))
    no_early_clause = _mentions(text, config.get_terms("no_early_clause"))
    facts.has_early_termination_clause = facts.is_early_termination and not no_early_clause and _mentions(
        text,
        config.get_terms("early_clause"),
    )

    if _mentions(text, config.get_terms("no_damage")):
        facts.has_damage = False
    elif _mentions(text, config.get_terms("damage")):
        facts.has_damage = True

    facts.traffic_accident = _mentions(text, config.get_terms("traffic_accident"))
    facts.traffic_accident_tenant_responsible = _mentions(
        text,
        config.get_terms("traffic_accident_tenant_responsible"),
    )
    facts.traffic_accident_other_responsible = _mentions(
        text,
        config.get_terms("traffic_accident_other_responsible"),
    )
    facts.traffic_accident_unknown_liability = _mentions(
        text,
        config.get_terms("traffic_accident_unknown_liability"),
    )
    if facts.traffic_accident and facts.has_damage is None:
        facts.has_damage = True

    facts.financing_lease = _mentions(text, config.get_terms("financing_lease"))
    facts.vehicle_no_driving_qualification = _mentions(
        text,
        config.get_terms("vehicle_no_driving_qualification"),
    )
    facts.lessor_checked_qualification = _mentions(
        text,
        config.get_terms("lessor_checked_qualification"),
    )
    facts.lessor_failed_qualification_check = _mentions(
        text,
        config.get_terms("lessor_failed_qualification_check"),
    )
    facts.actual_user_third_party = _mentions(
        text,
        config.get_terms("actual_user_vehicle") + config.get_terms("actual_user_equipment"),
    )
    facts.tenant_denies_actual_use_liability = _mentions(
        text,
        config.get_terms("tenant_denies_actual_use_liability"),
    )
    facts.vehicle_under_repair = _mentions(text, config.get_terms("vehicle_under_repair"))
    facts.stoppage_loss_claimed = _mentions(text, config.get_terms("stoppage_loss_claim"))
    facts.vehicle_over_repair = _mentions(text, config.get_terms("vehicle_over_repair"))
    facts.replacement_vehicle_provided = _mentions(text, config.get_terms("replacement_vehicle_provided"))
    if facts.vehicle_under_repair and facts.has_damage is None:
        facts.has_damage = True

    facts.equipment_fault_abnormal = _mentions(text, config.get_terms("equipment_fault_abnormal"))
    facts.tenant_timely_notice = _mentions(text, config.get_terms("tenant_timely_notice"))
    facts.tenant_failed_notice_or_measures = _mentions(
        text,
        config.get_terms("tenant_failed_notice_or_measures"),
    )
    facts.loss_expanded = _mentions(text, config.get_terms("loss_expanded"))
    facts.equipment_scrapped = _mentions(text, config.get_terms("equipment_scrapped"))
    facts.equipment_total_loss = _mentions(text, config.get_terms("equipment_total_loss"))
    facts.loss_during_lease = _mentions(text, config.get_terms("loss_during_lease"))
    facts.loss_tenant_fault = _mentions(text, config.get_terms("loss_tenant_fault"))
    facts.loss_no_fault = _mentions(text, config.get_terms("loss_no_fault"))
    facts.equipment_actual_user_damage = _mentions(text, config.get_terms("equipment_actual_user_damage"))
    if (facts.equipment_fault_abnormal or facts.equipment_total_loss) and facts.has_damage is None:
        facts.has_damage = True

    facts.overbroad_damage_liability_clause = _is_overbroad_tenant_damage_liability_clause(raw_text, config)

    if _mentions(text, config.get_terms("natural_wear")):
        facts.damage_reason = "natural_wear"
    if _mentions(text, config.get_terms("unproven")):
        facts.evidence_can_prove_cause = False
        facts.damage_reason = "unproven"
    elif facts.has_damage is True:
        facts.evidence_can_prove_cause = True
    if _mentions(text, config.get_terms("tenant_fault")):
        facts.damage_reason = "tenant_fault"
        facts.evidence_can_prove_cause = True

    facts.notified_defect_at_check_in = _mentions(text, config.get_terms("check_in_notice"))
    facts.landlord_knew_no_objection = _mentions(text, config.get_terms("lessor_no_objection"))

    facts.agreed_deduction = _extract_money_near(text, ("约定扣", "扣押金", "扣款", "扣除", "不退押金", "违约金"))
    facts.actual_loss = _extract_money_near(text, ("实际损失", "维修费", "维修报价", "修理费", "损失"))
    facts.deposit_amount = _extract_money_near(text, ("押金",))
    facts.repair_days = _extract_number_near(text, config.get_terms("repair_days"), ("天", "日"))
    facts.daily_rent = _extract_money_near(text, config.get_terms("daily_rent"))
    facts.unpaid_rent = _extract_money_near(text, config.get_terms("unpaid_rent"))

    if facts.agreed_deduction == 0 and "押金不退" in text and facts.deposit_amount > 0:
        facts.agreed_deduction = facts.deposit_amount
    if facts.actual_loss == 0 and facts.damage_reason == "tenant_fault":
        facts.notes.append("未识别到明确实际损失金额，维修费暂按0元处理。")

    return facts


def _format_output(
    major: str,
    minor: str,
    conclusion: str,
    triggered_items: List[str],
    facts: ExtractedFacts,
    path: List[str],
    procedure_findings: Optional[List[str]] = None,
    footer_label: str = "触发模块/补丁清单",
) -> Dict[str, Any]:
    list_text = "、".join(triggered_items) if triggered_items else "无"
    procedure_text = ""
    if procedure_findings:
        procedure_text = "程序审查：" + "；".join(procedure_findings) + "\n\n"
    result_text = (
        f"{procedure_text}"
        f"大前提（法律依据）：{major}\n\n"
        f"小前提（认定事实）：{minor}\n\n"
        f"结论（判决结果）：{conclusion}\n\n"
        f"{footer_label}：{list_text}"
    )
    return {
        "success": True,
        "result": result_text,
        "major_premise": major,
        "minor_premise": minor,
        "conclusion": conclusion,
        "triggered_patches": triggered_items,
        "path": path,
        "facts": facts.to_public_dict(),
        "procedure_findings": procedure_findings or [],
    }


def _format_edge_patch_output(
    patch_name: str,
    major: str,
    minor: str,
    conclusion: str,
    facts: ExtractedFacts,
    path_prefix: Optional[List[str]] = None,
    procedure_findings: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return _format_output(
        major=major,
        minor=minor,
        conclusion=conclusion,
        triggered_items=[patch_name],
        facts=facts,
        path=[*(path_prefix or []), patch_name],
        procedure_findings=procedure_findings,
        footer_label="触发补丁",
    )


def _run_configured_patch(
    patch_id: str,
    facts: ExtractedFacts,
    config: LeaseTypeConfig,
    path_prefix: Optional[List[str]] = None,
    procedure_findings: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    if patch_id == "tenant_death" and facts.tenant_dead:
        major = "《民法典》第732条规定，承租人在房屋租赁期限内死亡的，与其生前共同居住的人或者共同经营人可以按照原租赁合同租赁该房屋。"
        if facts.successor_requests_termination:
            minor = "识别到承租人在租赁期限内死亡，且共同居住人、共同经营人或继承人要求解除合同。"
            conclusion = "承租人死亡，存在共同居住人或共同经营人要求解除合同，可以解除，押金按合同约定处理，违约方承担相应责任。"
        elif facts.cohabitant_or_cooperator and facts.successor_willing_continue:
            minor = "识别到承租人在租赁期限内死亡，存在共同居住人或共同经营人，且该人愿意继续承租。"
            conclusion = "承租人死亡，存在共同居住人或共同经营人，原租赁合同继续有效，押金不退，合同由该人接替履行。"
        elif facts.cohabitant_or_cooperator:
            minor = "识别到承租人在租赁期限内死亡，并存在共同居住人或共同经营人。"
            conclusion = "承租人死亡，存在共同居住人或共同经营人，可以按照原租赁合同继续承租；其愿意继续承租的，押金不退，合同由该人接替履行。"
        else:
            minor = "识别到承租人在租赁期限内死亡，未识别到共同居住人或共同经营人。"
            conclusion = "承租人死亡，无共同居住人或共同经营人，租赁合同终止，押金应退还承租人的继承人。"
        return _format_edge_patch_output("补丁一：承租人死亡", major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "changed_circumstances" and facts.changed_circumstances:
        major = "《民法典》第533条规定，合同成立后基础条件发生当事人在订立合同时无法预见、不属于商业风险的重大变化，继续履行明显不公平的，受不利影响的一方可以请求变更或者解除合同。"
        minor = "识别到政策突变、疫情封控等重大变化，同时具备无法预见、非商业风险、继续履行显失公平三个条件。"
        conclusion = "可主张情势变更，建议先与对方协商减免租金或延长租期；协商不成可起诉请求变更或解除合同。"
        return _format_edge_patch_output("补丁二：情势变更", major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "illegal_asset" and facts.illegal_building:
        major = "《民法典》第153条规定，违反法律、行政法规强制性规定的民事法律行为无效；第157条规定，民事法律行为无效后，因该行为取得的财产应当返还。"
        minor = f"识别到租赁{config.asset_label}存在违反强制性规定，依法不能出租或不能正常使用的情形。"
        conclusion = config.patch_conclusions.get(
            "illegal_asset",
            f"租赁{config.asset_label}为违法标的，合同无效，{config.deposit_label}应返还，使用费另计，损失可主张赔偿。",
        )
        patch_label = config.patch_labels.get("illegal_asset", "补丁三：违法租赁标的")
        return _format_edge_patch_output(patch_label, major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "sublease_chain" and facts.sublease_chain_dispute:
        major = "《民法典》第716条规定，承租人经出租人同意转租的，原租赁合同继续有效；第三人造成租赁物损失的，承租人应当向出租人赔偿。未经出租人同意转租的，出租人可以解除合同。"
        minor = "识别到出租人、承租人、次承租人之间存在转租链条，争议发生在转租后的履行或损坏环节。"
        conclusion = "转租链条断裂适用合同相对性原则：A向B主张，B向C追偿，互不穿透。B对A的责任不变；若B未经A同意擅自转租，A可解除与B的租赁合同。"
        return _format_edge_patch_output("补丁四：转租链条断裂", major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "lessor_death" and facts.landlord_dead:
        major = "出租人在租赁期内死亡的，其合法继承人或受让人应继续履行原租赁合同。"
        if facts.heir_refuses_performance:
            minor = f"识别到{config.lessor_label}在租赁期间死亡，且继承人拒绝继续履行原租赁合同。"
            conclusion = config.patch_conclusions.get(
                "lessor_death_heir_refuse",
                f"{config.lessor_label}死亡，合同由继承人继续履行，{config.deposit_label}处理不受影响；继承人拒绝履行的，{config.tenant_label}可起诉要求继续履行或主张违约赔偿。",
            )
        else:
            minor = f"识别到{config.lessor_label}在租赁期间死亡，未识别到原合同已经依法终止。"
            conclusion = config.patch_conclusions.get(
                "lessor_death",
                f"{config.lessor_label}死亡，合同由继承人继续履行，{config.deposit_label}处理不受影响。",
            )
        return _format_edge_patch_output("补丁五：出租人死亡", major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "indefinite_lease" and facts.indefinite_lease:
        return _run_indefinite_lease_patch(facts, config, path_prefix, procedure_findings)

    if patch_id == "V2" and facts.financing_lease:
        major = "《民法典》融资租赁合同章规定，融资租赁中出租人根据承租人选择取得租赁物并交付承租人使用，承租人支付租金；以租代购实质符合融资租赁安排的，应按融资租赁规则处理。"
        minor = "识别到合同名称或合同内容具有融资租赁、以租代购特征，车辆通常在租赁期内归出租人所有，承租人按期支付租金并在期满后取得车辆所有权。"
        conclusion = "以租代购合同，适用融资租赁规则：所有权归出租人，违约可收回车辆，已付租金不予退还。"
        return _format_edge_patch_output(config.patch_name("V2", "以租代购"), major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "V4" and facts.actual_user_third_party and facts.tenant_denies_actual_use_liability:
        major = "《民法典》第465条规定，依法成立的合同仅对当事人具有法律约束力，但是法律另有规定的除外。"
        minor = "识别到承租人与出租人签订车辆租赁合同，车辆由第三人实际驾驶或使用，承租人以车不是本人驾驶为由拒绝赔偿。"
        conclusion = "合同相对性原则适用：承租人向出租人承担全部责任，可另行向实际使用人追偿。"
        return _format_edge_patch_output(config.patch_name("V4", "合同相对性原则例外-车辆"), major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "V3" and facts.vehicle_no_driving_qualification:
        major = "《民法典》第1209条规定，机动车所有人、管理人对损害发生有过错的，承担相应赔偿责任。"
        minor = "识别到承租人无有效驾驶资格、驾驶证被吊销或不具备合法驾驶条件。"
        if facts.lessor_checked_qualification:
            conclusion = "出租人审查义务判断：已审查，过错不成立，出租人不承担机动车所有人过错责任。"
        elif facts.lessor_failed_qualification_check:
            conclusion = "出租人审查义务判断：未审查或明知无资格仍出租，过错成立，责任承担比例按出租人过错程度和损害原因确定。"
        else:
            conclusion = "出租人审查义务判断：需补充出租人是否审查驾驶资格；未审查或明知无资格仍出租的，过错成立并承担相应责任。"
        return _format_edge_patch_output(config.patch_name("V3", "出租人审查义务"), major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "E3" and facts.actual_user_third_party and facts.equipment_actual_user_damage:
        major = "《民法典》第1165条规定，行为人因过错侵害他人民事权益造成损害的，应当承担侵权责任。"
        minor = "识别到设备租赁合同由承租人与出租人签订，但设备实际使用人为第三人，且第三人使用设备时造成设备损毁或他人损害。"
        conclusion = "实际使用人侵权责任成立，出租人可向承租人主张合同责任，也可直接向实际使用人主张侵权责任。"
        return _format_edge_patch_output(config.patch_name("E3", "实际使用人直接担责"), major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "E1" and facts.equipment_fault_abnormal and (
        facts.tenant_timely_notice or (facts.tenant_failed_notice_or_measures and facts.loss_expanded)
    ):
        major = "《民法典》第591条规定，当事人一方违约后，对方应当采取适当措施防止损失扩大；没有采取适当措施致使损失扩大的，不得就扩大的损失请求赔偿。"
        if facts.tenant_timely_notice:
            minor = "识别到设备出现故障或异常后，承租方已及时通知出租方或采取停止使用、报修等合理措施。"
            conclusion = "承租人防止损失扩大义务：已履行，设备故障导致不可用的，承租人可主张减租或免责。"
        elif facts.equipment_scrapped:
            minor = "识别到设备出现故障或异常后，承租方未及时通知或未采取合理措施，继续使用导致设备彻底报废。"
            conclusion = "承租人防止损失扩大义务：未履行，对扩大损失承担全部责任。"
        else:
            minor = "识别到设备出现故障或异常后，承租方未及时通知或未采取合理措施，损失因此扩大。"
            if facts.actual_loss > 0:
                conclusion = f"承租人防止损失扩大义务：未履行，对扩大损失承担{facts.actual_loss:.2f}元。"
            else:
                conclusion = "承租人防止损失扩大义务：未履行，对扩大损失承担相应责任，具体金额需结合维修单或鉴定结果确定。"
        return _format_edge_patch_output(config.patch_name("E1", "承租人防止损失扩大义务"), major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "traffic_accident_liability" and facts.traffic_accident:
        major = "车辆租赁中因交通事故造成车辆损失的，应结合事故责任认定、保险赔付、实际维修损失和押金担保目的判断是否扣款。"
        if facts.traffic_accident_other_responsible:
            minor = "识别到车辆损坏来源于交通事故，且事故责任由对方或第三方承担，未识别到承租人应承担事故责任。"
            conclusion = "交通事故由对方或第三方承担责任，出租人不得以该事故为由扣押金；出租人可向责任方或保险渠道追偿"
        elif facts.traffic_accident_tenant_responsible:
            minor = f"识别到车辆损坏来源于交通事故，且{config.tenant_label}对事故承担全部或主要责任。"
            deduction = facts.agreed_deduction if facts.agreed_deduction > 0 else facts.actual_loss
            if facts.actual_loss > 0 and facts.agreed_deduction > facts.actual_loss * 1.3:
                deduction = facts.actual_loss
            if deduction > 0:
                conclusion = f"{config.tenant_label}按事故责任承担合理维修费，扣除{deduction:.2f}元后返还余额"
            else:
                conclusion = f"{config.tenant_label}对交通事故承担责任，出租人可在实际维修损失范围内扣除押金，但需证明具体损失金额"
        elif facts.traffic_accident_unknown_liability:
            minor = "识别到车辆损坏来源于交通事故，但事故责任尚未认定或现有事实无法证明责任归属。"
            conclusion = "交通事故责任尚未查清，现阶段不得当然扣押金；需补充事故责任认定、保险赔付和实际维修损失后再计算"
        else:
            minor = "识别到车辆损坏来源于交通事故，但未识别到事故责任认定结果。"
            conclusion = "需先审查交通事故责任认定；责任未明确前，不宜直接进入维修金额扣除"
        return _format_edge_patch_output("交通事故责任", major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "V1" and facts.damage_reason == "tenant_fault" and facts.vehicle_under_repair and facts.stoppage_loss_claimed:
        major = "司法实践中，车辆因承租人过错损坏并在合理维修期间无法营运的，出租人可主张停运损失，通常按日租金乘以实际维修天数计算。"
        if facts.replacement_vehicle_provided:
            minor = "识别到车辆因承租人原因损坏并维修，但承租人已提供代步车或出租人已取得替代车辆使用利益。"
            conclusion = "停运损失不成立，出租人不得重复主张维修期间租金损失。"
        elif facts.vehicle_over_repair:
            minor = "识别到车辆维修期间出租人主张停运损失，但存在过度维修、扩大维修或维修时间明显不合理的事实。"
            conclusion = "停运损失应限于必要、合理维修期间；超过合理维修期间的租金损失不予支持。"
        elif facts.daily_rent > 0 and facts.repair_days > 0:
            amount = facts.daily_rent * facts.repair_days
            minor = f"识别到车辆因承租人原因损坏并维修，出租人主张维修期间租金损失；日租金为{facts.daily_rent:.2f}元，实际维修天数为{facts.repair_days:g}天。"
            conclusion = f"承租人承担停运损失 {amount:.2f} 元，计算依据为日租金{facts.daily_rent:.2f}元 × 维修天数{facts.repair_days:g}天。"
        else:
            minor = "识别到车辆因承租人原因损坏并维修，出租人主张维修期间租金损失，但未稳定识别到日租金或实际维修天数。"
            conclusion = "停运损失需补充日租金标准和合理维修天数后计算；维修必要性和维修天数应以维修单或鉴定报告为准。"
        return _format_edge_patch_output(config.patch_name("V1", "停运损失"), major, minor, conclusion, facts, path_prefix, procedure_findings)

    if patch_id == "E2" and facts.equipment_total_loss and facts.loss_during_lease:
        major = "租赁物在租赁期间灭失导致合同无法继续履行的，灭失前已经发生的租金义务不因此免除，灭失后的未来租金不再继续发生。"
        rent_text = f"灭失前已产生租金{facts.unpaid_rent:.2f}元仍需支付，" if facts.unpaid_rent > 0 else "灭失前已产生租金仍需支付，"
        if facts.loss_tenant_fault:
            minor = "识别到设备在租赁合同履行期间完全灭失，且灭失原因可归责于承租方。"
            amount_text = f"{facts.actual_loss:.2f}元" if facts.actual_loss > 0 else "以设备实际价值或鉴定损失为准"
            conclusion = f"设备灭失：{rent_text}未来租金不再支付，可归责于承租方，赔偿责任为{amount_text}。"
        elif facts.loss_no_fault:
            minor = "识别到设备在租赁合同履行期间完全灭失，且灭失原因属于自然灾害或不可归责于双方的原因。"
            conclusion = f"设备灭失：{rent_text}未来租金不再支付，不可归责于双方，合同解除，已付租金按实际使用期间结算。"
        else:
            minor = "识别到设备在租赁合同履行期间完全灭失，但现有事实未能稳定判断灭失原因是否可归责于承租方。"
            conclusion = f"设备灭失：{rent_text}未来租金不再支付，需查明可归责或不可归责原因后确定赔偿责任。"
        return _format_edge_patch_output(config.patch_name("E2", "租赁物灭失后的租金支付"), major, minor, conclusion, facts, path_prefix, procedure_findings)

    return None


def _run_mounted_patches(
    facts: ExtractedFacts,
    config: LeaseTypeConfig,
    node_id: str,
    mount_mode: str,
    path_prefix: Optional[List[str]] = None,
    procedure_findings: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    for patch_id in config.patch_ids_at(node_id, mount_mode):
        output = _run_configured_patch(patch_id, facts, config, path_prefix, procedure_findings)
        if output:
            return output
    return None


def _run_indefinite_lease_patch(
    facts: ExtractedFacts,
    config: LeaseTypeConfig,
    path_prefix: Optional[List[str]] = None,
    procedure_findings: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    if "indefinite_lease" not in set(config.enabled_patches) or not facts.indefinite_lease:
        return None

    major = "《民法典》第734条规定，租赁期限届满，承租人继续使用租赁物，出租人没有提出异议的，原租赁合同继续有效，但是租赁期限为不定期。"
    minor = f"识别到原{config.display_name}合同有固定期限且期限已经届满，{config.tenant_label}期满后{config.continue_use_label}{config.asset_label}，{config.lessor_label}继续收租或未提出异议，双方未签订新的租赁合同。"
    conclusion = f"租赁期满后双方未续签合同，但{config.tenant_label}{config.continue_use_label}{config.asset_label}、{config.lessor_label}继续收租，原合同转为不定期租赁。任何一方可随时解除合同，但应提前合理期限（通常1个月）通知对方。{config.deposit_label}退还按实际损坏情况处理，不适用{config.early_return_label}违约金条款。"
    return _format_output(
        major=major,
        minor=minor,
        conclusion=conclusion,
        triggered_items=["不定期租赁"],
        facts=facts,
        path=[*(path_prefix or []), "补丁六：不定期租赁"],
        procedure_findings=procedure_findings,
        footer_label="触发补丁",
    )


def _procedure_findings(facts: ExtractedFacts, config: LeaseTypeConfig) -> List[str]:
    findings: List[str] = []
    if facts.asks_jurisdiction:
        findings.append(config.procedure_court)
    if facts.signer_not_landlord:
        findings.append(config.non_lessor_signer_result)
    elif facts.asks_defendant:
        findings.append("合同签署方是谁，就列谁为被告")
    return findings


def _only_procedure_question(facts: ExtractedFacts) -> bool:
    return (
        (facts.asks_jurisdiction or facts.asks_defendant or facts.signer_not_landlord)
        and not facts.termination_requested
        and not facts.house_sold
        and not facts.pre_delivery_defect
        and not facts.third_party_defect
        and not facts.expropriation_or_demolition
        and not facts.serious_safety_risk
        and not facts.tenant_dead
        and not facts.changed_circumstances
        and not facts.illegal_building
        and not facts.sublease_chain_dispute
        and not facts.landlord_dead
        and not facts.indefinite_lease
        and facts.has_damage is None
        and not facts.is_early_termination
        and facts.contract_valid is not False
    )


def adjudicate_deposit_v2(
    case_text: str,
    today: Optional[date] = None,
    contract_type: Optional[str] = None,
) -> Dict[str, Any]:
    config = get_lease_config(contract_type)
    facts = extract_facts(case_text, config.key)
    triggered: List[str] = []
    path: List[str] = []
    today = today or date.today()

    if facts.contract_end_date and facts.contract_end_date <= today:
        facts.fixed_term_expired = True
        facts.indefinite_lease = (
            facts.fixed_term_expired
            and facts.tenant_continues_use_after_expiry
            and facts.landlord_collects_rent_or_no_objection
            and facts.no_new_lease_contract
        )

    path.append("程序审查")
    contract_type_patch_output = _run_mounted_patches(
        facts,
        config,
        node_id="contract_type_identification",
        mount_mode=MOUNT_POST,
        path_prefix=path,
    )
    if contract_type_patch_output:
        return contract_type_patch_output

    procedure_findings = _procedure_findings(facts, config)
    if procedure_findings:
        triggered.append("管辖程序")

    proper_defendant_patch_output = _run_mounted_patches(
        facts,
        config,
        node_id="proper_defendant",
        mount_mode=MOUNT_POST,
        path_prefix=path,
        procedure_findings=procedure_findings,
    )
    if proper_defendant_patch_output:
        return proper_defendant_patch_output

    if _only_procedure_question(facts):
        major = f"{config.display_name}纠纷的程序问题应先确认管辖法院和适格被告；被告应当按照合同签署方确定。"
        minor = "用户提出的是起诉地点或被告确定问题，未提出需要继续判断合同解除、房屋买卖、房屋瑕疵或押金扣退的事实。"
        conclusion = "；".join(procedure_findings)
        return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    procedure_patch_output = _run_mounted_patches(
        facts,
        config,
        node_id="procedure_review",
        mount_mode=MOUNT_POST,
        path_prefix=path,
        procedure_findings=procedure_findings,
    )
    if procedure_patch_output:
        return procedure_patch_output

    contract_validity_patch_output = _run_mounted_patches(
        facts,
        config,
        node_id="contract_validity",
        mount_mode=MOUNT_PRE,
        path_prefix=path,
        procedure_findings=procedure_findings,
    )
    if contract_validity_patch_output:
        return contract_validity_patch_output

    path.append("合同解除权")
    termination_reason = ""
    if facts.agreed_termination:
        termination_reason = "合同已经约定解除条件，按合同约定处理"
    elif facts.force_majeure:
        termination_reason = "存在不可抗力，导致合同目的不能实现"
    elif facts.fundamental_breach:
        if facts.unauthorized_sublease:
            termination_reason = "承租人擅自转租，构成根本违约"
        elif facts.rent_arrears_periods > 2 or facts.rent_arrears_months >= 6:
            termination_reason = "承租人欠租超过两期或累计达到六个月租金，构成根本违约"
        else:
            termination_reason = "一方存在根本违约"

    if termination_reason:
        triggered.append("合同解除权")
        if facts.landlord_knowledge_date and _years_between(facts.landlord_knowledge_date, today) > 1:
            major = "《民法典》第563条规定，一方根本违约时守约方可以解除合同；解除权人在知道或者应当知道解除事由后一年内不行使的，解除权消灭。"
            minor = f"识别到解除事由为：{termination_reason}；{config.lessor_label}知道或应当知道解除事由的时间为{facts.landlord_knowledge_date.isoformat()}，截至{today.isoformat()}已经超过一年。"
            conclusion = "解除权已经消灭，不能再以该事由单方解除合同"
            return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

        major = "《民法典》第563条规定，出现不可抗力、一方根本违约，或者合同约定的解除条件成就时，守约方可以解除合同。"
        minor = f"识别到解除事由为：{termination_reason}。"
        conclusion = f"合同依法解除，根据解除原因处理{config.deposit_label}，违约方承担相应责任"
        return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append("买卖不破租赁")
    if facts.house_sold and facts.sale_before_lease:
        triggered.append("买卖不破租赁")
        major = f"{config.asset_label}已经转让后，原{config.lessor_label}不再享有出租该{config.asset_label}的权利；无权出租导致租赁合同不能正常履行的，应承担相应责任。"
        minor = f"识别到{config.asset_label}先转让，原{config.lessor_label}在转让后又出租给{config.tenant_label}。"
        conclusion = f"租赁合同无效，{config.tenant_label}可向原{config.lessor_label}主张违约赔偿"
        return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.house_sold and facts.lease_before_sale:
        triggered.append("买卖不破租赁")
        major = "《民法典》第725条规定，租赁物在承租人按照租赁合同占有期限内发生所有权变动的，不影响租赁合同的效力。"
        minor = f"识别到{config.asset_label}是在租赁合同成立并履行期间转让给新的所有权人。"
        conclusion = (
            config.lease_before_transfer_conclusion
            or f"租赁合同对新的所有权人继续有效，{config.tenant_label}无需返还{config.asset_label}，{config.deposit_label}事宜仍按原合同执行"
        )
        return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.sale_without_notice:
        triggered.append("买卖不破租赁")
        major = f"{config.lessor_label}转让租赁{config.asset_label}时，应当在合理期限内通知{config.tenant_label}；未通知造成损失的，{config.tenant_label}可以依法主张赔偿。"
        minor = f"识别到{config.lessor_label}转让{config.asset_label}时没有提前通知{config.tenant_label}。"
        conclusion = f"{config.tenant_label}可以就未通知造成的损失向{config.lessor_label}主张赔偿"
        return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    path.append(config.defect_module_label)
    asset_defect_patch_output = _run_mounted_patches(
        facts,
        config,
        node_id="asset_defect",
        mount_mode=MOUNT_REPLACE,
        path_prefix=path,
        procedure_findings=procedure_findings,
    )
    if asset_defect_patch_output:
        return asset_defect_patch_output

    if facts.expropriation_or_demolition:
        triggered.append(config.defect_module_label)
        major = f"因依法征收、查封或强制处置导致租赁{config.asset_label}不能继续使用的，合同无法继续履行；{config.deposit_label}作为履约担保应当返还。"
        minor = f"识别到租赁{config.asset_label}被依法征收、查封或强制处置。"
        conclusion = config.expropriation_conclusion or f"合同自动终止，{config.deposit_label}全额退还，相关补偿或处置权益归所有权人"
        return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.serious_safety_risk:
        triggered.append(config.defect_module_label)
        major = f"{config.asset_label}存在严重安全隐患，导致租赁目的不能实现，且该原因不可归责于双方的，合同应当终止。"
        minor = f"识别到{config.asset_label}存在严重安全隐患或无法安全使用的情况。"
        conclusion = f"合同终止，{config.deposit_label}全额退还"
        return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.pre_delivery_defect:
        triggered.append(config.defect_module_label)
        major = f"{config.lessor_label}应当交付符合约定用途的{config.asset_label}；交付前已经存在影响使用的瑕疵，{config.lessor_label}应承担修复责任。"
        minor = f"识别到{config.asset_label}在交付前已经存在影响使用的瑕疵。"
        conclusion = f"{config.lessor_label}承担修复责任，{config.tenant_label}可以主张减租"
        return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.third_party_defect:
        triggered.append(config.defect_module_label)
        major = f"租赁期间{config.asset_label}因第三方原因影响正常使用的，{config.lessor_label}仍应保障{config.tenant_label}正常使用，并可另行向责任方追偿。"
        minor = f"识别到{config.asset_label}的问题由第三方原因导致。"
        conclusion = f"{config.lessor_label}负责协调处理和追偿，{config.tenant_label}可以主张减租"
        return _format_output(major, minor, conclusion, triggered, facts, path, procedure_findings)

    term_patch_output = _run_mounted_patches(
        facts,
        config,
        node_id="term_expiry",
        mount_mode=MOUNT_PRE,
        path_prefix=path,
        procedure_findings=procedure_findings,
    )
    if term_patch_output:
        return term_patch_output

    path.append("押金结算")
    deposit_major = (
        f"租赁{config.deposit_label}应按合同效力、履行期限、损坏事实、损坏原因及举证责任依次审查；"
        f"不得用明显不公平的条款扩大{config.tenant_label}责任，约定扣款明显高于实际损失的，应当调低。"
    )

    if facts.has_third_party and not facts.traffic_accident:
        conclusion = "本案涉及侵权责任，非合同纠纷，不适用本合同裁判引擎"
        minor = f"自然语言事实中识别到合同外第三方介入，争议基础已超出租赁合同相对方之间的{config.deposit_label}返还关系。"
        return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.contract_end_date and _years_between(facts.contract_end_date, today) > 3:
        conclusion = "诉讼时效已过，驳回请求"
        minor = f"识别到合同终止日期为{facts.contract_end_date.isoformat()}，截至{today.isoformat()}已超过三年。"
        return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.contract_valid is False:
        conclusion = f"{config.deposit_label}全额返还"
        minor = f"识别到合同无效或未成立事实，{config.deposit_label}不应作为有效合同项下的履约担保继续由{config.lessor_label}占有。"
        return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.overbroad_damage_liability_clause:
        triggered.append(f"明显扩大{config.tenant_label}损坏赔偿责任的条款无效")

    if facts.is_early_termination and facts.has_early_termination_clause:
        deduction = facts.agreed_deduction
        if facts.actual_loss > 0 and deduction > facts.actual_loss * 1.3:
            triggered.append("约定扣款超过实际损失百分之一百三十，调低至实际损失")
            deduction = facts.actual_loss
        conclusion = f"{config.early_return_label}按合同约定处理，扣除{deduction:.2f}元后返还余额" if deduction > 0 else f"{config.early_return_label}按合同约定处理"
        minor = f"识别到{config.tenant_label}{config.early_return_label}，且合同对{config.early_return_label}的{config.deposit_label}或违约扣款已有约定。"
        return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)

    damage_status_patch_output = _run_mounted_patches(
        facts,
        config,
        node_id="damage_status",
        mount_mode=MOUNT_PRE,
        path_prefix=path,
        procedure_findings=procedure_findings,
    )
    if damage_status_patch_output:
        return damage_status_patch_output

    if facts.has_damage is False:
        conclusion = f"{config.deposit_label}全额返还"
        minor = f"识别到返还{config.asset_label}时无损坏，{config.lessor_label}缺少扣留{config.deposit_label}的事实基础。"
        return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.notified_defect_at_check_in and facts.landlord_knew_no_objection:
        triggered.append(
            config.notified_defect_patch_label
            or f"{config.tenant_label}接收时已告知瑕疵且{config.lessor_label}知情未提异议"
        )
        conclusion = f"{config.deposit_label}全额返还"
        minor = f"识别到相关瑕疵在接收{config.asset_label}时已由{config.tenant_label}告知，{config.lessor_label}知情后未提出异议，返还时不得反向归责{config.tenant_label}。"
        return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)

    damage_cause_patch_output = _run_mounted_patches(
        facts,
        config,
        node_id="damage_cause",
        mount_mode=MOUNT_POST,
        path_prefix=path,
        procedure_findings=procedure_findings,
    )
    if damage_cause_patch_output:
        return damage_cause_patch_output

    if facts.overbroad_damage_liability_clause and facts.damage_reason in (None, "natural_wear", "unproven"):
        conclusion = f"{config.deposit_label}全额返还"
        minor = f"虽有扩大{config.tenant_label}责任的约定，但该约定把正常使用损耗或原因不明的风险都转给{config.tenant_label}，不能作为扣{config.deposit_label}依据。"
        return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.damage_reason in ("natural_wear", "unproven") or facts.evidence_can_prove_cause is False:
        conclusion = f"{config.deposit_label}全额返还"
        minor = f"识别到损坏属于正常损耗，或现有事实无法证明损坏由{config.tenant_label}造成，{config.lessor_label}应承担举证不能的不利后果。"
        return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)

    if facts.damage_reason == "tenant_fault":
        deduction = facts.actual_loss
        if facts.agreed_deduction > 0:
            deduction = facts.agreed_deduction
        if facts.actual_loss > 0 and facts.agreed_deduction > facts.actual_loss * 1.3:
            triggered.append("约定扣款超过实际损失百分之一百三十，调低至实际损失")
            deduction = facts.actual_loss
        amount_patch_output = _run_mounted_patches(
            facts,
            config,
            node_id="amount_calculation",
            mount_mode=MOUNT_POST,
            path_prefix=path,
            procedure_findings=procedure_findings,
        )
        if amount_patch_output:
            return amount_patch_output
        conclusion = f"扣除维修费{deduction:.2f}元后返还余额"
        minor = f"识别到损坏由{config.tenant_label}过错造成，{config.lessor_label}可在合理维修费或经调低后的实际损失范围内扣除{config.deposit_label}。"
        return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)

    conclusion = "事实要素不足，需补充合同解除原因、房屋买卖情况、房屋瑕疵、退租时间、损坏原因或损失金额后再裁判"
    minor = "自然语言事实未能稳定识别出足以进入最终结论的关键事实。"
    return _format_output(deposit_major, minor, conclusion, triggered, facts, path, procedure_findings)
