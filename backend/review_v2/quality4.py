"""Quality 4.0 ownership, ontology and validation helpers.

This module is intentionally deterministic. It gives the v2 engine a stable
target architecture without replacing the mature extraction/review pipeline in
one risky rewrite.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any, Dict, Iterable, List, Optional

from review_v2.domain_packs import get_domain_pack
from review_v2.domain_resolution import DomainResolution
from review_v2.technology_service_analysis import classify_technology_transaction


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
    contract_family: str = ""
    transaction_nature: str = ""
    contract_subtype: str = ""
    user_role: str = "neutral"
    counterparty_role: str = "neutral"
    transaction_purpose: str = ""
    usage_scenario: str = ""
    subject_matter: str = ""
    asset_usage: str = ""
    consideration_type: str = ""
    ownership_transfer: bool = False
    possession_transfer: bool = False
    product_category: str = ""
    transaction_structure: str = "OTHER"
    fixed_quantity: Optional[bool] = None
    dynamic_quantity: Optional[bool] = None
    master_agreement_exists: Optional[bool] = None
    order_driven_performance: Optional[bool] = None
    recurring_delivery: Optional[bool] = None
    recurring_settlement: Optional[bool] = None
    minimum_purchase_commitment: Optional[bool] = None
    forecast_exists: Optional[bool] = None
    forecast_binding: Optional[bool] = None
    price_adjustment_mechanism: str = ""
    term_based_relationship: Optional[bool] = None
    contract_value: Optional[float] = None
    currency: str = "CNY"
    duration: Optional[str] = None
    payment_frequency: Optional[str] = None
    payment_structure: str = ""
    delivery_structure: str = ""
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
    domain_attributes: Dict[str, Any] = field(default_factory=dict)

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


def _civil_code_authority(article: str, authority_id: str, text: str) -> LegalAuthority:
    return LegalAuthority(
        authority_id=authority_id, jurisdiction="CN", law_name="中华人民共和国民法典",
        article=article, paragraph="", text=text, authority_level="法律",
        effective_from="2021-01-01", effective_to=None, status="CURRENT", replacement=None,
        source="National Laws and Regulations Database / Civil Code",
        last_verified_at="2026-08-14",
    )


def _judicial_interpretation_authority(
    law_name: str, article: str, authority_id: str, text: str, effective_from: str,
) -> LegalAuthority:
    return LegalAuthority(
        authority_id=authority_id, jurisdiction="CN", law_name=law_name,
        article=article, paragraph="", text=text, authority_level="司法解释",
        effective_from=effective_from, effective_to=None, status="CURRENT", replacement=None,
        source="Supreme People's Court judicial interpretation",
        last_verified_at="2026-09-02",
    )


LEGAL_AUTHORITY_KB.update({
    ("中华人民共和国民法典", "第506条"): _civil_code_authority(
        "第506条", "CN-CC-506",
        "合同中造成对方人身损害的免责条款，以及因故意或者重大过失造成对方财产损失的免责条款无效。",
    ),
    ("中华人民共和国民法典", "第509条"): _civil_code_authority("第509条", "CN-CC-509", "当事人应当按照约定全面履行自己的义务，并遵循诚信原则履行通知、协助、保密等义务。"),
    ("中华人民共和国民法典", "第577条"): _civil_code_authority("第577条", "CN-CC-577", "当事人一方不履行合同义务或者履行不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。"),
    ("中华人民共和国民法典", "第582条"): _civil_code_authority("第582条", "CN-CC-582", "履行不符合约定时，受损害方可以根据标的性质和损失大小合理选择修理、重作、更换、退货、减少价款或者报酬等违约责任。"),
    ("中华人民共和国民法典", "第584条"): _civil_code_authority("第584条", "CN-CC-584", "违约损失赔偿包括合同履行后可以获得的利益，但不得超过违约方订立合同时预见到或者应当预见到的损失。"),
    ("中华人民共和国民法典", "第589条"): _civil_code_authority("第589条", "CN-CC-589", "债权人无正当理由拒绝受领的，债务人可以请求赔偿增加的费用；受领迟延期间债务人无须支付利息。"),
    ("中华人民共和国民法典", "第591条"): _civil_code_authority("第591条", "CN-CC-591", "违约后对方应采取适当措施防止损失扩大；未采取措施导致扩大的，不得就扩大部分请求赔偿。"),
    ("中华人民共和国民法典", "第604条"): _civil_code_authority("第604条", "CN-CC-604", "标的物毁损、灭失风险原则上在交付前由出卖人承担，交付后由买受人承担，但另有约定或法定例外除外。"),
    ("中华人民共和国民法典", "第605条"): _civil_code_authority("第605条", "CN-CC-605", "因买受人原因致使标的物未按约定期限交付的，买受人自违反约定时起承担标的物毁损、灭失风险。"),
    ("中华人民共和国民法典", "第607条"): _civil_code_authority("第607条", "CN-CC-607", "出卖人按约将标的物运送至买受人指定地点并交付承运人的，风险依法律规定的交付节点转移。"),
    ("中华人民共和国民法典", "第617条"): _civil_code_authority("第617条", "CN-CC-617", "出卖人交付的标的物不符合质量要求的，买受人可以依法请求承担违约责任。"),
    ("中华人民共和国民法典", "第620条"): _civil_code_authority("第620条", "CN-CC-620", "买受人收到标的物时应在约定检验期限内检验；没有约定检验期限的，应及时检验。"),
    ("中华人民共和国民法典", "第621条"): _civil_code_authority("第621条", "CN-CC-621", "当事人约定检验期限的，买受人应在期限内通知数量或质量不符合约定；未约定期限的，应在合理期限内通知。"),
    ("中华人民共和国民法典", "第563条"): _civil_code_authority("第563条", "CN-CC-563", "符合法定情形时，当事人可以依法解除合同。"),
    ("中华人民共和国民法典", "第565条"): _civil_code_authority("第565条", "CN-CC-565", "依法主张解除合同的，应当通知对方，合同自通知到达对方时解除。"),
    ("中华人民共和国民法典", "第845条"): _civil_code_authority("第845条", "CN-CC-845", "技术合同内容一般包括项目名称、标的内容范围和要求、履行计划地点方式、技术信息和资料保密、成果归属、验收标准和方法等。"),
    ("中华人民共和国民法典", "第850条"): _civil_code_authority("第850条", "CN-CC-850", "非法垄断技术或者侵害他人技术成果的技术合同无效。"),
    ("中华人民共和国民法典", "第874条"): _civil_code_authority("第874条", "CN-CC-874", "受让人或者被许可人按照约定实施专利、使用技术秘密侵害他人合法权益的，由让与人或者许可人承担责任，但当事人另有约定的除外。"),
    ("中华人民共和国民法典", "第875条"): _civil_code_authority("第875条", "CN-CC-875", "当事人可以按照互利原则，在合同中约定实施专利、使用技术秘密后续改进的技术成果分享办法。"),
    ("中华人民共和国民法典", "第883条"): _civil_code_authority("第883条", "CN-CC-883", "技术咨询合同、技术服务合同履行中涉及的必要费用依合同约定处理。"),
    ("中华人民共和国民法典", "第884条"): _civil_code_authority("第884条", "CN-CC-884", "技术咨询合同、技术服务合同的受托人应当按照约定期限完成咨询报告或者解决技术问题。"),
    ("中华人民共和国民法典", "第885条"): _civil_code_authority("第885条", "CN-CC-885", "技术咨询合同、技术服务合同履行过程中产生的新技术成果，依约定处理；没有约定或者约定不明确的，依法确定归属。"),
    (
        "最高人民法院关于审理技术合同纠纷案件适用法律若干问题的解释", "第10条",
    ): _judicial_interpretation_authority(
        "最高人民法院关于审理技术合同纠纷案件适用法律若干问题的解释",
        "第10条", "CN-SPC-TECH-CONTRACT-10",
        "限制一方研究开发、限制从其他来源取得技术、要求无偿提供改进技术等约定，可能构成非法垄断技术、妨碍技术进步。",
        "2021-01-01",
    ),
    (
        "最高人民法院关于适用〈中华人民共和国民法典〉合同编通则若干问题的解释", "第65条",
    ): _judicial_interpretation_authority(
        "最高人民法院关于适用〈中华人民共和国民法典〉合同编通则若干问题的解释",
        "第65条", "CN-SPC-CONTRACT-GENERAL-65",
        "判断约定违约金是否过分高于损失，应当以实际损失为基础，兼顾合同履行、过错程度和预期利益等因素衡量。",
        "2023-12-05",
    ),
})


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
    "sale_risk_transfer_delivery": "PARTIAL_DEFAULT",
    "sale_risk_carrier_delivery": "PARTIAL_DEFAULT",
    "sale_risk_buyer_delay_acceptance": "PARTIAL_DEFAULT",
    "sale_inspection_period": "PARTIAL_DEFAULT",
    "sale_quality_liability": "PARTIAL_DEFAULT",
    "sale_third_party_rights": "PARTIAL_DEFAULT",
    "sale_title_warranty": "PARTIAL_DEFAULT",
    "sale_delay_performance": "PARTIAL_DEFAULT",
    "sale_breach_damages": "PARTIAL_DEFAULT",
    "sale_termination": "PARTIAL_DEFAULT",
    "common_force_majeure": "PARTIAL_DEFAULT",
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


def _infer_contract_value(text: str) -> Optional[float]:
    amounts: List[float] = []
    for match in re.finditer(r"(?:(?:总价|合同价款|合同金额|价款|货款).{0,12})?(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:元|人民币)", text or ""):
        amount = _safe_amount(match.group(1))
        if amount is not None:
            amounts.append(amount)
    return max(amounts) if amounts else None


def _infer_sale_subject(text: str) -> str:
    if any(term in text for term in ("水泥", "硅酸盐")):
        return "cement"
    if any(term in text for term in ("货物", "产品", "设备", "材料")):
        return "goods"
    return ""


def _role_pair(perspective: str, contract_type: str) -> tuple[str, str]:
    if contract_type in {"sale"}:
        if perspective == "seller":
            return "seller", "buyer"
        return "buyer", "seller"
    if contract_type in {"house_lease", "lease"}:
        if perspective == "landlord":
            return "landlord", "tenant"
        return "tenant", "landlord"
    return perspective or "neutral", "neutral"


def build_contract_context(
    contract_type: str,
    facts: Optional[Dict[str, Any]],
    profile: Optional[Any] = None,
    contract_text: str = "",
    domain_resolution: Optional[DomainResolution] = None,
) -> ContractContext:
    facts = facts or {}
    normalized_type = "house_lease" if contract_type in {"house_lease", "lease"} else contract_type
    domain_pack = get_domain_pack(normalized_type)
    defaults = domain_pack.context_defaults
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
    user_role, counterparty_role = _role_pair(perspective, normalized_type)

    if normalized_type == "sale":
        resolution = domain_resolution
        framework = facts.get("framework_supply") or {}
        def framework_exists(name: str) -> Optional[bool]:
            value = framework.get(name) or {}
            return value.get("exists") if isinstance(value, dict) else None
        def framework_value(name: str) -> Any:
            value = framework.get(name) or {}
            return value.get("value") if isinstance(value, dict) else None
        selected_pack = (resolution.selected_domain_packs[-1] if resolution and resolution.selected_domain_packs else "sale")
        resolved_defaults: Dict[str, Any] = {}
        for pack_id in (resolution.selected_domain_packs if resolution else ["sale"]):
            resolved_defaults.update(get_domain_pack(pack_id).context_defaults)
        return ContractContext(
            contract_type=contract_type,
            contract_family=resolution.contract_family if resolution else "SALE",
            transaction_nature=resolution.transaction_nature if resolution else "OWNERSHIP_TRANSFER",
            contract_subtype=resolution.contract_subtype if resolution else defaults.get("contract_subtype", "GENERAL_GOODS_SALE"),
            user_role=user_role,
            counterparty_role=counterparty_role,
            transaction_purpose=resolution.transaction_purpose if resolution else defaults.get("transaction_purpose", "goods_sale"),
            usage_scenario=resolved_defaults.get("usage_scenario", resolution.contract_subtype if resolution else "GENERAL_GOODS_SALE"),
            subject_matter=resolution.subject_matter if resolution else _infer_sale_subject(contract_text),
            asset_usage=resolution.asset_usage if resolution else "GENERAL",
            consideration_type=resolution.consideration_type if resolution else "PURCHASE_PRICE",
            ownership_transfer=resolution.ownership_transfer if resolution else True,
            possession_transfer=resolution.possession_transfer if resolution else True,
            product_category=resolution.product_category if resolution else "GENERAL_GOODS",
            transaction_structure=resolution.transaction_structure if resolution else "SINGLE_TRANSACTION",
            fixed_quantity=False if framework_exists("dynamic_quantity") else None,
            dynamic_quantity=framework_exists("dynamic_quantity"),
            master_agreement_exists=framework_exists("master_agreement"),
            order_driven_performance=framework_exists("order_mechanism"),
            recurring_delivery=framework_exists("recurring_delivery"),
            recurring_settlement=framework_exists("periodic_settlement"),
            minimum_purchase_commitment=framework_value("minimum_purchase_commitment"),
            forecast_exists=framework_exists("demand_forecast"),
            forecast_binding=framework_value("forecast_binding"),
            price_adjustment_mechanism=framework_value("price_mechanism") or "",
            term_based_relationship=framework_exists("master_agreement"),
            contract_value=_infer_contract_value(contract_text),
            payment_structure=resolved_defaults.get("payment_structure", defaults.get("payment_structure", "goods_price_payment")),
            delivery_structure=resolved_defaults.get("delivery_structure", defaults.get("delivery_structure", "goods_delivery")),
            parties={k: v for k, v in (facts.get("parties") or {}).items() if v},
            bargaining_power=bargaining,
            user_perspective=perspective,
            domain_attributes={
                "domain_pack": domain_pack.version if resolution and resolution.subject_matter != "REAL_ESTATE" else get_domain_pack(selected_pack).version,
                "selected_domain_packs": resolution.selected_domain_packs if resolution else ["shared", "sale/common", "sale/goods/general"],
                "classification_evidence": [asdict(row) for row in resolution.evidence] if resolution else [],
                "primary_subject": resolution.primary_subject if resolution else "GOODS",
                "accessory_subjects": resolution.accessory_subjects if resolution else [],
                "domain_resolution": resolution.to_public_dict() if resolution else {},
                "framework_supply": framework,
                "context_resolver": "isolated_sale_context",
                "lease_fields_used": False,
                "default_law_nodes": domain_pack.default_law_nodes,
                "economic_ratio_keys": domain_pack.economic_ratio_keys,
            },
        )

    if normalized_type in {"house_lease", "lease"}:
        rent = facts.get("rent") or {}
        deposit = facts.get("deposit") or {}
        payment_frequency = rent.get("payment_cycle")
        return ContractContext(
            contract_type=contract_type,
            contract_family=domain_resolution.contract_family if domain_resolution else "LEASE",
            transaction_nature=domain_resolution.transaction_nature if domain_resolution else "USE_RIGHT_GRANT",
            contract_subtype=defaults.get("contract_subtype", "RESIDENTIAL_LEASE"),
            user_role=user_role,
            counterparty_role=counterparty_role,
            transaction_purpose=defaults.get("transaction_purpose", "residential_lease"),
            usage_scenario=defaults.get("usage_scenario", "residential_living"),
            subject_matter=domain_resolution.subject_matter if domain_resolution else "REAL_ESTATE",
            asset_usage=domain_resolution.asset_usage if domain_resolution else "RESIDENTIAL",
            consideration_type=domain_resolution.consideration_type if domain_resolution else "RENT",
            ownership_transfer=False,
            possession_transfer=True,
            transaction_structure=domain_resolution.transaction_structure if domain_resolution else "SINGLE_TRANSACTION",
            contract_value=_safe_amount(rent.get("monthly_amount")),
            duration=(facts.get("lease_term") or {}).get("text"),
            payment_frequency=payment_frequency,
            payment_structure=defaults.get("payment_structure", "rent_payment"),
            deposit=_safe_amount(deposit.get("amount")),
            parties={k: v for k, v in (facts.get("parties") or {}).items() if v},
            bargaining_power=bargaining,
            user_perspective=perspective,
            domain_attributes={
                "domain_pack": domain_pack.version,
                "context_resolver": "isolated_house_lease_context",
                "lease_fields_used": True,
            },
        )

    if normalized_type == "service":
        resolution = domain_resolution
        return ContractContext(
            contract_type=contract_type,
            contract_family=resolution.contract_family if resolution else "SERVICE",
            transaction_nature=resolution.transaction_nature if resolution else "SERVICE_PROVISION",
            contract_subtype=resolution.contract_subtype if resolution else defaults.get("contract_subtype", "GENERAL_SERVICE"),
            user_role=user_role,
            counterparty_role=counterparty_role,
            transaction_purpose=resolution.transaction_purpose if resolution else defaults.get("transaction_purpose", "service_provision"),
            usage_scenario=defaults.get("usage_scenario", "GENERAL_SERVICE"),
            subject_matter=resolution.subject_matter if resolution else "SERVICE",
            asset_usage=resolution.asset_usage if resolution else "NOT_APPLICABLE",
            consideration_type=resolution.consideration_type if resolution else "SERVICE_FEE",
            ownership_transfer=False,
            possession_transfer=False,
            product_category=resolution.product_category if resolution else "NOT_APPLICABLE",
            transaction_structure=resolution.transaction_structure if resolution else "SERVICE",
            payment_structure=defaults.get("payment_structure", "service_fee_payment"),
            delivery_structure=defaults.get("delivery_structure", "service_performance"),
            parties={k: v for k, v in (facts.get("parties") or {}).items() if v},
            bargaining_power=bargaining,
            user_perspective=perspective,
            domain_attributes={
                "domain_pack": domain_pack.version,
                "selected_domain_packs": resolution.selected_domain_packs if resolution else ["shared", "service"],
                "classification_evidence": [asdict(row) for row in resolution.evidence] if resolution else [],
                "primary_subject": resolution.primary_subject if resolution else "SERVICE",
                "accessory_subjects": resolution.accessory_subjects if resolution else [],
                "domain_resolution": resolution.to_public_dict() if resolution else {},
                "context_resolver": "isolated_service_context",
                "lease_fields_used": False,
            },
        )

    if normalized_type == "technology":
        classification = classify_technology_transaction(contract_text)
        patent_transfer = classification.get("tertiary_subtype") == "PATENT_RIGHT_TRANSFER"
        patent_license = classification.get("tertiary_subtype") == "PATENT_LICENSE"
        technology_pack = get_domain_pack("technology/transfer/patent_right" if patent_transfer else "technology")
        special_assets = []
        if classification["involves_personal_information"]:
            special_assets.append("PERSONAL_INFORMATION")
        if classification["involves_background_ip"]:
            special_assets.append("BACKGROUND_INTELLECTUAL_PROPERTY")
        if classification["involves_software_or_data"]:
            special_assets.append("SOFTWARE_ALGORITHM_DATA_PROCESSING")
        return ContractContext(
            contract_type=contract_type,
            contract_family="TECHNOLOGY",
            transaction_nature="SERVICE_PROVISION" if classification["is_technical_service"] else "INTELLECTUAL_PROPERTY_TRANSFER" if patent_transfer else "INTELLECTUAL_PROPERTY_LICENSE" if patent_license else "TECHNOLOGY_TRANSACTION",
            contract_subtype=classification["subtype"],
            user_role=user_role,
            counterparty_role=counterparty_role,
            transaction_purpose="technical_service" if classification["is_technical_service"] else "patent_right_acquisition" if patent_transfer else "patent_licensing" if patent_license else "technology_transaction",
            usage_scenario=classification["scenario"],
            subject_matter="TECHNICAL_SERVICE" if classification["is_technical_service"] else "PATENT_RIGHT" if patent_transfer else "PATENT_LICENSE" if patent_license else "TECHNOLOGY",
            asset_usage="BUSINESS_RESEARCH_DATA" if "UNIVERSITY" in classification["scenario"] else "BUSINESS",
            consideration_type="SERVICE_FEE" if classification["is_technical_service"] else "TRANSFER_PRICE" if patent_transfer else "LICENSE_FEE" if patent_license else "TECHNOLOGY_PRICE",
            ownership_transfer=patent_transfer,
            possession_transfer=False,
            transaction_structure=classification["transaction_structure"],
            business_or_consumer="B2B",
            bargaining_power=bargaining,
            user_perspective=perspective,
            special_assets=special_assets,
            special_facts=[classification["scenario"]],
            payment_structure="service_fee_payment" if classification["is_technical_service"] else "patent_transfer_installments" if patent_transfer else "technology_payment",
            delivery_structure="technical_service_deliverables" if classification["is_technical_service"] else "patent_documents_and_registration" if patent_transfer else "technology_delivery",
            domain_attributes={
                "domain_pack": technology_pack.version,
                "selected_domain_packs": ["shared", "technology/common", "technology/transfer/patent_right"] if patent_transfer else ["shared", "technology/common"],
                "default_law_nodes": technology_pack.default_law_nodes,
                "economic_ratio_keys": technology_pack.economic_ratio_keys,
                "classification": classification,
                "primary_category": classification.get("primary_category"),
                "tertiary_subtype": classification.get("tertiary_subtype"),
                "excluded_subtypes": classification.get("excluded_subtypes", []),
                "secondary_modules": classification.get("secondary_modules", []),
                "ancillary_obligations": classification.get("ancillary_obligations", []),
                "factual_triggers": classification.get("factual_triggers", []),
                "license_mode": classification.get("license_mode", ""),
                "context_resolver": "technology_transaction_context",
                "lease_fields_used": False,
            },
        )

    return ContractContext(
        contract_type=contract_type,
        contract_family=domain_resolution.contract_family if domain_resolution else normalized_type.upper(),
        transaction_nature=domain_resolution.transaction_nature if domain_resolution else "GENERAL_TRANSACTION",
        contract_subtype=defaults.get("contract_subtype", "GENERAL_CONTRACT"),
        user_role=user_role,
        counterparty_role=counterparty_role,
        transaction_purpose=domain_resolution.transaction_purpose if domain_resolution else defaults.get("transaction_purpose", "general_contract"),
        usage_scenario=defaults.get("usage_scenario", "general_contract"),
        subject_matter=domain_resolution.subject_matter if domain_resolution else "GENERAL",
        consideration_type=domain_resolution.consideration_type if domain_resolution else "UNKNOWN",
        transaction_structure=domain_resolution.transaction_structure if domain_resolution else "OTHER",
        payment_structure=defaults.get("payment_structure", ""),
        delivery_structure=defaults.get("delivery_structure", ""),
        parties={k: v for k, v in (facts.get("parties") or {}).items() if v},
        bargaining_power=bargaining,
        user_perspective=perspective,
        domain_attributes={
            "domain_pack": domain_pack.version,
            "context_resolver": "isolated_generic_context",
            "lease_fields_used": False,
        },
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
    elif article == "第620条" and any(term in prop for term in ("出卖人提供", "卖方提供", "供方提供", "合格证明", "合格证", "检验报告")):
        support_type = "NOT_SUPPORT"
        confidence = "high"
    elif article == "第620条" and ("买受人" in prop or claim_type == "STATUTORY_DEFAULT") and any(
        term in prop for term in ("检验", "及时检查", "验收")
    ):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第620条":
        support_type = "CONTEXT_ONLY"
        confidence = "medium"
    elif article == "第621条" and ("买受人" in prop or claim_type == "STATUTORY_DEFAULT") and any(
        term in prop for term in ("通知", "检验期限", "合理期限", "质量不符合", "数量不符合")
    ):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第621条":
        support_type = "CONTEXT_ONLY"
        confidence = "medium"
    elif article == "第584条" and any(term in prop for term in ("可得利益", "预期利益", "可预见", "损失赔偿")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第584条":
        support_type = "CONTEXT_ONLY"
        confidence = "medium"
    elif article == "第605条" and any(term in prop for term in ("迟延受领", "未收取货物", "未按约定期限交付")):
        support_type = "DIRECT_SUPPORT" if "风险" in prop else "PARTIAL_SUPPORT"
        confidence = "high" if support_type == "DIRECT_SUPPORT" else "medium"
    elif article == "第605条":
        support_type = "CONTEXT_ONLY"
        confidence = "medium"
    elif article == "第589条" and any(term in prop for term in ("拒绝受领", "拒收", "迟延受领")):
        support_type = "DIRECT_SUPPORT" if any(term in prop for term in ("费用", "利息", "赔偿")) else "PARTIAL_SUPPORT"
        confidence = "high" if support_type == "DIRECT_SUPPORT" else "medium"
    elif article == "第589条":
        support_type = "CONTEXT_ONLY"
        confidence = "medium"
    elif article == "第591条" and any(term in prop for term in ("防止损失扩大", "减损", "扩大部分")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第604条" and any(term in prop for term in ("毁损", "灭失", "风险", "交付前", "交付后")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第607条" and any(term in prop for term in ("承运人", "运输", "风险转移")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article in {"第582条", "第617条"} and any(term in prop for term in ("质量不符合", "违约责任", "修理", "更换", "退货", "减少价款")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article in {"第582条", "第617条"}:
        support_type = "CONTEXT_ONLY"
        confidence = "medium"
    elif article == "第188条" and any(term in prop for term in ("通知", "送达", "催告", "留痕")):
        support_type = "BACKGROUND_ONLY"
        confidence = "high"
    elif article == "第565条" and any(term in prop for term in ("解除通知", "通知到达", "解除")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第585条" and any(term in prop for term in ("违约金", "约定赔偿额", "调减违约金", "调整违约金")):
        support_type = "DIRECT_SUPPORT"
        confidence = "high"
    elif article == "第585条":
        support_type = "UNCERTAIN"
        confidence = "low"
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

    if not authority:
        if article == "第188条" and any(term in prop for term in ("通知", "送达", "催告", "留痕")):
            support_type = "BACKGROUND_ONLY"
            confidence = "medium"
        else:
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
    required_sections = ["合同总体评价", "核心风险摘要", "可选优化事项", "已覆盖关键事项", "完整审查明细"]
    if "建议优先修改" not in report and "建议修改事项" not in report:
        required_sections.append("建议优先修改或建议修改事项")
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
    contract_law_lines = [line for line in (report or "").splitlines() if "合同法" in line]
    unqualified_contract_law_lines = [
        line for line in contract_law_lines
        if not all(marker in line for marker in ("签署时法律依据", "现行对应规则", "民法典"))
    ]
    if not legal_reference_findings and unqualified_contract_law_lines:
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
