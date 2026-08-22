"""Domain-specific review pack registry for the v2 review engine."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class DefaultRule:
    rule_id: str
    domain: str
    proposition: str
    applicability_conditions: List[str]
    authority_ids: List[str]
    protection_scope: str
    exceptions: List[str]
    overrideable: bool
    confidence: str
    status: str = "PARTIAL_DEFAULT"
    proposition_id: str = ""
    supplied_element_ids: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DomainPack:
    contract_type: str
    version: str
    context_defaults: Dict[str, Any] = field(default_factory=dict)
    default_law_nodes: Dict[str, str] = field(default_factory=dict)
    default_law_rules: Dict[str, DefaultRule] = field(default_factory=dict)
    economic_ratio_keys: List[str] = field(default_factory=list)
    pack_id: str = ""
    parent_pack_ids: List[str] = field(default_factory=list)
    subject_matter: str = ""

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


SHARED_DOMAIN_PACK = DomainPack(
    contract_type="shared",
    version="domain-pack-shared-1.0",
    context_defaults={
        "jurisdiction": "CN",
        "business_or_consumer": "unknown",
        "bargaining_power": "unknown",
    },
    economic_ratio_keys=[
        "contract_value_ratio",
        "batch_value_ratio",
        "unpaid_amount_ratio",
        "advance_payment_ratio",
        "replacement_cost_ratio",
        "delay_loss_ratio",
    ],
)


SALE_DOMAIN_PACK = DomainPack(
    contract_type="sale",
    version="domain-pack-sale-1.0",
    context_defaults={
        "contract_subtype": "GENERAL_GOODS_SALE",
        "transaction_purpose": "goods_sale",
        "usage_scenario": "GENERAL_GOODS_SALE",
        "delivery_structure": "goods_delivery",
        "payment_structure": "goods_price_payment",
    },
    default_law_nodes={
        "sale_risk_transfer_delivery": "PARTIAL_DEFAULT",
        "sale_risk_carrier_delivery": "PARTIAL_DEFAULT",
        "sale_risk_buyer_delay_acceptance": "PARTIAL_DEFAULT",
        "sale_inspection_period": "PARTIAL_DEFAULT",
        "sale_quality_liability": "PARTIAL_DEFAULT",
        "sale_third_party_rights": "PARTIAL_DEFAULT",
        "sale_title_warranty": "PARTIAL_DEFAULT",
        "sale_delay_performance": "PARTIAL_DEFAULT",
        "sale_breach_damages": "PARTIAL_DEFAULT",
        "sale_expectation_loss": "PARTIAL_DEFAULT",
        "sale_termination": "PARTIAL_DEFAULT",
        "common_force_majeure": "PARTIAL_DEFAULT",
    },
    default_law_rules={
        "sale_risk_transfer_delivery": DefaultRule(
            rule_id="SALE-DEFAULT-RISK-DELIVERY",
            domain="sale",
            proposition="标的物毁损、灭失风险原则上随交付转移，但合同约定和法定例外优先。",
            applicability_conditions=["买卖合同", "未约定完整风险转移规则"],
            authority_ids=["CN-CC-604"],
            protection_scope="提供一般交付场景的风险转移基准，不替代交付节点、验收方式和业务例外约定。",
            exceptions=["当事人另有约定", "法律另有规定", "出卖人原因导致不能按约交付"],
            overrideable=True,
            confidence="high",
            status="CLEAR_DEFAULT",
        ),
        "sale_risk_carrier_delivery": DefaultRule(
            rule_id="SALE-DEFAULT-RISK-CARRIER",
            domain="sale",
            proposition="需要运输且未约定交付地点时，风险通常在货交第一承运人后转移。",
            applicability_conditions=["买卖合同", "交易需要运输", "当事人未另行约定交付地点或风险节点"],
            authority_ids=["CN-CC-607"],
            protection_scope="仅覆盖法定运输交付场景，不解决承运人选择、保险、包装和具体交接证据。",
            exceptions=["当事人约定交付地点或风险节点", "出卖人未按约包装或交运"],
            overrideable=True,
            confidence="high",
        ),
        "sale_risk_buyer_delay_acceptance": DefaultRule(
            rule_id="SALE-DEFAULT-DELAYED-ACCEPTANCE",
            domain="sale",
            proposition="买受人无正当理由拒绝或迟延受领时，增加的费用及相应风险依法分配。",
            applicability_conditions=["买卖合同", "买受人迟延或拒绝受领"],
            authority_ids=["CN-CC-605", "CN-CC-589"],
            protection_scope="提供迟延受领后的基础责任规则，不替代催告、保管、费用计算和处置流程。",
            exceptions=["买受人有正当拒收理由", "标的物不符合约定"],
            overrideable=True,
            confidence="medium",
        ),
        "sale_inspection_period": DefaultRule(
            rule_id="SALE-DEFAULT-INSPECTION",
            domain="sale",
            proposition="检验期限未约定或不明确时，买受人仍应在合理期限内检验并通知。",
            applicability_conditions=["买卖合同", "检验期限缺失或不完整"],
            authority_ids=["CN-CC-620", "CN-CC-621"],
            protection_scope="提供合理期限和通知的法定补充，不确定具体商品所需检验时长及隐蔽瑕疵流程。",
            exceptions=["当事人约定检验期限", "出卖人知道或应当知道标的物不符合约定"],
            overrideable=True,
            confidence="high",
            status="CLEAR_DEFAULT",
        ),
        "sale_quality_liability": DefaultRule(
            rule_id="SALE-DEFAULT-QUALITY-REMEDY",
            domain="sale",
            proposition="标的物不符合质量要求时，买受人可依法主张修理、重作、更换、退货、减价或赔偿。",
            applicability_conditions=["买卖合同", "标的物不符合约定质量"],
            authority_ids=["CN-CC-582", "CN-CC-617"],
            protection_scope="提供法定质量救济类型，不替代异议期限、举证标准、操作程序和费用承担约定。",
            exceptions=["标的物性质或当事人约定限制特定救济方式"],
            overrideable=True,
            confidence="high",
            status="CLEAR_DEFAULT",
        ),
        "sale_breach_damages": DefaultRule(
            rule_id="SALE-DEFAULT-BREACH-DAMAGES",
            domain="sale",
            proposition="违约造成损失时，损失赔偿适用可预见性、减损和损益相抵等一般规则。",
            applicability_conditions=["合同违约", "存在可证明损失"],
            authority_ids=["CN-CC-584", "CN-CC-591"],
            protection_scope="提供损害赔偿基础规则，不自动证明损失金额、因果关系或约定违约金合理性。",
            exceptions=["免责事由成立", "损失不可预见或未履行减损义务"],
            overrideable=True,
            confidence="high",
            status="CLEAR_DEFAULT",
        ),
        "sale_expectation_loss": DefaultRule(
            rule_id="SALE-DEFAULT-EXPECTATION-LOSS",
            domain="sale",
            proposition="可得利益损失赔偿受订约时可预见性边界约束。",
            applicability_conditions=["合同违约", "主张可得利益损失"],
            authority_ids=["CN-CC-584"],
            protection_scope="现行法律提供可得利益赔偿及可预见性边界，但不替代损失金额、因果关系和证明责任。",
            exceptions=["损失不具有可预见性", "损失或因果关系无法证明"],
            overrideable=False,
            confidence="high",
            status="PARTIAL_DEFAULT",
            proposition_id="legal.damages.foreseeability_limit",
            supplied_element_ids=["foreseeability_limit"],
        ),
        "sale_termination": DefaultRule(
            rule_id="SALE-DEFAULT-TERMINATION",
            domain="sale",
            proposition="达到法定或约定解除条件时，当事人可依法通知解除并进行清算。",
            applicability_conditions=["合同目的不能实现或其他解除事由", "依法履行通知程序"],
            authority_ids=["CN-CC-563", "CN-CC-565"],
            protection_scope="提供法定解除事由和通知框架，不替代合同中的宽限期、证据、返还和结算流程。",
            exceptions=["不具备法定或约定解除事由", "解除通知未有效到达"],
            overrideable=True,
            confidence="high",
        ),
    },
    economic_ratio_keys=SHARED_DOMAIN_PACK.economic_ratio_keys,
)


HOUSE_LEASE_DOMAIN_PACK = DomainPack(
    contract_type="house_lease",
    version="domain-pack-house-lease-1.0",
    context_defaults={
        "contract_subtype": "RESIDENTIAL_LEASE",
        "transaction_purpose": "residential_lease",
        "usage_scenario": "residential_living",
        "payment_structure": "rent_payment",
    },
)

SERVICE_DOMAIN_PACK = DomainPack(
    contract_type="service",
    version="domain-pack-service-1.0",
    context_defaults={
        "contract_subtype": "GENERAL_SERVICE",
        "transaction_purpose": "service_provision",
        "usage_scenario": "GENERAL_SERVICE",
        "payment_structure": "service_fee_payment",
        "delivery_structure": "service_performance",
    },
)


SALE_COMMON_DOMAIN_PACK = DomainPack(
    contract_type="sale", version="domain-pack-sale-common-1.0", pack_id="sale/common",
    parent_pack_ids=["shared"], subject_matter="ANY_SALE",
    context_defaults={"transaction_nature": "OWNERSHIP_TRANSFER", "consideration_type": "PURCHASE_PRICE"},
)

SALE_REAL_ESTATE_COMMON_DOMAIN_PACK = DomainPack(
    contract_type="sale", version="domain-pack-sale-real-estate-common-1.0", pack_id="sale/real_estate/common",
    parent_pack_ids=["shared", "sale/common"], subject_matter="REAL_ESTATE",
    context_defaults={"transaction_purpose": "real_estate_purchase", "delivery_structure": "property_handover", "payment_structure": "property_purchase_financing"},
)

SALE_RESIDENTIAL_SECONDARY_DOMAIN_PACK = DomainPack(
    contract_type="sale", version="domain-pack-sale-residential-secondary-1.0", pack_id="sale/real_estate/residential_secondary",
    parent_pack_ids=["shared", "sale/common", "sale/real_estate/common"], subject_matter="REAL_ESTATE",
    context_defaults={"contract_subtype": "RESIDENTIAL_SECONDARY_REAL_ESTATE_SALE", "asset_usage": "RESIDENTIAL"},
)

SALE_GOODS_GENERAL_DOMAIN_PACK = DomainPack(
    contract_type="sale", version="domain-pack-sale-goods-general-1.0", pack_id="sale/goods/general",
    parent_pack_ids=["shared", "sale/common"], subject_matter="GOODS", context_defaults=SALE_DOMAIN_PACK.context_defaults,
    default_law_nodes=SALE_DOMAIN_PACK.default_law_nodes, default_law_rules=SALE_DOMAIN_PACK.default_law_rules,
    economic_ratio_keys=SALE_DOMAIN_PACK.economic_ratio_keys,
)

SALE_GOODS_EQUIPMENT_DOMAIN_PACK = DomainPack(
    contract_type="sale", version="domain-pack-sale-goods-equipment-1.0", pack_id="sale/goods/equipment",
    parent_pack_ids=["shared", "sale/common", "sale/goods/general"], subject_matter="EQUIPMENT",
    context_defaults={**SALE_DOMAIN_PACK.context_defaults, "contract_subtype": "EQUIPMENT_SALE", "usage_scenario": "PRODUCTION_EQUIPMENT_SALE"},
    default_law_nodes=SALE_DOMAIN_PACK.default_law_nodes, default_law_rules=SALE_DOMAIN_PACK.default_law_rules,
    economic_ratio_keys=SALE_DOMAIN_PACK.economic_ratio_keys,
)

SALE_GOODS_FRAMEWORK_SUPPLY_DOMAIN_PACK = DomainPack(
    contract_type="sale", version="domain-pack-sale-framework-supply-1.0", pack_id="sale/goods/framework_supply",
    parent_pack_ids=["shared", "sale/common", "sale/goods/general"], subject_matter="GOODS",
    context_defaults={
        **SALE_DOMAIN_PACK.context_defaults,
        "contract_subtype": "FRAMEWORK_SUPPLY",
        "usage_scenario": "LONG_TERM_INDUSTRIAL_SUPPLY",
        "delivery_structure": "order_driven_recurring_delivery",
        "payment_structure": "periodic_reconciliation_settlement",
    },
    default_law_nodes=SALE_DOMAIN_PACK.default_law_nodes,
    default_law_rules=SALE_DOMAIN_PACK.default_law_rules,
    economic_ratio_keys=SALE_DOMAIN_PACK.economic_ratio_keys,
)


DOMAIN_PACKS: Dict[str, DomainPack] = {
    "shared": SHARED_DOMAIN_PACK,
    "sale": SALE_DOMAIN_PACK,
    "house_lease": HOUSE_LEASE_DOMAIN_PACK,
    "lease": HOUSE_LEASE_DOMAIN_PACK,
    "service": SERVICE_DOMAIN_PACK,
    "sale/common": SALE_COMMON_DOMAIN_PACK,
    "sale/goods/general": SALE_GOODS_GENERAL_DOMAIN_PACK,
    "sale/goods/equipment": SALE_GOODS_EQUIPMENT_DOMAIN_PACK,
    "sale/goods/framework_supply": SALE_GOODS_FRAMEWORK_SUPPLY_DOMAIN_PACK,
    "sale/real_estate/common": SALE_REAL_ESTATE_COMMON_DOMAIN_PACK,
    "sale/real_estate/residential_secondary": SALE_RESIDENTIAL_SECONDARY_DOMAIN_PACK,
}


def get_domain_pack(contract_type: str) -> DomainPack:
    return DOMAIN_PACKS.get(contract_type or "", SHARED_DOMAIN_PACK)


def domain_pack_snapshot(contract_type: str) -> Dict[str, Any]:
    pack = get_domain_pack(contract_type)
    return pack.to_public_dict()


def get_default_rule(contract_type: str, node_id: str) -> DefaultRule | None:
    return get_domain_pack(contract_type).default_law_rules.get(node_id)


def composed_domain_pack_snapshot(pack_ids: List[str]) -> Dict[str, Any]:
    packs = [get_domain_pack(pack_id).to_public_dict() for pack_id in pack_ids]
    selected = packs[-1] if packs else SHARED_DOMAIN_PACK.to_public_dict()
    return {
        **selected,
        "composition_order": list(pack_ids),
        "packs": packs,
        "composition_version": "domain-composition-6.5",
    }
