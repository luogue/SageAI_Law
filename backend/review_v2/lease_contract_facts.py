"""Unified fact extraction for house lease contract review.

The review engine should not let each checkpoint rediscover facts from the
same contract independently. This module extracts a shared fact layer once,
keeps source evidence for each fact, and lets checkpoint rules consume the
same source of truth.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional

from review_v2.clause_parser import ParsedClause, formal_evidence_clauses, parse_contract_clauses
from review_v2.formula_parser import parse_penalty_formula
from review_v2.template_parser import TemplateOption, is_blank_option_value, parse_template_options


UNSPECIFIED_PARTY = "not_specified"
LANDLORD = "landlord"
TENANT = "tenant"


@dataclass(frozen=True)
class FactEvidence:
    field: str
    value: Any
    clause_id: str
    section: str
    source_location: str
    source_text: str
    selected: bool = True
    source_type: str = "explicit_clause"

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "clause_id": self.clause_id,
            "section": self.section,
            "location": self.source_location,
            "text": self.source_text,
            "selected": self.selected,
            "source_type": self.source_type,
        }


@dataclass(frozen=True)
class FactNode:
    value: Any
    confidence: float
    evidence: list[FactEvidence] = field(default_factory=list)
    selected: bool = True
    source_type: str = "explicit_clause"

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "confidence": self.confidence,
            "evidence": [item.to_public_dict() for item in self.evidence],
            "selected": self.selected,
            "source_type": self.source_type,
        }


@dataclass(frozen=True)
class FactBackedClause:
    """A clause-like wrapper so fact evidence can reuse report evidence code."""

    clause_id: str
    location: str
    title: str
    text: str
    section_type: str = "正式合同条款"
    level: int = 0
    fact_field: str = ""
    fact_value: Any = None

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PropertyFacts:
    address: Optional[str] = None
    certificate_number: Optional[str] = None
    owner: Optional[str] = None
    is_owner: Optional[bool] = None
    is_mortgaged: Optional[bool] = None
    is_coowned: Optional[bool] = None


@dataclass(frozen=True)
class LeaseTermFacts:
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    term: Optional[str] = None


@dataclass(frozen=True)
class RentFacts:
    monthly_amount: Optional[str] = None
    payment_due_day: Optional[str] = None
    payment_cycle: Optional[str] = None
    payment_method: Optional[str] = None
    payment_account: Optional[str] = None
    daily_amount: Optional[str] = None


@dataclass(frozen=True)
class DepositFacts:
    amount: Optional[str] = None
    is_interest_bearing: Optional[bool] = None
    return_condition: Optional[str] = None
    return_deadline: Optional[str] = None


@dataclass(frozen=True)
class RepairFacts:
    natural_wear: str = UNSPECIFIED_PARTY
    tenant_fault: str = UNSPECIFIED_PARTY


@dataclass(frozen=True)
class SubleaseFacts:
    is_allowed: Optional[bool] = None
    requires_consent: Optional[bool] = None


@dataclass(frozen=True)
class EarlyTerminationFacts:
    exists: bool = False
    tenant_formula: Optional[str] = None
    landlord_formula: Optional[str] = None
    penalty_formula: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class JurisdictionFacts:
    type: Optional[str] = None
    court: Optional[str] = None
    arbitration_body: Optional[str] = None
    is_specified: bool = False


@dataclass(frozen=True)
class ForceMajeureFacts:
    is_defined: bool = False
    notice_required: Optional[bool] = None
    settlement_defined: Optional[bool] = None


@dataclass(frozen=True)
class RentDefaultFacts:
    exists: bool = False
    threshold_type: Optional[str] = None
    threshold_value: Optional[int] = None
    threshold_unit: Optional[str] = None
    requires_notice: Optional[bool] = None
    grace_period: Optional[int] = None
    effect: Optional[str] = None


@dataclass(frozen=True)
class TerminationFacts:
    rent_default: RentDefaultFacts = field(default_factory=RentDefaultFacts)


@dataclass(frozen=True)
class PropertySaleFacts:
    notice_required: Optional[bool] = None
    preemptive_right: Optional[bool] = None


@dataclass(frozen=True)
class SafetyFacts:
    dangerous_house_termination: Optional[bool] = None
    defect_termination: Optional[bool] = None
    landlord_safety_obligation: Optional[bool] = None


@dataclass(frozen=True)
class HandoverFacts:
    inventory_exists: Optional[bool] = None
    photo_required: Optional[bool] = None
    key_return_defined: Optional[bool] = None


@dataclass(frozen=True)
class HouseLeaseContractFacts:
    property: PropertyFacts = field(default_factory=PropertyFacts)
    lease: LeaseTermFacts = field(default_factory=LeaseTermFacts)
    rent: RentFacts = field(default_factory=RentFacts)
    deposit: DepositFacts = field(default_factory=DepositFacts)
    repair: RepairFacts = field(default_factory=RepairFacts)
    sublease: SubleaseFacts = field(default_factory=SubleaseFacts)
    termination: TerminationFacts = field(default_factory=TerminationFacts)
    early_termination: EarlyTerminationFacts = field(default_factory=EarlyTerminationFacts)
    jurisdiction: JurisdictionFacts = field(default_factory=JurisdictionFacts)
    force_majeure: ForceMajeureFacts = field(default_factory=ForceMajeureFacts)
    property_sale: PropertySaleFacts = field(default_factory=PropertySaleFacts)
    safety: SafetyFacts = field(default_factory=SafetyFacts)
    handover: HandoverFacts = field(default_factory=HandoverFacts)
    evidence: Dict[str, FactEvidence] = field(default_factory=dict)
    nodes: Dict[str, FactNode] = field(default_factory=dict)

    def to_public_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["evidence"] = {key: evidence.to_public_dict() for key, evidence in self.evidence.items()}
        data["fact_nodes"] = {key: node.to_public_dict() for key, node in self.nodes.items()}
        data["early_termination"]["tenant"] = {
            "formula": self.early_termination.tenant_formula,
            "penalty_formula": self.early_termination.penalty_formula,
            "evidence": self.evidence.get("early_termination.penalty_formula").to_public_dict()
            if self.evidence.get("early_termination.penalty_formula")
            else None,
        }
        return data

    def evidence_clause(self, field_name: str, *, title: str = "统一事实图谱") -> Optional[FactBackedClause]:
        evidence = self.evidence.get(field_name)
        if not evidence:
            return None
        return FactBackedClause(
            clause_id=f"FACT-{field_name}",
            location=evidence.source_location,
            title=title,
            text=evidence.source_text,
            fact_field=evidence.field,
            fact_value=evidence.value,
        )

    def node(self, field_name: str) -> Optional[FactNode]:
        return self.nodes.get(field_name)


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def _first_group(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, re.S)
    if not match:
        return None
    value = match.group(1).strip()
    return value or None


SELECTED_MARKS = {"☑", "☒", "√", "■", "✅"}
UNSELECTED_MARKS = {"□", "☐", "○", "◇"}


def _best_template_option(text: str, predicate) -> Optional[TemplateOption]:
    candidates = [option for option in parse_template_options(text) if predicate(option.label)]
    if not candidates:
        return None
    candidates.sort(key=lambda item: (-item.priority, item.blank, -len(item.label)))
    best = candidates[0]
    if best.selected:
        return best
    return None


def _is_blank_fact_value(value: Any) -> bool:
    return is_blank_option_value(value)


def _clause_selected(clause: ParsedClause, value: Any = None) -> bool:
    text = clause.text
    if value is not None and _is_blank_fact_value(value):
        return False
    if re.search(r"[☑☒√■]", text):
        return True
    if re.search(r"^[□○◇]\s*", text.strip()):
        return False
    if "□" in text and re.search(r"□\s*[_＿]{3,}", text) and not re.search(r"[☑☒√■]", text):
        return False
    return True


def _make_fact_evidence(field_name: str, value: Any, clause: ParsedClause, *, selected: bool = True, source_type: str = "explicit_clause") -> FactEvidence:
    return FactEvidence(
        field=field_name,
        value=value,
        clause_id=clause.clause_id,
        section=clause.location,
        source_location=clause.location,
        source_text=clause.text,
        selected=selected,
        source_type=source_type,
    )


def _set_evidence(
    evidence: Dict[str, FactEvidence],
    nodes: Dict[str, FactNode],
    field_name: str,
    value: Any,
    clause: ParsedClause,
    *,
    confidence: float = 0.9,
    selected: Optional[bool] = None,
    source_type: str = "explicit_clause",
) -> None:
    selected_value = _clause_selected(clause, value) if selected is None else selected
    if _is_blank_fact_value(value) or not selected_value or field_name in evidence:
        return
    fact_evidence = _make_fact_evidence(field_name, value, clause, selected=selected_value, source_type=source_type)
    evidence[field_name] = fact_evidence
    nodes[field_name] = FactNode(
        value=value,
        confidence=confidence,
        evidence=[fact_evidence],
        selected=selected_value,
        source_type=source_type,
    )


def _is_concrete_court(court: str) -> bool:
    if not court:
        return False
    generic_terms = ("有管辖权", "合同签订地", "原告所在地", "被告所在地")
    return "人民法院" in court and not any(term in court for term in generic_terms)


def _normalize_court(raw: str) -> str:
    court = re.sub(r"^(依法|均可|可|应|向)", "", raw or "").strip(" ，,。；;：:")
    court = re.sub(r"^(租赁)?房屋所在地", "", court)
    court = re.sub(r"^不动产所在地", "", court)
    court = court.replace("人民法院起诉", "人民法院")
    return court


def _extract_payment_method(text: str) -> Optional[str]:
    methods = []
    for checked, label in (("☑", "transfer"), ("√", "transfer"), ("■", "transfer")):
        if checked in text and "银行" in text:
            methods.append(label)
    for raw_label, normalized in (("银行转账", "transfer"), ("转账", "transfer"), ("现金", "cash"), ("微信", "wechat"), ("支付宝", "alipay")):
        if normalized == "transfer" and "transfer" in methods:
            continue
        if raw_label in text and normalized not in methods:
            methods.append(normalized)
    if not methods:
        return None
    # Do not treat unchecked free-text checkbox blanks as a payment method.
    return "、".join(method for method in methods if not re.fullmatch(r"□[_＿\s]+", method))


def _extract_payment_schedule(text: str) -> tuple[Optional[str], Optional[str]]:
    cycle_patterns = (
        ("monthly", "每月"),
        ("quarterly", "每季度"),
        ("semiannual", "每半年"),
        ("yearly", "每年"),
    )
    option = _best_template_option(
        text,
        lambda label: bool(re.search(r"每(月|季度|半年|年)\s*(\d+|[一二三四五六七八九十]+)\s*(?:日|号)?\s*(?:前|以前|之前)?", label or "")),
    )
    if option:
        label = option.label
        match = re.search(r"每(月|季度|半年|年)\s*(\d+|[一二三四五六七八九十]+)\s*(?:日|号)?", label)
        if match:
            cycle_label = match.group(1)
            cycle = {
                "月": "monthly",
                "季度": "quarterly",
                "半年": "semiannual",
                "年": "yearly",
            }.get(cycle_label)
            value = _chinese_number_to_int(match.group(2))
            return cycle, str(value or match.group(2))
    for cycle, marker in cycle_patterns:
        escaped_marker = re.escape(marker)
        patterns = (
            rf"{escaped_marker}\s*(\d+|[一二三四五六七八九十]+)\s*(?:日|号)?\s*(?:前|以前|之前).{{0,32}}(?:支付|付清|交纳|缴纳|向甲方支付租金)",
            rf"应于.{{0,12}}{escaped_marker}\s*(\d+|[一二三四五六七八九十]+)\s*(?:日|号)?\s*(?:前|以前|之前)",
            rf"【\s*{escaped_marker}\s*(\d+|[一二三四五六七八九十]+)\s*(?:日|号)?\s*(?:前|以前|之前)\s*】\s*[☑☒√■]",
        )
        for pattern in patterns:
            value = _first_group(pattern, text)
            if value:
                normalized = _chinese_number_to_int(value)
                return cycle, str(normalized or value)
    return None, None


def _extract_payment_due_day(text: str) -> Optional[str]:
    _, due_day = _extract_payment_schedule(text)
    return due_day


def _extract_payment_cycle(text: str) -> Optional[str]:
    cycle, _ = _extract_payment_schedule(text)
    return cycle


def _extract_payment_due_day_legacy(text: str) -> Optional[str]:
    patterns = (
        r"每月\s*(\d+|[一二三四五六七八九十]+)\s*(?:日|号)?\s*(?:前|以前|之前).{0,24}(?:支付|付清|交纳|缴纳|向甲方支付租金)",
        r"应于.{0,8}每月\s*(\d+|[一二三四五六七八九十]+)\s*(?:日|号)?\s*(?:前|以前|之前)",
        r"【\s*每月\s*(\d+|[一二三四五六七八九十]+)\s*(?:日|号)?\s*(?:前|以前|之前)\s*】\s*[☑☒√■]",
    )
    for pattern in patterns:
        value = _first_group(pattern, text)
        if value:
            return value
    return None


def _extract_payment_account(text: str) -> Optional[str]:
    if not any(term in text for term in ("账号", "银行账号", "收款账户", "开户行", "户名")):
        return None
    return _first_group(r"(?:账号|银行账号|收款账户)[:：]?\s*([-A-Za-z0-9 ]{6,})", text) or "已约定收款账户"


def _extract_area_sqm(text: str) -> Optional[float]:
    match = re.search(r"(\d+(?:\.\d+)?)\s*平方米", text)
    return float(match.group(1)) if match else None


def _extract_daily_rent_amount(text: str, area_sqm: Optional[float]) -> Optional[str]:
    rate_match = re.search(r"(\d+(?:\.\d+)?)\s*元\s*/?\s*(?:平方米|㎡)\s*/?\s*(?:日|天)", text)
    if not rate_match:
        return None
    rate = float(rate_match.group(1))
    if area_sqm:
        return str(round(rate * area_sqm, 2))
    return None


def _has_deposit_term(text: str) -> bool:
    return "押金" in (text or "") or "保证金" in (text or "")


def _extract_deposit_amount(text: str) -> Optional[str]:
    patterns = (
        r"(?:押金|保证金)\s*(\d[\d,，.]*\s*元?)",
        r"(?:押金|保证金)[^。\n]{0,80}即\s*[（(]?\s*人民币\s*[）)]?\s*(\d[\d,，.]*\s*元?)",
        r"(?:押金|保证金)[^。\n]{0,80}(?:金额为|计为|合计为|为人民币|为)\s*(?:人民币)?\s*(\d[\d,，.]*\s*元?)",
        r"(?:人民币)?\s*(\d[\d,，.]*\s*元?)\s*(?:押金|保证金)",
    )
    for pattern in patterns:
        value = _first_group(pattern, text)
        if value and not re.fullmatch(r"\d+\s*(?:个)?月", value):
            return value
    return None


def _extract_return_deadline(text: str) -> Optional[str]:
    if not _has_deposit_term(text) or not any(term in text for term in ("退还", "返还", "退回", "归还")):
        return None
    match = re.search(r"(\d+|[一二三四五六七八九十]+)\s*(个)?\s*(工作日|日|天|自然日|银行工作日)内", text)
    if not match:
        return None
    return "".join(group or "" for group in match.groups())


def _extract_penalty_formula(text: str) -> Optional[Dict[str, Any]]:
    compacted = _compact(text)
    if not ("违约金" in compacted and any(term in compacted for term in ("提前退租", "中途擅自退租", "提前解除"))):
        return None
    default_party = "tenant" if any(term in compacted for term in ("乙方", "承租人")) else "unspecified"
    return parse_penalty_formula(text, default_party=default_party)


def _penalty_formula_label(formula: Optional[Dict[str, Any]]) -> Optional[str]:
    if not formula:
        return None
    base = formula.get("base")
    multiplier = formula.get("multiplier")
    if base and multiplier:
        return f"{base} × {multiplier}"
    if formula.get("type") == "fixed_amount":
        return f"fixed_amount {formula.get('amount')}"
    if formula.get("rate") is not None:
        return f"{base} × {formula.get('rate')}"
    return None


def _extract_rent_default(text: str) -> Optional[RentDefaultFacts]:
    compacted = _compact(text)
    if not any(term in compacted for term in ("欠租", "欠付租金", "逾期不支付租金", "逾期支付租金", "拖欠租金", "未按时支付租金", "未支付租金", "未付款", "仍未支付", "仍未付")):
        return None
    month_match = re.search(r"(?:欠租|拖欠租金|逾期不支付租金|逾期支付租金|未按时支付租金).{0,18}?(?:超过|满|达|达到)?(\d+|[一二三四五六七八九十两]+)(?:个)?月", compacted)
    period_match = re.search(r"(?:连续|累计)?.{0,6}(?:欠租|拖欠租金|逾期不支付租金|逾期支付租金|未按时支付租金).{0,18}?(?:超过|满|达|达到)?(\d+|[一二三四五六七八九十两]+)期", compacted)
    month_before_match = re.search(r"(?:连续|累计)?(\d+|[一二三四五六七八九十两]+)(?:个)?月(?:未支付租金|未按时支付租金|不支付租金)", compacted)
    period_before_match = re.search(r"(?:连续|累计)?(\d+|[一二三四五六七八九十两]+)期(?:未支付租金|未按时支付租金|不支付租金)", compacted)
    day_match = re.search(r"(?:拖欠租金超过|逾期|催告后|通知后|宽限期满后|催告|通知)(\d+|[一二三四五六七八九十两]+)(?:日|天)", compacted)
    amount_match = re.search(r"(?:欠租|拖欠租金|欠付租金|逾期不支付租金|逾期支付租金).{0,10}?(?:达到|超过|累计达到|累计超过)?(?:人民币)?(\d[\d,，.]*)元", compacted)
    value: Optional[int] = None
    unit: Optional[str] = None
    threshold_type: Optional[str] = None
    grace_period: Optional[int] = None
    if month_match or month_before_match:
        value = _chinese_number_to_int((month_match or month_before_match).group(1))
        unit = "month"
        threshold_type = "duration"
    elif period_match or period_before_match:
        value = _chinese_number_to_int((period_match or period_before_match).group(1))
        unit = "period"
        threshold_type = "period_count"
    elif day_match:
        value = _chinese_number_to_int(day_match.group(1))
        unit = "day"
        if "催告" in compacted or "通知" in compacted:
            threshold_type = "notice_grace_period" if ("催告后" in compacted or "通知后" in compacted) else "grace_period"
            grace_period = value
        else:
            threshold_type = "duration"
    elif amount_match:
        value = int(float(amount_match.group(1).replace(",", "").replace("，", "")))
        unit = "yuan"
        threshold_type = "amount"
    elif "催告" in compacted:
        value = None
        unit = "day"
        threshold_type = "grace_period"
    effect = "termination" if any(term in compacted for term in ("解除", "终止", "单方解除")) else ("material_breach" if "重大违约" in compacted or value is not None else None)
    if value is None and unit is None and effect is None:
        return None
    return RentDefaultFacts(
        exists=True,
        threshold_type=threshold_type,
        threshold_value=value,
        threshold_unit=unit,
        requires_notice=("催告" in compacted or "通知" in compacted),
        grace_period=grace_period,
        effect=effect,
    )


def _chinese_number_to_int(value: str) -> Optional[int]:
    if not value:
        return None
    if value.isdigit():
        return int(value)
    mapping = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    if value in mapping:
        return mapping[value]
    if value.startswith("十") and len(value) == 2:
        return 10 + mapping.get(value[1], 0)
    if "十" in value:
        left, _, right = value.partition("十")
        return mapping.get(left, 1) * 10 + mapping.get(right, 0)
    return None


def _safety_fact_from_text(text: str) -> tuple[Optional[bool], Optional[bool], Optional[bool]]:
    dangerous = any(term in text for term in ("危险房屋", "危房", "严重安全隐患", "结构安全"))
    defect = any(term in text for term in ("房屋缺陷危及", "危及乙方安全", "不能安全居住", "安全隐患")) and any(term in text for term in ("解除", "终止"))
    landlord_obligation = any(term in text for term in ("保证安全", "安全状态", "安全使用", "造成人身伤害", "承担赔偿"))
    return dangerous or None, defect or None, landlord_obligation or None


def _extract_house_lease_facts_from_clauses(clauses: list[ParsedClause]) -> HouseLeaseContractFacts:
    evidence: Dict[str, FactEvidence] = {}
    nodes: Dict[str, FactNode] = {}

    property_address: Optional[str] = None
    certificate_number: Optional[str] = None
    owner: Optional[str] = None
    is_owner: Optional[bool] = None
    lease_start: Optional[str] = None
    lease_end: Optional[str] = None
    lease_term: Optional[str] = None
    rent_monthly: Optional[str] = None
    payment_due_day: Optional[str] = None
    payment_cycle: Optional[str] = None
    payment_method: Optional[str] = None
    payment_account: Optional[str] = None
    daily_amount: Optional[str] = None
    deposit_amount: Optional[str] = None
    deposit_interest: Optional[bool] = None
    deposit_condition: Optional[str] = None
    deposit_deadline: Optional[str] = None
    natural_wear = UNSPECIFIED_PARTY
    tenant_fault = UNSPECIFIED_PARTY
    sublease_allowed: Optional[bool] = None
    sublease_requires_consent: Optional[bool] = None
    tenant_formula: Optional[str] = None
    landlord_formula: Optional[str] = None
    early_exists = False
    penalty_formula: Optional[Dict[str, Any]] = None
    court: Optional[str] = None
    jurisdiction_type: Optional[str] = None
    arbitration_body: Optional[str] = None
    court_specified = False
    force_defined = False
    force_notice: Optional[bool] = None
    force_settlement: Optional[bool] = None
    rent_default = RentDefaultFacts()
    property_sale = PropertySaleFacts()
    safety = SafetyFacts()
    handover = HandoverFacts()
    property_area_sqm: Optional[float] = None

    for clause in clauses:
        text = clause.text
        compacted = _compact(text)

        if property_area_sqm is None:
            property_area_sqm = _extract_area_sqm(text)

        if property_address is None:
            property_address = _first_group(r"(?:坐落|地址|房屋位于|租赁房屋位于)[:：]?\s*([^。；;\n]+)", text)
            _set_evidence(evidence, nodes, "property.address", property_address, clause)

        if certificate_number is None:
            certificate_number = _first_group(r"(?:产证编号|不动产权证号|房地产权证号)[:：]?\s*([^，,。；;\n]+)", text)
            if certificate_number is None:
                certificate_number = _first_group(r"((?:沪房地|不动产权第|房地)[^，,。；;\n]*?号)", text)
            _set_evidence(evidence, nodes, "property.certificate_number", certificate_number, clause)

        if owner is None:
            owner = _first_group(r"(?:权利人|产权人|所有权人)[:：]?\s*([^，,。；;\n]+)", text)
            _set_evidence(evidence, nodes, "property.owner", owner, clause)

        if is_owner is None and any(term in text for term in ("产权人", "权利人", "房屋所有权人", "出租权来源")):
            is_owner = bool(any(term in text for term in ("甲方为产权人", "甲方系产权人", "甲方为权利人", "甲方系权利人")))
            if is_owner or "甲方" in text:
                _set_evidence(evidence, nodes, "property.is_owner", is_owner, clause)

        if lease_start is None or lease_end is None:
            lease_match = re.search(
                r"自\s*([^，,。；;\n]{4,30}?)\s*(?:起|至)\s*(?:至|到)?\s*([^，,。；;\n]{4,30}?)(?:止|$)",
                text,
            )
            if lease_match:
                lease_start = lease_start or lease_match.group(1).strip()
                lease_end = lease_end or lease_match.group(2).strip()
                _set_evidence(evidence, nodes, "lease.start_date", lease_start, clause)
                _set_evidence(evidence, nodes, "lease.end_date", lease_end, clause)
        if lease_term is None:
            lease_term = _first_group(r"租赁期限(?:为|共)?[:：]?\s*([^，,。；;\n]+)", text)
            _set_evidence(evidence, nodes, "lease.term", lease_term, clause)

        if rent_monthly is None:
            rent_monthly = _first_group(r"(?:月租金|每月租金|租金标准)[^\d一二三四五六七八九十百千万零〇]{0,12}(\d[\d,，.]*\s*元?)", text)
            _set_evidence(evidence, nodes, "rent.monthly_amount", rent_monthly, clause)
        if payment_due_day is None:
            payment_cycle_candidate, payment_due_day_candidate = _extract_payment_schedule(text)
            payment_due_day = payment_due_day_candidate
            _set_evidence(evidence, nodes, "rent.payment_due_day", payment_due_day, clause)
            if payment_due_day and payment_cycle is None:
                payment_cycle = payment_cycle_candidate or "monthly"
                _set_evidence(evidence, nodes, "rent.payment_cycle", payment_cycle, clause)
        if payment_method is None and any(term in text for term in ("支付方式", "付款方式", "银行转账", "转账", "现金", "微信", "支付宝")):
            payment_method = _extract_payment_method(text)
            _set_evidence(evidence, nodes, "rent.payment_method", payment_method, clause)
        if payment_account is None:
            payment_account = _extract_payment_account(text)
            _set_evidence(evidence, nodes, "rent.payment_account", payment_account, clause)
        if daily_amount is None:
            daily_amount = _extract_daily_rent_amount(text, property_area_sqm)
            _set_evidence(evidence, nodes, "rent.daily_amount", daily_amount, clause)

        if deposit_amount is None:
            deposit_amount = _extract_deposit_amount(text)
            _set_evidence(evidence, nodes, "deposit.amount", deposit_amount, clause)
        if deposit_interest is None and _has_deposit_term(text):
            if "不计息" in text or "无息" in text:
                deposit_interest = False
                _set_evidence(evidence, nodes, "deposit.is_interest_bearing", deposit_interest, clause)
            elif "计息" in text or "利息" in text:
                deposit_interest = True
                _set_evidence(evidence, nodes, "deposit.is_interest_bearing", deposit_interest, clause)
        if deposit_deadline is None:
            deposit_deadline = _extract_return_deadline(text)
            _set_evidence(evidence, nodes, "deposit.return_deadline", deposit_deadline, clause)
        if deposit_condition is None and _has_deposit_term(text) and any(term in text for term in ("结清", "无欠费", "无损坏", "交接", "合同终止", "租赁关系终止", "归还", "返还", "退还")):
            deposit_condition = "已约定押金返还条件"
            _set_evidence(evidence, nodes, "deposit.return_condition", deposit_condition, clause, confidence=0.82)

        if natural_wear == UNSPECIFIED_PARTY:
            has_natural = any(term in text for term in ("自然老化", "自然损耗", "正常磨损", "正常使用", "合理损耗", "非乙方原因", "非承租人原因"))
            if has_natural and any(term in text for term in ("甲方负责", "甲方承担", "出租人负责", "出租人承担", "由甲方维修", "由出租人维修")):
                natural_wear = LANDLORD
                _set_evidence(evidence, nodes, "repair.natural_wear", natural_wear, clause)
            elif has_natural and any(term in text for term in ("乙方负责", "乙方承担", "承租人负责", "承租人承担")):
                natural_wear = TENANT
                _set_evidence(evidence, nodes, "repair.natural_wear", natural_wear, clause)

        if tenant_fault == UNSPECIFIED_PARTY:
            has_tenant = "乙方" in text or "承租人" in text
            has_fault = any(term in text for term in ("使用不当", "人为", "过错", "故意", "重大过失", "擅自"))
            has_liability = any(term in text for term in ("赔偿", "承担", "负责维修", "修复", "负责修复"))
            negated_tenant_cause = any(term in text for term in ("非乙方原因", "非承租人原因", "非因乙方原因", "非因承租人原因"))
            if has_tenant and has_fault and has_liability and not negated_tenant_cause:
                tenant_fault = TENANT
                _set_evidence(evidence, nodes, "repair.tenant_fault", tenant_fault, clause)

        if sublease_allowed is None and "转租" in text:
            if "不得转租" in compacted or "不得擅自转租" in compacted or "禁止转租" in compacted:
                sublease_allowed = False
            elif "经甲方书面同意" in compacted or "经出租人书面同意" in compacted:
                sublease_allowed = True
                sublease_requires_consent = True
            _set_evidence(evidence, nodes, "sublease.is_allowed", sublease_allowed, clause)
            _set_evidence(evidence, nodes, "sublease.requires_consent", sublease_requires_consent, clause)

        if tenant_formula is None and any(term in text for term in ("乙方", "承租人")):
            penalty_formula = _extract_penalty_formula(text)
            tenant_formula = _penalty_formula_label(penalty_formula)
            if tenant_formula:
                early_exists = True
                _set_evidence(evidence, nodes, "early_termination.exists", early_exists, clause)
                _set_evidence(evidence, nodes, "early_termination.penalty_formula", penalty_formula, clause)
            _set_evidence(evidence, nodes, "early_termination.tenant_formula", tenant_formula, clause)
        if landlord_formula is None and any(term in text for term in ("甲方", "出租人", "提前收回")) and "提前退租" not in text:
            landlord_penalty_formula = _extract_penalty_formula(text)
            landlord_formula = _penalty_formula_label(landlord_penalty_formula)
            if landlord_formula:
                early_exists = True
                _set_evidence(evidence, nodes, "early_termination.exists", early_exists, clause)
            _set_evidence(evidence, nodes, "early_termination.landlord_formula", landlord_formula, clause)

        if not rent_default.exists:
            extracted_rent_default = _extract_rent_default(text)
            if extracted_rent_default:
                rent_default = extracted_rent_default
                _set_evidence(evidence, nodes, "termination.tenant.rent_default.exists", True, clause)
                _set_evidence(evidence, nodes, "termination.tenant.rent_default.threshold", {"type": rent_default.threshold_type, "value": rent_default.threshold_value, "unit": rent_default.threshold_unit}, clause)
                _set_evidence(evidence, nodes, "termination.tenant.rent_default.threshold_type", rent_default.threshold_type, clause)
                _set_evidence(evidence, nodes, "termination.tenant.rent_default.threshold_value", rent_default.threshold_value, clause)
                _set_evidence(evidence, nodes, "termination.tenant.rent_default.threshold_unit", rent_default.threshold_unit, clause)
                _set_evidence(evidence, nodes, "termination.tenant.rent_default.effect", rent_default.effect, clause)
                _set_evidence(evidence, nodes, "termination.tenant.rent_default.requires_notice", rent_default.requires_notice, clause)
                _set_evidence(evidence, nodes, "termination.tenant.rent_default.grace_period", rent_default.grace_period, clause)

        if court is None and ("法院" in text or "仲裁" in text or "起诉" in text):
            court_match = re.search(r"向\s*([^，,。；;\n]{2,40}?人民法院)\s*起诉", text)
            if court_match:
                candidate = _normalize_court(court_match.group(1))
                court = candidate
                jurisdiction_type = "court"
                court_specified = _is_concrete_court(candidate)
                _set_evidence(evidence, nodes, "jurisdiction.type", jurisdiction_type, clause)
                _set_evidence(evidence, nodes, "jurisdiction.court", court, clause)
                _set_evidence(evidence, nodes, "jurisdiction.is_specified", court_specified, clause)
                if "仲裁委员会" in text and re.search(r"□\s*提交.{0,12}[_＿]{3,}.{0,12}仲裁委员会", text):
                    fact_evidence = _make_fact_evidence("jurisdiction.arbitration_body", None, clause, selected=False, source_type="unchecked_option")
                    nodes["jurisdiction.arbitration_body"] = FactNode(
                        value=None,
                        confidence=0.95,
                        evidence=[fact_evidence],
                        selected=False,
                        source_type="unchecked_option",
                    )
            elif "仲裁委员会" in text:
                arbitration_candidate = _first_group(r"提交\s*([^，,。；;\n]{2,40}?仲裁委员会)\s*仲裁", text)
                arbitration_selected = _clause_selected(clause, arbitration_candidate)
                if arbitration_candidate and arbitration_selected:
                    jurisdiction_type = "arbitration"
                    arbitration_body = arbitration_candidate
                    court_specified = True
                    _set_evidence(evidence, nodes, "jurisdiction.type", jurisdiction_type, clause)
                    _set_evidence(evidence, nodes, "jurisdiction.arbitration_body", arbitration_body, clause)
                    _set_evidence(evidence, nodes, "jurisdiction.is_specified", court_specified, clause)
                elif "仲裁委员会" in text:
                    fact_evidence = _make_fact_evidence("jurisdiction.arbitration_body", None, clause, selected=False, source_type="unchecked_option")
                    nodes["jurisdiction.arbitration_body"] = FactNode(
                        value=None,
                        confidence=0.95,
                        evidence=[fact_evidence],
                        selected=False,
                        source_type="unchecked_option",
                    )

        if not force_defined and "不可抗力" in text:
            force_defined = True
            force_notice = any(term in text for term in ("通知", "告知", "证明", "书面"))
            force_settlement = any(term in text for term in ("结算", "减免", "解除", "终止", "顺延", "延期"))
            _set_evidence(evidence, nodes, "force_majeure.is_defined", force_defined, clause)
            _set_evidence(evidence, nodes, "force_majeure.notice_required", force_notice, clause)
            _set_evidence(evidence, nodes, "force_majeure.settlement_defined", force_settlement, clause)

        if property_sale.notice_required is None and any(term in text for term in ("出售", "转让", "买卖不破租赁", "优先购买权")):
            sale_notice = "通知" in text
            preemptive = "优先购买权" in text or "同等条件" in text
            property_sale = PropertySaleFacts(sale_notice, preemptive)
            _set_evidence(evidence, nodes, "property_sale.notice_required", sale_notice, clause)
            _set_evidence(evidence, nodes, "property_sale.preemptive_right", preemptive, clause)

        danger, defect, safety_obligation = _safety_fact_from_text(text)
        if safety.dangerous_house_termination is None and danger is not None:
            safety = SafetyFacts(danger, safety.defect_termination, safety.landlord_safety_obligation)
            _set_evidence(evidence, nodes, "safety.dangerous_house_termination", danger, clause)
        if safety.defect_termination is None and defect is not None:
            safety = SafetyFacts(safety.dangerous_house_termination, defect, safety.landlord_safety_obligation)
            _set_evidence(evidence, nodes, "safety.defect_termination", defect, clause)
        if safety.landlord_safety_obligation is None and safety_obligation is not None:
            safety = SafetyFacts(safety.dangerous_house_termination, safety.defect_termination, safety_obligation)
            _set_evidence(evidence, nodes, "safety.landlord_safety_obligation", safety_obligation, clause)

        if handover.inventory_exists is None and any(term in text for term in ("交接清单", "家具家电清单", "附件三", "附属设施清单", "交割单")):
            handover = HandoverFacts(True, handover.photo_required, handover.key_return_defined)
            _set_evidence(evidence, nodes, "handover.inventory_exists", True, clause)
        if handover.photo_required is None and any(term in text for term in ("照片", "视频", "拍照", "录像")):
            handover = HandoverFacts(handover.inventory_exists, True, handover.key_return_defined)
            _set_evidence(evidence, nodes, "handover.photo_required", True, clause)
        if handover.key_return_defined is None and any(term in text for term in ("钥匙", "门禁卡", "通行凭证")) and any(term in text for term in ("交还", "返还", "归还")):
            handover = HandoverFacts(handover.inventory_exists, handover.photo_required, True)
            _set_evidence(evidence, nodes, "handover.key_return_defined", True, clause)

    return HouseLeaseContractFacts(
        property=PropertyFacts(property_address, certificate_number, owner, is_owner),
        lease=LeaseTermFacts(lease_start, lease_end, lease_term),
        rent=RentFacts(rent_monthly, payment_due_day, payment_cycle, payment_method, payment_account, daily_amount),
        deposit=DepositFacts(deposit_amount, deposit_interest, deposit_condition, deposit_deadline),
        repair=RepairFacts(natural_wear, tenant_fault),
        sublease=SubleaseFacts(sublease_allowed, sublease_requires_consent),
        termination=TerminationFacts(rent_default),
        early_termination=EarlyTerminationFacts(early_exists, tenant_formula, landlord_formula, penalty_formula),
        jurisdiction=JurisdictionFacts(jurisdiction_type, court, arbitration_body if jurisdiction_type == "arbitration" else None, court_specified),
        force_majeure=ForceMajeureFacts(force_defined, force_notice, force_settlement),
        property_sale=property_sale,
        safety=safety,
        handover=handover,
        evidence=evidence,
        nodes=nodes,
    )


def extract_house_lease_facts(contract_text: str) -> HouseLeaseContractFacts:
    """Extract a shared fact graph from a house lease contract."""
    clauses = formal_evidence_clauses(parse_contract_clauses(contract_text))
    return _extract_house_lease_facts_from_clauses(clauses)
