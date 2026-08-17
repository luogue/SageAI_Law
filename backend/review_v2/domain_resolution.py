"""Hierarchical contract-domain resolution based on source-backed signals."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Sequence, Tuple

from review_v2.clause_parser import ParsedClause


@dataclass(frozen=True)
class ClassificationEvidence:
    signal_type: str
    signal: str
    target: str
    weight: int
    source_clause_ids: List[str]


@dataclass(frozen=True)
class DomainResolution:
    contract_family: str
    subject_matter: str
    transaction_nature: str
    contract_subtype: str
    asset_usage: str
    consideration_type: str
    ownership_transfer: bool
    possession_transfer: bool
    transaction_structure: str
    product_category: str
    transaction_purpose: str
    jurisdiction: str
    primary_subject: str
    accessory_subjects: List[str]
    selected_domain_packs: List[str]
    rejected_domain_packs: List[str]
    confidence: str
    evidence: List[ClassificationEvidence] = field(default_factory=list)
    domain_attributes: Dict[str, Any] = field(default_factory=dict)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


REAL_ESTATE_SIGNALS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("title_registration", ("不动产权证", "房地产权证", "登记权利人"), 4),
    ("ownership_transfer", ("转移登记", "转让过户", "房地产过户", "产权过户"), 4),
    ("land_right", ("土地使用权", "国有土地", "土地用途"), 3),
    ("property_identity", ("房地产坐落", "房屋建筑面积", "房屋用途", "住宅"), 3),
    ("encumbrance", ("抵押登记", "抵押权人", "司法查封"), 3),
    ("real_estate_process", ("房地产交易中心", "预告登记", "交房"), 3),
)

GOODS_SIGNALS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("goods_identity", ("货物名称", "产品名称", "设备名称", "材料名称"), 3),
    ("goods_quantity", ("计量单位", "供货数量", "产品数量", "规格型号"), 3),
    ("goods_delivery", ("交货地点", "承运人", "物流运输", "分批交货"), 2),
    ("goods_quality", ("质量标准", "检验标准", "质保期", "包装标准"), 2),
)


def _collect(text: str, clauses: Sequence[ParsedClause], definitions) -> tuple[int, List[ClassificationEvidence]]:
    rows: List[ClassificationEvidence] = []
    score = 0
    for signal_type, terms, weight in definitions:
        hits = [term for term in terms if term in text]
        if not hits:
            continue
        source_ids = [clause.clause_id for clause in clauses if any(term in clause.text for term in hits)][:8]
        rows.append(ClassificationEvidence(signal_type, hits[0], "REAL_ESTATE" if definitions is REAL_ESTATE_SIGNALS else "GOODS", weight, source_ids))
        score += weight
    return score, rows


def resolve_contract_domain(contract_family: str, text: str, clauses: Sequence[ParsedClause]) -> DomainResolution:
    family = "SALE" if contract_family in {"sale", "SALE"} else contract_family.upper()
    if family != "SALE":
        is_lease = contract_family in {"lease", "house_lease"}
        return DomainResolution(
            contract_family=family,
            subject_matter="REAL_ESTATE" if is_lease else "GENERAL",
            transaction_nature="USE_RIGHT_GRANT" if is_lease else "GENERAL_TRANSACTION",
            contract_subtype="RESIDENTIAL_LEASE" if is_lease else "GENERAL_CONTRACT",
            asset_usage="RESIDENTIAL" if is_lease else "UNKNOWN",
            consideration_type="RENT" if is_lease else "UNKNOWN",
            ownership_transfer=False,
            possession_transfer=is_lease,
            transaction_structure="SINGLE_TRANSACTION",
            product_category="NOT_APPLICABLE",
            transaction_purpose="residential_lease" if is_lease else "general_contract",
            jurisdiction="CN",
            primary_subject="REAL_ESTATE" if is_lease else "GENERAL",
            accessory_subjects=[],
            selected_domain_packs=["shared", "lease/residential"] if is_lease else ["shared"],
            rejected_domain_packs=[], confidence="high" if is_lease else "medium",
        )

    re_score, re_evidence = _collect(text, clauses, REAL_ESTATE_SIGNALS)
    goods_score, goods_evidence = _collect(text, clauses, GOODS_SIGNALS)
    if re_score >= 7 and len(re_evidence) >= 2:
        residential = any(term in text for term in ("住宅", "居住", "个人住房"))
        commercial = any(term in text for term in ("商铺", "商业用房", "办公用房")) and not residential
        usage = "RESIDENTIAL" if residential else "COMMERCIAL" if commercial else "UNKNOWN"
        subtype = "RESIDENTIAL_SECONDARY_REAL_ESTATE_SALE" if residential else "COMMERCIAL_REAL_ESTATE_SALE" if commercial else "REAL_ESTATE_SALE"
        packs = ["shared", "sale/common", "sale/real_estate/common"]
        packs.append("sale/real_estate/residential_secondary" if residential else "sale/real_estate/commercial" if commercial else "sale/real_estate/general")
        return DomainResolution(
            contract_family="SALE", subject_matter="REAL_ESTATE", transaction_nature="OWNERSHIP_TRANSFER",
            contract_subtype=subtype, asset_usage=usage, consideration_type="PURCHASE_PRICE",
            ownership_transfer=True, possession_transfer=True, transaction_purpose="real_estate_purchase",
            transaction_structure="SINGLE_TRANSACTION", product_category="REAL_ESTATE",
            jurisdiction="CN", primary_subject="REAL_ESTATE", accessory_subjects=["FIXTURES", "LAND_USE_RIGHT"],
            selected_domain_packs=packs, rejected_domain_packs=["sale/goods/general", "sale/goods/equipment"],
            confidence="high", evidence=re_evidence,
            domain_attributes={"real_estate_score": re_score, "goods_score": goods_score, "distinct_real_estate_signal_types": len(re_evidence)},
        )
    from review_v2.framework_supply import extract_framework_supply_profile

    framework = extract_framework_supply_profile(text, clauses)
    subject = "EQUIPMENT" if framework.product_category == "EQUIPMENT" else "GOODS" if goods_score >= 3 else "UNCERTAIN"
    if framework.is_framework:
        subject = "GOODS"
        subtype = "FRAMEWORK_SUPPLY"
    else:
        subtype = "EQUIPMENT_SALE" if subject == "EQUIPMENT" else "GENERAL_GOODS_SALE" if subject == "GOODS" else "SALE_SUBJECT_UNCERTAIN"
    selected_pack = "sale/goods/framework_supply" if framework.is_framework else "sale/goods/equipment" if subject == "EQUIPMENT" else "sale/goods/general"
    return DomainResolution(
        contract_family="SALE", subject_matter=subject, transaction_nature="OWNERSHIP_TRANSFER",
        contract_subtype=subtype, asset_usage="PRODUCTION" if subject == "EQUIPMENT" else "GENERAL",
        consideration_type="PURCHASE_PRICE", ownership_transfer=True, possession_transfer=True,
        transaction_structure=framework.transaction_structure,
        product_category=framework.product_category,
        transaction_purpose="goods_sale" if subject != "UNCERTAIN" else "sale_subject_pending",
        jurisdiction="CN", primary_subject=subject, accessory_subjects=[],
        selected_domain_packs=["shared", "sale/common", selected_pack],
        rejected_domain_packs=["sale/real_estate/common"], confidence="high" if goods_score >= 5 else "medium",
        evidence=goods_evidence,
        domain_attributes={
            "real_estate_score": re_score,
            "goods_score": goods_score,
            "distinct_goods_signal_types": len(goods_evidence),
            "framework_classification_score": framework.classification_score,
            "framework_classification_signals": framework.classification_signals,
        },
    )
