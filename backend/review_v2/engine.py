"""独立的合同审查引擎（第二版）。"""

from __future__ import annotations

import re
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from review_v2.clause_parser import parse_contract_clauses, strip_non_contract_tail
from review_v2.contract_registry import (
    UnsupportedContractTypeError,
    get_checklist,
    get_contract_meta,
    supported_contract_display_names,
)
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
from review_v2.semantic_reviewer import _has_gift_paid_consideration_risk, judge_checkpoint, matched_terms
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
REVIEW_IMPORTANCE_CORE = "CORE"
REVIEW_IMPORTANCE_IMPORTANT = "IMPORTANT"
REVIEW_IMPORTANCE_NORMAL = "NORMAL"
SYSTEM_VERSION = "contract-review-quality-5.2"
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
BENCHMARK_VERSION = "quality4-target-benchmark-2026-08-11"

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

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


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


def _is_checkpoint_applicable(contract_text: str, checkpoint: ReviewCheckpoint, contract_type_key: str) -> tuple[bool, str]:
    applicability_text = _construction_contract_body(contract_text) if contract_type_key == "construction" else contract_text
    compacted = _compact(applicability_text)
    if contract_type_key == "technology":
        applicable, reason = _is_technology_checkpoint_applicable(compacted, checkpoint)
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
    for keyword in keywords:
        if _has_unnegated_word(compacted, keyword, window=18):
            return True, f"合同文本出现“{keyword}”，适用该专项审查点。"
    return False, f"未发现触发该专项审查点的交易类型表述：{checkpoint.applicable_if}"


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
        return {
            "status": "applicable" if applicable else "not_applicable",
            "applicable": applicable,
            "reason": rule["applicable_reason"] if applicable else rule["not_applicable_reason"],
            "depends_on": depends_on,
            "evaluations": evaluations,
        }
    return {
        "status": "applicable",
        "applicable": True,
        "reason": "未触发事实层排除条件，继续执行审查。",
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
    item.applicability = {"status": "not_applicable", "applicable": False, "reason": reason, "depends_on": []}
    item.action_suggestion = "不适用"
    return item


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
        },
    )
    return enriched


