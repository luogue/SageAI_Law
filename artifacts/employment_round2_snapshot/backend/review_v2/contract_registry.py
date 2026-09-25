"""Unified registry for contract-review v2 checklists.

Usage:
    from review_v2.contract_registry import get_checklist

    checklist = get_checklist("sale")
    lease_checklist = get_checklist("house_lease")  # alias of "lease"
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Dict, Tuple

from review_v2.agency_contract_checklist import AGENCY_REVIEW_CHECKLIST
from review_v2.brokerage_contract_checklist import BROKERAGE_REVIEW_CHECKLIST
from review_v2.commission_agency_contract_checklist import COMMISSION_AGENCY_REVIEW_CHECKLIST
from review_v2.construction_contract_checklist import get_construction_checklist
from review_v2.finance_lease_contract_checklist import FINANCE_LEASE_REVIEW_CHECKLIST
from review_v2.framework_supply_checklist import FRAMEWORK_SUPPLY_REVIEW_CHECKLIST
from review_v2.gift_contract_checklist import GIFT_REVIEW_CHECKLIST
from review_v2.guarantee_contract_checklist import GUARANTEE_REVIEW_CHECKLIST
from review_v2.house_lease_checklist import HOUSE_LEASE_REVIEW_CHECKLIST, ReviewCheckpoint
from review_v2.loan_contract_checklist import LOAN_REVIEW_CHECKLIST
from review_v2.safekeeping_contract_checklist import SAFEKEEPING_REVIEW_CHECKLIST
from review_v2.sale_contract_checklist import SALE_REVIEW_CHECKLIST
from review_v2.real_estate_sale_checklist import REAL_ESTATE_SALE_REVIEW_CHECKLIST
from review_v2.service_contract_checklist import SERVICE_REVIEW_CHECKLIST
from review_v2.technology_contract_checklist import TECHNOLOGY_REVIEW_CHECKLIST
from review_v2.transportation_contract_checklist import TRANSPORTATION_REVIEW_CHECKLIST
from review_v2.utility_supply_contract_checklist import UTILITY_SUPPLY_REVIEW_CHECKLIST
from review_v2.warehouse_contract_checklist import WAREHOUSE_REVIEW_CHECKLIST
from review_v2.work_contract_checklist import WORK_CONTRACT_REVIEW_CHECKLIST
from review_v2.priority_contract_types import PRIORITY_TYPES
from review_v2.employment_contract_checklist import LABOR_CHECKLIST, NON_COMPETE_CHECKLIST, CONFIDENTIALITY_CHECKLIST, TERMINATION_CHECKLIST
from review_v2.security_property_checklist import MORTGAGE_CHECKLIST, MOVABLE_PLEDGE_CHECKLIST, EQUITY_PLEDGE_CHECKLIST, RIGHTS_PLEDGE_CHECKLIST
from review_v2.equity_investment_checklist import EQUITY_TRANSFER_CHECKLIST, CAPITAL_INCREASE_CHECKLIST, INVESTMENT_CHECKLIST, SHAREHOLDERS_CHECKLIST


class ContractType(str, Enum):
    """Implemented contract-review v2 checklist types."""

    LEASE = "lease"
    SALE = "sale"
    GIFT = "gift"
    DEPOSIT = "deposit"
    WORK_CONTRACT = "work_contract"
    TRANSPORTATION = "transportation"
    AGENCY = "agency"
    LOAN = "loan"
    SERVICE = "service"
    GUARANTEE = "guarantee"
    FINANCE_LEASE = "finance_lease"
    WAREHOUSE = "warehouse"
    CONSTRUCTION = "construction"
    TECHNOLOGY = "technology"
    COMMISSION_AGENCY = "commission_agency"
    UTILITY_SUPPLY = "utility_supply"
    BROKERAGE = "brokerage"
    LABOR = "labor"
    NON_COMPETE = "non_compete"
    CONFIDENTIALITY = "confidentiality"
    EMPLOYMENT_TERMINATION = "employment_termination"
    MORTGAGE = "mortgage"
    MOVABLE_PLEDGE = "movable_pledge"
    EQUITY_PLEDGE = "equity_pledge"
    RIGHTS_PLEDGE = "rights_pledge"
    EQUITY_TRANSFER = "equity_transfer"
    CAPITAL_INCREASE = "capital_increase"
    INVESTMENT = "investment"
    SHAREHOLDERS = "shareholders"


@dataclass(frozen=True)
class ContractTypeMeta:
    key: ContractType
    display_name: str
    response_key: str
    aliases: Tuple[str, ...]
    parent_family: str = ""


CONTRACT_CHECKLISTS: Dict[str, Tuple[ReviewCheckpoint, ...]] = {
    ContractType.LEASE.value: HOUSE_LEASE_REVIEW_CHECKLIST,
    ContractType.SALE.value: SALE_REVIEW_CHECKLIST,
    ContractType.GIFT.value: GIFT_REVIEW_CHECKLIST,
    ContractType.DEPOSIT.value: SAFEKEEPING_REVIEW_CHECKLIST,
    ContractType.WORK_CONTRACT.value: WORK_CONTRACT_REVIEW_CHECKLIST,
    ContractType.TRANSPORTATION.value: TRANSPORTATION_REVIEW_CHECKLIST,
    ContractType.AGENCY.value: AGENCY_REVIEW_CHECKLIST,
    ContractType.LOAN.value: LOAN_REVIEW_CHECKLIST,
    ContractType.SERVICE.value: SERVICE_REVIEW_CHECKLIST,
    ContractType.GUARANTEE.value: GUARANTEE_REVIEW_CHECKLIST,
    ContractType.FINANCE_LEASE.value: FINANCE_LEASE_REVIEW_CHECKLIST,
    ContractType.WAREHOUSE.value: WAREHOUSE_REVIEW_CHECKLIST,
    ContractType.CONSTRUCTION.value: get_construction_checklist(),
    ContractType.TECHNOLOGY.value: TECHNOLOGY_REVIEW_CHECKLIST,
    ContractType.COMMISSION_AGENCY.value: COMMISSION_AGENCY_REVIEW_CHECKLIST,
    ContractType.UTILITY_SUPPLY.value: UTILITY_SUPPLY_REVIEW_CHECKLIST,
    ContractType.BROKERAGE.value: BROKERAGE_REVIEW_CHECKLIST,
    "labor": LABOR_CHECKLIST,
    "non_compete": NON_COMPETE_CHECKLIST,
    "confidentiality": CONFIDENTIALITY_CHECKLIST,
    "employment_termination": TERMINATION_CHECKLIST,
    "mortgage": MORTGAGE_CHECKLIST,
    "movable_pledge": MOVABLE_PLEDGE_CHECKLIST,
    "equity_pledge": EQUITY_PLEDGE_CHECKLIST,
    "rights_pledge": RIGHTS_PLEDGE_CHECKLIST,
    "equity_transfer": EQUITY_TRANSFER_CHECKLIST,
    "capital_increase": CAPITAL_INCREASE_CHECKLIST,
    "investment": INVESTMENT_CHECKLIST,
    "shareholders": SHAREHOLDERS_CHECKLIST,
}


CONTRACT_TYPE_META: Dict[ContractType, ContractTypeMeta] = {
    ContractType.LEASE: ContractTypeMeta(
        key=ContractType.LEASE,
        display_name="房屋租赁合同",
        response_key="house_lease",
        aliases=("lease", "house", "housing", "house_lease", "房屋租赁", "房屋租赁合同", "租房"),
    ),
    ContractType.SALE: ContractTypeMeta(
        key=ContractType.SALE,
        display_name="买卖合同",
        response_key="sale",
        aliases=("sale", "sales", "sale_contract", "买卖", "买卖合同", "购销合同"),
    ),
    ContractType.GIFT: ContractTypeMeta(
        key=ContractType.GIFT,
        display_name="赠与合同",
        response_key="gift",
        aliases=("gift", "donation", "gift_contract", "赠与", "赠与合同", "捐赠合同", "捐赠"),
    ),
    ContractType.DEPOSIT: ContractTypeMeta(
        key=ContractType.DEPOSIT,
        display_name="保管合同",
        response_key="deposit",
        aliases=(
            "deposit",
            "safekeeping",
            "custody",
            "bailment",
            "deposit_contract",
            "保管",
            "保管合同",
            "寄存",
            "寄存合同",
        ),
    ),
    ContractType.WORK_CONTRACT: ContractTypeMeta(
        key=ContractType.WORK_CONTRACT,
        display_name="承揽合同",
        response_key="work_contract",
        aliases=("work_contract", "contracting", "work", "service_work", "承揽", "承揽合同", "加工", "定作", "修理"),
    ),
    ContractType.TRANSPORTATION: ContractTypeMeta(
        key=ContractType.TRANSPORTATION,
        display_name="运输合同",
        response_key="transportation",
        aliases=("transportation", "transport", "carriage", "freight", "logistics", "运输", "运输合同", "货运", "货运合同", "物流", "物流合同"),
    ),
    ContractType.AGENCY: ContractTypeMeta(
        key=ContractType.AGENCY,
        display_name="委托合同",
        response_key="agency",
        aliases=("agency", "entrustment", "mandate", "agent", "委托", "委托合同", "代理", "代办", "受托"),
    ),
    ContractType.LOAN: ContractTypeMeta(
        key=ContractType.LOAN,
        display_name="借款合同",
        response_key="loan",
        aliases=("loan", "borrow", "lending", "credit", "借款", "借款合同", "借贷", "民间借贷", "金融借款", "贷款"),
    ),
    ContractType.SERVICE: ContractTypeMeta(
        key=ContractType.SERVICE,
        display_name="服务合同",
        response_key="service",
        aliases=("service", "services", "consumer_service", "training", "fitness", "beauty", "服务", "服务合同", "培训", "培训合同", "健身", "美容", "会员卡", "预付式消费"),
    ),
    ContractType.GUARANTEE: ContractTypeMeta(
        key=ContractType.GUARANTEE,
        display_name="保证合同",
        response_key="guarantee",
        aliases=("guarantee", "surety", "suretyship", "security_guarantee", "保证", "保证合同", "担保", "担保合同", "保证担保", "担保人"),
    ),
    ContractType.FINANCE_LEASE: ContractTypeMeta(
        key=ContractType.FINANCE_LEASE,
        display_name="融资租赁合同",
        response_key="finance_lease",
        aliases=("finance_lease", "financial_lease", "leasing", "融资租赁", "融资租赁合同", "售后回租", "回租", "以租代购"),
    ),
    ContractType.WAREHOUSE: ContractTypeMeta(
        key=ContractType.WAREHOUSE,
        display_name="仓储合同",
        response_key="warehouse",
        aliases=("warehouse", "storage", "warehousing", "warehouse_contract", "仓储", "仓储合同", "仓储物", "仓单", "入库单"),
    ),
    ContractType.CONSTRUCTION: ContractTypeMeta(
        key=ContractType.CONSTRUCTION,
        display_name="建设工程合同",
        response_key="construction",
        aliases=("construction", "construction_contract", "construction_project", "building", "工程", "建设工程", "建设工程合同", "施工合同", "工程合同"),
    ),
    ContractType.TECHNOLOGY: ContractTypeMeta(
        key=ContractType.TECHNOLOGY,
        display_name="技术合同",
        response_key="technology",
        aliases=("technology", "tech", "technology_contract", "技术", "技术合同", "技术开发", "技术转让", "技术许可", "技术咨询", "技术服务"),
    ),
    ContractType.COMMISSION_AGENCY: ContractTypeMeta(
        key=ContractType.COMMISSION_AGENCY,
        display_name="行纪合同",
        response_key="commission_agency",
        aliases=("commission_agency", "commission", "commission_contract", "commission_agency_contract", "行纪", "行纪合同", "代购", "代销", "寄售"),
    ),
    ContractType.UTILITY_SUPPLY: ContractTypeMeta(
        key=ContractType.UTILITY_SUPPLY,
        display_name="供用电、水、气、热力合同",
        response_key="utility_supply",
        aliases=("utility_supply", "utility", "utilities", "power_supply", "water_supply", "gas_supply", "heat_supply", "供用", "供用电", "供用水", "供用气", "供用热力", "供水供电"),
    ),
    ContractType.BROKERAGE: ContractTypeMeta(
        key=ContractType.BROKERAGE,
        display_name="中介合同",
        response_key="brokerage",
        aliases=("brokerage", "broker", "intermediary", "intermediary_contract", "brokerage_contract", "居间", "居间合同", "中介", "中介合同", "房产中介"),
    ),
}


CONTRACT_TYPE_META.update({
    ContractType(key): ContractTypeMeta(ContractType(key), meta.name, key,
        (key, *meta.titles, *(("employment", "labor_contract") if key == "labor" else ("pledge",) if key == "movable_pledge" else ())),
        parent_family=meta.family)
    for key, meta in PRIORITY_TYPES.items()
})

# Additive type tree; existing flat keys and APIs remain valid.
CONTRACT_TYPE_TREE = {
    family: tuple(key for key, meta in PRIORITY_TYPES.items() if meta.family == family)
    for family in ("EMPLOYMENT", "SECURITY_PROPERTY", "EQUITY_INVESTMENT")
}

_ALIAS_TO_TYPE: Dict[str, ContractType] = {
    alias.lower(): meta.key
    for meta in CONTRACT_TYPE_META.values()
    for alias in meta.aliases
}

_VALID_RISK_LEVELS = {"高", "中", "低"}
_VALID_KINDS = {"required", "forbidden"}


class UnsupportedContractTypeError(ValueError):
    """Raised when review v2 has no checklist for a requested contract type."""


def supported_contract_types() -> Tuple[str, ...]:
    return tuple(contract_type.value for contract_type in ContractType)


def supported_contract_display_names() -> Tuple[str, ...]:
    return tuple(meta.display_name for meta in CONTRACT_TYPE_META.values())


def resolve_contract_type(contract_type: str | None) -> ContractType:
    normalized = (contract_type or ContractType.LEASE.value).strip().lower()
    if normalized in _ALIAS_TO_TYPE:
        return _ALIAS_TO_TYPE[normalized]
    supported = "、".join(supported_contract_types())
    raise UnsupportedContractTypeError(f"不支持的合同类型：{contract_type or ''}。当前支持：{supported}")


def get_contract_meta(contract_type: str | ContractType | None) -> ContractTypeMeta:
    if isinstance(contract_type, ContractType):
        return CONTRACT_TYPE_META[contract_type]
    return CONTRACT_TYPE_META[resolve_contract_type(contract_type)]


def get_checklist(contract_type: str | ContractType) -> Tuple[ReviewCheckpoint, ...]:
    resolved = contract_type if isinstance(contract_type, ContractType) else resolve_contract_type(contract_type)
    try:
        return CONTRACT_CHECKLISTS[resolved.value]
    except KeyError as exc:
        raise UnsupportedContractTypeError(f"合同类型 {resolved.value} 尚未配置审查清单") from exc


SALE_COMMON_NODE_IDS = {
    "common_effective_clause", "common_dispute_resolution", "common_jurisdiction",
    "sale_validity_party_capacity", "sale_validity_true_intent", "sale_validity_mandatory_law",
    "sale_price_amount_currency", "sale_payment_schedule", "sale_payment_method_account",
    "sale_breach_liability_general", "sale_termination", "common_force_majeure",
}


def _owned_sale_checklist() -> Tuple[ReviewCheckpoint, ...]:
    rows = []
    for checkpoint in SALE_REVIEW_CHECKLIST:
        owner = "sale/common" if checkpoint.node_id in SALE_COMMON_NODE_IDS else "sale/goods"
        rows.append(replace(
            checkpoint,
            allowed_families=("SALE",),
            allowed_subject_matters=("GOODS", "EQUIPMENT", "UNCERTAIN") if owner == "sale/goods" else (),
            prohibited_subject_matters=("REAL_ESTATE",) if owner == "sale/goods" else (),
            domain_owner=owner,
            material_group="COMMON" if owner == "sale/common" else "GOODS",
        ))
    return tuple(rows)


def get_checklist_for_resolution(contract_type: str | ContractType, resolution: object) -> Tuple[ReviewCheckpoint, ...]:
    resolved = contract_type if isinstance(contract_type, ContractType) else resolve_contract_type(contract_type)
    if resolved is ContractType.TECHNOLOGY and getattr(resolution, "transaction_structure", "") == "MIXED_SALE_TECHNOLOGY_LICENSE":
        sale_rows = tuple(replace(row, allowed_families=("TECHNOLOGY", "SALE")) for row in _owned_sale_checklist())
        return TECHNOLOGY_REVIEW_CHECKLIST + sale_rows
    if resolved is not ContractType.SALE:
        return get_checklist(resolved)
    owned = _owned_sale_checklist()
    subject = getattr(resolution, "subject_matter", "UNCERTAIN")
    if subject == "REAL_ESTATE":
        return tuple(row for row in owned if row.domain_owner == "sale/common") + REAL_ESTATE_SALE_REVIEW_CHECKLIST
    rows = tuple(
        row for row in owned
        if not row.allowed_subject_matters or subject in row.allowed_subject_matters
    )
    if getattr(resolution, "transaction_structure", "") == "FRAMEWORK_SUPPLY":
        rows += FRAMEWORK_SUPPLY_REVIEW_CHECKLIST
    return rows


def review_registry_debug(contract_type: str | ContractType, resolution: object) -> Dict[str, object]:
    rows = get_checklist_for_resolution(contract_type, resolution)
    traced_ids = {"TC-01-03", "TC-08-01", "TC-08-02", "TC-08-03", "TC-08-04", "TC-08-05", "TC-10-01", "TC-11-01", "TC-11-02", "TC-11-03", "TC-11-04", "TC-13-01"}
    return {
        "registry_module": __name__,
        "registry_file": __file__,
        "registry_type": type(rows).__name__,
        "registry_object_id": id(rows),
        "resolved_subject_matter": getattr(resolution, "subject_matter", ""),
        "transaction_structure": getattr(resolution, "transaction_structure", ""),
        "loaded_review_count": len(rows),
        "loaded_review_ids": [row.item_id for row in rows],
        "domain_owners": sorted({row.domain_owner for row in rows}),
        "prohibited_reviews": [
            row.item_id for row in rows
            if getattr(resolution, "subject_matter", "") in row.prohibited_subject_matters
        ],
        "review_bindings": {
            row.item_id: {
                "checkpoint_type": f"{type(row).__module__}.{type(row).__name__}",
                "node_id": row.node_id,
                "applicability_evaluator": "review_v2.engine._is_checkpoint_applicable",
                "coverage_evaluator": "review_v2.engine._judge_checkpoints_with_registry",
                "post_rule_evaluator": "review_v2.engine._apply_contract_specific_post_rules",
            }
            for row in rows if row.item_id in traced_ids
        },
    }


def validate_checklist_integrity(checklist: Tuple[ReviewCheckpoint, ...], *, checklist_key: str = "") -> Tuple[str, ...]:
    """Validate one checklist and return non-fatal warnings.

    Fatal structural problems raise ValueError. Warnings are returned for review conventions
    that are not strict schema violations, such as forbidden items carrying medium/high risk.
    """

    seen_item_ids: set[str] = set()
    seen_node_ids: set[str] = set()
    warnings: list[str] = []

    for checkpoint in checklist:
        prefix = f"{checklist_key}:{checkpoint.item_id}" if checklist_key else checkpoint.item_id
        if not isinstance(checkpoint, ReviewCheckpoint):
            raise ValueError(f"{prefix} 不是 ReviewCheckpoint 实例")
        if not checkpoint.item_id:
            raise ValueError(f"{prefix} 缺少 item_id")
        if checkpoint.item_id in seen_item_ids:
            raise ValueError(f"{prefix} item_id 重复")
        seen_item_ids.add(checkpoint.item_id)
        if not checkpoint.node_id:
            raise ValueError(f"{prefix} 缺少 node_id")
        seen_node_ids.add(checkpoint.node_id)
        if checkpoint.risk_level not in _VALID_RISK_LEVELS:
            raise ValueError(f"{prefix} risk_level 不合法：{checkpoint.risk_level}")
        if checkpoint.kind not in _VALID_KINDS:
            raise ValueError(f"{prefix} kind 不合法：{checkpoint.kind}")
        if checkpoint.kind == "forbidden" and checkpoint.risk_level != "低":
            warnings.append(f"{prefix} 为 forbidden 条款但风险等级为 {checkpoint.risk_level}，请人工确认是否符合业务口径")
        for field_name in (
            "title",
            "terms",
            "risk_point_missing",
            "risk_point_present",
            "suggested_clause",
            "legal_basis",
            "legal_consequence_if_missing",
            "semantic_question",
            "evidence_scope",
            "pass_criteria",
            "partial_criteria",
            "applicable_if",
        ):
            if not getattr(checkpoint, field_name):
                raise ValueError(f"{prefix} 缺少字段：{field_name}")

    if not seen_node_ids:
        raise ValueError(f"{checklist_key or 'checklist'} 为空")
    return tuple(warnings)


def validate_all_checklists() -> Dict[str, Tuple[str, ...]]:
    return {
        key: validate_checklist_integrity(checklist, checklist_key=key)
        for key, checklist in CONTRACT_CHECKLISTS.items()
    }


_REGISTRY_WARNINGS = validate_all_checklists()
