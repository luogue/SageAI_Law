"""Quality 4.0 ownership, ontology and validation helpers.

This module is intentionally deterministic. It gives the v2 engine a stable
target architecture without replacing the mature extraction/review pipeline in
one risky rewrite.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any, Dict, Iterable, List, Optional


COVERAGE_PASS = "PASS"
COVERAGE_PARTIAL = "PARTIAL"
COVERAGE_MISSING = "MISSING"
COVERAGE_RISK_CLAUSE = "RISK_CLAUSE"
COVERAGE_NOT_APPLICABLE = "NOT_APPLICABLE"
COVERAGE_UNCERTAIN = "UNCERTAIN"

SEVERITY_LOW = "LOW"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_HIGH = "HIGH"
SEVERITY_CRITICAL = "CRITICAL"

PRIORITY_A_CORE = "A_CORE"
PRIORITY_B_PRACTICAL = "B_PRACTICAL"
PRIORITY_C_OPTIMIZATION = "C_OPTIMIZATION"
ACTION_PRIORITY_NONE = "NONE"
ACTION_PRIORITY_NOT_APPLICABLE = "NOT_APPLICABLE"

PROBABILITY_VALUES = {"RARE", "LOW", "MEDIUM", "HIGH", "VERY_HIGH", "UNKNOWN"}
IMPACT_VALUES = {"NONE", "LOW", "MEDIUM", "HIGH", "SEVERE"}

ONTOLOGY_VERSION = "risk-ontology-4.0-2026-08-11"
QUALITY4_VERSION = "contract-review-quality-4.0-target-2026-08-11"

RISK_ONTOLOGY = {
    "identity",
    "authority",
    "ownership",
    "validity",
    "payment",
    "pricing",
    "price_adjustment",
    "deposit",
    "delivery",
    "acceptance",
    "performance",
    "termination",
    "default",
    "liquidated_damages",
    "indemnity",
    "limitation_of_liability",
    "repair",
    "damage",
    "evidence",
    "assignment",
    "sublease",
    "renewal",
    "jurisdiction",
    "arbitration",
    "force_majeure",
    "safety",
    "compliance",
    "legal_reference",
    "confidentiality",
    "data",
    "privacy",
    "ip",
    "warranty",
    "service_level",
    "change_control",
}

RECOMMENDATION_TYPES = {"MODIFY", "ADD", "DELETE", "VERIFY", "NEGOTIATE", "REJECT", "ESCALATE", "OPTIONAL"}

ZH_TO_COVERAGE = {
    "通过": COVERAGE_PASS,
    "部分覆盖": COVERAGE_PARTIAL,
    "缺失": COVERAGE_MISSING,
    "风险条款": COVERAGE_RISK_CLAUSE,
    "不适用": COVERAGE_NOT_APPLICABLE,
    "不确定": COVERAGE_UNCERTAIN,
}


@dataclass(frozen=True)
class ContractContext:
    contract_type: str
    contract_value: Optional[float] = None
    duration: Optional[str] = None
    payment_frequency: Optional[str] = None
    prepaid_amount: Optional[float] = None
    deposit: Optional[float] = None
    parties: Dict[str, Any] = field(default_factory=dict)
    business_or_consumer: str = "unknown"
    bargaining_power: str = "unknown"
    user_perspective: str = "neutral"
    industry: str = "unknown"
    jurisdiction: str = "CN"
    special_assets: List[str] = field(default_factory=list)
    special_facts: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LegalAuthority:
    authority_id: str
    jurisdiction: str
    law_name: str
    article: str
    paragraph: str
    text: str
    authority_level: str
    effective_from: str
    effective_to: Optional[str]
    status: str
    replacement: Optional[str]
    source: str
    last_verified_at: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CitationClaim:
    claim_id: str
    finding_id: str
    review_id: str
    proposition: str
    claim_type: str
    authority_id: str
    law_name: str
    article: str
    paragraph: str
    support_type: str
    support_scope: str
    authority_links: List[Dict[str, Any]]
    confidence: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


LEGAL_AUTHORITY_KB: Dict[tuple[str, str], LegalAuthority] = {
    ("中华人民共和国民法典", "第732条"): LegalAuthority(
        authority_id="CN-CIVIL-CODE-732",
        jurisdiction="CN",
        law_name="中华人民共和国民法典",
        article="第732条",
        paragraph="",
        text="承租人在房屋租赁期限内死亡的，与其生前共同居住的人或者共同经营人可以按照原租赁合同租赁该房屋。",
        authority_level="法律",
        effective_from="2021-01-01",
        effective_to=None,
        status="CURRENT",
        replacement=None,
        source="legal_authority_kb_minimal",
        last_verified_at="2026-08-11",
    ),
    ("中华人民共和国民法典", "第585条"): LegalAuthority(
        authority_id="CN-CIVIL-CODE-585",
        jurisdiction="CN",
        law_name="中华人民共和国民法典",
        article="第585条",
        paragraph="",
        text="约定的违约金低于或者过分高于造成的损失时，可以依法请求调整。",
        authority_level="法律",
        effective_from="2021-01-01",
        effective_to=None,
        status="CURRENT",
        replacement=None,
        source="legal_authority_kb_minimal",
        last_verified_at="2026-08-11",
    ),
    ("中华人民共和国民法典", "第725条"): LegalAuthority(
        authority_id="CN-CIVIL-CODE-725",
        jurisdiction="CN",
        law_name="中华人民共和国民法典",
        article="第725条",
        paragraph="",
        text="租赁物在承租人按照租赁合同占有期限内发生所有权变动的，不影响租赁合同的效力。",
        authority_level="法律",
        effective_from="2021-01-01",
        effective_to=None,
        status="CURRENT",
        replacement=None,
        source="legal_authority_kb_minimal",
        last_verified_at="2026-08-11",
    ),
    ("中华人民共和国民法典", "第734条"): LegalAuthority(
        authority_id="CN-CIVIL-CODE-734",
        jurisdiction="CN",
        law_name="中华人民共和国民法典",
        article="第734条",
        paragraph="",
        text="租赁期限届满后继续使用租赁物且出租人没有异议的，原租赁合同继续有效但转为不定期租赁。",
        authority_level="法律",
        effective_from="2021-01-01",
        effective_to=None,
        status="CURRENT",
        replacement=None,
        source="legal_authority_kb_minimal",
        last_verified_at="2026-08-11",
    ),
    ("中华人民共和国民法典", "第730条"): LegalAuthority(
        authority_id="CN-CIVIL-CODE-730",
        jurisdiction="CN",
        law_name="中华人民共和国民法典",
        article="第730条",
        paragraph="",
        text="当事人对租赁期限没有约定或者约定不明确，依法仍不能确定的，视为不定期租赁；当事人可以随时解除合同，但是应当在合理期限之前通知对方。",
        authority_level="法律",
        effective_from="2021-01-01",
        effective_to=None,
        status="CURRENT",
        replacement=None,
        source="legal_authority_kb_minimal",
        last_verified_at="2026-08-11",
    ),
    ("中华人民共和国合同法", ""): LegalAuthority(
        authority_id="CN-CONTRACT-LAW-REPEALED",
        jurisdiction="CN",
        law_name="中华人民共和国合同法",
        article="",
        paragraph="",
        text="《中华人民共和国合同法》已由《中华人民共和国民法典》吸收整合。",
        authority_level="法律",
        effective_from="1999-10-01",
        effective_to="2020-12-31",
        status="REPEALED",
        replacement="中华人民共和国民法典",
        source="legal_authority_kb_minimal",
        last_verified_at="2026-08-11",
    ),
}


def normalize_law_name(law_name: str) -> str:
    name = (law_name or "").strip().replace("《", "").replace("》", "")
    aliases = {
        "民法典": "中华人民共和国民法典",
        "中国民法典": "中华人民共和国民法典",
        "中华人民共和国合同法": "中华人民共和国合同法",
        "合同法": "中华人民共和国合同法",
    }
    return aliases.get(name, name)


DEFAULT_LAW_RULES = {
    "owner_change_no_break_lease": "CLEAR_DEFAULT",
    "normal_wear": "CLEAR_DEFAULT",
    "tenant_death_successor": "CLEAR_DEFAULT",
    "lessor_death": "CLEAR_DEFAULT",
    "indefinite_lease": "CLEAR_DEFAULT",
    "deposit_return_timing": "PARTIAL_DEFAULT",
    "deposit_offset_order": "PARTIAL_DEFAULT",
    "property_damage_deposit_evidence": "PARTIAL_DEFAULT",
}


def normalize_coverage(status: str) -> str:
    return ZH_TO_COVERAGE.get(status or "", COVERAGE_UNCERTAIN)


def default_law_status(risk_group: str, node_id: str = "") -> str:
    return DEFAULT_LAW_RULES.get(risk_group) or DEFAULT_LAW_RULES.get(node_id) or "UNCERTAIN_DEFAULT"


def ontology_category(risk_group: str, node_id: str = "") -> str:
    value = f"{risk_group} {node_id}"
    if "early_termination" in value or "解除" in value:
        return "termination"
    if "deposit" in value or "押金" in value:
        return "deposit"
    if "damage" in value or "defect" in value or "handover" in value:
        return "damage"
    if "payment" in value or "rent" in value:
        return "payment"
    if "jurisdiction" in value:
        return "jurisdiction"
    if "legal_reference" in value or "outdated" in value:
        return "legal_reference"
    if "safety" in value:
        return "safety"
    return "performance"


def aggregation_key(review: Any) -> str:
    """Create semantic aggregation signal independent of a single review id."""

    risk_group = getattr(review, "risk_group", "") or getattr(review, "node_id", "") or getattr(review, "item_id", "")
    category = ontology_category(risk_group, getattr(review, "node_id", ""))
    facts = tuple(sorted(getattr(review, "fact_dependencies", []) or []))
    clause_ids = tuple(
        sorted(
            str(clause.get("clause_id"))
            for clause in (getattr(review, "evidence_clauses", []) or [])
            if clause.get("clause_id")
        )
    )
    consequence = getattr(review, "legal_consequence_if_missing", "") or ""
    economic = getattr(review, "economic_impact", "") or ""
    if risk_group:
        return f"{category}|{risk_group}|facts={','.join(facts)}|clauses={','.join(clause_ids)}|econ={economic}"
    return f"{category}|{','.join(facts)}|{','.join(clause_ids)}|{consequence[:30]}"


def build_contract_context(contract_type: str, facts: Optional[Dict[str, Any]], profile: Optional[Any] = None) -> ContractContext:
    facts = facts or {}
    rent = facts.get("rent") or {}
    deposit = facts.get("deposit") or {}
    payment_frequency = rent.get("payment_cycle")
    perspective = "neutral"
    bargaining = "unknown"
    if profile is not None:
        identity = getattr(profile, "user_identity", "")
        if "承租" in identity:
            perspective = "tenant"
        elif "出租" in identity:
            perspective = "landlord"
        elif "买" in identity:
            perspective = "buyer"
        elif "卖" in identity or "出卖" in identity:
            perspective = "seller"
        bargaining = getattr(profile, "bargaining_position", "") or "unknown"
    return ContractContext(
        contract_type=contract_type,
        duration=(facts.get("lease_term") or {}).get("text"),
        payment_frequency=payment_frequency,
        deposit=_safe_amount(deposit.get("amount")),
        parties={k: v for k, v in (facts.get("parties") or {}).items() if v},
        bargaining_power=bargaining,
        user_perspective=perspective,
    )


def _safe_amount(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(str(value).replace("元", "").replace(",", "").replace("，", ""))
    except ValueError:
        return None


def validate_legal_citation(law_name: str, article: str = "", *, as_of: Optional[str] = None) -> Dict[str, Any]:
    normalized_law_name = normalize_law_name(law_name)
    key = (normalized_law_name or "", article or "")
    authority = LEGAL_AUTHORITY_KB.get(key) or LEGAL_AUTHORITY_KB.get((normalized_law_name or "", ""))
    if not authority:
        return {
            "status": "UNCERTAIN",
            "entailment": "PARTIAL",
            "law_name": normalized_law_name or law_name,
            "article": article,
            "message": "没有找到足够直接的具体条文。",
        }
    status = authority.status
    if as_of and authority.effective_to and as_of > authority.effective_to:
        status = "OUTDATED_REFERENCE"
    return {
        "status": status if status != "REPEALED" else "OUTDATED_REFERENCE",
        "entailment": "SUPPORTS" if status == "CURRENT" else "PARTIAL",
        "support_type": "DIRECT_SUPPORT" if status == "CURRENT" else "PARTIAL_SUPPORT",
        "authority": authority.to_public_dict(),
    }


def validate_citation_entailment(
    *,
    proposition: str,
    law_name: str,
    article: str = "",
    paragraph: str = "",
    claim_id: str = "",
    finding_id: str = "",
    review_id: str = "",
    claim_type: str = "STATUTORY_RULE",
) -> Dict[str, Any]:
    validation = validate_legal_citation(law_name, article)
    authority = validation.get("authority") or {}
    law_name = authority.get("law_name") or validation.get("law_name") or law_name
    status = validation.get("status", "UNCERTAIN")
    support_type = validation.get("support_type", "UNCERTAIN")
    confidence = "medium"
    prop = proposition or ""

    if status == "OUTDATED_REFERENCE":
        support_type = "BACKGROUND_ONLY"
        confidence = "medium"
    elif article == "第188条" and any(term in prop for term in ("通知", "送达", "催告", "留痕")):
        support_type = "BACKGROUND_ONLY"
        confidence = "high"
    elif article == "第565条" and any(term in prop for term in ("解除通知", "通知到达", "解除")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第585条" and any(term in prop for term in ("违约金", "损失", "调减", "调整")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第734条" and any(term in prop for term in ("期满", "继续使用", "继续居住", "继续收租", "不定期租赁")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第734条":
        support_type = "PARTIAL_SUPPORT"
        confidence = "medium"
    elif article == "第730条" and any(term in prop for term in ("不定期", "合理期限", "通知", "解除")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第732条" and any(term in prop for term in ("承租人", "死亡", "共同居住", "共同经营", "继续承租", "原租赁合同")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第732条":
        support_type = "PARTIAL_SUPPORT"
        confidence = "medium"
    elif article == "第725条" and any(term in prop for term in ("所有权", "权利", "受让", "继承", "不影响", "继续履行")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第725条":
        support_type = "PARTIAL_SUPPORT"
        confidence = "medium"
    elif not article:
        support_type = "UNCERTAIN"
        confidence = "low"

    support_scope = authority.get("text", "") if support_type in {"DIRECT_SUPPORT", "PARTIAL_SUPPORT"} else ""
    authority_link = {
        "authority_id": authority.get("authority_id", ""),
        "law_name": law_name,
        "article": article,
        "paragraph": paragraph,
        "freshness_status": status,
        "entailment_status": support_type,
        "support_scope": support_scope,
        "confidence": confidence,
    } if law_name or article else {}
    claim = CitationClaim(
        claim_id=claim_id,
        finding_id=finding_id,
        review_id=review_id,
        proposition=proposition,
        claim_type=claim_type,
        authority_id=authority.get("authority_id", ""),
        law_name=law_name,
        article=article,
        paragraph=paragraph,
        support_type=support_type,
        support_scope=support_scope,
        authority_links=[authority_link] if authority_link else [],
        confidence=confidence,
    )
    return {
        **validation,
        "support_type": support_type,
        "confidence": confidence,
        "claim": claim.to_public_dict(),
    }


def validate_formula_ast(formula: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not formula:
        return {"status": "NOT_APPLICABLE", "failures": []}
    failures: List[Dict[str, str]] = []
    formula_type = formula.get("type")
    allowed = {
        "fixed_amount",
        "monthly_payment_multiplier",
        "monthly_rent_multiplier",
        "daily_payment_multiplier",
        "daily_rent_multiplier",
        "remaining_term_multiplier",
        "remaining_term_rent_multiplier",
        "contract_value_percentage",
        "unpaid_amount_percentage",
        "daily_percentage",
        "tiered_formula",
        "capped_formula",
        "capped_amount",
        "minimum_formula",
        "maximum_formula",
        "min_max_formula",
        "compound_formula",
        "rent_multiplier",
    }
    if formula_type not in allowed:
        failures.append({"failure_stage": "Formula Validation", "root_cause": f"未知公式类型：{formula_type}"})
    if formula_type and "percentage" in formula_type and formula.get("rate") is None:
        failures.append({"failure_stage": "Numerical Unit Validation", "root_cause": "百分比公式缺少 rate。"})
    if formula_type and "multiplier" in formula_type and formula.get("multiplier") is None:
        failures.append({"failure_stage": "Numerical Unit Validation", "root_cause": "倍数公式缺少 multiplier。"})
    if formula.get("direction") == "unspecified":
        failures.append({"failure_stage": "Formula Validation", "root_cause": "责任方向无法确定。"})
    return {"status": "PASS" if not failures else "BLOCK", "failures": failures}


def calculation_provenance(formula: Optional[Dict[str, Any]], scenarios: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not formula:
        return {"status": "NOT_APPLICABLE"}
    cases = (scenarios or {}).get("cases") or []
    return {
        "status": "PASS",
        "formula": formula,
        "inputs": (scenarios or {}).get("inputs", {}),
        "units": {
            "currency": "CNY",
            "duration": "days" if any("remaining_days" in case for case in cases) else "unknown",
            "base": formula.get("base"),
        },
        "intermediate_steps": [
            {
                "case": case.get("label") or case.get("name"),
                "remaining_days": case.get("remaining_days"),
                "output": case.get("penalty") or case.get("amount"),
                "estimated": case.get("estimated", False),
            }
            for case in cases
        ],
        "estimated": any(case.get("estimated") for case in cases),
        "confidence": "high",
    }


def public_review_result(review: Any) -> Dict[str, Any]:
    return {
        "review_id": getattr(review, "item_id", ""),
        "applicable": normalize_coverage(getattr(review, "coverage_status", "")) != COVERAGE_NOT_APPLICABLE,
        "coverage_status": normalize_coverage(getattr(review, "coverage_status", "")),
        "priority": getattr(review, "action_priority", "") or getattr(review, "review_priority", ""),
        "review_importance": getattr(review, "review_importance", ""),
        "action_priority": getattr(review, "action_priority", "") or getattr(review, "review_priority", ""),
        "facts": list(getattr(review, "fact_dependencies", []) or []),
        "evidence": list(getattr(review, "evidence_clauses", []) or []),
        "legal_basis": list(getattr(review, "legal_references", []) or []),
        "conclusion": getattr(review, "reasoning_summary", ""),
        "related_finding_ids": list(getattr(review, "related_risks", []) or []),
        "confidence": dict(getattr(review, "system_confidence", {}) or {}),
        "needs_manual_review": bool(getattr(review, "needs_manual_review", False)),
    }


def post_render_quality_gate(
    report: str,
    review_results: Iterable[Dict[str, Any]],
    findings: Iterable[Dict[str, Any]],
    recommendations: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    failures: List[Dict[str, str]] = []
    finding_ids = {finding.get("finding_id") for finding in findings}
    forbidden = [
        "RF-",
        "REC-",
        "LLM_PRIORITY",
        "Legacy",
        "Fact Graph",
        "semantic entailment",
        "Semantic Entailment",
        "rule fallback",
        "rule_fallback",
        "建议继续核对表述是否具体、附件是否完整、责任边界是否清楚",
        "建议重点完善",
        "对你而言建议修改",
        "风险评级为",
        "行动建议",
        "用户风险偏好已纳入",
        "统一事实图谱",
        "Scenario Engine",
        "DIRECT_SUPPORT",
        "PARTIAL_SUPPORT",
        "BACKGROUND_ONLY",
        "NOT_SUPPORT",
        "CONTRADICTS",
        "early_termination.",
        "rule fallback",
        "fallback",
        "special correction",
    ]
    leaked = [term for term in forbidden if term in (report or "")]
    if leaked:
        failures.append(
            {
                "requirement": "Report Post-render Internal Term Gate",
                "failure_stage": "Report Consistency",
                "root_cause": f"正式报告存在内部术语或PASS模板噪音：{', '.join(leaked)}。",
                "fix_owner": "Report Serializer",
            }
        )
    wording_forbidden = ["【法律依据】：法律依据：", "【法律依据】：依据："]
    wording_leaks = [term for term in wording_forbidden if term in (report or "")]
    if wording_leaks:
        failures.append(
            {
                "requirement": "Production Legal Basis Wording",
                "failure_stage": "Post-render Validation",
                "root_cause": f"正式报告法律依据字段存在重复前缀：{', '.join(wording_leaks)}。",
                "fix_owner": "Report Serializer",
            }
        )
    required_sections = ["合同总体评价", "核心风险摘要", "建议优先修改", "可选优化事项", "已覆盖关键事项", "完整审查明细"]
    missing_sections = [section for section in required_sections if section not in (report or "")]
    if missing_sections:
        failures.append(
            {
                "requirement": "Production Report Required Sections",
                "failure_stage": "Post-render Validation",
                "root_cause": f"正式报告缺少必要栏目：{', '.join(missing_sections)}。",
                "fix_owner": "Report Serializer",
            }
        )
    legal_reference_findings = [
        finding for finding in findings
        if finding.get("risk_group") in {"legal_reference", "outdated_legal_reference"}
    ]
    if not legal_reference_findings and "合同法" in (report or ""):
        failures.append(
            {
                "requirement": "Legal Freshness Finding",
                "failure_stage": "Legal Freshness Validation",
                "root_cause": "报告出现合同法引用但没有形成过时法律引用风险发现。",
                "fix_owner": "Legal Freshness Checker",
            }
        )
    top_lines = []
    in_top = False
    for line in (report or "").splitlines():
        if "核心风险摘要" in line:
            in_top = True
            continue
        if in_top and line.startswith("## "):
            break
        if in_top and line.startswith("- **"):
            top_lines.append(line)
    top_titles = [line.split("**", 2)[1] for line in top_lines if "**" in line]
    if len(top_titles) != len(set(top_titles)):
        failures.append(
            {
                "requirement": "Top Risk duplicate",
                "failure_stage": "Post-render Validation",
                "root_cause": "核心风险摘要存在重复风险标题。",
                "fix_owner": "Risk Aggregator",
            }
        )
    for review in review_results:
        if review.get("coverage_status") == COVERAGE_NOT_APPLICABLE and review.get("related_finding_ids"):
            failures.append(
                {
                    "requirement": "N/A no finding",
                    "failure_stage": "Risk Aggregation Validation",
                    "root_cause": f"{review.get('review_id')} 为不适用但仍关联风险发现。",
                    "fix_owner": "Risk Aggregator",
                }
            )
        unknown = set(review.get("related_finding_ids") or []) - finding_ids
        if unknown:
            failures.append(
                {
                    "requirement": "Finding Traceability",
                    "failure_stage": "Report Consistency",
                    "root_cause": f"{review.get('review_id')} 关联不存在的风险发现。",
                    "fix_owner": "Risk Aggregator",
                }
            )
    for rec in recommendations:
        if rec.get("type") not in RECOMMENDATION_TYPES:
            failures.append(
                {
                    "requirement": "Recommendation Type",
                    "failure_stage": "Recommendation Validation",
                    "root_cause": f"未知建议类型：{rec.get('type')}",
                    "fix_owner": "Recommendation Aggregator",
                }
            )
    return {"status": "REPORT_READY" if not failures else "BLOCKED", "failures": failures}