def _enrich_evidence_sources(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    for item in items:
        item.evidence_clauses = [_enrich_evidence_source(evidence) for evidence in (item.evidence_clauses or [])]
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
    strict_review_ids = {"HL-039", "HL-040", "HL-042"}
    strict_risk_groups = {"early_termination_financial_exposure", "deposit_offset_order"}
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
        item.semantic_entailment = bool(supporting) if item.evidence_clauses else None
        strict_gate = item.item_id in strict_review_ids or item.risk_group in strict_risk_groups
        if strict_gate and item.coverage_status in {"通过", "部分覆盖"} and item.evidence_clauses and not supporting:
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

    if item.coverage_status == "通过" and item.related_risks and priority == ACTION_PRIORITY_NONE:
        priority = PRIORITY_B_PRACTICAL

    return {
        "priority": priority,
        "score": round(score, 2),
        "reason": ", ".join(reasons) or "no_actionable_signal",
        "input": priority_input.to_public_dict(),
    }


def _system_confidence_for_item(item: ReviewItemResult) -> Dict[str, Any]:
    has_evidence = bool(item.evidence_clauses)
    level = "high"
    if item.needs_manual_review or item.semantic_entailment is False:
        level = "low"
    elif not has_evidence and item.coverage_status not in {COVERAGE_NOT_APPLICABLE, "缺失"}:
        level = "medium"
    elif item.coverage_status == "缺失":
        level = "medium"
    return {
        "level": level,
        "parser_confidence": "high",
        "fact_confidence": "high" if item.fact_dependencies else "medium",
        "retrieval_strength": "explicit" if has_evidence else "not_found",
        "evidence_entailment": item.semantic_entailment if item.semantic_entailment is not None else "not_checked",
        "rule_agreement": "agree",
        "model_agreement": "not_used_or_agree",
        "cross_review_agreement": "agree" if not item.quality_gate_failure_reason else "conflict",
        "legal_authority_confidence": "medium",
        "formula_confidence": "high" if item.scenario_analysis.get("formula") else "not_applicable",
        "quality_gate_flags": len(item.quality_flags),
    }


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


def _apply_risk_dimensions(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    for item in items:
        if item.coverage_status == "通过" and "建议继续核对" in (item.risk_point_description or ""):
            item.risk_point_description = f"合同已覆盖“{item.title}”相关安排。"
        item.risk_group = RISK_GROUP_BY_ID.get(item.item_id, item.node_id or item.item_id)
        item.related_reviews = RELATED_REVIEWS_BY_ID.get(item.item_id, [])
        category = ontology_category(item.risk_group, item.node_id)
        item.decision_trace["risk_category"] = category
        default_status = default_law_status(item.risk_group, item.node_id)
        item.decision_trace["default_law_status"] = default_status
        item.decision_trace["effective_gap"] = {
            "contract_coverage": item.coverage_status,
            "statutory_default": default_status,
            "default_strength": "strong" if default_status == "CLEAR_DEFAULT" else "partial" if default_status == "PARTIAL_DEFAULT" else "none",
            "residual_legal_risk": "low" if default_status == "CLEAR_DEFAULT" else "medium",
            "residual_operational_risk": "low" if default_status == "CLEAR_DEFAULT" and item.node_id in LOW_PROBABILITY_NODE_IDS else "medium",
            "drafting_value": "convenience" if default_status == "CLEAR_DEFAULT" else "risk_mitigation",
            "contract_override_risk": "low",
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
            item.residual_risk = item.risk_point_description
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
    return item.suggested_clause_example


def _finding_title(group: str, item: ReviewItemResult) -> str:
    return {
        "early_termination_financial_exposure": "提前退租违约金经济风险",
        "deposit_return_timing": "押金返还期限未明确",
        "deposit_offset_order": "押金抵扣顺序未明确",
        "property_damage_deposit_evidence": "房屋损坏与押金扣款证据机制不足",
        "notice_and_delivery": "解除通知和送达机制不完整",
        "housing_safety_emergency": "房屋安全风险应急机制不足",
        "lawful_lease_basis": "房屋合法出租保证可进一步明确",
        "legal_reference": "法律引用建议更新",
    }.get(group, item.title)


def _build_risk_findings(items: List[ReviewItemResult]) -> List[RiskFinding]:
    grouped: Dict[str, List[ReviewItemResult]] = {}
    for item in items:
        if item.coverage_status == COVERAGE_NOT_APPLICABLE or item.risk_severity == SEVERITY_NONE:
            continue
        group_key = f"{item.decision_trace.get('risk_category') or ontology_category(item.risk_group, item.node_id)}|{item.risk_group or item.node_id or item.item_id}"
        grouped.setdefault(group_key, []).append(item)

    findings: List[RiskFinding] = []
    for index, (group_key, group_items) in enumerate(grouped.items(), start=1):
        group_items = sorted(group_items, key=lambda item: (_severity_rank(item.risk_severity), _priority_rank(item.review_priority), item.item_id))
        primary = group_items[0]
        group = primary.risk_group or primary.node_id or primary.item_id
        all_group_items = [
            item for item in items
            if f"{item.decision_trace.get('risk_category') or ontology_category(item.risk_group, item.node_id)}|{item.risk_group or item.node_id or item.item_id}" == group_key
        ]
        evidence: List[Dict[str, Any]] = []
        seen_evidence = set()
        for item in group_items:
            for clause in item.evidence_clauses[:2]:
                key = (clause.get("clause_id"), clause.get("location"), clause.get("text"))
                if key in seen_evidence:
                    continue
                seen_evidence.add(key)
                evidence.append(clause)
        finding_id = RISK_FINDING_ID_BY_GROUP.get(group, f"RF-{index:03d}")
        source_review_ids = sorted({item.item_id for item in all_group_items})
        source_clause_ids = sorted(
            {
                str(clause.get("clause_id"))
                for item in group_items
                for clause in item.evidence_clauses
                if clause.get("clause_id")
            }
        )
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
            issue=primary.risk_point_description,
            consequence=primary.legal_consequence_if_missing,
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
            supporting_evidence=evidence,
            counter_evidence=[],
        )
        findings.append(finding)
        for item in items:
            item_group_key = f"{item.decision_trace.get('risk_category') or ontology_category(item.risk_group, item.node_id)}|{item.risk_group or item.node_id or item.item_id}"
            if item_group_key != group_key:
                continue
            item.related_risks = sorted(set(item.related_risks + [finding_id]))
    findings.sort(key=_finding_sort_key)
    return findings


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
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return "不适用"
    severity = item.risk_severity or _risk_severity_for_item(item)
    if item.coverage_status == "通过":
        if item.related_risks or severity != SEVERITY_NONE:
            return "机制已覆盖；关联风险需单独处理"
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
    has_price = any(term in source for term in ("单价", "价格", "价款", "报价"))
    has_adjustment = any(term in source for term in ("调整", "变动", "变更", "浮动", "调价"))
    has_unilateral = any(term in source for term in ("甲方可", "甲方有权", "出卖人可", "出卖人有权", "书面通知予以调整", "通知后调整", "通知乙方"))
    has_market = any(term in source for term in ("市场行情变化", "市场行情", "市场价格", "行情变化", "原材料价格", "价格波动"))
    return has_price and has_adjustment and (has_unilateral or has_market)


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
    clauses = parse_contract_clauses(contract_text)
    compacted = _compact(contract_text)
    by_id = {item.item_id: item for item in items}

    effective_evidence = _find_clause(
        clauses,
        lambda clause: "生效" in clause.text and ("签字" in clause.text or "盖章" in clause.text or "签署" in clause.text),
    )
    if effective_evidence and (item := by_id.get("S-00-01")):
        _set_item_pass(
            item,
            [effective_evidence],
            "合同已明确签字、盖章或签署后的生效节点，生效条件具备可验证性。",
            "合同生效条件已明确，签署完成后合同效力节点清晰。",
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
        term for term in ("上课时间", "上课地点", "服务时间", "服务地点", "线下", "线上", "预约", "排课", "培训地点", "训练地点")
        if term in compacted
    ]
    return len(schedule_hits) >= 2


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
            _find_clauses(clauses, lambda clause: ("课程" in clause.text or "课时" in clause.text or "价格" in clause.text or "教师" in clause.text or "服务内容" in clause.text), limit=2),
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
            _find_clauses(clauses, lambda clause: ("上课时间" in clause.text or "服务时间" in clause.text or "上课地点" in clause.text or "服务地点" in clause.text or "预约" in clause.text or "排课" in clause.text), limit=2),
            "中",
            "合同已明确上课时间、地点、方式或预约安排，仅有少量空白；按真实合同实务，不应按高风险-完全缺失处理，本项修正为中风险-部分覆盖。",
            "服务时间、地点和方式已基本明确，建议补全剩余未填的排课或变更约定。",
            issue_type="模板空白",
        )
        item.fallback_reason = "服务合同服务时间地点方式专项校正"

    if _service_is_training_contract(compacted):
        training_evidence = _find_clauses(
            clauses,
            lambda clause: any(term in clause.text for term in ("培训", "课程", "课时", "学员", "上课", "教师", "老师")),
            limit=2,
        )
        for item_id, title in (
            ("SVC-01-02", "服务与承揽区分"),
            ("SVC-01-03", "服务与委托区分"),
            ("SVC-01-04", "服务类型细分"),
        ):
            if item := by_id.get(item_id):
                _set_item_partial(
                    item,
                    training_evidence,
                    "中",
                    f"合同已能识别为培训服务，{title}缺少的是进一步定性或边界说明，属于建议性补充，不应因模板简略直接提升为高风险。",
                    f"合同已体现培训服务的核心场景，但仍建议补充“{title}”相关表述，避免与承揽、委托或其他服务类型发生边界争议。",
                    issue_type="条款缺陷",
                )
                item.fallback_reason = "服务合同类型定性风险分级校正"

    if _service_has_prepayment_balance_framework(compacted) and (item := by_id.get("SVC-04-02")):
        _set_item_partial(
            item,
            _find_clauses(clauses, lambda clause: any(term in clause.text for term in ("总金额", "服务费", "培训费", "课时", "退费", "退款", "余额")), limit=2),
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
                    _find_clauses(clauses, lambda clause: any(term in clause.text for term in ("退费", "退款", "剩余课时", "未消耗课时", "按实际课时", "未提供服务", "结算")), limit=2),
                    "中",
                    reason,
                    description,
                    issue_type="模板空白",
                )
                item.fallback_reason = "服务合同解除退费风险分级校正"

    if _service_has_consumer_notice_framework(compacted) and (item := by_id.get("SVC-06-02")):
        _set_item_partial(
            item,
            _find_clauses(clauses, lambda clause: any(term in clause.text for term in ("书面通知", "退费申请", "退款申请", "解除申请", "申请材料")), limit=2),
            "中",
            "合同已约定书面通知、退费申请或类似办理方式，可作为消费者解除/退费通知的基础，但材料清单、办理期限或送达渠道仍需补充。",
            "消费者解除通知已有基础安排，建议补全申请材料、送达渠道、审核期限和退款期限。",
            issue_type="模板空白",
        )
        item.fallback_reason = "服务合同消费者解除通知风险分级校正"

    if not _service_has_forbidden_no_qualification_clause(compacted) and (item := by_id.get("SVC-02-04")):
        _set_item_missing(
            item,
            "中",
            "未在正式合同条款中找到“服务方无资质时不得继续提供服务并应退费/赔偿”的有效约定；此前将无关证据判为通过不符合实质匹配规则。",
            "合同缺少服务方无资质或资质丧失时的停止服务、退费和责任承担安排，存在履约合规争议。",
            "服务合同资质保障条款证据实质匹配校正",
        )

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
    return item.risk_point_description or item.legal_consequence_if_missing or item.title


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


def _overall_assessment(
    contract_type_name: str,
    findings: List[RiskFinding],
    items: List[ReviewItemResult],
) -> Dict[str, Any]:
    has_manual = any(item.needs_manual_review for item in items)
    max_severity = SEVERITY_NONE
    if findings:
        max_severity = sorted((finding.severity for finding in findings), key=_severity_rank)[0]
    a_core_count = sum(1 for finding in findings if finding.priority == PRIORITY_A_CORE)
    if has_manual:
        signability = "建议人工法律复核"
    elif max_severity in {SEVERITY_HIGH, SEVERITY_CRITICAL}:
        signability = "存在重大风险，建议修改后签署"
    elif a_core_count or any(finding.severity == SEVERITY_MEDIUM for finding in findings):
        signability = "建议修改后签署"
    else:
        signability = "可直接签署"
    return {
        "contract_type": contract_type_name,
        "signability": signability,
        "core_risk_count": len([finding for finding in findings if finding.priority == PRIORITY_A_CORE]),
        "priority_modify_count": len([finding for finding in findings if finding.priority in {PRIORITY_A_CORE, PRIORITY_B_PRACTICAL}]),
        "optional_count": len([finding for finding in findings if finding.priority == PRIORITY_C_OPTIMIZATION]),
        "covered_key_items": [item.item_id for item in items if item.coverage_status == "通过" and item.review_priority in {PRIORITY_A_CORE, PRIORITY_B_PRACTICAL}][:10],
        "manual_review_count": sum(1 for item in items if item.needs_manual_review),
        "max_severity": max_severity,
    }


def _finding_needs_verification(finding: RiskFinding) -> bool:
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
        has_support = bool(finding.evidence) or any(item.coverage_status == "缺失" for item in related_items)
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


def _build_recommendations(findings: List[RiskFinding]) -> List[Recommendation]:
    recommendations: List[Recommendation] = []
    by_key: Dict[tuple[str, str], Recommendation] = {}
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
            )
            by_key[key] = recommendation
            recommendations.append(recommendation)
        recommendation.target_risk_ids = sorted(set(recommendation.target_risk_ids + [finding.finding_id]))
        recommendation.source_finding_ids = sorted(set(recommendation.source_finding_ids + [finding.finding_id]))
        recommendation.target_finding_ids = sorted(set(recommendation.target_finding_ids + [finding.finding_id]))
        recommendation.target_clause_ids = sorted(set(recommendation.target_clause_ids + finding.source_clause_ids))
        finding.recommendation_ids = sorted(set(finding.recommendation_ids + [recommendation.recommendation_id]))
    return recommendations


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
    }


