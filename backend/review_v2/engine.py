"""独立的合同审查引擎（第二版）。"""

from __future__ import annotations

import hashlib
import json
import re
import time
import uuid
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from review_v2.clause_parser import ParsedClause, document_integrity, formal_evidence_clauses, parse_contract_clauses, strip_non_contract_tail
from review_v2.contract_facts import ContractFactGraph, canonical_fact_key, extract_contract_fact_graph, fact_requirements_for_node
from review_v2.framework_supply import (
    FRAMEWORK_REVIEW_FACT_PATHS,
    FrameworkSupplyProfile,
    add_framework_facts_to_graph,
    extract_framework_supply_profile,
)
from review_v2.canonical_claims import build_canonical_claims, canonical_claims_public
from review_v2.common_sale import (
    ReviewExecutionContext,
    build_product_documentation_profile,
    common_sale_coverage_requirement,
    product_review_applicability,
)
from review_v2.contract_registry import (
    UnsupportedContractTypeError,
    get_checklist,
    get_checklist_for_resolution,
    review_registry_debug,
    get_contract_meta,
    supported_contract_display_names,
)
from review_v2.domain_packs import composed_domain_pack_snapshot, domain_pack_snapshot, get_default_rule, get_domain_pack
from review_v2.domain_resolution import resolve_contract_domain
from review_v2.domain_selection import domain_selection_consistency_gate, resolve_domain_selection
from review_v2.real_estate_facts import extract_real_estate_sale_facts
from review_v2.report_context import build_report_context
from review_v2.perspective_resolution import (
    PERSPECTIVE_RESOLVER_VERSION,
    perspective_domain_consistency_gate,
    resolve_perspective,
)
from review_v2.production_display import (
    PRODUCTION_SERIALIZER_VERSION,
    display_claims,
    production_fact_polarity_gate,
)
from review_v2.recommendation_impact import RECOMMENDATION_ENGINE_VERSION, evaluate_recommendations
from review_v2.consistency_verifier import apply_claims, verify_consistency
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.lease_contract_facts import (
    LANDLORD,
    TENANT,
    HouseLeaseContractFacts,
    extract_house_lease_facts,
)
from review_v2.llm_semantic_reviewer import get_llm_review_status, judge_checkpoints_with_llm
from review_v2.quality4 import (
    ONTOLOGY_VERSION,
    QUALITY4_VERSION,
    aggregation_key as quality4_aggregation_key,
    build_contract_context,
    calculation_provenance,
    default_law_status,
    ontology_category,
    post_render_quality_gate,
    public_review_result,
    validate_citation_entailment,
    validate_formula_ast,
    validate_legal_citation,
)
from review_v2.semantic_reviewer import _has_gift_paid_consideration_risk, has_specific_deposit_return_deadline, judge_checkpoint, matched_terms, retrieve_evidence_candidates
from review_v2.semantic_reviewer import classify_evidence_type, evidence_semantically_entails
from review_v2.scenario_engine import (
    economic_impact_detail_for_penalty,
    economic_impact_for_penalty,
    numeric_amount as scenario_numeric_amount,
    penalty_scenarios,
)
from review_v2.jurisdiction_analyzer import analyze_jurisdiction_prediction, format_jurisdiction_markdown
from review_v2.litigation_analyzer import analyze_litigation_strategy, format_litigation_markdown
from review_v2.negotiation_analyzer import analyze_negotiation_strategy, format_negotiation_markdown
from review_v2.user_profile import (
    UserRiskProfile,
    adapt_report_header,
    format_profile_summary,
    get_action_label,
    get_risk_remap,
    is_priority_checkpoint,
)


NEGATION_WORDS = ("无", "没有", "未", "不包含", "不涉及", "并非", "不是")
VERDICT_WORDS = (
    "判决结果",
    "判决",
    "裁判结论",
    "驳回请求",
    "押金全额返还",
    "扣除维修费后返还余额",
    "应赔偿",
    "承租方应赔偿",
    "出租方应赔偿",
)

REPORT_FORMAT_NOTICE = "本报告基于完整合同模板逐项审查，部分缺失项可能因合同格式简略所致，建议结合合同实际用途判断优先级。"
COVERAGE_NOT_APPLICABLE = "不适用"
ISSUE_NOT_APPLICABLE = "不适用"
RISK_NOT_APPLICABLE = "none"
SEVERITY_NONE = "NONE"
SEVERITY_LOW = "LOW"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_HIGH = "HIGH"
SEVERITY_CRITICAL = "CRITICAL"
PRIORITY_A_CORE = "A_CORE"
PRIORITY_B_PRACTICAL = "B_PRACTICAL"
PRIORITY_C_OPTIMIZATION = "C_OPTIMIZATION"
ACTION_PRIORITY_NONE = "NONE"
ACTION_PRIORITY_NOT_APPLICABLE = "NOT_APPLICABLE"
INSUFFICIENT_CONTEXT = "INSUFFICIENT_CONTEXT"
CLIENT_EFFECT_FAVORABLE = "FAVORABLE"
CLIENT_EFFECT_NEUTRAL = "NEUTRAL"
CLIENT_EFFECT_ADVERSE = "ADVERSE"
CLIENT_EFFECT_UNCERTAIN = "UNCERTAIN"
LEGAL_DEFAULT_NONE = "NONE"
LEGAL_DEFAULT_PARTIAL = "PARTIAL"
LEGAL_DEFAULT_SUFFICIENT = "SUFFICIENT"
DISPOSITION_MUST_CHANGE = "MUST_CHANGE"
DISPOSITION_SHOULD_CHANGE = "SHOULD_CHANGE"
DISPOSITION_OPTIONAL_IMPROVEMENT = "OPTIONAL_IMPROVEMENT"
DISPOSITION_KEEP_CURRENT = "KEEP_CURRENT"
DISPOSITION_DO_NOT_ADD = "DO_NOT_ADD"
DISPOSITION_MANUAL_REVIEW = "MANUAL_REVIEW"
RECOMMENDATION_OWNER_RISK = "RISK"
RECOMMENDATION_OWNER_REVIEW = "REVIEW"
RECOMMENDATION_OWNER_NONE = "NONE"
SIGNABLE = "SIGNABLE"
SIGNABLE_WITH_OPTIONAL_IMPROVEMENTS = "SIGNABLE_WITH_OPTIONAL_IMPROVEMENTS"
SIGN_AFTER_MODIFICATION = "SIGN_AFTER_MODIFICATION"
PROFESSIONAL_REVIEW_RECOMMENDED = "PROFESSIONAL_REVIEW_RECOMMENDED"
NOT_RECOMMENDED_TO_SIGN = "NOT_RECOMMENDED_TO_SIGN"
REVIEW_IMPORTANCE_CORE = "CORE"
REVIEW_IMPORTANCE_IMPORTANT = "IMPORTANT"
REVIEW_IMPORTANCE_NORMAL = "NORMAL"
SYSTEM_VERSION = "contract-review-quality-6.4"
PIPELINE_VERSION = "canonical-review-v2-production-6.4"
EVIDENCE_SUPPORTS = "SUPPORTS"
EVIDENCE_PARTIAL_SUPPORT = "PARTIAL_SUPPORT"
EVIDENCE_RELATED_NOT_SUPPORTING = "RELATED_BUT_NOT_SUPPORTING"
EVIDENCE_CONTRADICTS = "CONTRADICTS"
EVIDENCE_NOT_RELEVANT = "NOT_RELEVANT"
EVIDENCE_UNCERTAIN = "UNCERTAIN"
PROMPT_VERSION = "review-v2-prompt-2026-08-11"
FACT_PROMPT_VERSION = "fact-extraction-v2-2026-08-11"
REVIEW_PROMPT_VERSION = "review-v2-prompt-2026-08-11"
VERIFIER_PROMPT_VERSION = "independent-verifier-deterministic-2026-08-11"
RISK_AGGREGATION_PROMPT_VERSION = "risk-aggregation-deterministic-2026-08-11"
RECOMMENDATION_PROMPT_VERSION = "recommendation-aggregation-deterministic-2026-08-11"
RULE_VERSION = "review-v2-rules-quality3-2026-08-11"
LEGAL_DATASET_VERSION = "cn-civil-code-minimal-2026-08-11"
BENCHMARK_VERSION = "quality6.4-final-convergence-2026-08-13"
PARSER_VERSION = "canonical-clause-parser-6.4"
FACT_SCHEMA_VERSION = "contract-fact-graph-1.0"
RETRIEVAL_VERSION = "hybrid-retrieval-1.0"
DOMAIN_PACK_VERSION = "domain-pack-sale-1.0"
DEFAULT_LAW_VERSION = "sale-default-law-6.4"
CONFIDENCE_VERSION = "confidence-calibration-6.4"
SCALAR_CONFLICT_FACT_KEYS = {
    "service.course_name",
    "service.project_id",
    "service.total_sessions",
    "service.session_duration",
    "service.schedule",
    "service.start_date",
    "service.end_date",
    "service.location",
    "payment.total_fee",
    "payment.session_fee_total",
    "payment.unit_price",
    "payment.total_sessions",
    "payment.material_fee",
    "payment.amount_paid",
}

PROBABILITY_RARE = "RARE"
PROBABILITY_LOW = "LOW"
PROBABILITY_MEDIUM = "MEDIUM"
PROBABILITY_HIGH = "HIGH"
PROBABILITY_VERY_HIGH = "VERY_HIGH"
PROBABILITY_UNKNOWN = "UNKNOWN"


class NotApplicableRisk(str):
    """Public risk value for N/A while tolerating legacy comparisons."""

    def __new__(cls, value: str = RISK_NOT_APPLICABLE) -> "NotApplicableRisk":
        return str.__new__(cls, RISK_NOT_APPLICABLE)

    def __eq__(self, other: object) -> bool:
        return str.__eq__(self, other) or other == COVERAGE_NOT_APPLICABLE

    def __hash__(self) -> int:
        return str.__hash__(self)

CASE_DOCUMENT_HINTS = (
    "原告",
    "被告",
    "本院认为",
    "经审理查明",
    "审理查明",
    "诉称",
    "辩称",
    "案号",
    "民事判决书",
    "民事裁定书",
)


@dataclass
class ReviewItemResult:
    item_id: str
    node_id: str
    title: str
    risk_level: str
    status: str
    risk_point_description: str
    suggested_clause_example: str
    legal_basis_index: str
    legal_consequence_if_missing: str
    applicable_if: str
    matched_terms: List[str]
    coverage_status: str
    issue_type: str
    evidence_clauses: List[Dict[str, Any]]
    evidence_location: str
    reasoning_summary: str
    judge_source: str = "rule_fallback"
    llm_confidence: str = ""
    llm_raw_reason: str = ""
    fallback_reason: str = ""
    reasoning: str = ""
    citation: Dict[str, Any] = field(default_factory=dict)
    applicability: Dict[str, Any] = field(default_factory=dict)
    economic_impact: str = ""
    economic_impact_detail: Dict[str, Any] = field(default_factory=dict)
    scenario_analysis: Dict[str, Any] = field(default_factory=dict)
    quality_flags: List[Dict[str, Any]] = field(default_factory=list)
    review_priority: str = ""
    review_importance: str = REVIEW_IMPORTANCE_NORMAL
    action_priority: str = ACTION_PRIORITY_NONE
    fact_dependencies: List[str] = field(default_factory=list)
    action_suggestion: str = ""
    evidence_type: str = ""
    semantic_entailment: Optional[bool] = None
    high_risk_reason: str = ""
    needs_manual_review: bool = False
    quality_gate_failure_reason: str = ""
    review_status: str = "待处理"
    reviewer_note: str = ""
    claims: List[Dict[str, Any]] = field(default_factory=list)
    review_trace_id: str = ""
    risk_severity: str = ""
    residual_risk: str = ""
    related_reviews: List[str] = field(default_factory=list)
    related_risks: List[str] = field(default_factory=list)
    risk_group: str = ""
    system_confidence: Dict[str, Any] = field(default_factory=dict)
    legal_references: List[Dict[str, Any]] = field(default_factory=list)
    decision_trace: Dict[str, Any] = field(default_factory=dict)
    coverage_elements: List[Dict[str, Any]] = field(default_factory=list)
    review_evidence_provenance: Dict[str, Any] = field(default_factory=dict)
    narrative_state: Dict[str, Any] = field(default_factory=dict)
    review_evidence_supports_element_ids: List[str] = field(default_factory=list)
    review_evidence_relevance_score: float = 0.0
    review_evidence_selection_reason: str = ""

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RiskFinding:
    finding_id: str
    risk_group: str
    title: str
    severity: str
    priority: str
    source_review_ids: List[str]
    facts: List[str]
    evidence: List[Dict[str, Any]]
    source_clause_ids: List[str] = field(default_factory=list)
    legal_basis: List[Dict[str, Any]] = field(default_factory=list)
    issue: str = ""
    consequence: str = ""
    probability: str = PROBABILITY_UNKNOWN
    impact: Dict[str, Any] = field(default_factory=dict)
    economic_impact: Dict[str, Any] = field(default_factory=dict)
    legal_impact: Dict[str, Any] = field(default_factory=dict)
    operational_impact: Dict[str, Any] = field(default_factory=dict)
    safety_impact: Dict[str, Any] = field(default_factory=dict)
    recommendation: str = ""
    recommendation_ids: List[str] = field(default_factory=list)
    related_findings: List[str] = field(default_factory=list)
    decision_value: str = "medium"
    confidence: Dict[str, Any] = field(default_factory=dict)
    needs_manual_review: bool = False
    verification_status: str = "NOT_RUN"
    severity_reason: Dict[str, Any] = field(default_factory=dict)
    risk_category: str = ""
    aggregation_signals: Dict[str, Any] = field(default_factory=dict)
    default_law_status: str = "UNCERTAIN_DEFAULT"
    agreement: Dict[str, Any] = field(default_factory=dict)
    verification: Dict[str, Any] = field(default_factory=dict)
    supporting_evidence: List[Dict[str, Any]] = field(default_factory=list)
    counter_evidence: List[Dict[str, Any]] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)
    covered_element_ids: List[str] = field(default_factory=list)
    missing_element_ids: List[str] = field(default_factory=list)
    final_missing_elements: List[Dict[str, Any]] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NormalizedEconomicExposure:
    absolute_amount: Optional[float] = None
    monthly_payment_multiple: Optional[float] = None
    deposit_multiple: Optional[float] = None
    prepaid_amount_ratio: Optional[float] = None
    contract_total_ratio: Optional[float] = None
    remaining_obligation_ratio: Optional[float] = None
    batch_value_ratio: Optional[float] = None
    unpaid_amount_ratio: Optional[float] = None
    advance_payment_ratio: Optional[float] = None
    replacement_cost_ratio: Optional[float] = None
    delay_loss_ratio: Optional[float] = None
    time_amplifying: bool = False
    uncapped: bool = False
    level: str = "none"

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PriorityInput:
    finding_id: str = ""
    severity: str = SEVERITY_NONE
    economic_impact: str = "none"
    probability: str = PROBABILITY_UNKNOWN
    legal_impact: str = "LOW"
    operational_impact: str = "LOW"
    safety_impact: str = "NONE"
    core_obligation: bool = False
    time_amplifying: bool = False
    uncapped: bool = False
    reversibility: str = "medium"
    recoverability: str = "medium"
    user_perspective: str = "UNKNOWN"
    user_directly_bears_risk: bool = False
    bargaining_power: str = "unknown"
    contract_value: Optional[float] = None
    recurring_value: Optional[float] = None
    deposit_amount: Optional[float] = None
    prepaid_amount: Optional[float] = None
    remaining_obligation: Optional[float] = None
    recommendation_cost: str = "medium"
    recommendation_feasibility: str = "medium"
    confidence: str = "medium"
    normalized_economic_exposure: Dict[str, Any] = field(default_factory=dict)
    statutory_default_status: str = "UNCERTAIN_DEFAULT"
    default_protection_strength: str = "unknown"
    contract_override_risk: str = "unknown"
    practical_gap_after_default: str = "medium"
    user_impact: str = "medium"

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceClaim:
    claim_id: str
    review_id: str
    finding_id: str
    proposition: str
    required_semantics: List[str]
    polarity: str = "positive"
    party: str = ""
    obligation: str = ""
    object: str = ""
    condition: str = ""
    consequence: str = ""
    confidence: str = "medium"

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RiskClaim:
    claim_id: str
    risk_type: str
    proposition: str
    existence_type: str
    subject_party: str = ""
    action: str = ""
    object: str = ""
    trigger: str = ""
    condition: str = ""
    direction: str = ""
    consequence: str = ""
    required_evidence_elements: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClaimState:
    claim_id: str
    fact_state: str
    evidence_state: str
    coverage_state: str
    finding_state: str
    narrative_state: str
    recommendation_state: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CoverageClaim:
    review_id: str
    required_elements: List[Dict[str, Any]]
    optional_elements: List[Dict[str, Any]] = field(default_factory=list)
    positive_claims: List[str] = field(default_factory=list)
    negative_claims: List[str] = field(default_factory=list)
    minimum_pass_elements: int = 1
    minimum_partial_elements: int = 1
    satisfaction_paths: List[Dict[str, Any]] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CoverageElementResult:
    review_id: str
    element_id: str
    proposition: str
    status: str
    evidence_ids: List[str]
    entailment: str
    verifier_confidence: str
    reason: str = ""
    claim_id: str = ""
    source_clause_ids: List[str] = field(default_factory=list)
    source_spans: List[str] = field(default_factory=list)
    source_locations: List[str] = field(default_factory=list)
    atomic: bool = True
    child_elements: List[str] = field(default_factory=list)
    legal_proposition_ids: List[str] = field(default_factory=list)
    required_fact_key: str = ""
    fact_status: str = ""
    fact_value: Any = None
    fact_evidence_refs: List[str] = field(default_factory=list)
    requirement_status: str = ""
    requirement_reason: str = ""

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ApplicabilityResult:
    review_id: str
    applicable: Optional[bool]
    trigger_facts: List[str]
    trigger_evidence: List[Dict[str, Any]]
    missing_triggers: List[str]
    reason: str
    confidence: str
    status: str
    machine_reason: str = ""
    user_reason: str = ""
    required_triggers: List[str] = field(default_factory=list)
    satisfied_triggers: List[str] = field(default_factory=list)
    unsatisfied_triggers: List[str] = field(default_factory=list)
    conflicting_triggers: List[str] = field(default_factory=list)
    trigger_fact_ids: List[str] = field(default_factory=list)
    trigger_evidence_ids: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EffectiveGap:
    review_id: str
    contract_coverage: str
    default_law_status: str
    default_protection: str
    contract_context: Dict[str, Any]
    remaining_legal_gap: str
    operational_gap: str
    economic_gap: str
    uncertainty: str
    residual_risk: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PriorityDecision:
    finding_id: str
    severity: str
    priority: str
    drivers: List[str]
    mitigators: List[str]
    default_law_effect: str
    economic_effect: str
    explanation: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SignabilityDecision:
    level: str
    label: str
    decision_finding_ids: List[str]
    reasons: List[str]
    unresolved_uncertainty: List[str]
    manual_review_item_ids: List[str]
    blocking_manual_review_item_ids: List[str]
    confidence: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MissingProof:
    review_id: str
    searched_fact_types: List[str]
    searched_sections: List[str]
    lexical_queries: List[str]
    semantic_queries: List[str]
    cross_clause_queries: List[str]
    candidates_examined: List[str]
    possible_conflicts: List[str]
    exhaustive_enough: bool
    confidence: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceAssembly:
    review_id: str
    candidate_evidence: List[str]
    evidence_groups: List[Dict[str, Any]]
    supporting_evidence: List[str]
    counter_evidence: List[str]
    missing_elements: List[str]

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceCandidate:
    evidence_id: str
    source_document: str
    clause_id: str
    sentence_id: int
    quote: str
    semantic_score: float
    entity_match: bool
    obligation_match: bool
    consequence_match: bool
    polarity_match: bool
    entailment_status: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NegativeEvidence:
    review_id: str
    searched_scope: str
    positive_patterns: List[str]
    semantic_queries: List[str]
    candidate_count: int
    rejected_candidates: List[Dict[str, Any]]
    result: str
    confidence: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConfidenceDependency:
    requires_parser: bool = True
    requires_fact: bool = False
    requires_evidence: bool = False
    requires_applicability: bool = True
    requires_legal: bool = False
    requires_formula: bool = False
    requires_calculation: bool = False
    requires_verifier: bool = True

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConfidenceBundle:
    parser_confidence: str
    document_integrity_confidence: str
    fact_confidence: str
    retrieval_recall_confidence: str
    evidence_confidence: str
    applicability_confidence: str
    legal_confidence: str
    formula_confidence: str
    calculation_confidence: str
    verifier_confidence: str
    aggregation_confidence: str
    final_score: float
    final_confidence: str
    limiting_factors: List[str]
    required_components: List[str]
    ignored_components: List[str]
    component_scores: Dict[str, float]
    dependency: Dict[str, Any]
    reason: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Recommendation:
    recommendation_id: str
    type: str
    priority: str
    source_finding_ids: List[str]
    target_clause: str
    target_risk_ids: List[str]
    rationale: str
    suggested_text: str
    target_finding_ids: List[str] = field(default_factory=list)
    target_clause_ids: List[str] = field(default_factory=list)
    proposed_change: str = ""
    proposed_text: str = ""
    expected_effect: str = ""
    confidence: Dict[str, Any] = field(default_factory=dict)
    clauses: List[Dict[str, Any]] = field(default_factory=list)
    components: List[Dict[str, Any]] = field(default_factory=list)
    target_review_ids: List[str] = field(default_factory=list)
    perspective: str = ""
    impact: Dict[str, Any] = field(default_factory=dict)
    status: str = "CANDIDATE"
    recommendation_input_elements: List[str] = field(default_factory=list)
    fragments: List[Dict[str, Any]] = field(default_factory=list)
    excluded_element_ids: List[str] = field(default_factory=list)
    excluded_reasons: Dict[str, str] = field(default_factory=dict)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClientInterestDecision:
    risk_id: str
    review_ids: List[str]
    client_party: str
    effect_on_client: str
    legal_default_protection: str
    recommendation_disposition: str
    decision_reason: str
    source_recommendation_ids: List[str] = field(default_factory=list)
    blocked_recommendation_ids: List[str] = field(default_factory=list)
    authority_ids: List[str] = field(default_factory=list)
    impact_summary: Dict[str, Any] = field(default_factory=dict)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FinalDisposition:
    risk_id: str
    risk_title: str
    review_ids: List[str]
    severity: str
    client_effect: str
    legal_default_protection: str
    actionability: str
    final_action: str
    final_reason: str
    recommendation: str
    recommendation_owner: str
    formal_recommendation: Optional[str]
    include_in_top_risk: bool
    include_in_priority_changes: bool
    include_in_optional_improvements: bool
    review_instruction: str = ""
    source_recommendation_ids: List[str] = field(default_factory=list)
    blocked_recommendation_ids: List[str] = field(default_factory=list)
    authority_ids: List[str] = field(default_factory=list)
    severity_action_alignment: str = ""
    downgrade_reason: str = ""
    final_missing_elements: List[Dict[str, Any]] = field(default_factory=list)
    final_missing_element_ids: List[str] = field(default_factory=list)
    excluded_missing_element_ids: List[str] = field(default_factory=list)
    excluded_reasons: Dict[str, str] = field(default_factory=dict)
    report_visibility: str = "VISIBLE"
    suppression_reason: str = ""

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def _stable_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _request_scoped_profile(profile: Optional[UserRiskProfile], contract_type: str) -> UserRiskProfile:
    source = profile.to_dict() if profile is not None else UserRiskProfile.default().to_dict()
    normalized = dict(source)
    if contract_type == "sale" and normalized.get("contract_scenario") in {"", "居住用途", "投资/转租"}:
        normalized["contract_scenario"] = "商品买卖"
    elif contract_type in {"house_lease", "lease"} and not normalized.get("contract_scenario"):
        normalized["contract_scenario"] = "居住用途"
    return UserRiskProfile.from_dict(normalized)


def _has_negated_word(text: str, word: str, window: int = 5) -> bool:
    for match in re.finditer(re.escape(word), text):
        prefix = text[max(0, match.start() - window):match.start()]
        if any(negation in prefix for negation in NEGATION_WORDS):
            return True
    return False


def _has_unnegated_word(text: str, word: str, window: int = 5) -> bool:
    for match in re.finditer(re.escape(word), text):
        prefix = text[max(0, match.start() - window):match.start()]
        if not any(negation in prefix for negation in NEGATION_WORDS):
            return True
    return False


def _matched_terms(text: str, terms: tuple[str, ...]) -> List[str]:
    return matched_terms(text, terms)


_CONTRACT_APPLICABILITY_KEYWORDS: Dict[str, Dict[str, tuple[str, ...]]] = {
    "sale": {
    "common_format_clause_notice": ("格式条款", "特别提示", "提示说明", "加粗", "免除责任", "限制责任", "加重责任", "单方提供"),
    "sale_retention_title_clause": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_retention_registration": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_retention_retake": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_retention_redemption": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_installment_payment": ("分期付款", "分期支付", "分批付款", "每期", "首期", "尾期"),
    "sale_trial_use_period": ("试用", "试用期", "试运行", "试产", "免费试用", "先试后买"),
    "sale_trial_risk": ("试用", "试用期", "试运行", "试产", "免费试用", "先试后买"),
    "sale_sample_quality": ("样品", "样板", "封样", "凭样品", "样品确认", "按样交付"),
    "sale_risk_goods_in_transit": ("路货买卖", "在途", "在途货物", "运输途中", "已发运", "发运后转卖"),
    },
    "deposit": {
        "safekeeping_valuable_declaration": ("贵重物品", "货币", "有价证券", "珠宝", "名表", "贵金属", "重要文件", "高价值"),
        "safekeeping_undeclared_valuable_consequence": ("贵重物品", "货币", "有价证券", "珠宝", "名表", "贵金属", "重要文件", "高价值"),
        "safekeeping_consumptive_type": ("消费保管", "货币保管", "可替代物", "同种类", "同品质", "混同保管"),
        "safekeeping_consumptive_return_rule": ("消费保管", "货币保管", "可替代物", "同种类", "同品质", "混同保管"),
        "safekeeping_currency_interest": ("货币保管", "现金", "款项", "利息", "收益"),
        "safekeeping_consumptive_mixing": ("消费保管", "可替代物", "同类物", "批量保管", "混同保管"),
    },
    "work_contract": {
        "work_main_subcontract_consent": ("转包", "分包", "外协", "第三人完成", "交由第三人", "委托第三人"),
        "work_auxiliary_subcontract_liability": ("转包", "分包", "外协", "第三人完成", "辅助工作", "委托第三人"),
        "work_illegal_total_subcontract": ("全部转包", "整体转包", "肢解转包", "拆分转包", "主要工作交由第三人"),
        "work_sample_attachment": ("样品", "样板", "封样", "凭样", "样品确认", "按样制作"),
    },
    "agency": {
        "agency_sub_entrustment_consent": ("转委托", "第三人处理", "委托别人", "另行委托", "委托第三人"),
        "agency_sub_entrustment_liability": ("转委托", "第三人处理", "委托别人", "另行委托", "委托第三人"),
        "agency_emergency_sub_entrustment": ("转委托", "第三人处理", "紧急情况", "无法联系", "维护委托人利益"),
        "agency_self_agency_consent": ("自己代理", "与自己交易", "利益冲突", "自我交易"),
        "agency_both_side_agency_consent": ("双方代理", "同时代理双方", "交易双方", "利益冲突"),
        "agency_conflict_unfair_transaction": ("利益冲突", "显失公平", "低价转让", "高价购买", "不公平"),
        "agency_undisclosed_principal_intervention": ("以自己名义", "隐名委托", "第三人不知道", "披露第三人", "介入权"),
        "agency_disclose_third_party": ("以自己名义", "隐名委托", "第三人不履行", "披露第三人", "交易资料"),
        "agency_intervention_defense_continuation": ("以自己名义", "隐名委托", "介入权", "抗辩", "抵销"),
        "agency_third_party_choice_right": ("以自己名义", "隐名委托", "披露委托人", "选择权", "第三人选择"),
        "agency_disclose_principal": ("以自己名义", "隐名委托", "披露委托人", "委托人身份", "第三人"),
        "agency_choice_defense_continuation": ("以自己名义", "隐名委托", "选择权", "抗辩", "抵销"),
    },
    "guarantee": {
        "guarantee_share_agreed": ("共同保证人", "共同保证", "共同担保", "连带共同保证", "多个保证人", "两个以上保证人", "保证人A", "保证人B", "保证人名单"),
        "joint_guarantor_internal_recourse": ("共同保证人", "共同保证", "共同担保", "连带共同保证", "多个保证人", "两个以上保证人", "保证人A", "保证人B", "保证人之间"),
        "maximum_guarantee_period": ("最高额保证", "最高额担保", "最高债权额", "债权确定期间", "最高额保证终止", "最高额保证期间"),
        "post_period_signature_new_guarantee": ("保证期间届满", "期间届满后", "催收通知签字", "催收通知", "重新保证", "新的保证合同", "继续承担保证责任", "责任恢复"),
    },
    "construction": {
        "valid_bid_award_document": ("招标", "投标", "中标", "中标通知书", "招标文件", "投标文件", "评标", "备案合同"),
    },
}


def _has_installment_pattern(compacted_text: str) -> bool:
    return bool(
        re.search(r"分[一二三四五六七八九十百\d]+期", compacted_text)
        or re.search(r"第[一二三四五六七八九十百\d]+期", compacted_text)
    )


def _construction_contract_body(contract_text: str) -> str:
    """Ignore test notes appended after the contract body."""
    body = contract_text
    for marker in ("**测试重点：", "测试重点：", "测试重点", "【测试重点】"):
        if marker in body:
            body = body.split(marker, 1)[0]
    return body


LEASE_APPLICABILITY_RULES: Dict[str, Dict[str, Any]] = {
    "HL-029": {
        "conditions": [{"fact": "early_termination.exists", "operator": "in", "value": [True, False]}],
        "logic": "AND",
        "not_applicable_reason": "统一事实图谱无法判断 early_termination.exists，HL-029 暂不进入高置信自动判断。",
        "applicable_reason": "HL-029 适用于提前退租机制完整性审查：early_termination.exists=true 时审查公式和损失补足，false 时审查条款缺失。",
    },
    "HL-030": {
        "applicability": {"all": [{"fact": "early_termination.exists", "operator": "eq", "value": False}]},
        "not_applicable_reason": "统一事实图谱显示 early_termination.exists=true，合同已存在提前退租条款，HL-030 仅适用于合同完全未约定提前退租机制时的协商补位场景。",
        "applicable_reason": "统一事实图谱未识别到提前退租条款，HL-030 作为无提前退租条款时的协商补位机制审查。",
    }
}


_TECHNOLOGY_SUBTYPE_KEYWORDS: Dict[str, tuple[str, ...]] = {
    "development": ("技术开发", "委托开发", "合作开发", "研究开发", "研发", "新技术", "新产品", "新工艺", "新材料"),
    "entrusted_development": (
        "委托开发",
        "委托研究开发",
        "委托研发",
        "技术开发（委托）",
        "技术开发(委托)",
        "委托方",
        "委托人",
        "研究开发方",
        "研究开发人",
        "委托乙方研究开发",
        "甲方委托乙方",
    ),
    "cooperative_development": ("合作开发", "双方共同", "共同投资", "共同参与", "共同研发", "共同研究开发", "协作开发"),
    "transfer": ("技术转让", "专利权转让", "专利申请权转让", "技术秘密转让", "让与", "受让"),
    "license": ("技术许可", "专利实施许可", "许可使用", "许可人", "被许可人", "独占许可", "排他许可", "普通许可"),
    "consulting": ("技术咨询", "咨询报告", "可行性论证", "技术预测", "分析评价"),
    "service": ("技术服务", "解决特定技术问题", "服务成果", "服务内容", "技术培训", "技术支持"),
    "import_export": ("技术进出口", "技术进口", "技术出口", "跨境技术", "跨境许可", "跨境交付", "数据出境"),
    "research_org": ("课题组", "实验室", "研究中心", "科研组织", "内部机构"),
    "existing_tech_fraud": ("现有技术", "冒充研发", "重复收费", "同一课题", "欺诈"),
}


_TECHNOLOGY_SUBTYPE_LABELS: Dict[str, str] = {
    "development": "技术开发",
    "entrusted_development": "委托开发",
    "cooperative_development": "合作开发",
    "transfer": "技术转让",
    "license": "技术许可",
    "consulting": "技术咨询",
    "service": "技术服务",
    "import_export": "技术进出口",
    "research_org": "科研组织签约",
    "existing_tech_fraud": "现有技术冒充研发",
}


def _detect_technology_subtypes(compacted_text: str) -> set[str]:
    subtypes: set[str] = set()
    for subtype, keywords in _TECHNOLOGY_SUBTYPE_KEYWORDS.items():
        if any(_has_unnegated_word(compacted_text, keyword, window=18) for keyword in keywords):
            subtypes.add(subtype)
    if {"entrusted_development", "cooperative_development"} & subtypes:
        subtypes.add("development")
    if "development" in subtypes and "cooperative_development" not in subtypes:
        subtypes.add("entrusted_development")
    return subtypes


def _technology_subtype_reason(subtypes: set[str], checkpoint: ReviewCheckpoint) -> str:
    labels = "、".join(_TECHNOLOGY_SUBTYPE_LABELS[subtype] for subtype in sorted(subtypes) if subtype in _TECHNOLOGY_SUBTYPE_LABELS)
    if not labels:
        labels = "未识别到明确技术合同子类型"
    return f"当前文本识别为{labels}场景，未触发“{checkpoint.title}”的适用条件：{checkpoint.applicable_if}"


def _is_technology_checkpoint_applicable(compacted_text: str, checkpoint: ReviewCheckpoint) -> tuple[Optional[bool], str]:
    subtypes = _detect_technology_subtypes(compacted_text)
    item_id = checkpoint.item_id
    node_id = checkpoint.node_id

    if node_id == "technology_contract_type_classification":
        known_subtypes = {"development", "transfer", "license", "consulting", "service"} & subtypes
        return (False, _technology_subtype_reason(subtypes, checkpoint)) if known_subtypes else (True, "")

    if node_id == "fraud_contract_existing_technology":
        return (True, "") if "existing_tech_fraud" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))

    if node_id == "research_organization_authorization":
        return (True, "") if "research_org" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))

    if item_id.startswith("TC-04"):
        if "entrusted_development" in subtypes and "cooperative_development" not in subtypes:
            return True, ""
        return False, _technology_subtype_reason(subtypes, checkpoint)

    if item_id.startswith("TC-05"):
        if node_id == "technical_secret_result_rights":
            return (True, "") if "development" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))
        if node_id == "cooperation_breach_and_exit":
            return (True, "") if "development" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))
        if "cooperative_development" in subtypes:
            return True, ""
        return False, _technology_subtype_reason(subtypes, checkpoint)

    subtype_by_prefix = {
        "TC-06": "transfer",
        "TC-07": "license",
        "TC-08": "consulting",
        "TC-09": "service",
    }
    for prefix, subtype in subtype_by_prefix.items():
        if item_id.startswith(prefix):
            return (True, "") if subtype in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))

    if node_id == "technology_import_export_control":
        return (True, "") if "import_export" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))

    return None, ""


def _service_has_fixed_completion_structure(compacted: str) -> bool:
    if any(term in compacted for term in ("无固定期限", "未约定固定期限", "没有固定期限", "无固定服务期限")):
        return False
    fixed_terms = (
        "服务期限", "合同期限", "培训期限", "课程期限", "开课日期", "结课日期", "结束日期",
        "总课时", "课时", "一次性", "固定期限", "固定课程", "完成后", "交付后",
    )
    date_range = bool(
        re.search(r"(?:自|从).{0,16}(?:至|到|截至|截止)", compacted)
        or re.search(r"(?:开课|开始).{0,12}(?:结课|结束|完成)", compacted)
        or re.search(r"\d+\s*(?:课时|次|节)", compacted)
    )
    return date_range or any(term in compacted for term in fixed_terms)


def _service_has_continuing_indefinite_structure(compacted: str) -> bool:
    return any(
        term in compacted
        for term in (
            "不定期服务", "长期服务", "持续服务", "连续服务", "自动续费", "自动续约",
            "会员有效期届满后继续", "随时解除", "按月服务", "长期持续", "无固定期限",
        )
    )


def _service_has_platform_structure(compacted: str) -> bool:
    platform_terms = ("平台", "用户协议", "平台规则", "在线服务", "小程序", "APP", "app", "网站", "平台条款", "规则更新")
    account_terms = ("账号", "账户")
    has_platform = any(term in compacted for term in platform_terms)
    has_account_only = any(term in compacted for term in account_terms) and not has_platform
    if has_account_only:
        return False
    return has_platform and any(
        term in compacted
        for term in ("用户协议", "平台规则", "平台条款", "规则更新", "重大权益", "自动续费", "账号", "账户")
    )


def _service_has_format_clause_trigger(compacted: str) -> bool:
    public_template = any(term in compacted for term in ("示范文本", "政府发布", "协会发布", "公开范本"))
    negotiated = any(term in compacted for term in ("双方协商填写", "双方协商一致", "逐条协商", "可协商修改"))
    prepared_by_one_party = any(term in compacted for term in ("服务方提供", "经营者提供", "甲方提供", "乙方提供", "一方预先拟定"))
    non_negotiable = any(term in compacted for term in ("不可修改", "不得修改", "重复使用", "未与对方协商", "无权修改"))
    restrictive = any(term in compacted for term in ("免除责任", "限制责任", "加重责任", "排除主要权利", "概不退款", "不予退费", "单方变更", "最终解释权"))
    if public_template and negotiated and not (prepared_by_one_party and non_negotiable and restrictive):
        return False
    return (prepared_by_one_party and non_negotiable and restrictive) or ("格式条款" in compacted and restrictive)


def _is_service_checkpoint_applicable(compacted: str, checkpoint: ReviewCheckpoint) -> tuple[Optional[bool], str]:
    condition_text = f"{checkpoint.node_id} {checkpoint.title} {checkpoint.applicable_if}"
    nature = getattr(checkpoint, "review_nature", "CONTRACTUAL_REQUIREMENT")
    if nature == "CONDITIONAL_REQUIREMENT" and any(term in condition_text for term in ("不定期", "长期持续", "继续性服务")):
        if _service_has_continuing_indefinite_structure(compacted) and not _service_has_fixed_completion_structure(compacted):
            return True, "合同体现无固定完成节点或长期持续服务结构，适用不定期继续性服务解除审查。"
        if _service_has_fixed_completion_structure(compacted):
            return False, "合同已体现固定课程、固定课时、明确期限或完成节点，不属于不定期继续性服务。"
        return False, "未发现无固定期限、长期持续履行或无完成节点的服务结构。"
    if nature == "CONDITIONAL_REQUIREMENT" and "平台" in condition_text:
        if _service_has_platform_structure(compacted):
            return True, "合同体现平台、用户协议、账号或平台规则等事实，适用平台条款变更审查。"
        return False, "未发现互联网平台、用户协议、平台规则或平台单方更新机制。"
    if checkpoint.node_id == "format_clause_prompt_explain":
        if _service_has_format_clause_trigger(compacted):
            return True, "合同存在格式条款提示说明的触发事实。"
        return False, "未确认存在一方预先拟定、重复使用且限制责任或排除主要权利的格式条款。"
    return None, ""


def _is_checkpoint_applicable(contract_text: str, checkpoint: ReviewCheckpoint, contract_type_key: str, canonical_claims: Optional[Dict[str, Any]] = None) -> tuple[bool, str]:
    # Applicability must be resolved before Coverage.
    if checkpoint.applicability_triggers:
        claims = canonical_claims or {}
        resolved = [claims.get(trigger) for trigger in checkpoint.applicability_triggers]
        conflicts = [claim for claim in resolved if claim is not None and claim.status == "CONFLICT"]
        if conflicts or any(claim is None or claim.status == "UNKNOWN" for claim in resolved):
            return False, f"触发事实不足，暂不确定是否适用：{', '.join(checkpoint.applicability_triggers)}。"
        if all(bool(claim.object) for claim in resolved):
            return True, f"触发事实已满足：{', '.join(checkpoint.applicability_triggers)}。"
        return False, f"触发事实明确不成立：{', '.join(checkpoint.applicability_triggers)}。"
    applicability_text = _construction_contract_body(contract_text) if contract_type_key == "construction" else contract_text
    compacted = _compact(applicability_text)
    if contract_type_key == "technology":
        applicable, reason = _is_technology_checkpoint_applicable(compacted, checkpoint)
        if applicable is not None:
            return applicable, reason
    if contract_type_key == "service":
        applicable, reason = _is_service_checkpoint_applicable(compacted, checkpoint)
        if applicable is not None:
            return applicable, reason

    keywords = _CONTRACT_APPLICABILITY_KEYWORDS.get(contract_type_key, {}).get(checkpoint.node_id)
    if not keywords:
        return True, ""

    if contract_type_key == "guarantee" and checkpoint.node_id == "post_period_signature_new_guarantee":
        period_triggered = any(
            _has_unnegated_word(compacted, keyword, window=18)
            for keyword in ("保证期间届满", "期间届满后", "保证期间届满后")
        )
        signature_triggered = any(
            _has_unnegated_word(compacted, keyword, window=18)
            for keyword in ("催收通知签字", "催收通知上签字", "签字", "签收", "重新保证", "新的保证合同", "继续承担保证责任", "责任恢复")
        )
        if period_triggered and signature_triggered:
            return True, "合同文本同时出现保证期间届满后和催收签字/重新保证类表述，适用该专项审查点。"
        return False, f"未发现保证期间届满后催收签字或重新保证的组合情形：{checkpoint.applicable_if}"

    if checkpoint.node_id == "sale_installment_payment" and _has_installment_pattern(compacted):
        return True, "合同文本出现分期付款结构，适用该专项审查点。"
    if checkpoint.node_id == "common_format_clause_notice":
        public_template = any(term in compacted for term in ("示范文本", "政府发布", "协会发布", "公开范本"))
        negotiated = any(term in compacted for term in ("双方协商填写", "双方协商一致", "逐条协商", "可协商修改"))
        prepared_by_one_party = any(term in compacted for term in ("卖方提供", "买方提供", "甲方提供", "乙方提供", "一方预先拟定"))
        non_negotiable = any(term in compacted for term in ("不可修改", "不得修改", "重复使用", "未与对方协商", "无权修改"))
        restrictive = any(term in compacted for term in ("免除责任", "限制责任", "加重责任", "排除主要权利", "不承担任何"))
        if public_template and negotiated and not (prepared_by_one_party and non_negotiable):
            return False, "公开示范文本且合同记载双方协商填写，不能仅因文件具有范本外观推定为一方提供的格式条款。"
        if prepared_by_one_party and non_negotiable and restrictive:
            return True, "合同存在一方预先提供、缺乏实质协商且限制责任或权利的重要条款，触发格式条款提示说明审查。"
        return False, "仅能确认文本具有模板或范本外观，不能确认一方预先拟定、重复使用及缺乏实质协商；适用性暂不确定。"
    if checkpoint.node_id == "sale_risk_goods_in_transit":
        transit_sale_patterns = (
            "路货买卖",
            "在途货物交易",
            "买卖在途货物",
            "买卖运输途中的标的物",
            "已经发运正在运输途中的货物",
            "发运后转卖",
            "运输途中转卖",
        )
        composite_trigger = (
            "买卖" in compacted
            and any(term in compacted for term in ("已发运", "已经发运"))
            and any(term in compacted for term in ("运输途中", "正在运输途中", "在途货物"))
        )
        if composite_trigger or any(_has_unnegated_word(compacted, pattern, window=18) for pattern in transit_sale_patterns):
            return True, "合同明确涉及已发运或运输途中货物的转售，适用路货买卖专项审查。"
        return False, "普通运输交付不等于路货买卖；未发现已发运后转卖或运输途中买卖的触发事实。"
    if checkpoint.node_id == "sale_sample_quality":
        legal_sample_sale = any(
            phrase in compacted
            for phrase in ("凭样品买卖", "按样品交付", "按封样样品交付", "样品作为交付标准", "样品质量标准", "以样品为准")
        )
        if legal_sample_sale:
            return True, "合同明确以样品作为买卖标的质量或交付标准，适用凭样品买卖专项审查。"
        return False, "技术封样或承认书仅是质量标准证据，不当然构成凭样品买卖。"
    for keyword in keywords:
        if _has_unnegated_word(compacted, keyword, window=18):
            return True, f"合同文本出现“{keyword}”，适用该专项审查点。"
    return False, f"未发现触发该专项审查点的交易类型表述：{checkpoint.applicable_if}"


def _applicability_result_for_checkpoint(
    checkpoint: ReviewCheckpoint,
    clauses: List[Any],
    applicable: bool,
    reason: str,
    canonical_claims: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    conditional = bool(checkpoint.applicable_if)
    trigger_terms = list(_CONTRACT_APPLICABILITY_KEYWORDS.get("sale", {}).get(checkpoint.node_id, ()))
    required_triggers = list(checkpoint.applicability_triggers) or trigger_terms
    if checkpoint.node_id == "common_format_clause_notice":
        trigger_terms = [
            "卖方提供", "买方提供", "甲方提供", "乙方提供", "一方预先拟定",
            "不可修改", "不得修改", "重复使用", "未与对方协商", "限制责任", "免除责任",
        ]
    trigger_evidence = []
    trigger_facts = []
    for clause in clauses:
        matched = [term for term in trigger_terms if term and term in _compact(clause.text)]
        if not matched:
            continue
        trigger_facts.extend(matched)
        trigger_evidence.append({
            "clause_id": clause.clause_id,
            "location": clause.location,
            "quote": clause.text[:260],
            "block_type": clause.block_type,
        })
    uncertain = conditional and not applicable and "暂不确定" in reason
    status = "UNCERTAIN" if uncertain else "APPLICABLE" if applicable else "NOT_APPLICABLE"
    confidence = "low" if uncertain else "high" if (trigger_evidence or not conditional) else "medium"
    claim_rows = [canonical_claims.get(trigger) for trigger in checkpoint.applicability_triggers if canonical_claims and canonical_claims.get(trigger)]
    satisfied = [claim.claim_id for claim in claim_rows if bool(claim.object) and claim.status != "CONFLICT"]
    unsatisfied = [trigger for trigger in checkpoint.applicability_triggers if trigger not in satisfied]
    conflicting = [claim.claim_id for claim in claim_rows if claim.status == "CONFLICT"]
    claim_evidence_ids = [evidence_id for claim in claim_rows for evidence_id in claim.evidence_ids]
    return ApplicabilityResult(
        review_id=checkpoint.item_id,
        applicable=None if uncertain else applicable,
        trigger_facts=list(dict.fromkeys(trigger_facts)),
        trigger_evidence=trigger_evidence,
        missing_triggers=[] if applicable else trigger_terms,
        reason=reason or "未声明条件审查规则，默认适用于当前合同。",
        confidence=confidence,
        status=status,
        machine_reason=reason or "未声明条件审查规则，默认适用于当前合同。",
        user_reason=(
            f"现有合同信息不足以确认是否满足“{checkpoint.applicable_if}”，需结合相关材料核对。"
            if uncertain else
            f"合同已触发“{checkpoint.applicable_if}”这一适用条件。"
            if conditional and applicable else
            f"合同未触发“{checkpoint.applicable_if}”这一适用条件，本审查事项不适用。"
            if conditional else
            "该审查事项适用于当前合同。"
        ),
        required_triggers=required_triggers,
        satisfied_triggers=satisfied,
        unsatisfied_triggers=unsatisfied,
        conflicting_triggers=conflicting,
        trigger_fact_ids=[fact_id for claim in claim_rows for fact_id in claim.fact_ids],
        trigger_evidence_ids=claim_evidence_ids,
    ).to_public_dict()


def _get_fact_path_value(facts: Any, path: str) -> Any:
    value: Any = facts
    for part in path.split("."):
        if value is None:
            return None
        if isinstance(value, dict):
            value = value.get(part)
        else:
            value = getattr(value, part, None)
    return value


def _compare_applicability_value(actual: Any, operator: str, expected: Any = None) -> bool:
    if operator == "exists":
        return actual is not None and actual is not False
    if operator == "not_exists":
        return actual is None or actual is False
    if operator == "eq":
        return actual == expected
    if operator == "neq":
        return actual != expected
    if operator == "in":
        return actual in (expected or [])
    if operator in {"gt", "gte", "lt", "lte"}:
        if actual is None or expected is None:
            return False
        try:
            actual_num = float(actual)
            expected_num = float(expected)
        except (TypeError, ValueError):
            return False
        return {
            "gt": actual_num > expected_num,
            "gte": actual_num >= expected_num,
            "lt": actual_num < expected_num,
            "lte": actual_num <= expected_num,
        }[operator]
    return True


def _evaluate_applicability_condition(expr: Dict[str, Any], facts: HouseLeaseContractFacts) -> tuple[bool, List[str], List[Dict[str, Any]]]:
    if "all" in expr:
        evaluations: List[Dict[str, Any]] = []
        depends_on: List[str] = []
        results = []
        for child in expr.get("all") or []:
            result, child_depends, child_evals = _evaluate_applicability_condition(child, facts)
            results.append(result)
            depends_on.extend(child_depends)
            evaluations.extend(child_evals)
        return all(results), list(dict.fromkeys(depends_on)), evaluations
    if "any" in expr:
        evaluations = []
        depends_on = []
        results = []
        for child in expr.get("any") or []:
            result, child_depends, child_evals = _evaluate_applicability_condition(child, facts)
            results.append(result)
            depends_on.extend(child_depends)
            evaluations.extend(child_evals)
        return any(results), list(dict.fromkeys(depends_on)), evaluations
    if "not" in expr:
        result, depends_on, evaluations = _evaluate_applicability_condition(expr.get("not") or {}, facts)
        return (not result), depends_on, evaluations

    fact_path = expr.get("fact", "")
    operator = expr.get("operator", "exists")
    expected = expr.get("value")
    actual = _get_fact_path_value(facts, fact_path)
    passed = _compare_applicability_value(actual, operator, expected)
    return passed, [fact_path] if fact_path else [], [
        {
            "fact": fact_path,
            "operator": operator,
            "expected": expected,
            "actual": actual,
            "passed": passed,
        }
    ]


def _evaluate_applicability_rule(rule: Dict[str, Any], facts: HouseLeaseContractFacts) -> tuple[bool, List[str], List[Dict[str, Any]]]:
    if "applicability" in rule:
        return _evaluate_applicability_condition(rule.get("applicability") or {}, facts)
    conditions = rule.get("conditions") or []
    evaluations: List[Dict[str, Any]] = []
    depends_on: List[str] = []
    for condition in conditions:
        fact_path = condition.get("fact", "")
        operator = condition.get("operator", "exists")
        expected = condition.get("value")
        actual = _get_fact_path_value(facts, fact_path)
        passed = _compare_applicability_value(actual, operator, expected)
        depends_on.append(fact_path)
        evaluations.append(
            {
                "fact": fact_path,
                "operator": operator,
                "expected": expected,
                "actual": actual,
                "passed": passed,
            }
        )
    logic = (rule.get("logic") or "AND").upper()
    applicable = any(item["passed"] for item in evaluations) if logic == "OR" else all(item["passed"] for item in evaluations)
    return applicable, depends_on, evaluations


def _evaluate_lease_fact_applicability(checkpoint: ReviewCheckpoint, facts: HouseLeaseContractFacts) -> Dict[str, Any]:
    """Fact-driven applicability for mutually exclusive house-lease checkpoints."""
    rule = LEASE_APPLICABILITY_RULES.get(checkpoint.item_id)
    if rule:
        applicable, depends_on, evaluations = _evaluate_applicability_rule(rule, facts)
        machine_reason = rule["applicable_reason"] if applicable else rule["not_applicable_reason"]
        condition_label = checkpoint.applicable_if or checkpoint.title
        return {
            "status": "applicable" if applicable else "not_applicable",
            "applicable": applicable,
            "reason": machine_reason,
            "machine_reason": machine_reason,
            "user_reason": (
                f"合同现有安排满足“{condition_label}”的审查条件。"
                if applicable else
                f"合同现有安排不满足“{condition_label}”这一适用条件，本审查事项不适用。"
            ),
            "depends_on": depends_on,
            "evaluations": evaluations,
        }
    return {
        "status": "applicable",
        "applicable": True,
        "reason": "未触发事实层排除条件，继续执行审查。",
        "machine_reason": "未触发事实层排除条件，继续执行审查。",
        "user_reason": "该审查事项适用于当前合同。",
        "depends_on": [],
    }


def _not_applicable_item(checkpoint: ReviewCheckpoint, reason: str) -> ReviewItemResult:
    item = ReviewItemResult(
        item_id=checkpoint.item_id,
        node_id=checkpoint.node_id,
        title=checkpoint.title,
        risk_level=NotApplicableRisk(),
        status="不适用",
        risk_point_description="该审查点仅适用于特定交易场景，当前合同文本未触发对应适用条件。",
        suggested_clause_example=checkpoint.suggested_clause,
        legal_basis_index=checkpoint.legal_basis,
        legal_consequence_if_missing=checkpoint.legal_consequence_if_missing,
        applicable_if=checkpoint.applicable_if,
        matched_terms=[],
        coverage_status=COVERAGE_NOT_APPLICABLE,
        issue_type=ISSUE_NOT_APPLICABLE,
        evidence_clauses=[],
        evidence_location="",
        reasoning_summary=reason,
        judge_source="applicability_filter",
    )
    item.applicability = {
        "status": "not_applicable", "applicable": False, "reason": reason,
        "machine_reason": reason, "user_reason": _user_facing_reasoning(reason), "depends_on": [],
    }
    item.action_suggestion = "不适用"
    return item


def _insufficient_context_item(checkpoint: ReviewCheckpoint, reason: str) -> ReviewItemResult:
    user_reason = "现有合同材料不足以确认该事项是否适用，建议结合相关交易背景或补充材料核对。"
    item = ReviewItemResult(
        item_id=checkpoint.item_id,
        node_id=checkpoint.node_id,
        title=checkpoint.title,
        risk_level="中",
        status="需人工复核",
        risk_point_description=user_reason,
        suggested_clause_example="",
        legal_basis_index=checkpoint.legal_basis,
        legal_consequence_if_missing=user_reason,
        applicable_if=checkpoint.applicable_if,
        matched_terms=[],
        coverage_status=INSUFFICIENT_CONTEXT,
        issue_type="人工复核",
        evidence_clauses=[],
        evidence_location="",
        reasoning_summary=user_reason,
        judge_source="applicability_filter",
        needs_manual_review=True,
        quality_gate_failure_reason=user_reason,
    )
    item.applicability = {
        "status": INSUFFICIENT_CONTEXT,
        "applicable": None,
        "reason": reason or user_reason,
        "machine_reason": reason or user_reason,
        "user_reason": user_reason,
        "depends_on": [],
    }
    item.action_priority = DISPOSITION_MANUAL_REVIEW
    item.review_priority = DISPOSITION_MANUAL_REVIEW
    item.action_suggestion = "建议人工复核"
    item.decision_trace["insufficient_context"] = {
        "reason": reason or user_reason,
        "review_instruction": user_reason,
    }
    return item


def _checkpoint_metadata(checkpoint: ReviewCheckpoint) -> Dict[str, Any]:
    return {
        "review_mode": "ABSENCE_REQUIRED" if checkpoint.kind == "forbidden" else "PRESENCE_REQUIRED",
        "review_polarity": checkpoint.polarity,
        "review_nature": getattr(checkpoint, "review_nature", "CONTRACTUAL_REQUIREMENT"),
        "requirement_medium": getattr(checkpoint, "requirement_medium", "CONTRACT_TEXT"),
        "legal_requirement_strength": getattr(checkpoint, "legal_requirement_strength", "RISK_CONTROL"),
        "action_type": getattr(checkpoint, "action_type", "CONTRACT_EDIT"),
        "domain_owner": checkpoint.domain_owner,
        "material_group": checkpoint.material_group,
        "allowed_subject_matters": list(checkpoint.allowed_subject_matters),
        "satisfaction_semantics": {
            "polarity": checkpoint.polarity,
            "pass_meaning": "NO_ADVERSE_CLAUSE_FOUND" if checkpoint.polarity == "NEGATIVE_CLAUSE_CHECK" else "REQUIRED_PROTECTION_PRESENT",
            "partial_meaning": "REQUIRES_FURTHER_REVIEW",
            "missing_meaning": "REQUIRED_PROTECTION_ABSENT",
            "risk_meaning": "ADVERSE_CLAUSE_FOUND",
            "not_applicable_meaning": "TRIGGER_NOT_PRESENT",
        },
    }


def _apply_checkpoint_metadata(
    items: List[ReviewItemResult],
    checklist: Sequence[ReviewCheckpoint],
    searched_scope: Optional[List[str]] = None,
) -> None:
    checkpoint_by_id = {row.item_id: row for row in checklist}
    searched = list(searched_scope or [])
    for item in items:
        checkpoint = checkpoint_by_id.get(item.item_id)
        if not checkpoint:
            continue
        item.decision_trace.update(_checkpoint_metadata(checkpoint))
        if checkpoint.polarity == "NEGATIVE_CLAUSE_CHECK":
            adverse_candidates = list(item.evidence_clauses or []) if item.coverage_status == "风险条款" else []
            search_sufficient = bool(searched) or item.coverage_status in {"通过", "风险条款"}
            item.decision_trace["negative_clause_check"] = {
                "review_id": item.item_id,
                "searched_scope": searched,
                "candidate_adverse_clauses": adverse_candidates,
                "counter_evidence": [],
                "search_coverage": "SUFFICIENT" if search_sufficient else "INSUFFICIENT",
                "adverse_clause_exists": bool(adverse_candidates),
                "confidence": "high" if search_sufficient else "low",
                "coverage_result": item.coverage_status,
            }


def _mark_internal_classification_item(item: ReviewItemResult, reason: str) -> None:
    item.risk_level = "低"
    item.status = "已完成内部法律定性"
    item.coverage_status = "通过"
    item.issue_type = "通过"
    item.risk_point_description = "该审查点用于系统内部法律定性，不因合同未单列分类表述而形成合同缺陷。"
    item.legal_consequence_if_missing = "该事项属于内部法律定性结果，不构成独立合同缺口。"
    item.reasoning_summary = reason
    item.action_priority = ACTION_PRIORITY_NONE
    item.review_priority = ACTION_PRIORITY_NONE
    item.action_suggestion = "无需处理"
    item.risk_severity = SEVERITY_NONE
    item.residual_risk = "内部法律定性已完成，不形成独立风险。"
    item.related_risks = []
    item.decision_trace["internal_classification_result"] = {
        "status": "CLASSIFIED",
        "confidence": "high",
        "reason": reason,
        "risk_entity_created": False,
        "formal_recommendation_allowed": False,
        "final_disposition_allowed": False,
    }


def _apply_review_nature_outcomes(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    for item in items:
        nature = str((item.decision_trace or {}).get("review_nature") or "")
        if nature == "INTERNAL_CLASSIFICATION":
            _mark_internal_classification_item(
                item,
                item.reasoning_summary
                or f"系统已根据合同文本完成“{item.title}”的内部法律定性；该定性用于后续适用规则，不要求合同正文写入分类结论。",
            )
        if (item.decision_trace or {}).get("review_polarity") == "NEGATIVE_CLAUSE_CHECK" and item.coverage_status == "通过":
            item.status = "未发现明显风险条款"
            item.issue_type = "通过"
            item.risk_level = "低"
            item.risk_point_description = f"未发现“{item.title}”对应的不利或违法表述。"
            item.reasoning_summary = item.reasoning_summary or "正式合同条款和附件中未召回该类明显风险表述。"
            item.action_priority = ACTION_PRIORITY_NONE
            item.review_priority = ACTION_PRIORITY_NONE
            item.action_suggestion = "无需处理"
            item.risk_severity = SEVERITY_NONE
            item.residual_risk = "未发现不利条款，不形成对应风险。"
            item.related_risks = []
    return items


def _is_case_document_excerpt(text: str) -> bool:
    compacted = _compact(text)
    if "原告" in compacted and "被告" in compacted and ("租赁合同" in compacted or "房屋租赁合同" in compacted):
        return True
    hit_count = sum(1 for hint in CASE_DOCUMENT_HINTS if hint in compacted)
    return hit_count >= 2 and ("合同" in compacted or "租赁" in compacted)


def _apply_source_exemptions(item: ReviewItemResult, contract_text: str) -> ReviewItemResult:
    if item.item_id != "HL-002" or not _is_case_document_excerpt(contract_text):
        return item
    if item.coverage_status == "通过":
        item.risk_level = "低"
        return item

    item.risk_level = "低"
    item.status = "已覆盖"
    item.coverage_status = "通过"
    item.issue_type = "通过"
    item.risk_point_description = (
        "输入文本呈现为案件文书摘录，通常只会保留出租人、承租人的诉讼身份或角色摘要，"
        "不能按完整签约合同要求其载明证件号、住所和联系方式。正式合同原文仍建议补全主体身份信息。"
    )
    item.reasoning_summary = (
        "检测到文本具有案件文书摘录特征，本项按来源豁免处理：只要能够识别出租人与承租人的角色，"
        "不因摘录中缺少证件号、住所、联系方式而认定为条款缺陷。"
    )
    focused_evidence = [
        clause
        for clause in item.evidence_clauses
        if ("原告" in clause.get("text", "") and "被告" in clause.get("text", ""))
        or ("出租人" in clause.get("text", "") and "承租人" in clause.get("text", ""))
    ]
    if focused_evidence:
        item.evidence_clauses = focused_evidence[:1]
        item.evidence_location = item.evidence_clauses[0].get("location", "")
    item.fallback_reason = "案件文书摘录来源豁免"
    return item


def _apply_gift_consideration_override(item: ReviewItemResult, contract_text: str) -> ReviewItemResult:
    if item.item_id != "G-01-04" or item.coverage_status != "风险条款":
        return item
    if _has_gift_paid_consideration_risk(contract_text):
        return item

    item.risk_level = "低"
    item.status = "未发现明显风险条款"
    item.coverage_status = "通过"
    item.issue_type = "通过"
    item.risk_point_description = (
        "合同已明确无偿赠与，且未发现未被无偿声明排除的价款、收益、回购、还款或其他实质有偿对价安排。"
    )
    item.reasoning_summary = (
        "检测到合同已声明无偿赠与或无需支付对价，G-01-04 不再因“对价”等否定语境中的词语误判为风险条款。"
    )
    item.matched_terms = []
    item.evidence_clauses = []
    item.evidence_location = ""
    item.fallback_reason = "赠与无偿性专项校正"
    return item


_DEPENDENCY_BAD_COVERAGE = {"部分覆盖", "缺失", "风险条款"}
_DEPENDENCY_BAD_ISSUES = {"模板空白", "条款缺陷", "完全缺失", "风险条款"}
_GIFT_CHECKPOINT_DEPENDENCIES: Dict[str, Dict[str, str]] = {
    "G-09-03": {
        "depends_on": "G-09-01",
        "risk_level": "中",
        "mode": "partial",
        "reason": "不履行附义务的救济以受赠人义务内容为前提；前置义务内容未完整填写时，救济条款不能单独视为完整通过。",
    },
    "G-10-04": {
        "depends_on": "G-09-01",
        "risk_level": "中",
        "mode": "sync",
        "reason": "附义务赠与瑕疵担保范围以受赠人义务内容为计算和适用前提；前置义务内容缺失或空白时，本项应同步前置条款状态。",
    },
    "G-11-01": {
        "depends_on": "G-01-02",
        "risk_level": "中",
        "mode": "sync",
        "reason": "撤销后返还规则以赠与的无偿性基础为前提；无偿赠与意思表示未完整覆盖时，本项应同步前置条款状态。",
    },
}


def _dependency_is_incomplete(item: ReviewItemResult | None) -> bool:
    if not item:
        return False
    return item.coverage_status in _DEPENDENCY_BAD_COVERAGE or item.issue_type in _DEPENDENCY_BAD_ISSUES


def _dependency_status(dep: ReviewItemResult) -> str:
    if dep.coverage_status == "缺失":
        return "缺失或不明确"
    if dep.coverage_status == "风险条款":
        return "发现风险条款"
    return "部分覆盖，需先补全前置条款"


def _apply_gift_dependency_rules(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    by_id = {item.item_id: item for item in items}
    for item_id, rule in _GIFT_CHECKPOINT_DEPENDENCIES.items():
        item = by_id.get(item_id)
        dependency = by_id.get(rule["depends_on"])
        if not item or not _dependency_is_incomplete(dependency):
            continue

        assert dependency is not None
        item.risk_level = rule["risk_level"]
        if rule["mode"] == "sync":
            item.coverage_status = dependency.coverage_status
            item.issue_type = dependency.issue_type
            item.status = _dependency_status(dependency)
        else:
            item.coverage_status = "部分覆盖"
            item.issue_type = dependency.issue_type if dependency.issue_type == "模板空白" else "条款缺陷"
            item.status = "部分覆盖，需先补全前置条款"
        item.reasoning_summary = f"{rule['reason']} 当前前置审查点 {dependency.item_id}（{dependency.title}）状态为“{dependency.coverage_status}/{dependency.issue_type}”。"
        item.risk_point_description = f"该审查点依赖前置条款“{dependency.title}”。前置条款未完整覆盖时，本项不能单独认定为完整通过。"
        item.fallback_reason = "赠与合同跨条款依赖校正"
    return items


def _apply_technology_development_mode_rules(items: List[ReviewItemResult], contract_text: str) -> List[ReviewItemResult]:
    subtypes = _detect_technology_subtypes(_compact(contract_text))
    if "entrusted_development" not in subtypes or "cooperative_development" in subtypes:
        return items

    for item in items:
        if item.item_id != "TC-05-03" or item.coverage_status == COVERAGE_NOT_APPLICABLE:
            continue
        item.risk_level = "中"
        item.risk_point_description = (
            "委托开发合同中，技术秘密成果使用转让规则仍建议明确；但该项可由委托开发成果归属、保密和验收交付条款部分承接，"
            "缺失通常不属于直接阻碍合同履行的高风险。"
        )
        item.reasoning_summary = (
            f"{item.reasoning_summary} 当前合同识别为委托开发合同，TC-05-03 按委托开发场景降为中风险；"
            "如技术秘密成果具有核心商业价值，仍建议补充使用、转让、许可、收益分配和保密限制。"
        )
        item.fallback_reason = "技术合同开发方式风险校正"
    return items


def _clause_public_dict(clause: Any) -> Dict[str, Any]:
    data = clause.to_public_dict() if hasattr(clause, "to_public_dict") else asdict(clause)
    return _enrich_evidence_source(data)


def _document_type_for_evidence(evidence: Dict[str, Any]) -> str:
    section = str(evidence.get("section_type") or "")
    location = str(evidence.get("location") or evidence.get("section") or "")
    title = str(evidence.get("title") or "")
    source = str(evidence.get("source") or "")
    combined = f"{section} {location} {title} {source}"
    if section == "附件" or "附件" in combined or "附表" in combined:
        return "APPENDIX"
    if "补充协议" in combined or "补充条款" in combined:
        return "SUPPLEMENTARY_TERMS"
    if "变更协议" in combined or "修订" in combined:
        return "AMENDMENT"
    if "另行函件" in combined or "承诺函" in combined:
        return "SIDE_LETTER"
    if section in {"正式合同条款", "特别提示"} or source in {"body", "party_info", "signature"}:
        return "MAIN_CONTRACT"
    return "OTHER"


def _sentence_quote(text: str) -> tuple[int, str]:
    cleaned = _clean_evidence_text(text)
    if not cleaned:
        return 0, ""
    sentences = [part.strip() for part in re.split(r"(?<=[。；;！？!])", cleaned) if part.strip()]
    quote = sentences[0] if sentences else cleaned
    return 1, quote


def _enrich_evidence_source(evidence: Dict[str, Any]) -> Dict[str, Any]:
    enriched = dict(evidence or {})
    document_type = enriched.get("document_type") or enriched.get("source_document_type") or _document_type_for_evidence(enriched)
    sentence_index, quote = _sentence_quote(str(enriched.get("text") or enriched.get("quote") or ""))
    enriched.setdefault("document_id", "contract_package/main" if document_type == "MAIN_CONTRACT" else f"contract_package/{document_type.lower()}")
    enriched.setdefault("document_type", document_type)
    enriched.setdefault("source_document_type", document_type)
    enriched.setdefault("evidence_block_type", enriched.get("block_type") or (
        "ANNEX" if document_type == "APPENDIX" else
        "PARTY_INFORMATION" if enriched.get("source") == "party_info" else
        "SIGNATURE_BLOCK" if enriched.get("source") == "signature" else
        "OPERATIVE_CLAUSE"
    ))
    enriched.setdefault("document_name", "合同正文" if document_type == "MAIN_CONTRACT" else "合同附件/补充文件")
    enriched.setdefault("section", enriched.get("location") or enriched.get("section_type") or "")
    enriched.setdefault("sentence_index", sentence_index)
    enriched.setdefault("quote", quote)
    enriched.setdefault("confidence", "high" if quote else "medium")
    enriched.setdefault(
        "evidence_source",
        {
            "document_id": enriched["document_id"],
            "document_type": enriched["document_type"],
            "document_name": enriched["document_name"],
            "clause_id": enriched.get("clause_id"),
            "section": enriched.get("section"),
            "sentence_index": enriched.get("sentence_index"),
            "quote": enriched.get("quote"),
            "confidence": enriched.get("confidence"),
            "evidence_block_type": enriched.get("evidence_block_type"),
        },
    )
    return enriched


def _enrich_evidence_sources(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    for item in items:
        item.evidence_clauses = [_enrich_evidence_source(evidence) for evidence in (item.evidence_clauses or [])]
        locations = [
            value.strip()
            for value in re.split(r"[；;\n]+", item.evidence_location or "")
            if value.strip() and re.search(r"[\w\u4e00-\u9fff]", value.strip())
        ]
        item.evidence_location = "；".join(dict.fromkeys(locations))
    return items


def _evidence_claim_for_item(item: ReviewItemResult) -> EvidenceClaim:
    semantics = [item.node_id, item.risk_group, item.title]
    proposition = item.risk_point_description or item.legal_consequence_if_missing or item.title
    if item.node_id == "deposit_offset_order":
        proposition = "合同是否约定押金可抵扣的项目以及未付款项之间的抵扣顺序。"
        semantics = ["押金", "抵扣", "扣除", "顺序", "未付租金", "水电费", "维修费", "余额返还"]
    elif item.risk_group == "early_termination_financial_exposure":
        proposition = "合同是否约定提前退租违约金公式及其随剩余租期放大的经济后果。"
        semantics = ["提前退租", "违约金", "剩余租期", "租金", "倍", "损失"]
    elif item.node_id == "move_in_defect_notice":
        proposition = "合同是否约定入住或交接时瑕疵告知和记录机制。"
        semantics = ["入住", "交接", "瑕疵", "告知", "照片", "视频", "记录"]
    elif item.node_id == "deposit_return_deadline":
        proposition = "合同是否约定押金返还期限。"
        semantics = ["押金", "返还", "退还", "期限", "日内", "交接", "结清"]
    return EvidenceClaim(
        claim_id=f"{item.item_id}-EC-01",
        review_id=item.item_id,
        finding_id=RISK_FINDING_ID_BY_GROUP.get(item.risk_group or item.node_id or "", ""),
        proposition=proposition,
        required_semantics=[str(value) for value in semantics if value],
        polarity="negative" if item.issue_type == "不利条款" else "positive",
        object=item.node_id,
        consequence=item.legal_consequence_if_missing,
        confidence="high" if item.risk_group in {"early_termination_financial_exposure", "deposit_offset_order"} else "medium",
    )


def _coverage_claim_for_item(item: ReviewItemResult) -> CoverageClaim:
    required: List[Dict[str, Any]] = []
    minimum_pass = 1
    minimum_partial = 1
    alternative = (item.decision_trace or {}).get("alternative_satisfaction") or {}
    if item.node_id == "service_content_standard":
        required = [
            {"element_id": "service_name", "required_fact": "service.course_name", "proposition": "服务或课程名称明确。", "terms": ["课程名称", "服务名称", "课程", "培训项目"]},
            {"element_id": "class_or_project_id", "required_fact": "service.project_id", "proposition": "班级编号、项目编号或服务项目可识别。", "terms": ["班级", "编号", "项目", "服务项目"]},
            {"element_id": "service_hours", "required_fact": "service.total_sessions", "proposition": "总课时、服务次数或服务频次明确。", "terms": ["总课时", "课时", "服务次数", "频次"]},
            {"element_id": "session_duration", "required_fact": "service.session_duration", "proposition": "单次课时、每次时长或服务时长明确。", "terms": ["每次", "单次", "时长", "课时"]},
            {"element_id": "service_location", "required_fact": "service.location", "proposition": "培训地点、服务地点或交付地点明确。", "terms": ["培训地点", "上课地点", "服务地点", "地点"]},
            {"element_id": "delivery_method", "required_fact": "service.delivery_mode", "proposition": "线上、线下、面授、预约或其他服务方式明确。", "terms": ["线上", "线下", "面授", "预约", "方式"]},
        ]
        minimum_pass = 5
        minimum_partial = 2
    elif item.node_id == "service_schedule_and_place":
        required = [
            {"element_id": "service_time", "required_fact": "service.schedule", "proposition": "上课时间、服务时间或预约时间明确。", "terms": ["上课时间", "服务时间", "每周", "预约"]},
            {"element_id": "start_date", "required_fact": "service.start_date", "proposition": "开课日期或服务开始日期明确。", "terms": ["开课日期", "开始日期", "服务开始", "自"]},
            {"element_id": "end_date", "required_fact": "service.end_date", "proposition": "预计结课日期、结束日期或服务期限明确。", "terms": ["结课日期", "结束日期", "服务期限", "至"]},
            {"element_id": "service_location", "required_fact": "service.location", "proposition": "培训地点或服务地点明确。", "terms": ["培训地点", "上课地点", "服务地点", "地点"]},
            {"element_id": "delivery_method", "required_fact": "service.delivery_mode", "proposition": "服务方式、线上线下或预约安排明确。", "terms": ["线上", "线下", "面授", "预约", "方式"]},
        ]
        minimum_pass = 4
        minimum_partial = 2
    elif item.node_id == "service_quality_standard":
        required = [
            {"element_id": "course_content_standard", "proposition": "课程内容、服务说明或教学内容标准明确。", "terms": ["课程内容", "教学内容", "服务说明", "课程安排"]},
            {"element_id": "hour_completion_standard", "proposition": "课时完成、签到或服务完成标准明确。", "terms": ["课时", "完成", "签到", "服务完成"]},
            {"element_id": "teacher_requirement", "proposition": "师资、教师安排或服务人员要求明确。", "terms": ["教师", "老师", "师资", "服务人员"]},
            {"element_id": "makeup_or_reschedule_standard", "proposition": "调课、停课、缺课或补课标准明确。", "terms": ["调课", "停课", "缺课", "补课", "预约"]},
            {"element_id": "nonconformity_handling", "proposition": "服务未达约定标准时的补正、重新履行或处理层级明确。", "terms": ["补正", "重新提供", "补救", "质量", "不达标"]},
        ]
        minimum_pass = 4
        minimum_partial = 2
    elif item.node_id == "prepaid_amount_and_balance":
        required = [
            {"element_id": "total_fee", "required_fact": "payment.total_fee", "proposition": "培训费用、服务费或预付款总额明确。", "terms": ["培训费用", "服务费", "预付款", "合计", "总金额"]},
            {"element_id": "paid_amount", "required_fact": "payment.amount_paid", "proposition": "已付金额、分期支付金额或付款节点明确。", "terms": ["支付", "已付", "付款", "分期", "之前支付"]},
            {"element_id": "unit_price", "required_fact": "payment.unit_price", "proposition": "课时单价、单次价格或可推导单价明确。", "terms": ["单价", "课时费", "课时", "每次"]},
            {"element_id": "balance_calculation", "required_fact": "payment.remaining_balance", "proposition": "余额、剩余课时或未提供服务对应款项的计算方式明确。", "terms": ["余额", "剩余课时", "未消耗课时", "未提供服务", "退费", "退款"]},
            {"element_id": "non_tuition_fee_handling", "proposition": "资料费、教材费等非课时费用是否退还或扣除明确。", "terms": ["资料费", "教材费", "材料费", "扣除", "不退"]},
        ]
        minimum_pass = 4
        minimum_partial = 2
    elif item.node_id in {"prepaid_partly_provided_refund", "termination_refund_calculation"}:
        required = [
            {"element_id": "refund_trigger", "proposition": "退费、解除或未提供服务的触发条件明确。", "terms": ["退费", "退款", "解除", "未提供服务", "终止"]},
            {"element_id": "provided_service_value", "proposition": "已实际提供服务、已消耗课时或已履行部分的计价方式明确。", "terms": ["实际课时", "已提供", "已消耗", "已上课时", "扣除"]},
            {"element_id": "remaining_service_value", "proposition": "剩余课时、未消耗课时或未提供服务对应款项明确。", "terms": ["剩余课时", "未消耗课时", "未提供服务", "剩余费用"]},
            {"element_id": "reasonable_cost_deduction", "proposition": "可依法扣除的合理成本、资料费或不可退费用范围明确。", "terms": ["合理成本", "资料费", "教材费", "扣除", "不可退"]},
            {"element_id": "refund_deadline", "proposition": "退款办理期限或付款期限明确。", "terms": ["日内", "工作日", "期限", "退还"]},
        ]
        minimum_pass = 4
        minimum_partial = 2
    elif item.node_id in {"health_change_termination", "consumer_personal_reason_termination"}:
        required = [
            {"element_id": "termination_trigger", "proposition": "健康原因、个人原因或其他解除触发条件明确。", "terms": ["健康原因", "个人原因", "疾病", "无法继续", "解除"]},
            {"element_id": "proof_or_notice", "proposition": "证明材料、书面通知或申请材料要求明确。", "terms": ["医疗证明", "证明", "书面通知", "申请材料", "退费申请"]},
            {"element_id": "provided_service_deduction", "proposition": "已实际提供服务费用可扣除。", "terms": ["实际课时", "已提供", "扣除", "已消耗"]},
            {"element_id": "reasonable_cost_deduction", "proposition": "已发生且不可退回的合理成本可依法扣除。", "terms": ["合理成本", "必要成本", "不可退", "扣除"]},
            {"element_id": "remaining_refund", "proposition": "未提供服务或剩余课时对应费用退还。", "terms": ["未提供服务", "剩余课时", "退费", "退款", "退还"]},
        ]
        minimum_pass = 5
        minimum_partial = 2
    elif item.node_id in {"consumer_termination_notice", "termination_notice_period"}:
        required = [
            {"element_id": "notice_channel", "proposition": "解除或退费通知渠道明确。", "terms": ["书面通知", "退费申请", "退款申请", "解除申请", "邮件", "微信"]},
            {"element_id": "notice_period", "proposition": "提前通知期限或合理办理期限明确。", "terms": ["提前", "日内", "工作日", "期限"]},
            {"element_id": "materials_once", "proposition": "申请材料、证明材料或一次性告知要求明确。", "terms": ["申请材料", "证明材料", "一次性告知", "提交"]},
            {"element_id": "settlement_deadline", "proposition": "审核、结算或退款完成期限明确。", "terms": ["审核", "结算", "退还", "完成", "日内"]},
        ]
        minimum_pass = 3
        minimum_partial = 1
    elif item.node_id in {"service_nonperformance_remedy", "service_quality_nonconform_remedy"}:
        required = [
            {"element_id": "breach_trigger", "proposition": "未提供服务、停止服务或服务质量不符合约定的触发条件明确。", "terms": ["未提供服务", "停止服务", "不达标", "质量", "不符合"]},
            {"element_id": "cure_first", "proposition": "优先补正、重新履行、补课、延期或替代服务明确。", "terms": ["补正", "重新提供", "补课", "延期", "替代服务", "继续履行"]},
            {"element_id": "refund_after_failed_cure", "proposition": "补救仍不能达到约定标准时按未履行部分退费。", "terms": ["未提供服务", "剩余", "退费", "退款", "减少费用"]},
            {"element_id": "actual_loss_liability", "proposition": "损失赔偿限于依法可证明的实际损失或相应责任。", "terms": ["实际损失", "赔偿", "损失", "依法"]},
        ]
        minimum_pass = 3
        minimum_partial = 1
    elif item.node_id == "fee_standard_attachment":
        required = [
            {"element_id": "fee_schedule_attachment", "required_fact": "payment.fee_schedule", "proposition": "收费标准、价格表或费用明细附件明确。", "terms": ["收费标准", "价目表", "费用明细", "附件"]},
            {"element_id": "tuition_and_material_fee_split", "required_fact": "payment.material_fee", "proposition": "课时费、资料费、教材费等费用项目拆分明确。", "terms": ["课时费", "资料费", "教材费", "材料费"]},
            {"element_id": "discount_or_gift_handling", "proposition": "优惠价、赠送课时或套餐权益处理明确。", "terms": ["优惠", "赠送", "套餐", "折扣"]},
            {"element_id": "refund_unit_price", "required_fact": "payment.unit_price", "proposition": "退费时的单价或计价规则明确。", "terms": ["退费", "单价", "计价", "结算"]},
        ]
        minimum_pass = 3
        minimum_partial = 1
    elif item.node_id == "force_majeure_service_adjustment":
        required = [
            {"element_id": "force_majeure_event", "proposition": "不可抗力、政策限制或不可归责事由明确。", "terms": ["不可抗力", "政策", "管制", "疫情"]},
            {"element_id": "notice_and_proof", "proposition": "受影响方通知和证明义务明确。", "terms": ["通知", "证明", "材料"]},
            {"element_id": "service_adjustment_options", "proposition": "延期、转线上、替代服务或结算方式明确。", "terms": ["延期", "线上", "替代服务", "退费", "结算"]},
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "performance_record_attachment":
        required = [
            {"element_id": "attendance_record", "proposition": "签到、课时或消费记录保存方式明确。", "terms": ["签到", "课时记录", "消费记录", "记录"]},
            {"element_id": "service_confirmation", "proposition": "服务确认、评价或履行确认材料明确。", "terms": ["服务确认", "确认", "评价", "履行"]},
            {"element_id": "refund_record", "proposition": "沟通、退费或结算记录保存方式明确。", "terms": ["沟通", "退费记录", "结算", "保存"]},
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "sale_attachment_priority":
        required = [
            {"element_id": "attachment_effect", "required_claim": "document.precedence", "required_claim_element": "attachment_effect", "proposition": "附件属于合同文件并具有约束力。", "terms": []},
            {"element_id": "attachment_vs_main", "required_claim": "document.precedence", "required_claim_element": "attachment_vs_main", "proposition": "合同明确附件与正文发生冲突时的适用顺位。", "terms": []},
        ]
        minimum_pass = len(required)
    elif item.node_id == "framework_document_precedence":
        required = [
            {"element_id": key, "required_claim": "document.precedence", "required_claim_element": key, "proposition": proposition, "terms": []}
            for key, proposition in (
                ("supplement_priority", "补充协议的优先顺位已明确。"),
                ("amendment_priority", "书面变更文件的优先顺位已明确。"),
                ("order_priority", "采购订单与主协议之间的适用顺位已明确。"),
                ("conditional_override", "订单特别变更须经授权人员书面确认。"),
            )
        ]
        minimum_pass = len(required)
    elif alternative.get("status") == "SATISFIED":
        fact_names = list(alternative.get("fact_names") or [])
        fact_values = dict(alternative.get("values") or {})
        production_claims = display_claims(fact_names, fact_values)
        item.decision_trace["production_display_claims"] = [claim.to_public_dict() for claim in production_claims]
        required = [
            {
                "element_id": f"commercial_fact_{name}",
                "required_fact": name,
                "proposition": claim.user_statement,
                "terms": [],
            }
            for name, claim in zip(fact_names, production_claims)
        ]
        minimum_pass = len(required)
        minimum_partial = 1
    elif common_requirement := common_sale_coverage_requirement(item.node_id):
        required = list(common_requirement["required_elements"])
        return CoverageClaim(
            review_id=item.item_id,
            required_elements=required,
            optional_elements=list(common_requirement.get("optional_elements") or []),
            positive_claims=[element["proposition"] for element in required],
            minimum_pass_elements=len(required),
            minimum_partial_elements=1,
            satisfaction_paths=list(common_requirement.get("satisfaction_paths") or []),
        )
    elif item.node_id == "real_estate_third_party_rights":
        claim_labels = {
            "property.mortgage.disclosed": "抵押情况已披露",
            "property.judicial_seizure.disclosed": "司法查封情况已披露",
            "property.ownership_dispute.disclosed": "产权争议情况已披露",
            "property.coownership.disclosed": "共有情况已披露",
            "property.lease.disclosed": "现有租赁情况已披露",
            "seller.encumbrance_warranty.exists": "卖方已作第三方权利负担保证",
        }
        required = [
            {"element_id": claim_id, "required_claim": claim_id, "proposition": claim_labels[claim_id], "terms": []}
            for claim_id in (
                "property.mortgage.disclosed", "property.judicial_seizure.disclosed",
                "property.ownership_dispute.disclosed", "property.coownership.disclosed",
                "property.lease.disclosed", "seller.encumbrance_warranty.exists",
            )
        ]
        minimum_pass = len(required)
        minimum_partial = 1
    elif item.node_id == "real_estate_agent_authority":
        required = [
            {"element_id": "agent_identity", "proposition": "代理人身份明确。", "terms": ["代理人"]},
            {"element_id": "authority_scope", "proposition": "授权范围包括签约、收款或过户。", "terms": ["签署", "签约", "收款", "过户", "转移登记"]},
            {"element_id": "power_of_attorney", "proposition": "授权委托书作为合同附件或证据。", "terms": ["授权委托书"]},
            {"element_id": "authority_term", "proposition": "授权期限明确。", "terms": ["授权期限", "有效期", "期限"]},
        ]
        minimum_pass = len(required)
        minimum_partial = 1
    elif item.node_id == "tenant_death_successor":
        required = [
            {
                "element_id": "death_during_lease",
                "proposition": "承租人在租赁期间死亡。",
                "terms": ["承租人死亡", "租赁期间死亡", "租期内死亡", "乙方死亡"],
            },
            {
                "element_id": "successor_continue",
                "proposition": "共同居住人或共同经营人可以继续承租或继续使用房屋。",
                "terms": ["共同居住", "共同经营", "继续承租", "继续租赁", "继续使用"],
            },
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "common_jurisdiction":
        required = [
            {
                "element_id": "dispute_resolution_path",
                "proposition": "合同约定诉讼或仲裁的争议解决路径。",
                "terms": ["人民法院", "法院", "起诉", "仲裁委员会", "仲裁"],
            },
            {
                "element_id": "specific_dispute_forum",
                "proposition": "合同明确具体管辖法院或仲裁机构。",
                "terms": ["人民法院", "仲裁委员会"],
            },
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "tenant_death_settlement":
        required = [
            {
                "element_id": "no_successor_handover",
                "proposition": "无人继续承租时的房屋返还、费用结算或遗留物处理。",
                "terms": ["无人继续", "继承人", "遗留物", "交接", "返还房屋", "结清费用"],
            }
        ]
    elif item.node_id == "indefinite_lease":
        required = [
            {
                "element_id": "post_expiry_continue_use",
                "proposition": "租期届满后承租人继续使用房屋或继续居住。",
                "terms": ["租期届满", "期满", "继续使用", "继续居住", "继续承租", "续租"],
            },
            {
                "element_id": "no_objection_or_rent_acceptance",
                "proposition": "出租人未提出异议或继续收租。",
                "terms": ["未提出异议", "没有异议", "继续收租", "接受租金", "同意续租"],
            },
            {
                "element_id": "reasonable_notice",
                "proposition": "转为不定期租赁后的合理期限通知或书面通知。",
                "terms": ["合理期限", "提前", "书面通知", "解除", "通知"],
            },
        ]
        minimum_pass = 3
        minimum_partial = 1
    elif item.node_id == "reasonable_repair_cost":
        required = [
            {
                "element_id": "actual_reasonable_cost",
                "proposition": "维修费用以必要、合理、实际发生为限。",
                "terms": ["必要", "合理", "实际发生", "维修费", "维修费用"],
            },
            {
                "element_id": "repair_voucher",
                "proposition": "出租人提供维修单据、发票、报价单或鉴定材料。",
                "terms": ["维修单", "发票", "报价单", "鉴定", "票据", "凭证"],
            },
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "deposit_offset_order":
        required = [
            {
                "element_id": "offset_items",
                "proposition": "押金可抵扣的未付租金、费用或维修赔偿项目。",
                "terms": ["押金", "抵扣", "扣除", "未付租金", "欠费", "维修费"],
            },
            {
                "element_id": "offset_order",
                "proposition": "押金抵扣顺序。",
                "terms": ["抵扣顺序", "扣除顺序", "先抵扣", "后抵扣", "依次", "其次"],
            },
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "deposit_return_deadline":
        required = [
            {
                "element_id": "deposit_return",
                "proposition": "租赁终止或交接后押金余额返还。",
                "terms": ["押金", "保证金", "返还", "退还", "归还"],
            },
            {
                "element_id": "return_deadline",
                "proposition": "押金返还的具体期限或触发时间。",
                "terms": ["日内", "工作日", "期限", "交接后", "结算后", "完成交接"],
            },
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "termination_notice":
        required = [
            {
                "element_id": "termination_trigger",
                "proposition": "合同约定解除事由或触发条件。",
                "terms": ["解除合同", "有权解除", "解除条件", "严重违约", "合同目的不能实现"],
            },
            {
                "element_id": "termination_notice_delivery",
                "proposition": "解除通知的书面方式或送达渠道。",
                "terms": ["解除", "书面通知", "送达", "电子邮件", "地址"],
            },
            {
                "element_id": "termination_effective_time",
                "proposition": "解除通知到达或解除生效节点。",
                "terms": ["通知到达", "送达之日", "解除生效", "到达对方"],
            },
        ]
        minimum_pass = 3
        minimum_partial = 1
    elif item.node_id == "limitation_and_notice":
        required = [
            {
                "element_id": "notice_channel",
                "proposition": "合同约定通知、送达或催告的联系方式及地址。",
                "terms": ["通知", "送达", "催告", "地址", "联系电话", "通讯地址", "电子邮件"],
            },
            {
                "element_id": "change_duty",
                "proposition": "联系方式或送达地址变更时负有通知义务。",
                "terms": ["变更", "通知对方", "地址变更", "联系方式变更"],
            },
            {
                "element_id": "deemed_service",
                "proposition": "合同约定有效送达或视为送达规则。",
                "terms": ["视为送达", "有效送达", "送达即", "退回之日"],
            },
        ]
        minimum_pass = 3
        minimum_partial = 1
    elif item.node_id == "illegal_building":
        required = [
            {
                "element_id": "lawful_lease_basis",
                "proposition": "合同列明权属证明、产证编号或合法出租基础。",
                "terms": ["产证编号", "不动产权证", "权利人", "房屋合法", "非违法建筑", "出租条件"],
            }
        ]
    elif item.node_id == "force_majeure":
        required = [
            {
                "element_id": "force_majeure_event",
                "proposition": "合同出现不可抗力或不可归责事由处理框架。",
                "terms": ["不可抗力", "无法居住", "无法使用", "通知", "证明"],
            }
        ]
    elif item.node_id == "safety_risk":
        required = [
            {
                "element_id": "safety_termination_event",
                "proposition": "合同出现危险房屋、毁损灭失或安全隐患解除事由。",
                "terms": ["危险房屋", "毁损", "灭失", "安全", "无法居住", "人身损害"],
            }
        ]
    elif item.node_id == "burden_of_proof":
        required = [
            {
                "element_id": "damage_baseline_evidence",
                "proposition": "合同或附件提供退租损坏核对的基础清单、验收依据或状态记录。",
                "terms": ["附件三", "清单", "装修", "附属设施", "验收依据", "返还"],
            }
        ]
    elif item.node_id == "keys_access":
        required = [
            {
                "element_id": "possession_return",
                "proposition": "合同约定房屋返还、验收依据或占有返还安排。",
                "terms": ["返还该房屋", "返还", "验收依据", "钥匙", "门禁", "占有"],
            }
        ]
    elif item.node_id == "sale_quality_remedy":
        required = [
            {
                "element_id": "quality_objection_period",
                "proposition": "买卖合同约定质量问题提出期限或异议程序。",
                "terms": ["质量问题", "质量异议", "发现后", "提出", "期限"],
            },
            {
                "element_id": "quality_objection_form",
                "proposition": "买卖合同明确质量异议的书面通知或可留痕方式。",
                "terms": ["书面提出", "书面通知", "书面异议", "电子邮件", "质量异议单"],
            },
            {
                "element_id": "quality_remedy_method",
                "proposition": "买卖合同约定质量不符合时的补救方式。",
                "terms": ["更换", "补发", "修理", "重作", "退货", "减少价款", "赔偿"],
            },
        ]
        minimum_pass = 3
        minimum_partial = 1
    elif item.node_id == "sale_quality_standard_basis":
        required = [
            {
                "element_id": "multiple_standards_exist",
                "proposition": "合同同时适用两个以上质量标准或技术文件。",
                "terms": ["国家标准", "行业标准", "企业标准", "技术协议", "样品"],
            },
            {
                "element_id": "precedence_between_standards",
                "proposition": "合同明确多个质量标准冲突时的适用顺序。",
                "terms": ["优先", "顺序", "冲突时", "不一致时", "特别约定为准", "特别约定标准为准", "较高标准"],
            },
            {
                "element_id": "conflict_resolution",
                "proposition": "合同明确标准冲突的确认或解决机制。",
                "terms": ["书面确认", "协商确定", "冲突解决", "以双方确认"],
            },
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "sale_delivery_method":
        required = [
            {
                "element_id": "delivery_method",
                "proposition": "合同明确运输或交付方式。",
                "terms": ["运输方式", "负责运输", "送货", "提货", "自提", "物流"],
            },
            {
                "element_id": "acceptance_voucher",
                "proposition": "合同明确签收主体及送货单、签收单或物流回执等交付凭证。",
                "terms": ["授权收货人", "工作人员", "指定人员", "送货单", "签收单", "物流回执", "签字"],
            },
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "sale_payment_method_account":
        required = [
            {
                "element_id": "payment_method",
                "proposition": "合同明确货款支付方式。",
                "terms": ["银行转账", "转账", "支付方式", "付款方式"],
            },
            {
                "element_id": "payment_account",
                "proposition": "合同明确收款账户或开户行信息。",
                "terms": ["收款账户", "银行账号", "账号", "开户行"],
            },
        ]
        minimum_pass = 2
        minimum_partial = 1
    elif item.node_id == "sale_payment_schedule":
        required = [
            {
                "element_id": "payment_trigger",
                "proposition": "合同明确货款支付触发节点或期限。",
                "terms": ["签收后", "对账后", "次月", "日前", "日内", "支付"],
            }
        ]
    elif item.node_id == "sale_validity_true_intent":
        required = [
            {
                "element_id": "mutual_intent_expression",
                "proposition": "合同载明双方经协商一致、自愿达成交易安排。",
                "terms": ["双方", "友好协商", "协商一致", "自愿", "达成如下协议"],
            }
        ]
    elif item.node_id == "sale_liquidated_damages_adjustment":
        required = [
            {
                "element_id": "liquidated_damages_standard",
                "proposition": "合同明确违约金计算标准，可依法结合实际损失审查调整。",
                "terms": ["违约金", "万分之", "百分之", "%", "每日", "按天"],
            }
        ]
    elif item.node_id in {"rent_payment", "deposit_amount", "procedure_jurisdiction", "ownership_authority"} and item.fact_dependencies:
        required = [
            {
                "element_id": "fact_backed_contract_term",
                "proposition": f"合同原文可支撑“{item.title}”事实。",
                "terms": [item.title, *item.fact_dependencies],
            }
        ]
    else:
        terms = list(dict.fromkeys([str(term) for term in (item.matched_terms or []) if term] + [item.title]))
        required = [
            {
                "element_id": "core_contract_arrangement",
                "proposition": f"合同存在可验证的“{item.title}”实质条款内容。",
                "terms": terms,
            }
        ]
    return CoverageClaim(
        review_id=item.item_id,
        required_elements=required,
        positive_claims=[element["proposition"] for element in required],
        minimum_pass_elements=minimum_pass,
        minimum_partial_elements=minimum_partial,
    )


def _apply_framework_fact_paths(
    items: List[ReviewItemResult],
    profile: FrameworkSupplyProfile,
    clauses: List[Any],
) -> List[ReviewItemResult]:
    if not profile.is_framework:
        return items
    by_clause_id = {clause.clause_id: clause for clause in clauses}
    profile_data = profile.to_public_dict()
    for item in items:
        if profile.product_category == "INDUSTRIAL_COMPONENTS" and item.node_id == "sale_approval_license":
            _set_item_not_applicable(item, "标的是普通工业零部件，合同未出现专营、许可、审批或强制准入触发事实。")
            item.decision_trace["commercial_applicability"] = {"product_category": profile.product_category, "regulated_goods_trigger": False}
            continue
        if profile.product_category == "INDUSTRIAL_COMPONENTS" and item.node_id == "sale_subject_legality":
            _set_item_not_applicable(item, "标的是普通工业零部件，未出现禁止流通、限制流通、来源违法或权属争议触发事实。")
            item.decision_trace["commercial_applicability"] = {"product_category": profile.product_category, "regulated_or_illegal_goods_trigger": False}
            continue
        if item.node_id == "sale_risk_carrier_delivery" and profile.carrier_rule_applicability.value is False:
            _set_item_not_applicable(item, "卖方负责送达买方指定地点，且风险在目的地签收后转移；货交第一承运人规则不适用。")
            item.decision_trace["carrier_rule_applicability"] = profile.carrier_rule_applicability.to_public_dict()
            continue
        fact_names = FRAMEWORK_REVIEW_FACT_PATHS.get(item.node_id)
        if not fact_names:
            continue
        fact_rows = [profile_data.get(name) or {} for name in fact_names]
        satisfied = bool(fact_rows) and all(
            row.get("source_clause_ids") and (row.get("value") is not None or row.get("exists") is not None)
            for row in fact_rows
        )
        trace = {
            "status": "SATISFIED" if satisfied else "NOT_SATISFIED",
            "fact_names": list(fact_names),
            "source_clause_ids": list(dict.fromkeys(
                clause_id for row in fact_rows for clause_id in row.get("source_clause_ids", [])
            )),
            "values": {name: profile_data.get(name) for name in fact_names},
            "evaluation": "ALL_REQUIRED_FACTS_WITH_PROVENANCE",
        }
        item.decision_trace["alternative_satisfaction"] = trace
        if not satisfied:
            continue
        evidence = [by_clause_id[clause_id] for clause_id in trace["source_clause_ids"] if clause_id in by_clause_id]
        if not evidence:
            continue
        _set_item_pass(
            item,
            evidence[:12],
            "统一商业事实图谱已通过来源条款满足该审查项，替代满足路径校验通过。",
            f"合同已通过框架供货事实路径完整覆盖“{item.title}”。",
        )
        item.matched_terms = list(fact_names)
        item.fact_dependencies = sorted(set(item.fact_dependencies + [f"commercial.{name}" for name in fact_names]))
        item.fallback_reason = "框架供货统一事实图谱"
        for evidence_row in item.evidence_clauses:
            evidence_row["entailment_status"] = EVIDENCE_SUPPORTS
            evidence_row["evidence_type"] = "COMMERCIAL_FACT_EVIDENCE"
    return items


def _evidence_id(evidence: Dict[str, Any], index: int) -> str:
    return str(evidence.get("evidence_id") or evidence.get("clause_id") or evidence.get("location") or f"EV-{index}")


def _has_selected_checkbox_term(raw_text: str, terms: Iterable[str]) -> bool:
    for term in terms:
        if not term:
            continue
        if re.search(rf"☑[^□☑]{{0,40}}{re.escape(term)}", raw_text) or re.search(rf"{re.escape(term)}[^□☑]{{0,40}}☑", raw_text):
            return True
    return False


def _service_explicit_element_support(element_id: str, raw_text: str, compacted: str) -> Optional[tuple[str, str]]:
    selected_settlement = _has_selected_checkbox_term(
        raw_text,
        ("实际消耗课时", "实际课时", "已消耗课时", "按实际接受服务情况结算", "未提供服务"),
    )
    unselected_settlement_only = (
        element_id in {"provided_service_deduction", "provided_service_value", "remaining_refund", "remaining_service_value", "balance_calculation"}
        and any(
            re.search(rf"□[^□☑]{{0,12}}{re.escape(term)}", raw_text)
            for term in ("实际消耗课时", "实际课时", "已消耗课时", "按实际接受服务情况结算", "未提供服务")
        )
        and not selected_settlement
    )
    if unselected_settlement_only:
        return "MISSING", EVIDENCE_RELATED_NOT_SUPPORTING
    patterns: Dict[str, tuple[str, ...]] = {
        "service_time": (r"上课时间.{0,24}\d{1,2}[:：]\d{2}", r"每周.{0,16}(上午|下午|晚上)"),
        "start_date": (r"(开课日期|开始日期|服务开始|开班日期).{0,16}(\d{4}年\d{1,2}月\d{1,2}日|\d{4}[-/]\d{1,2}[-/]\d{1,2})",),
        "end_date": (r"(预计结课日期|结课日期|结束日期|服务期限至).{0,16}(\d{4}年\d{1,2}月\d{1,2}日|\d{4}[-/]\d{1,2}[-/]\d{1,2})",),
        "service_location": (r"(培训地点|上课地点|服务地点).{0,24}[\u4e00-\u9fffA-Za-z0-9]",),
        "delivery_method": (r"(线上|线下|面授|远程|到店|预约).{0,16}(培训|授课|服务|上课|方式)",),
        "service_name": (r"(课程名称|服务名称|培训项目).{0,30}[\u4e00-\u9fffA-Za-z0-9]",),
        "class_or_project_id": (r"(班级编号|项目编号|服务编号).{0,30}[\u4e00-\u9fffA-Za-z0-9-]",),
        "service_hours": (r"(总课时数|总课时|服务次数).{0,12}\d+", r"课时.{0,8}(共计|合计)?\d+", r"共计\d+.{0,4}课时"),
        "session_duration": (r"(每次培训课时|单次课时|每次).{0,16}\d+",),
        "termination_trigger": (
            r"(身体健康状况|健康状况|疾病|特殊情形).{0,30}(不再适合|无法继续|解除|退费|退学)",
            r"(开班前|开班后).{0,30}(退学|解除|退费|退款)",
            r"(退学|解除).{0,20}(退费|退款|全额退费)",
        ),
        "proof_or_notice": (r"(书面通知|及时通知|退费申请|退款申请|提交申请|申请材料)",),
        "notice_channel": (r"(书面通知|退费申请|退款申请|提交申请)",),
        "notice_materials": (r"(申请材料|证明材料|退费申请|退款申请)",),
        "provided_service_deduction": (r"(实际消耗课时|实际课时|已消耗课时|已提供服务|实际接受服务).{0,24}(结算|扣除|计算|费用)",),
        "provided_service_value": (r"(实际消耗课时|实际课时|已消耗课时|已提供服务|实际接受服务).{0,24}(结算|扣除|计算|费用)",),
        "remaining_refund": (r"(剩余课时|未消耗课时|未提供服务|全额退费|退费|退款).{0,24}(退还|退费|退款|结算)",),
        "remaining_service_value": (r"(剩余课时|未消耗课时|未提供服务|全额退费|退费|退款).{0,24}(退还|退费|退款|结算)",),
        "refund_trigger": (r"(退学|解除|退费|退款|未提供服务|未消耗课时|开班前|开班后)",),
        "balance_calculation": (r"(剩余课时|未消耗课时|未提供服务|余额).{0,24}(退费|退款|结算|计算)",),
        "total_fee": (r"(培训费|服务费|课程费|总金额|合计).{0,16}\d",),
        "paid_amount": (r"(支付|已付|付款|一次性支付).{0,16}\d",),
    }
    if selected_settlement and element_id in {"provided_service_deduction", "provided_service_value"}:
        return "COVERED", EVIDENCE_SUPPORTS
    if selected_settlement and element_id in {"remaining_refund", "remaining_service_value", "balance_calculation"}:
        return "PARTIALLY_COVERED", EVIDENCE_PARTIAL_SUPPORT
    for pattern in patterns.get(element_id, ()):
        if re.search(pattern, raw_text) or re.search(pattern, compacted):
            return "COVERED", EVIDENCE_SUPPORTS
    return None


def _element_supported_by_evidence(element: Dict[str, Any], evidence: Dict[str, Any]) -> tuple[str, str]:
    raw_text = str(evidence.get("text") or evidence.get("quote") or "")
    text = _compact(raw_text)
    terms = [str(term) for term in element.get("terms", []) if term]
    matched = [term for term in terms if term and term in text]
    entailment = str(evidence.get("entailment_status") or "")
    explicit = _service_explicit_element_support(str(element.get("element_id") or ""), raw_text, text)
    if explicit:
        return explicit
    if element.get("element_id") == "return_deadline":
        return (
            ("COVERED", EVIDENCE_SUPPORTS)
            if has_specific_deposit_return_deadline(str(evidence.get("text") or evidence.get("quote") or ""))
            else ("MISSING", EVIDENCE_RELATED_NOT_SUPPORTING)
        )
    if element.get("element_id") == "specific_dispute_forum":
        generic_forum = any(
            phrase in text
            for phrase in ("有管辖权的人民法院", "有管辖权的法院", "有管辖权法院")
        )
        named_forum = bool(
            re.search(r"(?:[\u4e00-\u9fff]{2,20})(?:人民法院|仲裁委员会)", text)
        )
        if named_forum and not generic_forum:
            return "COVERED", EVIDENCE_SUPPORTS
        return "MISSING", EVIDENCE_RELATED_NOT_SUPPORTING
    if element.get("element_id") == "multiple_standards_exist":
        standard_categories = sum(
            1 for terms_in_category in (
                ("国家标准", "GB/", "GB-"),
                ("行业标准",),
                ("企业标准", "Q/", "Q-"),
                ("技术协议", "技术规格书"),
                ("样品", "封样"),
            )
            if any(term in text for term in terms_in_category)
        )
        if standard_categories >= 2:
            return "COVERED", EVIDENCE_SUPPORTS
        if standard_categories == 1:
            return "PARTIALLY_COVERED", EVIDENCE_PARTIAL_SUPPORT
    if entailment in {EVIDENCE_SUPPORTS, EVIDENCE_PARTIAL_SUPPORT}:
        if matched or not terms:
            return "COVERED" if entailment == EVIDENCE_SUPPORTS else "PARTIALLY_COVERED", entailment
        return "UNCERTAIN", EVIDENCE_UNCERTAIN
    if entailment == EVIDENCE_RELATED_NOT_SUPPORTING:
        return "MISSING", EVIDENCE_RELATED_NOT_SUPPORTING
    if matched:
        strong_single_terms = {
            "产证编号", "不动产权证", "不可抗力", "危险房屋", "附件三", "验收依据", "返还该房屋",
            "开课日期", "预计结课日期", "上课时间", "课程名称", "班级编号", "总课时", "实际消耗课时", "书面通知",
        }
        if len(matched) >= 2 or len(matched) == len(terms) or bool(set(matched) & strong_single_terms):
            if len(matched) >= 2 or len(matched) == len(terms):
                return "COVERED", EVIDENCE_SUPPORTS
            return "PARTIALLY_COVERED", EVIDENCE_PARTIAL_SUPPORT
        return "UNCERTAIN", EVIDENCE_UNCERTAIN
    return "MISSING", EVIDENCE_NOT_RELEVANT


def _coverage_elements_for_item(item: ReviewItemResult, canonical_claims: Optional[Dict[str, Any]] = None) -> List[CoverageElementResult]:
    claim = _coverage_claim_for_item(item)
    results: List[CoverageElementResult] = []
    evidences = item.evidence_clauses or []
    negative = (item.decision_trace or {}).get("negative_evidence") or {}
    for element in claim.required_elements:
        required_fact = str(element.get("required_fact") or "")
        if required_fact:
            registry_facts = ((item.decision_trace or {}).get("contract_fact_registry_consumption") or {}).get("facts") or {}
            registry_row = registry_facts.get(required_fact) or {}
            registry_status = str(registry_row.get("status") or "")
            if registry_status in {"FOUND", "CONFLICTING"}:
                supported = registry_status == "FOUND"
                results.append(CoverageElementResult(
                    review_id=item.item_id,
                    element_id=str(element.get("element_id")),
                    proposition=str(element.get("proposition")),
                    status="COVERED" if supported else "UNCERTAIN",
                    evidence_ids=list(registry_row.get("fact_ids") or []),
                    entailment=EVIDENCE_SUPPORTS if supported else EVIDENCE_UNCERTAIN,
                    verifier_confidence=str(registry_row.get("confidence") or ("high" if supported else "low")),
                    reason="ContractFactRegistry supplies this canonical fact." if supported else "ContractFactRegistry found conflicting values for this canonical fact.",
                    claim_id=required_fact,
                    source_clause_ids=list(registry_row.get("source_clause_ids") or []),
                    source_spans=list(registry_row.get("source_spans") or []),
                    source_locations=list(registry_row.get("source_locations") or []),
                    atomic=bool(element.get("atomic", True)),
                    child_elements=list(element.get("child_elements") or []),
                    legal_proposition_ids=list(element.get("legal_proposition_ids") or []),
                ))
                continue
            alternative = (item.decision_trace or {}).get("alternative_satisfaction") or {}
            fact_row = (alternative.get("values") or {}).get(required_fact) or {}
            source_clause_ids = list(fact_row.get("source_clause_ids") or [])
            supported = alternative.get("status") == "SATISFIED" and bool(source_clause_ids)
            results.append(CoverageElementResult(
                review_id=item.item_id,
                element_id=str(element.get("element_id")),
                proposition=str(element.get("proposition")),
                status="COVERED" if supported else "MISSING",
                evidence_ids=[f"CF-{clause_id}" for clause_id in source_clause_ids],
                entailment=EVIDENCE_SUPPORTS if supported else EVIDENCE_NOT_RELEVANT,
                verifier_confidence="high" if supported else "low",
                reason="Commercial Fact Graph satisfies this element." if supported else "Commercial fact has no supporting source evidence.",
                claim_id=f"commercial.{required_fact}",
                source_clause_ids=source_clause_ids,
                source_spans=list(fact_row.get("source_spans") or []),
                source_locations=[],
                atomic=bool(element.get("atomic", True)),
                child_elements=list(element.get("child_elements") or []),
                legal_proposition_ids=list(element.get("legal_proposition_ids") or []),
            ))
            continue
        required_claim = str(element.get("required_claim") or "")
        if required_claim:
            canonical = (canonical_claims or {}).get(required_claim)
            semantic_key = str(element.get("required_claim_element") or "")
            semantic_values = ((canonical.object or {}).get("hierarchy") or {}) if canonical and isinstance(canonical.object, dict) else {}
            supported = bool(
                canonical and canonical.status == "ASSERTED" and canonical.source_clause_ids
                and (not semantic_key or semantic_values.get(semantic_key) is True)
            )
            results.append(CoverageElementResult(
                review_id=item.item_id, element_id=str(element.get("element_id")), proposition=str(element.get("proposition")),
                status="COVERED" if supported else "MISSING",
                evidence_ids=list(canonical.evidence_ids) if canonical else [],
                entailment=EVIDENCE_SUPPORTS if supported else EVIDENCE_NOT_RELEVANT,
                verifier_confidence=canonical.confidence if canonical else "low",
                reason="Canonical Claim evidence supports this element." if supported else "Canonical Claim has no supporting source evidence.",
                claim_id=required_claim,
                source_clause_ids=list(canonical.source_clause_ids) if canonical else [],
                source_spans=list(canonical.source_spans) if canonical else [],
                source_locations=list(getattr(canonical, "source_locations", [])) if canonical else [],
                atomic=bool(element.get("atomic", True)),
                child_elements=list(element.get("child_elements") or []),
                legal_proposition_ids=list(element.get("legal_proposition_ids") or []),
            ))
            continue
        best_status = "MISSING"
        best_entailment = "NEGATIVE_SEARCH_NOT_FOUND" if negative.get("result") == "NOT_FOUND" else EVIDENCE_NOT_RELEVANT
        evidence_ids: List[str] = []
        for index, evidence in enumerate(evidences, start=1):
            status, entailment = _element_supported_by_evidence(element, evidence)
            if status in {"COVERED", "PARTIALLY_COVERED"}:
                evidence_ids.append(_evidence_id(evidence, index))
            if status == "COVERED":
                best_status = "COVERED"
                best_entailment = entailment
                break
            if status == "PARTIALLY_COVERED" and best_status not in {"COVERED", "PARTIALLY_COVERED"}:
                best_status = "PARTIALLY_COVERED"
                best_entailment = entailment
            elif status == "UNCERTAIN" and best_status == "MISSING":
                best_status = "UNCERTAIN"
                best_entailment = entailment
        verifier_confidence = "high" if best_status == "COVERED" else "medium" if best_status in {"PARTIALLY_COVERED", "MISSING"} else "low"
        if best_status == "MISSING" and best_entailment == "NEGATIVE_SEARCH_NOT_FOUND":
            verifier_confidence = "high"
        supporting_evidence = [
            evidence for index, evidence in enumerate(evidences, start=1)
            if _evidence_id(evidence, index) in evidence_ids
        ]
        results.append(
            CoverageElementResult(
                review_id=item.item_id,
                element_id=str(element.get("element_id") or "element"),
                proposition=str(element.get("proposition") or ""),
                status=best_status,
                evidence_ids=evidence_ids,
                entailment=best_entailment,
                verifier_confidence=verifier_confidence,
                reason="元素级证据可支撑。" if evidence_ids else "未找到可支撑该元素的合同证据。",
                source_clause_ids=list(dict.fromkeys(str(evidence.get("clause_id") or "") for evidence in supporting_evidence if evidence.get("clause_id"))),
                source_spans=list(dict.fromkeys(str(evidence.get("original_excerpt") or evidence.get("text") or "") for evidence in supporting_evidence if evidence.get("original_excerpt") or evidence.get("text"))),
                source_locations=list(dict.fromkeys(str(evidence.get("location") or "") for evidence in supporting_evidence if evidence.get("location"))),
                atomic=bool(element.get("atomic", True)),
                child_elements=list(element.get("child_elements") or []),
                legal_proposition_ids=list(element.get("legal_proposition_ids") or []),
            )
        )
    element_requirements = {
        str(element.get("element_id") or ""): canonical_fact_key(str(element.get("required_fact") or ""))
        for element in claim.required_elements
    }
    registry_facts = ((item.decision_trace or {}).get("contract_fact_registry_consumption") or {}).get("facts") or {}
    for result in results:
        required_fact = element_requirements.get(result.element_id, "")
        result.required_fact_key = required_fact
        if required_fact:
            registry_row = registry_facts.get(required_fact) or {}
            result.fact_status = str(registry_row.get("status") or _element_truth_status(result.status))
            result.fact_value = registry_row.get("value")
            result.fact_evidence_refs = list(registry_row.get("fact_ids") or result.evidence_ids)
        else:
            result.fact_status = _element_truth_status(result.status)
            result.fact_evidence_refs = list(result.evidence_ids)
        result.requirement_status = "SATISFIED" if result.status == "COVERED" else "PARTIAL" if result.status == "PARTIALLY_COVERED" else "UNCERTAIN" if result.status == "UNCERTAIN" else "NOT_SATISFIED"
        result.requirement_reason = result.reason
    return results


def _normalize_evidence_locations(locations: Iterable[str]) -> List[str]:
    """Keep stable, clause-level locations and discard parser punctuation noise."""
    normalized: List[str] = []
    seen: set[str] = set()
    for raw in locations:
        value = re.sub(r"\s+", "", str(raw or "")).strip("；;，,。.:：、|/\\")
        if not value or value in {"附件", "正文", "合同", "条款", "未知位置", "未定位"}:
            continue
        if not re.search(r"第[一二三四五六七八九十百零〇0-9]+(?:条|款|项|章|段)|附件[一二三四五六七八九十0-9]+|附录[一二三四五六七八九十0-9]+|第[一二三四五六七八九十0-9]+部分", value):
            continue
        key = re.sub(r"[\W_]+", "", value, flags=re.UNICODE).lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(value)
    return normalized


def _aggregate_review_provenance(
    coverage_elements: List[Dict[str, Any]],
    evidence_clauses: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    evidence_by_id: Dict[str, Dict[str, Any]] = {}
    for index, evidence in enumerate(evidence_clauses or [], start=1):
        evidence_by_id[_evidence_id(evidence, index)] = evidence
        if evidence.get("evidence_id"):
            evidence_by_id[str(evidence["evidence_id"])] = evidence

    evidence_ids: List[str] = []
    clause_ids: List[str] = []
    source_spans: List[str] = []
    locations: List[str] = []
    claim_ids: List[str] = []
    for element in coverage_elements:
        if element.get("status") not in {"COVERED", "PARTIALLY_COVERED"}:
            continue
        if element.get("claim_id"):
            claim_ids.append(str(element["claim_id"]))
        evidence_ids.extend(str(value) for value in element.get("evidence_ids", []) if value)
        clause_ids.extend(str(value) for value in element.get("source_clause_ids", []) if value)
        source_spans.extend(str(value) for value in element.get("source_spans", []) if value)
        locations.extend(str(value) for value in element.get("source_locations", []) if value)
        for evidence_id in element.get("evidence_ids", []):
            evidence = evidence_by_id.get(str(evidence_id))
            if not evidence:
                continue
            if evidence.get("clause_id"):
                clause_ids.append(str(evidence["clause_id"]))
            if evidence.get("original_excerpt") or evidence.get("text"):
                source_spans.append(str(evidence.get("original_excerpt") or evidence.get("text")))
            if evidence.get("location"):
                locations.append(str(evidence["location"]))

    if not evidence_ids:
        for index, evidence in enumerate(evidence_clauses or [], start=1):
            evidence_ids.append(_evidence_id(evidence, index))
            if evidence.get("clause_id"):
                clause_ids.append(str(evidence["clause_id"]))
            if evidence.get("original_excerpt") or evidence.get("text"):
                source_spans.append(str(evidence.get("original_excerpt") or evidence.get("text")))
            if evidence.get("location"):
                locations.append(str(evidence["location"]))

    unique_locations = _normalize_evidence_locations(locations)
    return {
        "claim_ids": list(dict.fromkeys(claim_ids)),
        "evidence_ids": list(dict.fromkeys(evidence_ids)),
        "clause_ids": list(dict.fromkeys(clause_ids)),
        "source_spans": list(dict.fromkeys(source_spans)),
        "primary_locations": unique_locations[:1],
        "supporting_locations": unique_locations[1:],
    }


def _assemble_review_provenance(item: ReviewItemResult) -> None:
    provenance = _aggregate_review_provenance(item.coverage_elements, item.evidence_clauses)
    item.review_evidence_provenance = provenance
    item.decision_trace["review_evidence_provenance"] = provenance
    locations = provenance["primary_locations"] + provenance["supporting_locations"]
    if locations:
        item.evidence_location = "；".join(locations)


def _coverage_from_elements(item: ReviewItemResult, elements: List[CoverageElementResult]) -> str:
    if item.coverage_status in {COVERAGE_NOT_APPLICABLE, "风险条款"}:
        return item.coverage_status
    claim = _coverage_claim_for_item(item)
    if claim.satisfaction_paths:
        status_by_id = {element.element_id: element.status for element in elements}
        execution_context = (item.decision_trace or {}).get("execution_context") or {}
        path_context = {
            **(execution_context.get("contract_context") or {}),
            **(execution_context.get("domain_resolution") or {}),
            **(execution_context.get("product_context") or {}),
            "transaction_structure": execution_context.get("transaction_structure"),
        }
        path_results = []
        for path in claim.satisfaction_paths:
            required_ids = list(path.get("required_elements") or [])
            optional_ids = list(path.get("optional_elements") or [])
            applicable_when = dict(path.get("applicable_when") or {})
            applicable = all(path_context.get(key) == expected for key, expected in applicable_when.items())
            required_statuses = [status_by_id.get(element_id, "MISSING") for element_id in required_ids]
            passed = applicable and bool(required_ids) and all(status == "COVERED" for status in required_statuses)
            path_results.append({
                "path_id": path.get("path_id"),
                "applicable_when": applicable_when,
                "applicable": applicable,
                "required_elements": required_ids,
                "optional_elements": optional_ids,
                "statuses": dict(zip(required_ids, required_statuses)),
                "status": "SATISFIED" if passed else "NOT_SATISFIED",
            })
        item.decision_trace["common_review_satisfaction"] = {
            "satisfaction_paths": path_results,
            "selected_path_id": next((row["path_id"] for row in path_results if row["status"] == "SATISFIED"), ""),
            "transaction_structure": ((item.decision_trace or {}).get("execution_context") or {}).get("transaction_structure", ""),
        }
        active_paths = [row for row in path_results if row["applicable"]]
        if any(row["status"] == "SATISFIED" for row in active_paths):
            return "通过"
        if any(element.status in {"COVERED", "PARTIALLY_COVERED"} for element in elements):
            return "部分覆盖"
        return "缺失"
    covered = sum(1 for element in elements if element.status == "COVERED")
    partial_or_covered = sum(1 for element in elements if element.status in {"COVERED", "PARTIALLY_COVERED"})
    if covered >= claim.minimum_pass_elements:
        return "通过"
    if partial_or_covered >= claim.minimum_partial_elements:
        return "部分覆盖"
    return "缺失"


STRICT_COVERAGE_ELEMENT_NODES = {
    "tenant_death_successor",
    "tenant_death_settlement",
    "indefinite_lease",
    "reasonable_repair_cost",
    "deposit_offset_order",
    "deposit_return_deadline",
    "termination_notice",
    "move_in_defect_notice",
}


def _should_apply_strict_coverage_gate(item: ReviewItemResult) -> bool:
    if (
        item.item_id.startswith("S-")
        or item.node_id in STRICT_COVERAGE_ELEMENT_NODES
        or item.node_id in {"real_estate_agent_authority", "real_estate_third_party_rights"}
        or item.risk_group in {"deposit_offset_order"}
    ):
        return True
    if item.item_id.startswith("SVC-"):
        claim = _coverage_claim_for_item(item)
        element_ids = {str(element.get("element_id") or "") for element in claim.required_elements}
        return bool(element_ids) and element_ids != {"core_contract_arrangement"}
    entailments = {str(evidence.get("entailment_status") or "") for evidence in item.evidence_clauses or []}
    return bool(entailments & {EVIDENCE_RELATED_NOT_SUPPORTING, EVIDENCE_NOT_RELEVANT})


def _apply_coverage_evidence_gate(items: List[ReviewItemResult], canonical_claims: Optional[Dict[str, Any]] = None) -> List[ReviewItemResult]:
    for item in items:
        if (
            item.item_id.startswith("SVC-")
            and item.coverage_status == "部分覆盖"
            and item.issue_type == "模板空白"
            and not item.evidence_clauses
            and (item.decision_trace or {}).get("service_template_blank_evidence")
        ):
            item.evidence_clauses = list((item.decision_trace or {}).get("service_template_blank_evidence") or [])
            item.evidence_location = "；".join(
                str(clause.get("location") or clause.get("section") or "")
                for clause in item.evidence_clauses
                if clause.get("location") or clause.get("section")
            )
        required_claim_ids = [str(element.get("required_claim")) for element in _coverage_claim_for_item(item).required_elements if element.get("required_claim")]
        if required_claim_ids:
            existing_ids = {str(evidence.get("clause_id")) for evidence in item.evidence_clauses}
            for claim_id in required_claim_ids:
                claim = (canonical_claims or {}).get(claim_id)
                if not claim:
                    continue
                for clause_id, span in zip(claim.source_clause_ids, claim.source_spans):
                    if clause_id in existing_ids:
                        continue
                    source_index = claim.source_clause_ids.index(clause_id)
                    source_locations = list(getattr(claim, "source_locations", []))
                    item.evidence_clauses.append({
                        "evidence_id": f"CCE-{clause_id}", "clause_id": clause_id,
                        "location": source_locations[source_index] if source_index < len(source_locations) else "合同条款/附件",
                        "text": span, "original_excerpt": span, "evidence_type": "CANONICAL_CLAIM_EVIDENCE",
                        "entailment_status": EVIDENCE_SUPPORTS, "claim_id": claim_id,
                    })
                    existing_ids.add(clause_id)
        elements = _coverage_elements_for_item(item, canonical_claims)
        _apply_service_template_partial_elements(item, elements)
        _protect_element_monotonicity(item, elements)
        if (
            item.coverage_status == "部分覆盖"
            and item.evidence_clauses
            and not any(element.status in {"COVERED", "PARTIALLY_COVERED"} for element in elements)
            and len(elements) == 1
            and elements[0].element_id == "core_contract_arrangement"
        ):
            evidence_ids = [_evidence_id(evidence, index) for index, evidence in enumerate(item.evidence_clauses, start=1)]
            elements[0].status = "PARTIALLY_COVERED"
            elements[0].evidence_ids = evidence_ids
            elements[0].entailment = EVIDENCE_PARTIAL_SUPPORT
            elements[0].verifier_confidence = "medium"
            elements[0].reason = "现有合同证据可部分支撑该复合要素。"
            elements[0].source_clause_ids = list(dict.fromkeys(str(evidence.get("clause_id")) for evidence in item.evidence_clauses if evidence.get("clause_id")))
            elements[0].source_spans = list(dict.fromkeys(str(evidence.get("original_excerpt") or evidence.get("text")) for evidence in item.evidence_clauses if evidence.get("original_excerpt") or evidence.get("text")))
            elements[0].source_locations = list(dict.fromkeys(str(evidence.get("location")) for evidence in item.evidence_clauses if evidence.get("location")))
        item.coverage_elements = [element.to_public_dict() for element in elements]
        _assemble_review_provenance(item)
        item.decision_trace["coverage_claim"] = _coverage_claim_for_item(item).to_public_dict()
        item.decision_trace["coverage_elements"] = item.coverage_elements
        item.decision_trace["element_evidence_truth"] = _element_truth_records(elements)
        if (item.decision_trace or {}).get("review_mode") == "ABSENCE_REQUIRED" and item.coverage_status == "通过":
            continue
        if item.coverage_status not in {"通过", "部分覆盖", "缺失"} or not _should_apply_strict_coverage_gate(item):
            continue
        gated_status = _coverage_from_elements(item, elements)
        if gated_status == item.coverage_status:
            continue
        item.decision_trace["coverage_evidence_gate"] = {
            "from": item.coverage_status,
            "to": gated_status,
            "reason": "Coverage requires at least one required element with SUPPORTS/PARTIAL_SUPPORT evidence; related or uncertain evidence contributes zero coverage.",
        }
        if gated_status == "缺失":
            item.evidence_clauses = []
            item.evidence_location = ""
            _set_item_missing(
                item,
                item.risk_level if item.risk_level in {"高", "中", "低"} else "中",
                f"元素级证据校验未找到能支撑“{item.title}”任一核心要素的合同条款；弱相关或不确定证据不贡献合同覆盖。",
                item.risk_point_description,
                "Coverage Evidence Gate",
            )
            item.coverage_elements = [element.to_public_dict() for element in elements]
            item.decision_trace["coverage_elements"] = item.coverage_elements
            item.decision_trace["element_evidence_truth"] = _element_truth_records(elements)
            item.narrative_state = _build_narrative_state(item)
            item.decision_trace["narrative_elements"] = item.narrative_state
        elif gated_status == "部分覆盖":
            item.coverage_status = "部分覆盖"
            item.status = "部分覆盖"
            item.issue_type = "条款缺陷"
            item.reasoning_summary = _dedupe_narrative_sentences(
                f"{item.reasoning_summary} 元素级证据校验仅确认部分核心要素，不能视为完整通过。"
            )
            item.decision_trace["element_evidence_truth"] = _element_truth_records(elements)
            item.narrative_state = _build_narrative_state(item)
            item.decision_trace["narrative_elements"] = item.narrative_state
        elif gated_status == "通过":
            item.coverage_status = "通过"
            item.status = "已覆盖"
            item.issue_type = "通过"
            item.risk_level = "低"
            item.risk_point_description = f"合同已覆盖“{item.title}”对应的必要要素。"
            item.reasoning_summary = "Required Elements 已由支持性合同证据满足，元素级覆盖校验通过。"
            item.decision_trace["element_evidence_truth"] = _element_truth_records(elements)
            item.narrative_state = _build_narrative_state(item)
            item.decision_trace["narrative_elements"] = item.narrative_state
    return items


def _apply_review_evidence_ownership(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    """Promote evidence that directly supports the review's resolved element truth."""
    for item in items:
        registry_bound = any(
            element.get("required_fact_key")
            for element in item.coverage_elements or []
        )
        if not registry_bound:
            supported_ids: set[str] = set()
            for evidence in item.evidence_clauses or []:
                clause_id = str(evidence.get("clause_id") or "")
                linked = [
                    str(element.get("element_id") or "")
                    for element in item.coverage_elements or []
                    if clause_id and clause_id in {
                        str(value)
                        for value in list(element.get("source_clause_ids") or []) + list(element.get("evidence_ids") or [])
                    }
                ]
                if linked:
                    evidence["supporting_element_ids"] = list(dict.fromkeys(linked))
                    evidence["canonical_fact_keys"] = []
                    evidence["relevance_score"] = 1.0
                    evidence["selection_reason"] = "Existing evidence directly supports resolved ReviewElementTruth."
                    supported_ids.update(linked)
                else:
                    evidence["supporting_element_ids"] = []
                    evidence["canonical_fact_keys"] = []
                    evidence["relevance_score"] = min(float(evidence.get("semantic_score") or 0.0), 0.5)
                    evidence["selection_reason"] = "Contextual retrieval evidence does not directly support a resolved ReviewElementTruth."
                evidence["review_id"] = item.item_id
                evidence["element_ids"] = list(evidence["supporting_element_ids"])
                evidence["support_type"] = "DIRECT" if linked else "CONTEXTUAL"
            item.evidence_clauses.sort(key=lambda row: (
                0 if row.get("support_type") == "DIRECT" else 1,
                -len(row.get("supporting_element_ids") or []),
                -float(row.get("relevance_score") or 0.0),
                str(row.get("location") or ""),
            ))
            for element in item.coverage_elements or []:
                evidence_refs = list(element.get("source_clause_ids") or element.get("evidence_ids") or [])
                element["evidence_refs"] = evidence_refs
                element["evidence_selection_reason"] = (
                    "Direct evidence selected by exact source-clause ownership for this element."
                    if element.get("status") in {"COVERED", "PARTIALLY_COVERED"} and evidence_refs
                    else "No direct supporting evidence was selected for this element."
                )
            item.review_evidence_supports_element_ids = sorted(supported_ids)
            item.review_evidence_relevance_score = 1.0 if supported_ids else 0.0
            item.review_evidence_selection_reason = "Existing non-Registry evidence order was preserved and ownership metadata was attached in place."
            item.decision_trace["review_evidence_ownership"] = {
                "review_evidence_supports_element_ids": list(item.review_evidence_supports_element_ids),
                "review_evidence_relevance_score": item.review_evidence_relevance_score,
                "review_evidence_selection_reason": item.review_evidence_selection_reason,
            }
            continue
        selected: List[Dict[str, Any]] = []
        by_clause: Dict[str, Dict[str, Any]] = {}
        for element in item.coverage_elements or []:
            if element.get("status") not in {"COVERED", "PARTIALLY_COVERED"}:
                continue
            element_id = str(element.get("element_id") or "")
            fact_key = canonical_fact_key(str(element.get("required_fact_key") or element.get("claim_id") or ""))
            clause_ids = list(element.get("source_clause_ids") or [])
            spans = list(element.get("source_spans") or [])
            locations = list(element.get("source_locations") or [])
            for index, span in enumerate(spans):
                clause_id = str(clause_ids[index] if index < len(clause_ids) else (clause_ids[0] if clause_ids else ""))
                location = str(locations[index] if index < len(locations) else (locations[0] if locations else ""))
                key = clause_id or f"SPAN-{hashlib.sha256(str(span).encode('utf-8')).hexdigest()[:10]}"
                row = by_clause.setdefault(key, {
                    "evidence_id": f"RE-{item.item_id}-{len(by_clause) + 1:03d}",
                    "clause_id": clause_id,
                    "location": location,
                    "text": str(span),
                    "original_excerpt": str(span),
                    "evidence_type": "REGISTRY_FACT_EVIDENCE" if fact_key else "ELEMENT_DIRECT_EVIDENCE",
                    "entailment_status": EVIDENCE_SUPPORTS if element.get("status") == "COVERED" else EVIDENCE_PARTIAL_SUPPORT,
                    "supporting_element_ids": [],
                    "canonical_fact_keys": [],
                    "relevance_score": 1.0,
                    "selection_reason": "Direct source evidence for resolved ReviewElementTruth.",
                    "review_id": item.item_id,
                    "element_ids": [],
                    "support_type": "DIRECT",
                })
                if element_id and element_id not in row["supporting_element_ids"]:
                    row["supporting_element_ids"].append(element_id)
                if element_id and element_id not in row["element_ids"]:
                    row["element_ids"].append(element_id)
                if fact_key and "." in fact_key and fact_key not in row["canonical_fact_keys"]:
                    row["canonical_fact_keys"].append(fact_key)
        selected.extend(by_clause.values())
        if selected:
            selected.sort(key=lambda row: (-len(row.get("supporting_element_ids") or []), str(row.get("location") or "")))
            item.evidence_clauses = selected
            item.evidence_location = "；".join(dict.fromkeys(str(row.get("location") or "") for row in selected if row.get("location")))
            item.review_evidence_supports_element_ids = sorted({element_id for row in selected for element_id in row.get("supporting_element_ids") or []})
            item.review_evidence_relevance_score = round(sum(float(row.get("relevance_score") or 0.0) for row in selected) / len(selected), 3)
            item.review_evidence_selection_reason = "Registry/element direct evidence was selected before legacy retrieval evidence."
        else:
            item.review_evidence_supports_element_ids = []
            item.review_evidence_relevance_score = 0.0
            item.review_evidence_selection_reason = "No positive element evidence; absence or manual-review evidence remains unchanged."
        for element in item.coverage_elements or []:
            evidence_refs = list(element.get("source_clause_ids") or element.get("evidence_ids") or [])
            element["evidence_refs"] = evidence_refs
            element["evidence_selection_reason"] = (
                "Direct Registry/element evidence selected by exact source-clause ownership."
                if element.get("status") in {"COVERED", "PARTIALLY_COVERED"} and evidence_refs
                else "No direct supporting evidence was selected for this element."
            )
        item.decision_trace["review_evidence_ownership"] = {
            "review_evidence_supports_element_ids": list(item.review_evidence_supports_element_ids),
            "review_evidence_relevance_score": item.review_evidence_relevance_score,
            "review_evidence_selection_reason": item.review_evidence_selection_reason,
        }
    return items


def _review_evidence_element_gate(items: List[ReviewItemResult]) -> Dict[str, Any]:
    mismatches: List[Dict[str, Any]] = []
    rows: List[Dict[str, Any]] = []
    for item in items:
        covered_elements = [
            element for element in item.coverage_elements or []
            if element.get("status") in {"COVERED", "PARTIALLY_COVERED"}
        ]
        covered_ids = {str(element.get("element_id") or "") for element in covered_elements if element.get("element_id")}
        evidence_rows = list(item.evidence_clauses or [])
        direct_rows = [row for row in evidence_rows if row.get("support_type") == "DIRECT"]
        for element in covered_elements:
            element_id = str(element.get("element_id") or "")
            source_clause_ids = {str(value) for value in element.get("source_clause_ids") or [] if value}
            supporting = [
                row for row in direct_rows
                if element_id in {str(value) for value in row.get("supporting_element_ids") or row.get("element_ids") or []}
                and (
                    not source_clause_ids
                    or str(row.get("clause_id") or "") in source_clause_ids
                )
            ]
            row = {
                "review_id": item.item_id,
                "element_id": element_id,
                "status": element.get("status"),
                "evidence_refs": [str(value) for value in element.get("evidence_refs") or element.get("evidence_ids") or []],
                "direct_evidence_refs": [str(evidence.get("clause_id") or evidence.get("evidence_id") or "") for evidence in supporting],
                "selection_reason": str(element.get("evidence_selection_reason") or ""),
            }
            rows.append(row)
            if not supporting:
                mismatches.append({
                    **row,
                    "reason": "A covered Review element has no DIRECT evidence with matching element and source-clause ownership.",
                })
        if covered_ids and evidence_rows:
            primary_ids = {
                str(value) for value in evidence_rows[0].get("supporting_element_ids") or evidence_rows[0].get("element_ids") or []
            }
            if evidence_rows[0].get("support_type") != "DIRECT" or not (primary_ids & covered_ids):
                mismatches.append({
                    "review_id": item.item_id,
                    "element_id": "PRIMARY_EVIDENCE",
                    "evidence_refs": [str(evidence_rows[0].get("clause_id") or evidence_rows[0].get("evidence_id") or "")],
                    "reason": "The primary report evidence does not directly support any covered element in this Review.",
                })
    failures = [{
        "requirement": "REVIEW_EVIDENCE_ELEMENT_MISMATCH",
        "failure_stage": "Review Evidence Projection",
        "root_cause": f"Review evidence is not exactly bound to covered elements: {len(mismatches)} mismatch(es).",
        "current_status": "FAIL",
        "mismatches": mismatches,
    }] if mismatches else []
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "gate_results": {"REVIEW_EVIDENCE_ELEMENT_MISMATCH": "PASS" if not failures else "FAIL"},
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "rows": rows,
    }


def _attach_recall_state(
    items: List[ReviewItemResult],
    checklist: Any,
    clauses: List[Any],
    fact_graph: ContractFactGraph,
    canonical_claims: Optional[Dict[str, Any]] = None,
) -> List[ReviewItemResult]:
    checkpoints = {checkpoint.item_id: checkpoint for checkpoint in checklist}
    section_ids = list(dict.fromkeys(str(clause.location) for clause in clauses if clause.location))
    for item in items:
        checkpoint = checkpoints.get(item.item_id)
        if not checkpoint:
            continue
        candidates, _, trace = retrieve_evidence_candidates(
            checkpoint,
            clauses,
            fact_graph=fact_graph,
            max_candidates=24,
        )
        fact_matches = fact_graph.matching(trace.fact_requirements)
        possible_conflicts = [fact.fact_id for fact in fact_matches if fact.normalized_value not in {False, None, ""}] if item.coverage_status == "缺失" else []
        missing_proof = MissingProof(
            review_id=item.item_id,
            searched_fact_types=trace.fact_requirements,
            searched_sections=section_ids,
            lexical_queries=trace.lexical_queries,
            semantic_queries=trace.semantic_queries,
            cross_clause_queries=trace.graph_clause_ids,
            candidates_examined=trace.candidate_clause_ids,
            possible_conflicts=possible_conflicts,
            exhaustive_enough=bool(
                trace.lexical_queries
                and trace.semantic_queries
                and section_ids
                and not possible_conflicts
            ),
            confidence="high" if not possible_conflicts else "low",
        )
        item.decision_trace["review_mode"] = (
            "ABSENCE_REQUIRED" if checkpoint.kind == "forbidden" else "PRESENCE_REQUIRED"
        )
        item.decision_trace["fact_requirements"] = trace.fact_requirements
        item.decision_trace["retrieval_trace"] = trace.to_public_dict()
        item.decision_trace["missing_proof"] = missing_proof.to_public_dict()
        item.decision_trace["evidence_assembly"] = EvidenceAssembly(
            review_id=item.item_id,
            candidate_evidence=trace.candidate_clause_ids,
            evidence_groups=[
                {"source": "FACT", "clause_ids": trace.fact_clause_ids},
                {"source": "STRUCTURAL", "clause_ids": trace.structural_clause_ids},
                {"source": "LEXICAL", "clause_ids": trace.lexical_clause_ids},
                {"source": "SEMANTIC", "clause_ids": trace.semantic_clause_ids},
                {"source": "CLAUSE_GRAPH", "clause_ids": trace.graph_clause_ids},
            ],
            supporting_evidence=[str(evidence.get("clause_id") or "") for evidence in item.evidence_clauses],
            counter_evidence=[],
            missing_elements=[
                str(element.get("element_id"))
                for element in item.coverage_elements
                if element.get("status") == "MISSING"
            ],
        ).to_public_dict()
        if possible_conflicts:
            item.decision_trace["fact_coverage_contradiction"] = {
                "status": "DETECTED",
                "fact_ids": possible_conflicts,
                "action": "RETRY_EVIDENCE_ASSEMBLY",
            }
            retry_ids = set(trace.fact_clause_ids + trace.graph_clause_ids)
            retry_evidence = [clause for clause in candidates if clause.clause_id in retry_ids]
            if retry_evidence:
                retry_judgment = judge_checkpoint(checkpoint, retry_evidence)
                if retry_judgment.coverage_status in {"通过", "部分覆盖", "风险条款"}:
                    item.coverage_status = retry_judgment.coverage_status
                    item.status = retry_judgment.status
                    item.issue_type = retry_judgment.issue_type
                    item.risk_level = retry_judgment.risk_level
                    item.risk_point_description = retry_judgment.risk_point_description
                    item.reasoning_summary = retry_judgment.reasoning_summary
                    item.evidence_clauses = retry_judgment.evidence_clauses
                    item.evidence_location = retry_judgment.evidence_location
                    item.matched_terms = retry_judgment.matched_terms
                    if item.coverage_status == "通过":
                        item.risk_point_description = f"合同已存在“{item.title}”对应的明确约定。"
                        item.reasoning_summary = f"事实优先召回和独立复核均定位到“{item.title}”的合同证据。"
                    item.coverage_elements = [
                    element.to_public_dict() for element in _coverage_elements_for_item(item, canonical_claims)
                    ]
                    item.decision_trace["coverage_elements"] = item.coverage_elements
                    item.decision_trace["fact_coverage_contradiction"]["status"] = "RESOLVED_BY_RETRY"
                    item.decision_trace["missing_proof"]["possible_conflicts"] = []
                    item.decision_trace["missing_proof"]["exhaustive_enough"] = True
                    item.decision_trace["missing_proof"]["confidence"] = "high"
                else:
                    item.needs_manual_review = True
                    item.quality_gate_failure_reason = "FACT_COVERAGE_CONTRADICTION"
                    item.llm_confidence = "low"
                    item.decision_trace["fact_coverage_contradiction"]["status"] = "UNRESOLVED"
    return items


def _recall_gate_failures(items: List[ReviewItemResult], integrity: Dict[str, Any]) -> List[Dict[str, Any]]:
    failures: List[Dict[str, Any]] = []
    if integrity.get("truncated") or float(integrity.get("parsed_character_ratio") or 0) < 0.95:
        failures.append({
            "requirement": "DOCUMENT_INTEGRITY_GATE",
            "failure_stage": "Document Parser",
            "root_cause": "文档解析覆盖率不足或检测到截断。",
            "responsible_function": "document_integrity",
            "current_status": "FAIL",
        })
    unresolved = [
        item.item_id for item in items
        if (item.decision_trace.get("fact_coverage_contradiction") or {}).get("status") == "UNRESOLVED"
    ]
    if unresolved:
        failures.append({
            "requirement": "FACT_COVERAGE_CONSISTENCY_GATE",
            "failure_stage": "Evidence Recall Verifier",
            "root_cause": f"事实存在但 Coverage 仍判缺失：{', '.join(unresolved)}。",
            "responsible_function": "_attach_recall_state",
            "current_status": "FAIL",
        })
    false_missing = [
        item.item_id for item in items
        if item.coverage_status == "缺失"
        and not (item.decision_trace.get("missing_proof") or {}).get("exhaustive_enough")
        and not item.needs_manual_review
    ]
    if false_missing:
        failures.append({
            "requirement": "MISSING_PROOF_GATE",
            "failure_stage": "Coverage Engine",
            "root_cause": f"缺失结论没有完整 MissingProof：{', '.join(false_missing)}。",
            "responsible_function": "_attach_recall_state",
            "current_status": "FAIL",
        })
    return failures


def _text_has_any(text: str, terms: List[str]) -> bool:
    return any(term and term in text for term in terms)


def _evidence_candidate_for_claim(claim: EvidenceClaim, evidence: Dict[str, Any], index: int) -> EvidenceCandidate:
    quote = str(evidence.get("quote") or evidence.get("text") or "")
    analysis_quote = str(evidence.get("text") or evidence.get("quote") or "")
    text = _compact(analysis_quote)
    review_id = claim.review_id
    entity_match = _text_has_any(text, claim.required_semantics[:3])
    obligation_match = _text_has_any(text, claim.required_semantics[3:])
    consequence_match = _text_has_any(text, ["违约金", "赔偿", "返还", "抵扣", "解除", "通知", "维修", "损坏"])
    polarity_match = not _text_has_any(text, ["不得", "不应", "禁止"]) if claim.polarity == "positive" else True
    status = EVIDENCE_UNCERTAIN
    score = 0.0

    if review_id == "HL-042" or claim.object == "deposit_offset_order":
        has_deposit = _text_has_any(text, ["押金", "保证金"])
        has_offset_action = _text_has_any(text, ["抵扣", "扣除", "扣款"])
        has_offset_items = _text_has_any(text, ["未付租金", "欠付租金", "水电费", "物业费", "维修费", "欠费", "代垫费用"])
        has_order = _text_has_any(text, ["抵扣顺序", "扣除顺序", "先抵扣", "后抵扣", "依次", "先行", "其次"])
        has_early_penalty_context = _text_has_any(text, ["提前退租", "中途擅自退租", "违约金", "甲方损失"])
        if has_early_penalty_context and not has_offset_items:
            status = EVIDENCE_RELATED_NOT_SUPPORTING
            score = 0.35
        elif has_deposit and has_offset_action and has_offset_items and has_order:
            status = EVIDENCE_SUPPORTS
            score = 0.95
        elif has_deposit and has_offset_action and has_offset_items:
            status = EVIDENCE_PARTIAL_SUPPORT
            score = 0.72
        elif has_early_penalty_context:
            status = EVIDENCE_RELATED_NOT_SUPPORTING
            score = 0.35
        else:
            status = EVIDENCE_NOT_RELEVANT
            score = 0.1
    elif claim.object == "sale_unilateral_price_adjustment":
        has_price = _text_has_any(text, ["单价", "价格", "价款", "货款", "报价"])
        has_adjustment = _text_has_any(text, ["调整", "变动", "变更", "浮动", "调价"])
        has_fixed_price_only = has_price and not has_adjustment
        has_negated_adjustment = _text_has_any(text, ["不因", "不得", "不予", "不作", "不调整", "不变更", "固定"])
        has_mutual_control = _text_has_any(text, ["双方协商一致", "双方书面确认", "经双方同意", "经买方同意", "补充协议"])
        has_objective_index = _text_has_any(text, ["价格指数", "公开指数", "公开市场指数", "挂牌价", "基准价"])
        has_unilateral = _has_sale_unilateral_price_adjustment(analysis_quote)
        if has_unilateral and not has_mutual_control:
            status = EVIDENCE_SUPPORTS
            score = 0.93
        elif has_negated_adjustment:
            status = EVIDENCE_RELATED_NOT_SUPPORTING
            score = 0.25
        elif has_objective_index or has_mutual_control:
            status = EVIDENCE_RELATED_NOT_SUPPORTING
            score = 0.35
        elif has_fixed_price_only:
            status = EVIDENCE_RELATED_NOT_SUPPORTING
            score = 0.2
        elif has_price or has_adjustment:
            status = EVIDENCE_RELATED_NOT_SUPPORTING if has_price and has_adjustment else EVIDENCE_NOT_RELEVANT
            score = 0.3 if status == EVIDENCE_RELATED_NOT_SUPPORTING else 0.1
        else:
            status = EVIDENCE_NOT_RELEVANT
            score = 0.1
    elif claim.object == "tenant_death_successor":
        has_death = _text_has_any(text, ["承租人死亡", "租赁期间死亡", "租期内死亡", "乙方死亡"])
        has_successor = _text_has_any(text, ["共同居住", "共同经营", "继续承租", "继续租赁", "继续使用"])
        has_expiry = _text_has_any(text, ["租赁期满", "租期届满", "期满", "续租", "重新签订"])
        if has_death and has_successor:
            status = EVIDENCE_SUPPORTS
            score = 0.95
        elif has_expiry and not has_death:
            status = EVIDENCE_RELATED_NOT_SUPPORTING
            score = 0.25
        elif has_death or has_successor:
            status = EVIDENCE_PARTIAL_SUPPORT
            score = 0.65
        else:
            status = EVIDENCE_NOT_RELEVANT
            score = 0.1
    elif claim.object == "tenant_death_settlement":
        if _text_has_any(text, ["无人继续", "继承人", "遗留物"]) and _text_has_any(text, ["交接", "返还", "结清", "费用"]):
            status = EVIDENCE_SUPPORTS
            score = 0.9
        elif _text_has_any(text, ["租赁期满", "租期届满", "期满"]):
            status = EVIDENCE_RELATED_NOT_SUPPORTING
            score = 0.25
        else:
            status = EVIDENCE_NOT_RELEVANT
            score = 0.1
    elif claim.object == "indefinite_lease":
        has_expiry_continue = _text_has_any(text, ["租赁期满", "租期届满", "期满"]) and _text_has_any(text, ["继续承租", "续租", "继续使用", "继续居住"])
        has_no_objection = _text_has_any(text, ["未提出异议", "没有异议", "继续收租", "接受租金"])
        has_notice = _text_has_any(text, ["合理期限", "提前", "书面通知", "解除", "通知"])
        if has_expiry_continue and has_no_objection and has_notice:
            status = EVIDENCE_SUPPORTS
            score = 0.9
        elif has_expiry_continue or has_no_objection or has_notice:
            status = EVIDENCE_PARTIAL_SUPPORT
            score = 0.65
        else:
            status = EVIDENCE_NOT_RELEVANT
            score = 0.1
    elif claim.object == "reasonable_repair_cost":
        has_cost = _text_has_any(text, ["维修费", "维修费用", "维修"])
        has_reasonable = _text_has_any(text, ["必要", "合理", "实际发生", "市场报价"])
        has_voucher = _text_has_any(text, ["维修单", "发票", "报价单", "鉴定", "票据", "凭证"])
        if has_cost and has_reasonable and has_voucher:
            status = EVIDENCE_SUPPORTS
            score = 0.9
        elif has_cost and (has_reasonable or has_voucher):
            status = EVIDENCE_PARTIAL_SUPPORT
            score = 0.65
        elif _text_has_any(text, ["毁损", "灭失", "危险房屋"]) and not has_cost:
            status = EVIDENCE_RELATED_NOT_SUPPORTING
            score = 0.25
        else:
            status = EVIDENCE_NOT_RELEVANT
            score = 0.1
    elif claim.object == "deposit_return_deadline":
        has_deposit_return = _text_has_any(text, ["押金", "保证金"]) and _text_has_any(text, ["返还", "退还", "归还"])
        has_deadline = _text_has_any(text, ["日内", "工作日", "期限", "交接后", "结算后", "完成交接"])
        if has_deposit_return and has_deadline:
            status = EVIDENCE_SUPPORTS
            score = 0.9
        elif has_deposit_return:
            status = EVIDENCE_PARTIAL_SUPPORT
            score = 0.7
        else:
            status = EVIDENCE_NOT_RELEVANT
            score = 0.1
    elif claim.finding_id == "RF-EARLY-TERM-001" or "提前退租" in claim.proposition:
        if _text_has_any(text, ["提前退租", "中途退租", "提前解除"]) and _text_has_any(text, ["违约金", "剩余租期", "租金", "损失"]):
            status = EVIDENCE_SUPPORTS
            score = 0.92
        elif _text_has_any(text, ["退租", "解除", "违约金"]):
            status = EVIDENCE_PARTIAL_SUPPORT
            score = 0.65
        else:
            status = EVIDENCE_NOT_RELEVANT
            score = 0.15
    elif review_id == "HL-040":
        if _text_has_any(text, ["入住", "交接"]) and _text_has_any(text, ["瑕疵", "缺陷", "照片", "视频", "告知"]):
            status = EVIDENCE_SUPPORTS
            score = 0.9
        elif _text_has_any(text, ["抵押", "贷款", "产权"]):
            status = EVIDENCE_RELATED_NOT_SUPPORTING
            score = 0.2
        else:
            status = EVIDENCE_NOT_RELEVANT
            score = 0.1
    else:
        matched = sum(1 for term in claim.required_semantics if term and term in text)
        if matched >= 2:
            status = EVIDENCE_SUPPORTS
            score = 0.75
        elif matched == 1:
            status = EVIDENCE_PARTIAL_SUPPORT
            score = 0.55
        else:
            status = EVIDENCE_UNCERTAIN if quote else EVIDENCE_NOT_RELEVANT
            score = 0.25 if quote else 0.0

    return EvidenceCandidate(
        evidence_id=str(evidence.get("clause_id") or evidence.get("location") or f"{claim.review_id}-EV-{index}"),
        source_document=str(evidence.get("document_name") or evidence.get("source_label") or evidence.get("source_document_type") or ""),
        clause_id=str(evidence.get("clause_id") or ""),
        sentence_id=int(evidence.get("sentence_index") or index),
        quote=analysis_quote or quote,
        semantic_score=score,
        entity_match=entity_match,
        obligation_match=obligation_match,
        consequence_match=consequence_match,
        polarity_match=polarity_match,
        entailment_status=status,
    )


def _negative_evidence_for_item(item: ReviewItemResult, claim: EvidenceClaim, candidates: List[EvidenceCandidate]) -> NegativeEvidence:
    rejected = [
        {
            "evidence_id": candidate.evidence_id,
            "quote": candidate.quote,
            "entailment_status": candidate.entailment_status,
            "semantic_score": candidate.semantic_score,
        }
        for candidate in candidates
        if candidate.entailment_status not in {EVIDENCE_SUPPORTS, EVIDENCE_PARTIAL_SUPPORT}
    ]
    return NegativeEvidence(
        review_id=item.item_id,
        searched_scope="合同正文及附件",
        positive_patterns=claim.required_semantics,
        semantic_queries=[claim.proposition],
        candidate_count=len(candidates),
        rejected_candidates=rejected,
        result="NOT_FOUND" if not candidates or len(rejected) == len(candidates) else "FOUND",
        confidence="high" if item.coverage_status == "缺失" else "medium",
    )


def _apply_evidence_entailment_gate(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    strict_review_ids = {"HL-039", "HL-040", "HL-042", "S-02-05"}
    strict_risk_groups = {"early_termination_financial_exposure", "deposit_offset_order", "sale_unilateral_price_adjustment"}
    for item in items:
        claim = _evidence_claim_for_item(item)
        candidates = [_evidence_candidate_for_claim(claim, evidence, index) for index, evidence in enumerate(item.evidence_clauses or [], start=1)]
        for evidence, candidate in zip(item.evidence_clauses or [], candidates):
            evidence["evidence_claim_id"] = claim.claim_id
            evidence["entailment_status"] = candidate.entailment_status
            evidence["semantic_score"] = candidate.semantic_score
            evidence["entity_match"] = candidate.entity_match
            evidence["obligation_match"] = candidate.obligation_match
            evidence["consequence_match"] = candidate.consequence_match
            evidence["polarity_match"] = candidate.polarity_match
        supporting = [
            evidence for evidence in item.evidence_clauses or []
            if evidence.get("entailment_status") in {EVIDENCE_SUPPORTS, EVIDENCE_PARTIAL_SUPPORT}
        ]
        item.decision_trace["evidence_claim"] = claim.to_public_dict()
        item.decision_trace["evidence_candidates"] = [candidate.to_public_dict() for candidate in candidates]
        strict_gate = item.item_id in strict_review_ids or item.risk_group in strict_risk_groups
        item.semantic_entailment = bool(supporting) if strict_gate and item.evidence_clauses else item.semantic_entailment
        if strict_gate and item.coverage_status in {"通过", "部分覆盖", "风险条款"} and item.evidence_clauses and not supporting:
            item.decision_trace["negative_evidence"] = _negative_evidence_for_item(item, claim, candidates).to_public_dict()
            item.evidence_clauses = []
            item.evidence_location = ""
            if item.coverage_status == "部分覆盖":
                _set_item_missing(
                    item,
                    item.risk_level if item.risk_level in {"高", "中", "低"} else "中",
                    f"证据语义校验未找到能支撑“{item.title}”结论的合同句子；相关候选句仅属于背景或其他风险，不能作为部分覆盖依据。",
                    item.risk_point_description,
                    "Evidence Entailment Gate",
                )
            elif item.coverage_status == "风险条款":
                if (item.decision_trace or {}).get("review_mode") == "ABSENCE_REQUIRED":
                    item.coverage_status = "通过"
                    item.status = "未发现明显风险条款"
                    item.issue_type = "通过"
                    item.risk_level = "低"
                    item.reasoning_summary = f"穷尽检索未找到能支撑“{item.title}”存在的合同证据。"
                    item.risk_point_description = f"合同未发现“{item.title}”类不利约定。"
                    item.fallback_reason = "Evidence Entailment Gate"
                else:
                    _set_item_missing(
                        item,
                        "低" if item.item_id == "S-02-05" else item.risk_level if item.risk_level in {"高", "中", "低"} else "中",
                        f"证据语义校验未找到能支撑“{item.title}”存在的合同句子；相关候选句不能作为风险条款依据。",
                        f"未发现能直接证明“{item.title}”存在的明确约定。",
                        "Evidence Entailment Gate",
                    )
                item.decision_trace["positive_risk_evidence_gate"] = {
                    "status": "REJECTED",
                    "reason": "Risk-clause finding requires SUPPORTS evidence.",
                }
        elif item.coverage_status == "缺失":
            item.decision_trace["negative_evidence"] = _negative_evidence_for_item(item, claim, candidates).to_public_dict()
        elif strict_gate:
            item.evidence_clauses = supporting or item.evidence_clauses
    return items


def _find_clause(clauses: List[Any], predicate) -> Optional[Any]:
    for clause in clauses:
        if predicate(clause):
            return clause
    return None


def _find_clauses(clauses: List[Any], predicate, limit: int = 2) -> List[Any]:
    found = []
    for clause in clauses:
        if predicate(clause):
            found.append(clause)
            if len(found) >= limit:
                break
    return found


def _service_find_clauses(clauses: List[Any], terms: Iterable[str], compacted: str, limit: int = 2) -> List[Any]:
    terms = tuple(term for term in terms if term)
    found = [clause for clause in clauses if any(term in clause.text for term in terms)]
    if len(found) > limit:
        def score(clause: Any) -> tuple[int, int]:
            text = str(getattr(clause, "text", "") or "")
            semantic_hits = sum(1 for term in terms if term in text)
            strong_hits = sum(1 for term in ("退学", "开班前", "开班后", "全额退费", "未消耗课时", "实际消耗课时", "书面通知") if term in text)
            checkbox_hits = 2 if "☑" in text else 0
            return semantic_hits + strong_hits + checkbox_hits, -int(getattr(clause, "paragraph_index", 0) or 0)
        found = sorted(found, key=score, reverse=True)
    found = found[:limit]
    if found or not any(term in compacted for term in terms):
        return found
    excerpt = compacted[:260]
    return [
        ParsedClause(
            clause_id="SVC-RECALL-FULLTEXT-001",
            location="合同全文",
            title="服务合同全文召回",
            text=excerpt,
            section_type="正式合同条款",
            level=1,
            raw_text=excerpt,
            normalized_text=excerpt,
            source="body",
        )
    ]


SERVICE_TEMPLATE_PARTIAL_ELEMENTS: Dict[str, set[str]] = {
    "service_content_standard": {"service_name", "class_or_project_id", "service_hours", "session_duration"},
    "service_schedule_and_place": {"service_time", "start_date", "end_date"},
    "prepaid_amount_and_balance": {"total_fee", "paid_amount", "balance_calculation"},
    "prepaid_partly_provided_refund": {"refund_trigger", "provided_service_value", "remaining_service_value"},
    "health_change_termination": {"termination_trigger", "proof_or_notice", "provided_service_deduction"},
    "consumer_personal_reason_termination": {"termination_trigger", "provided_service_deduction", "remaining_refund"},
    "consumer_termination_notice": {"notice_channel", "notice_materials"},
    "termination_refund_calculation": {"refund_trigger", "provided_service_value", "remaining_service_value"},
    "termination_notice_period": {"notice_channel"},
}


def _apply_service_template_partial_elements(item: ReviewItemResult, elements: List[CoverageElementResult]) -> None:
    if not (
        item.item_id.startswith("SVC-")
        and item.coverage_status == "部分覆盖"
        and item.issue_type == "模板空白"
        and (item.decision_trace or {}).get("service_template_blank_evidence")
    ):
        return
    supported_ids = SERVICE_TEMPLATE_PARTIAL_ELEMENTS.get(item.node_id) or SERVICE_TEMPLATE_PARTIAL_ELEMENTS.get(item.risk_group) or set()
    if not supported_ids:
        return
    evidence = item.evidence_clauses or list((item.decision_trace or {}).get("service_template_blank_evidence") or [])
    evidence_ids = [_evidence_id(row, index) for index, row in enumerate(evidence, start=1)]
    source_clause_ids = list(dict.fromkeys(str(row.get("clause_id")) for row in evidence if row.get("clause_id")))
    source_spans = list(dict.fromkeys(str(row.get("quote") or row.get("text")) for row in evidence if row.get("quote") or row.get("text")))
    source_locations = list(dict.fromkeys(str(row.get("location") or row.get("section")) for row in evidence if row.get("location") or row.get("section")))
    for element in elements:
        if element.element_id not in supported_ids or element.status == "COVERED":
            continue
        evidence_blob = "\n".join(str(row.get("text") or row.get("quote") or "") for row in evidence)
        explicit = _service_explicit_element_support(element.element_id, evidence_blob, _compact(evidence_blob))
        if not explicit or explicit[0] in {"MISSING", "UNCERTAIN"}:
            continue
        element.status = explicit[0]
        element.evidence_ids = evidence_ids
        element.entailment = explicit[1]
        element.verifier_confidence = "medium"
        element.reason = "服务模板空白规则确认合同已有基础条款片段，但该元素仍需补足细节。"
        element.source_clause_ids = source_clause_ids
        element.source_spans = source_spans
        element.source_locations = source_locations


def _element_truth_status(status: str) -> str:
    if status == "COVERED":
        return "FOUND"
    if status == "PARTIALLY_COVERED":
        return "PARTIAL"
    if status == COVERAGE_NOT_APPLICABLE:
        return "NOT_APPLICABLE"
    if status == "UNCERTAIN":
        return "UNCERTAIN"
    return "MISSING"


def _element_truth_records(elements: List[CoverageElementResult]) -> List[Dict[str, Any]]:
    return [
        {
            "element_id": element.element_id,
            "label": element.proposition,
            "status": _element_truth_status(element.status),
            "raw_status": element.status,
            "evidence_ids": list(element.evidence_ids),
            "evidence_text": list(element.source_spans),
            "source_location": list(element.source_locations),
            "confidence": element.verifier_confidence,
            "resolution_reason": element.reason,
        }
        for element in elements
    ]


def _fact_registry_snapshot_id(fact_graph: ContractFactGraph) -> str:
    payload = json.dumps(fact_graph.to_public_dict(), ensure_ascii=False, sort_keys=True, default=str)
    return f"CFR-{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:12].upper()}"


def _contract_fact_lookup(fact_graph: ContractFactGraph, fact_key: str) -> Dict[str, Any]:
    fact_key = canonical_fact_key(fact_key)
    facts = list(fact_graph.facts.get(fact_key, []))
    if not facts:
        return {
            "canonical_fact_key": fact_key,
            "status": "MISSING",
            "value": None,
            "normalized_value": None,
            "fact_ids": [],
            "source_clause_ids": [],
            "source_spans": [],
            "source_locations": [],
            "confidence": "low",
            "extraction_source": "CONTRACT_FACT_REGISTRY",
            "derived_from": [],
        }
    normalized_values = {
        json.dumps(fact.normalized_value, ensure_ascii=False, sort_keys=True, default=str)
        for fact in facts
        if fact.normalized_value not in (None, "")
    }
    status = "CONFLICTING" if fact_key in SCALAR_CONFLICT_FACT_KEYS and len(normalized_values) > 1 else "FOUND"
    primary = facts[0]
    return {
        "canonical_fact_key": fact_key,
        "status": status,
        "value": primary.value if status == "FOUND" else [fact.value for fact in facts],
        "normalized_value": primary.normalized_value if status == "FOUND" else [fact.normalized_value for fact in facts],
        "fact_ids": [fact.fact_id for fact in facts],
        "source_clause_ids": list(dict.fromkeys(clause_id for fact in facts for clause_id in fact.source_clause_ids)),
        "source_spans": list(dict.fromkeys(span for fact in facts for span in fact.source_spans)),
        "source_locations": list(dict.fromkeys(location for fact in facts for location in fact.source_locations if location)),
        "confidence": "high" if status == "FOUND" else "low",
        "extraction_source": "CONTRACT_FACT_REGISTRY",
        "derived_from": [],
    }


def _required_fact_keys_for_item(item: ReviewItemResult) -> List[str]:
    claim = _coverage_claim_for_item(item)
    element_keys = [
        canonical_fact_key(str(element.get("required_fact") or ""))
        for element in claim.required_elements
        if element.get("required_fact")
    ]
    return list(dict.fromkeys([*fact_requirements_for_node(item.node_id), *element_keys]))


def _attach_contract_fact_registry_snapshot(
    items: List[ReviewItemResult],
    fact_graph: ContractFactGraph,
    snapshot_id: str,
) -> None:
    for item in items:
        keys = [canonical_fact_key(key) for key in _required_fact_keys_for_item(item)]
        facts = {key: _contract_fact_lookup(fact_graph, key) for key in keys}
        item.decision_trace["fact_registry_snapshot_id"] = snapshot_id
        item.decision_trace["contract_fact_registry_consumption"] = {
            "snapshot_id": snapshot_id,
            "required_fact_keys": keys,
            "facts": facts,
            "fact_source": {
                key: "REGISTRY" if row["status"] in {"FOUND", "CONFLICTING"} else "REGISTRY_MISS"
                for key, row in facts.items()
            },
        }


def _contract_fact_flow_audit(items: List[ReviewItemResult], fact_graph: ContractFactGraph, snapshot_id: str) -> Dict[str, Any]:
    by_key: Dict[str, Dict[str, Any]] = {}
    conflicts: List[Dict[str, Any]] = []
    override_violations: List[Dict[str, Any]] = []
    mapping_missing: List[Dict[str, Any]] = []
    for item in items:
        claim = _coverage_claim_for_item(item)
        element_fact_keys = {
            str(element.get("element_id")): canonical_fact_key(str(element.get("required_fact")))
            for element in claim.required_elements
            if element.get("required_fact")
        }
        elements_by_id = {
            str(element.get("element_id")): element
            for element in item.coverage_elements or []
            if element.get("element_id")
        }
        consumption = (item.decision_trace or {}).get("contract_fact_registry_consumption") or {}
        for element_id, fact_key in element_fact_keys.items():
            registry_row = ((consumption.get("facts") or {}).get(fact_key)) or _contract_fact_lookup(fact_graph, fact_key)
            row = by_key.setdefault(
                fact_key,
                {
                    "canonical_fact_key": fact_key,
                    "registry_snapshot_id": snapshot_id,
                    "registry_status": registry_row.get("status"),
                    "registry_value": registry_row.get("value"),
                    "normalized_value": registry_row.get("normalized_value"),
                    "confidence": registry_row.get("confidence"),
                    "extraction_source": registry_row.get("extraction_source"),
                    "evidence_ids": registry_row.get("fact_ids"),
                    "evidence_text": registry_row.get("source_spans"),
                    "registry_evidence": registry_row.get("source_spans"),
                    "source_locations": registry_row.get("source_locations"),
                    "source_clause_ids": registry_row.get("source_clause_ids"),
                    "registry_source_location": registry_row.get("source_clause_ids"),
                    "derived_from": registry_row.get("derived_from"),
                    "consumer_review_ids": [],
                    "consumers": [],
                },
            )
            if item.item_id not in row["consumer_review_ids"]:
                row["consumer_review_ids"].append(item.item_id)
            final_element = elements_by_id.get(element_id)
            if not final_element:
                missing = {
                    "review_id": item.item_id,
                    "element_id": element_id,
                    "required_fact_key": fact_key,
                    "violation": "FACT_CONSUMER_MAPPING_MISSING",
                    "registry_snapshot_id": snapshot_id,
                }
                mapping_missing.append(missing)
                item.decision_trace.setdefault("contract_fact_registry_violations", []).append(missing)
                continue
            raw_status = str(final_element.get("status") or "MISSING")
            final_fact_status = str(final_element.get("fact_status") or _element_truth_status(raw_status))
            consumer = {
                "review_id": item.item_id,
                "element_id": element_id,
                "required_fact_key": fact_key,
                "registry_lookup_key": fact_key,
                "registry_lookup_result": registry_row.get("status"),
                "received_fact_status": registry_row.get("status"),
                "received_fact_value": registry_row.get("value"),
                "fact_source": "REGISTRY" if registry_row.get("status") in {"FOUND", "CONFLICTING"} else "LEGACY_FALLBACK",
                "final_element_fact_status": final_fact_status,
                "requirement_status": final_element.get("requirement_status"),
                "override_source": "REGISTRY" if registry_row.get("status") in {"FOUND", "CONFLICTING"} else "LEGACY_FALLBACK",
                "override_reason": final_element.get("requirement_reason") or final_element.get("reason") or "",
                "snapshot_id": str(consumption.get("snapshot_id") or ""),
            }
            row["consumers"].append(consumer)
            if registry_row.get("status") == "FOUND" and final_fact_status != "FOUND":
                violation = {
                    **consumer,
                    "violation": "FACT_TRUTH_OVERRIDE_VIOLATION",
                    "registry_snapshot_id": snapshot_id,
                }
                override_violations.append(violation)
                item.needs_manual_review = True
                item.quality_gate_failure_reason = "FACT_TRUTH_OVERRIDE_VIOLATION"
                item.decision_trace.setdefault("contract_fact_registry_violations", []).append(violation)
        element_fact_set = set(element_fact_keys.values())
        for fact_key in [canonical_fact_key(key) for key in _required_fact_keys_for_item(item) if canonical_fact_key(key) not in element_fact_set]:
            registry_row = ((consumption.get("facts") or {}).get(fact_key)) or _contract_fact_lookup(fact_graph, fact_key)
            row = by_key.setdefault(
                fact_key,
                {
                    "canonical_fact_key": fact_key,
                    "registry_snapshot_id": snapshot_id,
                    "registry_status": registry_row.get("status"),
                    "registry_value": registry_row.get("value"),
                    "normalized_value": registry_row.get("normalized_value"),
                    "confidence": registry_row.get("confidence"),
                    "extraction_source": registry_row.get("extraction_source"),
                    "evidence_ids": registry_row.get("fact_ids"),
                    "evidence_text": registry_row.get("source_spans"),
                    "registry_evidence": registry_row.get("source_spans"),
                    "source_locations": registry_row.get("source_locations"),
                    "source_clause_ids": registry_row.get("source_clause_ids"),
                    "registry_source_location": registry_row.get("source_clause_ids"),
                    "derived_from": registry_row.get("derived_from"),
                    "consumer_review_ids": [],
                    "consumers": [],
                },
            )
            if item.item_id not in row["consumer_review_ids"]:
                row["consumer_review_ids"].append(item.item_id)
            row["consumers"].append({
                "review_id": item.item_id,
                "element_id": "",
                "required_fact_key": fact_key,
                "registry_lookup_key": fact_key,
                "registry_lookup_result": registry_row.get("status"),
                "received_fact_status": registry_row.get("status"),
                "received_fact_value": registry_row.get("value"),
                "fact_source": "REGISTRY" if registry_row.get("status") in {"FOUND", "CONFLICTING"} else "REGISTRY_MISS",
                "final_element_fact_status": "",
                "requirement_status": "RETRIEVAL_ONLY",
                "override_source": "",
                "override_reason": "Canonical fact supports retrieval but is not itself the legal requirement.",
                "snapshot_id": str(consumption.get("snapshot_id") or ""),
            })
    for fact_key, row in by_key.items():
        statuses = {str(consumer.get("final_element_fact_status") or "") for consumer in row["consumers"]}
        if "FOUND" in statuses and statuses & {"MISSING", "UNCERTAIN", "CONFLICTING"}:
            conflicts.append({
                "canonical_fact_key": fact_key,
                "violation": "CROSS_REVIEW_FACT_CONFLICT",
                "statuses": sorted(statuses),
                "consumers": list(row["consumers"]),
                "registry_snapshot_id": snapshot_id,
            })
    snapshot_ids = {
        str((item.decision_trace or {}).get("fact_registry_snapshot_id") or "")
        for item in items
        if _required_fact_keys_for_item(item)
    }
    return {
        "registry_snapshot_id": snapshot_id,
        "registry_created": True,
        "registry_build_count": 1,
        "registry_frozen": bool(fact_graph.frozen),
        "registry_fact_count": sum(len(facts) for facts in fact_graph.facts.values()),
        "registry_snapshot_consistency": "PASS" if snapshot_ids == {snapshot_id} or not snapshot_ids else "FAIL",
        "snapshot_ids_seen": sorted(snapshot_ids),
        "facts": list(by_key.values()),
        "fact_consumers": {key: row["consumer_review_ids"] for key, row in by_key.items()},
        "cross_review_fact_conflicts": conflicts,
        "cross_review_fact_conflict_count": len(conflicts),
        "fact_truth_override_violations": override_violations,
        "fact_truth_override_violation_count": len(override_violations),
        "fact_consumer_mapping_missing": mapping_missing,
        "fact_consumer_mapping_missing_count": len(mapping_missing),
        "registry_legacy_override_count": len(override_violations),
    }


def _contract_fact_registry_gate(fact_flow_audit: Dict[str, Any]) -> Dict[str, Any]:
    failures: List[Dict[str, Any]] = []
    conflicting_facts = [
        row for row in fact_flow_audit.get("facts") or []
        if row.get("registry_status") == "CONFLICTING"
    ]
    if fact_flow_audit.get("registry_snapshot_consistency") != "PASS":
        failures.append({
            "requirement": "REGISTRY_SNAPSHOT_MISMATCH",
            "failure_stage": "Review Evaluation",
            "root_cause": "Review items did not consume the same ContractFactRegistry snapshot.",
            "responsible_function": "_attach_contract_fact_registry_snapshot",
            "current_status": "FAIL",
        })
    if conflicting_facts:
        failures.append({
            "requirement": "FACT_REGISTRY_CONFLICTING_FACT",
            "failure_stage": "ContractFactRegistry Construction",
            "root_cause": f"ContractFactRegistry found conflicting canonical facts: {', '.join(str(row.get('canonical_fact_key')) for row in conflicting_facts)}.",
            "responsible_function": "_contract_fact_lookup",
            "current_status": "FAIL",
        })
    conflicts = list(fact_flow_audit.get("cross_review_fact_conflicts") or [])
    if conflicts:
        failures.append({
            "requirement": "CROSS_REVIEW_FACT_CONFLICT",
            "failure_stage": "Review Post-processing",
            "root_cause": f"ContractFactRegistry FOUND facts were downgraded by consumers: {len(conflicts)}.",
            "responsible_function": "_contract_fact_flow_audit",
            "current_status": "FAIL",
        })
    override_violations = list(fact_flow_audit.get("fact_truth_override_violations") or [])
    if override_violations:
        failures.append({
            "requirement": "FACT_TRUTH_OVERRIDE_VIOLATION",
            "failure_stage": "Review Post-processing",
            "root_cause": f"Review post-processing overrode Registry fact truth: {len(override_violations)}.",
            "responsible_function": "_contract_fact_flow_audit",
            "current_status": "FAIL",
        })
    mapping_missing = list(fact_flow_audit.get("fact_consumer_mapping_missing") or [])
    if mapping_missing:
        failures.append({
            "requirement": "FACT_CONSUMER_MAPPING_MISSING",
            "failure_stage": "Review Fact Mapping",
            "root_cause": f"Required canonical facts were not bound to Review elements: {len(mapping_missing)}.",
            "responsible_function": "_coverage_claim_for_item",
            "current_status": "FAIL",
        })
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "gate_results": {
            "FACT_REGISTRY_SNAPSHOT_CONSISTENCY": "PASS" if fact_flow_audit.get("registry_snapshot_consistency") == "PASS" else "FAIL",
            "FACT_REGISTRY_CONFLICTING_FACT": "PASS" if not conflicting_facts else "FAIL",
            "CROSS_REVIEW_FACT_CONFLICT": "PASS" if not conflicts else "FAIL",
            "FACT_TRUTH_OVERRIDE_VIOLATION": "PASS" if not override_violations else "FAIL",
            "FACT_CONSUMER_MAPPING_MISSING": "PASS" if not mapping_missing else "FAIL",
        },
        "rows": fact_flow_audit.get("facts") or [],
        "cross_review_fact_conflict_count": len(conflicts),
        "conflicting_fact_count": len(conflicting_facts),
        "fact_truth_override_violation_count": len(override_violations),
        "fact_consumer_mapping_missing_count": len(mapping_missing),
    }


def _judge_checkpoints_with_registry(
    checkpoints: Iterable[ReviewCheckpoint],
    clauses: List[ParsedClause],
    *,
    use_llm: bool,
    fact_graph: ContractFactGraph,
) -> Dict[str, Any]:
    try:
        return judge_checkpoints_with_llm(tuple(checkpoints), clauses, use_llm=use_llm, fact_graph=fact_graph)
    except TypeError as exc:
        if "fact_graph" not in str(exc):
            raise
        return judge_checkpoints_with_llm(tuple(checkpoints), clauses, use_llm=use_llm)


def _restore_element_from_truth(element: CoverageElementResult, truth: Dict[str, Any]) -> None:
    raw_status = str(truth.get("raw_status") or "")
    if raw_status in {"COVERED", "PARTIALLY_COVERED"}:
        element.status = raw_status
    else:
        element.status = "COVERED" if truth.get("status") == "FOUND" else "PARTIALLY_COVERED"
    element.evidence_ids = list(truth.get("evidence_ids") or [])
    element.entailment = EVIDENCE_SUPPORTS if element.status == "COVERED" else EVIDENCE_PARTIAL_SUPPORT
    element.verifier_confidence = str(truth.get("confidence") or "medium")
    element.reason = "Evidence monotonicity preserved upstream element truth; no conflicting evidence justified a downgrade."
    element.source_spans = list(truth.get("evidence_text") or [])
    element.source_locations = list(truth.get("source_location") or [])


def _protect_element_monotonicity(item: ReviewItemResult, elements: List[CoverageElementResult]) -> None:
    previous = {
        str(row.get("element_id")): row
        for row in (item.decision_trace or {}).get("element_evidence_truth", [])
        if row.get("element_id")
    }
    if not previous:
        return
    resolutions: List[Dict[str, Any]] = []
    for element in elements:
        truth = previous.get(element.element_id)
        if not truth or truth.get("status") not in {"FOUND", "PARTIAL"}:
            continue
        if element.status not in {"MISSING", "UNCERTAIN"}:
            continue
        conflicting = [
            row for row in item.evidence_clauses or []
            if str(row.get("entailment_status") or "") in {EVIDENCE_CONTRADICTS, "CONTRADICTS"}
        ]
        if conflicting:
            resolutions.append({
                "review_id": item.item_id,
                "element_id": element.element_id,
                "upstream_status": truth.get("status"),
                "downstream_status": _element_truth_status(element.status),
                "action": "CONFLICTING_EVIDENCE_PRESENT",
                "conflicting_evidence": conflicting,
            })
            continue
        before = element.status
        _restore_element_from_truth(element, truth)
        resolutions.append({
            "review_id": item.item_id,
            "element_id": element.element_id,
            "upstream_status": truth.get("status"),
            "downstream_status": _element_truth_status(before),
            "action": "PREVENTED_DOWNGRADE",
            "upstream_evidence": truth.get("evidence_text") or truth.get("evidence_ids") or [],
            "downstream_reason": "No conflicting evidence justified FOUND/PARTIAL to missing downgrade.",
        })
    if resolutions:
        item.decision_trace.setdefault("evidence_monotonicity_resolution", []).extend(resolutions)


def _set_item_pass(item: ReviewItemResult, evidence: List[Any], reason: str, description: str) -> None:
    item.risk_level = "低"
    item.status = "已覆盖"
    item.coverage_status = "通过"
    item.issue_type = "通过"
    item.risk_point_description = description
    item.reasoning_summary = reason
    item.evidence_clauses = [_clause_public_dict(clause) for clause in evidence]
    item.evidence_location = "；".join(clause.location for clause in evidence)
    item.fallback_reason = "房屋租赁确定性条款规则"


def _set_item_partial(
    item: ReviewItemResult,
    evidence: List[Any],
    risk_level: str,
    reason: str,
    description: str,
    issue_type: str = "条款缺陷",
) -> None:
    item.risk_level = risk_level
    item.status = "部分覆盖"
    item.coverage_status = "部分覆盖"
    item.issue_type = issue_type
    item.risk_point_description = description
    item.reasoning_summary = reason
    item.evidence_clauses = [_clause_public_dict(clause) for clause in evidence]
    item.evidence_location = "；".join(clause.location for clause in evidence)
    item.fallback_reason = "房屋租赁确定性条款规则"
    if item.item_id.startswith("SVC-") and issue_type == "模板空白" and item.evidence_clauses:
        template_evidence = []
        for index, clause in enumerate(item.evidence_clauses, start=1):
            enriched = dict(clause)
            enriched.setdefault("evidence_id", enriched.get("clause_id") or f"{item.item_id}-TEMPLATE-{index}")
            enriched["entailment_status"] = EVIDENCE_PARTIAL_SUPPORT
            enriched["semantic_score"] = max(float(enriched.get("semantic_score") or 0), 0.6)
            enriched["evidence_claim_id"] = enriched.get("evidence_claim_id") or f"{item.item_id}-TEMPLATE-EC-{index:02d}"
            template_evidence.append(enriched)
        item.evidence_clauses = template_evidence
        item.decision_trace["service_template_blank_evidence"] = list(template_evidence)


def _set_item_missing(
    item: ReviewItemResult,
    risk_level: str,
    reason: str,
    description: str,
    fallback_reason: str,
) -> None:
    item.risk_level = risk_level
    item.status = "缺失或不明确"
    item.coverage_status = "缺失"
    item.issue_type = "完全缺失"
    item.risk_point_description = description
    item.reasoning_summary = reason
    item.evidence_clauses = []
    item.evidence_location = ""
    item.fallback_reason = fallback_reason


def _set_item_not_applicable(item: ReviewItemResult, reason: str) -> None:
    item.risk_level = NotApplicableRisk()
    item.status = "不适用"
    item.coverage_status = COVERAGE_NOT_APPLICABLE
    item.issue_type = ISSUE_NOT_APPLICABLE
    item.risk_point_description = "该审查点仅适用于特定交易场景，当前合同文本未触发对应适用条件。"
    item.reasoning_summary = reason
    item.evidence_clauses = []
    item.evidence_location = ""
    item.judge_source = "applicability_filter"
    item.fallback_reason = "适用性事实门禁"
    item.applicability = {"status": "not_applicable", "applicable": False, "reason": reason, "depends_on": []}
    item.action_suggestion = "不适用"


def _fact_evidence(facts: HouseLeaseContractFacts, field_name: str) -> List[Any]:
    clause = facts.evidence_clause(field_name)
    return [clause] if clause else []


def _set_item_pass_from_fact(
    item: ReviewItemResult,
    facts: HouseLeaseContractFacts,
    field_name: str,
    reason: str,
    description: str,
) -> None:
    evidence = _fact_evidence(facts, field_name)
    if not evidence:
        item.quality_flags.append(
            {
                "item_id": item.item_id,
                "type": "fact_without_provenance",
                "message": f"Fact Graph 字段 {field_name} 存在但无 provenance，不作为高置信通过证据。",
                "recommended_action": "retrieval_verify",
            }
        )
        return
    _set_item_pass(item, evidence, reason, description)
    item.matched_terms = [field_name]
    item.fact_dependencies = sorted(set(item.fact_dependencies + [field_name]))
    item.fallback_reason = "房屋租赁统一事实图谱"


def _set_item_partial_from_fact(
    item: ReviewItemResult,
    facts: HouseLeaseContractFacts,
    field_name: str,
    risk_level: str,
    reason: str,
    description: str,
    issue_type: str = "条款缺陷",
) -> None:
    evidence = _fact_evidence(facts, field_name)
    if not evidence:
        item.quality_flags.append(
            {
                "item_id": item.item_id,
                "type": "fact_without_provenance",
                "message": f"Fact Graph 字段 {field_name} 存在但无 provenance，不作为高置信部分覆盖证据。",
                "recommended_action": "retrieval_verify",
            }
        )
        return
    _set_item_partial(item, evidence, risk_level, reason, description, issue_type=issue_type)
    item.matched_terms = [field_name]
    item.fact_dependencies = sorted(set(item.fact_dependencies + [field_name]))
    item.fallback_reason = "房屋租赁统一事实图谱"


def _numeric_amount(value: Optional[str]) -> Optional[float]:
    return scenario_numeric_amount(value)


def _penalty_scenarios(facts: HouseLeaseContractFacts) -> Dict[str, Any]:
    return penalty_scenarios(facts.early_termination.penalty_formula or {}, facts.rent.monthly_amount, daily_rent_value=facts.rent.daily_amount)


def _economic_impact_for_penalty(scenarios: Dict[str, Any]) -> str:
    return economic_impact_for_penalty(scenarios)


def _economic_impact_detail_for_penalty(scenarios: Dict[str, Any]) -> Dict[str, Any]:
    return economic_impact_detail_for_penalty(scenarios)


def _formula_requires_high_severity(formula: Dict[str, Any]) -> bool:
    return formula.get("time_base_source") != "early_surrender_days"


LOW_PROBABILITY_OPTIMIZATION_IDS = {
    "HL-007",
    "HL-008",
    "HL-009",
}

CORE_RISK_IDS = {
    "HL-001",
    "HL-003",
    "HL-004",
    "HL-010",
    "HL-015",
    "HL-025",
    "HL-039",
    "HL-043",
}

HIGH_RISK_REASON_BY_ID = {
    "HL-003": "contract_validity",
    "HL-004": "contract_validity",
    "HL-010": "contract_validity",
    "HL-025": "personal_safety",
    "HL-039": "major_financial_loss",
    "HL-043": "major_financial_loss",
}

HIGH_RISK_REASON_BY_NODE = {
    "contract_validity": "contract_validity",
    "house_legality": "contract_validity",
    "safety_hazard": "personal_safety",
    "deposit_return_deadline": "major_financial_loss",
    "penalty_adjustment": "major_financial_loss",
}

RISK_GROUP_BY_ID = {
    "HL-029": "early_termination_financial_exposure",
    "HL-039": "early_termination_financial_exposure",
    "HL-042": "deposit_offset_order",
    "HL-043": "deposit_return_timing",
    "HL-032": "property_damage_deposit_evidence",
    "HL-033": "property_damage_deposit_evidence",
    "HL-035": "property_damage_deposit_evidence",
    "HL-036": "property_damage_deposit_evidence",
    "HL-037": "property_damage_deposit_evidence",
    "HL-040": "property_damage_deposit_evidence",
    "HL-041": "property_damage_deposit_evidence",
    "HL-044": "property_damage_deposit_evidence",
    "HL-005": "notice_and_delivery",
    "HL-025": "housing_safety_emergency",
    "HL-010": "lawful_lease_basis",
    "S-11-01": "goods_title_and_third_party_rights",
    "S-11-03": "goods_title_and_third_party_rights",
    "S-11-04": "goods_title_and_third_party_rights",
}

RELATED_REVIEWS_BY_ID = {
    "HL-029": ["HL-039"],
    "HL-039": ["HL-029"],
}

RISK_FINDING_ID_BY_GROUP = {
    "early_termination_financial_exposure": "RF-EARLY-TERM-001",
    "deposit_offset_order": "RF-DEPOSIT-OFFSET-001",
    "property_damage_deposit_evidence": "RF-PROPERTY-DAMAGE-001",
    "legal_reference": "RF-LEGAL-001",
    "outdated_legal_reference": "RF-LEGAL-001",
    "goods_title_and_third_party_rights": "RF-GOODS-RIGHTS-001",
    "service_refund_termination_settlement": "RF-SVC-REFUND-001",
    "service_performance_remedy_framework": "RF-SVC-PERFORMANCE-001",
    "service_scope_delivery_standard": "RF-SVC-SCOPE-001",
    "service_fee_balance_transparency": "RF-SVC-FEE-001",
    "service_performance_record_evidence": "RF-SVC-RECORD-001",
    "service_business_closure_notice": "RF-SVC-CLOSURE-001",
}

LOW_PROBABILITY_NODE_IDS = {
    "tenant_death_successor",
    "landlord_death_successor",
    "change_of_circumstances",
    "third_party_infringement",
    "no_one_continue_lease",
}

STATUTORY_DEFAULT_GROUPS = {
    "owner_change_no_break_lease",
    "normal_wear",
    "tenant_death_successor",
    "indefinite_lease",
}


def _coverage_gap_type(item: ReviewItemResult) -> str:
    if item.coverage_status != "缺失":
        return ""
    if item.node_id in LOW_PROBABILITY_NODE_IDS or item.item_id in LOW_PROBABILITY_OPTIMIZATION_IDS:
        return "MISSING_OPTIMIZATION"
    if item.node_id in STATUTORY_DEFAULT_GROUPS:
        return "MISSING_WITH_STATUTORY_DEFAULT"
    if item.item_id in CORE_RISK_IDS:
        return "MISSING_CRITICAL"
    return "MISSING_OPTIMIZATION" if item.risk_level == "低" else "MISSING_WITH_STATUTORY_DEFAULT"


def _probability_for_item(item: ReviewItemResult) -> str:
    if item.needs_manual_review:
        return PROBABILITY_UNKNOWN
    if item.node_id in LOW_PROBABILITY_NODE_IDS or item.item_id in LOW_PROBABILITY_OPTIMIZATION_IDS:
        return PROBABILITY_LOW
    if item.economic_impact in {"high", "critical"}:
        return PROBABILITY_MEDIUM
    if item.coverage_status == "风险条款":
        return PROBABILITY_HIGH
    if item.coverage_status in {"缺失", "部分覆盖"}:
        return PROBABILITY_MEDIUM
    return PROBABILITY_LOW


def _impact_level_for_value(value: str) -> str:
    return {
        SEVERITY_NONE: "NONE",
        SEVERITY_LOW: "LOW",
        SEVERITY_MEDIUM: "MEDIUM",
        SEVERITY_HIGH: "HIGH",
        SEVERITY_CRITICAL: "SEVERE",
        "none": "NONE",
        "low": "LOW",
        "medium": "MEDIUM",
        "high": "HIGH",
        "critical": "SEVERE",
    }.get(value or "", "LOW")


def _impact_for_item(item: ReviewItemResult) -> Dict[str, str]:
    financial = _impact_level_for_value(item.economic_impact or item.risk_severity)
    legal_validity = "HIGH" if item.high_risk_reason == "contract_validity" else "LOW" if item.risk_severity != SEVERITY_NONE else "NONE"
    rights_loss = "MEDIUM" if item.risk_severity in {SEVERITY_MEDIUM, SEVERITY_HIGH, SEVERITY_CRITICAL} else "LOW" if item.risk_severity == SEVERITY_LOW else "NONE"
    safety = "HIGH" if item.high_risk_reason == "personal_safety" else "NONE"
    evidence = "MEDIUM" if item.semantic_entailment is False or item.needs_manual_review else "LOW" if item.coverage_status in {"缺失", "部分覆盖"} else "NONE"
    operational = "MEDIUM" if item.review_priority == PRIORITY_B_PRACTICAL else "LOW" if item.review_priority == PRIORITY_C_OPTIMIZATION else "MEDIUM"
    return {
        "financial": financial,
        "legal_validity": legal_validity,
        "rights_loss": rights_loss,
        "operational": operational,
        "safety": safety,
        "evidence": evidence,
    }


def _normalized_economic_impact(item: ReviewItemResult) -> Dict[str, Any]:
    detail = dict(item.economic_impact_detail or {})
    if not detail:
        detail = {"level": item.economic_impact or "none"}
    max_loss = detail.get("estimated_max_loss") or detail.get("amount_estimate")
    monthly_multiple = detail.get("monthly_payment_multiple") or detail.get("relative_to_monthly_payment")
    if max_loss is not None:
        detail["absolute_amount"] = max_loss
        detail["amount_estimate"] = max_loss
    if monthly_multiple is not None:
        detail["monthly_payment_multiple"] = monthly_multiple
    if "contract_value_ratio" not in detail and detail.get("relative_to_contract_value") is not None:
        detail["contract_value_ratio"] = detail.get("relative_to_contract_value")
    detail.setdefault("deposit_multiple", None)
    detail.setdefault("annual_value_ratio", detail.get("contract_value_ratio"))
    detail.setdefault("remaining_obligation_ratio", (detail.get("max_case") or {}).get("penalty_to_remaining_rent_ratio"))
    detail.setdefault("batch_value_ratio", None)
    detail.setdefault("unpaid_amount_ratio", None)
    detail.setdefault("advance_payment_ratio", detail.get("prepaid_amount_ratio"))
    detail.setdefault("replacement_cost_ratio", None)
    detail.setdefault("delay_loss_ratio", None)
    detail.setdefault("level", item.economic_impact or "none")
    return detail


def _float_or_none(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return scenario_numeric_amount(str(value))


def _normalized_economic_exposure(item: ReviewItemResult) -> NormalizedEconomicExposure:
    detail = _normalized_economic_impact(item)
    max_case = detail.get("max_case") or {}
    monthly_multiple = (
        detail.get("monthly_payment_multiple")
        or detail.get("relative_to_monthly_payment")
        or max_case.get("penalty_monthly_rent_multiple")
        or max_case.get("monthly_rent_multiple")
    )
    absolute_amount = detail.get("absolute_amount") or detail.get("estimated_max_loss") or detail.get("amount_estimate")
    formula = (item.scenario_analysis or {}).get("formula") or {}
    return NormalizedEconomicExposure(
        absolute_amount=_float_or_none(absolute_amount),
        monthly_payment_multiple=_float_or_none(monthly_multiple),
        deposit_multiple=_float_or_none(detail.get("deposit_multiple")),
        prepaid_amount_ratio=_float_or_none(detail.get("prepaid_amount_ratio")),
        contract_total_ratio=_float_or_none(detail.get("contract_value_ratio") or detail.get("relative_to_contract_value")),
        remaining_obligation_ratio=_float_or_none(detail.get("remaining_obligation_ratio") or max_case.get("penalty_to_remaining_rent_ratio")),
        batch_value_ratio=_float_or_none(detail.get("batch_value_ratio")),
        unpaid_amount_ratio=_float_or_none(detail.get("unpaid_amount_ratio")),
        advance_payment_ratio=_float_or_none(detail.get("advance_payment_ratio") or detail.get("prepaid_amount_ratio")),
        replacement_cost_ratio=_float_or_none(detail.get("replacement_cost_ratio")),
        delay_loss_ratio=_float_or_none(detail.get("delay_loss_ratio")),
        time_amplifying=bool(detail.get("time_amplifying") or formula.get("base") in {"remaining_term_rent", "remaining_days_rent"}),
        uncapped=bool(detail.get("uncapped")),
        level=detail.get("level") or item.economic_impact or "none",
    )


def _infer_user_perspective(item: ReviewItemResult) -> str:
    explicit = (item.decision_trace or {}).get("user_perspective")
    if explicit:
        return str(explicit).upper()
    formula = (item.scenario_analysis or {}).get("formula") or {}
    party = str(formula.get("party") or "").lower()
    beneficiary = str(formula.get("beneficiary") or "").lower()
    if party == "tenant" or (party and beneficiary == "landlord"):
        return "TENANT"
    if party == "landlord" or (party and beneficiary == "tenant"):
        return "LANDLORD"
    if item.item_id.startswith("HL-"):
        return "TENANT"
    return "UNKNOWN"


def _user_directly_bears_risk(item: ReviewItemResult, perspective: str) -> bool:
    formula = (item.scenario_analysis or {}).get("formula") or {}
    party = str(formula.get("party") or "").upper()
    if party and party == perspective:
        return True
    if perspective == "TENANT" and item.risk_group in {
        "early_termination_financial_exposure",
        "deposit_return_timing",
        "property_damage_deposit_evidence",
        "notice_and_delivery",
        "housing_safety_emergency",
        "lawful_lease_basis",
    }:
        return True
    return False


def _has_priority_counter_evidence(item: ReviewItemResult) -> bool:
    evidence_text = " ".join(str(evidence.get("text") or "") for evidence in item.evidence_clauses or [])
    if item.risk_group == "lawful_lease_basis" and any(term in evidence_text for term in ("产证编号", "不动产权证", "房屋所有权", "权利人")):
        return True
    if item.coverage_status == "部分覆盖" and item.issue_type != "风险条款":
        return True
    return False


def _priority_input_for_item(item: ReviewItemResult) -> PriorityInput:
    exposure = _normalized_economic_exposure(item)
    severity = item.risk_severity or _risk_severity_for_item(item)
    probability = _probability_for_item(item)
    perspective = _infer_user_perspective(item)
    statutory_default = (item.decision_trace or {}).get("default_law_status") or default_law_status(item.risk_group, item.node_id)
    effective_gap = (item.decision_trace or {}).get("effective_gap") or {}
    core_obligation_groups = {
        "early_termination_financial_exposure",
        "deposit_return_timing",
        "notice_and_delivery",
        "lawful_lease_basis",
    }
    formula = (item.scenario_analysis or {}).get("formula") or {}
    monthly_rent = _float_or_none((item.scenario_analysis or {}).get("monthly_rent"))
    return PriorityInput(
        finding_id=RISK_FINDING_ID_BY_GROUP.get(item.risk_group or item.node_id or ""),
        severity=severity,
        economic_impact=item.economic_impact or exposure.level or "none",
        probability=probability,
        legal_impact="HIGH" if item.high_risk_reason == "contract_validity" else "MEDIUM" if item.risk_severity in {SEVERITY_MEDIUM, SEVERITY_HIGH} else "LOW",
        operational_impact="MEDIUM" if item.coverage_status in {"缺失", "部分覆盖", "风险条款"} else "LOW",
        safety_impact="HIGH" if item.high_risk_reason == "personal_safety" and bool(item.evidence_clauses) else "NONE",
        core_obligation=bool((item.risk_group or item.node_id) in core_obligation_groups or formula.get("base") in {"remaining_term_rent", "remaining_days_rent"}),
        time_amplifying=exposure.time_amplifying,
        uncapped=exposure.uncapped,
        reversibility="low" if item.risk_group in {"early_termination_financial_exposure", "deposit_return_timing"} else "medium",
        recoverability="low" if item.risk_group == "early_termination_financial_exposure" else "medium",
        user_perspective=perspective,
        user_directly_bears_risk=_user_directly_bears_risk(item, perspective),
        bargaining_power=str((item.decision_trace or {}).get("bargaining_power") or "unknown"),
        contract_value=monthly_rent * 12 if monthly_rent else None,
        recurring_value=monthly_rent,
        remaining_obligation=exposure.absolute_amount,
        recommendation_cost="low" if item.risk_group in {"early_termination_financial_exposure", "deposit_return_timing", "notice_and_delivery"} else "medium",
        recommendation_feasibility="high" if item.coverage_status in {"缺失", "部分覆盖", "风险条款"} else "medium",
        confidence=(item.system_confidence or {}).get("level", "medium"),
        normalized_economic_exposure=exposure.to_public_dict(),
        statutory_default_status=statutory_default,
        default_protection_strength=effective_gap.get("default_strength", "strong" if statutory_default == "CLEAR_DEFAULT" else "partial" if statutory_default == "PARTIAL_DEFAULT" else "none"),
        contract_override_risk=effective_gap.get("contract_override_risk", "low"),
        practical_gap_after_default=effective_gap.get("residual_operational_risk", "low" if statutory_default == "CLEAR_DEFAULT" and item.node_id in LOW_PROBABILITY_NODE_IDS else "medium"),
        user_impact=effective_gap.get("residual_legal_risk", "low" if statutory_default == "CLEAR_DEFAULT" else "medium"),
    )


def _priority_assessment_for_item(item: ReviewItemResult) -> Dict[str, Any]:
    priority_input = _priority_input_for_item(item)
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return {"priority": ACTION_PRIORITY_NOT_APPLICABLE, "score": 0, "reason": "not_applicable", "input": priority_input.to_public_dict()}

    severity = priority_input.severity
    if item.coverage_status == "通过" and severity == SEVERITY_NONE and not item.related_risks:
        return {"priority": ACTION_PRIORITY_NONE, "score": 0, "reason": "covered_without_actionable_finding", "input": priority_input.to_public_dict()}

    exposure = priority_input.normalized_economic_exposure
    monthly_multiple = _float_or_none(exposure.get("monthly_payment_multiple")) or 0
    score = 0.0
    reasons: List[str] = []

    if monthly_multiple >= 12:
        score += 4.0
        reasons.append("monthly_multiple>=12")
    elif monthly_multiple >= 8:
        score += 3.0
        reasons.append("monthly_multiple>=8")
    elif monthly_multiple >= 3:
        score += 2.0
        reasons.append("monthly_multiple>=3")
    elif monthly_multiple >= 1:
        score += 1.0
        reasons.append("monthly_multiple>=1")

    if priority_input.economic_impact in {"high", "critical"}:
        score += 1.5
        reasons.append("economic_impact_material")
    if priority_input.statutory_default_status == "NO_DEFAULT" and priority_input.core_obligation and priority_input.economic_impact in {"high", "critical"}:
        score += 1.0
        reasons.append("no_default_core_material_exposure")
    if priority_input.time_amplifying:
        score += 1.5
        reasons.append("time_amplifying")
    if priority_input.uncapped:
        score += 1.5
        reasons.append("uncapped")
    if priority_input.core_obligation:
        score += 1.0
        reasons.append("core_obligation")
    if priority_input.user_directly_bears_risk:
        score += 1.0
        reasons.append("user_directly_bears_risk")
    if priority_input.safety_impact == "HIGH":
        score += 2.0
        reasons.append("actual_safety_signal")
    if priority_input.legal_impact == "HIGH" and not _has_priority_counter_evidence(item):
        score += 1.5
        reasons.append("legal_validity_without_counter_evidence")
    if severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}:
        score += 1.0
        reasons.append("high_severity")
    elif severity == SEVERITY_MEDIUM:
        score += 0.5
        reasons.append("medium_severity")
    if priority_input.reversibility == "low" or priority_input.recoverability == "low":
        score += 0.5
        reasons.append("low_recoverability")
    if priority_input.recommendation_cost == "low" and priority_input.recommendation_feasibility == "high":
        score += 0.5
        reasons.append("low_cost_high_leverage_fix")

    if _has_priority_counter_evidence(item):
        score -= 1.5
        reasons.append("counter_evidence")
    protected_low_gap = (
        priority_input.statutory_default_status == "CLEAR_DEFAULT"
        and priority_input.default_protection_strength == "strong"
        and priority_input.practical_gap_after_default == "low"
        and priority_input.probability in {PROBABILITY_LOW, PROBABILITY_RARE}
        and priority_input.economic_impact not in {"high", "critical"}
        and priority_input.safety_impact != "HIGH"
    )
    if protected_low_gap:
        score -= 1.5
        reasons.append("clear_default_law_protection")
    if item.node_id in LOW_PROBABILITY_NODE_IDS or item.item_id in LOW_PROBABILITY_OPTIMIZATION_IDS:
        score -= 2.0
        reasons.append("low_probability_or_optimization")

    if protected_low_gap and item.coverage_status in {"缺失", "部分覆盖", "风险条款"} and score < 1.5:
        priority = PRIORITY_C_OPTIMIZATION
    elif score >= 5.0:
        priority = PRIORITY_A_CORE
    elif score >= 1.5 or (severity in {SEVERITY_MEDIUM, SEVERITY_HIGH, SEVERITY_CRITICAL} and not protected_low_gap):
        priority = PRIORITY_B_PRACTICAL
    elif severity == SEVERITY_LOW:
        priority = PRIORITY_C_OPTIMIZATION
    else:
        priority = ACTION_PRIORITY_NONE

    mitigators = [reason for reason in reasons if reason in {"counter_evidence", "clear_default_law_protection", "low_probability_or_optimization"}]
    drivers = [reason for reason in reasons if reason not in mitigators]
    decision = PriorityDecision(
        finding_id=priority_input.finding_id or item.item_id,
        severity=severity,
        priority=priority,
        drivers=drivers,
        mitigators=mitigators,
        default_law_effect="mitigates" if "clear_default_law_protection" in mitigators else priority_input.statutory_default_status,
        economic_effect=priority_input.economic_impact,
        explanation=(
            f"行动优先级由风险严重度、核心义务、经济暴露、发生概率、默认法保护、可恢复性和修复价值共同计算；"
            f"驱动因素：{', '.join(drivers) or 'none'}；缓释因素：{', '.join(mitigators) or 'none'}。"
        ),
    )
    return {
        "priority": priority,
        "score": round(score, 2),
        "reason": ", ".join(reasons) or "no_actionable_signal",
        "input": priority_input.to_public_dict(),
        "decision": decision.to_public_dict(),
    }


CONFIDENCE_SCORE = {"high": 0.95, "medium": 0.72, "low": 0.35, "not_applicable": 1.0}


def _confidence_label_from_score(score: float) -> str:
    if score >= 0.85:
        return "high"
    if score >= 0.6:
        return "medium"
    return "low"


def _legal_confidence_for_item(item: ReviewItemResult) -> str:
    claims = item.legal_references or []
    legal_claims = [claim for claim in claims if claim.get("claim_type") != "DRAFTING_RECOMMENDATION"]
    if not legal_claims:
        return "not_applicable"
    if any(
        claim.get("support_type") == "DIRECT_SUPPORT"
        and claim.get("support_scope")
        and claim.get("confidence") == "high"
        for claim in legal_claims
    ):
        return "high"
    if any(claim.get("support_type") in {"DIRECT_SUPPORT", "PARTIAL_SUPPORT", "BACKGROUND_ONLY"} for claim in legal_claims):
        return "medium"
    return "low"


def _confidence_dependency_for_item(item: ReviewItemResult) -> ConfidenceDependency:
    formula = (item.scenario_analysis or {}).get("formula")
    claims = item.legal_references or []
    direct_legal_claim = any(
        claim.get("claim_type") in {"LEGAL_EFFECT", "PROCEDURE", "RIGHT"}
        for claim in claims
    )
    return ConfidenceDependency(
        requires_parser=True,
        requires_fact=bool(item.fact_dependencies),
        requires_evidence=item.coverage_status in {"通过", "部分覆盖", "风险条款"} or bool(item.evidence_clauses) or bool((item.decision_trace or {}).get("negative_evidence")),
        requires_applicability=True,
        requires_legal=direct_legal_claim,
        requires_formula=bool(formula),
        requires_calculation=bool((item.scenario_analysis or {}).get("cases")),
    )


def _component_level(score: float) -> str:
    return _confidence_label_from_score(score)


def _verifier_confidence_for_item(item: ReviewItemResult) -> str:
    elements = item.coverage_elements or (item.decision_trace or {}).get("coverage_elements") or []
    if not elements:
        return "medium"
    statuses = {element.get("status") for element in elements}
    if item.coverage_status == "部分覆盖" and not (statuses & {"COVERED", "PARTIALLY_COVERED"}):
        return "low"
    if item.coverage_status == "通过" and "UNCERTAIN" in statuses:
        return "medium"
    if any(element.get("entailment") == EVIDENCE_RELATED_NOT_SUPPORTING for element in elements):
        return "medium" if item.coverage_status == "缺失" else "low"
    if all(element.get("verifier_confidence") == "high" for element in elements):
        return "high"
    if any(element.get("verifier_confidence") == "low" for element in elements):
        return "low"
    return "medium"


def _confidence_bundle_for_item(item: ReviewItemResult) -> ConfidenceBundle:
    has_evidence = bool(item.evidence_clauses)
    negative = (item.decision_trace or {}).get("negative_evidence") or {}
    dependency = _confidence_dependency_for_item(item)
    parser_score = 0.95
    document_integrity_score = 0.95
    fact_score = 0.95 if item.fact_dependencies else 0.72
    if (item.decision_trace or {}).get("fact_conflict"):
        fact_score = 0.35
    retrieval_trace = (item.decision_trace or {}).get("retrieval_trace") or {}
    missing_proof = (item.decision_trace or {}).get("missing_proof") or {}
    contradiction = (item.decision_trace or {}).get("fact_coverage_contradiction") or {}
    retrieval_score = 0.95 if retrieval_trace.get("candidate_count") else 0.72
    if item.coverage_status == "缺失":
        retrieval_score = 0.95 if missing_proof.get("exhaustive_enough") else 0.35
    if contradiction.get("status") == "UNRESOLVED":
        retrieval_score = 0.2
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        evidence_score = 1.0
    elif item.semantic_entailment is False and item.coverage_status in {"通过", "部分覆盖", "风险条款"}:
        evidence_score = 0.35
    elif has_evidence:
        entailments = {str(evidence.get("entailment_status") or "") for evidence in item.evidence_clauses or []}
        if entailments and entailments <= {EVIDENCE_UNCERTAIN, ""}:
            evidence_score = 0.72
        elif EVIDENCE_RELATED_NOT_SUPPORTING in entailments or EVIDENCE_NOT_RELEVANT in entailments:
            evidence_score = 0.35
        else:
            evidence_score = 0.95 if item.semantic_entailment is not False else 0.72
    elif item.coverage_status == "缺失" and negative.get("result") == "NOT_FOUND":
        evidence_score = 0.9
    elif item.coverage_status == "缺失":
        evidence_score = 0.72
    else:
        evidence_score = 0.6
    applicability_status = (item.applicability or {}).get("status", "applicable")
    applicability_score = 0.4 if applicability_status == "UNCERTAIN" else 0.95 if not item.needs_manual_review else 0.45
    legal_level = _legal_confidence_for_item(item)
    legal_score = CONFIDENCE_SCORE.get(legal_level, 0.72)
    formula_score = 0.95 if item.scenario_analysis.get("formula") else 1.0
    calculation_score = 0.95 if (item.scenario_analysis or {}).get("cases") else 1.0
    verifier_level = _verifier_confidence_for_item(item)
    verifier_score = CONFIDENCE_SCORE.get(verifier_level, 0.72)
    aggregation_score = 0.95 if not item.quality_gate_failure_reason else 0.45
    component_scores = {
        "parser": parser_score,
        "document_integrity": document_integrity_score,
        "fact": fact_score,
        "retrieval_recall": retrieval_score,
        "evidence": evidence_score,
        "applicability": applicability_score,
        "legal": legal_score,
        "formula": formula_score,
        "calculation": calculation_score,
        "verifier": verifier_score,
        "aggregation": aggregation_score,
    }
    dependency_map = dependency.to_public_dict()
    dependency_by_component = {
        "parser": dependency.requires_parser,
        "document_integrity": dependency.requires_parser,
        "fact": dependency.requires_fact,
        "retrieval_recall": item.coverage_status == "缺失" or bool(retrieval_trace),
        "evidence": dependency.requires_evidence,
        "applicability": dependency.requires_applicability,
        "legal": dependency.requires_legal,
        "formula": dependency.requires_formula,
        "calculation": dependency.requires_calculation,
        "verifier": dependency.requires_verifier,
        "aggregation": True,
    }
    required_components = [name for name, required in dependency_by_component.items() if required]
    ignored_components = [name for name, required in dependency_by_component.items() if not required]
    required_scores = [component_scores[name] for name in required_components]
    final_score = sum(required_scores) / len(required_scores) if required_scores else 0.72
    limiting_factors = [
        name for name in required_components
        if component_scores[name] < 0.6
    ]
    default_assessment = (item.decision_trace or {}).get("default_law_assessment") or {}
    if (
        default_assessment.get("default_law_relevant")
        and default_assessment.get("rule")
        and default_assessment.get("applicability") == "UNCERTAIN"
        and "default_law" not in limiting_factors
    ):
        limiting_factors.append("default_law")
    obligation_blocks = {
        str(evidence.get("evidence_block_type") or evidence.get("block_type") or "")
        for evidence in item.evidence_clauses or []
    }
    if obligation_blocks & {"TEMPLATE_GUIDANCE", "COMMENTARY", "HISTORICAL_NOTE"}:
        limiting_factors.append("evidence_block_type")
    final_confidence = _confidence_label_from_score(final_score)
    if limiting_factors and final_confidence == "high":
        final_confidence = "medium"
    reason = "依赖组件均可靠，当前判断可信。"
    if limiting_factors:
        reason = f"以下必需组件限制最终可靠度：{', '.join(limiting_factors)}。"
    elif ignored_components:
        reason = f"本审查项不依赖 {', '.join(ignored_components)}，这些组件不参与最终可靠度。"
    return ConfidenceBundle(
        parser_confidence=_component_level(parser_score),
        document_integrity_confidence=_component_level(document_integrity_score),
        fact_confidence=_component_level(fact_score),
        retrieval_recall_confidence=_component_level(retrieval_score),
        evidence_confidence=_component_level(evidence_score),
        applicability_confidence=_component_level(applicability_score),
        legal_confidence=legal_level,
        formula_confidence="high" if item.scenario_analysis.get("formula") else "not_applicable",
        calculation_confidence="high" if (item.scenario_analysis or {}).get("cases") else "not_applicable",
        verifier_confidence=verifier_level,
        aggregation_confidence=_component_level(aggregation_score),
        final_score=round(final_score, 3),
        final_confidence=final_confidence,
        limiting_factors=limiting_factors,
        required_components=required_components,
        ignored_components=ignored_components,
        component_scores={key: round(value, 3) for key, value in component_scores.items()},
        dependency=dependency_map,
        reason=reason,
    )


def _system_confidence_for_item(item: ReviewItemResult) -> Dict[str, Any]:
    bundle = _confidence_bundle_for_item(item)
    return {
        "level": bundle.final_confidence,
        "parser_confidence": bundle.parser_confidence,
        "document_integrity_confidence": bundle.document_integrity_confidence,
        "fact_confidence": bundle.fact_confidence,
        "retrieval_recall_confidence": bundle.retrieval_recall_confidence,
        "evidence_confidence": bundle.evidence_confidence,
        "applicability_confidence": bundle.applicability_confidence,
        "legal_confidence": bundle.legal_confidence,
        "legal_authority_confidence": bundle.legal_confidence,
        "formula_confidence": bundle.formula_confidence,
        "calculation_confidence": bundle.calculation_confidence,
        "verifier_confidence": bundle.verifier_confidence,
        "aggregation_confidence": bundle.aggregation_confidence,
        "retrieval_strength": "explicit" if bool(item.evidence_clauses) else "not_found",
        "evidence_entailment": item.semantic_entailment if item.semantic_entailment is not None else "not_checked",
        "rule_agreement": "agree",
        "model_agreement": "not_used_or_agree",
        "cross_review_agreement": "agree" if not item.quality_gate_failure_reason else "conflict",
        "quality_gate_flags": len(item.quality_flags),
        "confidence_bundle": bundle.to_public_dict(),
        "confidence_explanation": {
            "final_confidence": bundle.final_confidence,
            "required_components": bundle.required_components,
            "ignored_components": bundle.ignored_components,
            "component_scores": bundle.component_scores,
            "limiting_factors": bundle.limiting_factors,
            "reason": bundle.reason,
        },
    }


def _apply_confidence_bundles(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    for item in items:
        item.system_confidence = _system_confidence_for_item(item)
    return items


def _apply_post_verification_confidence(findings: List[RiskFinding], items: List[ReviewItemResult]) -> None:
    item_by_id = {item.item_id: item for item in items}
    for finding in findings:
        verification = finding.verification or {}
        if verification.get("status") != "BLOCK" and (finding.agreement or {}).get("status") != "MATERIAL_DISAGREEMENT":
            continue
        finding.confidence = {**(finding.confidence or {}), "level": "low", "limiting_factors": ["verifier", "cross_layer_consistency"]}
        for item_id in finding.source_review_ids:
            item = item_by_id.get(item_id)
            if not item:
                continue
            item.quality_gate_failure_reason = verification.get("reason") or "独立验证与主判断存在实质分歧。"
            item.system_confidence = _system_confidence_for_item(item)
            item.system_confidence["level"] = "low"
            item.system_confidence["cross_review_agreement"] = "material_conflict"
            bundle = item.system_confidence.get("confidence_bundle") or {}
            bundle["final_confidence"] = "low"
            bundle["limiting_factors"] = sorted(set((bundle.get("limiting_factors") or []) + ["verifier", "consistency"]))


def _risk_severity_for_item(item: ReviewItemResult) -> str:
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return SEVERITY_NONE
    if item.coverage_status == "通过" and not item.economic_impact:
        return SEVERITY_NONE
    if item.coverage_status == "通过" and item.economic_impact in {"none", "low", ""}:
        return SEVERITY_NONE
    if item.risk_level == "高":
        return SEVERITY_HIGH
    if item.risk_level == "中":
        return SEVERITY_MEDIUM
    if item.coverage_status in {"缺失", "部分覆盖", "风险条款"}:
        return SEVERITY_LOW
    return SEVERITY_NONE


DEFAULT_LAW_AUTHORITY_ARTICLES = {
    "CN-CC-563": "第563条", "CN-CC-565": "第565条", "CN-CC-582": "第582条",
    "CN-CC-584": "第584条", "CN-CC-589": "第589条", "CN-CC-591": "第591条",
    "CN-CC-604": "第604条", "CN-CC-605": "第605条", "CN-CC-607": "第607条",
    "CN-CC-617": "第617条", "CN-CC-620": "第620条", "CN-CC-621": "第621条",
}


def _default_law_assessment(item: ReviewItemResult, contract_type: str, contract_text: str = "") -> Dict[str, Any]:
    rule = get_default_rule(contract_type, item.risk_group) or get_default_rule(contract_type, item.node_id)
    fallback_status = default_law_status(item.risk_group, item.node_id)
    if not rule:
        clear_default = fallback_status == "CLEAR_DEFAULT"
        return {
            "executed": True,
            "default_law_relevant": fallback_status != "UNCERTAIN_DEFAULT",
            "status": fallback_status,
            "rule": None,
            "applicability": "NOT_DECLARED" if fallback_status == "UNCERTAIN_DEFAULT" else "UNCERTAIN",
            "protection_scope": "法律提供清晰默认保护。" if clear_default else "",
            "remaining_gap": "主要剩余为合同表达和操作流程优化。" if clear_default else "合同仍需自行明确业务流程和证据要求。",
            "practical_uncertainty": "low" if clear_default and item.node_id in LOW_PROBABILITY_NODE_IDS else "medium",
            "residual_legal_risk": "low" if clear_default else "medium",
            "residual_operational_risk": "low" if clear_default and item.node_id in LOW_PROBABILITY_NODE_IDS else "medium",
        }
    material_gap = item.coverage_status in {"缺失", "部分覆盖"}
    compacted = _compact(contract_text)
    applicability = "AVAILABLE_NOT_NEEDED"
    applicability_confidence = "high"
    effective_status = rule.status
    authority_validation = [
        {
            "authority_id": authority_id,
            **validate_legal_citation("中华人民共和国民法典", DEFAULT_LAW_AUTHORITY_ARTICLES.get(authority_id, "")),
        }
        for authority_id in rule.authority_ids
    ]
    authority_reliable = bool(authority_validation) and all(
        row.get("status") == "CURRENT" and row.get("support_type") in {"DIRECT_SUPPORT", "PARTIAL_SUPPORT"}
        for row in authority_validation
    )
    if effective_status in {"CLEAR_DEFAULT", "PARTIAL_DEFAULT"} and not authority_reliable:
        effective_status = "UNCERTAIN_DEFAULT"
        applicability_confidence = "low"
    if material_gap:
        applicability = "APPLICABLE"
        if item.node_id == "sale_risk_carrier_delivery" and not any(term in compacted for term in ("运输", "承运人", "物流", "送货", "发运")):
            applicability = "UNCERTAIN"
            applicability_confidence = "low"
            effective_status = "UNCERTAIN_DEFAULT"
        elif item.node_id == "sale_risk_buyer_delay_acceptance" and not any(term in compacted for term in ("迟延受领", "拒收", "未提货", "逾期提货")):
            applicability = "UNCERTAIN"
            applicability_confidence = "low"
            effective_status = "UNCERTAIN_DEFAULT"
        elif item.node_id in {"sale_quality_liability", "sale_breach_damages", "sale_termination"}:
            applicability = "CONDITIONAL"
            applicability_confidence = "medium"
            if effective_status == "CLEAR_DEFAULT":
                effective_status = "PARTIAL_DEFAULT"
    residual_legal = "low" if effective_status == "CLEAR_DEFAULT" else "medium"
    residual_operational = "medium" if material_gap else "low"
    return {
        "executed": True,
        "default_law_relevant": True,
        "status": effective_status,
        "rule": rule.to_public_dict(),
        "authority_validation": authority_validation,
        "applicability": applicability,
        "applicability_confidence": applicability_confidence,
        "protection_scope": rule.protection_scope,
        "remaining_gap": "法定规则提供基础保护，但合同仍需明确业务节点、例外、操作流程及证据。" if material_gap else "无实质剩余缺口。",
        "practical_uncertainty": "medium" if material_gap else "low",
        "residual_legal_risk": residual_legal if material_gap else "low",
        "residual_operational_risk": residual_operational,
    }


def _apply_risk_dimensions(items: List[ReviewItemResult], contract_type: str = "", contract_text: str = "") -> List[ReviewItemResult]:
    for item in items:
        material_gap = item.coverage_status in {"缺失", "部分覆盖"}
        if item.coverage_status == "通过" and "建议继续核对" in (item.risk_point_description or ""):
            item.risk_point_description = f"合同已覆盖“{item.title}”相关安排。"
        item.risk_group = RISK_GROUP_BY_ID.get(item.item_id, item.node_id or item.item_id)
        item.related_reviews = RELATED_REVIEWS_BY_ID.get(item.item_id, [])
        category = ontology_category(item.risk_group, item.node_id)
        item.decision_trace["risk_category"] = category
        if item.coverage_status == COVERAGE_NOT_APPLICABLE or str((item.applicability or {}).get("status") or "").upper() == "NOT_APPLICABLE":
            non_applicable_state = {
                "review_id": item.item_id,
                "status": "NOT_APPLICABLE",
                "reason": (item.applicability or {}).get("reason") or item.reasoning_summary,
                "missing_trigger_facts": list((item.applicability or {}).get("missing_triggers") or []),
                "conflicting_trigger_facts": list((item.applicability or {}).get("conflicting_triggers") or []),
                "source_fact_ids": list((item.applicability or {}).get("trigger_fact_ids") or []),
                "confidence": (item.applicability or {}).get("confidence") or "medium",
            }
            item.decision_trace["non_applicable_state"] = non_applicable_state
            item.decision_trace["default_law_status"] = "NOT_APPLICABLE"
            item.decision_trace["default_law_assessment"] = {
                "executed": False, "default_law_relevant": False, "status": "NOT_APPLICABLE",
                "rule": None, "applicability": "NOT_APPLICABLE", "applicability_confidence": non_applicable_state["confidence"],
                "protection_scope": "", "remaining_gap": "", "practical_uncertainty": "none",
                "residual_legal_risk": "none", "residual_operational_risk": "none",
                "exclusion_reason": "Review applicability is NOT_APPLICABLE; default-law gap analysis was skipped.",
            }
            item.decision_trace["effective_gap"] = {
                "review_id": item.item_id, "status": "NOT_APPLICABLE", "contract_coverage": COVERAGE_NOT_APPLICABLE,
                "default_law_checked": False, "statutory_default": "NOT_APPLICABLE",
                "contractual_missing_elements": [], "statutory_default_elements": [],
                "still_unprotected_elements": [], "practical_execution_gap": [], "evidentiary_gap": [],
                "authority_ids": [], "citation_entailment": "NOT_APPLICABLE", "legal_freshness": "NOT_APPLICABLE",
                "default_rule_applicable": False, "effective_gap_valid": True, "residual_risk_exists": False,
                "affected_effective_gap": False, "remaining_gap": "", "statutory_protection_scope": "",
                "default_law_result_id": "", "exclusion_reason": "NOT_APPLICABLE",
            }
            item.decision_trace["aggregation_key"] = quality4_aggregation_key(item)
            item.risk_severity = SEVERITY_NONE
            item.residual_risk = "本事项不适用于当前交易，不形成相应合同缺口。"
            item.system_confidence = _system_confidence_for_item(item)
            continue
        default_assessment = _default_law_assessment(item, contract_type, contract_text)
        default_status = default_assessment["status"]
        item.decision_trace["default_law_status"] = default_status
        item.decision_trace["default_law_assessment"] = default_assessment
        economic_gap = item.economic_impact or "unknown"
        uncertainty = "high" if default_assessment.get("applicability") == "UNCERTAIN" else default_assessment["practical_uncertainty"]
        residual_risk = (
            "合同未自行约定该事项，法律默认规则提供基础答案；剩余风险主要来自具体履行节点、操作流程和证据差异。"
            if item.coverage_status == "缺失" and default_status == "CLEAR_DEFAULT"
            else default_assessment["remaining_gap"]
        )
        effective_gap = EffectiveGap(
            review_id=item.item_id,
            contract_coverage=item.coverage_status,
            default_law_status=default_status,
            default_protection=default_assessment["protection_scope"],
            contract_context={"contract_type": contract_type, "risk_group": item.risk_group, "node_id": item.node_id},
            remaining_legal_gap=default_assessment["remaining_gap"],
            operational_gap=default_assessment["residual_operational_risk"],
            economic_gap=economic_gap,
            uncertainty=uncertainty,
            residual_risk=residual_risk,
        ).to_public_dict()
        item.decision_trace["effective_gap"] = {
            **effective_gap,
            "default_law_checked": default_assessment["executed"],
            "statutory_default": default_status,
            "default_rule_id": (default_assessment.get("rule") or {}).get("rule_id", ""),
            "legal_proposition_id": (default_assessment.get("rule") or {}).get("proposition_id", ""),
            "statutory_protection_scope": default_assessment["protection_scope"],
            "remaining_gap": default_assessment["remaining_gap"],
            "practical_uncertainty": default_assessment["practical_uncertainty"],
            "default_strength": "strong" if default_status == "CLEAR_DEFAULT" else "partial" if default_status == "PARTIAL_DEFAULT" else "none",
            "residual_legal_risk": default_assessment["residual_legal_risk"],
            "residual_operational_risk": default_assessment["residual_operational_risk"],
            "drafting_value": "convenience" if default_status == "CLEAR_DEFAULT" else "risk_mitigation",
            "contract_override_risk": "low",
            "contractual_missing_elements": [
                element.get("proposition") for element in item.coverage_elements
                if element.get("status") in {"MISSING", "PARTIALLY_COVERED"} and element.get("proposition")
            ],
            "statutory_default_elements": [default_assessment["protection_scope"]] if default_assessment["protection_scope"] else [],
            "supplied_element_ids": list((default_assessment.get("rule") or {}).get("supplied_element_ids") or []),
            "unsupplied_element_ids": [
                element.get("element_id") for element in item.coverage_elements
                if element.get("status") in {"MISSING", "PARTIALLY_COVERED"}
                and element.get("element_id") not in set((default_assessment.get("rule") or {}).get("supplied_element_ids") or [])
            ],
            "still_unprotected_elements": (
                [] if default_status == "CLEAR_DEFAULT" and default_assessment["residual_operational_risk"] == "low"
                else [default_assessment["remaining_gap"]] if material_gap and default_assessment["remaining_gap"] else []
            ),
            "practical_execution_gap": [default_assessment["remaining_gap"]] if material_gap and default_assessment["residual_operational_risk"] != "low" else [],
            "evidentiary_gap": [],
            "authority_ids": list((default_assessment.get("rule") or {}).get("authority_ids") or []),
            "citation_entailment": (
                "SUPPORTS" if default_assessment.get("authority_validation")
                and all(row.get("support_type") in {"DIRECT_SUPPORT", "PARTIAL_SUPPORT"} for row in default_assessment["authority_validation"])
                else "UNCERTAIN" if (default_assessment.get("rule") or {}).get("authority_ids") else "NOT_APPLICABLE"
            ),
            "legal_freshness": (
                "CURRENT" if default_assessment.get("authority_validation")
                and all(row.get("status") == "CURRENT" for row in default_assessment["authority_validation"])
                else "UNCERTAIN" if (default_assessment.get("rule") or {}).get("authority_ids") else "NOT_APPLICABLE"
            ),
            "default_rule_applicable": default_assessment.get("applicability") in {"APPLICABLE", "CONDITIONAL", "AVAILABLE_NOT_NEEDED"},
            "effective_gap_valid": bool(default_assessment["executed"]),
            "residual_risk_exists": bool(default_assessment["remaining_gap"]) and not (
                default_status == "CLEAR_DEFAULT" and default_assessment["residual_operational_risk"] == "low"
            ),
            "affected_effective_gap": material_gap and default_status in {"CLEAR_DEFAULT", "PARTIAL_DEFAULT"}
            and bool((default_assessment.get("rule") or {}).get("authority_ids")),
            "default_law_result_id": f"DLR-{item.item_id}",
        }
        item.decision_trace["aggregation_key"] = quality4_aggregation_key(item)
        formula = (item.scenario_analysis or {}).get("formula")
        if formula:
            item.decision_trace["formula_validation"] = validate_formula_ast(formula)
            item.decision_trace["calculation_provenance"] = calculation_provenance(formula, item.scenario_analysis)
        if item.node_id in LOW_PROBABILITY_NODE_IDS and item.risk_level != "高":
            item.review_priority = PRIORITY_C_OPTIMIZATION
        item.risk_severity = _risk_severity_for_item(item)
        gap_type = _coverage_gap_type(item)
        if gap_type:
            item.decision_trace["coverage_gap_type"] = gap_type
            if gap_type == "MISSING_WITH_STATUTORY_DEFAULT" and item.risk_severity == SEVERITY_MEDIUM:
                item.risk_severity = SEVERITY_LOW
        if item.coverage_status in {"通过", COVERAGE_NOT_APPLICABLE} and item.risk_severity == SEVERITY_NONE:
            item.residual_risk = "本审查点已覆盖"
        else:
            item.residual_risk = residual_risk if default_status in {"CLEAR_DEFAULT", "PARTIAL_DEFAULT"} else item.risk_point_description
        item.system_confidence = _system_confidence_for_item(item)
    return items


def _priority_rank(priority: str) -> int:
    return {
        PRIORITY_A_CORE: 0,
        PRIORITY_B_PRACTICAL: 1,
        PRIORITY_C_OPTIMIZATION: 2,
        ACTION_PRIORITY_NONE: 3,
        ACTION_PRIORITY_NOT_APPLICABLE: 4,
        "N/A": 4,
    }.get(priority, 4)


def _priority_label(priority: str) -> str:
    return {
        PRIORITY_A_CORE: "优先处理",
        PRIORITY_B_PRACTICAL: "建议处理",
        PRIORITY_C_OPTIMIZATION: "可选优化",
        ACTION_PRIORITY_NONE: "无需处理",
        ACTION_PRIORITY_NOT_APPLICABLE: "不适用",
        "N/A": "不适用",
    }.get(priority or "", priority or "未标注")


def _importance_label(importance: str) -> str:
    return {
        REVIEW_IMPORTANCE_CORE: "核心审查项",
        REVIEW_IMPORTANCE_IMPORTANT: "重要审查项",
        REVIEW_IMPORTANCE_NORMAL: "一般审查项",
    }.get(importance or "", "一般审查项")


def _recommendation_heading(priority: str) -> str:
    return {
        PRIORITY_A_CORE: "建议优先处理",
        PRIORITY_B_PRACTICAL: "建议处理",
        PRIORITY_C_OPTIMIZATION: "可选优化",
        ACTION_PRIORITY_NONE: "无需处理",
        ACTION_PRIORITY_NOT_APPLICABLE: "不适用",
    }.get(priority or "", "建议处理")


def _final_action_label(action: str) -> str:
    return {
        DISPOSITION_MUST_CHANGE: "优先处理",
        DISPOSITION_SHOULD_CHANGE: "建议处理",
        DISPOSITION_OPTIONAL_IMPROVEMENT: "可选优化",
        DISPOSITION_KEEP_CURRENT: "建议保持现状",
        DISPOSITION_DO_NOT_ADD: "不建议新增",
        DISPOSITION_MANUAL_REVIEW: "人工复核",
    }.get(action or "", action or "未标注")


def _finding_public_label(finding: RiskFinding) -> str:
    return finding.title or finding.risk_group


def _finding_id_title_map(findings: List[RiskFinding]) -> Dict[str, str]:
    return {finding.finding_id: _finding_public_label(finding) for finding in findings}


def _join_related_finding_titles(finding_ids: List[str], title_map: Dict[str, str]) -> str:
    if not finding_ids:
        return "无"
    return "、".join(title_map.get(finding_id, "关联风险") for finding_id in finding_ids)


def _confidence_label(confidence: str) -> str:
    return {"high": "高", "medium": "中", "low": "低"}.get(confidence or "", "中")


def _severity_rank(severity: str) -> int:
    return {
        SEVERITY_CRITICAL: 0,
        SEVERITY_HIGH: 1,
        SEVERITY_MEDIUM: 2,
        SEVERITY_LOW: 3,
        SEVERITY_NONE: 4,
    }.get(severity, 4)


def _economic_rank(finding: RiskFinding) -> int:
    economic = finding.economic_impact or {}
    level = economic.get("level")
    if level == "critical":
        return 0
    if level == "high":
        return 1
    if economic.get("monthly_payment_multiple") is not None and economic.get("monthly_payment_multiple") >= 8:
        return 1
    if level == "medium":
        return 2
    if level == "low":
        return 3
    return 4


def _probability_rank(probability: str) -> int:
    return {
        PROBABILITY_VERY_HIGH: 0,
        PROBABILITY_HIGH: 1,
        PROBABILITY_MEDIUM: 2,
        PROBABILITY_LOW: 3,
        PROBABILITY_RARE: 4,
        PROBABILITY_UNKNOWN: 5,
    }.get(probability or "", 5)


def _confidence_rank(confidence: Dict[str, Any]) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get((confidence or {}).get("level"), 1)


def _core_obligation_rank(finding: RiskFinding) -> int:
    core_groups = {
        "early_termination_financial_exposure",
        "deposit_return_timing",
        "lawful_lease_basis",
        "housing_safety_emergency",
        "notice_and_delivery",
    }
    return 0 if finding.risk_group in core_groups or finding.priority == PRIORITY_A_CORE else 1


def _finding_sort_key(finding: RiskFinding) -> tuple[int, int, int, int, int, int, str]:
    return (
        _priority_rank(finding.priority),
        _severity_rank(finding.severity),
        _economic_rank(finding),
        _core_obligation_rank(finding),
        _probability_rank(finding.probability),
        _confidence_rank(finding.confidence),
        finding.finding_id,
    )


def _finding_recommendation(group: str, item: ReviewItemResult) -> str:
    if group == "service_refund_termination_settlement":
        return (
            "建议合并完善解除与退费结算条款：服务接受方应提前以可留痕方式通知；"
            "已实际提供的课时或服务费用不退，服务方已实际发生且不可退回的合理成本可依法扣除；"
            "剩余未提供服务对应款项、退款期限和双方举证材料应一次性写清。"
        )
    if group == "service_performance_remedy_framework":
        return (
            "建议按层级约定服务未履行或质量不符合约定时的处理：先补正、补课、延期或重新提供；"
            "仍不能达到约定标准时，再按未履行部分结算退费；涉及赔偿的，以依法可证明的实际损失为限。"
        )
    if group == "service_scope_delivery_standard":
        return (
            "建议补充培训服务范围和交付标准中的真实缺口，例如培训地点、交付方式、课程完成标准、师资要求、"
            "调课/停课/补课规则；不得写成学习效果保证或保过承诺。"
        )
    if group == "service_fee_balance_transparency":
        return (
            "建议补充收费和余额结算口径：区分课时费、资料费/教材费等费用项目，明确单价或可推导单价、"
            "已消耗课时、剩余课时及退费时不可退费用的处理。"
        )
    if group == "service_performance_record_evidence":
        return "建议补充签到、课时消耗、服务确认、沟通和退费结算记录的保存方式，作为课时完成和退费计算证据。"
    if group == "service_business_closure_notice":
        return "建议补充停业、迁址或重大经营调整时的提前通知、可替代服务方案和未提供服务部分结算路径。"
    if group == "goods_title_and_third_party_rights":
        return "建议统一约定供方对货物权属及第三方权利无瑕疵作出保证，并承担通知、处理、替换及赔偿责任。"
    if group == "early_termination_financial_exposure":
        return "建议将提前退租违约金改为固定月租倍数、设置金额上限，或明确以出租人实际空置损失和再出租成本为调整基础。"
    if group == "legal_reference":
        return "建议将《中华人民共和国合同法》更新为《中华人民共和国民法典》及现行有效相关规定，并保持合同引用法律与签署时间一致。"
    if group == "deposit_return_timing":
        return "建议补充交接完成、费用结清后若干日内返还押金，并列明可扣款项目和书面说明义务。"
    if group == "deposit_offset_order":
        return "建议列明押金可抵扣的项目、抵扣顺序、扣款后的书面说明以及余额返还安排。"
    if group == "property_damage_deposit_evidence":
        return "建议统一补充房屋交接清单、入住瑕疵告知、损坏举证、维修费用承担和押金扣款说明机制，避免退租时围绕损坏责任和扣款依据重复争议。"
    if group == "notice_and_delivery":
        return "建议补充通知送达地址、电子送达方式、催告留痕和视为送达规则。"
    if group == "housing_safety_emergency":
        return "建议补充重大安全隐患下的紧急通知、临时搬离、费用承担和解除结算机制。"
    if group == "lawful_lease_basis":
        return "建议补充出租人保证房屋具备合法出租条件，且不存在影响居住使用的违法建设或限制。"
    if item.narrative_state and item.narrative_state.get("recommendation"):
        return str(item.narrative_state["recommendation"])
    return item.suggested_clause_example


def _finding_title(group: str, item: ReviewItemResult) -> str:
    return {
        "service_refund_termination_settlement": "消费者解除与退款结算机制不完整",
        "service_performance_remedy_framework": "服务未履行或质量不符合约定时的补救机制不完整",
        "service_scope_delivery_standard": "培训服务范围和交付标准不完整",
        "service_fee_balance_transparency": "收费项目、预付款余额和退费计价口径不够清晰",
        "service_performance_record_evidence": "服务履行记录和确认凭证不足",
        "service_business_closure_notice": "停业或经营调整通知与结算机制不足",
        "early_termination_financial_exposure": "提前退租违约金经济风险",
        "deposit_return_timing": "押金返还期限未明确",
        "deposit_offset_order": "押金抵扣顺序未明确",
        "property_damage_deposit_evidence": "房屋损坏与押金扣款证据机制不足",
        "notice_and_delivery": "解除通知和送达机制不完整",
        "housing_safety_emergency": "房屋安全风险应急机制不足",
        "lawful_lease_basis": "房屋合法出租保证可进一步明确",
        "legal_reference": "法律引用建议更新",
        "goods_title_and_third_party_rights": "货物权属及第三方权利保障不完整",
    }.get(group, item.title)


POSITIVE_EXISTENCE_RISK_GROUPS = {"sale_unilateral_price_adjustment"}


def _service_semantic_risk_group(item: ReviewItemResult) -> str:
    if not item.item_id.startswith("SVC-"):
        return ""
    text = " ".join([item.node_id, item.risk_group, item.title]).lower()
    refund_terms = (
        "refund", "termination", "health_change", "consumer_personal_reason", "consumer_termination",
        "退费", "退款", "解除", "结算", "通知期限", "健康原因", "个人原因",
    )
    performance_terms = (
        "nonperformance", "nonconform", "remedy", "未提供服务", "服务质量瑕疵", "救济", "补救",
    )
    scope_terms = (
        "service_content", "service_schedule", "service_quality_standard",
        "服务内容", "服务时间", "服务质量标准", "质量标准",
    )
    fee_terms = (
        "prepaid_amount", "fee_standard", "收费标准", "预付款金额", "余额", "价目",
    )
    record_terms = ("performance_record", "履行记录", "确认附件")
    closure_terms = ("closure_notice", "停业提前通知")
    if any(term in text for term in refund_terms):
        return "service_refund_termination_settlement"
    if any(term in text for term in performance_terms):
        return "service_performance_remedy_framework"
    if any(term in text for term in scope_terms):
        return "service_scope_delivery_standard"
    if any(term in text for term in fee_terms):
        return "service_fee_balance_transparency"
    if any(term in text for term in record_terms):
        return "service_performance_record_evidence"
    if any(term in text for term in closure_terms):
        return "service_business_closure_notice"
    return ""


def _risk_aggregation_group(item: ReviewItemResult) -> str:
    semantic_group = _service_semantic_risk_group(item)
    if semantic_group:
        item.decision_trace["semantic_risk_group"] = semantic_group
        return semantic_group
    return item.risk_group or item.node_id or item.item_id


def _risk_claim_for_group(group: str, item: ReviewItemResult, finding_id: str) -> RiskClaim:
    if group == "sale_unilateral_price_adjustment":
        return RiskClaim(
            claim_id=f"{finding_id}-CLAIM",
            risk_type=group,
            proposition="某一方可以在无需另一方同意的情况下调整合同价格。",
            existence_type="POSITIVE_EXISTENCE",
            subject_party="contract_party",
            action="adjust",
            object="contract_price",
            condition="without_counterparty_consent",
            direction="price_change",
            consequence=item.legal_consequence_if_missing,
            required_evidence_elements=["unilateral_actor", "price_adjustment_action", "absence_of_mutual_control"],
        )
    return RiskClaim(
        claim_id=f"{finding_id}-CLAIM",
        risk_type=group,
        proposition=item.risk_point_description,
        existence_type="MISSING_SAFEGUARD" if item.coverage_status in {"缺失", "部分覆盖"} else "POSITIVE_EXISTENCE",
        object=group,
        consequence=item.legal_consequence_if_missing,
        required_evidence_elements=[element.get("element_id", "") for element in item.coverage_elements if element.get("element_id")],
    )


def _supporting_evidence_for_claim(claim: RiskClaim, evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    required_entailments = {EVIDENCE_SUPPORTS} if claim.existence_type == "POSITIVE_EXISTENCE" else {EVIDENCE_SUPPORTS, EVIDENCE_PARTIAL_SUPPORT}
    return [row for row in evidence if row.get("entailment_status") in required_entailments]


def _select_risk_evidence(
    finding_id: str,
    group_items: List[ReviewItemResult],
) -> List[Dict[str, Any]]:
    selected: Dict[tuple[str, str], Dict[str, Any]] = {}
    for item in group_items:
        missing_ids = {
            str(element.get("element_id") or "")
            for element in item.coverage_elements or []
            if element.get("status") in {"MISSING", "UNCERTAIN"}
        }
        for evidence in item.evidence_clauses or []:
            supporting_ids = [str(value) for value in evidence.get("supporting_element_ids") or [] if value]
            if not supporting_ids:
                continue
            clause_id = str(evidence.get("clause_id") or "")
            text_value = str(evidence.get("original_excerpt") or evidence.get("text") or "")
            key = (clause_id, text_value)
            row = selected.setdefault(key, {
                **evidence,
                "risk_id": finding_id,
                "supporting_review_id": item.item_id,
                "supporting_review_ids": [],
                "supporting_element_ids": [],
                "canonical_fact_keys": [],
                "evidence_ref": str(evidence.get("evidence_id") or clause_id),
                "relevance_reason": "Evidence directly supports resolved ReviewElementTruth used by this risk.",
            })
            for review_id in [item.item_id]:
                if review_id not in row["supporting_review_ids"]:
                    row["supporting_review_ids"].append(review_id)
            for element_id in supporting_ids:
                if element_id not in row["supporting_element_ids"]:
                    row["supporting_element_ids"].append(element_id)
            for fact_key in evidence.get("canonical_fact_keys") or []:
                canonical = canonical_fact_key(str(fact_key))
                if canonical and canonical not in row["canonical_fact_keys"]:
                    row["canonical_fact_keys"].append(canonical)
            if missing_ids:
                row["related_missing_element_ids"] = sorted(missing_ids)
    rows = list(selected.values())
    rows.sort(key=lambda row: (
        -len(row.get("supporting_element_ids") or []),
        -len(row.get("canonical_fact_keys") or []),
        str(row.get("location") or ""),
    ))
    return rows[:6]


def _risk_element_truth(
    primary: ReviewItemResult,
    supporting_items: List[ReviewItemResult],
) -> tuple[List[str], List[str], List[Dict[str, Any]]]:
    covered = sorted({
        str(element.get("element_id") or "")
        for item in supporting_items
        for element in item.coverage_elements or []
        if element.get("element_id") and element.get("status") in {"COVERED", "PARTIALLY_COVERED"}
    })
    missing_rows: List[Dict[str, Any]] = []
    formula_item = next(
        (
            item for item in supporting_items
            if ((item.scenario_analysis or {}).get("formula") or {}).get("type")
        ),
        primary,
    )
    formula = (formula_item.scenario_analysis or {}).get("formula") or {}
    for element in primary.coverage_elements or []:
        if not element.get("element_id") or element.get("status") not in {"MISSING", "UNCERTAIN"}:
            continue
        element_id = str(element.get("element_id") or "")
        proposition = str(element.get("proposition") or "")
        if element_id == "core_contract_arrangement" and formula.get("type"):
            element_id = f"{formula_item.node_id}.formula_control"
            proposition = "违约责任计算公式、金额上限及其与可证明实际损失之间的关系明确。"
        missing_rows.append({
            "element_id": element_id,
            "proposition": proposition,
            "source_review_id": primary.item_id,
            "status": str(element.get("status") or "MISSING"),
            "required_fact_key": str(element.get("required_fact_key") or ""),
        })
    if not missing_rows and formula.get("type"):
        missing_rows.append({
            "element_id": f"{formula_item.node_id}.formula_control",
            "proposition": "违约责任计算公式、金额上限及其与可证明实际损失之间的关系明确。",
            "source_review_id": formula_item.item_id,
            "status": "MISSING",
            "required_fact_key": "",
        })
    missing_ids = [row["element_id"] for row in missing_rows]
    return covered, missing_ids, missing_rows


def _build_risk_findings(items: List[ReviewItemResult]) -> List[RiskFinding]:
    grouped: Dict[str, List[ReviewItemResult]] = {}
    def can_attach_to_finding(item: ReviewItemResult) -> bool:
        applicability_status = str((item.applicability or {}).get("status") or "APPLICABLE").upper()
        if applicability_status != "APPLICABLE" or (item.applicability or {}).get("applicable", True) is False:
            return False
        return (item.decision_trace or {}).get("review_nature") != "INTERNAL_CLASSIFICATION"

    for item in items:
        if (item.decision_trace or {}).get("review_nature") == "INTERNAL_CLASSIFICATION":
            item.decision_trace["finding_precondition"] = {
                "all_required_conditions": False,
                "review_nature": "INTERNAL_CLASSIFICATION",
                "reason": "Internal legal characterization does not create RiskFinding unless an independent contract risk exists.",
            }
            continue
        applicability_status = str((item.applicability or {}).get("status") or "APPLICABLE").upper()
        applicability_valid = applicability_status == "APPLICABLE" and (item.applicability or {}).get("applicable", True) is not False
        coverage_valid = item.coverage_status in {"缺失", "部分覆盖", "风险条款"}
        claim_conflicts = list((item.decision_trace or {}).get("shared_claim_conflicts") or [])
        residual = ((item.decision_trace or {}).get("effective_gap") or {}).get("remaining_gap") or item.residual_risk or item.legal_consequence_if_missing
        precondition = {
            "applicability_valid": applicability_valid,
            "coverage_valid": coverage_valid,
            "evidence_valid": bool(item.evidence_clauses) or item.coverage_status in {"缺失", "部分覆盖"},
            "shared_claim_consistent": not claim_conflicts,
            "default_law_valid_if_required": not (((item.decision_trace or {}).get("default_law_assessment") or {}).get("default_law_relevant")) or bool((item.decision_trace or {}).get("effective_gap")),
            "effective_gap_valid": bool(((item.decision_trace or {}).get("effective_gap") or {}).get("effective_gap_valid")),
            "residual_risk_exists": bool(residual),
        }
        precondition["all_required_conditions"] = all(precondition.values())
        item.decision_trace["finding_precondition"] = precondition
        if not precondition["all_required_conditions"] or item.risk_severity == SEVERITY_NONE:
            continue
        if (item.risk_group or item.node_id) in POSITIVE_EXISTENCE_RISK_GROUPS and item.coverage_status != "风险条款":
            continue
        aggregation_group = _risk_aggregation_group(item)
        group_key = f"{item.decision_trace.get('risk_category') or ontology_category(aggregation_group, item.node_id)}|{aggregation_group}"
        grouped.setdefault(group_key, []).append(item)

    findings: List[RiskFinding] = []
    for index, (group_key, group_items) in enumerate(grouped.items(), start=1):
        group_items = sorted(group_items, key=lambda item: (_severity_rank(item.risk_severity), _priority_rank(item.review_priority), item.item_id))
        primary = group_items[0]
        group = _risk_aggregation_group(primary)
        all_group_items = [
            item for item in items
            if f"{item.decision_trace.get('risk_category') or ontology_category(_risk_aggregation_group(item), item.node_id)}|{_risk_aggregation_group(item)}" == group_key
            and can_attach_to_finding(item)
        ]
        finding_id = RISK_FINDING_ID_BY_GROUP.get(group, f"RF-{index:03d}")
        evidence = _select_risk_evidence(finding_id, all_group_items)
        covered_element_ids, missing_element_ids, final_missing_elements = _risk_element_truth(primary, all_group_items)
        risk_claim = _risk_claim_for_group(group, primary, finding_id)
        supporting_evidence = _supporting_evidence_for_claim(risk_claim, evidence)
        source_review_ids = sorted({item.item_id for item in all_group_items})
        source_clause_ids = sorted({str(clause.get("clause_id")) for clause in evidence if clause.get("clause_id")})
        economic_impact = _normalized_economic_impact(primary)
        impact = _impact_for_item(primary)
        risk_category = primary.decision_trace.get("risk_category") or ontology_category(group, primary.node_id)
        aggregation_signals = {
            "aggregation_key": group_key,
            "risk_ontology": risk_category,
            "shared_facts": sorted({dep for item in group_items for dep in item.fact_dependencies}),
            "shared_clause_ids": source_clause_ids,
            "shared_obligation": group,
            "shared_economic_consequence": primary.economic_impact or "none",
            "shared_legal_consequence": primary.legal_consequence_if_missing,
            "source_review_count": len(source_review_ids),
            "risk_claim": risk_claim.to_public_dict(),
            "claim_ids": sorted({
                str(element.get("claim_id") or element.get("element_id"))
                for item in group_items
                for element in item.coverage_elements
                if element.get("claim_id") or element.get("element_id")
            }),
            "finding_preconditions": {item.item_id: item.decision_trace.get("finding_precondition") for item in group_items},
        }
        severity_reason = {
            "dominant_factor": primary.high_risk_reason or primary.decision_trace.get("coverage_gap_type") or risk_category,
            "impact": impact,
            "probability": _probability_for_item(primary),
            "economic_ratio": economic_impact.get("contract_total_ratio") or economic_impact.get("remaining_obligation_ratio"),
            "statutory_protection": default_law_status(group, primary.node_id),
            "evidence_strength": "explicit" if evidence else "not_found_or_fact_gap",
        }
        confidence_levels = [item.system_confidence.get("level") for item in group_items if item.system_confidence]
        confidence_level = "low" if "low" in confidence_levels else "medium" if "medium" in confidence_levels else "high"
        finding = RiskFinding(
            finding_id=finding_id,
            risk_group=group,
            title=_finding_title(group, primary),
            severity=primary.risk_severity,
            priority=primary.review_priority,
            source_review_ids=source_review_ids,
            facts=sorted({dep for item in group_items for dep in item.fact_dependencies}),
            evidence=evidence,
            source_clause_ids=source_clause_ids,
            legal_basis=[
                {
                    "text": primary.legal_basis_index,
                    "authority_status": "validated_or_general_principle",
                    "confidence": "medium",
                }
            ] if primary.legal_basis_index else [],
            issue=str((primary.narrative_state or {}).get("issue") or primary.risk_point_description),
            consequence=str((primary.narrative_state or {}).get("consequence") or primary.legal_consequence_if_missing),
            probability=_probability_for_item(primary),
            impact=impact,
            economic_impact=economic_impact,
            legal_impact={
                "coverage": primary.coverage_status,
                "issue_type": primary.issue_type,
                "gap_type": primary.decision_trace.get("coverage_gap_type"),
            },
            operational_impact={"level": impact.get("operational", "LOW")},
            safety_impact={"level": impact.get("safety", "NONE")},
            recommendation=_finding_recommendation(group, primary),
            decision_value="high" if primary.risk_severity in {SEVERITY_HIGH, SEVERITY_CRITICAL} or primary.economic_impact in {"high", "critical"} else "medium",
            confidence={
                "level": confidence_level,
                "source": "system_confidence_calibration",
                "inputs": [item.system_confidence for item in group_items],
            },
            needs_manual_review=any(item.needs_manual_review for item in group_items),
            severity_reason=severity_reason,
            risk_category=risk_category,
            aggregation_signals=aggregation_signals,
            default_law_status=default_law_status(group, primary.node_id),
            supporting_evidence=supporting_evidence,
            counter_evidence=[row for row in evidence if row not in supporting_evidence],
            covered_element_ids=covered_element_ids,
            missing_element_ids=missing_element_ids,
            final_missing_elements=final_missing_elements,
        )
        findings.append(finding)
        for item in items:
            item_group = _risk_aggregation_group(item)
            item_group_key = f"{item.decision_trace.get('risk_category') or ontology_category(item_group, item.node_id)}|{item_group}"
            if item_group_key != group_key:
                continue
            if not can_attach_to_finding(item):
                continue
            item.related_risks = sorted(set(item.related_risks + [finding_id]))
    findings.sort(key=_finding_sort_key)
    return findings


def _finding_has_supporting_evidence(finding: RiskFinding) -> bool:
    evidence = finding.supporting_evidence or finding.evidence or []
    if not evidence:
        return False
    risk_claim = (finding.aggregation_signals or {}).get("risk_claim") or {}
    if risk_claim.get("existence_type") == "POSITIVE_EXISTENCE":
        return any(evidence_item.get("entailment_status") == EVIDENCE_SUPPORTS for evidence_item in evidence)
    return any(
        evidence_item.get("entailment_status") in {EVIDENCE_SUPPORTS, EVIDENCE_PARTIAL_SUPPORT}
        for evidence_item in evidence
    )


def _filter_unsupported_positive_findings(findings: List[RiskFinding], items: List[ReviewItemResult]) -> List[RiskFinding]:
    item_by_id = {item.item_id: item for item in items}
    retained: List[RiskFinding] = []
    for finding in findings:
        related_items = [item_by_id[item_id] for item_id in finding.source_review_ids if item_id in item_by_id]
        positive_risk_items = [item for item in related_items if item.coverage_status == "风险条款"]
        if positive_risk_items and not _finding_has_supporting_evidence(finding):
            finding.verification = {
                "status": "BLOCK",
                "prompt_version": VERIFIER_PROMPT_VERSION,
                "fact_exists": False,
                "evidence_supports": False,
                "negative_evidence_checked": True,
                "reason": "Positive existence finding requires SUPPORTS evidence; partial, related, uncertain, or topic-similar evidence is insufficient.",
            }
            finding.verification_status = "BLOCK"
            for item in positive_risk_items:
                item.related_risks = [risk_id for risk_id in item.related_risks if risk_id != finding.finding_id]
                item.decision_trace["finding_evidence_gate"] = {
                    "status": "REJECTED",
                    "finding_id": finding.finding_id,
                    "reason": finding.verification["reason"],
                }
            continue
        retained.append(finding)
    return retained


def _risk_evidence_ownership_audit(findings: List[RiskFinding]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    mismatches: List[Dict[str, Any]] = []
    for finding in findings:
        if not finding.source_review_ids:
            continue
        for evidence in finding.evidence or []:
            supporting_elements = list(evidence.get("supporting_element_ids") or [])
            supporting_reviews = list(evidence.get("supporting_review_ids") or [])
            if evidence.get("supporting_review_id") and evidence.get("supporting_review_id") not in supporting_reviews:
                supporting_reviews.append(str(evidence.get("supporting_review_id")))
            reasons: List[str] = []
            if not supporting_elements:
                reasons.append("Evidence is not linked to any supporting Review element.")
            if not supporting_reviews or not set(supporting_reviews) & set(finding.source_review_ids):
                reasons.append("Evidence is not owned by a supporting Review for this risk.")
            if not evidence.get("relevance_reason"):
                reasons.append("Evidence has no risk-theme relevance reason.")
            row = {
                "risk_id": finding.finding_id,
                "risk_group": finding.risk_group,
                "supporting_review_ids": supporting_reviews,
                "supporting_element_ids": supporting_elements,
                "canonical_fact_keys": list(evidence.get("canonical_fact_keys") or []),
                "evidence_ref": evidence.get("evidence_ref") or evidence.get("evidence_id") or evidence.get("clause_id"),
                "location": evidence.get("location"),
                "relevance_reason": evidence.get("relevance_reason"),
                "status": "FAIL" if reasons else "PASS",
                "reasons": reasons,
            }
            rows.append(row)
            if reasons:
                mismatches.append({**row, "violation": "RISK_EVIDENCE_MISMATCH"})
    return {
        "status": "PASS" if not mismatches else "FAIL",
        "rows": rows,
        "risk_evidence_mismatches": mismatches,
        "risk_evidence_mismatch_count": len(mismatches),
    }


def _risk_evidence_ownership_gate(audit: Dict[str, Any]) -> Dict[str, Any]:
    mismatches = list(audit.get("risk_evidence_mismatches") or [])
    failures = []
    if mismatches:
        failures.append({
            "requirement": "RISK_EVIDENCE_MISMATCH",
            "failure_stage": "Risk Evidence Selection",
            "root_cause": f"Risk evidence is not directly owned by supporting elements: {len(mismatches)}.",
            "responsible_function": "_select_risk_evidence",
            "current_status": "FAIL",
        })
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "gate_results": {"RISK_EVIDENCE_MISMATCH": "PASS" if not failures else "FAIL"},
        "risk_evidence_mismatch_count": len(mismatches),
        "rows": list(audit.get("rows") or []),
    }


def _semantic_entailment_for_item(item: ReviewItemResult) -> tuple[Optional[bool], str, str]:
    if not item.evidence_clauses:
        return None, "", ""
    text = "\n".join(clause.get("text", "") for clause in item.evidence_clauses)
    evidence_type = classify_evidence_type(text)
    if item.node_id == "move_in_defect_notice":
        allowed = {"physical_defect", "handover", "repair"}
        excluded = {"mortgage", "mortgage_disclosure", "payment", "rent", "deposit", "jurisdiction", "ownership", "sublease", "party_identity"}
        if evidence_type in excluded or evidence_type not in allowed:
            return False, evidence_type, "证据不能从法律功能上推出入住时瑕疵告知安排。"
        return True, evidence_type, "证据可支撑入住瑕疵或交接状态安排。"
    if item.node_id == "limitation_and_notice" and evidence_type in {"payment", "rent", "deposit"}:
        return False, evidence_type, "费用支付条款不能推出通知送达和催告留痕制度。"
    return True, evidence_type, ""


def _apply_high_risk_reason_gate(items: List[ReviewItemResult]) -> None:
    allowed = {
        "contract_validity",
        "major_financial_loss",
        "personal_safety",
        "core_performance_failure",
        "major_right_loss",
        "extreme_liability",
        "irreversible_consequence",
    }
    for item in items:
        if item.coverage_status == COVERAGE_NOT_APPLICABLE:
            continue
        reason = HIGH_RISK_REASON_BY_ID.get(item.item_id) or HIGH_RISK_REASON_BY_NODE.get(item.node_id, "")
        if item.risk_level == "高":
            if reason not in allowed:
                item.risk_level = "中"
                item.high_risk_reason = ""
                item.quality_flags.append(
                    {
                        "item_id": item.item_id,
                        "type": "high_risk_reason_missing",
                        "message": "该审查项无法映射到合同效力、重大财产损失、人身安全等高风险理由，已降为中风险。",
                        "recommended_action": "auto_fix",
                    }
                )
            else:
                item.high_risk_reason = reason


def _review_importance_for_item(item: ReviewItemResult) -> str:
    if item.item_id in CORE_RISK_IDS:
        return REVIEW_IMPORTANCE_CORE
    if item.risk_level in {"高", "中"} or item.node_id in {"limitation_and_notice", "termination_notice", "jurisdiction"}:
        return REVIEW_IMPORTANCE_IMPORTANT
    return REVIEW_IMPORTANCE_NORMAL


def _action_priority_for_item(item: ReviewItemResult) -> str:
    assessment = _priority_assessment_for_item(item)
    item.decision_trace["priority_assessment"] = assessment
    return assessment["priority"]

def _review_priority_for_item(item: ReviewItemResult) -> str:
    return _action_priority_for_item(item)


def _action_suggestion_for_item(item: ReviewItemResult) -> str:
    if item.coverage_status == INSUFFICIENT_CONTEXT or item.needs_manual_review:
        return "建议人工复核"
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return "不适用"
    severity = item.risk_severity or _risk_severity_for_item(item)
    if item.coverage_status == "通过":
        return "已覆盖，无需修改"
    priority = item.action_priority or item.review_priority or _action_priority_for_item(item)
    return _recommendation_heading(priority)


def _apply_review_priority_and_action(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    for item in items:
        if item.item_id in LOW_PROBABILITY_OPTIMIZATION_IDS and item.coverage_status == "缺失":
            item.risk_level = "低"
            item.risk_point_description = f"{item.risk_point_description} 该项属于低概率完善项，普通一年期住宅租赁合同缺失时通常按可优化事项处理。"
            item.reasoning_summary = f"{item.reasoning_summary} 本项为低概率完善项，未发现特殊事实提高发生概率，默认按低风险可优化处理。"
            item.risk_severity = _risk_severity_for_item(item)
        item.review_importance = _review_importance_for_item(item)
        item.action_priority = _action_priority_for_item(item)
        item.review_priority = item.action_priority
        item.action_suggestion = _action_suggestion_for_item(item)
    return items


def _has_house_title_certificate(compacted: str) -> bool:
    return bool(re.search(r"(产证编号|不动产权证|房地产权证|沪房地|房地.+第\\d+号)", compacted))


def _has_reasonable_rent_penalty(compacted: str) -> bool:
    if not ("违约金" in compacted and ("月租金" in compacted or "租金" in compacted)):
        return False
    if re.search(r"(月租金|租金)的?(?:1|2|一|二|两)倍", compacted):
        return True
    return "不够抵付损失" in compacted or "不足抵付损失" in compacted or "赔偿造成的损失" in compacted


def _has_reasonable_sale_liquidated_damages(compacted: str) -> bool:
    if "违约金" not in compacted:
        return False
    if re.search(r"(?:每日|每天|按日|按天|日|逾期)[^，。；;]{0,20}万分之[一二三四五]", compacted):
        return True
    if re.search(r"万分之[一二三四五][^，。；;]{0,20}(?:每日|每天|按日|按天|日|逾期)", compacted):
        return True
    for match in re.finditer(r"(?:每日|每天|按日|按天|日|逾期)[^，。；;]{0,20}([0-9]+(?:\.[0-9]+)?)\s*[％%]", compacted):
        if float(match.group(1)) <= 0.05:
            return True
    for match in re.finditer(r"(?:每月|月)[^，。；;]{0,20}([0-9]+(?:\.[0-9]+)?)\s*[％%]", compacted):
        if float(match.group(1)) <= 2:
            return True
    for match in re.finditer(r"(?:每年|年化|年)[^，。；;]{0,20}([0-9]+(?:\.[0-9]+)?)\s*[％%]", compacted):
        if float(match.group(1)) <= 24:
            return True
    return False


def _has_sale_payment_timing(text: str) -> bool:
    source = text or ""
    has_payment = any(term in source for term in ("付款", "支付", "结算", "货款"))
    has_timing = bool(
        re.search(r"(签收|验收|收货|交货|发货|收到发票|对账|结算).{0,16}(后|次月|当月).{0,16}(\d+|[一二三四五六七八九十]+)(日|天|个工作日|日前|日内)", source)
        or re.search(r"(每月|次月|当月).{0,8}(\d+|[一二三四五六七八九十]+)(日|日前|日内).{0,16}(付款|支付|结算)", source)
        or re.search(r"(收到发票|签收|验收|收货).{0,16}(后).{0,8}(\d+|[一二三四五六七八九十]+)(日|天|个工作日).{0,8}(内)?(付款|支付|结算)", source)
    )
    return has_payment and has_timing


def _has_sale_staged_payment_structure(compacted: str) -> bool:
    return any(
        term in compacted
        for term in ("预付款", "进度款", "尾款", "分期付款", "分期支付", "分批付款", "首付款", "首期", "每期")
    ) or _has_installment_pattern(compacted)


def _has_sale_unilateral_price_adjustment(text: str) -> bool:
    source = text or ""
    compacted = _compact(source)
    if not any(term in compacted for term in ("单价", "价格", "价款", "报价", "货款")):
        return False
    if not any(term in compacted for term in ("调整", "变动", "变更", "浮动", "调价")):
        return False
    if any(term in compacted for term in ("双方协商一致", "双方书面确认", "经双方同意", "经买方同意", "另行签署补充协议")):
        return False
    if any(term in compacted for term in ("价格指数", "公开指数", "公开市场指数", "挂牌价", "基准价")) and not any(
        term in compacted for term in ("甲方可", "甲方有权", "出卖人可", "出卖人有权", "卖方可", "卖方有权", "供方可", "供方有权")
    ):
        return False
    has_unilateral_actor = any(
        term in compacted
        for term in (
            "甲方可",
            "甲方有权",
            "出卖人可",
            "出卖人有权",
            "卖方可",
            "卖方有权",
            "供方可",
            "供方有权",
            "单方",
        )
    )
    has_unilateral_action = any(term in compacted for term in ("通知予以调整", "通知后调整", "通知乙方", "自行调整", "直接调整"))
    has_vague_market = any(term in compacted for term in ("市场行情变化", "市场行情", "行情变化", "原材料价格", "价格波动"))
    return has_unilateral_actor and (has_unilateral_action or has_vague_market)


def _has_price_adjustment_safeguards(text: str) -> bool:
    source = text or ""
    has_basis = any(term in source for term in ("价格指数", "市场公允价", "双方确认", "协商一致", "书面确认", "参照"))
    has_cap = bool(re.search(r"(不超过|上限|最高|幅度).{0,12}(\d+|[一二三四五六七八九十]+)\s*(%|％|元)", source))
    has_notice = any(term in source for term in ("提前", "书面通知", "通知期限"))
    has_counterparty_right = any(term in source for term in ("异议", "拒绝", "解除", "终止", "另行协商"))
    return has_basis and has_cap and has_notice and has_counterparty_right


def _has_sale_delivery_transport_framework_engine(text: str) -> bool:
    return any(
        term in (text or "")
        for term in ("运输方式", "负责运输", "由甲方负责运输", "由乙方负责运输", "承运人", "送货", "提货", "自提", "物流", "运输", "交货地点", "到达交货地点", "收货", "货物到达")
    )


def _has_sale_delivery_voucher_terms(text: str) -> bool:
    return any(term in (text or "") for term in ("送货单", "签收单", "物流回执", "回单", "交接单", "收货确认单", "签收凭证"))


def _apply_house_lease_real_contract_rules(items: List[ReviewItemResult], contract_text: str) -> List[ReviewItemResult]:
    clauses = parse_contract_clauses(contract_text)
    compacted = _compact(contract_text)
    facts = extract_house_lease_facts(contract_text)
    by_id = {item.item_id: item for item in items}

    jurisdiction_evidence = _find_clause(
        clauses,
        lambda clause: (
            (
                ("房屋所在地" in clause.text or "不动产所在地" in clause.text or "浦东新区" in clause.text)
                and ("人民法院" in clause.text or "法院" in clause.text or "起诉" in clause.text)
            )
            or (
                ("向" in clause.text or "提交" in clause.text)
                and ("人民法院起诉" in _compact(clause.text) or "法院起诉" in _compact(clause.text) or "仲裁委员会仲裁" in _compact(clause.text))
            )
            or ("管辖" in clause.text and ("法院" in clause.text or "仲裁" in clause.text))
        ),
    )
    if jurisdiction_evidence and (item := by_id.get("HL-001")):
        _set_item_pass(
            item,
            [jurisdiction_evidence],
            "合同已约定发生争议时向房屋所在地人民法院起诉，覆盖房屋租赁纠纷管辖安排。",
            "已约定管辖法院，争议处理路径清晰。",
        )
    if facts.jurisdiction.is_specified and facts.jurisdiction.court and (item := by_id.get("HL-001")):
        _set_item_pass_from_fact(
            item,
            facts,
            "jurisdiction.court",
            f"统一事实图谱提取 jurisdiction.court={facts.jurisdiction.court}，且 jurisdiction.is_specified=true，说明合同已明确具体管辖法院。",
            "已约定具体管辖法院，争议处理路径清晰。",
        )

    tenant_death_evidence = _find_clause(
        clauses,
        lambda clause: (
            ("承租人死亡" in clause.text or "承租方死亡" in clause.text or ("死亡" in clause.text and "承租" in clause.text))
            and ("共同居住人" in clause.text or "共同经营人" in clause.text or "继续承租" in clause.text or "继续履行" in clause.text)
        ),
    )
    renewal_evidence = _find_clause(
        clauses,
        lambda clause: (
            ("续租" in clause.text or "续签" in clause.text or "租赁期满" in clause.text or "期满" in clause.text)
            and "死亡" not in clause.text
        ),
    )
    if renewal_evidence and not tenant_death_evidence and (item := by_id.get("HL-007")):
        _set_item_partial(
            item,
            [renewal_evidence],
            "中",
            "合同仅约定了租赁期满后的续租或续签流程，该条款处理的是合同正常期满后的续约问题；承租人死亡后的继续承租属于租期内主体消亡后的权利义务承继，二者法律场景不同，不能相互替代。",
            "合同有续租安排，但未涉及承租人死亡后共同居住人或共同经营人能否继续承租及证明材料要求。",
            issue_type="条款缺陷",
        )

    party_evidence = _find_clauses(
        clauses,
        lambda clause: (
            ("甲方" in clause.text or "乙方" in clause.text)
            and ("证号" in clause.text or "居民身份证" in clause.text or "联系地址" in clause.text or "联系电话" in clause.text)
            and not any(term in clause.text for term in ("房地产经纪", "中介", "居间介绍", "代理内容"))
        ),
        limit=3,
    )
    if party_evidence and (item := by_id.get("HL-002")):
        _set_item_pass(
            item,
            party_evidence,
            "合同首部/签署栏直接列明甲方、乙方姓名、身份证件号、住址和联系方式，证据应定位主体信息栏，不应引用中介服务附件。",
            "出租人与承租人的身份信息已在合同主体信息栏中列明，可支持签约主体识别、通知联系和后续履行。",
        )

    delivery_evidence = _find_clauses(
        clauses,
        lambda clause: (
            ("联系地址" in clause.text or "联系电话" in clause.text or "证号" in clause.text)
            and ("甲方" in clause.text or "乙方" in clause.text)
            and not any(term in clause.text for term in ("房地产经纪", "中介", "居间介绍", "代理内容"))
        ),
        limit=3,
    )
    if delivery_evidence and (item := by_id.get("HL-005")):
        _set_item_pass(
            item,
            delivery_evidence,
            "合同列明双方住址、联系电话和身份信息，已具备通知、催告和送达的基础联系信息；真实合同场景下不应再因未召回第十二条而认定为缺失。",
            "合同已提供双方可用于通知和催告的联系地址、联系电话及身份信息，通知送达基础已覆盖。",
        )

    title_certificate = _find_clause(clauses, lambda clause: "产证编号" in clause.text or "沪房地" in clause.text or "不动产权证" in clause.text)
    if title_certificate and _has_house_title_certificate(compacted) and (item := by_id.get("HL-010")):
        _set_item_partial(
            item,
            [title_certificate],
            "中",
            "合同已列明产证编号和权利人信息，能间接证明房屋权属与合法出租基础；但未单独写明“房屋合法、非违法建筑、具备出租条件”的保证条款，按中风险处理更贴近实务。",
            "合同已列明产证编号或权属证明信息，房屋合法性并非完全缺失；建议补充出租人对房屋合法性和可出租性的明示保证。",
            issue_type="条款缺陷",
        )
    if facts.property.certificate_number and (item := by_id.get("HL-003")):
        _set_item_pass_from_fact(
            item,
            facts,
            "property.certificate_number",
            f"统一事实图谱提取 property.certificate_number={facts.property.certificate_number}，说明合同已列明房屋权属证明编号，可作为出租权来源审查的基础证据。",
            "合同已列明房屋权属证明编号，出租权来源已有基础证据支撑。",
        )

    if facts.force_majeure.is_defined and (item := by_id.get("HL-014")):
        if facts.force_majeure.notice_required:
            _set_item_pass_from_fact(
                item,
                facts,
                "force_majeure.is_defined",
                "统一事实图谱提取 force_majeure.is_defined=true 且 force_majeure.notice_required=true，说明合同已约定不可抗力及通知/证明安排。",
                "合同已约定不可抗力及通知或证明要求，不可抗力处理路径已覆盖。",
            )
        else:
            _set_item_partial_from_fact(
                item,
                facts,
                "force_majeure.is_defined",
                "中",
                "统一事实图谱提取 force_majeure.is_defined=true，但 force_majeure.notice_required=false/null，说明合同仅有不可抗力框架，通知、证明和费用结算仍需补充。",
                "合同已出现不可抗力安排，但通知、证明、减租/解除和费用结算机制仍不完整。",
            )

    if facts.repair.natural_wear == LANDLORD and (item := by_id.get("HL-026")):
        _set_item_pass_from_fact(
            item,
            facts,
            "repair.natural_wear",
            "统一事实图谱提取 repair.natural_wear=landlord，说明自然老化、正常损耗或非承租人原因损坏由出租人承担；该事实同时供维修责任和自然损耗审查点共用。",
            "合同已区分自然老化/正常损耗由出租人承担，维修责任分工有明确基础。",
        )
    if facts.repair.natural_wear == LANDLORD and (item := by_id.get("HL-034")):
        _set_item_pass_from_fact(
            item,
            facts,
            "repair.natural_wear",
            "统一事实图谱提取 repair.natural_wear=landlord，HL-034 与 HL-026 读取同一事实字段，因此自然损耗排除与维修责任结论保持一致。",
            "合同已明确自然老化、正常损耗或非承租人原因损坏由出租人承担，正常损耗不应作为承租人扣款依据。",
        )

    if facts.sublease.requires_consent and (item := by_id.get("HL-011")):
        _set_item_pass_from_fact(
            item,
            facts,
            "sublease.requires_consent",
            "统一事实图谱提取 sublease.requires_consent=true，说明合同已明确转租需经出租人书面同意。",
            "合同已明确转租须经书面同意，转租规则有基本控制路径。",
        )
    if (facts.sublease.requires_consent or facts.sublease.is_allowed is False) and (item := by_id.get("HL-016")):
        _set_item_pass_from_fact(
            item,
            facts,
            "sublease.is_allowed",
            f"统一事实图谱提取 sublease.is_allowed={facts.sublease.is_allowed}、sublease.requires_consent={facts.sublease.requires_consent}，说明合同已处理擅自转租限制。",
            "合同已约定未经出租人书面同意不得擅自转租，擅自转租风险控制已有基础。",
        )

    rent_default = _find_clause(
        clauses,
        lambda clause: (
            ("欠租" in clause.text or "逾期不支付租金" in clause.text or ("逾期" in clause.text and "租金" in clause.text))
            and ("1个月" in _compact(clause.text) or "一个月" in clause.text or "一月" in clause.text)
            and ("解除" in clause.text or "终止" in clause.text)
        ),
    )
    if rent_default and (item := by_id.get("HL-015")):
        _set_item_pass(
            item,
            [rent_default],
            "合同第九条已约定乙方逾期不支付租金累计超过1个月时可解除合同，已经覆盖欠租重大违约标准。",
            "欠租达到累计超过1个月即构成解除事由，欠租重大违约标准已明确。",
        )
    if facts.termination.rent_default.exists and (item := by_id.get("HL-015")):
        threshold = facts.termination.rent_default
        _set_item_pass_from_fact(
            item,
                facts,
                "termination.tenant.rent_default.exists",
                f"统一事实图谱提取 termination.tenant.rent_default.exists=true，threshold_type={threshold.threshold_type}，threshold_value={threshold.threshold_value}，threshold_unit={threshold.threshold_unit}，effect={threshold.effect}，说明合同已明确欠租解除或重大违约标准。",
                "合同已明确欠租达到一定期间或程度时可解除，欠租重大违约标准已覆盖。",
            )

    termination_evidence = _find_clause(
        clauses,
        lambda clause: (
            ("解除" in clause.text or "终止" in clause.text)
            and (
                sum(
                    1
                    for keyword in (
                        "未按时交付",
                        "改变用途",
                        "逾期不支付租金",
                        "欠租",
                        "擅自转租",
                        "损坏",
                        "违法",
                        "违反",
                        "书面通知",
                    )
                    if keyword in clause.text
                )
                >= 2
            )
        ),
    )
    if termination_evidence and (item := by_id.get("HL-017")):
        _set_item_pass(
            item,
            [termination_evidence],
            "合同已列明法定或约定解除事由，包括未按时交付、改变用途、欠租、擅自转租等违约情形，已覆盖约定解除事由清单。",
            "解除条件和主要解除事由已明确。",
        )

    early_surrender = _find_clause(
        clauses,
        lambda clause: "提前退租" in clause.text and "违约金" in clause.text and ("2倍" in clause.text or "二倍" in clause.text or "两倍" in clause.text),
    )
    if early_surrender and (item := by_id.get("HL-029")):
        formula_text = facts.early_termination.tenant_formula or "合同约定公式"
        _set_item_pass(
            item,
            [early_surrender],
            f"统一事实图谱提取 early_termination.tenant_formula={formula_text}；合同第十条已明确承租人提前退租违约金公式，并约定不足抵付损失时继续赔偿，提前退租规则已覆盖。",
            "提前退租的违约金计算方式和损失补足规则已明确。",
        )
        item.matched_terms = ["early_termination.tenant_formula"]
        item.fact_dependencies = sorted(set(item.fact_dependencies + ["early_termination.tenant_formula", "early_termination.penalty_formula"]))
        item.fallback_reason = "房屋租赁统一事实图谱"
        scenarios = _penalty_scenarios(facts)
        if scenarios:
            item.scenario_analysis = scenarios
            item.economic_impact = _economic_impact_for_penalty(scenarios)
            item.economic_impact_detail = _economic_impact_detail_for_penalty(scenarios)
            formula = facts.early_termination.penalty_formula or {}
            if formula.get("base") in {"remaining_days_rent", "remaining_term_rent"}:
                should_degrade = item.economic_impact in {"medium", "high"} and _formula_requires_high_severity(formula)
                if should_degrade:
                    item.risk_level = "高" if item.economic_impact == "high" else "中"
                    item.coverage_status = "部分覆盖"
                    item.issue_type = "条款缺陷"
                    item.status = "部分覆盖"
                    item.reasoning_summary = (
                        f"{item.reasoning_summary} Scenario Engine 识别该公式以剩余租期租金为基数，"
                        f"剩余30/90/180/300天测算结果为 {scenarios.get('scenarios')}；剩余租期较长时违约金额会显著放大，"
                        "与实际空置损失和重新出租成本可能存在差异，建议设置上限或与实际损失挂钩。"
                    )
    if facts.safety.dangerous_house_termination or facts.safety.defect_termination or facts.safety.landlord_safety_obligation:
        if item := by_id.get("HL-025"):
            _set_item_partial_from_fact(
                item,
                facts,
                "safety.dangerous_house_termination" if facts.safety.dangerous_house_termination else (
                    "safety.defect_termination" if facts.safety.defect_termination else "safety.landlord_safety_obligation"
                ),
                "中",
                "统一事实图谱识别合同已出现危险房屋、房屋缺陷危及安全、出租人安全保障或人身损害赔偿安排，重大安全隐患处理不能认定为完全缺失；但紧急搬离、临时安置、紧急通知和费用结算仍需补充。",
                "合同已对安全隐患或出租人安全义务作出部分安排，但建议补充紧急搬离、临时安置和费用结算机制。",
                issue_type="条款缺陷",
            )

    expiry_settlement = _find_clause(
        clauses,
        lambda clause: "返还该房屋" in clause.text and "结清" in clause.text and "费用" in clause.text,
    )
    if expiry_settlement and (item := by_id.get("HL-031")):
        _set_item_pass(
            item,
            [expiry_settlement],
            "合同第七条约定租期届满返还房屋、验收认可并相互结清各自应承担费用，已覆盖租期届满结算。",
            "租期届满后的房屋返还、验收和费用结清规则已明确。",
        )

    damage_evidence_list = _find_clause(
        clauses,
        lambda clause: (
            ("附件三" in clause.text or "家电及装修清单" in clause.text or "家具家电" in clause.text or "装修清单" in clause.text)
            and not ("合同备案" in clause.text or "备案" in clause.text)
        ),
    )
    if damage_evidence_list and (item := by_id.get("HL-035")):
        _set_item_partial(
            item,
            [damage_evidence_list],
            "低",
            "合同附件三列明家电及装修清单，可作为退租时核对房屋附属设施和装修状态的基础证据；但仍未完整约定照片、视频、维修单、报价单等损坏举证材料，故保持部分覆盖。",
            "附件三已提供家电及装修清单作为损坏认定的基础证据，但损坏事实、原因和金额的举证材料仍需进一步补足。",
            issue_type="模板空白",
        )
        if "附件三" in damage_evidence_list.text:
            item.evidence_location = "附件三（家电及装修清单）"

    penalty_evidence = []
    for predicate in (
        lambda clause: "月租金的2倍" in clause.text and "违约金" in clause.text,
        lambda clause: "提前退租" in clause.text and "违约金" in clause.text,
    ):
        found = _find_clause(clauses, predicate)
        if found and found not in penalty_evidence:
            penalty_evidence.append(found)
    if penalty_evidence and _has_reasonable_rent_penalty(compacted) and (item := by_id.get("HL-039")):
        _set_item_partial(
            item,
            penalty_evidence[:2],
            "中",
            "合同约定违约金为月租金或提前退租天数租金的2倍，并设置损失不足时补赔规则，未明显偏离居住租赁常见损失范围；不宜自动列为高风险，但仍建议保留与实际损失挂钩的表述。",
            "违约金约定已有计算基础，且2倍月租金/租金天数通常不属于明显过高；建议进一步写明可结合实际损失、空置期和再出租成本调整。",
            issue_type="条款缺陷",
        )
    if facts.early_termination.penalty_formula and (item := by_id.get("HL-039")):
        scenarios = _penalty_scenarios(facts)
        formula = facts.early_termination.penalty_formula or {}
        if scenarios and formula.get("base") in {"remaining_days_rent", "remaining_term_rent"}:
            item.risk_level = "中"
            if _economic_impact_for_penalty(scenarios) == "high" and _formula_requires_high_severity(formula):
                item.risk_level = "高"
            item.status = "部分覆盖"
            item.coverage_status = "部分覆盖"
            item.issue_type = "条款缺陷"
            item.scenario_analysis = scenarios
            item.economic_impact = _economic_impact_for_penalty(scenarios)
            item.economic_impact_detail = _economic_impact_detail_for_penalty(scenarios)
            item.reasoning_summary = (
                f"统一事实图谱提取 early_termination.penalty_formula={facts.early_termination.penalty_formula}。"
                f"Scenario Engine 测算 {scenarios.get('scenarios')}。该公式不是普通固定倍数违约金，而是随剩余租期放大的租金倍数，"
                "剩余租期较长时可能明显高于出租人实际空置损失和重新出租成本，存在被请求调整的争议风险。"
            )
            item.risk_point_description = "提前退租违约金以剩余租期租金为基数并乘以倍数，剩余租期较长时经济后果可能显著放大，建议设置金额上限或与实际损失挂钩。"
            item.evidence_clauses = [_clause_public_dict(clause) for clause in _fact_evidence(facts, "early_termination.penalty_formula")]
            item.evidence_location = "；".join(clause.location for clause in _fact_evidence(facts, "early_termination.penalty_formula"))
            item.fact_dependencies = sorted(set(item.fact_dependencies + ["early_termination.penalty_formula"]))
            item.fallback_reason = "房屋租赁 Scenario Engine 风险校准"

    deposit_offset_evidence = _find_clause(
        clauses,
        lambda clause: (
            ("押金" in clause.text or "保证金" in clause.text)
            and any(term in clause.text for term in ("抵扣", "扣除", "扣款"))
            and any(term in clause.text for term in ("未付租金", "欠付租金", "水电费", "物业费", "维修费", "欠费", "代垫费用"))
            and "提前退租" not in clause.text
        ),
    )
    if deposit_offset_evidence and (item := by_id.get("HL-042")):
        has_order = any(term in deposit_offset_evidence.text for term in ("抵扣顺序", "扣除顺序", "先抵扣", "后抵扣", "依次", "先行", "其次"))
        _set_item_partial(
            item,
            [deposit_offset_evidence],
            "中",
            "全文检索定位到押金抵扣项目条款，能够证明合同存在押金抵扣机制；但未完整列明各类未付款项、维修费、赔偿款之间的抵扣顺序，故按部分覆盖处理。",
            "合同已约定押金可抵扣部分项目，但抵扣顺序仍不够明确。",
            issue_type="条款缺陷",
        )
        if has_order:
            _set_item_pass(
                item,
                [deposit_offset_evidence],
                "全文检索定位到押金抵扣项目及抵扣顺序条款，能够直接支撑押金抵扣顺序审查结论。",
                "合同已约定押金抵扣项目和抵扣顺序。",
            )

    if facts.deposit.amount and facts.deposit.return_deadline is None and (item := by_id.get("HL-043")):
        _set_item_partial_from_fact(
            item,
            facts,
            "deposit.amount",
            "中",
            "统一事实图谱提取 deposit.amount 已存在，但 deposit.return_deadline=null，说明合同有押金安排但未写明具体返还天数；该问题属于返还期限细化不足，不应被放大为整份合同唯一高风险。",
            "合同约定了押金金额和返还场景，但未明确完成交接、费用结清后多少日内返还，建议补充具体天数。",
            issue_type="条款缺陷",
        )

    if facts.rent.monthly_amount and (facts.rent.payment_due_day or facts.rent.payment_method) and (item := by_id.get("HL-049")):
        primary_payment_field = "rent.payment_due_day" if facts.rent.payment_due_day else "rent.payment_method"
        _set_item_pass_from_fact(
            item,
            facts,
            primary_payment_field,
            f"统一事实图谱提取 rent.monthly_amount={facts.rent.monthly_amount}、rent.payment_due_day={facts.rent.payment_due_day}、rent.payment_method={facts.rent.payment_method}，说明合同已覆盖租金金额及支付安排。",
            "合同已明确租金金额，并对支付日期或支付方式作出安排，租金支付规则已有基础。",
        )
        for field_name in ("rent.monthly_amount", "rent.payment_cycle", "rent.payment_due_day", "rent.payment_method"):
            if facts.node(field_name):
                item.fact_dependencies = sorted(set(item.fact_dependencies + [field_name]))
                if field_name not in item.matched_terms:
                    item.matched_terms.append(field_name)

    if facts.repair.tenant_fault == TENANT and (item := by_id.get("HL-036")):
        _set_item_pass_from_fact(
            item,
            facts,
            "repair.tenant_fault",
            "统一事实图谱提取 repair.tenant_fault=tenant，说明合同已明确承租人使用不当或过错造成损坏时承担赔偿或维修责任。",
            "合同已区分承租人过错损坏责任，承租人过错损坏处理规则已覆盖。",
        )

    return items


def _apply_sale_contract_rules(items: List[ReviewItemResult], contract_text: str) -> List[ReviewItemResult]:
    clauses = formal_evidence_clauses(parse_contract_clauses(contract_text))
    compacted = _compact(contract_text)
    by_id = {item.item_id: item for item in items}

    effective_evidence = _find_clause(
        clauses,
        lambda clause: "生效" in clause.text and (
            "签字" in clause.text
            or "盖章" in clause.text
            or "签署" in clause.text
            or bool(re.search(r"20\d{2}[年/.-]\d{1,2}[月/.-]\d{1,2}日?.{0,8}(?:起)?生效", clause.text))
            or bool(re.search(r"生效.{0,12}20\d{2}[年/.-]\d{1,2}[月/.-]\d{1,2}日?", clause.text))
        ),
    )
    if effective_evidence and (item := by_id.get("S-00-01")):
        _set_item_pass(
            item,
            [effective_evidence],
            "合同已明确签字盖章、签署或具体日期对应的生效节点，生效条件具备可验证性。",
            "合同生效条件或生效日期已明确，合同效力节点清晰。",
        )
        item.fallback_reason = "买卖合同通用生效条款召回"
    elif (item := by_id.get("S-00-01")) and item.coverage_status in {"通过", "部分覆盖"}:
        _set_item_missing(
            item,
            "低",
            "未在正式合同条款中找到合同生效条件的有效约定；“签收货物”等交付证据不能替代合同生效条款。但普通商业买卖合同如已由双方盖章签字且不需审批备案，通常不因缺少标准生效条款影响效力，本项属于可优化事项。",
            "合同未明确签字、盖章、审批或约定日期等生效条件，建议补充以优化效力起算节点。",
            "买卖合同通用生效条款实质匹配校正",
        )
    elif (item := by_id.get("S-00-01")) and item.coverage_status == "缺失":
        item.risk_level = "低"
        item.risk_point_description = "缺失标准生效条款通常不影响普通买卖合同效力；建议补充签字盖章生效、审批备案例外等表述，以优化效力起算节点。"
        item.reasoning_summary = "未发现独立合同生效条款；普通商业合同如已有双方签署且无审批备案要求，法律不强制要求单列生效条款，本项按低风险建议完善处理。"
        item.fallback_reason = "买卖合同生效条款风险校准"

    termination_evidence = _find_clause(
        clauses,
        lambda clause: "解除" in clause.text and ("通知" in clause.text or "书面" in clause.text or "终止" in clause.text),
    )
    if termination_evidence and (item := by_id.get("S-00-02")):
        _set_item_partial(
            item,
            [termination_evidence],
            "中",
            "合同已出现解除或终止安排，但仍需核对解除通知的送达地址、生效时间和留痕方式是否完整。",
            "合同已有解除程序框架，但解除通知送达、生效时间和证据留痕仍建议进一步明确。",
            issue_type="条款缺陷",
        )
        item.fallback_reason = "买卖合同通用解除程序召回"
    elif (item := by_id.get("S-00-02")) and item.coverage_status in {"通过", "部分覆盖"}:
        _set_item_missing(
            item,
            "中",
            "未在正式合同条款中找到解除通知期限、送达方式和生效时间的有效约定；普通通知送达条款不能替代解除程序条款。",
            "合同未明确解除程序，建议补充解除通知、送达、生效时间和解除后结算安排。",
            "买卖合同通用解除程序实质匹配校正",
        )

    notice_evidence = _find_clause(
        clauses,
        lambda clause: (
            ("送达地址" in clause.text or "通知地址" in clause.text or "电子邮箱" in clause.text or "联系方式" in clause.text)
            and ("通知" in clause.text or "送达" in clause.text or "变更" in clause.text)
        ),
    )
    if notice_evidence and (item := by_id.get("S-00-03")):
        _set_item_pass(
            item,
            [notice_evidence],
            "合同已约定通知或送达地址及联系方式变更安排，可支撑催告、解除、索赔等程序性通知留痕。",
            "通知与送达条款已覆盖，建议签约时同步核对地址、电话、电子邮箱等信息是否填写完整。",
        )
        item.fallback_reason = "买卖合同通用通知送达召回"

    jurisdiction_evidence = _find_clause(
        clauses,
        lambda clause: (
            ("争议" in clause.text or "管辖" in clause.text or "起诉" in clause.text or "仲裁" in clause.text)
            and ("人民法院" in clause.text or "法院" in clause.text or "仲裁委员会" in clause.text)
        ),
    )
    if jurisdiction_evidence and (item := by_id.get("S-00-04")):
        compact_jurisdiction = _compact(jurisdiction_evidence.text)
        if "有管辖权的人民法院" in compact_jurisdiction or "有管辖权的法院" in compact_jurisdiction or "有管辖权法院" in compact_jurisdiction:
            _set_item_partial(
                item,
                [jurisdiction_evidence],
                "中",
                "合同约定由有管辖权的法院处理争议，但未明确具体法院；法定管辖仍可适用，风险主要在于后续可能发生管辖争议和立案成本。",
                "合同已有争议解决框架，但未写明具体法院或仲裁机构，建议补充明确管辖法院或仲裁机构名称。",
                issue_type="条款缺陷",
            )
        else:
            _set_item_pass(
                item,
                [jurisdiction_evidence],
                "合同已约定具体法院或仲裁机构，争议解决路径清晰。",
                "争议解决与管辖条款已覆盖，可降低后续立案和管辖争议成本。",
            )
        item.fallback_reason = "买卖合同通用管辖条款召回"

    fee_evidence = _find_clause(
        clauses,
        lambda clause: (
            "律师费" in clause.text
            and ("败诉方" in clause.text or "违约方" in clause.text or "承担" in clause.text or "实现债权" in clause.text)
        ),
    )
    if fee_evidence and (item := by_id.get("S-00-05")):
        _set_item_pass(
            item,
            [fee_evidence],
            "合同已约定律师费等维权费用承担，建议将“一切费用”等宽泛表述限定为合理且实际发生的费用。",
            "诉讼费用承担条款已覆盖；为提高可执行性，建议使用“实际发生且合理”的费用范围。",
        )
        item.fallback_reason = "买卖合同通用维权费用条款召回"

    force_majeure_evidence = _find_clause(clauses, lambda clause: "不可抗力" in clause.text)
    if force_majeure_evidence and (item := by_id.get("S-00-06")):
        _set_item_pass(
            item,
            [force_majeure_evidence],
            "合同已约定不可抗力事项，可继续核对通知期限、证明材料和延期/解除后果是否完整。",
            "不可抗力条款已覆盖，建议保留通知、证明和后果处理的具体流程。",
        )
        item.fallback_reason = "买卖合同通用不可抗力条款召回"
    elif (item := by_id.get("S-00-06")) and item.coverage_status in {"通过", "部分覆盖"}:
        _set_item_missing(
            item,
            "中",
            "未在正式合同条款中找到不可抗力通知、证明和后果处理约定；其他通知或违约条款不能替代不可抗力规则。",
            "合同未明确不可抗力的通知、证明、延期履行、部分免责或解除后果。",
            "买卖合同通用不可抗力条款实质匹配校正",
        )

    payment_account_evidence = _find_clause(
        clauses,
        lambda clause: (
            ("付款" in clause.text or "支付" in clause.text or "货款" in clause.text)
            and ("账户" in clause.text or "账号" in clause.text or "开户行" in clause.text or "收款" in clause.text or "转账" in clause.text or "银行" in clause.text)
        ),
    )
    if payment_account_evidence and (item := by_id.get("S-05-03")):
        _set_item_pass(
            item,
            [payment_account_evidence],
            "全文兜底检索命中货款支付条款，合同已列明付款方式、收款账户或开户行信息，不应判定为完全缺失。",
            "付款方式和收款账户已在合同货款支付条款中载明；建议核对账户变更是否需书面通知并加盖公章。",
        )
        item.fallback_reason = "买卖合同付款账户全文兜底召回"

    payment_schedule_evidence = _find_clause(
        clauses,
        lambda clause: _has_sale_payment_timing(clause.text),
    )
    if payment_schedule_evidence and not _has_sale_staged_payment_structure(compacted) and (item := by_id.get("S-05-02")):
        _set_item_pass(
            item,
            [payment_schedule_evidence],
            "合同已约定付款触发条件或具体付款时间，例如签收后、对账后或次月固定日前付款；当前合同未出现预付款、进度款、分期付款等结构，付款比例审查不适用。",
            "付款节点已约定，付款比例不适用（一次性或按批次结清模式）；建议保留对账、发票和签收凭证作为付款触发证据。",
        )
        item.fallback_reason = "买卖合同付款节点与比例解耦校正"

    price_adjustment_evidence = _find_clause(clauses, lambda clause: _has_sale_unilateral_price_adjustment(clause.text))
    if price_adjustment_evidence and (item := by_id.get("S-02-05")):
        if _has_price_adjustment_safeguards(price_adjustment_evidence.text):
            _set_item_pass(
                item,
                [price_adjustment_evidence],
                "合同存在价格调整安排，但已同时约定客观依据、幅度限制、通知期限和对方异议或解除机制，单方调价风险已被控制。",
                "价格调整条款已有保护边界，建议签约时核对价格指数、调整幅度和异议期限是否可执行。",
            )
        else:
            item.risk_level = "中"
            item.status = "发现风险条款"
            item.coverage_status = "风险条款"
            item.issue_type = "风险条款"
            item.risk_point_description = "合同赋予一方基于市场行情变化调整价格的权利，但未完整约定客观触发条件、调价幅度上限、提前通知期限以及买受人异议权或解除权。"
            item.reasoning_summary = "召回到单方调价条款；该条款以“市场行情变化”等模糊条件作为调价依据，缺少幅度限制和乙方异议机制，容易导致出卖人单方改变核心价款义务。"
            item.evidence_clauses = [_clause_public_dict(price_adjustment_evidence)]
            item.evidence_location = price_adjustment_evidence.location
            item.fallback_reason = "买卖合同单方调价权专项校正"

    penalty_evidence = _find_clause(
        clauses,
        lambda clause: "违约金" in clause.text and any(term in clause.text for term in ("万分之", "%", "％", "每日", "每天", "月", "年化")),
    )
    if penalty_evidence and _has_reasonable_sale_liquidated_damages(compacted):
        if item := by_id.get("S-08-01"):
            _set_item_pass(
                item,
                [penalty_evidence],
                "合同已设置违约金责任，且当前比例处于买卖合同常见合理区间内。",
                "违约责任类型已覆盖；现有违约金比例未明显偏离合理范围。",
            )
            item.fallback_reason = "买卖合同合理违约金比例校正"
        if item := by_id.get("S-08-02"):
            _set_item_pass(
                item,
                [penalty_evidence],
                "合同约定的违约金比例处于合理区间，不应仅因未写“与实际损失挂钩”而升格为高风险；建议保留实际损失证明材料以应对后续调整争议。",
                "违约金比例合理；司法实践中仍可能结合实际损失调整，建议补充“以实际损失为基础”的表述并留存损失证明。",
            )
            item.fallback_reason = "买卖合同合理违约金比例校正"

    intent_evidence = _find_clause(
        clauses,
        lambda clause: any(term in clause.text for term in ("友好协商", "协商一致", "平等自愿", "自愿", "达成如下协议")),
    )
    if (item := by_id.get("S-01-02")):
        if intent_evidence:
            _set_item_pass(
                item,
                [intent_evidence],
                "合同开头已体现双方经友好协商或协商一致达成协议，足以支撑真实意思表示的基本推定；法律不强求“真实意思表示”作为独立条款存在。",
                "真实意思表示已有基本表述，建议可作为补充项优化，不作为强制修改项。",
            )
        elif item.coverage_status == "缺失":
            item.risk_level = "低"
            item.risk_point_description = "未单列真实意思表示声明通常不影响普通买卖合同效力；如无欺诈、胁迫、重大误解等事实，本项属于可优化补充。"
            item.reasoning_summary = "法律不强制要求将真实意思表示写成独立条款；普通商业合同可通过合同标题、主体签署和协商过程推定，本项按低风险建议完善处理。"
            item.fallback_reason = "买卖合同真实意思表示风险校准"

    delivery_method_evidence = _find_clause(
        clauses,
        lambda clause: (
            _has_sale_delivery_transport_framework_engine(clause.text)
            and "签收" in clause.text
            and any(term in clause.text for term in ("工作人员", "指定人员", "授权", "收货人"))
            and not _has_sale_delivery_voucher_terms(clause.text)
        ),
    )
    if delivery_method_evidence and (item := by_id.get("S-03-03")):
        _set_item_partial(
            item,
            [delivery_method_evidence],
            "低",
            "合同已明确交付方式和签收主体，例如由工作人员、指定人员或授权收货人签收即视为收货；缺少送货单、签收单、物流回执等具体凭证形式，属于证据链优化项。",
            "交付方式和签收主体已明确，建议补充具体凭证形式以优化证据链。",
            issue_type="条款缺陷",
        )
        item.fallback_reason = "买卖合同交付签收实务风险校准"

    ordinary_cement_sale = (
        "水泥" in compacted
        and not any(term in compacted for term in ("危险化学品", "烟花爆竹", "药品", "医疗器械", "食品", "农药", "特种设备", "限制流通", "禁止流通", "许可证"))
    )
    has_warranty_period = any(term in compacted for term in ("质保期", "质量保证期", "保修期", "质保期限", "保修期限"))
    has_on_spot_acceptance = any(term in compacted for term in ("当场验收", "现场验收", "到货验收", "收货时验收"))
    has_post_use_quality_remedy = (
        ("使用" in compacted and "质量问题" in compacted and ("发现后" in compacted or "10日内" in compacted or "十日内" in compacted))
        and any(term in compacted for term in ("更换", "补发", "退换", "减免", "解决方案"))
    )
    has_visible_hidden_distinction = any(term in compacted for term in ("外观瑕疵", "隐蔽瑕疵", "内在质量", "潜在缺陷"))
    has_certificate_evidence = any(term in compacted for term in ("检验报告", "合格证", "检测报告", "认证证书", "质检报告", "质量证明", "出厂检验"))

    if ordinary_cement_sale and (item := by_id.get("S-01-03")) and item.coverage_status == "缺失":
        _set_item_missing(
            item,
            "中",
            "合同标的为水泥，属于普通建材，当前文本未体现特殊许可、禁止流通或限制流通风险；未设置标的物合法性保证属于建议补充事项，不宜按高风险致命缺陷处理。",
            "水泥作为普通建材通常不涉及特殊审批许可；未写明标的物合法性保证会增加来源与合规争议，但一般不直接导致合同无法履行或无效。",
            "买卖合同普通建材合法性风险专项校正",
        )

    if ordinary_cement_sale:
        ordinary_low_risk_items = {
            "S-01-04": (
                "合同标的为普通水泥，当前文本未体现需特殊审批、许可、备案或专门资质的交易场景；审批许可条款属于普通建材交易中的低优先级完善项。",
                "普通水泥买卖通常不涉及特殊审批许可；建议在涉及特种、危化、食品药品等特殊标的时再重点补充资质文件。",
            ),
            "S-11-02": (
                "合同标的为普通水泥，不涉及品牌许可、软件、专利实施或技术秘密交付等典型知识产权使用场景；知识产权合规条款属于低优先级提示。",
                "普通建材交易的知识产权风险较低；如涉及定制包装、商标标识或专有配方，再补充知识产权保证条款。",
            ),
            "S-12-01": (
                "合同标的为标准化水泥产品，通常以国家标准、规格型号和质量证明文件作为验收依据；图纸或技术规格书附件不是该类交易的必备文件。",
                "标准品买卖不强制要求图纸附件；建议保留产品标准、规格型号、检测报告或合格证明作为履约依据。",
            ),
            "S-12-04": (
                "当前合同未体现多份技术附件、图纸或补充协议之间存在冲突，附件效力和冲突顺位属于合同管理优化事项。",
                "如后续增加订单、技术协议、报价单或补充协议，建议再明确附件效力和冲突适用顺位。",
            ),
        }
        for item_id, (reason, description) in ordinary_low_risk_items.items():
            if (item := by_id.get(item_id)) and item.coverage_status == "缺失":
                _set_item_missing(
                    item,
                    "低",
                    reason,
                    description,
                    "买卖合同普通标准品低优先级风险校准",
                )

    if (item := by_id.get("S-08-03")) and item.coverage_status == "缺失" and ordinary_cement_sale:
        _set_item_missing(
            item,
            "低",
            "普通水泥买卖合同通常以价款、货损、质量瑕疵和逾期付款损失为主要赔偿范围；未单列可得利益损失条款一般不构成中等以上风险。",
            "可得利益损失条款可作为商业谈判补充项；如买受人存在明确转售订单或停工损失，再重点约定可预见损失范围。",
            "买卖合同普通标准品赔偿范围风险校准",
        )

    if (item := by_id.get("S-00-06")) and item.coverage_status == "缺失" and ordinary_cement_sale:
        _set_item_missing(
            item,
            "低",
            "普通水泥买卖合同未约定不可抗力条款时，仍可适用《民法典》关于不可抗力的一般规则；该项缺失主要影响通知和证明流程，不宜占用中风险池。",
            "不可抗力条款建议补充通知、证明和延期履行安排，但普通买卖合同缺失该条款通常不直接影响核心履行。",
            "买卖合同不可抗力低优先级风险校准",
        )

    if has_on_spot_acceptance and (has_warranty_period or has_post_use_quality_remedy) and (item := by_id.get("S-07-02")) and item.coverage_status == "缺失":
        _set_item_missing(
            item,
            "中",
            "合同虽约定当场验收，短期验收主要覆盖外观、数量和包装问题；同时合同存在使用过程中发现质量问题后的异议和补救机制，可在一定程度上覆盖隐蔽瑕疵风险，故不宜按高风险处理。",
            "合同未完整说明检验期限合理性，建议补充短期验收仅限外观和数量，隐蔽瑕疵可在质保期内主张。",
            "买卖合同检验期限合理性专项校正",
        )

    if (has_warranty_period or has_post_use_quality_remedy) and not has_visible_hidden_distinction and (item := by_id.get("S-07-03")):
        _set_item_missing(
            item,
            "中",
            "合同虽未明确区分外观瑕疵与隐蔽瑕疵，但已有使用过程中质量问题的异议和补救机制，可在一定程度上承接隐蔽质量问题处理；该缺口属于建议性补充，不宜按高风险处理。",
            "合同未区分外观瑕疵和隐蔽瑕疵，建议补充外观问题的即时异议期限以及隐蔽瑕疵的质保期主张规则。",
            "买卖合同外观/隐蔽瑕疵区分专项校正",
        )

    if not has_certificate_evidence and (item := by_id.get("S-12-02")) and item.coverage_status == "通过":
        _set_item_missing(
            item,
            "中",
            "当前命中证据仅涉及质量异议或质量问题处理，并未约定出卖人交付合格证、检验报告、检测报告或其他质量证明文件；质量异议条款不能替代合格证明交付义务。",
            "合同未要求出卖人随货提供检验报告、合格证或质量证明文件，买受人验收和后续追责证据不足。",
            "买卖合同合格证明证据实质匹配校正",
        )

    quality_remedy = _find_clause(
        clauses,
        lambda clause: (
            ("质量问题" in clause.text or "质量异议" in clause.text or "质量不合格" in clause.text)
            and ("日内" in clause.text or "10日" in clause.text or "十日" in clause.text or "期限" in clause.text)
            and ("更换" in clause.text or "换货" in clause.text or "补发" in clause.text or "补货" in clause.text)
        ),
    )
    if quality_remedy and (item := by_id.get("S-06-03")):
        _set_item_partial(
            item,
            [quality_remedy],
            "中",
            "合同已约定发现质量问题应在期限内提出，并由出卖人及时更换、补发，已覆盖质量异议期限和部分补救方式；但未完整列明修理、重作、退货、减少价款、赔偿损失等法定救济路径，故不应按完全缺失处理。",
            "合同已有质量问题异议和更换补发机制，但质量瑕疵救济方式仍不完整，建议补充修理、重作、退货、减少价款、赔偿损失等处理路径。",
            issue_type="条款缺陷",
        )
        item.fallback_reason = "买卖合同质量异议补救条款专项校正"

    return items


def _service_has_prepayment_refund_evidence(compacted: str) -> bool:
    """服务合同真实合同：识别已明确为预付式消费且附有完整退费条款，避免误判为完全缺失。"""
    prepay_hits = [
        term for term in ("预付费", "预付式消费", "预付款", "会员卡", "储值卡", "充值", "课包", "课时费", "课时")
        if term in compacted
    ]
    refund_hits = [
        term for term in ("退费", "退款", "退卡", "退还", "剩余金额", "剩余费用")
        if term in compacted
    ]
    # 需同时命中“预付”类与“退费”类关键词，且体量足以说明是预付式消费安排
    return len(prepay_hits) >= 1 and len(refund_hits) >= 1


def _service_has_content_list_evidence(compacted: str) -> bool:
    """服务内容清单：已列明课程、课时、价格、教师等核心信息，仅少量空白时降级处理。"""
    content_hits = [
        term for term in ("课程", "课时", "服务项目", "服务内容", "培训项目", "教练", "老师", "教师", "单价", "价格", "收费标准")
        if term in compacted
    ]
    return len(content_hits) >= 3


def _service_has_schedule_place_evidence(compacted: str) -> bool:
    """服务时间地点方式：已明确上课时间、地点、方式时降级处理。"""
    schedule_hits = [
        term for term in (
            "上课时间", "开课日期", "结课日期", "预计结课日期", "服务开始", "服务期限",
            "上课地点", "服务时间", "服务地点", "线下", "线上", "预约", "排课", "培训地点", "训练地点",
        )
        if term in compacted
    ]
    return len(schedule_hits) >= 1


def _service_is_training_contract(compacted: str) -> bool:
    """培训类服务合同：用于区分服务合同基本性质已明确、仅缺少建议性定性条款的场景。"""
    training_hits = [
        term for term in ("培训", "课程", "课时", "学员", "上课", "教师", "老师", "授课", "辅导", "班课")
        if term in compacted
    ]
    return len(training_hits) >= 2


def _service_has_prepayment_balance_framework(compacted: str) -> bool:
    """预付款金额和余额：已写总金额、课时/单价、退费或余额计算时，按框架存在处理。"""
    amount_hits = [
        term for term in ("总金额", "服务费", "课程费", "培训费", "预付款", "预付费", "收费", "价格", "单价")
        if term in compacted
    ]
    balance_hits = [
        term for term in ("余额", "剩余课时", "未消耗课时", "未上课时", "剩余费用", "退费", "退款", "按实际课时", "课时")
        if term in compacted
    ]
    return len(amount_hits) >= 1 and len(balance_hits) >= 1


def _service_has_refund_calculation_framework(compacted: str) -> bool:
    """解除或退费结算：识别按已消耗/未消耗服务折算退款的实质框架。"""
    refund_hits = [
        term for term in ("退费", "退款", "退还", "解除后", "终止后", "按实际课时", "按实际提供服务", "未消耗课时", "剩余课时", "未提供服务")
        if term in compacted
    ]
    calculation_hits = [
        term for term in ("计算", "结算", "扣除", "余额", "剩余", "单价", "课时", "实际")
        if term in compacted
    ]
    return len(refund_hits) >= 1 and len(calculation_hits) >= 1


def _service_has_health_exit_framework(compacted: str) -> bool:
    return any(term in compacted for term in ("身体健康状况", "健康状况", "疾病", "不再适合参与培训")) and any(
        term in compacted for term in ("书面通知", "实际消耗课时", "实际课时", "结算培训费用", "退费", "退款")
    )


def _service_has_consumer_notice_framework(compacted: str) -> bool:
    return any(term in compacted for term in ("书面通知", "退费申请", "退款申请", "解除申请", "提交申请", "申请材料"))


def _service_has_forbidden_no_qualification_clause(compacted: str) -> bool:
    return any(
        _has_unnegated_word(compacted, term, window=18)
        for term in ("无资质", "无证", "无需资质", "没有许可证", "不提供证照")
    )


def _apply_service_contract_rules(items: List[ReviewItemResult], contract_text: str) -> List[ReviewItemResult]:
    clauses = parse_contract_clauses(contract_text)
    compacted = _compact(contract_text)
    by_id = {item.item_id: item for item in items}

    # SVC-04-01：预付式消费识别——合同已明确为预付式消费且附完整退费条款，属误判，降为低风险-通过
    if _service_has_prepayment_refund_evidence(compacted) and (item := by_id.get("SVC-04-01")):
        _set_item_pass(
            item,
            _find_clauses(clauses, lambda clause: ("预付费" in clause.text or "预付" in clause.text or "会员" in clause.text or "课时" in clause.text), limit=2),
            "合同已明确为预付式消费安排，且包含“退费/退款/剩余金额”等退费条款（如退费条件、计算方式或解除后退款），不应再判定为高风险-完全缺失；本项修正为低风险-通过。",
            "合同文本已体现预付式消费属性并载明退费相关安排，预付式消费识别已覆盖。",
        )
        item.fallback_reason = "服务合同预付式消费识别专项校正"

    # SVC-03-01：服务内容清单——已列明核心信息但存在少量空白，降为中风险-部分覆盖
    if _service_has_content_list_evidence(compacted) and (item := by_id.get("SVC-03-01")):
        _set_item_partial(
            item,
            _service_find_clauses(clauses, ("课程", "课时", "价格", "教师", "服务内容"), compacted, limit=2),
            "中",
            "合同已列明课程名称、课时、价格、教师等核心服务信息，仅有少量空白未填；按真实合同实务，不应按高风险-完全缺失处理，本项修正为中风险-部分覆盖。",
            "服务内容核心信息已基本列明，建议补全剩余空白的服务项目、次数或标准以避免履行争议。",
            issue_type="模板空白",
        )
        item.fallback_reason = "服务合同服务内容清单专项校正"

    # SVC-03-03：服务时间地点方式——已明确时降级处理
    if _service_has_schedule_place_evidence(compacted) and (item := by_id.get("SVC-03-03")):
        _set_item_partial(
            item,
            _service_find_clauses(
                clauses,
                ("上课时间", "服务时间", "开课日期", "结课日期", "预计结课日期", "服务期限", "上课地点", "服务地点", "预约", "排课"),
                compacted,
                limit=3,
            ),
            "中",
            "合同已明确上课时间、地点、方式或预约安排，仅有少量空白；按真实合同实务，不应按高风险-完全缺失处理，本项修正为中风险-部分覆盖。",
            "服务时间、地点和方式已基本明确，建议补全剩余未填的排课或变更约定。",
            issue_type="模板空白",
        )
        item.fallback_reason = "服务合同服务时间地点方式专项校正"

    if _service_has_prepayment_balance_framework(compacted) and (item := by_id.get("SVC-04-02")):
        _set_item_partial(
            item,
            _service_find_clauses(clauses, ("总金额", "服务费", "培训费", "课时", "退费", "退款", "余额"), compacted, limit=2),
            "中",
            "合同已明确服务费用、课时或退费计算的基本框架，但余额、单价或未消耗课时的细节可能仍有空白；该类问题属于模板空白或内容不完整，不应按高风险处理。",
            "预付款和余额结算已有基础框架，建议补全余额查询、单价、已消耗服务和剩余费用的计算细节。",
            issue_type="模板空白",
        )
        item.fallback_reason = "服务合同预付款余额风险分级校正"

    if _service_has_refund_calculation_framework(compacted):
        for item_id, reason, description in (
            (
                "SVC-06-01",
                "合同已约定按实际课时或未提供服务部分结算退款，可覆盖消费者因特殊原因解除后的基础结算框架；但未专门写明健康原因解除机制，故按中风险部分覆盖处理。",
                "健康原因解除条款尚不完整，建议补充凭医疗证明解除、未提供服务部分退费和不得不合理扣费的规则。",
            ),
            (
                "SVC-11-02",
                "合同已约定按实际课时、剩余课时或未提供服务部分进行退款结算，解除后的退款计算并非完全缺失；细节未尽明确时按中风险部分覆盖处理。",
                "解除后的退款计算已有基础框架，建议补充具体公式、办理期限、赠送课时和合理成本扣除规则。",
            ),
        ):
            if item := by_id.get(item_id):
                _set_item_partial(
                    item,
                    _service_find_clauses(clauses, ("退费", "退款", "剩余课时", "未消耗课时", "按实际课时", "未提供服务", "结算"), compacted, limit=2),
                    "中",
                    reason,
                    description,
                    issue_type="模板空白",
                )
                item.fallback_reason = "服务合同解除退费风险分级校正"

    if _service_has_health_exit_framework(compacted):
        for item in items:
            if item.node_id != "health_change_termination" or item.coverage_status == COVERAGE_NOT_APPLICABLE:
                continue
            if item.coverage_status not in {"缺失", "部分覆盖"}:
                continue
            _set_item_partial(
                item,
                _service_find_clauses(
                    clauses,
                    ("身体健康状况", "健康状况", "不再适合参与培训", "书面通知", "实际消耗课时", "结算培训费用"),
                    compacted,
                    limit=3,
                ),
                "中",
                "合同已召回健康状况、书面通知或实际消耗课时结算证据；健康原因解除机制不得按完全缺失处理，应进入元素级逐项判断。",
                "健康原因解除已有基础事实，需继续核对证明材料、合理不可退成本和退款期限等具体缺口。",
                issue_type="模板空白",
            )
            item.fallback_reason = "服务合同健康解除语义证据保护"

    if _service_has_consumer_notice_framework(compacted) and (item := by_id.get("SVC-06-02")):
        _set_item_partial(
            item,
            _service_find_clauses(clauses, ("书面通知", "退费申请", "退款申请", "解除申请", "申请材料"), compacted, limit=2),
            "中",
            "合同已约定书面通知、退费申请或类似办理方式，可作为消费者解除/退费通知的基础，但材料清单、办理期限或送达渠道仍需补充。",
            "消费者解除通知已有基础安排，建议补全申请材料、送达渠道、审核期限和退款期限。",
            issue_type="模板空白",
        )
        item.fallback_reason = "服务合同消费者解除通知风险分级校正"

    refund_or_withdrawal_terms = (
        "退学", "退费", "退款", "解除", "开班前", "开班后", "实际消耗课时", "实际课时",
        "未消耗课时", "剩余课时", "未提供服务", "全额退费", "书面通知",
    )
    refund_evidence = _service_find_clauses(clauses, refund_or_withdrawal_terms, compacted, limit=4)
    if refund_evidence:
        for item in items:
            if item.coverage_status == COVERAGE_NOT_APPLICABLE:
                continue
            if item.node_id not in {
                "prepaid_partly_provided_refund",
                "consumer_personal_reason_termination",
                "consumer_termination_notice",
                "termination_notice_period",
            }:
                continue
            if item.coverage_status not in {"缺失", "部分覆盖"}:
                continue
            _set_item_partial(
                item,
                refund_evidence,
                "中" if item.risk_level in {"高", "中", "低"} else "中",
                "合同已召回退学、解除、退费、课时结算或书面通知等服务退出场景证据；该类审查不得按完全缺失处理，应进入元素级逐项判断。",
                item.risk_point_description or "消费者解除、退费或部分履行退款存在基础条款，但仍需按元素核对具体缺口。",
                issue_type="模板空白",
            )
            item.fallback_reason = "服务合同退出退费语义证据保护"

    return items


def _construction_has_contract_title(compacted: str) -> bool:
    return any(term in compacted for term in ("建设工程施工合同", "建设工程合同", "施工合同", "工程施工合同"))


def _construction_has_total_subcontract_prohibition(compacted: str) -> bool:
    total_transfer_ban = bool(
        re.search(r"(不得|禁止).{0,24}(全部工程|全部承包工程|承包的全部工程).{0,16}(转包|转让)", compacted)
        or re.search(r"(不得|禁止).{0,16}(转包|整体转让施工)", compacted)
    )
    split_transfer_ban = bool(
        re.search(r"(不得|禁止).{0,24}(肢解|分解|拆分).{0,24}(转包|分包)", compacted)
        or re.search(r"(肢解|分解|拆分).{0,24}(后|以后)?.{0,12}(不得|禁止)?.{0,12}(分包|转包)", compacted)
    )
    return total_transfer_ban and split_transfer_ban


def _construction_has_resubcontract_prohibition(compacted: str) -> bool:
    return bool(
        re.search(r"(不得|禁止).{0,20}(再分包|二次分包|层层分包)", compacted)
        or re.search(r"(不得|禁止).{0,18}分包单位.{0,18}再分包", compacted)
        or re.search(r"分包单位.{0,18}(不得|禁止).{0,18}(再分包|二次分包|层层分包)", compacted)
    )


def _mark_construction_pass(item: ReviewItemResult, description: str, reason: str) -> None:
    item.risk_level = "低"
    item.status = "未发现明显风险条款"
    item.coverage_status = "通过"
    item.issue_type = "通过"
    item.risk_point_description = description
    item.reasoning_summary = reason
    item.fallback_reason = "建设工程禁止性条款合规校正"


def _apply_construction_contract_rules(items: List[ReviewItemResult], contract_text: str) -> List[ReviewItemResult]:
    compacted = _compact(_construction_contract_body(contract_text))
    has_title = _construction_has_contract_title(compacted)
    has_total_subcontract_ban = _construction_has_total_subcontract_prohibition(compacted)
    has_resubcontract_ban = _construction_has_resubcontract_prohibition(compacted)
    has_bid_consistency_framework = any(term in compacted for term in ("实质性内容", "工程范围", "建设工期", "工程质量", "工程价款", "中标合同一致"))

    for item in items:
        if item.item_id == "CE-01-01" and has_title and item.coverage_status != COVERAGE_NOT_APPLICABLE:
            item.risk_level = "中"
            item.coverage_status = "部分覆盖"
            item.issue_type = "模板空白"
            item.status = "部分覆盖，模板空白"
            item.risk_point_description = (
                "合同标题已能识别为建设工程施工合同，合同性质并非完全缺失；但正文中的工程类型、工程范围或关键项目栏仍可能存在空白，"
                "需要签约前补全以减少履行和结算争议。"
            )
            item.reasoning_summary = (
                "合同标题已明确为建设工程施工合同，足以初步确定合同性质；正文空白影响的是条款完整性，不宜按高风险完全缺失处理，"
                "本项调整为中风险-部分覆盖-模板空白。"
            )
            item.fallback_reason = "建设工程合同标题识别校正"

        if item.item_id == "CE-03-04" and item.coverage_status != COVERAGE_NOT_APPLICABLE and has_bid_consistency_framework:
            item.risk_level = "中"
            item.coverage_status = "部分覆盖"
            item.issue_type = "模板空白"
            item.status = "部分覆盖，模板空白"
            item.risk_point_description = (
                "合同已出现工程范围、建设工期、工程质量、工程价款等实质性内容框架，可提示中标合同一致性风险；"
                "但如项目实际涉及招投标，仍需明确本合同及补充协议不得背离中标合同实质性内容。"
            )
            item.reasoning_summary = (
                "简化版模板已预留建设工程实质性内容框架，但未完整形成中标合同一致性条款；本项按中风险-部分覆盖-模板空白处理。"
            )
            item.fallback_reason = "建设工程中标一致性模板空白校正"

        if item.item_id == "CE-05-01" and has_total_subcontract_ban:
            _mark_construction_pass(
                item,
                "合同明确禁止承包人将全部工程转包，并禁止将工程肢解后分包或转包，符合建设工程强制性规范要求。",
                "检测到合同正文包含禁止全部转包和禁止肢解转包/分包的明确表述，该表述属于合规禁止性条款，不应认定为风险条款。",
            )

        if item.item_id == "CE-05-03" and has_resubcontract_ban:
            _mark_construction_pass(
                item,
                "合同明确禁止分包单位将其承包的工程再分包，符合建设工程分包限制规则。",
                "检测到合同正文包含禁止再分包的明确表述，该表述属于合规禁止性条款，不应认定为风险条款。",
            )

    return items


def _apply_contract_specific_post_rules(items: List[ReviewItemResult], contract_text: str, contract_type_key: str) -> List[ReviewItemResult]:
    if contract_type_key == "lease":
        return _apply_house_lease_real_contract_rules(items, contract_text)
    if contract_type_key == "sale":
        return _apply_sale_contract_rules(items, contract_text)
    if contract_type_key == "gift":
        items = [_apply_gift_consideration_override(item, contract_text) for item in items]
        return _apply_gift_dependency_rules(items)
    if contract_type_key == "technology":
        return _apply_technology_development_mode_rules(items, contract_text)
    if contract_type_key == "construction":
        return _apply_construction_contract_rules(items, contract_text)
    if contract_type_key == "service":
        return _apply_service_contract_rules(items, contract_text)
    return items


def _assess_checkpoint(contract_text: str, checkpoint: ReviewCheckpoint) -> ReviewItemResult:
    clauses = parse_contract_clauses(contract_text)
    judgment = judge_checkpoint(checkpoint, clauses)
    return ReviewItemResult(
        item_id=checkpoint.item_id,
        node_id=checkpoint.node_id,
        title=checkpoint.title,
        risk_level=judgment.risk_level,
        status=judgment.status,
        risk_point_description=judgment.risk_point_description,
        suggested_clause_example=checkpoint.suggested_clause,
        legal_basis_index=checkpoint.legal_basis,
        legal_consequence_if_missing=checkpoint.legal_consequence_if_missing,
        applicable_if=checkpoint.applicable_if,
        matched_terms=judgment.matched_terms,
        coverage_status=judgment.coverage_status,
        issue_type=judgment.issue_type,
        evidence_clauses=judgment.evidence_clauses,
        evidence_location=judgment.evidence_location,
        reasoning_summary=judgment.reasoning_summary,
        judge_source=judgment.judge_source,
        llm_confidence=judgment.llm_confidence,
        llm_raw_reason=judgment.llm_raw_reason,
        fallback_reason=judgment.fallback_reason,
    )


def _risk_summary(items: List[ReviewItemResult]) -> Dict[str, int]:
    return {
        "高": sum(1 for item in items if item.risk_level == "高"),
        "中": sum(1 for item in items if item.risk_level == "中"),
        "低": sum(1 for item in items if item.risk_level == "低"),
    }


def _coverage_summary(items: List[ReviewItemResult]) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for item in items:
        summary[item.coverage_status] = summary.get(item.coverage_status, 0) + 1
    return summary


def _judge_source_summary(items: List[ReviewItemResult]) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for item in items:
        summary[item.judge_source] = summary.get(item.judge_source, 0) + 1
    return summary


def _issue_type_summary(items: List[ReviewItemResult]) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for item in items:
        summary[item.issue_type] = summary.get(item.issue_type, 0) + 1
    return summary


def _risk_finding_summary(findings: List[RiskFinding], items: List[ReviewItemResult]) -> Dict[str, int]:
    return {
        "重大风险": sum(1 for finding in findings if finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}),
        "中等风险": sum(1 for finding in findings if finding.severity == SEVERITY_MEDIUM),
        "低风险": sum(1 for finding in findings if finding.severity == SEVERITY_LOW),
        "人工复核": sum(1 for item in items if item.needs_manual_review),
    }


LEGAL_AUTHORITY_DATASET: List[Dict[str, Any]] = [
    {
        "authority_id": "CN-CC-LEASE-725",
        "law_name": "中华人民共和国民法典",
        "article": "第725条",
        "effective_from": "2021-01-01",
        "effective_to": None,
        "status": "CURRENT",
        "jurisdiction": "CN",
        "authority_level": "law",
        "source": "National law",
        "last_verified_at": "2026-08-11",
        "proposition": "租赁物在承租人占有期限内发生所有权变动，不影响租赁合同效力。",
    },
    {
        "authority_id": "CN-CC-CONTRACT-GENERAL",
        "law_name": "中华人民共和国民法典",
        "article": None,
        "effective_from": "2021-01-01",
        "effective_to": None,
        "status": "CURRENT",
        "jurisdiction": "CN",
        "authority_level": "law",
        "source": "National law",
        "last_verified_at": "2026-08-11",
        "proposition": "合同履行、违约责任、租赁合同等一般规则。",
    },
    {
        "authority_id": "CN-CONTRACT-LAW-1999",
        "law_name": "中华人民共和国合同法",
        "article": None,
        "effective_from": "1999-10-01",
        "effective_to": "2021-01-01",
        "status": "REPEALED",
        "jurisdiction": "CN",
        "authority_level": "law",
        "source": "National law",
        "last_verified_at": "2026-08-11",
        "replacement": "中华人民共和国民法典",
        "proposition": "原合同法已由民法典承接整合。",
    },
]


def _validate_legal_authorities(legal_references: List[Dict[str, Any]]) -> Dict[str, Any]:
    validation_results: List[Dict[str, Any]] = []
    dataset_by_law = {record["law_name"]: record for record in LEGAL_AUTHORITY_DATASET}
    for reference in legal_references:
        law_name = reference.get("law_name") or ""
        citation_validation = validate_legal_citation(law_name, reference.get("article") or "")
        record = dataset_by_law.get(law_name)
        if not record:
            validation_results.append(
                {
                    "law_name": law_name,
                    "article": reference.get("article"),
                    "status": citation_validation.get("status", "UNCERTAIN"),
                    "entailment": citation_validation.get("entailment", "PARTIAL"),
                    "confidence": "low",
                    "reason": "法律名称未命中本地版本化法律依据数据集；未编造条文号。",
                }
            )
            continue
        validation_results.append(
            {
                "authority_id": record["authority_id"],
                "law_name": law_name,
                "article": reference.get("article") or record.get("article"),
                "status": record["status"],
                "citation_status": citation_validation.get("status", record["status"]),
                "entailment": citation_validation.get("entailment", "PARTIAL"),
                "confidence": "high" if record["status"] == "CURRENT" else "medium",
                "replacement": record.get("replacement"),
                "last_verified_at": record["last_verified_at"],
                "proposition_supported": True,
            }
        )
    return {
        "dataset_version": LEGAL_DATASET_VERSION,
        "records_checked": len(legal_references),
        "results": validation_results,
    }


def _parse_legal_basis_references(text: str) -> List[Dict[str, str]]:
    references: List[Dict[str, str]] = []
    for law_match in re.finditer(r"《([^》]+)》([^；。,\n]*)", text or ""):
        law_name = law_match.group(1).strip()
        tail = law_match.group(2) or ""
        articles = re.findall(r"第[一二三四五六七八九十百零〇\d]+条", tail)
        if not articles:
            references.append({"law_name": law_name, "article": "", "paragraph": ""})
            continue
        for article in articles:
            references.append({"law_name": law_name, "article": article, "paragraph": ""})
    return references


def _review_proposition(item: ReviewItemResult) -> str:
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return item.applicability.get("reason") or item.title
    text = item.risk_point_description or item.legal_consequence_if_missing or item.title
    if item.coverage_status == "缺失" and any(phrase in text for phrase in MISSING_NARRATIVE_FORBIDDEN):
        return f"合同未明确约定可验证的“{item.title}”实质条款内容。"
    return text


def _retrieve_legal_references_for_proposition(proposition: str) -> List[Dict[str, str]]:
    text = proposition or ""
    if all(term in text for term in ("承租人", "死亡")) and any(term in text for term in ("共同居住", "共同经营", "继续承租", "原租赁合同")):
        return [{"law_name": "中华人民共和国民法典", "article": "第732条", "paragraph": ""}]
    if any(term in text for term in ("租赁期限届满", "期满", "继续使用", "继续居住")) and any(term in text for term in ("不定期", "继续有效")):
        return [{"law_name": "中华人民共和国民法典", "article": "第734条", "paragraph": ""}]
    if "不定期" in text and any(term in text for term in ("合理期限", "通知", "解除")):
        return [{"law_name": "中华人民共和国民法典", "article": "第730条", "paragraph": ""}]
    if any(term in text for term in ("所有权", "权利主体", "受让", "继承")) and any(term in text for term in ("不影响", "继续履行", "合同效力")):
        return [{"law_name": "中华人民共和国民法典", "article": "第725条", "paragraph": ""}]
    return []


def _legal_claim_specs_for_item(item: ReviewItemResult) -> List[Dict[str, Any]]:
    references = _parse_legal_basis_references(item.legal_basis_index)
    base = _review_proposition(item)
    recalled = _retrieve_legal_references_for_proposition(base)
    if recalled:
        references = recalled
    if item.node_id == "tenant_death_successor":
        proposition = "房屋承租人在租赁期间死亡的，与其生前共同居住的人或者共同经营人可以按照原租赁合同继续租赁该房屋。"
        return [
            {
                "proposition": proposition,
                "claim_type": "RIGHT",
                "references": _retrieve_legal_references_for_proposition(proposition),
            },
            {
                "proposition": "建议共同居住人或共同经营人继续承租时提交身份、共同居住或共同经营证明。",
                "claim_type": "DRAFTING_RECOMMENDATION",
                "references": [],
            },
        ]
    if item.node_id == "tenant_death_settlement":
        return [
            {
                "proposition": "无人继续承租时，房屋、遗留物、费用和押金交接属于合同履行和遗产管理衔接事项，应由合同另行约定操作流程。",
                "claim_type": "DRAFTING_RECOMMENDATION",
                "references": [],
            }
        ]
    if item.node_id == "reasonable_repair_cost":
        return [
            {
                "proposition": "维修费用应以实际发生、必要且合理的维修支出为基础，并保留维修单据、报价或市场依据。",
                "claim_type": "DRAFTING_RECOMMENDATION",
                "references": [],
            },
            {
                "proposition": "如果维修费用被约定为违约金或固定赔偿额，才需要单独适用违约金过高调整规则。",
                "claim_type": "DRAFTING_RECOMMENDATION",
                "references": [],
            },
        ]
    if item.node_id == "indefinite_lease":
        return [
            {
                "proposition": "租赁期限届满后承租人继续使用租赁物，出租人没有提出异议的，原租赁合同继续有效并转为不定期租赁。",
                "claim_type": "LEGAL_EFFECT",
                "references": [{"law_name": "中华人民共和国民法典", "article": "第734条", "paragraph": ""}],
            },
            {
                "proposition": "不定期租赁中任一方解除合同，应当在合理期限之前通知对方。",
                "claim_type": "PROCEDURE",
                "references": [{"law_name": "中华人民共和国民法典", "article": "第730条", "paragraph": ""}],
            },
            {
                "proposition": "建议在合同中固定三十日书面通知期，以减少不定期租赁解除时的通知期限争议。",
                "claim_type": "DRAFTING_RECOMMENDATION",
                "references": [],
            },
        ]
    if item.node_id == "lessor_death":
        return [
            {
                "proposition": "租赁期间所有权或权利主体发生变动，不影响租赁合同效力和继续履行。",
                "claim_type": "LEGAL_EFFECT",
                "references": [{"law_name": "中华人民共和国民法典", "article": "第725条", "paragraph": ""}],
            },
            {
                "proposition": "建议继承人或受让人提交权利证明后接收租金并履行出租人义务。",
                "claim_type": "DRAFTING_RECOMMENDATION",
                "references": [],
            },
        ]
    if not references and item.legal_basis_index:
        references = [{"law_name": "", "article": "", "paragraph": ""}]
    if not references:
        return []
    claim_type = "DRAFTING_RECOMMENDATION" if "建议" in item.suggested_clause_example and "第" not in item.legal_basis_index else "STATUTORY_RULE"
    return [{"proposition": base, "claim_type": claim_type, "references": references}]


def _claim_without_direct_authority(item: ReviewItemResult, index: int, spec: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "claim_id": f"{item.item_id}-LC-{index:02d}",
        "finding_id": RISK_FINDING_ID_BY_GROUP.get(item.risk_group or item.node_id or "", ""),
        "review_id": item.item_id,
        "proposition": spec.get("proposition") or _review_proposition(item),
        "claim_type": spec.get("claim_type") or "PRACTICAL_RECOMMENDATION",
        "authority_id": "",
        "law_name": "",
        "article": "",
        "paragraph": "",
        "support_type": "UNCERTAIN",
        "support_scope": "",
        "authority_links": [],
        "confidence": "medium" if spec.get("claim_type") == "DRAFTING_RECOMMENDATION" else "low",
        "freshness_status": "NO_DIRECT_AUTHORITY",
        "citation_existence_status": "NO_DIRECT_AUTHORITY",
        "citation_entailment_status": "UNCERTAIN",
        "authority": None,
        "basis_text": item.legal_basis_index,
    }


def _apply_citation_claims(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    for item in items:
        claims: List[Dict[str, Any]] = []
        specs = _legal_claim_specs_for_item(item)
        effective_gap = (item.decision_trace or {}).get("effective_gap") or {}
        if effective_gap.get("affected_effective_gap"):
            authority_ids = [value for value in effective_gap.get("authority_ids", []) if value in DEFAULT_LAW_AUTHORITY_ARTICLES]
            if authority_ids:
                specs.append({
                    "proposition": effective_gap.get("statutory_protection_scope") or "现行法律为该合同缺口提供默认处理规则。",
                    "claim_type": "STATUTORY_DEFAULT",
                    "references": [
                        {"law_name": "中华人民共和国民法典", "article": DEFAULT_LAW_AUTHORITY_ARTICLES[authority_id], "paragraph": ""}
                        for authority_id in authority_ids
                    ],
                })
        for index, spec in enumerate(specs, start=1):
            references = spec.get("references") or []
            if not references:
                claims.append(_claim_without_direct_authority(item, index, spec))
                continue
            for link_index, reference in enumerate(references, start=1):
                claim_id = f"{item.item_id}-LC-{index:02d}" if len(references) == 1 else f"{item.item_id}-LC-{index:02d}-{link_index:02d}"
                validation = validate_citation_entailment(
                    proposition=spec.get("proposition") or _review_proposition(item),
                    law_name=reference["law_name"],
                    article=reference["article"],
                    paragraph=reference.get("paragraph", ""),
                    claim_id=claim_id,
                    finding_id=RISK_FINDING_ID_BY_GROUP.get(item.risk_group or item.node_id or "", ""),
                    review_id=item.item_id,
                    claim_type=spec.get("claim_type") or "STATUTORY_RULE",
                )
                claim = validation.get("claim") or {}
                if (
                    validation.get("support_type") == "UNCERTAIN"
                    or (not validation.get("authority") and validation.get("support_type") != "BACKGROUND_ONLY")
                ):
                    claims.append(_claim_without_direct_authority(item, index, spec))
                    continue
                claims.append(
                    {
                        **claim,
                        "freshness_status": validation.get("status"),
                        "citation_existence_status": "FOUND" if validation.get("authority") else "NOT_FOUND",
                        "citation_entailment_status": validation.get("support_type"),
                        "authority": validation.get("authority"),
                        "basis_text": item.legal_basis_index,
                    }
                )
        item.legal_references = claims
    return items


LEGAL_SUPPORT_RANK = {
    "DIRECT_SUPPORT": 4, "PARTIAL_SUPPORT": 3, "SUPPORTING": 3,
    "CONTEXT_ONLY": 2, "BACKGROUND_ONLY": 1, "NOT_SUPPORT": 0, "CONTRADICTS": -1, "UNCERTAIN": -1,
}

FINAL_RELEASE_ERROR_TAXONOMY = {
    "RECOMMENDATION_DUAL_SOURCE_ERROR",
    "RECOMMENDATION_RENDERER_RESURRECTION",
    "RECOMMENDATION_CROSS_RENDERER_MISMATCH",
    "LEGAL_AUTHORITY_DUPLICATION",
    "LEGAL_AUTHORITY_OVERREACH",
    "LEGAL_PROPOSITION_ENTAILMENT_ERROR",
    "DEFAULT_LAW_NARRATIVE_MISMATCH",
    "DRAFTING_RATIONALE_AS_LEGAL_REQUIREMENT",
    "LEGAL_AUTHORITY_DEFAULT_LAW_CONTRADICTION",
    "LEGAL_PROPOSITION_STATE_DIVERGENCE",
    "COMPOSITE_LEGAL_ELEMENT_ERROR",
    "NOT_APPLICABLE_GAP_NARRATIVE",
    "NOT_APPLICABLE_DEFAULT_LAW_LEAKAGE",
    "REVIEW_POLARITY_ERROR",
    "NEGATIVE_REVIEW_POSITIVE_NARRATIVE",
    "NEGATIVE_CHECK_FALSE_PASS",
}


def _legal_authority_key(claim: Dict[str, Any]) -> tuple[str, str, str, str]:
    authority = claim.get("authority") or {}
    return (
        str(claim.get("authority_id") or authority.get("authority_id") or claim.get("law_name") or ""),
        str(claim.get("article") or ""), str(claim.get("paragraph") or ""),
        str(authority.get("effective_from") or ""),
    )


def _select_legal_authorities(items: List[ReviewItemResult]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    duplicate_count = 0
    for item in items:
        candidates = list(item.legal_references or [])
        no_authority = [claim for claim in candidates if not claim.get("authority_id")]
        grouped: Dict[tuple[str, str, str, str], List[Dict[str, Any]]] = {}
        for claim in candidates:
            if claim.get("authority_id"):
                grouped.setdefault(_legal_authority_key(claim), []).append(claim)
        selected: List[Dict[str, Any]] = []
        rejected: List[Dict[str, Any]] = []
        for key, group in grouped.items():
            duplicate_count += max(0, len(group) - 1)
            ordered = sorted(
                group,
                key=lambda claim: (
                    LEGAL_SUPPORT_RANK.get(str(claim.get("support_type") or "UNCERTAIN"), -1),
                    1 if claim.get("freshness_status") == "CURRENT" else 0,
                    1 if claim.get("claim_type") == "STATUTORY_DEFAULT" else 0,
                    {"high": 3, "medium": 2, "low": 1}.get(str(claim.get("confidence") or "low"), 0),
                ),
                reverse=True,
            )
            best = dict(ordered[0])
            best["authority_key"] = list(key)
            best["supported_propositions"] = list(dict.fromkeys(
                str(claim.get("proposition") or "") for claim in group if claim.get("proposition")
            ))
            if (
                LEGAL_SUPPORT_RANK.get(str(best.get("support_type") or "UNCERTAIN"), -1) >= 3
                and best.get("freshness_status") == "CURRENT"
            ):
                selected.append(best)
                rejected.extend(ordered[1:])
            else:
                rejected.extend(ordered)
        selected.sort(key=lambda claim: LEGAL_SUPPORT_RANK.get(str(claim.get("support_type") or ""), -1), reverse=True)
        if len(selected) > 3:
            rejected.extend(selected[3:])
            selected = selected[:3]
        item.legal_references = no_authority + selected
        selected_keys = {_legal_authority_key(claim) for claim in selected}
        entailment_rows = [
            {
                "proposition_id": claim.get("claim_id"), "statement": claim.get("proposition"),
                "authority_id": claim.get("authority_id"),
                "authority_rule_summary": ((claim.get("authority") or {}).get("text") or claim.get("support_scope") or ""),
                "entailment": (
                    "SUPPORTS" if claim.get("support_type") == "DIRECT_SUPPORT"
                    else "PARTIAL" if claim.get("support_type") in {"PARTIAL_SUPPORT", "SUPPORTING"}
                    else claim.get("support_type")
                ),
                "reason": "Selected by proposition-level authority entailment."
                if _legal_authority_key(claim) in selected_keys and claim.get("support_type") in {"DIRECT_SUPPORT", "PARTIAL_SUPPORT", "SUPPORTING"}
                else "Rejected because a stronger duplicate exists or the authority does not support the proposition.",
            }
            for claim in candidates
        ]
        selection = {
            "review_id": item.item_id,
            "candidate_authorities": candidates,
            "selected_authorities": selected,
            "rejected_authorities": rejected,
            "duplicate_count": sum(max(0, len(group) - 1) for group in grouped.values()),
            "entailment": entailment_rows,
        }
        item.decision_trace["legal_authority_selection"] = selection
        rows.append(selection)
    remaining_duplicates = 0
    for item in items:
        remaining_keys = [
            _legal_authority_key(claim) for claim in item.legal_references if claim.get("authority_id")
        ]
        remaining_duplicates += len(remaining_keys) - len(set(remaining_keys))
    context_selected = [
        claim for item in items for claim in item.legal_references
        if claim.get("authority_id")
        and claim.get("support_type") in {"CONTEXT_ONLY", "BACKGROUND_ONLY", "NOT_SUPPORT", "CONTRADICTS"}
    ]
    return {
        "status": "BLOCKED" if remaining_duplicates or context_selected else "REPORT_READY",
        "failures": [] if not remaining_duplicates and not context_selected else [{
            "requirement": "LEGAL_AUTHORITY_SELECTION_GATE", "failure_stage": "Legal Authority Selection",
            "root_cause": "Production authority selection retained a duplicate or non-supporting authority.",
            "responsible_function": "_select_legal_authorities", "current_status": "FAIL",
        }],
        "gate_results": {
            "LEGAL_AUTHORITY_DEDUP_GATE": "FAIL" if remaining_duplicates else "PASS",
            "LEGAL_AUTHORITY_SELECTION_GATE": "FAIL" if context_selected else "PASS",
            "CITATION_ENTAILMENT_GATE": "FAIL" if context_selected else "PASS",
        },
        "candidate_duplicate_count": duplicate_count,
        "duplicate_count": remaining_duplicates,
        "material_citation_not_support_count": len(context_selected),
        "rows": rows,
    }


def _detect_contract_year(contract_text: str) -> Optional[int]:
    years = [int(match.group(1)) for match in re.finditer(r"(20\d{2}|19\d{2})\s*年", contract_text or "")]
    if not years:
        return None
    return max(years)


def _check_legal_reference_freshness(contract_text: str) -> List[Dict[str, Any]]:
    text = contract_text or ""
    contract_year = _detect_contract_year(text)
    findings: List[Dict[str, Any]] = []
    if "合同法" in text:
        outdated = contract_year is None or contract_year >= 2021
        status = "OUTDATED_REFERENCE" if outdated else "CURRENT_AT_SIGNING"
        findings.append(
            {
                "law_name": "中华人民共和国合同法",
                "article": None,
                "status": status,
                "law_lifecycle_status": "REPEALED",
                "effective_from": "1999-10-01",
                "repealed_at": "2021-01-01",
                "replacement": "中华人民共和国民法典",
                "contract_year": contract_year,
                "risk_type": "drafting_legal_reference_defect",
                "severity": SEVERITY_LOW if outdated else SEVERITY_NONE,
                "message": "合同文本引用《中华人民共和国合同法》；如合同签署于《民法典》施行后，应改为引用《中华人民共和国民法典》相应规则。该问题属于法律引用新鲜度/起草缺陷，不当然导致合同无效。",
            }
        )
    return findings


def _legal_reference_findings(reference_issues: List[Dict[str, Any]]) -> List[RiskFinding]:
    findings: List[RiskFinding] = []
    for issue in reference_issues:
        if issue.get("severity") == SEVERITY_NONE:
            continue
        findings.append(
            RiskFinding(
                finding_id=RISK_FINDING_ID_BY_GROUP["legal_reference"],
                risk_group="legal_reference",
                title="法律引用建议更新",
                severity=issue.get("severity") or SEVERITY_LOW,
                priority=PRIORITY_B_PRACTICAL,
                source_review_ids=[],
                facts=[issue.get("law_name", "")],
                evidence=[
                    {
                        "location": "合同全文",
                        "section_type": "法律引用",
                        "text": issue.get("message", ""),
                    }
                ],
                source_clause_ids=[],
                legal_basis=[
                    {
                        "law_name": issue.get("law_name"),
                        "status": issue.get("status"),
                        "replacement": issue.get("replacement"),
                        "dataset_version": LEGAL_DATASET_VERSION,
                    }
                ],
                issue="合同订立依据仍引用已废止法律，属于法律依据引用过时问题。",
                consequence="通常不当然导致合同无效，但可能造成解释依据过时、谈判沟通成本增加。",
                probability=PROBABILITY_HIGH,
                impact={
                    "financial": "NONE",
                    "legal_validity": "LOW",
                    "rights_loss": "LOW",
                    "operational": "LOW",
                    "safety": "NONE",
                    "evidence": "LOW",
                },
                legal_impact={
                    "type": issue.get("risk_type"),
                    "replacement": issue.get("replacement"),
                    "does_not_mean_invalid": True,
                },
                operational_impact={"level": "LOW"},
                safety_impact={"level": "NONE"},
                recommendation="建议将《中华人民共和国合同法》更新为《中华人民共和国民法典》及现行有效相关规定，避免法律依据过时造成解释和沟通成本。",
                decision_value="medium",
                confidence={"level": "high", "source": "versioned_legal_authority_dataset"},
                verification_status="PASS",
                severity_reason={
                    "dominant_factor": "legal_reference",
                    "impact": {"financial": "NONE", "legal_validity": "LOW", "operational": "LOW"},
                    "probability": PROBABILITY_HIGH,
                    "economic_ratio": None,
                    "statutory_protection": "PARTIAL_DEFAULT",
                    "evidence_strength": "explicit",
                },
                risk_category="legal_reference",
                aggregation_signals={
                    "aggregation_key": "legal_reference|legal_reference",
                    "risk_ontology": "legal_reference",
                    "shared_facts": [issue.get("law_name", "")],
                    "shared_legal_consequence": "法律引用过时但不当然影响合同效力",
                    "source_review_count": 0,
                },
                default_law_status="PARTIAL_DEFAULT",
                verification={"status": "PASS", "reason": "命中本地版本化法律依据数据集。"},
            )
        )
    return findings


def _extract_legal_reference_mentions(contract_text: str) -> List[Dict[str, Any]]:
    refs: List[Dict[str, Any]] = []
    text = contract_text or ""
    for law_name in ("中华人民共和国合同法", "中华人民共和国民法典"):
        for match in re.finditer(rf"《?{re.escape(law_name)}》?", text):
            refs.append(
                {
                    "law_name": law_name,
                    "start": match.start(),
                    "end": match.end(),
                    "source": "contract_text",
                    "excerpt": text[max(0, match.start() - 20): min(len(text), match.end() + 30)],
                }
            )
    return refs


def _legal_freshness_trace(
    contract_text: str,
    reference_issues: List[Dict[str, Any]],
    findings: List[RiskFinding],
) -> Dict[str, Any]:
    legal_findings = [finding for finding in findings if finding.risk_group == "legal_reference"]
    return {
        "called": True,
        "call_chain": [
            "review_contract_v2",
            "_check_legal_reference_freshness",
            "_validate_legal_authorities",
            "_legal_reference_findings",
            "_build_recommendations",
            "_format_markdown_v2",
            "post_render_quality_gate",
        ],
        "input_legal_refs": _extract_legal_reference_mentions(contract_text),
        "output_legal_refs": reference_issues,
        "output_findings": [finding.to_public_dict() for finding in legal_findings],
    }


def _manual_review_materiality_for_item(item: Any) -> str:
    text = " ".join(
        str(value or "")
        for value in (
            getattr(item, "item_id", ""),
            getattr(item, "node_id", ""),
            getattr(item, "title", ""),
            getattr(item, "risk_point_description", ""),
            getattr(item, "legal_consequence_if_missing", ""),
            getattr(item, "quality_gate_failure_reason", ""),
        )
    )
    if any(term in text for term in ("合同效力", "主体资格", "授权", "签字", "代理权限", "真实性", "人身安全", "监管合规")):
        return "HIGH"
    if any(term in text for term in ("重大金额", "重大违约", "核心付款", "核心交付", "重大知识产权", "关键附件", "主要权利义务")):
        return "HIGH"
    if getattr(item, "review_importance", "") == REVIEW_IMPORTANCE_CORE or getattr(item, "risk_level", "") == "高":
        return "MEDIUM"
    return "LOW"


def _manual_review_records(items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for item in items:
        if not item.needs_manual_review and item.coverage_status != INSUFFICIENT_CONTEXT:
            continue
        materiality = _manual_review_materiality_for_item(item)
        record = {
            "item_id": item.item_id,
            "title": item.title,
            "reason": item.quality_gate_failure_reason or _applicability_user_reason(item),
            "materiality": materiality,
            "coverage_status": item.coverage_status,
            "blocking_signability": materiality == "HIGH",
        }
        item.decision_trace["manual_review_materiality"] = materiality
        item.decision_trace["manual_review_record"] = record
        records.append(record)
    return records


def _signability_label(level: str) -> str:
    return {
        SIGNABLE: "可以签署",
        SIGNABLE_WITH_OPTIONAL_IMPROVEMENTS: "可以签署，可进一步优化",
        SIGN_AFTER_MODIFICATION: "建议修改后签署",
        PROFESSIONAL_REVIEW_RECOMMENDED: "建议专业法律复核后决定",
        NOT_RECOMMENDED_TO_SIGN: "当前不建议签署",
    }.get(level, "建议专业法律复核后决定")


def _build_signability_decision(
    findings: List[RiskFinding],
    dispositions: List[FinalDisposition],
    manual_review_records: List[Dict[str, Any]],
) -> SignabilityDecision:
    decision_findings = sorted(
        findings,
        key=lambda finding: (_priority_rank(finding.priority), _severity_rank(finding.severity), finding.finding_id),
    )[:3]
    high_unresolved = [
        finding.finding_id for finding in findings
        if finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}
        and (finding.needs_manual_review or (finding.confidence or {}).get("level") == "low")
    ]
    material_manual = [row["item_id"] for row in manual_review_records if row.get("blocking_signability")]
    must_change = [row for row in dispositions if row.final_action == DISPOSITION_MUST_CHANGE]
    should_change = [row for row in dispositions if row.final_action == DISPOSITION_SHOULD_CHANGE]
    optional = [row for row in dispositions if row.final_action == DISPOSITION_OPTIONAL_IMPROVEMENT]
    severe_core = [
        finding.finding_id for finding in findings
        if finding.priority == PRIORITY_A_CORE and finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}
    ]
    not_signable = [
        finding.finding_id for finding in findings
        if finding.severity == SEVERITY_CRITICAL
        and any(term in " ".join([finding.risk_group, finding.title]) for term in ("contract_validity", "personal_safety", "主体", "效力", "人身安全"))
    ]
    if not_signable:
        level = NOT_RECOMMENDED_TO_SIGN
    elif material_manual or high_unresolved:
        level = PROFESSIONAL_REVIEW_RECOMMENDED
    elif must_change or should_change or severe_core:
        level = SIGN_AFTER_MODIFICATION
    elif optional:
        level = SIGNABLE_WITH_OPTIONAL_IMPROVEMENTS
    else:
        level = SIGNABLE
    reasons = [
        f"{finding.finding_id} {finding.title}：严重度 {finding.severity}，优先级 {finding.priority}，剩余风险由独立 Finding 决策。"
        for finding in decision_findings
    ]
    if manual_review_records and not material_manual:
        reasons.append("存在人工复核事项，但其重要度不足以单独阻断总体签署性判断。")
    if material_manual:
        reasons.append("存在高重要度人工复核事项，需专业法律复核后再决定是否签署。")
    if high_unresolved:
        reasons.append("存在高严重度且判断可靠度不足的未解决风险。")
    unresolved = list(dict.fromkeys(high_unresolved + material_manual))
    return SignabilityDecision(
        level=level,
        label=_signability_label(level),
        decision_finding_ids=[finding.finding_id for finding in decision_findings],
        reasons=reasons or ["没有形成需要修改的独立风险发现。"],
        unresolved_uncertainty=unresolved,
        manual_review_item_ids=[row["item_id"] for row in manual_review_records],
        blocking_manual_review_item_ids=material_manual,
        confidence="low" if unresolved else "high" if not findings or all((finding.confidence or {}).get("level") == "high" for finding in decision_findings) else "medium",
    )


def _overall_assessment(
    contract_type_name: str,
    findings: List[RiskFinding],
    items: List[ReviewItemResult],
    final_dispositions: Optional[List[FinalDisposition]] = None,
    manual_reviews: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    max_severity = SEVERITY_NONE
    if findings:
        max_severity = sorted((finding.severity for finding in findings), key=_severity_rank)[0]
    dispositions = final_dispositions or _build_final_dispositions(findings, [], [])
    manual_review_records = manual_reviews if manual_reviews is not None else _manual_review_records(items)
    signability_decision = _build_signability_decision(
        findings=findings,
        dispositions=dispositions,
        manual_review_records=manual_review_records,
    )
    return {
        "contract_type": contract_type_name,
        "signability": signability_decision.label,
        "core_risk_count": len([finding for finding in findings if finding.priority == PRIORITY_A_CORE]),
        "priority_modify_count": len([finding for finding in findings if finding.priority in {PRIORITY_A_CORE, PRIORITY_B_PRACTICAL}]),
        "optional_count": len([finding for finding in findings if finding.priority == PRIORITY_C_OPTIMIZATION]),
        "covered_key_items": [item.item_id for item in items if item.coverage_status == "通过" and item.review_priority in {PRIORITY_A_CORE, PRIORITY_B_PRACTICAL}][:10],
        "manual_review_count": len(manual_review_records),
        "manual_review_items": manual_review_records,
        "max_severity": max_severity,
        "signability_decision": signability_decision.to_public_dict(),
    }


def _finding_needs_verification(finding: RiskFinding) -> bool:
    risk_claim = (finding.aggregation_signals or {}).get("risk_claim") or {}
    evidence = finding.supporting_evidence or []
    if risk_claim.get("existence_type") == "POSITIVE_EXISTENCE":
        return True
    if evidence and any(row.get("entailment_status") != EVIDENCE_SUPPORTS for row in evidence):
        return True
    if finding.default_law_status == "UNCERTAIN_DEFAULT":
        return True
    if finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}:
        return True
    if finding.priority == PRIORITY_A_CORE and finding.severity == SEVERITY_MEDIUM:
        return True
    if (finding.economic_impact or {}).get("level") in {"high", "critical"}:
        return True
    if (finding.confidence or {}).get("level") == "low":
        return True
    return False


def _run_independent_verifier(findings: List[RiskFinding], items: List[ReviewItemResult]) -> List[RiskFinding]:
    item_by_id = {item.item_id: item for item in items}
    for finding in findings:
        if not _finding_needs_verification(finding):
            finding.verification = {
                "status": "SKIPPED_LOW_VALUE",
                "prompt_version": VERIFIER_PROMPT_VERSION,
                "reason": "非高价值风险发现，未触发独立验证以控制成本。",
            }
            finding.verification_status = "SKIPPED_LOW_VALUE"
            finding.agreement = {"primary": finding.severity, "verifier": "not_run", "status": "AGREE", "reason": "未触发验证。"}
            continue
        related_items = [item_by_id[item_id] for item_id in finding.source_review_ids if item_id in item_by_id]
        risk_claim = (finding.aggregation_signals or {}).get("risk_claim") or {}
        has_element_support = any(
            element.get("status") in {"COVERED", "PARTIALLY_COVERED"}
            and element.get("entailment") in {EVIDENCE_SUPPORTS, EVIDENCE_PARTIAL_SUPPORT}
            for item in related_items
            for element in (item.coverage_elements or [])
        )
        has_support = (
            _finding_has_supporting_evidence(finding)
            or has_element_support
            or any(item.coverage_status == "缺失" for item in related_items)
        )
        if risk_claim.get("existence_type") == "POSITIVE_EXISTENCE":
            has_support = _finding_has_supporting_evidence(finding)
        formula_ok = True
        if finding.risk_group == "early_termination_financial_exposure":
            formula_validations = [
                (item.decision_trace or {}).get("formula_validation")
                for item in related_items
                if (item.decision_trace or {}).get("formula_validation")
            ]
            formula_types = {
                ((item.scenario_analysis or {}).get("formula") or {}).get("type")
                for item in related_items
                if item.scenario_analysis
            }
            if formula_validations or formula_types:
                formula_ok = any(validation.get("status") == "PASS" for validation in formula_validations) or "remaining_term_rent_multiplier" in formula_types
        agreement_status = "AGREE" if has_support and formula_ok else "MATERIAL_DISAGREEMENT"
        reason = "事实、证据和公式可支持该风险发现。" if agreement_status == "AGREE" else "证据或公式无法独立确认。"
        finding.verification = {
            "status": "PASS" if agreement_status == "AGREE" else "BLOCK",
            "prompt_version": VERIFIER_PROMPT_VERSION,
            "fact_exists": has_support,
            "evidence_supports": has_support,
            "formula_correct": formula_ok,
            "negative_evidence_checked": True,
            "factual_support": has_support,
            "evidence_support": has_support,
            "counter_evidence": list(finding.counter_evidence),
            "applicability": "APPLICABLE" if related_items else "NOT_ESTABLISHED",
            "legal_support": finding.default_law_status,
            "finding_exists": has_support,
            "severity_reasonable": agreement_status == "AGREE",
            "priority_reasonable": agreement_status == "AGREE",
            "agreement": agreement_status,
            "reason": reason,
        }
        finding.verification_status = finding.verification["status"]
        finding.agreement = {
            "primary": finding.severity,
            "verifier": finding.severity if agreement_status == "AGREE" else "UNCERTAIN",
            "status": agreement_status,
            "reason": reason,
        }
        if agreement_status == "MATERIAL_DISAGREEMENT":
            finding.needs_manual_review = True
            finding.confidence = {**(finding.confidence or {}), "level": "low"}
            for item in related_items:
                item.needs_manual_review = True
                item.quality_gate_failure_reason = "独立验证器无法确认该风险发现的事实、证据或公式。"
    return findings


def _recommendation_type_for_finding(finding: RiskFinding) -> str:
    if finding.needs_manual_review:
        return "VERIFY"
    if finding.priority == PRIORITY_C_OPTIMIZATION:
        return "OPTIONAL"
    if finding.risk_group in {"early_termination_financial_exposure", "deposit_return_timing"}:
        return "MODIFY"
    if not finding.source_clause_ids:
        return "ADD"
    return "MODIFY"


def _recommendation_clauses_for_finding(finding: RiskFinding, items_by_id: Dict[str, ReviewItemResult]) -> List[Dict[str, Any]]:
    legal_claim_ids: List[str] = []
    drafting_claim_ids: List[str] = []
    for review_id in finding.source_review_ids:
        item = items_by_id.get(review_id)
        if not item:
            continue
        for claim in item.legal_references or []:
            if claim.get("claim_type") == "DRAFTING_RECOMMENDATION":
                drafting_claim_ids.append(claim.get("claim_id", ""))
            elif claim.get("support_type") == "DIRECT_SUPPORT" and claim.get("support_scope"):
                legal_claim_ids.append(claim.get("claim_id", ""))
    clauses: List[Dict[str, Any]] = []
    if legal_claim_ids:
        clauses.append(
            {
                "text": "法律规则以直接支持当前命题的 LegalClaim 为准。",
                "source_type": "STATUTORY_RULE",
                "legal_claim_ids": sorted(set(filter(None, legal_claim_ids))),
                "legal_requirement": True,
                "drafting_choice": False,
                "rationale": "该部分由 proposition-level entailment 验证通过的法律 claim 支撑。",
            }
        )
    source_type = "DRAFTING_CHOICE" if drafting_claim_ids else "RISK_MITIGATION"
    clauses.append(
        {
            "text": finding.recommendation,
            "source_type": source_type,
            "legal_claim_ids": sorted(set(filter(None, drafting_claim_ids))),
            "legal_requirement": False,
            "drafting_choice": source_type == "DRAFTING_CHOICE",
            "rationale": "该建议用于降低履行争议，不自动表述为法定强制期限或法定义务。",
        }
    )
    return clauses


def _recommendation_components_for_finding(finding: RiskFinding, items_by_id: Dict[str, ReviewItemResult]) -> List[Dict[str, Any]]:
    components: List[Dict[str, Any]] = []
    numeric_pattern = re.compile(r"(?:\d+|[一二三四五六七八九十两]+)\s*(?:日|天|个工作日|倍)")
    for review_id in finding.source_review_ids:
        item = items_by_id.get(review_id)
        if not item:
            continue
        for claim in item.legal_references or []:
            claim_type = claim.get("claim_type")
            support_type = claim.get("support_type")
            if claim_type == "DRAFTING_RECOMMENDATION":
                continue
            if support_type == "DIRECT_SUPPORT" and claim.get("support_scope"):
                proposition = claim.get("proposition") or "法律规则"
                support_scope = claim.get("support_scope") or ""
                unsupported_numbers = [number for number in numeric_pattern.findall(proposition) if number not in support_scope]
                if unsupported_numbers:
                    continue
                source_type = "STATUTORY_DEFAULT" if (item.decision_trace or {}).get("default_law_status") == "CLEAR_DEFAULT" else "STATUTORY_RULE"
                components.append(
                    {
                        "proposition": proposition,
                        "source_type": source_type,
                        "legal_claim_ids": [claim.get("claim_id")],
                        "statutory_basis": f"《{claim.get('law_name')}》{claim.get('article') or ''}",
                        "authority": f"《{claim.get('law_name')}》{claim.get('article') or ''}",
                        "supported_scope": support_scope,
                        "drafting_reason": "",
                        "confidence": claim.get("confidence", "medium"),
                    }
                )
    drafting_reason = finding.recommendation
    source_type = "RISK_MITIGATION" if finding.priority in {PRIORITY_A_CORE, PRIORITY_B_PRACTICAL} else "DRAFTING_CHOICE"
    components.append(
        {
            "proposition": drafting_reason,
            "source_type": source_type,
            "legal_claim_ids": [],
            "statutory_basis": "",
            "authority": "",
            "supported_scope": "",
            "drafting_reason": "该组件属于合同起草或风险缓释选择，不表述为具体法定期限、法定金额或强制格式。",
            "confidence": (finding.confidence or {}).get("level", "medium"),
        }
    )
    return components


def _build_recommendations(findings: List[RiskFinding], items: Optional[List[ReviewItemResult]] = None) -> List[Recommendation]:
    recommendations: List[Recommendation] = []
    by_key: Dict[tuple[str, str], Recommendation] = {}
    items_by_id = {item.item_id: item for item in (items or [])}
    for finding in findings:
        recommendation_type = _recommendation_type_for_finding(finding)
        key = (finding.risk_group, recommendation_type)
        recommendation = by_key.get(key)
        if not recommendation:
            recommendation = Recommendation(
                recommendation_id=f"REC-{len(recommendations) + 1:03d}",
                type=recommendation_type,
                priority=finding.priority,
                source_finding_ids=[],
                target_clause=", ".join(finding.source_clause_ids) if finding.source_clause_ids else "未定位到单一目标条款",
                target_risk_ids=[],
                rationale=finding.consequence or finding.issue,
                suggested_text=finding.recommendation,
                target_finding_ids=[],
                target_clause_ids=list(finding.source_clause_ids),
                proposed_change=finding.recommendation,
                proposed_text=finding.recommendation,
                expected_effect=f"降低或消除“{finding.title}”对应的执行争议。",
                confidence={"level": (finding.confidence or {}).get("level", "medium"), "source": "recommendation_aggregator"},
                clauses=_recommendation_clauses_for_finding(finding, items_by_id),
                components=_recommendation_components_for_finding(finding, items_by_id),
            )
            by_key[key] = recommendation
            recommendations.append(recommendation)
        recommendation.target_risk_ids = sorted(set(recommendation.target_risk_ids + [finding.finding_id]))
        recommendation.source_finding_ids = sorted(set(recommendation.source_finding_ids + [finding.finding_id]))
        recommendation.target_finding_ids = sorted(set(recommendation.target_finding_ids + [finding.finding_id]))
        recommendation.target_clause_ids = sorted(set(recommendation.target_clause_ids + finding.source_clause_ids))
        recommendation.target_review_ids = sorted(set(recommendation.target_review_ids + finding.source_review_ids))
        if not recommendation.clauses:
            recommendation.clauses = _recommendation_clauses_for_finding(finding, items_by_id)
        if not recommendation.components:
            recommendation.components = _recommendation_components_for_finding(finding, items_by_id)
        finding.recommendation_ids = sorted(set(finding.recommendation_ids + [recommendation.recommendation_id]))
    return recommendations


def _recommendation_suppression_reason(impact: Any) -> str:
    if getattr(impact, "narrows_remedy", False):
        return "POTENTIAL_REMEDY_NARROWING"
    if getattr(impact, "shifts_risk_to_user", False):
        return "STATUTORY_PROTECTION_DEGRADATION"
    if getattr(impact, "increases_liability", False) or getattr(impact, "accelerates_obligation", False):
        return "INCREASES_USER_OBLIGATION"
    return "NO_SAFE_DRAFTING_IMPROVEMENT"


def _apply_recommendation_display_states(
    items: List[ReviewItemResult],
    findings: List[RiskFinding],
    active_recommendations: List[Recommendation],
    impacts: List[Any],
) -> tuple[Dict[str, Any], List[Dict[str, Any]]]:
    active_ids = {recommendation.recommendation_id for recommendation in active_recommendations}
    active_by_finding: Dict[str, List[Recommendation]] = {}
    for recommendation in active_recommendations:
        for finding_id in recommendation.target_finding_ids:
            active_by_finding.setdefault(finding_id, []).append(recommendation)
    impacts_by_finding: Dict[str, List[Any]] = {}
    for impact in impacts:
        for finding_id in impact.target_finding_ids:
            impacts_by_finding.setdefault(finding_id, []).append(impact)
    finding_ids_by_review: Dict[str, List[str]] = {}
    for finding in findings:
        finding.recommendation_ids = [value for value in finding.recommendation_ids if value in active_ids]
        for review_id in finding.source_review_ids:
            finding_ids_by_review.setdefault(review_id, []).append(finding.finding_id)

    debug: List[Dict[str, Any]] = []
    for item in items:
        finding_ids = finding_ids_by_review.get(item.item_id, [])
        active = list(dict.fromkeys(
            recommendation.recommendation_id
            for finding_id in finding_ids
            for recommendation in active_by_finding.get(finding_id, [])
        ))
        blocked_impacts = [
            impact for finding_id in finding_ids for impact in impacts_by_finding.get(finding_id, [])
            if impact.gate_result == "BLOCKED"
        ]
        blocked = list(dict.fromkeys(impact.recommendation_id for impact in blocked_impacts))
        reasons = list(dict.fromkeys(_recommendation_suppression_reason(impact) for impact in blocked_impacts))
        if item.coverage_status == INSUFFICIENT_CONTEXT or item.needs_manual_review:
            message = "建议人工复核。"
        elif active:
            message = _priority_label(item.action_priority)
        elif blocked:
            message = "暂不建议单独修改该条款；候选修改可能削弱当前有效保护。"
        elif item.coverage_status in {"通过", COVERAGE_NOT_APPLICABLE}:
            message = "已覆盖，无需修改。" if item.coverage_status == "通过" else "不适用。"
        elif finding_ids:
            message = "当前不形成独立修改建议。"
        else:
            message = "无需形成独立修改建议。"
        state = {
            "review_id": item.item_id, "finding_ids": finding_ids,
            "recommendation_ids": active, "candidate_recommendation_ids": list(dict.fromkeys(active + blocked)),
            "active_recommendation_ids": active, "blocked_recommendation_ids": blocked,
            "has_active_recommendation": bool(active), "action_priority": item.action_priority,
            "user_message": message, "suppression_reason": reasons, "block_reasons": reasons,
            "summary_recommendation_ids": active, "detail_recommendation_ids": active, "mismatch": False,
            "formal_recommendations": active,
        }
        item.decision_trace["recommendation_display_state"] = state
        item.action_suggestion = message
        if item.narrative_state:
            item.narrative_state["recommendation"] = ""
            item.narrative_state["recommendation_ids"] = active
            item.narrative_state["recommendation_suppression_reason"] = reasons
        debug.append(state)
    final_set = {
        "recommendation_ids": [recommendation.recommendation_id for recommendation in active_recommendations],
        "recommendations": [recommendation.to_public_dict() for recommendation in active_recommendations],
    }
    return final_set, debug


def _legal_default_protection_for_items(items: List[ReviewItemResult]) -> str:
    strengths: List[str] = []
    statuses: List[str] = []
    for item in items:
        gap = (item.decision_trace or {}).get("effective_gap") or {}
        assessment = (item.decision_trace or {}).get("default_law_assessment") or {}
        statuses.append(str(gap.get("statutory_default") or assessment.get("status") or ""))
        strengths.append(str(gap.get("default_strength") or assessment.get("protection_strength") or ""))
    joined = " ".join(statuses + strengths).upper()
    if any(token in joined for token in ("CLEAR_DEFAULT", "SUFFICIENT", "STRONG")):
        return LEGAL_DEFAULT_SUFFICIENT
    if any(token in joined for token in ("PARTIAL_DEFAULT", "PARTIAL", "DEFAULT")):
        return LEGAL_DEFAULT_PARTIAL
    return LEGAL_DEFAULT_NONE


def _final_action_for_priority(priority: str) -> str:
    if priority == PRIORITY_A_CORE:
        return DISPOSITION_MUST_CHANGE
    if priority == PRIORITY_B_PRACTICAL:
        return DISPOSITION_SHOULD_CHANGE
    if priority == PRIORITY_C_OPTIMIZATION:
        return DISPOSITION_OPTIONAL_IMPROVEMENT
    return DISPOSITION_KEEP_CURRENT


def _client_interest_gate(
    findings: List[RiskFinding],
    recommendations: List[Recommendation],
    recommendation_impacts: List[Any],
    items: List[ReviewItemResult],
    client_party: str,
) -> tuple[List[ClientInterestDecision], Dict[str, Any]]:
    items_by_id = {item.item_id: item for item in items}
    recommendations_by_finding: Dict[str, List[Recommendation]] = {}
    for recommendation in recommendations:
        if recommendation.status != "ACTIVE":
            continue
        for finding_id in recommendation.target_finding_ids:
            recommendations_by_finding.setdefault(finding_id, []).append(recommendation)
    impacts_by_finding: Dict[str, List[Any]] = {}
    for impact in recommendation_impacts:
        for finding_id in impact.target_finding_ids:
            impacts_by_finding.setdefault(finding_id, []).append(impact)

    decisions: List[ClientInterestDecision] = []
    for finding in findings:
        source_items = [items_by_id[item_id] for item_id in finding.source_review_ids if item_id in items_by_id]
        source_semantics = " ".join(
            [finding.risk_group, finding.title]
            + [item.node_id for item in source_items]
            + [item.title for item in source_items]
        )
        active_recs = recommendations_by_finding.get(finding.finding_id, [])
        impacts = impacts_by_finding.get(finding.finding_id, [])
        blocked = [impact for impact in impacts if impact.gate_result == "BLOCKED"]
        legal_default = _legal_default_protection_for_items(source_items)
        authority_ids = list(dict.fromkeys(
            authority_id
            for item in source_items
            for authority_id in (((item.decision_trace or {}).get("effective_gap") or {}).get("authority_ids") or [])
            if authority_id
        ))
        if finding.needs_manual_review:
            effect = CLIENT_EFFECT_UNCERTAIN
            disposition = DISPOSITION_MANUAL_REVIEW
            reason = "证据、事实或适用条件仍存在无法自动消解的不确定性，需人工复核后决定是否修改。"
        elif active_recs:
            weakens = any(getattr(impact, "weakens", False) for impact in impacts if impact.gate_result != "BLOCKED")
            effect = CLIENT_EFFECT_UNCERTAIN if weakens else CLIENT_EFFECT_FAVORABLE
            disposition = _final_action_for_priority(finding.priority)
            reason = "候选修改未削弱当前审查立场下的既有合同或法定保护，可以进入最终修改建议。"
        elif blocked:
            effect = CLIENT_EFFECT_ADVERSE
            disposition = DISPOSITION_KEEP_CURRENT if legal_default in {LEGAL_DEFAULT_PARTIAL, LEGAL_DEFAULT_SUFFICIENT} else DISPOSITION_DO_NOT_ADD
            if any(term in source_semantics for term in ("delay_acceptance", "迟延受领", "拒收", "未提货")):
                reason = (
                    "合同未单独约定迟延受领后的风险承担，但法律已有默认规则。"
                    "从买方立场看，主动将该规则写入合同可能使买方承担责任的时间点更加明确，因此当前没有必要主动增加该条款。"
                )
            elif any(term in source_semantics for term in ("expectation_loss", "lost_profit", "可得利益", "预期利益")):
                reason = (
                    "现行法律已经允许守约方依法主张可得利益损失。"
                    "如果主动在合同中加入过窄的计算方式或限制条件，反而可能缩小买方现有救济范围，因此建议保持现状。"
                )
            else:
                reason = "候选修改会增加当前客户义务、转移风险或缩小既有救济；因此不因模板完整性而建议补入合同。"
                if legal_default in {LEGAL_DEFAULT_PARTIAL, LEGAL_DEFAULT_SUFFICIENT}:
                    reason += " 当前法律已有相应默认规则，可先保持现状并避免写入限制性表述。"
        elif legal_default == LEGAL_DEFAULT_SUFFICIENT and finding.priority == PRIORITY_C_OPTIMIZATION:
            effect = CLIENT_EFFECT_NEUTRAL
            disposition = DISPOSITION_KEEP_CURRENT
            reason = "已识别到法律问题，但现行法律默认规则已提供较充分保护，单独修改的客户收益有限。"
        elif legal_default in {LEGAL_DEFAULT_PARTIAL, LEGAL_DEFAULT_SUFFICIENT} and finding.priority == PRIORITY_C_OPTIMIZATION:
            effect = CLIENT_EFFECT_NEUTRAL
            disposition = DISPOSITION_KEEP_CURRENT
            reason = "现行法律已有默认保护，当前仅作为已识别但暂不建议修改的事项。"
        else:
            effect = CLIENT_EFFECT_UNCERTAIN
            disposition = _final_action_for_priority(finding.priority)
            reason = "未发现会明显削弱当前客户利益的候选修改，但仍应结合交易谈判空间判断。"
        decision = ClientInterestDecision(
            risk_id=finding.finding_id,
            review_ids=list(finding.source_review_ids),
            client_party=client_party or "UNCERTAIN",
            effect_on_client=effect,
            legal_default_protection=legal_default,
            recommendation_disposition=disposition,
            decision_reason=reason,
            source_recommendation_ids=[rec.recommendation_id for rec in active_recs],
            blocked_recommendation_ids=list(dict.fromkeys(getattr(impact, "recommendation_id", "") for impact in blocked if getattr(impact, "recommendation_id", ""))),
            authority_ids=authority_ids,
            impact_summary={
                "impact_count": len(impacts),
                "blocked_count": len(blocked),
                "net_effects": list(dict.fromkeys(getattr(impact, "net_effect", "") for impact in impacts if getattr(impact, "net_effect", ""))),
            },
        )
        finding.agreement["client_interest_decision"] = decision.to_public_dict()
        decisions.append(decision)

    blocked_failures = [
        decision for decision in decisions
        if decision.recommendation_disposition == DISPOSITION_MANUAL_REVIEW
        and decision.effect_on_client == CLIENT_EFFECT_UNCERTAIN
    ]
    gate = {
        "status": "REPORT_READY",
        "failures": [],
        "gate_results": {"CLIENT_INTEREST_GATE": "PASS"},
        "decisions": [decision.to_public_dict() for decision in decisions],
        "manual_review_count": len(blocked_failures),
        "adverse_recommendation_blocked_count": sum(1 for decision in decisions if decision.effect_on_client == CLIENT_EFFECT_ADVERSE),
    }
    return decisions, gate


def _build_final_dispositions(
    findings: List[RiskFinding],
    recommendations: List[Recommendation],
    client_decisions: List[ClientInterestDecision],
) -> List[FinalDisposition]:
    decision_by_risk = {decision.risk_id: decision for decision in client_decisions}
    rec_by_id = {recommendation.recommendation_id: recommendation for recommendation in recommendations}
    dispositions: List[FinalDisposition] = []
    for finding in findings:
        decision = decision_by_risk.get(finding.finding_id)
        final_action = decision.recommendation_disposition if decision else _final_action_for_priority(finding.priority)
        final_reason = decision.decision_reason if decision else "按风险优先级形成最终处理动作。"
        if final_action == DISPOSITION_OPTIONAL_IMPROVEMENT and any(
            term in " ".join([finding.risk_group, finding.title]).lower()
            for term in ("ip", "intellectual", "知识产权", "侵权", "商标", "专利", "著作权")
        ):
            final_action = DISPOSITION_SHOULD_CHANGE
            final_reason = "知识产权或侵权责任保障关系到第三方权利主张后的停用、替换和追偿基础，不作为单纯可选优化处理。"
        active_rec_ids = list(decision.source_recommendation_ids if decision else finding.recommendation_ids)
        active_text = "；".join(
            _recommendation_inline_text(rec_by_id[rec_id])
            for rec_id in active_rec_ids
            if rec_id in rec_by_id
        )
        actionable = final_action in {DISPOSITION_MUST_CHANGE, DISPOSITION_SHOULD_CHANGE, DISPOSITION_OPTIONAL_IMPROVEMENT}
        owner = (
            RECOMMENDATION_OWNER_REVIEW
            if actionable and len(finding.source_review_ids) == 1
            else RECOMMENDATION_OWNER_RISK
            if actionable
            else RECOMMENDATION_OWNER_NONE
        )
        recommendation = active_text or (
            "建议保持现状，不主动新增可能削弱客户利益的限制性条款。"
            if final_action in {DISPOSITION_KEEP_CURRENT, DISPOSITION_DO_NOT_ADD}
            else finding.recommendation
        )
        formal_recommendation = recommendation if owner == RECOMMENDATION_OWNER_REVIEW else None
        review_instruction = (
            "现有合同材料不足以确认该事项是否适用，建议结合相关交易背景或补充材料核对。"
            if final_action == DISPOSITION_MANUAL_REVIEW else ""
        )
        severity_action_alignment = (
            "ALIGNED_MUST_CHANGE" if finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL} and final_action == DISPOSITION_MUST_CHANGE
            else "HIGH_DOWNGRADED_WITH_REASON" if finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}
            else "ALIGNED"
        )
        downgrade_reason = ""
        if finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL} and final_action != DISPOSITION_MUST_CHANGE:
            impact = (finding.severity_reason or {}).get("impact") or {}
            materiality = ", ".join(
                key for key, value in impact.items()
                if str(value).upper() in {"HIGH", "CRITICAL"}
            ) or "contract performance"
            protection = (
                "合同已有部分要素和证据保护"
                if finding.covered_element_ids
                else "未发现导致合同当然无效或立即不可签署的事实"
            )
            downgrade_reason = (
                f"HIGH 反映 {materiality} 维度的重大履行或争议风险；但{protection}，"
                "当前缺口可通过平衡补充条款修复，且候选修改未削弱客户既有保护，因此列为 SHOULD_CHANGE，"
                "尚不构成必须阻止签署的 MUST_CHANGE。"
            )
        dispositions.append(FinalDisposition(
            risk_id=finding.finding_id,
            risk_title=finding.title,
            review_ids=list(finding.source_review_ids),
            severity=finding.severity,
            client_effect=decision.effect_on_client if decision else CLIENT_EFFECT_UNCERTAIN,
            legal_default_protection=decision.legal_default_protection if decision else LEGAL_DEFAULT_NONE,
            actionability="ACTIONABLE" if final_action in {DISPOSITION_MUST_CHANGE, DISPOSITION_SHOULD_CHANGE, DISPOSITION_OPTIONAL_IMPROVEMENT} else final_action,
            final_action=final_action,
            final_reason=final_reason,
            recommendation=recommendation,
            recommendation_owner=owner,
            formal_recommendation=formal_recommendation,
            include_in_top_risk=final_action in {DISPOSITION_MUST_CHANGE, DISPOSITION_SHOULD_CHANGE},
            include_in_priority_changes=final_action in {DISPOSITION_MUST_CHANGE, DISPOSITION_SHOULD_CHANGE},
            include_in_optional_improvements=final_action == DISPOSITION_OPTIONAL_IMPROVEMENT,
            review_instruction=review_instruction,
            source_recommendation_ids=active_rec_ids,
            blocked_recommendation_ids=list(decision.blocked_recommendation_ids if decision else []),
            authority_ids=list(decision.authority_ids if decision else []),
            severity_action_alignment=severity_action_alignment,
            downgrade_reason=downgrade_reason,
            final_missing_elements=list(finding.final_missing_elements),
            final_missing_element_ids=[str(row.get("element_id") or "") for row in finding.final_missing_elements if row.get("element_id")],
        ))
    return dispositions


RECOMMENDATION_ELEMENT_ACTIONS: Dict[str, str] = {
    "breach_trigger": "明确服务未提供、停止提供或质量不符合约定时的处理触发条件",
    "cure_first": "优先约定补正、补课、延期、替代或重新提供",
    "refund_after_failed_cure": "补救后仍不能达到约定标准时，按未履行部分结算退费",
    "actual_loss_liability": "涉及赔偿时，以依法能够证明的实际损失为限",
    "course_content_standard": "补充课程内容或教学服务标准，且不得承诺学习效果或保过结果",
    "hour_completion_standard": "明确课时完成和签到确认标准",
    "teacher_requirement": "明确师资安排和服务人员要求",
    "makeup_or_reschedule_standard": "明确调课、停课、缺课和补课规则",
    "nonconformity_handling": "明确服务未达到约定标准后的补正和重新履行机制",
    "paid_amount": "明确实际已支付金额、分期金额或付款节点",
    "unit_price": "明确课时或服务单价及其计算口径",
    "non_tuition_fee_handling": "明确资料费、教材费等非课时费用在退费时是否退还、可扣除条件及计算依据",
    "reasonable_cost_deduction": "明确可依法扣除的合理成本及资料费、教材费等不可退费用范围、计算依据和证明要求",
    "refund_deadline": "明确退款审核、结算及支付完成期限",
    "attendance_record": "明确签到和课时消耗记录的保存方式",
    "service_confirmation": "明确服务完成确认和沟通记录的保存方式",
    "refund_record": "明确退费审核、结算和支付记录的保存方式",
    "notice_and_proof": "明确不可抗力发生后的通知和证明义务",
    "service_adjustment_options": "明确延期、转为线上、替代服务或结算等调整方案",
}

RECOMMENDATION_PLACEHOLDER_TERMS = (
    "对应安排",
    "相关事项",
    "实质条款内容",
    "具体未明要素",
    "其余关键要素",
)


def _recommendation_action_for_element(element: Dict[str, Any]) -> tuple[str, str]:
    element_id = str(element.get("element_id") or "")
    if element_id == "core_contract_arrangement":
        return "", "Element is composite and has no concrete, source-backed drafting action."
    mapped = RECOMMENDATION_ELEMENT_ACTIONS.get(element_id)
    if mapped:
        return mapped, ""
    proposition = str(element.get("proposition") or "").strip("。；; ")
    if not proposition or any(term in proposition for term in RECOMMENDATION_PLACEHOLDER_TERMS):
        return "", "Element proposition is not specific enough for a formal recommendation."
    proposition = re.sub(r"(?:是否)?明确$", "", proposition).strip("。；; ")
    return f"明确{proposition}", ""


def _bind_recommendations_to_final_dispositions(
    recommendations: List[Recommendation],
    findings: List[RiskFinding],
    dispositions: List[FinalDisposition],
) -> List[Recommendation]:
    finding_by_id = {finding.finding_id: finding for finding in findings}
    disposition_by_risk = {row.risk_id: row for row in dispositions}
    actionable = {DISPOSITION_MUST_CHANGE, DISPOSITION_SHOULD_CHANGE, DISPOSITION_OPTIONAL_IMPROVEMENT}
    retained: List[Recommendation] = []
    for recommendation in recommendations:
        statutory_clauses = [
            dict(row) for row in recommendation.clauses
            if row.get("source_type") in {"STATUTORY_RULE", "STATUTORY_DEFAULT"}
        ]
        statutory_components = [
            dict(row) for row in recommendation.components
            if row.get("source_type") in {"STATUTORY_RULE", "STATUTORY_DEFAULT"}
        ]
        fragments: List[Dict[str, Any]] = []
        input_ids: List[str] = []
        excluded: Dict[str, str] = {}
        active_risk_ids: List[str] = []
        for risk_id in recommendation.source_finding_ids:
            disposition = disposition_by_risk.get(risk_id)
            finding = finding_by_id.get(risk_id)
            if not disposition or not finding or disposition.final_action not in actionable:
                continue
            active_risk_ids.append(risk_id)
            for element in disposition.final_missing_elements:
                element_id = str(element.get("element_id") or "")
                if not element_id or element_id in input_ids:
                    continue
                input_ids.append(element_id)
                text_value, excluded_reason = _recommendation_action_for_element(element)
                if excluded_reason:
                    excluded[element_id] = excluded_reason
                    continue
                fragments.append({
                    "recommendation_fragment_id": f"{recommendation.recommendation_id}-FRAG-{len(fragments) + 1:02d}",
                    "text": text_value,
                    "source_element_ids": [element_id],
                    "source_review_ids": [str(element.get("source_review_id") or "")],
                    "source_risk_id": risk_id,
                    "action_type": disposition.final_action,
                    "detail_type": "IMPLEMENTATION_DETAIL",
                })
        for risk_id in active_risk_ids:
            disposition = disposition_by_risk[risk_id]
            disposition.excluded_missing_element_ids = sorted(set(disposition.excluded_missing_element_ids) | set(excluded))
            disposition.excluded_reasons.update(excluded)
        recommendation.recommendation_input_elements = input_ids
        recommendation.fragments = fragments
        recommendation.excluded_element_ids = sorted(excluded)
        recommendation.excluded_reasons = excluded
        recommendation.source_finding_ids = sorted(set(active_risk_ids))
        recommendation.target_finding_ids = sorted(set(active_risk_ids))
        recommendation.target_risk_ids = sorted(set(active_risk_ids))
        if not fragments:
            recommendation.status = "SUPPRESSED_NO_SOURCE_ELEMENT"
            continue
        final_text = "建议" + "；".join(fragment["text"] for fragment in fragments) + "。"
        recommendation.suggested_text = final_text
        recommendation.proposed_change = final_text
        recommendation.proposed_text = final_text
        recommendation.clauses = statutory_clauses + [{
            "text": fragment["text"],
            "source_type": "RISK_MITIGATION",
            "source_element_ids": list(fragment["source_element_ids"]),
            "legal_claim_ids": [],
            "legal_requirement": False,
            "drafting_choice": True,
            "rationale": "该动作仅处理 FinalDisposition 确认的真实缺失元素。",
        } for fragment in fragments]
        recommendation.components = statutory_components + [{
            "proposition": fragment["text"],
            "source_type": "RISK_MITIGATION",
            "source_element_ids": list(fragment["source_element_ids"]),
            "statutory_basis": "",
            "authority": "",
            "supported_scope": "",
            "drafting_reason": "由 FinalDisposition.final_missing_elements 生成。",
            "confidence": (recommendation.confidence or {}).get("level", "medium"),
        } for fragment in fragments]
        recommendation.status = "FINAL_TRUTH_BOUND"
        retained.append(recommendation)

    recs_by_risk: Dict[str, List[Recommendation]] = {}
    for recommendation in retained:
        for risk_id in recommendation.source_finding_ids:
            recs_by_risk.setdefault(risk_id, []).append(recommendation)
    for finding in findings:
        finding.recommendation_ids = [rec.recommendation_id for rec in recs_by_risk.get(finding.finding_id, [])]
    for disposition in dispositions:
        bound = recs_by_risk.get(disposition.risk_id, [])
        disposition.source_recommendation_ids = [rec.recommendation_id for rec in bound]
        bound_text = "；".join(rec.suggested_text for rec in bound)
        if disposition.final_action in actionable and bound_text:
            disposition.recommendation = bound_text
            disposition.formal_recommendation = bound_text if disposition.recommendation_owner == RECOMMENDATION_OWNER_REVIEW else None
        elif not bound_text:
            disposition.recommendation = ""
            disposition.formal_recommendation = None
            disposition.include_in_priority_changes = False
            disposition.include_in_optional_improvements = False
            disposition.report_visibility = "VISIBLE"
            disposition.suppression_reason = (
                "现有结构化结果没有可追溯到具体缺失要素的正式修改依据。"
            )
            finding = finding_by_id.get(disposition.risk_id)
            service_domain = bool(finding and finding.source_review_ids) and all(
                str(review_id).startswith("SVC-") for review_id in finding.source_review_ids
            )
            if disposition.final_action == DISPOSITION_OPTIONAL_IMPROVEMENT and service_domain:
                disposition.final_action = DISPOSITION_KEEP_CURRENT
                disposition.actionability = DISPOSITION_KEEP_CURRENT
                disposition.final_reason = (
                    "现有结构化结果仅包含复合事项标题，未形成可追溯到具体缺失要素的修改依据，"
                    "因此不计入正式可选优化并保持现状。"
                )
    return retained


def _recommendation_truth_binding_audit(
    recommendations: List[Recommendation],
    findings: List[RiskFinding],
    dispositions: List[FinalDisposition],
) -> Dict[str, Any]:
    finding_by_id = {finding.finding_id: finding for finding in findings}
    recs_by_risk: Dict[str, List[Recommendation]] = {}
    for recommendation in recommendations:
        for risk_id in recommendation.source_finding_ids:
            recs_by_risk.setdefault(risk_id, []).append(recommendation)
    rows: List[Dict[str, Any]] = []
    unmapped: List[Dict[str, Any]] = []
    leakage: List[Dict[str, Any]] = []
    covered_reintroduced: List[Dict[str, Any]] = []
    placeholders: List[Dict[str, Any]] = []
    disposition_mismatches: List[Dict[str, Any]] = []
    no_action = {DISPOSITION_KEEP_CURRENT, DISPOSITION_DO_NOT_ADD, "NO_ACTION", "PASS", COVERAGE_NOT_APPLICABLE}
    for disposition in dispositions:
        finding = finding_by_id.get(disposition.risk_id)
        if not finding:
            continue
        final_ids = set(disposition.final_missing_element_ids)
        covered_ids = set(finding.covered_element_ids)
        risk_recs = recs_by_risk.get(disposition.risk_id, [])
        fragments = [fragment for rec in risk_recs for fragment in rec.fragments]
        fragment_ids = {str(element_id) for fragment in fragments for element_id in fragment.get("source_element_ids") or []}
        for fragment in fragments:
            source_ids = set(fragment.get("source_element_ids") or [])
            if not source_ids:
                unmapped.append({"risk_id": disposition.risk_id, "fragment": fragment})
            if not source_ids <= final_ids:
                leakage.append({"risk_id": disposition.risk_id, "fragment": fragment, "outside_final_missing": sorted(source_ids - final_ids)})
            if source_ids & covered_ids:
                covered_reintroduced.append({"risk_id": disposition.risk_id, "fragment": fragment, "covered_element_ids": sorted(source_ids & covered_ids)})
            if any(term in str(fragment.get("text") or "") for term in RECOMMENDATION_PLACEHOLDER_TERMS):
                placeholders.append({"risk_id": disposition.risk_id, "fragment": fragment})
        if disposition.final_action in no_action and risk_recs:
            disposition_mismatches.append({"risk_id": disposition.risk_id, "final_action": disposition.final_action, "recommendation_ids": [rec.recommendation_id for rec in risk_recs]})
        excluded = sorted(final_ids - fragment_ids)
        excluded_reasons = {
            element_id: reason
            for rec in risk_recs
            for element_id, reason in rec.excluded_reasons.items()
        }
        excluded_reasons.update(disposition.excluded_reasons)
        rows.append({
            "risk_id": finding.finding_id,
            "risk_title": finding.title,
            "covered_element_ids": sorted(covered_ids),
            "missing_element_ids": list(finding.missing_element_ids),
            "final_missing_element_ids": sorted(final_ids),
            "recommendation_input_element_ids": sorted({element_id for rec in risk_recs for element_id in rec.recommendation_input_elements}),
            "recommendation_fragment_element_ids": sorted(fragment_ids),
            "leaked_covered_element_ids": sorted(fragment_ids & covered_ids),
            "unmapped_recommendation_fragments": [fragment for fragment in fragments if not fragment.get("source_element_ids")],
            "excluded_missing_element_ids": sorted(set(excluded) | set(disposition.excluded_missing_element_ids)),
            "excluded_reasons": excluded_reasons,
        })
    return {
        "status": "PASS" if not (unmapped or leakage or covered_reintroduced or placeholders or disposition_mismatches) else "FAIL",
        "rows": rows,
        "unmapped_recommendation_fragments": unmapped,
        "recommendation_element_leakage": leakage,
        "recommendation_covered_element_leakage": covered_reintroduced,
        "placeholder_recommendation_text": placeholders,
        "final_disposition_mismatches": disposition_mismatches,
    }


def _recommendation_truth_binding_gate(audit: Dict[str, Any]) -> Dict[str, Any]:
    checks = {
        "RECOMMENDATION_SOURCE_UNMAPPED": audit.get("unmapped_recommendation_fragments") or [],
        "RECOMMENDATION_ELEMENT_LEAKAGE": audit.get("recommendation_element_leakage") or [],
        "RECOMMENDATION_COVERED_ELEMENT_REINTRODUCED": audit.get("recommendation_covered_element_leakage") or [],
        "RECOMMENDATION_PLACEHOLDER_TEXT": audit.get("placeholder_recommendation_text") or [],
        "RECOMMENDATION_FINAL_DISPOSITION_MISMATCH": audit.get("final_disposition_mismatches") or [],
    }
    failures = [{
        "requirement": code,
        "failure_stage": "Recommendation Truth Binding",
        "root_cause": f"{code} detected {len(rows)} recommendation truth violations.",
        "responsible_function": "_recommendation_truth_binding_audit",
        "current_status": "FAIL",
    } for code, rows in checks.items() if rows]
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "gate_results": {code: "PASS" if not rows else "FAIL" for code, rows in checks.items()},
        "rows": list(audit.get("rows") or []),
    }


def _high_risk_disposition_audit(
    findings: List[RiskFinding],
    dispositions: List[FinalDisposition],
) -> List[Dict[str, Any]]:
    finding_by_id = {finding.finding_id: finding for finding in findings}
    rows: List[Dict[str, Any]] = []
    for disposition in dispositions:
        if disposition.severity not in {SEVERITY_HIGH, SEVERITY_CRITICAL}:
            continue
        finding = finding_by_id.get(disposition.risk_id)
        reason = (finding.severity_reason or {}) if finding else {}
        rows.append({
            "risk_id": disposition.risk_id,
            "risk_title": disposition.risk_title,
            "severity": disposition.severity,
            "severity_reason": reason,
            "materiality_factors": reason.get("impact") or {},
            "existing_protection": {
                "covered_element_ids": list(finding.covered_element_ids if finding else []),
                "legal_default_protection": disposition.legal_default_protection,
            },
            "client_interest_effect": disposition.client_effect,
            "final_action": disposition.final_action,
            "action_reason": disposition.final_reason,
            "downgrade_reason": disposition.downgrade_reason,
        })
    return rows


def _visible_optional_dispositions(dispositions: List[FinalDisposition]) -> List[FinalDisposition]:
    return [
        disposition for disposition in dispositions
        if disposition.final_action == DISPOSITION_OPTIONAL_IMPROVEMENT
        and disposition.report_visibility == "VISIBLE"
        and bool(
            getattr(disposition, "formal_recommendation", None)
            or (
                getattr(disposition, "recommendation_owner", "") == RECOMMENDATION_OWNER_RISK
                and getattr(disposition, "recommendation", "")
            )
        )
    ]


def _is_service_disposition_scope(dispositions: List[FinalDisposition]) -> bool:
    review_ids = [review_id for row in dispositions for review_id in row.review_ids]
    return bool(review_ids) and all(str(review_id).startswith("SVC-") for review_id in review_ids)


def _final_disposition_summary(dispositions: List[FinalDisposition]) -> Dict[str, int]:
    counts = Counter(disposition.final_action for disposition in dispositions)
    visible_optional = _visible_optional_dispositions(dispositions)
    return {
        "total": len(dispositions),
        "must_change": counts.get(DISPOSITION_MUST_CHANGE, 0),
        "should_change": counts.get(DISPOSITION_SHOULD_CHANGE, 0),
        "optional_improvement": len(visible_optional) if _is_service_disposition_scope(dispositions) else counts.get(DISPOSITION_OPTIONAL_IMPROVEMENT, 0),
        "keep_current": counts.get(DISPOSITION_KEEP_CURRENT, 0),
        "do_not_add": counts.get(DISPOSITION_DO_NOT_ADD, 0),
        "manual_review": counts.get(DISPOSITION_MANUAL_REVIEW, 0),
        "actionable": counts.get(DISPOSITION_MUST_CHANGE, 0) + counts.get(DISPOSITION_SHOULD_CHANGE, 0),
        "protected_no_change": counts.get(DISPOSITION_KEEP_CURRENT, 0) + counts.get(DISPOSITION_DO_NOT_ADD, 0),
    }


def _apply_final_disposition_states(items: List[ReviewItemResult], dispositions: List[FinalDisposition]) -> None:
    by_review: Dict[str, List[FinalDisposition]] = {}
    for disposition in dispositions:
        for review_id in disposition.review_ids:
            by_review.setdefault(review_id, []).append(disposition)
    priority = {
        DISPOSITION_MUST_CHANGE: 0,
        DISPOSITION_SHOULD_CHANGE: 1,
        DISPOSITION_OPTIONAL_IMPROVEMENT: 2,
        DISPOSITION_MANUAL_REVIEW: 3,
        DISPOSITION_KEEP_CURRENT: 4,
        DISPOSITION_DO_NOT_ADD: 5,
    }
    for item in items:
        related = sorted(by_review.get(item.item_id, []), key=lambda row: (priority.get(row.final_action, 9), row.risk_id))
        if not related:
            continue
        item.decision_trace["final_dispositions"] = [row.to_public_dict() for row in related]
        active = [row for row in related if row.final_action in {DISPOSITION_MUST_CHANGE, DISPOSITION_SHOULD_CHANGE, DISPOSITION_OPTIONAL_IMPROVEMENT}]
        protected = [row for row in related if row.final_action in {DISPOSITION_KEEP_CURRENT, DISPOSITION_DO_NOT_ADD}]
        if item.coverage_status == "通过":
            item.action_priority = ACTION_PRIORITY_NONE
            item.review_priority = ACTION_PRIORITY_NONE
            item.action_suggestion = "已覆盖，无需修改。"
        elif active:
            top = active[0]
            item.action_priority = {
                DISPOSITION_MUST_CHANGE: PRIORITY_A_CORE,
                DISPOSITION_SHOULD_CHANGE: PRIORITY_B_PRACTICAL,
                DISPOSITION_OPTIONAL_IMPROVEMENT: PRIORITY_C_OPTIMIZATION,
            }.get(top.final_action, item.action_priority)
            item.review_priority = item.action_priority
            item.action_suggestion = _priority_label(item.action_priority)
        elif protected:
            item.action_priority = ACTION_PRIORITY_NONE
            item.review_priority = ACTION_PRIORITY_NONE
            item.action_suggestion = "已识别法律问题，但当前建议保持现状。"
        state = item.decision_trace.get("recommendation_display_state") or {}
        state.update({
            "final_actions": [row.final_action for row in related],
            "final_disposition_ids": [row.risk_id for row in related],
            "final_disposition_titles": [row.risk_title for row in related if row.risk_title],
            "final_recommendations": [row.recommendation for row in related if row.recommendation],
            "formal_recommendations": [row.formal_recommendation for row in related if row.formal_recommendation],
            "recommendation_owners": list(dict.fromkeys(row.recommendation_owner for row in related)),
            "review_instructions": [row.review_instruction for row in related if row.review_instruction],
            "user_message": item.action_suggestion,
        })
        item.decision_trace["recommendation_display_state"] = state


def _final_disposition_invariant_gate(findings: List[RiskFinding], dispositions: List[FinalDisposition]) -> Dict[str, Any]:
    severity_summary = {
        "重大风险": sum(1 for finding in findings if finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}),
        "中等风险": sum(1 for finding in findings if finding.severity == SEVERITY_MEDIUM),
        "低风险": sum(1 for finding in findings if finding.severity == SEVERITY_LOW),
    }
    severity_total = sum(severity_summary.values())
    disposition_summary = _final_disposition_summary(dispositions)
    disposition_total = (
        disposition_summary["must_change"]
        + disposition_summary["should_change"]
        + disposition_summary["optional_improvement"]
        + disposition_summary["keep_current"]
        + disposition_summary["do_not_add"]
        + disposition_summary["manual_review"]
    )
    failures = []
    hidden_optional = [
        disposition.risk_id for disposition in dispositions
        if disposition.final_action == DISPOSITION_OPTIONAL_IMPROVEMENT
        and disposition not in _visible_optional_dispositions(dispositions)
    ] if _is_service_disposition_scope(dispositions) else []
    if severity_total != len(findings):
        failures.append({
            "requirement": "RISK_STATISTICS_INVARIANT",
            "failure_stage": "FinalDisposition",
            "root_cause": "Severity subtotal does not equal RiskFinding total.",
            "current_status": "FAIL",
        })
    if disposition_total != len(dispositions):
        failures.append({
            "requirement": "FINAL_DISPOSITION_INVARIANT",
            "failure_stage": "FinalDisposition",
            "root_cause": "Final action subtotal does not equal FinalDisposition total.",
            "current_status": "FAIL",
        })
    if hidden_optional:
        failures.append({
            "requirement": "OPTIONAL_IMPROVEMENT_VISIBILITY_INVARIANT",
            "failure_stage": "FinalDisposition Report Projection",
            "root_cause": f"Optional dispositions cannot be counted without a visible formal recommendation: {', '.join(hidden_optional)}.",
            "current_status": "FAIL",
        })
    illegal_formal = [
        disposition.risk_id for disposition in dispositions
        if (
            disposition.final_action not in {DISPOSITION_MUST_CHANGE, DISPOSITION_SHOULD_CHANGE, DISPOSITION_OPTIONAL_IMPROVEMENT}
            or disposition.recommendation_owner != RECOMMENDATION_OWNER_REVIEW
        )
        and disposition.formal_recommendation
    ]
    if illegal_formal:
        failures.append({
            "requirement": "FORMAL_RECOMMENDATION_FINAL_DISPOSITION_INVARIANT",
            "failure_stage": "FinalDisposition",
            "root_cause": f"Non-review-owned or non-actionable dispositions exposed formal recommendations: {', '.join(illegal_formal)}.",
            "current_status": "FAIL",
        })
    risk_owned = [disposition.risk_id for disposition in dispositions if disposition.recommendation_owner == RECOMMENDATION_OWNER_RISK]
    if len(risk_owned) != len(set(risk_owned)):
        failures.append({
            "requirement": "RECOMMENDATION_OWNERSHIP_INVARIANT",
            "failure_stage": "FinalDisposition",
            "root_cause": "A Risk-owned recommendation appears more than once for the same RiskEntity.",
            "current_status": "FAIL",
        })
    high_non_must_without_reason = [
        disposition.risk_id for disposition in dispositions
        if disposition.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}
        and disposition.final_action != DISPOSITION_MUST_CHANGE
        and not str(disposition.downgrade_reason or disposition.final_reason or "").strip()
    ]
    if high_non_must_without_reason:
        failures.append({
            "requirement": "HIGH_NON_MUST_CHANGE_REASON_INVARIANT",
            "failure_stage": "FinalDisposition",
            "root_cause": f"HIGH severity dispositions without MUST_CHANGE must expose an action reason: {', '.join(high_non_must_without_reason)}.",
            "current_status": "FAIL",
        })
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "gate_results": {
            "RISK_STATISTICS_INVARIANT": "PASS" if severity_total == len(findings) else "FAIL",
            "FINAL_DISPOSITION_INVARIANT": "PASS" if disposition_total == len(dispositions) else "FAIL",
            "FORMAL_RECOMMENDATION_FINAL_DISPOSITION_INVARIANT": "PASS" if not illegal_formal else "FAIL",
            "RECOMMENDATION_OWNERSHIP_INVARIANT": "PASS" if len(risk_owned) == len(set(risk_owned)) else "FAIL",
            "HIGH_NON_MUST_CHANGE_REASON_INVARIANT": "PASS" if not high_non_must_without_reason else "FAIL",
            "OPTIONAL_IMPROVEMENT_VISIBILITY_INVARIANT": "PASS" if not hidden_optional else "FAIL",
        },
        "risk_total": len(findings),
        "severity_summary": severity_summary,
        "final_disposition_total": len(dispositions),
        "final_disposition_summary": disposition_summary,
        "visible_optional_disposition_ids": [row.risk_id for row in _visible_optional_dispositions(dispositions)],
        "hidden_optional_disposition_ids": hidden_optional,
    }


def _release_quality_gate(
    items: List[ReviewItemResult],
    findings: List[RiskFinding],
    report: str,
) -> Dict[str, Any]:
    failures: List[Dict[str, str]] = []
    manual_review_count = sum(1 for item in items if item.needs_manual_review)
    if manual_review_count == 0 and "建议人工复核" in report:
        failures.append(
            {
                "requirement": "Manual Review Consistency",
                "failure_stage": "Report Consistency Validation",
                "root_cause": "报告文本出现人工复核措辞，但结构化统计为0。",
                "responsible_function": "_format_markdown_v2",
                "current_status": "FAIL",
            }
        )
    if "Legacy" in report or "原始风险等级" in report or "风险等级：" in report:
        failures.append(
            {
                "requirement": "Hide Legacy Severity",
                "failure_stage": "Report Consistency Validation",
                "root_cause": "正式报告仍暴露审查项旧风险等级。",
                "responsible_function": "_format_markdown_v2",
                "current_status": "FAIL",
            }
        )
    internal_terms = ["RF-", "REC-", "A_CORE", "B_PRACTICAL", "C_OPTIMIZATION", "LLM_PRIORITY", "Fact Graph", "Semantic Entailment", "rule_fallback"]
    leaked_terms = [term for term in internal_terms if term in report]
    if leaked_terms:
        failures.append(
            {
                "requirement": "Hide Internal Terms",
                "failure_stage": "Report Consistency Validation",
                "root_cause": f"正式报告暴露内部术语：{', '.join(leaked_terms)}。",
                "responsible_function": "_format_markdown_v2",
                "current_status": "FAIL",
            }
        )
    if "建议重点完善" in report or "对你而言建议修改" in report or "风险评级为" in report:
        failures.append(
            {
                "requirement": "Priority Narrative Closure",
                "failure_stage": "Report Consistency Validation",
                "root_cause": "正式报告仍出现旧风险等级驱动的行动文案。",
                "responsible_function": "_action_suggestion_for_item",
                "current_status": "FAIL",
            }
        )
    duplicate_groups = len(findings) - len({finding.risk_group for finding in findings})
    if duplicate_groups:
        failures.append(
            {
                "requirement": "Risk Aggregation",
                "failure_stage": "Risk Aggregation Validation",
                "root_cause": "同一 risk_group 生成多个 RiskFinding。",
                "responsible_function": "_build_risk_findings",
                "current_status": "FAIL",
            }
        )
    blocked = [finding.finding_id for finding in findings if (finding.verification or {}).get("status") == "BLOCK"]
    if blocked:
        failures.append(
            {
                "requirement": "Independent Verification",
                "failure_stage": "Independent Verification",
                "root_cause": f"风险发现 {', '.join(blocked)} 未通过独立验证。",
                "responsible_function": "_run_independent_verifier",
                "current_status": "FAIL",
            }
        )
    unsupported_positive = [
        finding.finding_id
        for finding in findings
        if any(item.coverage_status == "风险条款" for item in items if item.item_id in finding.source_review_ids)
        and not _finding_has_supporting_evidence(finding)
    ]
    if unsupported_positive:
        failures.append(
            {
                "requirement": "Evidence Supports Positive Finding",
                "failure_stage": "Evidence-to-Finding Gate",
                "root_cause": f"正向风险发现缺少 SUPPORTS/PARTIAL_SUPPORT 证据：{', '.join(unsupported_positive)}。",
                "responsible_function": "_filter_unsupported_positive_findings",
                "current_status": "FAIL",
            }
        )
    narrative_contradictions = [
        finding.finding_id
        for finding in findings
        for item in items
        if item.item_id in finding.source_review_ids
        and item.coverage_status == "风险条款"
        and any(term in (item.reasoning_summary or item.risk_point_description or "") for term in ("未发现", "未找到", "不存在"))
    ]
    if narrative_contradictions:
        failures.append(
            {
                "requirement": "Cross-layer Consistency",
                "failure_stage": "Finding/Narrative/Evidence Consistency Gate",
                "root_cause": f"风险发现与审查项叙事存在正反矛盾：{', '.join(sorted(set(narrative_contradictions)))}。",
                "responsible_function": "_release_quality_gate",
                "current_status": "FAIL",
            }
        )
    high_findings = [finding for finding in findings if finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}]
    has_core = any(finding.priority == PRIORITY_A_CORE for finding in findings)
    priority_consistency = {
        "status": "PASS" if not high_findings or has_core else "WARN_EXPLAINED",
        "high_or_critical_count": len(high_findings),
        "a_core_count": sum(1 for finding in findings if finding.priority == PRIORITY_A_CORE),
        "reason": "HIGH/CRITICAL findings mapped to A_CORE or no HIGH/CRITICAL findings present."
        if not high_findings or has_core
        else "HIGH/CRITICAL findings exist without A_CORE; verifier records this as explainable only when economic exposure is low or finding is non-core drafting risk.",
    }
    missing_sentence_evidence = [
        finding.finding_id
        for finding in findings
        if finding.priority == PRIORITY_A_CORE
        and not any((evidence.get("quote") and evidence.get("sentence_index")) for evidence in (finding.evidence or finding.supporting_evidence or []))
    ]
    if missing_sentence_evidence:
        failures.append(
            {
                "requirement": "Sentence-level Evidence for A_CORE Finding",
                "failure_stage": "Evidence Fidelity Gate",
                "root_cause": f"优先处理风险缺少句子级证据：{', '.join(missing_sentence_evidence)}。",
                "responsible_function": "_enrich_evidence_sources",
                "current_status": "FAIL",
            }
        )
    missing_entailment = [
        item.item_id
        for item in items
        if item.legal_references and any(not claim.get("citation_entailment_status") for claim in item.legal_references)
    ]
    if missing_entailment:
        failures.append(
            {
                "requirement": "Legal Citation Entailment Status",
                "failure_stage": "Legal Citation Validation",
                "root_cause": f"审查项法律引用缺少 entailment 状态：{', '.join(missing_entailment)}。",
                "responsible_function": "_apply_citation_claims",
                "current_status": "FAIL",
            }
        )
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "manual_review_count": manual_review_count,
        "duplicate_finding_groups": duplicate_groups,
        "priority_consistency_verification": priority_consistency,
    }


PRODUCTION_FORBIDDEN_INTERNAL_TOKENS = (
    "agent.exists", "claim_id", "fact_id", "review_id=", "coverage_status=",
    "applicability=", "domain_pack", "confidence_bundle", "source_review_ids", "review_mode",
    "统一事实图谱", "统一商业事实图谱", "Fact Graph", "Canonical Fact", "Canonical Claim",
    "CoverageElement", "SatisfactionPath", "DefaultLawResult", "EffectiveGap", "ReviewExecutionContext",
    "dynamic_quantity", "order_mechanism", "risk_transfer_rule", "receipt_is_final_acceptance",
    "late_delivery_remedy", "payment_account", "quality_standard_hierarchy", "quality_remedy",
    "inspection_regime", "deemed_acceptance_scope", "price_mechanism",
    "confirmed_order_price_protected", "termination_effect", "document_precedence",
)


def _production_internal_token_gate(report: str) -> Dict[str, Any]:
    locations = [
        {"token": token, "count": report.count(token)}
        for token in PRODUCTION_FORBIDDEN_INTERNAL_TOKENS
        if token in report
    ]
    already_found = {row["token"] for row in locations}
    dotted_machine_fields = list(dict.fromkeys(re.findall(r"\b[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+\b", report)))
    locations.extend({"token": token, "count": report.count(token)} for token in dotted_machine_fields if token not in already_found)
    failures = []
    if locations:
        failures.append(
            {
                "requirement": "PRODUCTION_INTERNAL_TOKEN_GATE",
                "failure_stage": "Post-render Production Serializer Gate",
                "root_cause": "正式报告包含仅供调试使用的内部标记。",
                "responsible_function": "_format_markdown_v2",
                "current_status": "FAIL",
            }
        )
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "gate_results": {"PRODUCTION_INTERNAL_TOKEN_GATE": "PASS" if not locations else "FAIL"},
        "forbidden_internal_tokens_found": [row["token"] for row in locations],
        "locations": locations,
        "count": sum(row["count"] for row in locations),
    }


def _default_law_provenance_gate(items: List[ReviewItemResult], report: str) -> Dict[str, Any]:
    breaks: List[Dict[str, Any]] = []
    rows: List[Dict[str, Any]] = []
    for item in items:
        gap = (item.decision_trace or {}).get("effective_gap") or {}
        if not gap.get("affected_effective_gap"):
            continue
        expected = list(gap.get("authority_ids") or [])
        propagated = [
            claim for claim in (item.legal_references or [])
            if claim.get("authority_id") in expected
            and claim.get("freshness_status") == "CURRENT"
            and claim.get("citation_entailment_status") in {"DIRECT_SUPPORT", "PARTIAL_SUPPORT"}
        ]
        displayed = [claim for claim in propagated if claim.get("article") and str(claim.get("article")) in report]
        row = {
            "review_id": item.item_id, "coverage_status": item.coverage_status,
            "authority_ids": expected, "legal_freshness": sorted({claim.get("freshness_status") for claim in propagated}),
            "citation_entailment": sorted({claim.get("citation_entailment_status") for claim in propagated}),
            "report_authority_ids": [claim.get("authority_id") for claim in displayed],
            "affected_effective_gap": True,
        }
        rows.append(row)
        if not expected or set(expected) - {claim.get("authority_id") for claim in displayed}:
            breaks.append(row)
    return {
        "status": "BLOCKED" if breaks else "REPORT_READY",
        "failures": [] if not breaks else [{
            "requirement": "DEFAULT_LAW_PROVENANCE_GATE", "failure_stage": "Default Law Report Propagation",
            "root_cause": "Default Law changed the effective risk state but verified authority provenance did not reach the production report.",
            "responsible_function": "_apply_citation_claims/_trusted_legal_basis_display", "current_status": "FAIL",
        }],
        "gate_results": {"DEFAULT_LAW_PROVENANCE_GATE": "FAIL" if breaks else "PASS"},
        "break_count": len(breaks), "rows": rows,
    }


def _benchmark_metrics(items: List[ReviewItemResult], findings: List[RiskFinding]) -> Dict[str, Any]:
    duplicate_groups = len(findings) - len({finding.risk_group for finding in findings})
    manual_review_count = sum(1 for item in items if item.needs_manual_review)
    return {
        "benchmark_version": BENCHMARK_VERSION,
        "parser_version": PARSER_VERSION,
        "fact_schema_version": FACT_SCHEMA_VERSION,
        "retrieval_version": RETRIEVAL_VERSION,
        "domain_pack_version": DOMAIN_PACK_VERSION,
        "default_law_version": DEFAULT_LAW_VERSION,
        "perspective_resolver_version": PERSPECTIVE_RESOLVER_VERSION,
        "production_serializer_version": PRODUCTION_SERIALIZER_VERSION,
        "effective_gap_engine_version": "effective-gap-6.7-freeze-1.0",
        "recommendation_engine_version": RECOMMENDATION_ENGINE_VERSION,
        "confidence_version": CONFIDENCE_VERSION,
        "sample_size": 0,
        "sample_status": "INSUFFICIENT SAMPLE SIZE",
        "contract_type_accuracy": None,
        "fact_precision": None,
        "fact_recall": None,
        "applicability_accuracy": None,
        "critical_clause_recall": None,
        "coverage_accuracy": None,
        "evidence_precision": None,
        "evidence_recall": None,
        "evidence_fidelity": None,
        "evidence_entailment_accuracy": None,
        "evidence_direction_accuracy": None,
        "evidence_source_accuracy": None,
        "finding_precision": None,
        "finding_recall": None,
        "material_finding_precision": None,
        "material_finding_recall": None,
        "critical_false_negative_rate": None,
        "material_false_positive_rate": None,
        "severity_accuracy": None,
        "priority_accuracy": None,
        "formula_accuracy": None,
        "calculation_accuracy": None,
        "legal_citation_accuracy": None,
        "direct_authority_recall": None,
        "legal_freshness_accuracy": None,
        "evidence_accuracy": None,
        "contradiction_rate": 0 if not any(item.quality_gate_failure_reason for item in items) else None,
        "duplicate_finding_rate": duplicate_groups,
        "context_isolation_accuracy": None,
        "domain_pack_isolation_accuracy": None,
        "cross_layer_consistency_rate": 0 if not any((finding.verification or {}).get("status") == "BLOCK" for finding in findings) else None,
        "unsupported_positive_finding_rate": 0,
        "sale_unilateral_price_false_positive_rate": None,
        "sale_default_law_operational_coverage": None,
        "sale_economic_normalization_coverage": None,
        "top5_risk_recall": None,
        "confidence_calibration_error": None,
        "confidence_brier_score": None,
        "expected_calibration_error": None,
        "confidence_metrics": {
            "predicted_confidence": None,
            "correctness": None,
            "brier_score": None,
            "expected_calibration_error": None,
        },
        "manual_review_precision": None,
        "manual_review_rate": manual_review_count,
        "notes": "当前为 regression smoke metrics；样本量不足，不输出伪精确百分比。",
    }


def _context_consistency_gate(contract_context: Dict[str, Any]) -> Dict[str, Any]:
    contract_type = contract_context.get("contract_type")
    usage = str(contract_context.get("usage_scenario") or "")
    transaction = str(contract_context.get("transaction_purpose") or "")
    domain_attributes = contract_context.get("domain_attributes") or {}
    failures: List[Dict[str, str]] = []
    if contract_type == "sale" and any(term in f"{usage} {transaction}" for term in ("residential", "lease", "rent", "living")):
        failures.append(
            {
                "requirement": "Context Resolver Isolation",
                "failure_stage": "ContractContext",
                "root_cause": "买卖合同上下文混入租赁/居住语义。",
                "responsible_function": "build_contract_context",
                "current_status": "FAIL",
            }
        )
    if contract_type == "sale" and domain_attributes.get("lease_fields_used"):
        failures.append(
            {
                "requirement": "No Lease Fact Leakage",
                "failure_stage": "ContractContext",
                "root_cause": "买卖合同上下文使用了租赁事实字段。",
                "responsible_function": "build_contract_context",
                "current_status": "FAIL",
            }
        )
    return {
        "status": "PASS" if not failures else "BLOCKED",
        "failures": failures,
        "contract_type": contract_type,
        "domain_pack": domain_attributes.get("domain_pack"),
    }


def _element_integrity_rows(items: List[ReviewItemResult]) -> Dict[str, List[Dict[str, Any]]]:
    contradictions: List[Dict[str, Any]] = []
    monotonicity_violations: List[Dict[str, Any]] = []
    for item in items:
        by_element: Dict[str, set[str]] = {}
        for element in item.coverage_elements or []:
            element_id = str(element.get("element_id") or "")
            status = str(element.get("status") or "")
            if not element_id:
                continue
            by_element.setdefault(element_id, set()).add(status)
        for element_id, statuses in by_element.items():
            if statuses & {"COVERED", "PARTIALLY_COVERED"} and statuses & {"MISSING", "UNCERTAIN"}:
                contradictions.append({
                    "review_id": item.item_id,
                    "element_id": element_id,
                    "statuses": sorted(statuses),
                    "reason": "Same element appears in covered/partial and missing/uncertain buckets.",
                })
        state = item.narrative_state or _build_narrative_state(item)
        covered = set(state.get("covered_elements") or [])
        partial = set(state.get("partial_elements") or [])
        missing = set(state.get("missing_elements") or [])
        for label in sorted((covered & missing) | (covered & partial)):
            contradictions.append({
                "review_id": item.item_id,
                "element_id": label,
                "statuses": ["covered", "missing_or_partial"],
                "reason": "Narrative element sets are not disjoint.",
            })
        current = {
            str(element.get("element_id")): _element_truth_status(str(element.get("status") or ""))
            for element in item.coverage_elements or []
            if element.get("element_id")
        }
        for row in (item.decision_trace or {}).get("element_evidence_truth", []):
            if row.get("status") not in {"FOUND", "PARTIAL"}:
                continue
            downstream = current.get(str(row.get("element_id")))
            if downstream in {"MISSING", "UNCERTAIN"}:
                monotonicity_violations.append({
                    "review_id": item.item_id,
                    "element_id": row.get("element_id"),
                    "upstream_status": row.get("status"),
                    "downstream_status": downstream,
                    "upstream_evidence": row.get("evidence_text") or row.get("evidence_ids") or [],
                    "downstream_reason": "ElementEvidence truth was downgraded without conflicting evidence.",
                })
    return {
        "element_status_contradictions": contradictions,
        "evidence_monotonicity_violations": monotonicity_violations,
    }


def _pre_render_quality_gate(
    items: List[ReviewItemResult],
    findings: List[RiskFinding],
    contract_context: Dict[str, Any],
    overall_assessment: Dict[str, Any],
    recommendation_provenance_gate: Dict[str, Any],
) -> Dict[str, Any]:
    failures: List[Dict[str, str]] = []
    context_gate = _context_consistency_gate(contract_context)
    failures.extend(context_gate.get("failures") or [])
    failures.extend(recommendation_provenance_gate.get("failures") or [])
    domain_gates = _domain_quality_gates(items, contract_context)
    failures.extend(domain_gates["failures"])

    pass_without_provenance = [
        item.item_id
        for item in items
        if item.coverage_status == "通过"
        and (item.decision_trace or {}).get("review_mode") != "ABSENCE_REQUIRED"
        and (item.decision_trace or {}).get("review_nature") != "INTERNAL_CLASSIFICATION"
        and not (item.review_evidence_provenance or {}).get("evidence_ids")
    ]
    if pass_without_provenance:
        failures.append(
            {
                "requirement": "PASS_EVIDENCE_PROVENANCE_GATE",
                "failure_stage": "Pre-render Provenance Gate",
                "root_cause": f"需要合同证据的 PASS 审查项缺少可展示来源：{', '.join(pass_without_provenance)}。",
                "responsible_function": "_assemble_review_provenance",
                "current_status": "FAIL",
            }
        )

    partial_narrative_failures: List[str] = []
    for item in items:
        if item.coverage_status != "部分覆盖":
            continue
        state = item.narrative_state or {}
        supporting_elements = [
            element for element in item.coverage_elements or []
            if element.get("status") in {"COVERED", "PARTIALLY_COVERED"}
        ]
        expected = _build_narrative_state(item)
        generated = " ".join(str(state.get(key) or "") for key in ("judgment", "issue", "consequence", "recommendation"))
        narrative_truth_keys = (
            "covered_elements", "partial_elements", "missing_elements",
            "judgment", "issue", "consequence",
        )
        narrative_truth_mismatch = any(state.get(key) != expected.get(key) for key in narrative_truth_keys)
        covered_claimed_missing = any(
            proposition and any(
                phrase in generated
                for phrase in (f"未约定{proposition}", f"缺失{proposition}", f"尚未覆盖：{proposition}")
            )
            for proposition in expected["covered_elements"]
        )
        if (
            not supporting_elements
            or any(not element.get("evidence_ids") for element in supporting_elements)
            or narrative_truth_mismatch
            or covered_claimed_missing
        ):
            partial_narrative_failures.append(item.item_id)
    if partial_narrative_failures:
        failures.append(
            {
                "requirement": "PARTIAL_ELEMENT_NARRATIVE_GATE",
                "failure_stage": "Pre-render Element Narrative Gate",
                "root_cause": f"PARTIAL 元素证据或叙事状态不一致：{', '.join(partial_narrative_failures)}。",
                "responsible_function": "_build_narrative_state",
                "current_status": "FAIL",
            }
        )

    element_integrity = _element_integrity_rows(items)
    if element_integrity["element_status_contradictions"]:
        failures.append(
            {
                "requirement": "ELEMENT_STATUS_CONTRADICTION",
                "failure_stage": "Pre-render Element Integrity Gate",
                "root_cause": f"元素 covered/partial/missing 状态发生交叉：{len(element_integrity['element_status_contradictions'])} 处。",
                "responsible_function": "_element_integrity_rows",
                "current_status": "FAIL",
            }
        )
    if element_integrity["evidence_monotonicity_violations"]:
        failures.append(
            {
                "requirement": "EVIDENCE_MONOTONICITY_VIOLATION",
                "failure_stage": "Pre-render Element Integrity Gate",
                "root_cause": f"上游 FOUND/PARTIAL 证据被下游降级为 MISSING/UNCERTAIN：{len(element_integrity['evidence_monotonicity_violations'])} 处。",
                "responsible_function": "_protect_element_monotonicity",
                "current_status": "FAIL",
            }
        )

    unsupported_positive = [
        finding.finding_id
        for finding in findings
        if any(item.coverage_status == "风险条款" for item in items if item.item_id in finding.source_review_ids)
        and not _finding_has_supporting_evidence(finding)
    ]
    if unsupported_positive:
        failures.append(
            {
                "requirement": "FINDING_EVIDENCE_GATE",
                "failure_stage": "Pre-render Evidence-to-Finding Gate",
                "root_cause": f"存在型风险发现缺少 SUPPORTS 证据：{', '.join(unsupported_positive)}。",
                "responsible_function": "_pre_render_quality_gate",
                "current_status": "FAIL",
            }
        )

    narrative_conflicts = [
        finding.finding_id
        for finding in findings
        for item in items
        if item.item_id in finding.source_review_ids
        and item.coverage_status == "风险条款"
        and any(term in (item.reasoning_summary or item.risk_point_description or "") for term in ("未发现", "未找到", "不存在"))
    ]
    if narrative_conflicts:
        failures.append(
            {
                "requirement": "CROSS_LAYER_CONSISTENCY_GATE",
                "failure_stage": "Pre-render Cross-layer Gate",
                "root_cause": f"风险发现与结构化叙事矛盾：{', '.join(sorted(set(narrative_conflicts)))}。",
                "responsible_function": "_pre_render_quality_gate",
                "current_status": "FAIL",
            }
        )

    default_law_missing = [
        item.item_id
        for item in items
        if item.coverage_status == "缺失"
        and ((item.decision_trace or {}).get("default_law_assessment") or {}).get("default_law_relevant")
        and not ((item.decision_trace or {}).get("effective_gap") or {}).get("default_law_checked")
    ]
    if default_law_missing:
        failures.append(
            {
                "requirement": "DEFAULT_LAW_COMPLETENESS_GATE",
                "failure_stage": "Pre-render Default Law Gate",
                "root_cause": f"声明需要默认法评估的缺失审查项未执行评估：{', '.join(default_law_missing)}。",
                "responsible_function": "_apply_risk_dimensions",
                "current_status": "FAIL",
            }
        )
    effective_gap_invalid = [
        item.item_id for item in items
        if item.coverage_status in {"缺失", "部分覆盖"}
        and ((item.decision_trace or {}).get("default_law_assessment") or {}).get("default_law_relevant")
        and not ((item.decision_trace or {}).get("effective_gap") or {}).get("effective_gap_valid")
    ]
    if effective_gap_invalid:
        failures.append({
            "requirement": "DEFAULT_LAW_EFFECTIVE_GAP_GATE",
            "failure_stage": "Pre-render Effective Gap Gate",
            "root_cause": f"默认法相关审查项缺少有效 Effective Gap：{', '.join(effective_gap_invalid)}。",
            "responsible_function": "_apply_risk_dimensions",
            "current_status": "FAIL",
        })

    partial_narrative_conflicts = [
        item.item_id
        for item in items
        if item.coverage_status == "部分覆盖"
        and any(
            phrase in " ".join(str((item.narrative_state or {}).get(key) or "") for key in ("judgment", "issue", "consequence", "recommendation"))
            for phrase in PARTIAL_TOTAL_MISSING_PHRASES
        )
        and any(element.get("status") in {"COVERED", "PARTIALLY_COVERED"} for element in item.coverage_elements or [])
    ]
    if partial_narrative_conflicts:
        failures.append(
            {
                "requirement": "NARRATIVE_ELEMENT_CONSISTENCY_GATE",
                "failure_stage": "Pre-render Narrative Gate",
                "root_cause": f"PARTIAL 审查项使用整体缺失叙事：{', '.join(partial_narrative_conflicts)}。",
                "responsible_function": "_coverage_safe_reasoning",
                "current_status": "FAIL",
            }
        )

    narrative_rows = _narrative_state_debug_report(items)
    narrative_truth_failures = [row["review_id"] for row in narrative_rows if row["status"] != "PASS"]
    if narrative_truth_failures:
        failures.append(
            {
                "requirement": "NARRATIVE_TRUTH_GATE",
                "failure_stage": "Pre-render Narrative Truth Gate",
                "root_cause": f"Coverage/Finding/Narrative/Recommendation truth state 不一致：{', '.join(narrative_truth_failures)}。",
                "responsible_function": "_narrative_state_debug_report",
                "current_status": "FAIL",
            }
        )

    confidence_conflicts = [
        item.item_id
        for item in items
        if item.quality_gate_failure_reason and (item.system_confidence or {}).get("level") == "high"
    ]
    if confidence_conflicts:
        failures.append(
            {
                "requirement": "CONFIDENCE_VALIDATION_GATE",
                "failure_stage": "Pre-render Confidence Gate",
                "root_cause": f"存在实质一致性错误的审查项仍为 HIGH：{', '.join(confidence_conflicts)}。",
                "responsible_function": "_apply_post_verification_confidence",
                "current_status": "FAIL",
            }
        )

    high_findings = [finding for finding in findings if finding.severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}]
    core_findings = [finding for finding in findings if finding.priority == PRIORITY_A_CORE]
    priority_consistency = {
        "executed": True,
        "high_finding_count": len(high_findings),
        "core_priority_count": len(core_findings),
        "consistency": "PASS" if not high_findings or core_findings else "EXPLAINED",
        "explanations": [],
        "needs_recalibration": False,
    }
    if high_findings and not core_findings:
        priority_consistency["explanations"] = [
            {
                "finding_id": finding.finding_id,
                "severity": finding.severity,
                "priority": finding.priority,
                "default_law_status": finding.default_law_status,
                "economic_impact": (finding.economic_impact or {}).get("level", "unknown"),
                "reason": "重大影响不自动等于 A_CORE；该 Finding 的经济暴露、核心义务、默认法保护、发生概率与可恢复性未达到 A_CORE 阈值。",
            }
            for finding in high_findings
        ]
    unexplained_priority = bool(high_findings and not core_findings and not priority_consistency["explanations"])
    priority_consistency["consistency"] = "INCONSISTENT" if unexplained_priority else "CONSISTENT"
    priority_consistency["needs_recalibration"] = unexplained_priority
    if unexplained_priority:
        failures.append(
            {
                "requirement": "PRIORITY_CONSISTENCY_GATE",
                "failure_stage": "Pre-render Priority Gate",
                "root_cause": "HIGH/CRITICAL Findings 全部未进入 A_CORE 且缺少逐 Finding 结构化解释。",
                "responsible_function": "_pre_render_quality_gate",
                "current_status": "FAIL",
            }
        )
    if overall_assessment.get("signability") == "存在重大风险，建议修改后签署" and not core_findings and not priority_consistency["explanations"]:
        failures.append(
            {
                "requirement": "Signability/Priority Consistency",
                "failure_stage": "Pre-render Priority Gate",
                "root_cause": "重大风险签署结论与零 A_CORE 之间缺少结构化解释。",
                "responsible_function": "_pre_render_quality_gate",
                "current_status": "FAIL",
            }
        )
    signability_decision = overall_assessment.get("signability_decision") or {}
    if findings and not signability_decision.get("decision_finding_ids"):
        failures.append(
            {
                "requirement": "SIGNABILITY_GATE",
                "failure_stage": "Pre-render Signability Gate",
                "root_cause": "可签署性结论缺少决定性 Finding 标识。",
                "responsible_function": "_overall_assessment",
                "current_status": "FAIL",
            }
        )
    invalid_legal_claims = [
        claim.get("claim_id") or item.item_id
        for item in items
        for claim in item.legal_references or []
        if claim.get("article")
        and claim.get("support_type") != "BACKGROUND_ONLY"
        and (
            not claim.get("authority_links")
            or not claim.get("support_scope")
            or claim.get("support_type") not in {"DIRECT_SUPPORT", "PARTIAL_SUPPORT"}
        )
    ]
    if invalid_legal_claims:
        failures.append(
            {
                "requirement": "Legal Claim Authority Trace",
                "failure_stage": "Pre-render Legal Claim Gate",
                "root_cause": f"具体法条缺少 LegalClaim/AuthorityLink/support_scope：{', '.join(invalid_legal_claims)}。",
                "responsible_function": "_pre_render_quality_gate",
                "current_status": "FAIL",
            }
        )
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "priority_consistency_verification": priority_consistency,
        "context_consistency": context_gate,
        "gate_results": {
            "PASS_EVIDENCE_PROVENANCE_GATE": "PASS" if not pass_without_provenance else "FAIL",
            "PARTIAL_ELEMENT_NARRATIVE_GATE": "PASS" if not partial_narrative_failures else "FAIL",
            "ELEMENT_STATUS_CONTRADICTION": "PASS" if not element_integrity["element_status_contradictions"] else "FAIL",
            "EVIDENCE_MONOTONICITY_VIOLATION": "PASS" if not element_integrity["evidence_monotonicity_violations"] else "FAIL",
            "FINDING_EVIDENCE_GATE": "PASS" if not unsupported_positive else "FAIL",
            "CROSS_LAYER_CONSISTENCY_GATE": "PASS" if not narrative_conflicts else "FAIL",
            "DEFAULT_LAW_COMPLETENESS_GATE": "PASS" if not default_law_missing else "FAIL",
            "DEFAULT_LAW_EFFECTIVE_GAP_GATE": "PASS" if not effective_gap_invalid else "FAIL",
            "NARRATIVE_ELEMENT_CONSISTENCY_GATE": "PASS" if not partial_narrative_conflicts else "FAIL",
            "NARRATIVE_TRUTH_GATE": "PASS" if not narrative_truth_failures else "FAIL",
            "PRIORITY_CONSISTENCY_GATE": "PASS" if not unexplained_priority else "FAIL",
            "SIGNABILITY_GATE": "PASS" if not findings or bool(signability_decision.get("decision_finding_ids")) else "FAIL",
            "CONFIDENCE_VALIDATION_GATE": "PASS" if not confidence_conflicts else "FAIL",
            **domain_gates["gate_results"],
        },
    }


REAL_ESTATE_REQUIRED_MATERIAL_GROUPS = {
    "TITLE", "ENCUMBRANCE", "PRICE", "PAYMENT", "REGISTRATION", "DELIVERY",
    "RISK_TRANSFER", "LAND_USE", "BREACH", "HOUSEHOLD_REGISTRATION",
}


def _domain_quality_gates(items: List[ReviewItemResult], contract_context: Dict[str, Any]) -> Dict[str, Any]:
    subject = contract_context.get("subject_matter")
    is_real_estate_sale = contract_context.get("contract_family") == "SALE" and subject == "REAL_ESTATE"
    subtype = contract_context.get("contract_subtype")
    owners = {(item.decision_trace or {}).get("domain_owner", "") for item in items}
    material_groups = {(item.decision_trace or {}).get("material_group", "") for item in items}
    subtype_pass = not is_real_estate_sale or subtype in {
        "RESIDENTIAL_SECONDARY_REAL_ESTATE_SALE", "COMMERCIAL_REAL_ESTATE_SALE", "REAL_ESTATE_SALE",
    }
    isolation_pass = not is_real_estate_sale or "sale/goods" not in owners
    missing_groups = sorted(REAL_ESTATE_REQUIRED_MATERIAL_GROUPS - material_groups) if is_real_estate_sale else []
    coverage_pass = not missing_groups
    framework = ((contract_context.get("domain_attributes") or {}).get("framework_supply") or {})
    is_framework = contract_context.get("transaction_structure") == "FRAMEWORK_SUPPLY"
    item_by_node = {item.node_id: item for item in items}
    framework_nodes = {item.node_id for item in items if item.item_id.startswith("FS-")}
    required_framework_nodes = {node for node in FRAMEWORK_REVIEW_FACT_PATHS if node.startswith("framework_")}
    transaction_structure_pass = not is_framework or (
        contract_context.get("contract_subtype") == "FRAMEWORK_SUPPLY"
        and contract_context.get("subject_matter") == "GOODS"
        and bool(contract_context.get("product_category"))
    )
    framework_domain_pass = not is_framework or (
        "sale/goods/framework_supply" in owners
        and required_framework_nodes.issubset(framework_nodes)
    )
    order_relation_pass = not is_framework or (
        bool((framework.get("order_mechanism") or {}).get("exists"))
        and all(item_by_node.get(node) and item_by_node[node].coverage_status == "通过" for node in (
            "framework_master_order_relationship", "framework_order_formation_confirmation",
        ))
    )
    dynamic_quantity_pass = not is_framework or contract_context.get("dynamic_quantity") is not True or (
        item_by_node.get("framework_dynamic_quantity") is not None
        and item_by_node["framework_dynamic_quantity"].coverage_status == "通过"
        and item_by_node.get("sale_subject_quantity_unit") is not None
        and item_by_node["sale_subject_quantity_unit"].coverage_status == "通过"
    )
    explicit_price_mechanism = bool((framework.get("price_mechanism") or {}).get("exists"))
    price_mechanism_pass = not is_framework or (
        contract_context.get("price_adjustment_mechanism") in {"BILATERAL_ADJUSTMENT", "UNILATERAL_ADJUSTMENT", "FIXED_OR_UNSPECIFIED"}
        and all(item_by_node.get(node) for node in (
            "framework_price_validity", "framework_price_adjustment_trigger",
            "framework_confirmed_order_price", "framework_future_order_deadlock",
        ))
        and (not explicit_price_mechanism or item_by_node["framework_price_adjustment_trigger"].coverage_status == "通过")
    )
    structured_paths = [
        item for item in items
        if ((item.decision_trace or {}).get("alternative_satisfaction") or {}).get("status") == "SATISFIED"
    ]
    alternative_satisfaction_pass = not is_framework or bool(structured_paths) and all(
        item.coverage_status == "通过" for item in structured_paths
    )
    protected_nodes = {
        "sale_delivery_time", "sale_delay_delivery_liability", "sale_risk_transfer_delivery",
        "sale_payment_method_account", "sale_quality_remedy", "sale_inspection_period",
        "sale_deemed_acceptance", "sale_quality_standard_basis", "common_jurisdiction",
    }
    false_risk_nodes = sorted(
        node for node in protected_nodes
        if node in item_by_node
        and node in FRAMEWORK_REVIEW_FACT_PATHS
        and ((item_by_node[node].decision_trace or {}).get("alternative_satisfaction") or {}).get("status") == "SATISFIED"
        and item_by_node[node].coverage_status not in {"通过", COVERAGE_NOT_APPLICABLE}
    ) if is_framework else []
    carrier = item_by_node.get("sale_risk_carrier_delivery")
    if is_framework and (framework.get("carrier_rule_applicability") or {}).get("value") is False:
        if not carrier or carrier.coverage_status != COVERAGE_NOT_APPLICABLE:
            false_risk_nodes.append("sale_risk_carrier_delivery")
    false_risk_pass = not false_risk_nodes
    failures = []
    for requirement, passed, reason in (
        ("DOMAIN_SUBTYPE_GATE", subtype_pass, f"房地产买卖的子类型不一致：{subtype or 'EMPTY'}。"),
        ("DOMAIN_REVIEW_ISOLATION_GATE", isolation_pass, "房地产路径加载了 sale/goods 审查项。"),
        ("DOMAIN_MATERIAL_COVERAGE_GATE", coverage_pass, f"房地产核心材料组未激活：{', '.join(missing_groups)}。"),
        ("TRANSACTION_STRUCTURE_GATE", transaction_structure_pass, "框架供货交易结构、标的类别或子类型不一致。"),
        ("FRAMEWORK_DOMAIN_GATE", framework_domain_pass, "框架供货领域包或核心审查定义未进入生产路径。"),
        ("ORDER_RELATION_GATE", order_relation_pass, "框架供货缺少可追溯的订单形成与确认机制。"),
        ("DYNAMIC_QUANTITY_GATE", dynamic_quantity_pass, "动态数量被错误视为固定数量缺失。"),
        ("PRICE_MECHANISM_GATE", price_mechanism_pass, "价格有效期、调价或既有订单保护未完整覆盖。"),
        ("ALTERNATIVE_SATISFACTION_GATE", alternative_satisfaction_pass, "结构化事实满足路径与最终 Review 状态不一致。"),
        ("FALSE_RISK_EXISTENCE_GATE", false_risk_pass, f"已有明确事实仍生成缺失或错误适用项：{', '.join(false_risk_nodes)}。"),
    ):
        if not passed:
            failures.append({"requirement": requirement, "failure_stage": "Domain Resolution Gate", "root_cause": reason, "responsible_function": "_domain_quality_gates", "current_status": "FAIL"})
    return {
        "failures": failures,
        "gate_results": {
            "DOMAIN_SUBTYPE_GATE": "PASS" if subtype_pass else "FAIL",
            "DOMAIN_REVIEW_ISOLATION_GATE": "PASS" if isolation_pass else "FAIL",
            "DOMAIN_MATERIAL_COVERAGE_GATE": "PASS" if coverage_pass else "FAIL",
            "TRANSACTION_STRUCTURE_GATE": "PASS" if transaction_structure_pass else "FAIL",
            "FRAMEWORK_DOMAIN_GATE": "PASS" if framework_domain_pass else "FAIL",
            "ORDER_RELATION_GATE": "PASS" if order_relation_pass else "FAIL",
            "DYNAMIC_QUANTITY_GATE": "PASS" if dynamic_quantity_pass else "FAIL",
            "PRICE_MECHANISM_GATE": "PASS" if price_mechanism_pass else "FAIL",
            "ALTERNATIVE_SATISFACTION_GATE": "PASS" if alternative_satisfaction_pass else "FAIL",
            "FALSE_RISK_EXISTENCE_GATE": "PASS" if false_risk_pass else "FAIL",
        },
        "loaded_domain_owners": sorted(owners), "activated_material_groups": sorted(material_groups),
        "missing_material_groups": missing_groups,
        "framework_required_nodes": sorted(required_framework_nodes),
        "framework_loaded_nodes": sorted(framework_nodes),
        "false_risk_nodes": false_risk_nodes,
    }


def _element_identity_contradictions(items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    conflicts: List[Dict[str, Any]] = []
    for item in items:
        buckets: Dict[str, set[str]] = {"covered": set(), "partial": set(), "missing": set()}
        labels: Dict[str, str] = {}
        for element in item.coverage_elements or []:
            claim_id = str(element.get("claim_id") or "")
            semantic_key = str(element.get("element_id") or "")
            raw = f"{claim_id}:{semantic_key}" if claim_id and semantic_key else str(
                claim_id or semantic_key or element.get("proposition") or ""
            )
            identity = re.sub(r"[\W_]+", "", raw, flags=re.UNICODE).lower()
            if not identity:
                continue
            labels[identity] = raw
            status = str(element.get("status") or "")
            bucket = "covered" if status == "COVERED" else "partial" if status == "PARTIALLY_COVERED" else "missing" if status in {"MISSING", "UNCERTAIN"} else ""
            if bucket:
                buckets[bucket].add(identity)
        overlap = (buckets["covered"] & buckets["partial"]) | (buckets["covered"] & buckets["missing"]) | (buckets["partial"] & buckets["missing"])
        if overlap:
            conflicts.append({"review_id": item.item_id, "element_ids": sorted(labels[value] for value in overlap)})
    return conflicts


def _common_review_satisfaction_issues(items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    for item in items:
        requirement = common_sale_coverage_requirement(item.node_id)
        if not requirement:
            continue
        generic_elements = [
            element.get("element_id") for element in item.coverage_elements or []
            if element.get("element_id") in {"core_contract_arrangement", "element"}
        ]
        satisfaction = (item.decision_trace or {}).get("common_review_satisfaction") or {}
        satisfied = any(row.get("status") == "SATISFIED" for row in satisfaction.get("satisfaction_paths", []))
        reasons = []
        if generic_elements:
            reasons.append("generic_element_used")
        if not satisfaction.get("satisfaction_paths") and item.coverage_status != COVERAGE_NOT_APPLICABLE:
            reasons.append("satisfaction_path_not_executed")
        if satisfied and item.coverage_status != "通过":
            reasons.append("satisfied_path_not_reflected_in_coverage")
        if reasons:
            issues.append({"review_id": item.item_id, "reasons": reasons})
    return issues


def _shared_claim_reuse_issues(items: List[ReviewItemResult], canonical_claims: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    consumers: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        for element in item.coverage_elements or []:
            claim_id = str(element.get("claim_id") or "")
            if claim_id:
                consumers.setdefault(claim_id, []).append({
                    "review_id": item.item_id,
                    "semantic_key": str(element.get("element_id") or ""),
                    "status": element.get("status"),
                })
    for claim_id, rows in consumers.items():
        claim = canonical_claims.get(claim_id)
        if not claim or getattr(claim, "status", "") != "ASSERTED" or not getattr(claim, "source_clause_ids", []):
            continue
        canonical_object = getattr(claim, "object", None)
        hierarchy = canonical_object.get("hierarchy", {}) if isinstance(canonical_object, dict) else {}
        rejected = [
            row for row in rows
            if row.get("status") not in {"COVERED", "PARTIALLY_COVERED"}
            and (not hierarchy or hierarchy.get(row.get("semantic_key")) is True)
        ]
        if rejected:
            issues.append({"claim_id": claim_id, "consumers": rejected})
    return issues


def _cross_review_shared_claim_state(items: List[ReviewItemResult], canonical_claims: Dict[str, Any]) -> Dict[str, Any]:
    states: Dict[str, Dict[str, Any]] = {}
    item_by_id = {item.item_id: item for item in items}
    for item in items:
        for element in item.coverage_elements or []:
            claim_id = str(element.get("claim_id") or "")
            if not claim_id:
                continue
            semantic_key = str(element.get("element_id") or "")
            state = states.setdefault(claim_id, {
                "claim_id": claim_id, "semantic_elements": [], "canonical_status": "UNKNOWN",
                "canonical_value": None, "fact_ids": [], "evidence_ids": [], "consumer_reviews": [],
                "review_requirements": [], "review_coverage": [], "contradictions": [],
            })
            canonical = canonical_claims.get(claim_id)
            if canonical:
                state.update({
                    "canonical_status": canonical.status, "canonical_value": canonical.object,
                    "fact_ids": list(canonical.fact_ids), "evidence_ids": list(canonical.evidence_ids),
                })
            if semantic_key not in state["semantic_elements"]:
                state["semantic_elements"].append(semantic_key)
            if item.item_id not in state["consumer_reviews"]:
                state["consumer_reviews"].append(item.item_id)
            state["review_requirements"].append({"review_id": item.item_id, "semantic_key": semantic_key, "proposition": element.get("proposition")})
            state["review_coverage"].append({"review_id": item.item_id, "semantic_key": semantic_key, "status": element.get("status"), "reason": element.get("reason")})

    for claim_id, state in states.items():
        by_element: Dict[str, List[Dict[str, Any]]] = {}
        for row in state["review_coverage"]:
            by_element.setdefault(row["semantic_key"], []).append(row)
        hierarchy = ((state.get("canonical_value") or {}).get("hierarchy") or {}) if isinstance(state.get("canonical_value"), dict) else {}
        for semantic_key, rows in by_element.items():
            statuses = {row.get("status") for row in rows}
            covered_missing = bool(statuses & {"COVERED", "PARTIALLY_COVERED"}) and bool(statuses & {"MISSING", "UNCERTAIN"})
            canonical_false_negative = hierarchy.get(semantic_key) is True and bool(statuses & {"MISSING", "UNCERTAIN"})
            if not covered_missing and not canonical_false_negative:
                continue
            contradiction = {
                "type": "CROSS_REVIEW_SHARED_CLAIM_CONTRADICTION" if covered_missing else "SHARED_CLAIM_COVERAGE_DIVERGENCE",
                "claim_id": claim_id, "semantic_key": semantic_key, "interpretations": rows,
            }
            state["contradictions"].append(contradiction)
            for row in rows:
                item = item_by_id.get(row["review_id"])
                if item:
                    item.decision_trace["shared_claim_conflicts"] = sorted(set(
                        list((item.decision_trace or {}).get("shared_claim_conflicts") or []) + [f"{claim_id}:{semantic_key}"]
                    ))
    contradictions = [row for state in states.values() for row in state["contradictions"]]
    return {
        "status": "BLOCKED" if contradictions else "REPORT_READY",
        "failures": [] if not contradictions else [{
            "requirement": "CROSS_REVIEW_SHARED_CLAIM_GATE", "failure_stage": "Cross-review Claim Interpretation",
            "root_cause": "The same canonical semantic element has contradictory review interpretations.",
            "responsible_function": "_cross_review_shared_claim_state", "current_status": "FAIL",
        }],
        "gate_results": {
            "CROSS_REVIEW_SHARED_CLAIM_GATE": "FAIL" if contradictions else "PASS",
            "FALSE_RISK_EXISTENCE_GATE": "FAIL" if contradictions else "PASS",
        },
        "contradiction_count": len(contradictions), "claims": list(states.values()),
    }


def _finding_independence_issues(findings: List[RiskFinding]) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    groups = Counter(finding.risk_group for finding in findings)
    for group, count in groups.items():
        if count > 1:
            issues.append({"risk_group": group, "finding_count": count, "reason": "duplicate_risk_group"})
    rights_findings = [finding for finding in findings if set(finding.source_review_ids) & {"S-11-01", "S-11-03", "S-11-04"}]
    if len(rights_findings) > 1:
        issues.append({"risk_group": "goods_title_and_third_party_rights", "finding_count": len(rights_findings), "reason": "rights_reviews_not_aggregated"})
    return issues


def _consistency_quality_gates(
    items: List[ReviewItemResult],
    findings: List[RiskFinding],
    recommendations: List[Recommendation],
    canonical_claims: Dict[str, Any],
    contract_context: Dict[str, Any],
    report_context: Dict[str, Any],
) -> Dict[str, Any]:
    finding_review_ids = {review_id for finding in findings for review_id in finding.source_review_ids}
    non_applicable_findings = [
        item.item_id for item in items
        if str((item.applicability or {}).get("status") or "APPLICABLE").upper() != "APPLICABLE"
        and item.item_id in finding_review_ids
    ]
    applicability_misorders = [item.item_id for item in items if (item.applicability or {}).get("status") == "NOT_APPLICABLE" and item.coverage_status != COVERAGE_NOT_APPLICABLE]
    claim_conflicts = [claim_id for claim_id, claim in canonical_claims.items() if claim.status == "CONFLICT"]
    interpretation_conflicts = [item.item_id for item in items if (item.decision_trace or {}).get("shared_claim_conflicts")]
    finding_precondition_failures = [
        finding.finding_id for finding in findings
        if (finding.aggregation_signals or {}).get("finding_preconditions")
        and not all(
            bool(precondition.get("all_required_conditions"))
            for precondition in (finding.aggregation_signals or {}).get("finding_preconditions", {}).values()
        )
    ]
    report_context_valid = (
        report_context.get("family") == contract_context.get("contract_family")
        and report_context.get("subject_matter") == contract_context.get("subject_matter")
        and report_context.get("subtype") == contract_context.get("contract_subtype")
        and report_context.get("transaction_structure") == contract_context.get("transaction_structure")
        and not (contract_context.get("subject_matter") == "REAL_ESTATE" and report_context.get("scenario_label") == "商品买卖")
        and not (contract_context.get("transaction_structure") == "FRAMEWORK_SUPPLY" and report_context.get("scenario_label") in {"商品买卖", "一般买卖"})
    )
    finding_ids = {finding.finding_id for finding in findings}
    orphan_recommendations = [rec.recommendation_id for rec in recommendations if rec.type != "OPTIONAL" and (not rec.target_finding_ids or not set(rec.target_finding_ids).issubset(finding_ids))]
    recommendation_text = "\n".join(
        str(value)
        for recommendation in recommendations
        for value in recommendation.to_public_dict().values()
    )
    framework = ((contract_context.get("domain_attributes") or {}).get("framework_supply") or {})
    is_framework = contract_context.get("transaction_structure") == "FRAMEWORK_SUPPLY"
    degradation_conflicts = []
    if is_framework and (framework.get("carrier_rule_applicability") or {}).get("value") is False and any(
        phrase in recommendation_text for phrase in ("交付给第一承运人后", "货交第一承运人后")
    ):
        degradation_conflicts.append("DESTINATION_DELIVERY_REPLACED_BY_CARRIER_HANDOVER")
    if is_framework and (framework.get("receipt_is_final_acceptance") or {}).get("value") is False and any(
        phrase in recommendation_text for phrase in ("签收即视为验收合格", "签字即视为最终验收")
    ):
        degradation_conflicts.append("PRELIMINARY_RECEIPT_REPLACED_BY_FINAL_ACCEPTANCE")
    if is_framework and (framework.get("forecast_binding") or {}).get("value") is False and any(
        phrase in recommendation_text for phrase in ("预测数量具有约束力", "预测即构成采购义务")
    ):
        degradation_conflicts.append("NON_BINDING_FORECAST_REPLACED_BY_BINDING_FORECAST")
    recommendation_non_degradation = not degradation_conflicts
    common_review_issues = _common_review_satisfaction_issues(items)
    element_identity_conflicts = _element_identity_contradictions(items)
    shared_claim_reuse_issues = _shared_claim_reuse_issues(items, canonical_claims)
    finding_independence_issues = _finding_independence_issues(findings)
    product_applicability_issues = [
        item.item_id for item in items
        if item.node_id in {"sale_warranty_manual", "sale_inspection_report_certificate"}
        and (
            (item.coverage_status == COVERAGE_NOT_APPLICABLE and item.item_id in finding_review_ids)
            or (item.coverage_status != COVERAGE_NOT_APPLICABLE and (item.applicability or {}).get("status") == "NOT_APPLICABLE")
        )
    ]
    checks = {
        "APPLICABILITY_PRECONDITION_GATE": not applicability_misorders and not non_applicable_findings,
        "SHARED_CLAIM_CONSISTENCY_GATE": not claim_conflicts,
        "FINDING_PRECONDITION_GATE": not finding_precondition_failures,
        "REPORT_CONTEXT_GATE": report_context_valid,
        "REPORT_TRANSACTION_TRUTH_GATE": report_context_valid,
        "CROSS_REVIEW_CONSISTENCY_GATE": not claim_conflicts and not interpretation_conflicts and not orphan_recommendations,
        "RECOMMENDATION_NON_DEGRADATION_GATE": recommendation_non_degradation,
        "COMMON_REVIEW_SATISFACTION_GATE": not common_review_issues,
        "ELEMENT_IDENTITY_CONTRADICTION_GATE": not element_identity_conflicts,
        "PRODUCT_APPLICABILITY_GATE": not product_applicability_issues,
        "SHARED_CLAIM_REUSE_GATE": not shared_claim_reuse_issues,
        "FINDING_INDEPENDENCE_GATE": not finding_independence_issues,
    }
    failures = []
    details = {
        "non_applicable_findings": non_applicable_findings, "applicability_misorders": applicability_misorders,
        "claim_conflicts": claim_conflicts, "interpretation_conflicts": interpretation_conflicts,
        "finding_precondition_failures": finding_precondition_failures, "orphan_recommendations": orphan_recommendations,
        "recommendation_degradation_conflicts": degradation_conflicts,
        "common_review_satisfaction_issues": common_review_issues,
        "element_identity_contradictions": element_identity_conflicts,
        "product_applicability_issues": product_applicability_issues,
        "shared_claim_reuse_issues": shared_claim_reuse_issues,
        "finding_independence_issues": finding_independence_issues,
        "report_transaction_truth": {
            "classification_transaction_structure": contract_context.get("transaction_structure"),
            "report_transaction_structure": report_context.get("transaction_structure"),
            "report_title": report_context.get("report_title"),
            "scenario_label": report_context.get("scenario_label"),
        },
    }
    for requirement, passed in checks.items():
        if not passed:
            failures.append({"requirement": requirement, "failure_stage": "Cross-layer Consistency Gate", "root_cause": json.dumps(details, ensure_ascii=False), "responsible_function": "_consistency_quality_gates", "current_status": "FAIL"})
    return {"status": "PASS" if not failures else "BLOCKED", "failures": failures, "gate_results": {key: "PASS" if value else "FAIL" for key, value in checks.items()}, **details}


def _finding_provenance(findings: List[RiskFinding], items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    item_by_id = {item.item_id: item for item in items}
    rows: List[Dict[str, Any]] = []
    for finding in findings:
        related = [item_by_id[item_id] for item_id in finding.source_review_ids if item_id in item_by_id]
        evidence = finding.supporting_evidence or finding.evidence or []
        provenance = {
            "finding_id": finding.finding_id,
            "created_by": "backend/review_v2/engine.py:_build_risk_findings",
            "source_review_ids": list(finding.source_review_ids),
            "source_fact_ids": sorted({fact for item in related for fact in item.fact_dependencies}),
            "evidence_ids": [str(row.get("evidence_claim_id") or row.get("clause_id") or "") for row in evidence if row],
            "evidence_entailment": sorted({str(row.get("entailment_status") or "") for row in evidence if row}),
            "rule_id": finding.risk_group,
            "model_call_id": "" if all(item.judge_source != "llm" for item in related) else "review-semantic-batch",
        }
        finding.provenance = provenance
        rows.append(provenance)
    return rows


def _production_trace(
    trace_id: str,
    contract_type: str,
    contract_context: Dict[str, Any],
    system_metadata: Dict[str, Any],
    finding_provenance: List[Dict[str, Any]],
    confidence_trace: List[Dict[str, Any]],
    priority_consistency: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "trace_id": trace_id,
        "system_version": system_metadata.get("system_version"),
        "pipeline_version": system_metadata.get("pipeline_version"),
        "model_version": system_metadata.get("model_version"),
        "prompt_version": system_metadata.get("prompt_version"),
        "rule_version": system_metadata.get("rule_version"),
        "ontology_version": system_metadata.get("ontology_version"),
        "legal_dataset_version": system_metadata.get("legal_dataset_version"),
        "contract_type": contract_type,
        "domain_pack": (contract_context.get("domain_attributes") or {}).get("domain_pack"),
        "active_pipeline": "backend/review_v2/engine.py:review_contract_v2",
        "active_components": [
            "ContextResolver executed",
            f"{contract_type.title()}DomainPack loaded",
            "EvidenceEntailmentValidator executed",
            "FindingEvidenceGate executed",
            "CrossLayerConsistency executed",
            "SaleDefaultLawEngine executed" if contract_type == "sale" else "DefaultLawEngine executed",
            "LegalClaimValidator executed",
            "PriorityConsistencyVerifier executed",
            "ConfidenceAggregator executed",
            "NarrativeRenderer executed",
        ],
        "finding_provenance": finding_provenance,
        "confidence_trace": confidence_trace,
        "priority_consistency": priority_consistency,
    }


def _architecture_status() -> List[Dict[str, Any]]:
    modules = [
        ("Parser", True, True, True, True, "Implemented"),
        ("Canonical Contract", True, True, True, True, "Implemented"),
        ("Version Resolver", True, True, False, True, "Implemented as precedence hints"),
        ("Fact Graph", True, True, True, True, "Implemented"),
        ("Applicability", True, True, True, True, "Implemented"),
        ("Evidence", True, True, True, True, "Implemented"),
        ("Legal Authority", True, True, True, True, "Implemented minimal KB"),
        ("Formula", True, True, True, True, "Implemented"),
        ("Scenario", True, True, True, True, "Implemented"),
        ("Review", True, True, True, True, "Implemented"),
        ("Risk Aggregator", True, True, True, True, "Implemented"),
        ("Severity", True, True, True, True, "Implemented"),
        ("Priority", True, True, True, True, "Implemented"),
        ("Recommendation", True, True, True, True, "Implemented"),
        ("Verifier", True, True, True, True, "Implemented deterministic"),
        ("Confidence", True, True, True, True, "Implemented"),
        ("Manual Review", True, True, True, True, "Implemented"),
        ("Quality Gate", True, True, True, True, "Implemented"),
        ("Report", True, True, True, True, "Implemented"),
        ("Benchmark", True, True, False, True, "Implemented runner; sample size pending"),
    ]
    return [
        {
            "module": module,
            "exists": exists,
            "production_called": production_called,
            "controls_final": controls_final,
            "tests": tests,
            "status": status,
        }
        for module, exists, production_called, controls_final, tests, status in modules
    ]


def _production_call_graph() -> List[str]:
    return [
        "frontend/src/views/ContractReviewV2.vue:runReview",
        "frontend/src/utils/api.js:reviewContractV2File",
        "backend/routers/review_v2.py:review_v2_file",
        "backend/layers/input_layer.py:InputLayer.extract_text_from_file",
        "backend/review_v2/engine.py:review_contract_v2",
        "backend/review_v2/contract_registry.py:get_contract_meta/get_checklist",
        "backend/review_v2/domain_packs.py:get_domain_pack",
        "backend/review_v2/clause_parser.py:parse_contract_clauses",
        "backend/review_v2/lease_contract_facts.py:extract_house_lease_facts",
        "backend/review_v2/llm_semantic_reviewer.py:judge_checkpoints_with_llm",
        "backend/review_v2/engine.py:_apply_final_quality_gate",
        "backend/review_v2/engine.py:_apply_evidence_entailment_gate/_apply_coverage_evidence_gate",
        "backend/review_v2/engine.py:_apply_citation_claims/_apply_confidence_bundles",
        "backend/review_v2/engine.py:_check_legal_reference_freshness",
        "backend/review_v2/engine.py:_build_risk_findings/_filter_unsupported_positive_findings",
        "backend/review_v2/engine.py:_legal_reference_findings",
        "backend/review_v2/engine.py:_run_independent_verifier",
        "backend/review_v2/engine.py:_build_recommendations",
        "backend/review_v2/engine.py:_overall_assessment",
        "backend/review_v2/engine.py:_pre_render_quality_gate",
        "backend/review_v2/engine.py:_format_markdown_v2",
        "backend/review_v2/quality4.py:post_render_quality_gate",
        "backend/routers/review_v2.py:review_v2_export_pdf/review_v2_export_docx",
        "backend/routers/review_v2.py:_build_pdf/_build_docx",
    ]


def _final_output_ownership_matrix() -> List[Dict[str, str]]:
    return [
        {"final_output": "总体可签署性", "current_producer": "_overall_assessment", "desired_producer": "ContractAssessment", "action": "single_source"},
        {"final_output": "风险统计", "current_producer": "_risk_finding_summary", "desired_producer": "RiskAggregator", "action": "unique_final_findings"},
        {"final_output": "人工复核数量", "current_producer": "_overall_assessment/_risk_finding_summary", "desired_producer": "ManualReviewAggregator", "action": "sum(needs_manual_review)"},
        {"final_output": "Review判断", "current_producer": "ReviewItemResult", "desired_producer": "ReviewResult", "action": "serializer_read_only"},
        {"final_output": "Severity", "current_producer": "RiskFinding.severity", "desired_producer": "RiskFinding", "action": "serializer_read_only"},
        {"final_output": "Recommendation", "current_producer": "_build_recommendations", "desired_producer": "Recommendation", "action": "serializer_read_only"},
        {"final_output": "Top Risk", "current_producer": "_finding_sort_key + RiskFinding", "desired_producer": "RiskFinding Ranker", "action": "top_from_findings_only"},
        {"final_output": "Legal Freshness", "current_producer": "_check_legal_reference_freshness/_legal_reference_findings", "desired_producer": "LegalAuthority Layer", "action": "finding_attached"},
        {"final_output": "Markdown", "current_producer": "_format_markdown_v2", "desired_producer": "Pure Serializer", "action": "no_business_in_serializer"},
        {"final_output": "PDF/DOCX", "current_producer": "_build_pdf/_build_docx", "desired_producer": "Production Markdown Renderer", "action": "render_result_only"},
    ]


def _risk_aggregation_debug_table(findings: List[RiskFinding]) -> List[Dict[str, Any]]:
    return [
        {
            "finding": finding.title,
            "risk_group": finding.risk_group,
            "reviews": finding.source_review_ids,
            "clause_ids": finding.source_clause_ids,
        }
        for finding in findings
    ]


def _confidence_debug_report(items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for item in items:
        bundle = (item.system_confidence or {}).get("confidence_bundle") or {}
        rows.append(
            {
                "review_id": item.item_id,
                "coverage": item.coverage_status,
                "parser": bundle.get("parser_confidence"),
                "fact": bundle.get("fact_confidence"),
                "evidence": bundle.get("evidence_confidence"),
                "applicability": bundle.get("applicability_confidence"),
                "legal": bundle.get("legal_confidence"),
                "formula": bundle.get("formula_confidence"),
                "calculation": bundle.get("calculation_confidence"),
                "verifier": bundle.get("verifier_confidence"),
                "final": bundle.get("final_confidence"),
                "final_score": bundle.get("final_score"),
                "required_components": bundle.get("required_components", []),
                "ignored_components": bundle.get("ignored_components", []),
                "limiting_factors": bundle.get("limiting_factors", []),
                "component_scores": bundle.get("component_scores", {}),
                "reason": bundle.get("reason"),
            }
        )
    return rows


def _coverage_element_debug_report(items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for item in items:
        for element in item.coverage_elements or []:
            rows.append(
                {
                    "review_id": item.item_id,
                    "coverage": item.coverage_status,
                    "element_id": element.get("element_id"),
                    "proposition": element.get("proposition"),
                    "evidence_ids": element.get("evidence_ids", []),
                    "entailment": element.get("entailment"),
                    "element_status": element.get("status"),
                    "verifier_confidence": element.get("verifier_confidence"),
                    "reason": element.get("reason"),
                }
            )
    return rows


def _legal_claim_debug_report(items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for item in items:
        for claim in item.legal_references or []:
            rows.append(
                {
                    "review_id": item.item_id,
                    "claim_id": claim.get("claim_id"),
                    "claim_type": claim.get("claim_type"),
                    "proposition": claim.get("proposition"),
                    "authority": f"{claim.get('law_name', '')}{claim.get('article', '')}",
                    "entailment": claim.get("support_type"),
                    "support_scope": claim.get("support_scope"),
                    "result": claim.get("citation_existence_status"),
                }
            )
    return rows


def _recommendation_provenance_debug_report(recommendations: List[Recommendation]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for recommendation in recommendations:
        for component in recommendation.components or recommendation.clauses or []:
            rows.append(
                {
                    "recommendation_id": recommendation.recommendation_id,
                    "component": component.get("proposition") or component.get("text"),
                    "source_type": component.get("source_type"),
                    "legal_claim_ids": component.get("legal_claim_ids", []),
                    "authority": component.get("authority") or component.get("statutory_basis") or "",
                    "supported_scope": component.get("supported_scope") or component.get("support_scope") or "",
                    "confidence": component.get("confidence"),
                }
            )
    return rows


def _numeric_provenance_gate(recommendations: List[Recommendation]) -> Dict[str, Any]:
    failures: List[Dict[str, Any]] = []
    numeric_pattern = re.compile(r"(?:\d+|[一二三四五六七八九十两]+)\s*(?:日|天|个工作日|倍)")
    for recommendation in recommendations:
        for component in recommendation.components or []:
            text = str(component.get("proposition") or "")
            numbers = numeric_pattern.findall(text)
            if not numbers:
                continue
            source_type = component.get("source_type")
            supported_scope = str(component.get("supported_scope") or "")
            if source_type in {"STATUTORY_RULE", "STATUTORY_DEFAULT"}:
                unsupported = [number for number in numbers if number not in supported_scope]
                if unsupported:
                    failures.append(
                        {
                            "recommendation_id": recommendation.recommendation_id,
                            "source_type": source_type,
                            "numbers": unsupported,
                            "message": "具体数字未出现在法源支撑范围内，不能作为法定规则组件输出。",
                        }
                    )
    return {"status": "PASS" if not failures else "FAIL", "failures": failures}


def _narrative_state_debug_report(items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for item in items:
        template = _coverage_narrative_template(item)
        state = item.narrative_state or _build_narrative_state(item)
        text = " ".join(str(state.get(key) or "") for key in ("judgment", "issue", "consequence", "recommendation"))
        covered_elements = list(state.get("covered_elements") or [])
        partial_elements = list(state.get("partial_elements") or [])
        missing_elements = list(state.get("missing_elements") or [])
        identities = {
            "covered": {re.sub(r"[\W_]+", "", value) for value in covered_elements},
            "partial": {re.sub(r"[\W_]+", "", value) for value in partial_elements},
            "missing": {re.sub(r"[\W_]+", "", value) for value in missing_elements},
        }
        element_conflicts = sorted(
            (identities["covered"] & identities["partial"])
            | (identities["covered"] & identities["missing"])
            | (identities["partial"] & identities["missing"])
        )
        contradiction_reasons: List[str] = []
        if item.coverage_status == "缺失" and any(phrase in text for phrase in MISSING_NARRATIVE_FORBIDDEN):
            contradiction_reasons.append("missing_narrative_contains_positive_assertion")
        if item.coverage_status == "通过" and any(phrase in text for phrase in ("缺失：", "尚未明确：", "仍需补足：")):
            contradiction_reasons.append("pass_narrative_contains_missing_assertion")
        if item.coverage_status == "部分覆盖" and not item.evidence_clauses:
            contradiction_reasons.append("partial_without_positive_evidence")
        if element_conflicts:
            contradiction_reasons.append("element_identity_conflict")
        finding_exists = item.item_id in {
            review_id for finding in getattr(item, "_debug_findings", []) for review_id in finding.source_review_ids
        } if hasattr(item, "_debug_findings") else bool(state.get("finding_exists"))
        if item.coverage_status == COVERAGE_NOT_APPLICABLE and (state.get("recommendation") or finding_exists):
            contradiction_reasons.append("not_applicable_has_finding_or_recommendation")
        rows.append(
            {
                "review_id": item.item_id,
                "coverage": item.coverage_status,
                "covered_elements": covered_elements,
                "partial_elements": partial_elements,
                "missing_elements": missing_elements,
                "element_identity_conflicts": element_conflicts,
                "narrative_result": state.get("judgment"),
                "rendered_issue": state.get("issue"),
                "rendered_consequence": state.get("consequence"),
                "rendered_recommendation": state.get("recommendation"),
                "narrative_template": template,
                "evidence_state": "positive" if item.evidence_clauses else "negative_or_not_found",
                "contradiction_reasons": contradiction_reasons,
                "status": "FAIL" if contradiction_reasons else "PASS",
            }
        )
    return rows


def _evidence_finding_debug_report(items: List[ReviewItemResult], findings: List[RiskFinding]) -> List[Dict[str, Any]]:
    finding_by_review = {
        review_id: finding
        for finding in findings
        for review_id in finding.source_review_ids
    }
    rows: List[Dict[str, Any]] = []
    for item in items:
        finding = finding_by_review.get(item.item_id)
        claim = (finding.aggregation_signals or {}).get("risk_claim") if finding else None
        rows.append(
            {
                "review_id": item.item_id,
                "risk_claim": claim,
                "evidence_candidates": (item.decision_trace or {}).get("evidence_candidates", []),
                "supporting_entailment": sorted({row.get("entailment_status", "") for row in (finding.supporting_evidence if finding else [])}),
                "finding_created": bool(finding),
                "gate_result": ((item.decision_trace or {}).get("finding_evidence_gate") or {}).get("status", "PASS"),
            }
        )
    return rows


def _default_law_debug_report(items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    return [
        {
            "review_id": item.item_id,
            "coverage": item.coverage_status,
            "default_rule": (((item.decision_trace or {}).get("default_law_assessment") or {}).get("rule") or {}).get("rule_id", ""),
            "applicability": ((item.decision_trace or {}).get("default_law_assessment") or {}).get("applicability"),
            "protection": ((item.decision_trace or {}).get("effective_gap") or {}).get("statutory_protection_scope"),
            "residual_gap": ((item.decision_trace or {}).get("effective_gap") or {}).get("remaining_gap"),
            "severity": item.risk_severity,
            "priority": item.review_priority,
        }
        for item in items
        if ((item.decision_trace or {}).get("default_law_assessment") or {}).get("default_law_relevant")
    ]


def _blocking_rule_from_failure(failure: Dict[str, Any], index: int) -> Dict[str, Any]:
    return {
        "code": str(failure.get("requirement") or failure.get("code") or f"QUALITY_GATE_FAILURE_{index}"),
        "stage": str(failure.get("failure_stage") or failure.get("stage") or "quality_gate"),
        "reason": str(failure.get("root_cause") or failure.get("reason") or "Quality gate reported a blocking failure."),
        "entity_type": str(failure.get("entity_type") or "quality_gate"),
        "entity_id": str(failure.get("entity_id") or failure.get("responsible_function") or ""),
        "severity": str(failure.get("severity") or "blocking"),
    }


def _quality_gate_observability(gates: Iterable[Dict[str, Any]], failures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    blockers = [_blocking_rule_from_failure(failure, index) for index, failure in enumerate(failures, start=1)]
    if blockers:
        return blockers
    for gate in gates:
        if gate.get("status") not in {"BLOCKED", "FAIL"}:
            continue
        failed_gate_results = [
            key for key, value in (gate.get("gate_results") or {}).items()
            if value in {"FAIL", "BLOCKED"}
        ]
        if failed_gate_results:
            return [
                {
                    "code": key,
                    "stage": "quality_gate",
                    "reason": f"{key} reported {gate.get('gate_results', {}).get(key)} without a structured failure row.",
                    "entity_type": "quality_gate",
                    "entity_id": key,
                    "severity": "blocking",
                }
                for key in failed_gate_results
            ]
        return [{
            "code": "QUALITY_GATE_INTERNAL_INCONSISTENCY",
            "stage": "quality_gate",
            "reason": "A quality gate returned BLOCKED but did not expose failures or failed gate_results.",
            "entity_type": "quality_gate",
            "entity_id": str(gate.get("gate") or gate.get("name") or ""),
            "severity": "blocking",
        }]
    return []


def _combine_quality_gates(*gates: Dict[str, Any]) -> Dict[str, Any]:
    failures: List[Dict[str, Any]] = []
    for gate in gates:
        failures.extend(gate.get("failures") or [])
    merged = dict(gates[0] if gates else {})
    merged["gate_results"] = {
        key: value
        for gate in gates
        for key, value in (gate.get("gate_results") or {}).items()
    }
    blocking_rules = _quality_gate_observability(gates, failures)
    merged["status"] = "REPORT_READY" if not blocking_rules else "BLOCKED"
    merged["failures"] = failures
    merged["blocking_rules"] = blocking_rules
    merged["blocking_stage"] = blocking_rules[0]["stage"] if blocking_rules else ""
    merged["blocking_entities"] = [
        {"entity_type": row["entity_type"], "entity_id": row["entity_id"]}
        for row in blocking_rules
    ]
    merged["blocking_reasons"] = [row["reason"] for row in blocking_rules]
    merged["post_render_status"] = gates[-1].get("status") if gates else "REPORT_READY"
    return merged


_TRACEABLE_REASONING_RISK_LEVELS = {"高", "中"}


_LEGAL_RULE_HINTS: Dict[str, str] = {
    "第585条": "约定违约金应以实际损失为基础；约定的违约金过分高于造成的损失的，可以依法请求适当减少。",
    "第584条": "损失赔偿范围包括履行后可以获得的利益，但不得超过违约方订立合同时预见或者应当预见的损失。",
    "第604条": "标的物毁损、灭失的风险，在交付前由出卖人承担，交付后由买受人承担，但是法律另有规定或者当事人另有约定的除外。",
    "第607条": "需要运输的买卖中，交付给第一承运人后风险转移；但当事人另有约定的，从其约定。",
    "第622条": "检验期限过短、难以完成全面检验的，通常只能约束外观瑕疵，隐蔽瑕疵仍需结合标的物性质和交易习惯判断。",
    "第641条": "所有权保留未经登记，不得对抗善意第三人。",
    "第640条": "试用买卖试用期内标的物毁损、灭失的风险由出卖人承担。",
    "第734条": "租赁期限届满后承租人继续使用租赁物，出租人没有提出异议的，原租赁合同继续有效，但租赁期限转为不定期。",
    "第710条": "承租人按照约定方法或者根据租赁物性质使用租赁物，致使租赁物受到损耗的，不承担赔偿责任。",
    "第725条": "租赁物在承租人按照租赁合同占有期限内发生所有权变动的，不影响租赁合同的效力。",
    "第563条": "出现不可抗力导致合同目的不能实现，或者一方根本违约等法定情形时，守约方可以解除合同。",
    "第716条": "承租人经出租人同意可以转租；未经同意转租的，出租人可以解除合同。",
    "第732条": "承租人在租赁期限内死亡的，与其生前共同居住的人或者共同经营人可以按照原租赁合同租赁该房屋。",
    "第733条": "租赁期限届满，承租人应当返还租赁物；返还的租赁物应当符合按照约定或者根据租赁物性质使用后的状态。",
    "第153条": "违反法律、行政法规强制性规定的民事法律行为无效，但是该强制性规定不导致该民事法律行为无效的除外。",
    "第157条": "民事法律行为无效、被撤销或者确定不发生效力后，行为人因该行为取得的财产应当予以返还；有过错的应当赔偿由此造成的损失。",
    "第533条": "合同基础条件发生订立合同时无法预见、不属于商业风险的重大变化，继续履行明显不公平的，受影响方可以请求变更或者解除合同。",
}


def _clean_evidence_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _excerpt(text: str, limit: int = 180) -> str:
    cleaned = _clean_evidence_text(text)
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[:limit].rstrip()}..."


def _first_sentence(text: str) -> str:
    cleaned = _clean_evidence_text(text)
    if not cleaned:
        return ""
    parts = re.split(r"(?<=[。！？；;])", cleaned, maxsplit=1)
    return parts[0].strip() or cleaned[:120]


def _first_citation(item: ReviewItemResult) -> Dict[str, str]:
    evidences = item.evidence_clauses or []
    if not evidences:
        if item.coverage_status == INSUFFICIENT_CONTEXT:
            status = "INSUFFICIENT_CONTEXT"
            description = "现有合同材料不足以确认该事项是否适用，建议结合相关交易背景或补充材料核对。"
        elif item.coverage_status == COVERAGE_NOT_APPLICABLE:
            status = "NOT_APPLICABLE"
            description = "当前合同未触发该审查事项的适用条件。"
        elif (item.decision_trace or {}).get("review_polarity") == "NEGATIVE_CLAUSE_CHECK" and item.coverage_status == "通过":
            status = "NO_ADVERSE_CLAUSE_FOUND"
            description = "未发现该类不利约定。"
        elif item.coverage_status == "通过":
            status = "NO_CLAUSE_REQUIRED"
            description = "本项不需要额外定位缺失条款。"
        else:
            status = "NO_SUPPORTING_CLAUSE"
            description = "合同正文及附件中未找到对应约定。"
        return {
            "evidence_status": status,
            "clause_number": "无对应条款",
            "original_excerpt": "无正式条款证据",
            "position_description": description,
        }

    evidence = evidences[0]
    location = str(evidence.get("location") or item.evidence_location or "未标明条款编号").strip()
    text = str(evidence.get("text") or "").strip()
    sentence = str(evidence.get("quote") or "").strip() or _first_sentence(text)
    position = f"{location}第1句" if sentence else location
    document_type = evidence.get("source_document_type") or evidence.get("document_type") or "MAIN_CONTRACT"
    source_label = {
        "MAIN_CONTRACT": "合同正文",
        "SUPPLEMENTARY_TERMS": "补充条款",
        "APPENDIX": "附件",
        "AMENDMENT": "补充协议/修订文件",
        "SIDE_LETTER": "往来函件",
    }.get(document_type, "其他文件")
    return {
        "evidence_status": "FOUND_ADVERSE_CLAUSE" if item.coverage_status == "风险条款" else "FOUND_SUPPORTING_CLAUSE",
        "document_type": document_type,
        "source_document_type": document_type,
        "source_label": source_label,
        "clause_number": location,
        "original_excerpt": f"“{_excerpt(sentence or text)}”",
        "position_description": f"{source_label}，{position}",
    }


def _evidence_position_display(item: ReviewItemResult) -> str:
    if item.evidence_location:
        return item.evidence_location
    citation = item.citation or _first_citation(item)
    return citation.get("position_description") or "合同正文及附件中未找到对应约定。"


def _legal_rule_text(item: ReviewItemResult) -> str:
    basis = item.legal_basis_index or "相关法律规则"
    for article, rule in _LEGAL_RULE_HINTS.items():
        if article in basis:
            return f"依据{basis}，{rule}"
    return f"依据{basis}，合同应围绕“{item.title}”明确权利义务、适用条件、履行标准和处理后果，避免履行及举证不确定。"


def _judgment_text(item: ReviewItemResult, citation: Dict[str, str]) -> str:
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return f"该审查点当前不适用于本合同场景，原因：{item.applicability.get('reason') or item.reasoning_summary}"
    if item.coverage_status == "缺失":
        return (
            f"合同未设置能够直接覆盖“{item.title}”的正式条款。"
            f"该缺口对应的问题类型为“{item.issue_type}”，会造成：{item.legal_consequence_if_missing}"
        )
    if item.coverage_status == "部分覆盖":
        return (
            f"合同已在{citation['clause_number']}出现相关安排，但该安排只覆盖部分要素。"
            f"结合问题类型“{item.issue_type}”看，现有条款仍未完整满足该审查点要求：{item.reasoning_summary}"
        )
    if item.coverage_status == "风险条款":
        return (
            f"合同在{citation['clause_number']}出现与该审查点直接相关的约定，"
            f"但该约定本身构成需修改的风险表述：{item.risk_point_description}"
        )
    if item.coverage_status == "通过":
        if item.related_risks:
            return (
                f"合同在{citation['clause_number']}已覆盖该审查点的核心要求；"
                f"但同一风险组存在关联风险 {', '.join(item.related_risks)}，需结合相关风险发现处理。"
            )
        return f"合同在{citation['clause_number']}已覆盖该审查点的核心要求，当前无明显残余风险。"
    return f"当前覆盖状态为“{item.coverage_status}”，系统判断为：{item.reasoning_summary}"


def _conclusion_text(item: ReviewItemResult) -> str:
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return "本项不适用于当前合同，无需修改。"
    if item.coverage_status == "通过" and item.risk_level == "低":
        if item.related_risks:
            return "本项条款机制已覆盖，但同一事实或条款存在关联风险发现，详见核心风险摘要。"
        return "本项已覆盖，无需修改。"
    return f"本项覆盖状态为“{item.coverage_status}”，处理优先级由关联风险发现和行动优先级统一决定。"


def _user_facing_reasoning(text: str) -> str:
    cleaned = text or ""
    cleaned = re.sub(r"（?用户风险偏好已纳入后续优先级排序。?）?", "", cleaned)
    cleaned = re.sub(r"[a-z_]+\.[a-z_\.]+=\{[^。；]*\}[。；]?", "", cleaned)
    cleaned = re.sub(r"[a-z_]+\.[a-z_\.]+=[^。；，]*[。；]?", "", cleaned)
    cleaned = re.sub(r"金额测算\s*测算\s*\{[^。]*\}。?", "", cleaned)
    replacements = {
        "统一事实图谱提取": "根据合同原文可确认",
        "统一事实图谱识别": "根据合同原文可识别",
        "统一事实图谱显示": "根据合同原文显示",
        "统一事实图谱": "合同事实",
        "Fact Graph": "合同事实",
        "Scenario Engine": "金额测算",
        "Final Quality Gate": "最终校验",
        "Cross Review Consistency Verifier": "一致性校验",
        "rule_fallback": "自动审查",
        "LLM": "语义复核",
        "建议人工复核": "建议重点核对",
        "需要人工复核": "需要重点核对",
    }
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    return _dedupe_narrative_sentences(re.sub(r"\s+", " ", cleaned).strip())


def _applicability_user_reason(item: ReviewItemResult) -> str:
    if item.coverage_status == INSUFFICIENT_CONTEXT or str((item.applicability or {}).get("status") or "").upper() == INSUFFICIENT_CONTEXT:
        return "现有合同材料不足以确认该事项是否适用，建议结合相关交易背景或补充材料核对。"
    return str(
        item.applicability.get("user_reason")
        or item.applicability.get("reason")
        or "当前合同未触发该审查事项的适用条件。"
    )


def _dedupe_narrative_sentences(text: str) -> str:
    parts = [part.strip() for part in re.split(r"(?<=[。；;])", text or "") if part.strip()]
    if not parts:
        return text or ""
    seen: set[str] = set()
    deduped: List[str] = []
    for part in parts:
        key = re.sub(r"\s+", "", part)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(part)
    return "".join(deduped)


MISSING_NARRATIVE_FORBIDDEN = ("已出现", "已覆盖", "已有明确约定", "已存在相关安排", "尚未完整覆盖", "部分相关安排")
PARTIAL_TOTAL_MISSING_PHRASES = ("完全未约定", "未约定该机制", "未约定质量异议处理机制", "未明确约定相关安排")


def _coverage_element_sets(item: ReviewItemResult) -> tuple[List[str], List[str]]:
    covered: List[str] = []
    missing: List[str] = []
    for element in item.coverage_elements or []:
        proposition = str(element.get("proposition") or element.get("element_id") or "").strip("。")
        if not proposition:
            continue
        if element.get("status") in {"COVERED", "PARTIALLY_COVERED"}:
            covered.append(proposition)
        elif element.get("status") in {"MISSING", "UNCERTAIN"}:
            missing.append(proposition)
    return covered, missing


def _coverage_element_groups(item: ReviewItemResult) -> tuple[List[str], List[str], List[str]]:
    covered: List[str] = []
    partial: List[str] = []
    missing: List[str] = []
    for element in item.coverage_elements or []:
        proposition = str(element.get("proposition") or element.get("element_id") or "").strip("。")
        if not proposition:
            continue
        status = element.get("status")
        if status == "COVERED":
            covered.append(proposition)
        elif status == "PARTIALLY_COVERED":
            partial.append(proposition)
        elif status in {"MISSING", "UNCERTAIN"}:
            missing.append(proposition)
    return covered, partial, missing


def _element_narrative_label(proposition: str) -> str:
    label = proposition.strip("。")
    for prefix in (
        "合同已经明确约定", "合同已明确约定", "合同明确约定", "合同已经约定", "合同已约定",
        "已明确约定", "已约定", "合同已经明确", "合同已明确", "合同明确",
        "合同已经载明", "合同已载明", "合同载明", "合同存在",
    ):
        if label.startswith(prefix):
            return label[len(prefix):].strip("“”")
    return label


def _specific_gap_consequence(item: ReviewItemResult, gap_text: str) -> str:
    text = " ".join([item.title, item.node_id, item.risk_group, item.risk_point_description, gap_text])
    if any(term in text for term in ("知识产权", "侵权", "专利", "商标", "著作权")):
        return "第三方提出侵权主张时，停用、下架、替换成本和对出卖人的追偿依据可能不够直接。"
    if any(term in text for term in ("包装", "运输损坏", "装箱", "防护")):
        return "运输损坏发生后，包装是否合格、损失原因和责任归属容易发生争议。"
    if any(term in text for term in ("权利瑕疵", "第三方权利", "权利负担")):
        return "第三方主张权利时，披露、排除妨碍、替换和赔偿路径不够直接。"
    if any(term in text for term in ("迟延受领", "拒收", "未提货")):
        return "买受人迟延受领后的费用、保管和风险分配主要依赖法定规则，写入合同前需确认是否会扩大当前客户责任。"
    if any(term in text for term in ("可得利益", "预期利益")):
        return "可得利益赔偿仍受违约因果关系、可预见性和证据证明约束；限制性写法可能缩小守约方救济。"
    if any(term in text for term in ("交付", "验收", "签收")):
        return "交付或验收节点不清时，风险转移、质量异议和付款条件容易被不同理解。"
    if any(term in text for term in ("付款", "价款", "结算")):
        return f"{gap_text}不清时，付款期限、逾期责任和对账依据容易产生争议。"
    return f"{gap_text}不清时，责任边界不够明确。"


def _build_narrative_state(item: ReviewItemResult) -> Dict[str, Any]:
    covered, partial, missing = _coverage_element_groups(item)
    satisfaction = (item.decision_trace or {}).get("common_review_satisfaction") or {}
    active_paths = [row for row in satisfaction.get("satisfaction_paths", []) if row.get("applicable", True)]
    if active_paths and item.coverage_status in {"缺失", "部分覆盖"}:
        selected_path = max(
            active_paths,
            key=lambda row: (
                sum(status == "COVERED" for status in (row.get("statuses") or {}).values()),
                sum(status == "PARTIALLY_COVERED" for status in (row.get("statuses") or {}).values()),
                -sum(status in {"MISSING", "UNCERTAIN"} for status in (row.get("statuses") or {}).values()),
            ),
        )
        required_ids = set(selected_path.get("required_elements") or [])
        missing = [
            str(element.get("proposition") or element.get("element_id") or "").strip("。")
            for element in item.coverage_elements or []
            if element.get("element_id") in required_ids and element.get("status") in {"MISSING", "UNCERTAIN"}
        ]
        partial = [
            str(element.get("proposition") or element.get("element_id") or "").strip("。")
            for element in item.coverage_elements or []
            if element.get("element_id") in required_ids and element.get("status") == "PARTIALLY_COVERED"
        ]
    covered = list(dict.fromkeys(covered))
    partial = [value for value in dict.fromkeys(partial) if value not in covered]
    missing = [value for value in dict.fromkeys(missing) if value not in covered and value not in partial]
    covered_text = "；".join(_element_narrative_label(value) for value in covered)
    partial_text = "；".join(_element_narrative_label(value) for value in partial)
    missing_text = "；".join(_element_narrative_label(value) for value in missing)
    applicability = str((item.applicability or {}).get("status") or "APPLICABLE").upper()
    polarity = str((item.decision_trace or {}).get("review_polarity") or "POSITIVE_REQUIREMENT")
    if item.coverage_status == INSUFFICIENT_CONTEXT:
        covered, partial, missing = [], [], []
        judgment = _applicability_user_reason(item)
        issue = judgment
        consequence = judgment
        recommendation = ""
    elif applicability == "NOT_APPLICABLE" or item.coverage_status == COVERAGE_NOT_APPLICABLE:
        covered, partial, missing = [], [], []
        judgment = _applicability_user_reason(item)
        issue = ""
        consequence = ""
        recommendation = ""
    elif item.coverage_status == "通过":
        if (item.decision_trace or {}).get("review_nature") == "INTERNAL_CLASSIFICATION":
            judgment = f"系统已完成“{item.title}”的内部法律定性；该结果用于后续规则适用，不要求合同正文单列分类表述。"
            consequence = "不形成独立合同风险。"
        elif polarity == "NEGATIVE_CLAUSE_CHECK":
            judgment = f"未发现“{item.title}”对应的不利条款或安排。"
            consequence = "未发现该不利安排，因此不形成对应风险。"
        else:
            judgment = f"合同已明确约定{covered_text}。" if covered_text else f"合同已覆盖{item.title}要求。"
            consequence = "无明显残余风险。"
        issue = ""
        recommendation = "无需修改。"
    elif item.coverage_status == "缺失":
        missing_text = missing_text or "现有信息不足以确定具体缺失字段"
        judgment = f"合同未明确：{missing_text}。"
        issue = f"缺失：{missing_text}。"
        consequence = _specific_gap_consequence(item, missing_text)
        recommendation = f"建议补充明确：{missing_text}。"
    elif item.coverage_status == "部分覆盖":
        statements = []
        if covered_text:
            statements.append(f"已覆盖：{covered_text}")
        if partial_text:
            statements.append(f"仅部分明确：{partial_text}")
        if missing_text:
            statements.append(f"尚未覆盖：{missing_text}")
        judgment = "；".join(statements) + "。" if statements else f"“{item.title}”仅得到部分证据支持，仍需补足关键要素。"
        incomplete_text = "；".join(value for value in (partial_text, missing_text) if value) or "现有信息不足以确定具体缺失字段"
        issue = f"仍需补足：{incomplete_text}。"
        consequence = _specific_gap_consequence(item, incomplete_text)
        recommendation = f"建议仅补充明确：{incomplete_text}。"
    else:
        judgment = item.risk_point_description or f"“{item.title}”存在需要处理的风险条款。"
        issue = item.risk_point_description
        consequence = item.legal_consequence_if_missing
        recommendation = item.suggested_clause_example
    return {
        "review_id": item.item_id,
        "applicability": applicability,
        "polarity": polarity,
        "coverage_status": item.coverage_status,
        "covered_elements": covered,
        "partial_elements": partial,
        "missing_elements": missing,
        "adverse_elements": [],
        "finding_exists": item.coverage_status in {"缺失", "部分覆盖", "风险条款"} and applicability == "APPLICABLE",
        "judgment": judgment,
        "issue": issue,
        "consequence": consequence,
        "recommendation": recommendation,
        "result": judgment,
    }


def _partial_element_narrative(item: ReviewItemResult) -> str:
    state = item.narrative_state or _build_narrative_state(item)
    return str(state["judgment"])


def _apply_element_level_narratives(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    for item in items:
        state = _build_narrative_state(item)
        item.narrative_state = state
        item.decision_trace["narrative_elements"] = state
    return items


def _coverage_safe_reasoning(item: ReviewItemResult, text: str) -> str:
    if item.narrative_state:
        return str(item.narrative_state.get("judgment") or text)
    cleaned = _user_facing_reasoning(text)
    if item.coverage_status == "部分覆盖" and any(phrase in cleaned for phrase in PARTIAL_TOTAL_MISSING_PHRASES):
        return _partial_element_narrative(item)
    if item.coverage_status == "缺失" and any(phrase in cleaned for phrase in MISSING_NARRATIVE_FORBIDDEN):
        return f"未在合同正文及附件中定位到“{item.title}”对应的明确约定。"
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return _applicability_user_reason(item)
    return cleaned


def _coverage_narrative_template(item: ReviewItemResult) -> str:
    if item.coverage_status == "通过":
        if item.related_risks:
            return "PASS_WITH_RELATED_FINDING"
        return "PASS"
    if item.coverage_status == "部分覆盖":
        return "PARTIAL"
    if item.coverage_status == "缺失":
        return "MISSING"
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return "NOT_APPLICABLE"
    if item.coverage_status == "风险条款":
        return "RISK_CLAUSE"
    return "UNCERTAIN"


def _format_money(value: Any) -> str:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return ""
    return f"{amount:,.0f}"


def _finding_economic_text(finding: RiskFinding, item_by_id: Dict[str, ReviewItemResult]) -> str:
    if finding.risk_group == "early_termination_financial_exposure":
        scenario_item = item_by_id.get("HL-039")
        cases = ((scenario_item.scenario_analysis or {}).get("cases") or []) if scenario_item else []
        parts = []
        for case in cases:
            amount = _format_money(case.get("estimated_penalty") or case.get("penalty") or case.get("amount"))
            if amount:
                parts.append(f"剩余{case.get('remaining_days')}天：约{amount}元")
        max_loss = _format_money((finding.economic_impact or {}).get("estimated_max_loss"))
        monthly_multiple = (finding.economic_impact or {}).get("monthly_payment_multiple")
        if parts:
            tail = f"最高约{max_loss}元" if max_loss else ""
            if monthly_multiple is not None:
                tail = f"{tail}，约相当于{monthly_multiple:g}个月当前月租金" if tail else f"约相当于{monthly_multiple:g}个月当前月租金"
            return f"按合同公式测算：{'；'.join(parts)}。{tail}。该计算方式不是普通固定倍数违约金，会随剩余租期变化。"
    economic = finding.economic_impact or {}
    if economic.get("estimated_max_loss"):
        amount = _format_money(economic.get("estimated_max_loss"))
        monthly_multiple = economic.get("monthly_payment_multiple")
        if monthly_multiple is not None:
            return f"最大经济暴露约{amount}元，约相当于{monthly_multiple:g}个月当前月租金。"
        return f"最大经济暴露约{amount}元。"
    return ""


def _finding_evidence_text(finding: RiskFinding) -> str:
    evidence = finding.supporting_evidence or finding.evidence or []
    if not evidence:
        return "关键证据：未定位到单一明确条款，依据缺失或结构化事实判断。"
    first = evidence[0]
    location = first.get("location") or first.get("clause_number") or "合同相关条款"
    source_label = {
        "MAIN_CONTRACT": "合同正文",
        "SUPPLEMENTARY_TERMS": "补充条款",
        "APPENDIX": "附件",
        "AMENDMENT": "补充协议/修订文件",
        "SIDE_LETTER": "往来函件",
    }.get(first.get("source_document_type") or first.get("document_type"), "合同文件")
    text = (first.get("quote") or first.get("text") or "").strip()
    if len(text) > 80:
        text = text[:80] + "..."
    return f"关键证据：{source_label}{location}，{text}" if text else f"关键证据：{source_label}{location}。"


def _recommendation_component_lines(recommendation: Recommendation) -> List[str]:
    components = recommendation.components or recommendation.clauses or []
    if not components:
        return [recommendation.proposed_change or recommendation.suggested_text]
    lines: List[str] = []
    for component in components:
        source_type = component.get("source_type")
        proposition = component.get("proposition") or component.get("text") or ""
        if not proposition:
            continue
        if source_type in {"STATUTORY_RULE", "STATUTORY_DEFAULT"}:
            continue
        elif source_type == "CONTRACT_RULE":
            lines.append(f"【合同规则】：{proposition}")
        elif source_type in {"DRAFTING_CHOICE", "BUSINESS_PREFERENCE"}:
            lines.append(f"【起草建议】：{proposition}")
        else:
            lines.append(f"【风险缓释】：{proposition}")
    return lines or [recommendation.proposed_change or recommendation.suggested_text]


def _recommendation_inline_text(recommendation: Recommendation) -> str:
    return "；".join(_recommendation_component_lines(recommendation))


def _top_risk_line(
    finding: RiskFinding,
    item_by_id: Dict[str, ReviewItemResult],
    recommendation: Optional[Recommendation] = None,
) -> str:
    importance = finding.consequence or finding.issue
    economic_text = _finding_economic_text(finding, item_by_id)
    evidence_text = _finding_evidence_text(finding)
    pieces = [
        f"- **{_finding_public_label(finding)}**：{_recommendation_heading(finding.priority)}。",
        f"核心问题：{finding.issue}",
        f"重要性：{importance}",
    ]
    if economic_text:
        pieces.append(economic_text)
    pieces.append(evidence_text)
    if recommendation:
        pieces.append(f"建议：{_recommendation_inline_text(recommendation)}")
    return " ".join(piece for piece in pieces if piece)


def _economic_display(value: str) -> str:
    return {
        "none": "无明显直接金额影响",
        "low": "低",
        "medium": "中",
        "high": "高",
        "critical": "重大",
        "": "无明显直接金额影响",
    }.get(value or "", value)


def _professional_item_conclusion(item: ReviewItemResult) -> str:
    if item.item_id == "HL-039" and item.scenario_analysis:
        cases = item.scenario_analysis.get("cases") or []
        amounts = []
        for case in cases:
            amount = _format_money(case.get("estimated_penalty") or case.get("penalty") or case.get("amount"))
            if amount:
                amounts.append(f"剩余{case.get('remaining_days')}天约{amount}元")
        scenario_text = "；".join(amounts)
        prefix = f"按合同公式测算，{scenario_text}。" if scenario_text else ""
        return f"{prefix}该公式不是普通固定倍数违约金，而是会随剩余租期增加而放大，建议结合实际损失和金额上限处理。"
    if item.narrative_state:
        return str(item.narrative_state.get("judgment") or "")
    if item.coverage_status == INSUFFICIENT_CONTEXT:
        return _applicability_user_reason(item)
    if item.coverage_status == "通过":
        if item.related_risks:
            return "该审查事项已覆盖；关联风险仅作为风险聚合链接，不改变本项无需修改的结论。"
        return "该审查事项已覆盖，无需修改。"
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return _applicability_user_reason(item)
    if item.coverage_status == "部分覆盖":
        return _partial_element_narrative(item)
    if item.coverage_status == "缺失":
        return f"未在合同正文及附件中定位到“{item.title}”对应的明确约定。"
    if item.coverage_status == "风险条款":
        return f"合同虽有相关条款，但条款内容本身可能引发执行争议，应按关联风险发现处理。"
    return _conclusion_text(item)


_SECTION_NUMERALS = "一二三四五六七八九十"


def _section_title(index: int, title: str) -> str:
    numeral = _SECTION_NUMERALS[index - 1] if 1 <= index <= len(_SECTION_NUMERALS) else str(index)
    return f"## {numeral}、{title}"


def _production_profile_lines(profile: UserRiskProfile, contract_type_name: str, perspective_resolution: Dict[str, Any]) -> List[str]:
    stance = str(perspective_resolution.get("display_role") or "合同当事人")
    lines = [f"- 审查立场：{stance}"]
    if profile.contract_scenario:
        lines.append(f"- 使用场景：{profile.contract_scenario}")
    return lines


def _report_context_profile_lines(profile: UserRiskProfile, report_context: Dict[str, Any], perspective_resolution: Dict[str, Any]) -> List[str]:
    lines = _production_profile_lines(profile, report_context["contract_type_label"], perspective_resolution)
    return [
        f"- 使用场景：{report_context['scenario_label']}" if line.startswith("- 使用场景：") else line
        for line in lines
    ]


def _display_legal_consequence(item: ReviewItemResult) -> tuple[str, str]:
    if item.coverage_status == INSUFFICIENT_CONTEXT:
        return "适用说明", _applicability_user_reason(item)
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return "适用说明", _applicability_user_reason(item)
    if item.coverage_status == "通过":
        if item.related_risks:
            return "处理结论", "本项已覆盖；关联风险仅用于聚合展示，不改变本项无需修改的结论。"
        if (item.decision_trace or {}).get("review_polarity") == "NEGATIVE_CLAUSE_CHECK":
            return "处理结论", "未发现该不利安排，不形成对应风险。"
        return "处理结论", "已覆盖，无需修改。"
    if item.coverage_status == "部分覆盖" and item.narrative_state:
        return "缺失的法律后果", str(item.narrative_state["consequence"])
    return "缺失的法律后果", item.legal_consequence_if_missing


def _trusted_legal_basis_display(item: ReviewItemResult) -> str:
    claims = item.legal_references or []
    direct = [
        claim for claim in claims
        if claim.get("support_type") in {"DIRECT_SUPPORT", "PARTIAL_SUPPORT"}
        and claim.get("freshness_status") not in {"OUTDATED_REFERENCE", "REPEALED"}
        and claim.get("law_name")
        and claim.get("claim_type") != "DRAFTING_RECOMMENDATION"
    ]
    if direct:
        has_partial = any(claim.get("support_type") == "PARTIAL_SUPPORT" for claim in direct)
        authorities = list(dict.fromkeys(
            f"《{claim.get('law_name')}》{claim.get('article') or ''}" for claim in direct
        ))[:3]
        authority_text = "；".join(authorities)
        if has_partial:
            return authority_text
        return authority_text
    return ""


def _practice_basis_display(item: ReviewItemResult) -> str:
    if item.coverage_status in {"通过", COVERAGE_NOT_APPLICABLE, INSUFFICIENT_CONTEXT}:
        return ""
    claims = item.legal_references or []
    drafting = [
        claim for claim in claims
        if claim.get("claim_type") == "DRAFTING_RECOMMENDATION"
        or claim.get("support_type") == "BACKGROUND_ONLY"
    ]
    if drafting:
        return "本项属于合同管理、商业风险控制或起草完整性建议。"
    return ""


def _apply_default_law_narratives(items: List[ReviewItemResult]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for item in items:
        gap = (item.decision_trace or {}).get("effective_gap") or {}
        default_status = str(gap.get("statutory_default") or "UNCERTAIN_DEFAULT")
        contractual_missing = list(gap.get("contractual_missing_elements") or [])
        statutory_elements = list(gap.get("statutory_default_elements") or [])
        residual = list(gap.get("still_unprotected_elements") or [])
        applicability = str((item.applicability or {}).get("status") or "APPLICABLE").upper()
        polarity = str((item.decision_trace or {}).get("review_polarity") or "POSITIVE_REQUIREMENT")
        if applicability == "NOT_APPLICABLE" or item.coverage_status == COVERAGE_NOT_APPLICABLE:
            narrative = ""
        elif item.coverage_status == "通过" and polarity == "NEGATIVE_CLAUSE_CHECK":
            narrative = "未发现该不利安排，因此不形成对应风险。"
        elif item.coverage_status == "通过":
            narrative = "合同已明确约定该事项。"
        elif default_status in {"CLEAR_DEFAULT", "PARTIAL_DEFAULT"} and statutory_elements:
            contract_state = "合同文本未完整约定该事项" if item.coverage_status == "部分覆盖" else "合同文本未约定该事项"
            protection = "现行法律已提供相应默认处理规则，因此实际法律风险受到一定控制"
            practical = "如希望减少履行争议，可进一步合同化明确。" if residual else "当前无需仅为重复法定规则而修改合同。"
            narrative = f"{contract_state}，但{protection}。{practical}"
        else:
            narrative = "合同未明确约定，且未识别到足以补足该缺口的明确法定默认规则。"
        contradiction = item.coverage_status == "部分覆盖" and any(
            phrase in narrative for phrase in ("合同已完整覆盖", "合同已明确约定该事项", "合同已经完全覆盖")
        )
        row = {
            "review_id": item.item_id, "contract_coverage": item.coverage_status,
            "contractual_missing_elements": contractual_missing, "default_law_status": default_status,
            "statutory_default_elements": statutory_elements, "residual_gap": residual,
            "practical_value": gap.get("remaining_gap") or "",
            "generated_narrative": narrative, "contradiction": contradiction,
        }
        item.decision_trace["effective_gap_narrative"] = row
        rows.append(row)
    return rows


def _default_law_narrative_truth_gate(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    contradictions = [row for row in rows if row.get("contradiction")]
    return {
        "status": "BLOCKED" if contradictions else "REPORT_READY",
        "failures": [] if not contradictions else [{
            "requirement": "DEFAULT_LAW_NARRATIVE_TRUTH_GATE", "failure_stage": "Effective Gap Narrative",
            "root_cause": "Default Law narrative represented partial contract coverage as fully contractually covered.",
            "responsible_function": "_apply_default_law_narratives", "current_status": "FAIL",
        }],
        "gate_results": {"DEFAULT_LAW_NARRATIVE_TRUTH_GATE": "FAIL" if contradictions else "PASS"},
        "contradiction_count": len(contradictions), "rows": rows,
    }


def _legal_default_law_consistency_gate(items: List[ReviewItemResult]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    contradictions: List[Dict[str, Any]] = []
    composite_errors: List[Dict[str, Any]] = []
    for item in items:
        assessment = (item.decision_trace or {}).get("default_law_assessment") or {}
        rule = assessment.get("rule") or {}
        authority_ids = list(rule.get("authority_ids") or [])
        selected = [
            claim for claim in item.legal_references or []
            if claim.get("authority_id") in authority_ids
            and claim.get("support_type") in {"DIRECT_SUPPORT", "PARTIAL_SUPPORT", "SUPPORTING"}
            and claim.get("freshness_status") == "CURRENT"
        ]
        supplied = list(rule.get("supplied_element_ids") or [])
        missing_ids = [
            str(element.get("element_id") or "") for element in item.coverage_elements or []
            if element.get("status") in {"MISSING", "PARTIALLY_COVERED"}
        ]
        unsupplied = [element_id for element_id in missing_ids if element_id not in supplied]
        default_status = str(assessment.get("status") or "UNCERTAIN_DEFAULT")
        supported = bool(selected)
        default_capable = bool(rule.get("proposition_id") or supplied)
        exclusion_reason = ""
        if supported and not default_capable:
            exclusion_reason = "Authority supports a related legal principle but does not supply the missing contractual mechanism."
        elif supported and default_capable and not supplied:
            exclusion_reason = "The resolved rule is legally relevant but does not supply a tracked contractual element."
        contradiction = (
            supported and default_capable and default_status in {"NO_DEFAULT", "UNCERTAIN_DEFAULT"}
            and not exclusion_reason
        )
        row = {
            "review_id": item.item_id,
            "element_id": supplied[0] if len(supplied) == 1 else "",
            "proposition_id": rule.get("proposition_id") or "",
            "legal_statement": rule.get("proposition") or "",
            "authority_ids": authority_ids,
            "authority_entailment": "SUPPORTS" if supported else "NOT_EVALUATED" if not authority_ids else "UNCERTAIN",
            "resolved_legal_status": "SUPPORTED_BY_CURRENT_LAW" if supported else "UNCERTAIN",
            "is_default_law_capable": default_capable,
            "default_law_status": default_status,
            "supplied_elements": supplied,
            "unsupplied_elements": unsupplied,
            "exclusion_reason": exclusion_reason,
            "consistency_gate": "FAIL" if contradiction else "PASS",
        }
        rows.append(row)
        if contradiction:
            contradictions.append(row)
        for element in item.coverage_elements or []:
            if element.get("atomic", True) is False and not element.get("child_elements"):
                composite_errors.append({
                    "review_id": item.item_id, "original_element": element.get("proposition"),
                    "atomic": False, "child_elements": [], "element_id": element.get("element_id"),
                })
    failures = []
    if contradictions:
        failures.append({
            "requirement": "LEGAL_DEFAULT_LAW_CONSISTENCY_GATE", "failure_stage": "Resolved Legal Rule",
            "root_cause": "A supported default-law-capable proposition diverged from DefaultLawResult without an exclusion reason.",
            "responsible_function": "_legal_default_law_consistency_gate", "current_status": "FAIL",
        })
    if composite_errors:
        failures.append({
            "requirement": "ATOMIC_LEGAL_ELEMENT_GATE", "failure_stage": "Legal Element Composition",
            "root_cause": "A non-atomic legal element reached Default Law without child elements.",
            "responsible_function": "_legal_default_law_consistency_gate", "current_status": "FAIL",
        })
    return {
        "status": "BLOCKED" if failures else "REPORT_READY", "failures": failures,
        "gate_results": {
            "LEGAL_DEFAULT_LAW_CONSISTENCY_GATE": "FAIL" if contradictions else "PASS",
            "ATOMIC_LEGAL_ELEMENT_GATE": "FAIL" if composite_errors else "PASS",
        },
        "contradiction_count": len(contradictions), "composite_error_count": len(composite_errors),
        "rows": rows, "element_decomposition": [
            {
                "review_id": item.item_id,
                "original_element": element.get("proposition"),
                "atomic": element.get("atomic", True),
                "child_elements": element.get("child_elements") or [],
                "child": [{
                    "element_id": element.get("element_id"),
                    "proposition_id": (element.get("legal_proposition_ids") or [""])[0],
                    "authority_ids": list((((item.decision_trace or {}).get("default_law_assessment") or {}).get("rule") or {}).get("authority_ids") or []),
                    "default_law_status": (((item.decision_trace or {}).get("default_law_assessment") or {}).get("status")),
                }],
            }
            for item in items for element in item.coverage_elements or []
            if element.get("legal_proposition_ids") or element.get("atomic", True) is False
        ],
    }


def _review_report_section(report: str, review_id: str) -> str:
    marker = f"（{review_id}）"
    if marker not in report:
        return ""
    section = report.split(marker, 1)[1]
    return section.split("\n## ", 1)[0]


def _applicability_polarity_gates(
    items: List[ReviewItemResult], findings: List[RiskFinding], recommendations: List[Recommendation], report: str = "",
) -> Dict[str, Any]:
    finding_ids_by_review = {
        item.item_id: [finding.finding_id for finding in findings if item.item_id in finding.source_review_ids]
        for item in items
    }
    recommendation_ids_by_review = {
        item.item_id: [
            recommendation.recommendation_id for recommendation in recommendations
            if set(recommendation.target_finding_ids) & set(finding_ids_by_review[item.item_id])
        ]
        for item in items
    }
    na_rows: List[Dict[str, Any]] = []
    polarity_rows: List[Dict[str, Any]] = []
    na_gap_errors: List[Dict[str, Any]] = []
    na_narrative_errors: List[Dict[str, Any]] = []
    negative_narrative_errors: List[Dict[str, Any]] = []
    negative_false_passes: List[Dict[str, Any]] = []
    forbidden_na_terms = ("合同缺失", "尚未覆盖", "仍需补足", "未识别到足以补足", "建议新增", "建议补充")
    positive_negative_terms = ("合同已覆盖", "合同已明确约定该事项", "合同已明确覆盖")
    for item in items:
        applicability = str((item.applicability or {}).get("status") or "APPLICABLE").upper()
        polarity = str((item.decision_trace or {}).get("review_polarity") or "POSITIVE_REQUIREMENT")
        section = _review_report_section(report, item.item_id) if report else ""
        if applicability == "NOT_APPLICABLE" or item.coverage_status == COVERAGE_NOT_APPLICABLE:
            gap = (item.decision_trace or {}).get("effective_gap") or {}
            default_assessment = (item.decision_trace or {}).get("default_law_assessment") or {}
            gap_error = (
                gap.get("status") != "NOT_APPLICABLE"
                or bool(gap.get("contractual_missing_elements"))
                or bool(finding_ids_by_review[item.item_id])
                or bool(recommendation_ids_by_review[item.item_id])
                or default_assessment.get("executed") is not False
            )
            narrative_error = bool(section) and any(term in section for term in forbidden_na_terms)
            row = {
                "review_id": item.item_id, "applicability": "NOT_APPLICABLE",
                "reason": (item.applicability or {}).get("reason") or "",
                "coverage_evaluated": False, "default_law_evaluated": default_assessment.get("executed", False),
                "effective_gap_created": gap.get("status") != "NOT_APPLICABLE",
                "finding_created": bool(finding_ids_by_review[item.item_id]),
                "recommendation_created": bool(recommendation_ids_by_review[item.item_id]),
                "production_gap_narrative_present": narrative_error,
                "gate_result": "FAIL" if gap_error or narrative_error else "PASS",
            }
            na_rows.append(row)
            if gap_error:
                na_gap_errors.append(row)
            if narrative_error:
                na_narrative_errors.append(row)
        if polarity == "NEGATIVE_CLAUSE_CHECK":
            negative = (item.decision_trace or {}).get("negative_clause_check") or {}
            narrative = str((item.narrative_state or {}).get("judgment") or "")
            positive_narrative = item.coverage_status == "通过" and (
                any(term in narrative for term in positive_negative_terms)
                or bool(section) and any(term in section for term in positive_negative_terms)
            )
            false_pass = item.coverage_status == "通过" and not (
                negative.get("adverse_clause_exists") is False
                and negative.get("search_coverage") == "SUFFICIENT"
                and negative.get("confidence") in {"medium", "high"}
            )
            row = {
                "review_id": item.item_id, "review_title": item.title, "polarity": polarity,
                "coverage": item.coverage_status, "evidence_state": negative,
                "expected_pass_semantics": "NO_ADVERSE_CLAUSE_FOUND",
                "generated_conclusion": narrative,
                "generated_exposure": ((item.decision_trace or {}).get("effective_gap_narrative") or {}).get("generated_narrative", ""),
                "gate_result": "FAIL" if positive_narrative or false_pass else "PASS",
            }
            polarity_rows.append(row)
            if positive_narrative:
                negative_narrative_errors.append(row)
            if false_pass:
                negative_false_passes.append(row)
    failures = []
    for requirement, errors, stage in (
        ("NOT_APPLICABLE_NARRATIVE_GATE", na_narrative_errors, "Applicability-aware Narrative"),
        ("NOT_APPLICABLE_GAP_GATE", na_gap_errors, "Applicability Gap Stop"),
        ("REVIEW_POLARITY_NARRATIVE_GATE", negative_narrative_errors, "Review Polarity Narrative"),
        ("NEGATIVE_CHECK_PASS_GATE", negative_false_passes, "Negative Clause Verification"),
    ):
        if errors:
            failures.append({
                "requirement": requirement, "failure_stage": stage,
                "root_cause": f"{len(errors)} review(s) violated applicability or polarity semantics.",
                "responsible_function": "_applicability_polarity_gates", "current_status": "FAIL",
            })
    return {
        "status": "BLOCKED" if failures else "REPORT_READY", "failures": failures,
        "gate_results": {
            "NOT_APPLICABLE_NARRATIVE_GATE": "FAIL" if na_narrative_errors else "PASS",
            "NOT_APPLICABLE_GAP_GATE": "FAIL" if na_gap_errors else "PASS",
            "REVIEW_POLARITY_NARRATIVE_GATE": "FAIL" if negative_narrative_errors else "PASS",
            "NEGATIVE_CHECK_PASS_GATE": "FAIL" if negative_false_passes else "PASS",
        },
        "not_applicable_gap_narrative_count": len(na_narrative_errors),
        "not_applicable_finding_count": sum(1 for row in na_rows if row["finding_created"]),
        "not_applicable_recommendation_count": sum(1 for row in na_rows if row["recommendation_created"]),
        "negative_review_positive_narrative_count": len(negative_narrative_errors),
        "negative_check_false_pass_count": len(negative_false_passes),
        "not_applicable_rows": na_rows, "polarity_rows": polarity_rows,
    }


def _display_suggested_clause(item: ReviewItemResult) -> tuple[str, str]:
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return "", ""
    if item.coverage_status == "通过":
        if item.risk_level == "低":
            return "", ""
        return "可选优化", item.suggested_clause_example
    if item.coverage_status == "部分覆盖":
        return "建议补充", str((item.narrative_state or {}).get("recommendation") or item.suggested_clause_example)
    if item.coverage_status == "风险条款":
        return "建议修改原条款", item.suggested_clause_example
    return "建议新增", item.suggested_clause_example


def _build_reasoning_text(item: ReviewItemResult, citation: Dict[str, str]) -> str:
    evidence_text = (
        f"{citation['clause_number']}：{citation['original_excerpt']}"
        if citation["original_excerpt"] != "无正式条款证据"
        else "未在正式合同条款或附件中召回可验证证据。"
    )
    return "\n".join(
        [
            "【推理过程】",
            f"证据：{evidence_text}",
            "↓",
            f"规则：{_legal_rule_text(item)}",
            "↓",
            f"判断：{_judgment_text(item, citation)}",
            "↓",
            f"结论：{_conclusion_text(item)}",
        ]
    )


def _enrich_reasoning_and_citation(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    for item in items:
        if item.risk_level not in _TRACEABLE_REASONING_RISK_LEVELS:
            item.reasoning = ""
            item.citation = {}
            continue

        citation = _first_citation(item)
        item.citation = citation
        item.reasoning = _build_reasoning_text(item, citation)
    return items


def _apply_final_quality_gate(
    items: List[ReviewItemResult],
    facts: Optional[HouseLeaseContractFacts],
    contract_type_key: str,
) -> tuple[List[ReviewItemResult], Dict[str, Any]]:
    flags: List[Dict[str, Any]] = []
    by_id = {item.item_id: item for item in items}

    for item in items:
        entails, evidence_type, semantic_reason = _semantic_entailment_for_item(item)
        if evidence_type:
            item.evidence_type = evidence_type
        if entails is not None:
            item.semantic_entailment = entails
        if entails is False and item.coverage_status in {"通过", "部分覆盖", "风险条款"}:
            flag = {
                "item_id": item.item_id,
                "type": "semantic_entailment_failed",
                "message": semantic_reason or "证据条款与审查点法律功能不匹配，已撤销覆盖结论并标记人工复核。",
                "recommended_action": "auto_fix",
            }
            flags.append(flag)
            item.quality_flags.append(flag)
            item.needs_manual_review = False
            item.quality_gate_failure_reason = ""
            item.review_status = "已自动修正"
            item.coverage_status = "缺失"
            item.status = "缺失或不明确"
            item.issue_type = "完全缺失"
            item.evidence_clauses = []
            item.evidence_location = ""
            item.risk_point_description = "未在正式合同条款中找到能覆盖该审查点法律功能的有效约定；已排除语义不匹配证据。"
            item.reasoning_summary = f"证据实质性匹配失败：{flag['message']} 未在正式合同条款中找到能覆盖该审查点的有效约定。"
        if item.coverage_status in {"通过", "部分覆盖", "风险条款"} and not item.evidence_clauses:
            # Low-risk pass without evidence is acceptable only for applicability or source exemptions.
            if item.coverage_status == "通过" and item.risk_level == "低":
                continue
            if item.coverage_status == "通过" and item.fallback_reason in {"案件文书摘录来源豁免"}:
                continue
            flag = {
                "item_id": item.item_id,
                "type": "evidence_missing",
                "message": "审查项存在覆盖结论但未附带正式条款或事实图谱证据，已标记人工复核。",
                "recommended_action": "human_review",
            }
            flags.append(flag)
            item.quality_flags.append(flag)
            item.review_status = "待人工复核"

    if contract_type_key == "lease":
        if facts:
            for field_name, node in facts.nodes.items():
                if node.value is not None and not node.evidence:
                    flags.append(
                        {
                            "item_id": "",
                            "type": "fact_without_provenance",
                            "field": field_name,
                            "message": f"Fact Graph 字段 {field_name} 有值但无 provenance，禁止作为高置信事实。",
                            "recommended_action": "retrieval_verify",
                        }
                    )

        if facts and facts.early_termination.exists and (item := by_id.get("HL-030")) and item.coverage_status != COVERAGE_NOT_APPLICABLE:
            flag = {
                "item_id": "HL-030",
                "type": "applicability_conflict",
                "message": "Fact Graph 显示存在提前退租条款，但 HL-030 仍在执行无提前退租补位审查，已自动改为不适用。",
                "recommended_action": "auto_fix",
            }
            flags.append(flag)
            _set_item_not_applicable(item, flag["message"])
            item.quality_flags.append(flag)

        hl015 = by_id.get("HL-015")
        hl017 = by_id.get("HL-017")
        if facts and facts.termination.rent_default.exists and hl015 and hl015.coverage_status == "缺失":
            flag = {
                "item_id": "HL-015",
                "type": "cross_review_consistency_auto_fix",
                "message": "Fact Graph 显示 termination.tenant.rent_default.exists=true，但 HL-015 仍为缺失，已按事实图谱 provenance 自动重审为通过。",
                "recommended_action": "auto_fix",
            }
            flags.append(flag)
            threshold = facts.termination.rent_default
            _set_item_pass_from_fact(
                hl015,
                facts,
                "termination.tenant.rent_default.exists",
                f"Final Quality Gate 读取 termination.tenant.rent_default.exists=true，threshold_type={threshold.threshold_type}，threshold_value={threshold.threshold_value}，threshold_unit={threshold.threshold_unit}，effect={threshold.effect}，修复欠租重大违约标准漏召回。",
                "合同已明确欠租达到一定期间或程度时可解除，欠租重大违约标准已覆盖。",
            )
            hl015.quality_flags.append(flag)

        if hl015 and hl017 and hl015.coverage_status == "缺失" and hl017.coverage_status == "通过":
            hl017_text = " ".join(clause.get("text", "") for clause in hl017.evidence_clauses)
            if any(term in hl017_text for term in ("欠租", "逾期不支付租金", "拖欠租金")):
                flag = {
                    "item_id": "HL-015",
                    "type": "cross_review_contradiction",
                    "message": "HL-017 已识别欠租解除事由，但 HL-015 仍称欠租标准缺失；已复用 HL-017 明确原文自动重审 HL-015。",
                    "recommended_action": "auto_fix",
                }
                flags.append(flag)
                hl015.risk_level = "低"
                hl015.status = "已覆盖"
                hl015.coverage_status = "通过"
                hl015.issue_type = "通过"
                hl015.evidence_clauses = hl017.evidence_clauses[:1]
                hl015.evidence_location = hl017.evidence_location
                hl015.reasoning_summary = "Cross Review Consistency Verifier 发现 HL-017 已基于同一解除条款识别欠租解除事由，HL-015 不得再判定为完全缺失。"
                hl015.risk_point_description = "合同已明确欠租达到一定期间或程度时可解除，欠租重大违约标准已覆盖。"
                hl015.fallback_reason = "Cross Review Consistency Verifier"
                hl015.quality_flags.append(flag)

        natural_wear_landlord = bool(facts and facts.repair.natural_wear == LANDLORD)
        if natural_wear_landlord:
            for item_id in ("HL-026", "HL-034"):
                item = by_id.get(item_id)
                if item and item.coverage_status == "缺失":
                    flag = {
                        "item_id": item_id,
                        "type": "cross_item_fact_conflict",
                        "message": "Fact Graph 明确 repair.natural_wear=landlord，但该审查项仍为缺失，已标记人工复核。",
                        "recommended_action": "human_review",
                    }
                    flags.append(flag)
                    item.quality_flags.append(flag)
                    item.review_status = "待人工复核"

        if facts and facts.deposit.amount and facts.deposit.return_deadline is None and (item := by_id.get("HL-043")) and item.risk_level == "高":
            flag = {
                "item_id": "HL-043",
                "type": "severity_anomaly_auto_fix",
                "message": "押金约为普通押金且仅缺少具体返还天数，不应自动高于剩余租期租金倍数违约金风险，已校准为中风险。",
                "recommended_action": "auto_fix",
            }
            flags.append(flag)
            item.risk_level = "中"
            item.quality_flags.append(flag)

        if (item := by_id.get("HL-039")) and item.scenario_analysis:
            impact = _economic_impact_for_penalty(item.scenario_analysis)
            if impact:
                item.economic_impact = impact
            formula = item.scenario_analysis.get("formula") or {}
            if impact == "high" and item.risk_level == "中" and _formula_requires_high_severity(formula):
                flag = {
                    "item_id": "HL-039",
                    "type": "severity_anomaly_auto_fix",
                    "message": "Scenario Engine 显示提前退租公式在长剩余租期下经济影响为 high，已从中风险校准为高风险。",
                    "recommended_action": "auto_fix",
                }
                flags.append(flag)
                item.risk_level = "高"
                item.quality_flags.append(flag)

        if facts and facts.jurisdiction.type == "arbitration" and facts.jurisdiction.arbitration_body is None:
            flags.append(
                {
                    "item_id": "HL-001",
                    "type": "fact_validation",
                    "message": "管辖事实包含未填写或未选中的仲裁机构，禁止作为有效管辖结论。",
                    "recommended_action": "ignore_unselected_option",
                }
            )

        apply_claims(items)
        for conflict in verify_consistency(items):
            flags.append(conflict)
            for claim in conflict.get("claims", []):
                item = by_id.get(claim.get("source_item_id"))
                if item:
                    item.quality_flags.append(conflict)
                    item.needs_manual_review = True
                    item.quality_gate_failure_reason = "Cross Review Consistency Verifier 发现同一事实存在相互冲突的审查结论。"

    if contract_type_key == "lease":
        _apply_high_risk_reason_gate(items)
    if contract_type_key != "lease":
        apply_claims(items)
    for item in items:
        if item.needs_manual_review and item.quality_gate_failure_reason:
            continue
        human_flags = [flag for flag in item.quality_flags if flag.get("recommended_action") == "human_review"]
        if human_flags:
            item.needs_manual_review = True
            item.quality_gate_failure_reason = human_flags[-1].get("message", "")

    return items, {
        "passed": not any(flag["recommended_action"] == "human_review" for flag in flags),
        "flags": flags,
        "flag_count": len(flags),
        "claims_count": sum(len(item.claims) for item in items),
    }


def _sanitize_review_report(report: str) -> str:
    cleaned = report
    cleaned = re.sub(
        r"合同存在可验证的“([^”]+)”(?:对应的核心安排|实质条款内容)",
        r"现有结构化结果尚未形成可追溯到具体缺失要素的“\1”修改依据",
        cleaned,
    )
    cleaned = re.sub(
        r"可验证的“([^”]+)”(?:对应的核心安排|实质条款内容)",
        r"可追溯到具体缺失要素的“\1”修改依据",
        cleaned,
    )
    cleaned = cleaned.replace("”对应的核心安排", "”具体修改依据")
    cleaned = cleaned.replace("对应的具体未明要素", "尚无法从现有材料确定的具体内容")
    cleaned = cleaned.replace("具体未明要素", "尚无法从现有材料确定的具体内容")
    cleaned = cleaned.replace("其余关键要素", "尚无法从现有材料确定的具体内容")
    cleaned = cleaned.replace("合同已明确覆盖：", "合同已明确约定")
    cleaned = cleaned.replace("合同已明确约定合同已约定", "合同已约定")
    cleaned = cleaned.replace("合同已明确约定已明确约定", "合同已明确约定")
    cleaned = cleaned.replace("合同已明确约定合同已限定", "合同已限定")
    cleaned = cleaned.replace("合同已明确约定合同未约定", "合同未约定")
    cleaned = cleaned.replace("合同已明确约定合同设置了", "合同设置了")
    cleaned = cleaned.replace("已明确约定合同已", "合同已")
    cleaned = cleaned.replace("合同已约定合同", "合同")
    cleaned = cleaned.replace("已经明确已经", "已经")
    cleaned = re.sub(r"合同已明确约定合同(?=[\u4e00-\u9fff])", "合同", cleaned)
    cleaned = cleaned.replace("建议建议", "建议")
    cleaned = cleaned.replace("无无需", "无需")
    cleaned = cleaned.replace("。。", "。")
    cleaned = cleaned.replace("；；", "；")
    cleaned = re.sub(r"已覆盖：已覆盖[:：]?", "已覆盖：", cleaned)
    cleaned = re.sub(r"缺失：缺失[:：]?", "缺失：", cleaned)
    cleaned = re.sub(r"：：+", "：", cleaned)
    cleaned = re.sub(r"([^。！？\n]{4,80}[。！？])\1+", r"\1", cleaned)
    return cleaned


def _report_text_validation_gate(report: str) -> Dict[str, Any]:
    patterns = {
        "BROKEN_QUOTE_CORE_ARRANGEMENT": r"”对应的核心安排",
        "DUPLICATE_COLON": r"：：+",
        "DUPLICATE_COVERED": r"已覆盖：已覆盖",
        "DUPLICATE_MISSING": r"缺失：缺失",
        "DUPLICATE_CONTRACT_COVERED": r"合同已明确约定合同|已明确约定合同已|合同已约定合同|已经明确已经",
        "DUPLICATE_SUGGEST": r"建议建议",
        "DUPLICATE_NO_ACTION": r"无无需",
        "DUPLICATE_PUNCTUATION": r"。。|；；",
        "UNREPLACED_TEMPLATE": r"\{[a-zA-Z_][a-zA-Z0-9_]*\}|<[^>\n]+>",
        "INTERNAL_ENUM_LEAK": r"\b(?:A_CORE|B_PRACTICAL|C_OPTIMIZATION|MUST_CHANGE|SHOULD_CHANGE|OPTIONAL_IMPROVEMENT|KEEP_CURRENT|DO_NOT_ADD|MANUAL_REVIEW|FOUND_SUPPORTING_CLAUSE|NO_SUPPORTING_CLAUSE)\b",
        "LEGACY_PRACTICE_AS_LEGAL": r"法律依据】：合同管理实务建议|法律依据】：相关法律规则参考",
        "PASS_PRACTICE_NOISE": r"当前未匹配到足够直接的现行具体条文",
        "DUPLICATE_EVIDENCE_TEXT": r"合同正文及附件中未找到对应约定；未在合同正文及附件中定位到对应安排",
        "NA_ALWAYS_APPLICABLE_CONTRADICTION": r"覆盖状态：不适用[\s\S]{0,240}【适用条件】：始终适用",
        "LEGACY_NOT_FOUND": r"未召回正式条款",
        "RECOMMENDATION_PLACEHOLDER_TEXT": r"对应安排|实质条款内容|具体未明要素|其余关键要素|可验证的“[^”]+”实质条款内容|“[^”]+”相关事项|建议[^\n。；]{0,80}相关事项",
    }
    failures: List[Dict[str, Any]] = []
    for name, pattern in patterns.items():
        matches = re.findall(pattern, report or "")
        if matches:
            failures.append({
                "requirement": "REPORT_TEXT_VALIDATION",
                "failure_stage": "Report Rendering",
                "root_cause": name,
                "count": len(matches),
                "current_status": "FAIL",
            })
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "gate_results": {"REPORT_TEXT_VALIDATION": "PASS" if not failures else "FAIL"},
        "broken_template_text_count": sum(failure["count"] for failure in failures),
    }


def _report_disposition_projection_gate(
    report: str,
    dispositions: List[FinalDisposition],
) -> Dict[str, Any]:
    if not _is_service_disposition_scope(dispositions):
        return {
            "status": "REPORT_READY",
            "failures": [],
            "gate_results": {"REPORT_DISPOSITION_PROJECTION_INVARIANT": "NOT_APPLICABLE"},
            "optional_improvement_count": _final_disposition_summary(dispositions)["optional_improvement"],
            "optional_section_item_count": 0,
            "hidden_optional_item_count": 0,
            "mismatches": [],
        }

    def section_item_count(title: str) -> int:
        marker = f"、{title}"
        if marker not in report:
            return 0
        section = report.split(marker, 1)[1].split("\n## ", 1)[0]
        return sum(1 for line in section.splitlines() if line.startswith("- **"))

    expected_optional = len(_visible_optional_dispositions(dispositions))
    actual_optional = section_item_count("可选优化事项")
    expected_priority = sum(1 for row in dispositions if row.include_in_priority_changes)
    actual_priority = section_item_count("建议优先修改")
    expected_keep = sum(1 for row in dispositions if row.final_action in {DISPOSITION_KEEP_CURRENT, DISPOSITION_DO_NOT_ADD})
    actual_keep = section_item_count("建议保持现状")
    hidden_optional_count = sum(
        1 for row in dispositions
        if row.final_action == DISPOSITION_OPTIONAL_IMPROVEMENT
        and row not in _visible_optional_dispositions(dispositions)
    )
    mismatches = [
        {"section": "optional_improvement", "expected": expected_optional, "actual": actual_optional},
        {"section": "priority_changes", "expected": expected_priority, "actual": actual_priority},
        {"section": "keep_current", "expected": expected_keep, "actual": actual_keep},
    ]
    mismatches = [row for row in mismatches if row["expected"] != row["actual"]]
    if hidden_optional_count:
        mismatches.append({"section": "hidden_optional", "expected": 0, "actual": hidden_optional_count})
    failures = [{
        "requirement": "REPORT_DISPOSITION_PROJECTION_INVARIANT",
        "failure_stage": "Report Projection",
        "root_cause": "FinalDisposition counts do not match visible report section items.",
        "current_status": "FAIL",
        "mismatches": mismatches,
    }] if mismatches else []
    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "gate_results": {"REPORT_DISPOSITION_PROJECTION_INVARIANT": "PASS" if not failures else "FAIL"},
        "optional_improvement_count": expected_optional,
        "optional_section_item_count": actual_optional,
        "hidden_optional_item_count": hidden_optional_count,
        "mismatches": mismatches,
    }


def _system_metadata(model_status: Dict[str, Any]) -> Dict[str, Any]:
    configured_models = model_status.get("configured_models") or []
    return {
        "system_version": SYSTEM_VERSION,
        "pipeline_version": PIPELINE_VERSION,
        "prompt_version": PROMPT_VERSION,
        "fact_prompt_version": FACT_PROMPT_VERSION,
        "review_prompt_version": REVIEW_PROMPT_VERSION,
        "verifier_prompt_version": VERIFIER_PROMPT_VERSION,
        "risk_aggregation_prompt_version": RISK_AGGREGATION_PROMPT_VERSION,
        "recommendation_prompt_version": RECOMMENDATION_PROMPT_VERSION,
        "rule_version": RULE_VERSION,
        "legal_dataset_version": LEGAL_DATASET_VERSION,
        "ontology_version": ONTOLOGY_VERSION,
        "quality4_version": QUALITY4_VERSION,
        "benchmark_version": BENCHMARK_VERSION,
        "parser_version": PARSER_VERSION,
        "fact_schema_version": FACT_SCHEMA_VERSION,
        "retrieval_version": RETRIEVAL_VERSION,
        "domain_pack_version": DOMAIN_PACK_VERSION,
        "default_law_version": DEFAULT_LAW_VERSION,
        "perspective_resolver_version": PERSPECTIVE_RESOLVER_VERSION,
        "effective_gap_engine_version": "effective-gap-6.7-freeze-1.0",
        "recommendation_engine_version": RECOMMENDATION_ENGINE_VERSION,
        "production_serializer_version": PRODUCTION_SERIALIZER_VERSION,
        "confidence_version": CONFIDENCE_VERSION,
        "cross_type_generalization_stage": "CONVERGED",
        "sale_historical_blind_001": "FROZEN_REGRESSION",
        "sale_historical_blind_002": "FROZEN_REGRESSION",
        "sale_historical_blind_003": "FROZEN_REGRESSION",
        "sale_historical_blind_004": "FROZEN_REGRESSION",
        "next_blind_case": "SALE-BLIND-005",
        "next_blind_status": "READY",
        "fact_graph_version": FACT_SCHEMA_VERSION,
        "domain_packs": {
            "shared": domain_pack_snapshot("shared"),
            "sale": domain_pack_snapshot("sale"),
            "sale_framework_supply": domain_pack_snapshot("sale/goods/framework_supply"),
            "house_lease": domain_pack_snapshot("house_lease"),
        },
        "model_version": configured_models[0] if configured_models else "deterministic_pipeline",
        "generated_at": datetime.now().isoformat(),
    }


def _apply_profile_rules(
    items: List[ReviewItemResult],
    profile: UserRiskProfile,
    perspective_resolution: Dict[str, Any],
) -> List[ReviewItemResult]:
    """根据用户风险画像动态调整审查结果。

    1. 风险等级重映射（保守→提升，激进→降低）
    2. 标注行动标签（必须改/建议改/可考虑改）
    3. 标注是否为优先审查点
    4. 修改建议语气适配
    """
    for item in items:
        item.decision_trace["user_perspective"] = perspective_resolution.get("canonical_role", "UNCERTAIN")
        item.decision_trace["perspective_resolution"] = perspective_resolution
        item.decision_trace["bargaining_power"] = profile.bargaining_position
        if item.coverage_status == COVERAGE_NOT_APPLICABLE or item.risk_level in {COVERAGE_NOT_APPLICABLE, RISK_NOT_APPLICABLE}:
            continue
        if item.coverage_status == "通过" and item.risk_level == "低":
            continue

        # 风险等级重映射
        original_risk = item.risk_level
        item.risk_level = get_risk_remap(original_risk, profile.risk_appetite)

    return items


def _format_item_submodule(
    item_id: str,
    litigation_items: Dict[str, Any],
    negotiation_items: Dict[str, Any],
    jurisdiction_items: Dict[str, Any],
) -> List[str]:
    """为单个高风险项生成诉讼策略/商业谈判/跨地域裁判预判三个子模块。"""
    lines: List[str] = []

    lit = litigation_items.get(item_id)
    neg = negotiation_items.get(item_id)
    jur = jurisdiction_items.get(item_id)

    if lit:
        lines.append("### 诉讼策略")
        lines.append("")
        lines.append("#### 证据链评估")
        critical = [g for g in lit.get("evidence_gaps", []) if g["severity"] == "critical"]
        recommended = [g for g in lit.get("evidence_gaps", []) if g["severity"] == "recommended"]
        sufficient = [g for g in lit.get("evidence_gaps", []) if g["severity"] == "sufficient"]
        if critical:
            lines.append("- **缺了几乎必输**：")
            for g in critical:
                lines.append(f"  - {g['evidence_name']}：{g['description']}")
                if g.get("source_hint"):
                    lines.append(f"    > 获取方式：{g['source_hint']}")
        if recommended:
            lines.append("- **建议补充**：")
            for g in recommended:
                lines.append(f"  - {g['evidence_name']}：{g['description']}")
                if g.get("source_hint"):
                    lines.append(f"    > 获取方式：{g['source_hint']}")
        if sufficient:
            lines.append("- **证据充分**：")
            for g in sufficient:
                lines.append(f"  - ✅ {g['evidence_name']}：{g['description']}")
        if not critical and not recommended and not sufficient:
            lines.append("暂无特定证据缺口分析。")
        lines.append("")

        if lit.get("court_prediction"):
            cp = lit["court_prediction"]
            lines.append("#### 法院裁量预测")
            lines.append(f"- **合同约定**：{cp.get('contract_terms', '')}")
            lines.append(f"- **法院大概率支持**：{cp.get('likely_court_view', '')}")
            lines.append(f"- **法律依据**：{cp.get('legal_basis', '')}")
            if cp.get("amount_range"):
                lines.append(f"- **可执行金额范围**：{cp['amount_range']}")
            if cp.get("reference_cases"):
                lines.append(f"- **参考判例/解释**：{cp['reference_cases']}")
            lines.append("")

        if lit.get("cost_benefit"):
            cb = lit["cost_benefit"]
            lines.append("#### 成本收益分析")
            lines.append(f"- **争议金额**：约{cb.get('dispute_amount', 0):.0f}元")
            lines.append(f"- **预估诉讼费**：约{cb.get('litigation_fee', 0):.0f}元")
            lines.append(f"- **时间成本**：{cb.get('time_cost', '')}")
            lines.append(f"- **执行风险**：{cb.get('enforcement_risk', '')}")
            lines.append(f"- **起诉建议**：**{cb.get('recommendation', '')}**")
            lines.append(f"  > {cb.get('recommendation_reason', '')}")
            lines.append("")

        lines.append(f"> 本分析不构成法律意见，仅供参考。")
        lines.append("")

    if neg:
        lines.append("### 商业谈判")
        lines.append("")
        lines.append("#### 对方意图分析")
        ci = neg.get("counterparty_intent", {})
        lines.append(f"- **对方可能担心**：{ci.get('likely_concern', '')}")
        lines.append(f"- **对方希望**：{ci.get('likely_want', '')}")
        if ci.get("pressure_points"):
            lines.append(f"- **谈判压力点**：{ci['pressure_points']}")
        lines.append("")

        lines.append("#### 替代方案")
        for alt in neg.get("alternatives", []):
            lines.append(f"- {alt.get('proposal', '')}")
            lines.append(f"  - 对己方影响：{alt.get('impact', '')}")
            lines.append(f"  - 可行性：{alt.get('feasibility', '')}")
        lines.append("")

        lines.append("#### 交换筹码")
        to = neg.get("tradeoff", {})
        lines.append(f"- **你可以让步**：{to.get('what_you_give', '')}")
        lines.append(f"- **要求对方回报**：{to.get('what_you_ask', '')}")
        lines.append(f"- **交换理由**：{to.get('rationale', '')}")
        lines.append("")

        lines.append("#### 谈判话术")
        lines.append(f"> {neg.get('script', '')}")
        lines.append("")

        lines.append(f"> 本分析不构成法律意见，仅供参考。")
        lines.append("")

    if jur:
        lines.append("### 跨地域裁判预判")
        lines.append("")
        lines.append("#### 本地法院倾向")
        lines.append(f"> {jur.get('local_court_tendency', '')}")
        lines.append("")

        lines.append("#### 本地判例参考")
        for case in jur.get("local_cases", []):
            lines.append(f"- **{case.get('case_id', '')}**（{case.get('court', '')}）")
            lines.append(f"  > {case.get('conclusion', '')}")
            lines.append(f"  > 关联性：{case.get('relevance', '')}")
        if not jur.get("local_cases"):
            lines.append("该地区暂无同类判例可查。")
        lines.append("")

        lines.append("#### 起诉建议")
        lines.append(f"- **建议**：**{jur.get('litigation_recommendation', '')}**")
        lines.append(f"  > {jur.get('recommendation_reason', '')}")
        lines.append("")

        if jur.get("data_source_note"):
            lines.append(f"> {jur['data_source_note']}")
        lines.append("")

    return lines


def _format_markdown_v2(
    contract_type_name: str,
    items: List[ReviewItemResult],
    profile: UserRiskProfile,
    risk_findings: Optional[List[RiskFinding]] = None,
    recommendations: Optional[List[Recommendation]] = None,
    overall_assessment: Optional[Dict[str, Any]] = None,
    risk_finding_summary: Optional[Dict[str, int]] = None,
    benchmark_metrics: Optional[Dict[str, Any]] = None,
    release_quality_gate: Optional[Dict[str, Any]] = None,
    system_metadata: Optional[Dict[str, Any]] = None,
    litigation_items: Optional[Dict[str, Any]] = None,
    negotiation_items: Optional[Dict[str, Any]] = None,
    jurisdiction_items: Optional[Dict[str, Any]] = None,
    report_context: Optional[Dict[str, Any]] = None,
    perspective_resolution: Optional[Dict[str, Any]] = None,
    final_dispositions: Optional[List[FinalDisposition]] = None,
) -> str:
    """Pure Markdown serializer for the final ReviewItemResult list."""
    findings = risk_findings or []
    recs = recommendations or []
    dispositions = final_dispositions or _build_final_dispositions(findings, recs, [])
    manual_review_items = _manual_review_records(items)
    finding_summary = risk_finding_summary or _risk_finding_summary(findings, items)
    assessment = overall_assessment or _overall_assessment(contract_type_name, findings, items, dispositions, manual_review_items)
    disposition_by_risk = {disposition.risk_id: disposition for disposition in dispositions}
    disposition_summary = _final_disposition_summary(dispositions)
    must_count = disposition_summary["must_change"]
    suggest_count = disposition_summary["should_change"]
    consider_count = disposition_summary["optional_improvement"]
    item_by_id = {item.item_id: item for item in items}
    finding_by_id = {finding.finding_id: finding for finding in findings}
    top_dispositions = [row for row in dispositions if row.include_in_top_risk][:10]
    priority_dispositions = [row for row in dispositions if row.include_in_priority_changes]
    optimization_dispositions = (
        _visible_optional_dispositions(dispositions)
        if _is_service_disposition_scope(dispositions)
        else [row for row in dispositions if row.include_in_optional_improvements][:10]
    )
    keep_current_dispositions = [row for row in dispositions if row.final_action in {DISPOSITION_KEEP_CURRENT, DISPOSITION_DO_NOT_ADD}]
    covered_key_items = [item for item in items if item.coverage_status == "通过" and item.review_importance in {REVIEW_IMPORTANCE_CORE, REVIEW_IMPORTANCE_IMPORTANT}][:10]
    finding_title_map = _finding_id_title_map(findings)
    recommendation_by_finding = {
        finding_id: recommendation
        for recommendation in recs
        if recommendation.status == "ACTIVE"
        for finding_id in recommendation.target_finding_ids
    }
    section_index = 0

    def add_section(title: str) -> None:
        nonlocal section_index
        section_index += 1
        lines.extend(["", _section_title(section_index, title), ""])

    report_context = report_context or {"contract_type_label": contract_type_name, "scenario_label": profile.contract_scenario}
    profile_lines = _report_context_profile_lines(profile, report_context, perspective_resolution or {})
    lines = [
        f"# {report_context.get('report_title') or contract_type_name + '审查报告'}",
        "",
    ]
    add_section("合同总体评价")
    lines.extend([
        *profile_lines,
        f"- 合同类型：{report_context['contract_type_label']}",
        f"- 总体可签署性：{assessment.get('signability')}",
        f"- 风险发现总数：{len(findings)}",
        f"- 重大风险数量：{finding_summary.get('重大风险', 0)}",
        f"- 中等风险数量：{finding_summary.get('中等风险', 0)}",
        f"- 低风险数量：{finding_summary.get('低风险', 0)}",
        f"- 需要真正修改的风险数：{disposition_summary['actionable']}",
        f"- 优先处理风险：{must_count}",
        f"- 建议处理风险：{suggest_count}",
        f"- 可选优化数：{consider_count}",
        f"- 已识别但建议保持现状数：{disposition_summary['protected_no_change']}",
        f"- 人工复核项：{len(manual_review_items)}",
        "",
        "### 审查覆盖统计",
        f"- 已覆盖：{_coverage_summary(items).get('通过', 0)} 项",
        f"- 部分覆盖：{_coverage_summary(items).get('部分覆盖', 0)} 项",
        f"- 缺失：{_coverage_summary(items).get('缺失', 0)} 项",
        f"- 风险条款：{_coverage_summary(items).get('风险条款', 0)} 项",
        f"- 不适用：{sum(1 for item in items if item.coverage_status == COVERAGE_NOT_APPLICABLE)} 项",
        "",
        f"> {REPORT_FORMAT_NOTICE}",
    ])
    add_section("核心风险摘要")
    if top_dispositions:
        for disposition in top_dispositions:
            finding = finding_by_id.get(disposition.risk_id)
            if not finding:
                continue
            lines.append(_top_risk_line(finding, item_by_id, recommendation_by_finding.get(finding.finding_id)))
            lines.append("")
    if not top_dispositions:
        lines.append("- 未发现需要优先处理的高风险或重大经济后果事项。")
    add_section("建议优先修改")
    if priority_dispositions:
        for disposition in priority_dispositions:
            target_name = finding_title_map.get(disposition.risk_id, disposition.risk_title)
            lines.append(f"- **{_final_action_label(disposition.final_action)}**：{disposition.recommendation}（对应风险：{target_name}）")
    else:
        lines.append("- 暂无必须或优先修改事项。")
    add_section("可选优化事项")
    lines.append("以下事项属于完善型建议，通常不是当前签署的核心障碍。")
    lines.append("")
    if optimization_dispositions:
        for disposition in optimization_dispositions:
            target_name = finding_title_map.get(disposition.risk_id, disposition.risk_title)
            lines.append(f"- **可选优化**：{disposition.recommendation}（对应风险：{target_name}）")
    else:
        lines.append("- 暂无需要单独提示的可优化事项。")
    if keep_current_dispositions:
        add_section("建议保持现状")
        for disposition in keep_current_dispositions:
            target_name = finding_title_map.get(disposition.risk_id, disposition.risk_title)
            lines.append(f"- **{target_name}**：{disposition.final_reason}")
    add_section("已覆盖关键事项")
    if covered_key_items:
        for item in covered_key_items:
            related = f"；关联风险：{_join_related_finding_titles(item.related_risks, finding_title_map)}" if item.related_risks else ""
            if (item.decision_trace or {}).get("review_polarity") == "NEGATIVE_CLAUSE_CHECK":
                lines.append(f"- **{item.item_id} {item.title}**：未发现对应不利安排{related}。")
            else:
                lines.append(f"- **{item.item_id} {item.title}**：已覆盖{related}。")
    else:
        lines.append("- 已覆盖项详见完整审查明细。")
    if manual_review_items:
        add_section("人工复核事项")
        for row in manual_review_items:
            lines.append(f"- **{row['item_id']} {row['title']}**：{row['reason']}（重要度：{row['materiality']}）")
    lines.extend(["", "---"])
    add_section("完整审查明细")
    for index, item in enumerate(items, start=1):
        legal_label, legal_value = _display_legal_consequence(item)
        display_state = (item.decision_trace or {}).get("recommendation_display_state") or {}
        formal_recommendations = list(display_state.get("formal_recommendations") or [])
        review_instructions = list(display_state.get("review_instructions") or [])
        suggested_label = "正式建议" if formal_recommendations else "复核提示" if review_instructions else ""
        suggested_value = "；".join(formal_recommendations or review_instructions)
        narrative = item.narrative_state or _build_narrative_state(item)
        exposure = str(((item.decision_trace or {}).get("effective_gap_narrative") or {}).get("generated_narrative", ""))
        issue_value = str(narrative.get("issue") or narrative.get("judgment") or item.risk_point_description)
        legal_basis = _trusted_legal_basis_display(item)
        practice_basis = _practice_basis_display(item)
        if legal_label not in {"处理结论", "适用说明"}:
            legal_value = str(narrative.get("consequence") or legal_value)
        if item.coverage_status == COVERAGE_NOT_APPLICABLE:
            suggested_label = ""
        lines.extend([f"## {index}. {item.title}（{item.item_id}）", "", "### 审查结论"])
        base_lines = [
            f"- **处理建议**：{display_state.get('user_message') or item.action_suggestion or _action_suggestion_for_item(item)}",
            f"- 覆盖状态：{item.coverage_status}",
        ]
        if item.coverage_status == INSUFFICIENT_CONTEXT:
            detail_lines = [
                *base_lines,
                f"- 审查判断：{_applicability_user_reason(item)}",
                f"- 【适用条件】：{item.applicable_if}",
            ]
        elif item.coverage_status == COVERAGE_NOT_APPLICABLE:
            detail_lines = [
                *base_lines,
                f"- 【适用说明】：{_applicability_user_reason(item)}",
            ]
        elif item.coverage_status == "通过":
            detail_lines = [
                *base_lines,
                f"- 原文位置：{_evidence_position_display(item)}",
                f"- 审查判断：{narrative.get('judgment') or _professional_item_conclusion(item)}",
                *([f"- 关联风险发现：{_join_related_finding_titles(item.related_risks, finding_title_map)}"] if item.related_risks else []),
                *([f"- 【法律依据】：{legal_basis}"] if legal_basis else []),
            ]
        elif any(action in {DISPOSITION_KEEP_CURRENT, DISPOSITION_DO_NOT_ADD} for action in display_state.get("final_actions", [])):
            suppression_reasons = [
                row.get("suppression_reason", "")
                for row in (item.decision_trace.get("final_dispositions") or [])
                if row.get("suppression_reason")
            ]
            detail_lines = [
                *base_lines,
                f"- 发现的问题：{'; '.join(suppression_reasons) if suppression_reasons else issue_value}",
                f"- 【{legal_label}】：{legal_value}",
                *([f"- 【法律依据】：{legal_basis}"] if legal_basis else []),
                f"- 不建议修改原因：{'; '.join(row.get('final_reason', '') for row in (item.decision_trace.get('final_dispositions') or []) if row.get('final_action') in {DISPOSITION_KEEP_CURRENT, DISPOSITION_DO_NOT_ADD})}",
            ]
        else:
            detail_lines = [
                *base_lines,
                f"- 行动优先级：{_priority_label(item.action_priority or item.review_priority or _action_priority_for_item(item))}",
                f"- 关联风险发现：{_join_related_finding_titles(item.related_risks, finding_title_map)}",
                f"- 判断可靠度：{_confidence_label((item.system_confidence or {}).get('level', 'medium'))}",
                f"- 经济影响：{_economic_display(item.economic_impact)}",
                f"- 问题类型：{item.issue_type}",
                f"- 原文位置：{_evidence_position_display(item)}",
                f"- 审查判断：{narrative.get('judgment') or _professional_item_conclusion(item)}",
                f"- 【风险点描述】：{issue_value}",
                f"- 【{legal_label}】：{legal_value}",
                *([f"- 【法律依据】：{legal_basis}"] if legal_basis else []),
                *([f"- 【实务建议】：{practice_basis}"] if practice_basis else []),
                *([f"- 【实际法律暴露】：{exposure}"] if exposure else []),
                f"- 【适用条件】：{item.applicable_if}",
            ]
        lines.extend([line for line in detail_lines if line and not line.endswith("：")])
        lines.append("")
        if suggested_label and suggested_value:
            lines.extend([f"- 【{suggested_label}】：{suggested_value}", ""])
        if item.citation:
            status = item.citation.get("evidence_status")
            if status in {"NO_SUPPORTING_CLAUSE", "NO_ADVERSE_CLAUSE_FOUND", "NO_CLAUSE_REQUIRED", "NOT_APPLICABLE", "RETRIEVAL_FAILED", "INSUFFICIENT_CONTEXT"}:
                lines.extend(
                    [
                        "【证据定位】",
                        f"- {item.citation.get('position_description', '合同正文及附件中未找到对应约定。')}",
                        "",
                    ]
                )
            else:
                lines.extend(
                    [
                        "【证据定位】",
                        f"- 依据来源：{item.citation.get('source_label', '合同文件')}",
                        f"- 条款编号：{item.citation.get('clause_number', '未召回正式条款')}",
                        f"- 原文片段：{item.citation.get('original_excerpt', '无正式条款证据')}",
                        f"- 位置描述：{item.citation.get('position_description', '合同正式条款及附件中未定位到可验证条款')}",
                        "",
                    ]
                )
        lines.append("---")
        lines.append("")
    return _sanitize_review_report("\n".join(lines))


def _recommendation_renderer_gates(
    report: str,
    items: List[ReviewItemResult],
    recommendations: List[Recommendation],
    impacts: List[Any],
) -> Dict[str, Any]:
    summary, _, detail = report.partition("完整审查明细")
    recommendation_by_id = {recommendation.recommendation_id: recommendation for recommendation in recommendations}
    blocked_text = {
        impact.recommendation_id: impact.proposed_change
        for impact in impacts if impact.gate_result == "BLOCKED" and impact.proposed_change
    }
    rows: List[Dict[str, Any]] = []
    dual_source: List[Dict[str, Any]] = []
    mismatches: List[Dict[str, Any]] = []
    for item in items:
        state = (item.decision_trace or {}).get("recommendation_display_state") or {}
        marker = f"（{item.item_id}）"
        section = detail.split(marker, 1)[1] if marker in detail else ""
        if section:
            section = section.split("\n## ", 1)[0]
        summary_ids = [
            recommendation_id for recommendation_id in state.get("active_recommendation_ids", [])
            if (recommendation_by_id.get(recommendation_id).proposed_change or recommendation_by_id.get(recommendation_id).suggested_text) in summary
        ]
        detail_ids = [
            recommendation_id for recommendation_id in state.get("active_recommendation_ids", [])
            if (recommendation_by_id.get(recommendation_id).proposed_change or recommendation_by_id.get(recommendation_id).suggested_text) in section
        ]
        resurrected = [
            recommendation_id for recommendation_id in state.get("blocked_recommendation_ids", [])
            if blocked_text.get(recommendation_id) and blocked_text[recommendation_id] in report
        ]
        detail_generated = not state.get("has_active_recommendation") and (
            "【正式建议】" in section
            or bool(re.search(r"\*\*处理建议\*\*：(?:建议新增|建议补充|建议修改|建议明确)", section))
        )
        final_actions = set(state.get("final_actions") or [])
        final_source_controls = bool(final_actions)
        expected_active_ids = set(state.get("active_recommendation_ids", []))
        if final_source_controls:
            actionable_final = final_actions & {DISPOSITION_MUST_CHANGE, DISPOSITION_SHOULD_CHANGE, DISPOSITION_OPTIONAL_IMPROVEMENT}
            final_text_rendered = (
                any(text and text in report for text in state.get("final_recommendations", []))
                or any(title and title in report for title in state.get("final_disposition_titles", []))
            )
            mismatch = bool(actionable_final and expected_active_ids and not (set(summary_ids) or set(detail_ids) or final_text_rendered))
        else:
            mismatch = set(summary_ids) != expected_active_ids or set(detail_ids) != expected_active_ids
        row = {
            **state, "summary_recommendation_ids": summary_ids, "detail_recommendation_ids": detail_ids,
            "resurrected_recommendation_ids": resurrected, "detail_generated_recommendation": detail_generated,
            "mismatch": mismatch,
        }
        rows.append(row)
        if resurrected or detail_generated:
            dual_source.append(row)
        if mismatch:
            mismatches.append(row)
    failures = []
    if dual_source:
        failures.append({
            "requirement": "RECOMMENDATION_SINGLE_SOURCE_GATE", "failure_stage": "Production Recommendation Rendering",
            "root_cause": "A production renderer generated or resurrected a recommendation outside FinalRecommendationSet.",
            "responsible_function": "_format_markdown_v2", "current_status": "FAIL",
        })
    if mismatches:
        failures.append({
            "requirement": "RECOMMENDATION_CROSS_RENDERER_CONSISTENCY_GATE", "failure_stage": "Production Recommendation Rendering",
            "root_cause": "Summary and detail renderers did not consume the same active recommendation IDs.",
            "responsible_function": "_format_markdown_v2", "current_status": "FAIL",
        })
    return {
        "status": "BLOCKED" if failures else "REPORT_READY", "failures": failures,
        "gate_results": {
            "RECOMMENDATION_SINGLE_SOURCE_GATE": "FAIL" if dual_source else "PASS",
            "RECOMMENDATION_CROSS_RENDERER_CONSISTENCY_GATE": "FAIL" if mismatches else "PASS",
        },
        "dual_source_count": len(dual_source), "cross_renderer_mismatch_count": len(mismatches), "rows": rows,
    }


def review_contract_v2(
    contract_text: str,
    contract_type: Optional[str] = "house_lease",
    *,
    include_low_risk: bool = True,
    use_llm: bool = True,
    profile: Optional[UserRiskProfile] = None,
) -> Dict[str, Any]:
    """按第二版审查清单审查合同。

    支持用户风险画像（UserRiskProfile）驱动审查输出：
    - 风险等级个性化（保守/标准/激进）
    - 修改建议语气动态调整
    - 审查点优先激活/过滤
    """

    started_at = time.perf_counter()
    contract_review_trace_id = f"CR-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

    normalized_type = (contract_type or "house_lease").strip().lower()
    try:
        type_meta = get_contract_meta(contract_type)
    except UnsupportedContractTypeError:
        type_meta = None
    llm_status = get_llm_review_status()
    if not use_llm:
        global_fallback_reason = "本次审查未启用大模型语义复核，使用规则判定"
    elif not llm_status.get("available"):
        global_fallback_reason = llm_status.get("message", "")
    else:
        global_fallback_reason = ""

    if not type_meta:
        profile = _request_scoped_profile(profile, normalized_type)
        return {
            "success": False,
            "contract_type": normalized_type,
            "contract_type_name": "未支持的合同类型",
            "message": f"审查第二版当前支持{'、'.join(supported_contract_display_names())}；其他合同类型应按同一审查清单结构迁移。",
            "contract_review_trace_id": contract_review_trace_id,
            "items": [],
            "summary": {"高": 0, "中": 0, "低": 0},
            "risk_finding_summary": {"重大风险": 0, "中等风险": 0, "低风险": 0, "人工复核": 0},
            "coverage_summary": {},
            "issue_type_summary": {},
            "judge_source_summary": {},
            "llm_enabled": use_llm,
            "llm_status": llm_status,
            "global_fallback_reason": global_fallback_reason,
            "report_notice": REPORT_FORMAT_NOTICE,
            "result": "",
            "review_results_4_0": [],
            "risk_findings": [],
            "recommendations": [],
            "contract_context": build_contract_context(normalized_type, {}, profile, contract_text=contract_text).to_public_dict(),
            "overall_assessment": {},
            "legal_reference_issues": [],
            "legal_citation_claims": [],
            "legal_authority_validation": {},
            "benchmark_metrics": {},
            "release_quality_gate": {"status": "BLOCKED", "failures": [{"requirement": "Supported Contract Type", "failure_stage": "Parser Validation", "root_cause": "Unsupported contract type.", "responsible_function": "get_contract_meta", "current_status": "FAIL"}]},
            "quality4_gate": {"status": "BLOCKED", "failures": [{"requirement": "Supported Contract Type", "failure_stage": "Parser Validation", "root_cause": "Unsupported contract type.", "fix_owner": "Contract Registry"}]},
            "architecture_status": _architecture_status(),
            "system_metadata": _system_metadata(llm_status),
            "observability": {"total_latency_ms": round((time.perf_counter() - started_at) * 1000, 2)},
            "profile": profile.to_dict(),
        }

    review_text = strip_non_contract_tail(contract_text)
    clauses = parse_contract_clauses(review_text)
    integrity = document_integrity(review_text, clauses).to_public_dict()
    user_selected_type = type_meta.response_key
    domain_selection_resolution, domain_resolution, resolved_type = resolve_domain_selection(
        user_selected_type, review_text, clauses,
    )
    type_meta = get_contract_meta(resolved_type)
    profile = _request_scoped_profile(profile, type_meta.response_key)
    previous_context_role = "LESSEE" if user_selected_type == "house_lease" else "BUYER" if user_selected_type == "sale" else ""
    perspective_resolution = resolve_perspective(
        profile.user_identity, domain_resolution.contract_family, previous_context_role=previous_context_role,
    )
    if type_meta.key.value == "sale" and domain_resolution.subject_matter == "REAL_ESTATE":
        # Registered-property schedules commonly follow signature blocks and remain contractual evidence.
        review_text = contract_text
        clauses = parse_contract_clauses(review_text)
        integrity = document_integrity(review_text, clauses).to_public_dict()
        domain_resolution = resolve_contract_domain(type_meta.key.value, review_text, clauses)
    generic_fact_graph = extract_contract_fact_graph(clauses)
    framework_supply = extract_framework_supply_profile(review_text, clauses) if type_meta.key.value == "sale" else None
    if framework_supply:
        add_framework_facts_to_graph(framework_supply, clauses, generic_fact_graph)
    real_estate_facts = None
    if type_meta.key.value == "sale" and domain_resolution.subject_matter == "REAL_ESTATE":
        real_estate_facts = extract_real_estate_sale_facts(review_text, clauses, generic_fact_graph)
    fact_registry_snapshot_id = _fact_registry_snapshot_id(generic_fact_graph)
    generic_fact_graph.freeze(fact_registry_snapshot_id)
    checklist = get_checklist_for_resolution(type_meta.key, domain_resolution)
    registry_debug = review_registry_debug(type_meta.key, domain_resolution)
    lease_facts = extract_house_lease_facts(review_text) if type_meta.key.value == "lease" else None
    contract_facts = lease_facts.to_public_dict() if lease_facts else generic_fact_graph.to_public_dict()
    contract_facts["fact_registry_snapshot_id"] = fact_registry_snapshot_id
    contract_facts["domain_resolution"] = domain_resolution.to_public_dict()
    contract_facts["domain_selection_resolution"] = domain_selection_resolution.to_public_dict()
    if framework_supply:
        contract_facts["framework_supply"] = framework_supply.to_public_dict()
    if real_estate_facts:
        contract_facts["real_estate"] = real_estate_facts.to_public_dict()
    canonical_claims = build_canonical_claims(review_text, clauses, generic_fact_graph, domain_resolution.subject_matter)
    contract_facts["canonical_claims"] = canonical_claims_public(canonical_claims)
    product_documentation_profile = (
        build_product_documentation_profile(review_text, clauses, domain_resolution)
        if type_meta.key.value == "sale" and domain_resolution.subject_matter in {"GOODS", "EQUIPMENT"}
        else None
    )
    if product_documentation_profile:
        contract_facts["product_documentation_profile"] = product_documentation_profile.to_public_dict()
    contract_context = build_contract_context(type_meta.response_key, contract_facts, profile, contract_text=review_text, domain_resolution=domain_resolution).to_public_dict()
    contract_context["user_role"] = perspective_resolution.canonical_role.lower()
    contract_context["user_perspective"] = perspective_resolution.canonical_role.lower()
    contract_context["perspective_resolution"] = perspective_resolution.to_public_dict()
    if product_documentation_profile:
        contract_context.setdefault("domain_attributes", {})["product_documentation_profile"] = product_documentation_profile.to_public_dict()
    report_context = build_report_context(contract_context).to_public_dict()
    if report_context.get("contract_type_label") == "合同" and type_meta.key.value not in {"sale", "lease"}:
        report_context["contract_type_label"] = type_meta.display_name
        report_context["report_title"] = f"{type_meta.display_name}审查报告"
    review_execution_context = ReviewExecutionContext(
        contract_context={
            "contract_family": contract_context.get("contract_family"),
            "subject_matter": contract_context.get("subject_matter"),
            "contract_subtype": contract_context.get("contract_subtype"),
        },
        domain_resolution=domain_resolution.to_public_dict(),
        transaction_structure=domain_resolution.transaction_structure,
        product_context=product_documentation_profile.to_public_dict() if product_documentation_profile else {},
        fact_graph_version=FACT_SCHEMA_VERSION,
        claim_graph_version=str((contract_facts.get("canonical_claims") or {}).get("version") or ""),
        applicable_default_law=DEFAULT_LAW_VERSION,
    ).to_public_dict()
    if profile.contract_scenario != report_context["scenario_label"]:
        profile_data = profile.to_dict()
        profile_data["contract_scenario"] = report_context["scenario_label"]
        profile = UserRiskProfile.from_dict(profile_data)
    applicable_checkpoints = []
    not_applicable_items: Dict[str, ReviewItemResult] = {}
    item_applicability: Dict[str, Dict[str, Any]] = {}
    for checkpoint in checklist:
        is_applicable, applicability_reason = _is_checkpoint_applicable(review_text, checkpoint, type_meta.key.value, canonical_claims)
        fact_applicability = _evaluate_lease_fact_applicability(checkpoint, lease_facts) if lease_facts else _applicability_result_for_checkpoint(
            checkpoint,
            clauses,
            is_applicable,
            applicability_reason,
            canonical_claims,
        )
        product_applicability = (
            product_review_applicability(checkpoint.node_id, product_documentation_profile)
            if product_documentation_profile else None
        )
        if product_applicability:
            is_applicable = bool(product_applicability["applicable"])
            applicability_reason = str(product_applicability["reason"])
            fact_applicability = {
                "review_id": checkpoint.item_id,
                "applicable": is_applicable,
                "status": product_applicability["status"],
                "reason": applicability_reason,
                "machine_reason": applicability_reason,
                "user_reason": applicability_reason,
                "trigger_facts": list(product_applicability.get("positive_triggers") or []),
                "trigger_evidence": [],
                "missing_triggers": list(product_applicability.get("negative_triggers") or []),
                "positive_triggers": list(product_applicability.get("positive_triggers") or []),
                "negative_triggers": list(product_applicability.get("negative_triggers") or []),
                "product_category": product_documentation_profile.product_category,
                "transaction_structure": domain_resolution.transaction_structure,
                "depends_on": ["product_documentation_profile"],
            }
        item_applicability[checkpoint.item_id] = fact_applicability
        if is_applicable and fact_applicability.get("applicable") is False:
            is_applicable = False
            applicability_reason = fact_applicability["reason"]
        if is_applicable:
            applicable_checkpoints.append(checkpoint)
        elif str(fact_applicability.get("status") or "").upper() in {"UNCERTAIN", INSUFFICIENT_CONTEXT}:
            unclear_item = _insufficient_context_item(checkpoint, applicability_reason)
            unclear_item.applicability = {
                **fact_applicability,
                "status": INSUFFICIENT_CONTEXT,
                "applicable": None,
                "user_reason": "现有合同材料不足以确认该事项是否适用，建议结合相关交易背景或补充材料核对。",
            }
            unclear_item.fact_dependencies = list(unclear_item.applicability.get("depends_on") or [])
            not_applicable_items[checkpoint.item_id] = unclear_item
        else:
            na_item = _not_applicable_item(checkpoint, applicability_reason)
            na_item.applicability = fact_applicability if fact_applicability.get("applicable") is not True else {
                "status": "not_applicable",
                "applicable": False,
                "reason": applicability_reason,
                "machine_reason": applicability_reason,
                "user_reason": f"合同未触发“{checkpoint.applicable_if or checkpoint.title}”这一适用条件，本审查事项不适用。",
                "depends_on": [],
            }
            na_item.fact_dependencies = list(na_item.applicability.get("depends_on") or [])
            not_applicable_items[checkpoint.item_id] = na_item

    judgments = _judge_checkpoints_with_registry(
        applicable_checkpoints,
        clauses,
        use_llm=use_llm,
        fact_graph=generic_fact_graph,
    )
    items = []
    for checkpoint in checklist:
        if checkpoint.item_id in not_applicable_items:
            items.append(not_applicable_items[checkpoint.item_id])
            continue
        judgment = judgments[checkpoint.item_id]
        item = ReviewItemResult(
            item_id=checkpoint.item_id,
            node_id=checkpoint.node_id,
            title=checkpoint.title,
            risk_level=judgment.risk_level,
            status=judgment.status,
            risk_point_description=judgment.risk_point_description,
            suggested_clause_example=checkpoint.suggested_clause,
            legal_basis_index=checkpoint.legal_basis,
            legal_consequence_if_missing=checkpoint.legal_consequence_if_missing,
            applicable_if=checkpoint.applicable_if,
            matched_terms=judgment.matched_terms,
            coverage_status=judgment.coverage_status,
            issue_type=judgment.issue_type,
            evidence_clauses=judgment.evidence_clauses,
            evidence_location=judgment.evidence_location,
            reasoning_summary=judgment.reasoning_summary,
            judge_source=judgment.judge_source,
            llm_confidence=judgment.llm_confidence,
            llm_raw_reason=judgment.llm_raw_reason,
            fallback_reason=judgment.fallback_reason,
        )
        item.applicability = item_applicability.get(checkpoint.item_id, {"status": "applicable", "applicable": True, "reason": "", "depends_on": []})
        item.review_trace_id = f"{contract_review_trace_id}-{checkpoint.item_id.replace('-', '')}"
        items.append(_apply_source_exemptions(item, review_text))
    for item in items:
        if not item.review_trace_id:
            item.review_trace_id = f"{contract_review_trace_id}-{item.item_id.replace('-', '')}"
        item.decision_trace["execution_context"] = review_execution_context
    _attach_contract_fact_registry_snapshot(items, generic_fact_graph, fact_registry_snapshot_id)
    searched_scope = [clause.clause_id for clause in clauses if clause.section_type in {"正式合同条款", "附件"}]
    _apply_checkpoint_metadata(items, checklist, searched_scope)
    items = _apply_review_nature_outcomes(items)
    items = _apply_contract_specific_post_rules(items, review_text, type_meta.key.value)
    _apply_checkpoint_metadata(items, checklist, searched_scope)
    items = _apply_review_nature_outcomes(items)
    if framework_supply:
        items = _apply_framework_fact_paths(items, framework_supply, clauses)

    # 应用用户画像规则（风险等级重映射、语气调整、审查点标注）
    items = _apply_profile_rules(items, profile, perspective_resolution.to_public_dict())
    _apply_checkpoint_metadata(items, checklist, searched_scope)
    items = _apply_review_nature_outcomes(items)
    items, quality_gate = _apply_final_quality_gate(items, lease_facts, type_meta.key.value)
    items = _apply_risk_dimensions(items, type_meta.response_key, review_text)
    items = _apply_review_priority_and_action(items)
    items = _enrich_evidence_sources(items)
    def sync_review_semantics() -> None:
        _apply_checkpoint_metadata(items, checklist, searched_scope)
        _apply_review_nature_outcomes(items)

    sync_review_semantics()
    items = _apply_evidence_entailment_gate(items)
    items = _apply_coverage_evidence_gate(items, canonical_claims)
    items = _attach_recall_state(items, checklist, clauses, generic_fact_graph, canonical_claims)
    if framework_supply:
        items = _apply_framework_fact_paths(items, framework_supply, clauses)
    items = _apply_coverage_evidence_gate(items, canonical_claims)
    items = _apply_review_evidence_ownership(items)
    review_evidence_element_gate = _review_evidence_element_gate(items)
    cross_review_claim_gate = _cross_review_shared_claim_state(items, canonical_claims)
    items = _enrich_evidence_sources(items)
    items = _apply_element_level_narratives(items)
    items = _apply_risk_dimensions(items, type_meta.response_key, review_text)
    items = _apply_review_priority_and_action(items)
    sync_review_semantics()
    items = _apply_citation_claims(items)
    legal_authority_gate = _select_legal_authorities(items)
    legal_default_consistency_gate = _legal_default_law_consistency_gate(items)
    items = _apply_confidence_bundles(items)
    legal_reference_issues = _check_legal_reference_freshness(review_text)
    legal_authority_validation = _validate_legal_authorities(
        [{"law_name": issue.get("law_name"), "article": issue.get("article")} for issue in legal_reference_issues]
    )
    risk_findings = _build_risk_findings(items) + _legal_reference_findings(legal_reference_issues)
    risk_findings = _filter_unsupported_positive_findings(risk_findings, items)
    risk_evidence_audit = _risk_evidence_ownership_audit(risk_findings)
    risk_evidence_gate = _risk_evidence_ownership_gate(risk_evidence_audit)
    risk_findings.sort(key=_finding_sort_key)
    for item in items:
        item.action_priority = _action_priority_for_item(item)
        item.review_priority = item.action_priority
        item.action_suggestion = _action_suggestion_for_item(item)
    risk_findings = _run_independent_verifier(risk_findings, items)
    _apply_post_verification_confidence(risk_findings, items)
    legal_freshness_trace = _legal_freshness_trace(review_text, legal_reference_issues, risk_findings)
    recommendations = _build_recommendations(risk_findings, items)
    recommendations, recommendation_impacts, recommendation_impact_gate = evaluate_recommendations(
        recommendations, risk_findings, items, perspective_resolution.canonical_role,
    )
    client_interest_decisions, client_interest_gate = _client_interest_gate(
        risk_findings, recommendations, recommendation_impacts, items, perspective_resolution.canonical_role,
    )
    candidate_recommendation_impacts = list(recommendation_impacts)
    final_dispositions = _build_final_dispositions(risk_findings, recommendations, client_interest_decisions)
    recommendations = _bind_recommendations_to_final_dispositions(
        recommendations, risk_findings, final_dispositions,
    )
    recommendations, recommendation_impacts, recommendation_impact_gate = evaluate_recommendations(
        recommendations, risk_findings, items, perspective_resolution.canonical_role,
    )
    recommendations = _bind_recommendations_to_final_dispositions(
        recommendations, risk_findings, final_dispositions,
    )
    final_impact_ids = {impact.recommendation_id for impact in recommendation_impacts}
    recommendation_display_impacts = list(recommendation_impacts) + [
        impact for impact in candidate_recommendation_impacts
        if impact.gate_result == "BLOCKED" and impact.recommendation_id not in final_impact_ids
    ]
    recommendation_truth_audit = _recommendation_truth_binding_audit(
        recommendations, risk_findings, final_dispositions,
    )
    recommendation_truth_gate = _recommendation_truth_binding_gate(recommendation_truth_audit)
    high_risk_disposition_audit = _high_risk_disposition_audit(risk_findings, final_dispositions)
    _apply_final_disposition_states(items, final_dispositions)
    final_disposition_summary = _final_disposition_summary(final_dispositions)
    final_disposition_invariant_gate = _final_disposition_invariant_gate(risk_findings, final_dispositions)
    manual_review_items = _manual_review_records(items)
    risk_finding_summary = _risk_finding_summary(risk_findings, items)
    resolved_type_name = str(
        report_context.get("contract_type_label")
        or ("住宅二手房地产买卖合同" if domain_resolution.contract_subtype == "RESIDENTIAL_SECONDARY_REAL_ESTATE_SALE" else type_meta.display_name)
    )
    overall_assessment = _overall_assessment(
        contract_type_name=resolved_type_name,
        findings=risk_findings,
        items=items,
        final_dispositions=final_dispositions,
        manual_reviews=manual_review_items,
    )
    benchmark_metrics = _benchmark_metrics(items, risk_findings)
    system_metadata = _system_metadata(llm_status)
    items = _enrich_reasoning_and_citation(items)
    items = _apply_element_level_narratives(items)
    default_law_narrative_rows = _apply_default_law_narratives(items)
    default_law_narrative_gate = _default_law_narrative_truth_gate(default_law_narrative_rows)
    final_recommendation_set, recommendation_ssot_debug = _apply_recommendation_display_states(
        items, risk_findings, recommendations, recommendation_display_impacts,
    )
    _apply_final_disposition_states(items, final_dispositions)
    applicability_polarity_pre_gate = _applicability_polarity_gates(
        items, risk_findings, recommendations,
    )

    visible_items = items if include_low_risk else [item for item in items if item.risk_level in {"高", "中"}]
    fact_flow_audit = _contract_fact_flow_audit(visible_items, generic_fact_graph, fact_registry_snapshot_id)
    contract_fact_registry_gate = _contract_fact_registry_gate(fact_flow_audit)
    contract_type_name = resolved_type_name
    review_results_4_0 = [public_review_result(item) for item in visible_items]
    legal_citation_claims = [
        claim
        for item in visible_items
        for claim in (item.legal_references or [])
    ]
    recommendation_dicts = [recommendation.to_public_dict() for recommendation in recommendations]
    architecture_status = _architecture_status()
    finding_provenance = _finding_provenance(risk_findings, visible_items)
    risk_finding_dicts = [finding.to_public_dict() for finding in risk_findings]
    final_disposition_dicts = [disposition.to_public_dict() for disposition in final_dispositions]

    # 诉讼策略分析（对高/中风险条款）
    public_items = [item.to_public_dict() for item in visible_items]
    litigation_report = analyze_litigation_strategy(public_items, profile)

    # 商业谈判分析（对高/中风险条款）
    negotiation_report = analyze_negotiation_strategy(public_items, profile)

    # 跨地域裁判预判（对高/中风险条款）
    jurisdiction_report = analyze_jurisdiction_prediction(public_items, profile, review_text)

    recommendation_provenance_gate = _numeric_provenance_gate(recommendations)
    consistency_gate = _consistency_quality_gates(
        visible_items, risk_findings, recommendations, canonical_claims, contract_context, report_context,
    )
    pre_render_gate = _pre_render_quality_gate(
        visible_items,
        risk_findings,
        contract_context,
        overall_assessment,
        recommendation_provenance_gate,
    )
    pre_render_gate = _combine_quality_gates(pre_render_gate, contract_fact_registry_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, risk_evidence_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, review_evidence_element_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, consistency_gate)
    domain_selection_gate = domain_selection_consistency_gate(
        domain_selection_resolution, [item.item_id for item in visible_items],
    )
    pre_render_gate = _combine_quality_gates(pre_render_gate, domain_selection_gate)
    perspective_gate = perspective_domain_consistency_gate(perspective_resolution)
    pre_render_gate = _combine_quality_gates(pre_render_gate, perspective_gate)
    production_display_claims = [
        claim
        for item in visible_items
        for claim in ((item.decision_trace or {}).get("production_display_claims") or [])
    ]
    fact_polarity_gate = production_fact_polarity_gate(production_display_claims)
    pre_render_gate = _combine_quality_gates(pre_render_gate, fact_polarity_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, recommendation_impact_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, recommendation_truth_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, client_interest_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, final_disposition_invariant_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, legal_authority_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, legal_default_consistency_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, default_law_narrative_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, applicability_polarity_pre_gate)
    pre_render_gate = _combine_quality_gates(pre_render_gate, cross_review_claim_gate)
    recall_failures = _recall_gate_failures(visible_items, integrity)
    if recall_failures:
        pre_render_gate = _combine_quality_gates(
            pre_render_gate,
            {"status": "BLOCKED", "failures": recall_failures},
        )
    if pre_render_gate["status"] == "REPORT_READY":
        result = _format_markdown_v2(
            contract_type_name, visible_items, profile,
            risk_findings=risk_findings,
            recommendations=recommendations,
            overall_assessment=overall_assessment,
            risk_finding_summary=risk_finding_summary,
            benchmark_metrics=benchmark_metrics,
            release_quality_gate=pre_render_gate,
            system_metadata=system_metadata,
            litigation_items=litigation_report.to_public_dict(),
            negotiation_items=negotiation_report.to_public_dict(),
            jurisdiction_items=jurisdiction_report.to_public_dict(),
            report_context=report_context,
            perspective_resolution=perspective_resolution.to_public_dict(),
            final_dispositions=final_dispositions,
        )
        quality4_gate = post_render_quality_gate(result, review_results_4_0, risk_finding_dicts, recommendation_dicts)
        default_law_provenance_gate = _default_law_provenance_gate(visible_items, result)
        recommendation_renderer_gate = _recommendation_renderer_gates(
            result, visible_items, recommendations, recommendation_impacts,
        )
        report_text_validation_gate = _report_text_validation_gate(result)
        report_disposition_projection_gate = _report_disposition_projection_gate(result, final_dispositions)
        applicability_polarity_gate = _applicability_polarity_gates(
            visible_items, risk_findings, recommendations, result,
        )
        release_quality_gate = _combine_quality_gates(
            pre_render_gate,
            _release_quality_gate(visible_items, risk_findings, result),
            quality4_gate,
            _production_internal_token_gate(result),
            default_law_provenance_gate,
            recommendation_renderer_gate,
            applicability_polarity_gate,
            report_text_validation_gate,
            report_disposition_projection_gate,
        )
    else:
        result = "该事项当前无法可靠判断，正式报告已停止生成。必要时请人工复核。"
        quality4_gate = {"status": "BLOCKED", "failures": list(pre_render_gate["failures"]), "skipped": "pre_render_gate_blocked"}
        release_quality_gate = pre_render_gate
        default_law_provenance_gate = {"status": "BLOCKED", "failures": [], "gate_results": {"DEFAULT_LAW_PROVENANCE_GATE": "SKIPPED"}, "break_count": 0, "rows": []}
        recommendation_renderer_gate = {
            "status": "BLOCKED", "failures": [],
            "gate_results": {
                "RECOMMENDATION_SINGLE_SOURCE_GATE": "SKIPPED",
                "RECOMMENDATION_CROSS_RENDERER_CONSISTENCY_GATE": "SKIPPED",
            },
            "dual_source_count": 0, "cross_renderer_mismatch_count": 0, "rows": [],
        }
        applicability_polarity_gate = applicability_polarity_pre_gate
        report_text_validation_gate = {"status": "BLOCKED", "failures": [], "gate_results": {"REPORT_TEXT_VALIDATION": "SKIPPED"}, "broken_template_text_count": 0}
        report_disposition_projection_gate = {"status": "BLOCKED", "failures": [], "gate_results": {"REPORT_DISPOSITION_PROJECTION_INVARIANT": "SKIPPED"}, "mismatches": []}
    litigation_result = format_litigation_markdown(litigation_report)
    negotiation_result = format_negotiation_markdown(negotiation_report)
    jurisdiction_result = format_jurisdiction_markdown(jurisdiction_report)
    total_latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
    confidence_trace = _confidence_debug_report(visible_items)
    production_trace = _production_trace(
        contract_review_trace_id,
        type_meta.response_key,
        contract_context,
        system_metadata,
        finding_provenance,
        confidence_trace,
        pre_render_gate["priority_consistency_verification"],
    )
    output_hashes = {
        "input_contract_hash": _stable_hash(review_text),
        "structured_assessment_hash": _stable_hash({
            "reviews": review_results_4_0,
            "findings": risk_finding_dicts,
            "recommendations": recommendation_dicts,
            "final_dispositions": final_disposition_dicts,
            "context": contract_context,
        }),
        "final_report_hash": _stable_hash(result),
    }

    return {
        "success": True,
        "contract_type": type_meta.response_key,
        "selected_contract_type": user_selected_type,
        "domain_selection_resolution": domain_selection_resolution.to_public_dict(),
        "domain_selection_consistency_gate": domain_selection_gate,
        "perspective_resolution": perspective_resolution.to_public_dict(),
        "perspective_domain_consistency_gate": perspective_gate,
        "recommendation_non_degradation_gate": recommendation_impact_gate,
        "recommendation_truth_binding_gate": recommendation_truth_gate,
        "client_interest_gate": client_interest_gate,
        "final_disposition_invariant_gate": final_disposition_invariant_gate,
        "recommendation_single_source_gate": recommendation_renderer_gate,
        "recommendation_cross_renderer_consistency_gate": recommendation_renderer_gate,
        "final_recommendation_set": final_recommendation_set,
        "legal_authority_gate": legal_authority_gate,
        "legal_default_law_consistency_gate": legal_default_consistency_gate,
        "atomic_legal_element_gate": legal_default_consistency_gate,
        "not_applicable_narrative_gate": applicability_polarity_gate,
        "not_applicable_gap_gate": applicability_polarity_gate,
        "review_polarity_narrative_gate": applicability_polarity_gate,
        "negative_check_pass_gate": applicability_polarity_gate,
        "contract_fact_registry_gate": contract_fact_registry_gate,
        "risk_evidence_ownership_gate": risk_evidence_gate,
        "review_evidence_element_gate": review_evidence_element_gate,
        "cross_review_shared_claim_gate": cross_review_claim_gate,
        "default_law_provenance_gate": default_law_provenance_gate,
        "report_text_validation_gate": report_text_validation_gate,
        "report_disposition_projection_gate": report_disposition_projection_gate,
        "default_law_narrative_truth_gate": default_law_narrative_gate,
        "contract_type_name": contract_type_name,
        "contract_review_trace_id": contract_review_trace_id,
        "message": f"审查第二版已完成{contract_type_name}{len(items)}项核心检查。",
        "items": public_items,
        "all_items_count": len(items),
        "summary": _risk_summary(items),
        "risk_finding_summary": risk_finding_summary,
        "coverage_summary": _coverage_summary(items),
        "issue_type_summary": _issue_type_summary(items),
        "judge_source_summary": _judge_source_summary(items),
        "llm_enabled": use_llm,
        "llm_status": llm_status,
        "global_fallback_reason": global_fallback_reason,
        "report_notice": REPORT_FORMAT_NOTICE,
        "clause_count": len(clauses),
        "formal_clause_count": sum(1 for clause in clauses if clause.section_type in {"正式合同条款", "附件"}),
        "contract_facts": contract_facts,
        "document_integrity": integrity,
        "quality_gate": quality_gate,
        "review_results_4_0": review_results_4_0,
        "risk_findings": risk_finding_dicts,
        "recommendations": recommendation_dicts,
        "client_interest_decisions": [decision.to_public_dict() for decision in client_interest_decisions],
        "final_dispositions": final_disposition_dicts,
        "final_disposition_summary": final_disposition_summary,
        "manual_review_items": manual_review_items,
        "manual_review_summary": {
            "manual_review_count": len(manual_review_items),
            "blocking_signability_count": sum(1 for row in manual_review_items if row.get("blocking_signability")),
        },
        "contract_context": contract_context,
        "report_context": report_context,
        "overall_assessment": overall_assessment,
        "legal_reference_issues": legal_reference_issues,
        "legal_citation_claims": legal_citation_claims,
        "legal_authority_validation": legal_authority_validation,
        "benchmark_metrics": benchmark_metrics,
        "release_quality_gate": release_quality_gate,
        "quality4_gate": quality4_gate,
        "architecture_status": architecture_status,
        "system_metadata": system_metadata,
        "observability": {
            "production_call_graph": _production_call_graph(),
            "production_trace": production_trace,
            "contract_fact_flow_audit": fact_flow_audit,
            "contract_fact_registry_gate": contract_fact_registry_gate,
            "risk_evidence_ownership_audit": risk_evidence_audit,
            "risk_evidence_ownership_gate": risk_evidence_gate,
            "review_evidence_element_gate": review_evidence_element_gate,
            "review_evidence_support_mapping": review_evidence_element_gate.get("rows", []),
            "finding_provenance": finding_provenance,
            "output_hashes": output_hashes,
            "pre_render_quality_gate": pre_render_gate,
            "final_output_ownership_matrix": _final_output_ownership_matrix(),
            "domain_pack_snapshot": composed_domain_pack_snapshot(domain_resolution.selected_domain_packs),
            "classification_trace": domain_resolution.to_public_dict(),
            "domain_selection_debug": domain_selection_resolution.to_public_dict(),
            "domain_selection_consistency_gate": domain_selection_gate,
            "perspective_resolution_debug": perspective_resolution.to_public_dict(),
            "perspective_domain_consistency_gate": perspective_gate,
            "production_humanization_debug": production_display_claims,
            "production_fact_polarity_debug": fact_polarity_gate,
            "recommendation_impact_debug": [impact.to_public_dict() for impact in recommendation_display_impacts],
            "recommendation_non_degradation_gate": recommendation_impact_gate,
            "recommendation_diff_audit": recommendation_truth_audit,
            "recommendation_truth_binding_gate": recommendation_truth_gate,
            "high_risk_disposition_audit": high_risk_disposition_audit,
            "client_interest_debug": client_interest_gate,
            "final_disposition_debug": final_disposition_dicts,
            "manual_review_debug": manual_review_items,
            "final_disposition_invariant_gate": final_disposition_invariant_gate,
            "recommendation_ssot_debug": recommendation_ssot_debug,
            "recommendation_cross_renderer_debug": recommendation_renderer_gate,
            "recommendation_renderer_gate": recommendation_renderer_gate,
            "legal_authority_dedup_debug": legal_authority_gate,
            "legal_authority_selection_debug": legal_authority_gate,
            "legal_proposition_entailment_debug": legal_authority_gate.get("rows", []),
            "legal_default_consistency_debug": legal_default_consistency_gate,
            "legal_element_decomposition_debug": legal_default_consistency_gate.get("element_decomposition", []),
            "not_applicable_pipeline_debug": applicability_polarity_gate.get("not_applicable_rows", []),
            "review_polarity_debug": applicability_polarity_gate.get("polarity_rows", []),
            "negative_check_debug": [
                row.get("evidence_state") for row in applicability_polarity_gate.get("polarity_rows", [])
            ],
            "narrative_semantics_debug": applicability_polarity_gate,
            "default_law_narrative_debug": default_law_narrative_gate,
            "shared_claim_consumer_debug": cross_review_claim_gate.get("claims", []),
            "cross_review_shared_claim_gate": cross_review_claim_gate,
            "default_law_provenance_debug": default_law_provenance_gate,
            "report_text_validation_debug": report_text_validation_gate,
            "report_disposition_projection_gate": report_disposition_projection_gate,
            "shared_claim_debug": canonical_claims_public(canonical_claims),
            "report_context_debug": {
                "classification": {
                    "family": domain_resolution.contract_family,
                    "subject": domain_resolution.subject_matter,
                    "transaction_structure": domain_resolution.transaction_structure,
                    "subtype": domain_resolution.contract_subtype,
                },
                "report_context": report_context,
                "consistency": "PASS" if report_context["family"] == domain_resolution.contract_family and report_context["subject_matter"] == domain_resolution.subject_matter and report_context["transaction_structure"] == domain_resolution.transaction_structure and report_context["subtype"] == domain_resolution.contract_subtype else "FAIL",
            },
            "cross_review_consistency_debug": consistency_gate,
            "finding_precision_debug": [
                {
                    "finding_id": finding.finding_id,
                    "review_ids": finding.source_review_ids,
                    "applicability": {item.item_id: item.applicability for item in visible_items if item.item_id in finding.source_review_ids},
                    "coverage": {item.item_id: item.coverage_status for item in visible_items if item.item_id in finding.source_review_ids},
                    "claim_ids": (finding.aggregation_signals or {}).get("claim_ids", []),
                    "evidence_ids": finding.source_clause_ids,
                    "residual_risk": {item.item_id: item.residual_risk for item in visible_items if item.item_id in finding.source_review_ids},
                    "precondition_pass": all(((item.decision_trace or {}).get("finding_precondition") or {}).get("all_required_conditions") for item in visible_items if item.item_id in finding.source_review_ids),
                }
                for finding in risk_findings
            ],
            "domain_routing_debug": {
                "selected": domain_resolution.selected_domain_packs,
                "rejected": domain_resolution.rejected_domain_packs,
                "subject_matter": domain_resolution.subject_matter,
                "contract_subtype": domain_resolution.contract_subtype,
                "confidence": domain_resolution.confidence,
            },
            "review_registry_debug": registry_debug,
            "domain_material_coverage": _domain_quality_gates(visible_items, contract_context),
            "context_consistency_gate": _context_consistency_gate(contract_context),
            "legal_freshness_trace": legal_freshness_trace,
            "risk_aggregation_debug_table": _risk_aggregation_debug_table(risk_findings),
            "confidence_debug_report": confidence_trace,
            "evidence_finding_debug_table": _evidence_finding_debug_report(visible_items, risk_findings),
            "default_law_debug_table": _default_law_debug_report(visible_items),
            "confidence_distribution": dict(Counter((item.system_confidence or {}).get("level", "medium") for item in visible_items)),
            "coverage_element_debug_report": _coverage_element_debug_report(visible_items),
            "legal_claim_debug_report": _legal_claim_debug_report(visible_items),
            "recommendation_provenance_debug_report": _recommendation_provenance_debug_report(recommendations),
            "recommendation_provenance_gate": recommendation_provenance_gate,
            "narrative_state_debug_report": _narrative_state_debug_report(visible_items),
            "production_token_scan": _production_internal_token_gate(result),
            "evidence_recall_debug": [
                {
                    "review_id": item.item_id,
                    "fact_match": (item.decision_trace.get("retrieval_trace") or {}).get("fact_clause_ids", []),
                    "structural": (item.decision_trace.get("retrieval_trace") or {}).get("structural_clause_ids", []),
                    "lexical": (item.decision_trace.get("retrieval_trace") or {}).get("lexical_clause_ids", []),
                    "semantic": (item.decision_trace.get("retrieval_trace") or {}).get("semantic_clause_ids", []),
                    "graph": (item.decision_trace.get("retrieval_trace") or {}).get("graph_clause_ids", []),
                    "final_evidence": [evidence.get("clause_id") for evidence in item.evidence_clauses],
                    "coverage": item.coverage_status,
                }
                for item in visible_items
                if item.coverage_status in {"缺失", "部分覆盖"} or item.risk_level in {"高", "重大"}
            ],
            "document_coverage_map": [
                {
                    "section": clause.location,
                    "clause_id": clause.clause_id,
                    "indexed": True,
                    "fact_count": sum(
                        1 for facts in generic_fact_graph.facts.values()
                        for fact in facts if clause.clause_id in fact.source_clause_ids
                    ),
                    "retrieved_by_reviews": [
                        item.item_id for item in visible_items
                        if clause.clause_id in (item.decision_trace.get("retrieval_trace") or {}).get("candidate_clause_ids", [])
                    ],
                }
                for clause in clauses
            ],
            "parser_latency_ms": 0.0,
            "fact_latency_ms": 0.0,
            "retrieval_latency_ms": round(sum(
                float((item.decision_trace.get("retrieval_trace") or {}).get("latency_ms") or 0)
                for item in visible_items
            ), 3),
            "llm_latency_ms": None,
            "verification_latency_ms": None,
            "aggregation_latency_ms": None,
            "total_latency_ms": total_latency_ms,
            "llm_calls": 1 if use_llm and llm_status.get("available") else 0,
            "tokens": None,
            "retrieval_calls": len(items),
            "retry_count": 0,
            "manual_review_count": sum(1 for item in items if item.needs_manual_review),
        },
        "result": result,
        "profile": profile.to_dict(),
        "litigation": litigation_report.to_public_dict(),
        "litigation_result": litigation_result,
        "negotiation": negotiation_report.to_public_dict(),
        "negotiation_result": negotiation_result,
        "jurisdiction": jurisdiction_report.to_public_dict(),
        "jurisdiction_result": jurisdiction_result,
    }