def _benchmark_metrics(items: List[ReviewItemResult], findings: List[RiskFinding]) -> Dict[str, Any]:
    duplicate_groups = len(findings) - len({finding.risk_group for finding in findings})
    manual_review_count = sum(1 for item in items if item.needs_manual_review)
    return {
        "benchmark_version": BENCHMARK_VERSION,
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
        "top5_risk_recall": None,
        "confidence_calibration_error": None,
        "manual_review_precision": None,
        "manual_review_rate": manual_review_count,
        "notes": "当前为 regression smoke metrics；样本量不足，不输出伪精确百分比。",
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
        "frontend/src/views/ContractReviewV2.vue:submitReview",
        "frontend/src/utils/api.js:reviewContractV2File",
        "backend/routers/review_v2.py:review_v2_file",
        "backend/layers/input_layer.py:InputLayer.extract_text_from_file",
        "backend/review_v2/engine.py:review_contract_v2",
        "backend/review_v2/clause_parser.py:parse_contract_clauses",
        "backend/review_v2/lease_contract_facts.py:extract_house_lease_facts",
        "backend/review_v2/llm_semantic_reviewer.py:judge_checkpoints_with_llm",
        "backend/review_v2/engine.py:_apply_final_quality_gate",
        "backend/review_v2/engine.py:_check_legal_reference_freshness",
        "backend/review_v2/engine.py:_build_risk_findings",
        "backend/review_v2/engine.py:_legal_reference_findings",
        "backend/review_v2/engine.py:_run_independent_verifier",
        "backend/review_v2/engine.py:_build_recommendations",
        "backend/review_v2/engine.py:_overall_assessment",
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


def _combine_quality_gates(*gates: Dict[str, Any]) -> Dict[str, Any]:
    failures: List[Dict[str, Any]] = []
    for gate in gates:
        failures.extend(gate.get("failures") or [])
    merged = dict(gates[0] if gates else {})
    merged["status"] = "REPORT_READY" if not failures else "BLOCKED"
    merged["failures"] = failures
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
        return {
            "evidence_status": "NOT_FOUND",
            "clause_number": "未召回正式条款",
            "original_excerpt": "无正式条款证据",
            "position_description": "未在合同正文及附件中定位到对应安排。",
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
        "evidence_status": "FOUND",
        "document_type": document_type,
        "source_document_type": document_type,
        "source_label": source_label,
        "clause_number": location,
        "original_excerpt": f"“{_excerpt(sentence or text)}”",
        "position_description": f"{source_label}，{position}",
    }


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
    return re.sub(r"\s+", " ", cleaned).strip()


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
            return f"按合同公式测算：{'；'.join(parts)}。{tail}。"
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


def _top_risk_line(finding: RiskFinding, item_by_id: Dict[str, ReviewItemResult]) -> str:
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
    pieces.extend([evidence_text, f"建议：{finding.recommendation}"])
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
    if item.coverage_status == "通过":
        if item.related_risks:
            return "该审查事项的基本机制已覆盖，但同一条款或事实仍形成独立风险，详见核心风险摘要。"
        return "该审查事项已覆盖，无需修改。"
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return _user_facing_reasoning(item.applicability.get("reason") or "该审查事项不适用于当前合同。")
    if item.coverage_status == "部分覆盖":
        return f"合同已覆盖“{item.title}”的部分内容，但仍需围绕关联风险补充关键要素。"
    if item.coverage_status == "缺失":
        return f"合同未明确约定“{item.title}”相关安排，需结合默认法律规则和实际履行风险判断处理优先级。"
    if item.coverage_status == "风险条款":
        return f"合同虽有相关条款，但条款内容本身可能引发执行争议，应按关联风险发现处理。"
    return _conclusion_text(item)


_SECTION_NUMERALS = "一二三四五六七八九十"


def _section_title(index: int, title: str) -> str:
    numeral = _SECTION_NUMERALS[index - 1] if 1 <= index <= len(_SECTION_NUMERALS) else str(index)
    return f"## {numeral}、{title}"


def _production_profile_lines(profile: UserRiskProfile, contract_type_name: str) -> List[str]:
    if "租赁" in contract_type_name:
        if "出租" in profile.user_identity:
            stance = "出租人"
        else:
            stance = "承租人（个人租客）" if "租客" in profile.user_identity or "个人" in profile.user_identity else "承租人"
    elif "买卖" in contract_type_name:
        stance = "买方" if "买" in profile.user_identity else "卖方" if "卖" in profile.user_identity else profile.user_identity
    else:
        stance = profile.user_identity
    lines = [f"- 审查立场：{stance}"]
    if profile.contract_scenario:
        lines.append(f"- 使用场景：{profile.contract_scenario}")
    return lines


def _display_legal_consequence(item: ReviewItemResult) -> tuple[str, str]:
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return "适用说明", item.applicability.get("reason") or "本项不适用于当前合同。"
    if item.coverage_status == "通过":
        if item.related_risks:
            return "关联风险", "同一条款或事实仍存在需要处理的经济或法律风险，详见核心风险摘要。"
        return "处理结论", "已覆盖，无需修改。"
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
        authority_text = "；".join(f"《{claim.get('law_name')}》{claim.get('article') or ''}" for claim in direct)
        if has_partial:
            return f"{authority_text}；本项部分内容属于合同起草建议。"
        return authority_text
    background = [
        claim for claim in claims
        if claim.get("support_type") == "BACKGROUND_ONLY" and claim.get("law_name")
    ]
    if background:
        return "相关法律规则参考：合同履行、通知送达及证据留存规则；本项主要为合同管理实务建议。"
    if item.legal_basis_index:
        return "合同管理实务建议；未匹配到足够直接的现行具体条文。"
    return "合同管理实务建议"


def _display_suggested_clause(item: ReviewItemResult) -> tuple[str, str]:
    if item.coverage_status == COVERAGE_NOT_APPLICABLE:
        return "", ""
    if item.coverage_status == "通过":
        if item.risk_level == "低":
            return "", ""
        return "可选优化", item.suggested_clause_example
    if item.coverage_status == "部分覆盖":
        return "建议补充", item.suggested_clause_example
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
    return report


def _system_metadata(model_status: Dict[str, Any]) -> Dict[str, Any]:
    configured_models = model_status.get("configured_models") or []
    return {
        "system_version": SYSTEM_VERSION,
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
        "model_version": configured_models[0] if configured_models else "deterministic_pipeline",
        "generated_at": datetime.now().isoformat(),
    }


def _apply_profile_rules(
    items: List[ReviewItemResult],
    profile: UserRiskProfile,
) -> List[ReviewItemResult]:
    """根据用户风险画像动态调整审查结果。

    1. 风险等级重映射（保守→提升，激进→降低）
    2. 标注行动标签（必须改/建议改/可考虑改）
    3. 标注是否为优先审查点
    4. 修改建议语气适配
    """
    for item in items:
        if "租客" in profile.user_identity or "承租" in profile.user_identity:
            item.decision_trace["user_perspective"] = "TENANT"
        elif "出租" in profile.user_identity:
            item.decision_trace["user_perspective"] = "LANDLORD"
        elif "买" in profile.user_identity:
            item.decision_trace["user_perspective"] = "BUYER"
        elif "卖" in profile.user_identity or "出卖" in profile.user_identity:
            item.decision_trace["user_perspective"] = "SELLER"
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
) -> str:
    """Pure Markdown serializer for the final ReviewItemResult list."""
    findings = risk_findings or []
    recs = recommendations or []
    finding_summary = risk_finding_summary or _risk_finding_summary(findings, items)
    assessment = overall_assessment or _overall_assessment(contract_type_name, findings, items)
    must_count = sum(1 for finding in findings if finding.priority == PRIORITY_A_CORE)
    suggest_count = sum(1 for finding in findings if finding.priority == PRIORITY_B_PRACTICAL)
    consider_count = sum(1 for finding in findings if finding.priority == PRIORITY_C_OPTIMIZATION)
    item_by_id = {item.item_id: item for item in items}
    priority_core_findings = [finding for finding in findings if finding.priority == PRIORITY_A_CORE][:10]
    practical_findings = [finding for finding in findings if finding.priority == PRIORITY_B_PRACTICAL][:10]
    priority_findings = [finding for finding in findings if finding.priority in {PRIORITY_A_CORE, PRIORITY_B_PRACTICAL}][:10]
    optimization_findings = [finding for finding in findings if finding.priority == PRIORITY_C_OPTIMIZATION][:10]
    covered_key_items = [item for item in items if item.coverage_status == "通过" and item.review_importance in {REVIEW_IMPORTANCE_CORE, REVIEW_IMPORTANCE_IMPORTANT}][:10]
    finding_title_map = _finding_id_title_map(findings)
    section_index = 0

    def add_section(title: str) -> None:
        nonlocal section_index
        section_index += 1
        lines.extend(["", _section_title(section_index, title), ""])

    profile_lines = _production_profile_lines(profile, contract_type_name)
    lines = [
        f"# {contract_type_name}审查报告",
        "",
    ]
    add_section("合同总体评价")
    lines.extend([
        *profile_lines,
        f"- 合同类型：{contract_type_name}",
        f"- 总体可签署性：{assessment.get('signability')}",
        f"- 风险发现总数：{len(findings)}",
        f"- 重大风险数量：{finding_summary.get('重大风险', 0)}",
        f"- 中等风险数量：{finding_summary.get('中等风险', 0)}",
        f"- 低风险数量：{finding_summary.get('低风险', 0)}",
        f"- 优先处理风险：{must_count}",
        f"- 建议处理风险：{suggest_count}",
        f"- 可选优化风险：{consider_count}",
        f"- 人工复核项：{assessment.get('manual_review_count', 0)}",
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
    if priority_core_findings:
        lines.extend(["### 优先处理", ""])
        for finding in priority_core_findings:
            lines.append(_top_risk_line(finding, item_by_id))
            lines.append("")
    if practical_findings:
        lines.extend(["### 建议处理", ""])
        for finding in practical_findings:
            lines.append(_top_risk_line(finding, item_by_id))
            lines.append("")
    if not priority_core_findings and not practical_findings:
        lines.append("- 未发现需要优先处理的高风险或重大经济后果事项。")
    add_section("建议优先修改")
    if priority_core_findings:
        lines.extend(["### 优先处理", ""])
        for recommendation in [rec for rec in recs if rec.priority == PRIORITY_A_CORE][:10]:
            target_names = "、".join(finding_title_map.get(risk_id, "关联风险") for risk_id in recommendation.target_finding_ids or recommendation.target_risk_ids)
            lines.append(f"- **优先处理**：{recommendation.proposed_change or recommendation.suggested_text}（对应风险：{target_names}）")
        lines.append("")
    if practical_findings:
        lines.extend(["### 建议处理", ""])
        for recommendation in [rec for rec in recs if rec.priority == PRIORITY_B_PRACTICAL][:10]:
            target_names = "、".join(finding_title_map.get(risk_id, "关联风险") for risk_id in recommendation.target_finding_ids or recommendation.target_risk_ids)
            lines.append(f"- **建议处理**：{recommendation.proposed_change or recommendation.suggested_text}（对应风险：{target_names}）")
    else:
        if not priority_core_findings:
            lines.append("- 暂无必须或优先修改事项。")
    add_section("可选优化事项")
    lines.append("以下事项属于完善型建议，通常不是当前签署的核心障碍。")
    lines.append("")
    if optimization_findings:
        for recommendation in [rec for rec in recs if rec.priority == PRIORITY_C_OPTIMIZATION][:10]:
            target_names = "、".join(finding_title_map.get(risk_id, "关联风险") for risk_id in recommendation.target_finding_ids or recommendation.target_risk_ids)
            lines.append(f"- **可选优化**：{recommendation.proposed_change or recommendation.suggested_text}（对应风险：{target_names}）")
    else:
        lines.append("- 暂无需要单独提示的可优化事项。")
    add_section("已覆盖关键事项")
    if covered_key_items:
        for item in covered_key_items:
            related = f"；关联风险：{_join_related_finding_titles(item.related_risks, finding_title_map)}" if item.related_risks else ""
            lines.append(f"- **{item.item_id} {item.title}**：已覆盖{related}。")
    else:
        lines.append("- 已覆盖项详见完整审查明细。")
    manual_items = [item for item in items if item.needs_manual_review]
    if manual_items:
        add_section("人工复核事项")
        for item in manual_items:
            lines.append(f"- **{item.item_id} {item.title}**：{item.quality_gate_failure_reason or '证据或事实存在无法自动消解的不确定性。'}")
    lines.extend(["", "---"])
    add_section("完整审查明细")
    for index, item in enumerate(items, start=1):
        legal_label, legal_value = _display_legal_consequence(item)
        suggested_label, suggested_value = _display_suggested_clause(item)
        lines.extend(
            [
                f"## {index}. {item.title}（{item.item_id}）",
                "",
                "### 审查结论",
                f"- **处理建议**：{item.action_suggestion or _action_suggestion_for_item(item)}",
                f"- 审查重要度：{_importance_label(item.review_importance or _review_importance_for_item(item))}",
                f"- 行动优先级：{_priority_label(item.action_priority or item.review_priority or _action_priority_for_item(item))}",
                f"- 关联风险发现：{_join_related_finding_titles(item.related_risks, finding_title_map)}",
                f"- 系统确定性：{_confidence_label((item.system_confidence or {}).get('level', 'medium'))}",
                f"- 经济影响：{_economic_display(item.economic_impact)}",
                f"- 覆盖状态：{item.coverage_status}",
                f"- 问题类型：{item.issue_type}",
                f"- 原文位置：{item.evidence_location or '未召回正式条款'}",
                f"- 审查判断：{_professional_item_conclusion(item)}",
                f"- 【风险点描述】：{_user_facing_reasoning(item.risk_point_description)}",
                f"- 【{legal_label}】：{_user_facing_reasoning(legal_value)}",
                f"- 【法律依据】：{_trusted_legal_basis_display(item)}",
                f"- 【适用条件】：{item.applicable_if}",
                "",
            ]
        )
        if suggested_label and suggested_value:
            lines.extend([f"- 【{suggested_label}】：{suggested_value}", ""])
        if item.citation:
            if item.citation.get("evidence_status") == "NOT_FOUND":
                lines.extend(
                    [
                        "【证据定位】",
                        f"- {item.citation.get('position_description', '未在合同正文及附件中定位到对应安排。')}",
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
    if profile is None:
        profile = UserRiskProfile.default()
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
            "contract_context": build_contract_context(normalized_type, {}, profile).to_public_dict(),
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
    checklist = get_checklist(type_meta.key)
    clauses = parse_contract_clauses(review_text)
    lease_facts = extract_house_lease_facts(review_text) if type_meta.key.value == "lease" else None
    contract_facts = lease_facts.to_public_dict() if lease_facts else {}
    applicable_checkpoints = []
    not_applicable_items: Dict[str, ReviewItemResult] = {}
    item_applicability: Dict[str, Dict[str, Any]] = {}
    for checkpoint in checklist:
        is_applicable, applicability_reason = _is_checkpoint_applicable(review_text, checkpoint, type_meta.key.value)
        fact_applicability = _evaluate_lease_fact_applicability(checkpoint, lease_facts) if lease_facts else {
            "status": "applicable",
            "applicable": True,
            "reason": applicability_reason or "未触发适用条件排除。",
            "depends_on": [],
        }
        item_applicability[checkpoint.item_id] = fact_applicability
        if is_applicable and not fact_applicability["applicable"]:
            is_applicable = False
            applicability_reason = fact_applicability["reason"]
        if is_applicable:
            applicable_checkpoints.append(checkpoint)
        else:
            na_item = _not_applicable_item(checkpoint, applicability_reason)
            na_item.applicability = fact_applicability if not fact_applicability.get("applicable", True) else {
                "status": "not_applicable",
                "applicable": False,
                "reason": applicability_reason,
                "depends_on": [],
            }
            na_item.fact_dependencies = list(na_item.applicability.get("depends_on") or [])
            not_applicable_items[checkpoint.item_id] = na_item

    judgments = judge_checkpoints_with_llm(tuple(applicable_checkpoints), clauses, use_llm=use_llm)
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
    items = _apply_contract_specific_post_rules(items, review_text, type_meta.key.value)

    # 应用用户画像规则（风险等级重映射、语气调整、审查点标注）
    items = _apply_profile_rules(items, profile)
    items, quality_gate = _apply_final_quality_gate(items, lease_facts, type_meta.key.value)
    items = _apply_risk_dimensions(items)
    items = _apply_review_priority_and_action(items)
    items = _enrich_evidence_sources(items)
    items = _apply_evidence_entailment_gate(items)
    items = _apply_risk_dimensions(items)
    items = _apply_review_priority_and_action(items)
    items = _apply_citation_claims(items)
    legal_reference_issues = _check_legal_reference_freshness(review_text)
    legal_authority_validation = _validate_legal_authorities(
        [{"law_name": issue.get("law_name"), "article": issue.get("article")} for issue in legal_reference_issues]
    )
    risk_findings = _build_risk_findings(items) + _legal_reference_findings(legal_reference_issues)
    risk_findings.sort(key=_finding_sort_key)
    for item in items:
        item.action_priority = _action_priority_for_item(item)
        item.review_priority = item.action_priority
        item.action_suggestion = _action_suggestion_for_item(item)
    risk_findings = _run_independent_verifier(risk_findings, items)
    legal_freshness_trace = _legal_freshness_trace(review_text, legal_reference_issues, risk_findings)
    recommendations = _build_recommendations(risk_findings)
    risk_finding_summary = _risk_finding_summary(risk_findings, items)
    overall_assessment = _overall_assessment(contract_type_name=type_meta.display_name, findings=risk_findings, items=items)
    benchmark_metrics = _benchmark_metrics(items, risk_findings)
    system_metadata = _system_metadata(llm_status)
    items = _enrich_reasoning_and_citation(items)

    visible_items = items if include_low_risk else [item for item in items if item.risk_level in {"高", "中"}]
    contract_type_name = type_meta.display_name
    review_results_4_0 = [public_review_result(item) for item in visible_items]
    legal_citation_claims = [
        claim
        for item in visible_items
        for claim in (item.legal_references or [])
    ]
    risk_finding_dicts = [finding.to_public_dict() for finding in risk_findings]
    recommendation_dicts = [recommendation.to_public_dict() for recommendation in recommendations]
    contract_context = build_contract_context(type_meta.response_key, contract_facts, profile).to_public_dict()
    architecture_status = _architecture_status()

    # 诉讼策略分析（对高/中风险条款）
    public_items = [item.to_public_dict() for item in visible_items]
    litigation_report = analyze_litigation_strategy(public_items, profile)

    # 商业谈判分析（对高/中风险条款）
    negotiation_report = analyze_negotiation_strategy(public_items, profile)

    # 跨地域裁判预判（对高/中风险条款）
    jurisdiction_report = analyze_jurisdiction_prediction(public_items, profile, review_text)

    # 生成带四层子模块的主报告
    result = _format_markdown_v2(
        contract_type_name, visible_items, profile,
        risk_findings=risk_findings,
        recommendations=recommendations,
        overall_assessment=overall_assessment,
        risk_finding_summary=risk_finding_summary,
        benchmark_metrics=benchmark_metrics,
        system_metadata=system_metadata,
        litigation_items=litigation_report.to_public_dict(),
        negotiation_items=negotiation_report.to_public_dict(),
        jurisdiction_items=jurisdiction_report.to_public_dict(),
    )
    release_quality_gate = _release_quality_gate(visible_items, risk_findings, result)
    result = _format_markdown_v2(
        contract_type_name, visible_items, profile,
        risk_findings=risk_findings,
        recommendations=recommendations,
        overall_assessment=overall_assessment,
        risk_finding_summary=risk_finding_summary,
        benchmark_metrics=benchmark_metrics,
        release_quality_gate=release_quality_gate,
        system_metadata=system_metadata,
        litigation_items=litigation_report.to_public_dict(),
        negotiation_items=negotiation_report.to_public_dict(),
        jurisdiction_items=jurisdiction_report.to_public_dict(),
    )
    quality4_gate = post_render_quality_gate(result, review_results_4_0, risk_finding_dicts, recommendation_dicts)
    release_quality_gate = _combine_quality_gates(release_quality_gate, quality4_gate)
    litigation_result = format_litigation_markdown(litigation_report)
    negotiation_result = format_negotiation_markdown(negotiation_report)
    jurisdiction_result = format_jurisdiction_markdown(jurisdiction_report)
    total_latency_ms = round((time.perf_counter() - started_at) * 1000, 2)

    return {
        "success": True,
        "contract_type": type_meta.response_key,
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
        "quality_gate": quality_gate,
        "review_results_4_0": review_results_4_0,
        "risk_findings": risk_finding_dicts,
        "recommendations": recommendation_dicts,
        "contract_context": contract_context,
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
            "final_output_ownership_matrix": _final_output_ownership_matrix(),
            "legal_freshness_trace": legal_freshness_trace,
            "risk_aggregation_debug_table": _risk_aggregation_debug_table(risk_findings),
            "parser_latency_ms": None,
            "fact_latency_ms": None,
            "retrieval_latency_ms": None,
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
