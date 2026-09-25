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
    default_law_nodes={
        "owner_change_no_break_lease": "CLEAR_DEFAULT",
        "lease_before_sale": "CLEAR_DEFAULT",
        "normal_wear": "CLEAR_DEFAULT",
        "tenant_death_successor": "CLEAR_DEFAULT",
        "lessor_death": "CLEAR_DEFAULT",
        "indefinite_lease": "CLEAR_DEFAULT",
        "force_majeure": "PARTIAL_DEFAULT",
        "changed_circumstances": "PARTIAL_DEFAULT",
        "pre_delivery_defect": "PARTIAL_DEFAULT",
        "third_party_tort": "PARTIAL_DEFAULT",
        "third_party_defect": "PARTIAL_DEFAULT",
        "housing_safety_emergency": "PARTIAL_DEFAULT",
        "reasonable_repair_cost": "PARTIAL_DEFAULT",
        "excessive_deduction": "CLEAR_DEFAULT",
        "handover_evidence": "PARTIAL_DEFAULT",
        "deposit_return_timing": "PARTIAL_DEFAULT",
        "deposit_offset_order": "PARTIAL_DEFAULT",
        "property_damage_deposit_evidence": "PARTIAL_DEFAULT",
    },
    default_law_rules={
        "lease_before_sale": DefaultRule(
            rule_id="LEASE-DEFAULT-SALE-NO-BREAK",
            domain="house_lease",
            proposition="租赁期间租赁物所有权发生变动的，不影响租赁合同效力。",
            proposition_id="lease_ownership_change_no_break",
            applicability_conditions=["房屋租赁合同", "承租人按租赁合同占有使用期间", "租赁物所有权发生变动"],
            authority_ids=["CN-CIVIL-CODE-725"],
            protection_scope="《民法典》第725条提供买卖不破租赁的法定承继保护，所有权变动不影响租赁合同效力。",
            exceptions=["当事人另有有效约定", "承租人未依租赁合同占有租赁物", "法律另有特别规定"],
            overrideable=False,
            confidence="high",
            status="CLEAR_DEFAULT",
            supplied_element_ids=["core_contract_arrangement"],
        ),
        "indefinite_lease": DefaultRule(
            rule_id="LEASE-DEFAULT-INDEFINITE-LEASE",
            domain="house_lease",
            proposition="租赁期限届满后承租人继续使用租赁物，出租人没有提出异议的，原租赁合同继续有效但租赁期限转为不定期；不定期租赁解除应在合理期限前通知。",
            proposition_id="lease_post_expiry_indefinite_default",
            applicability_conditions=["房屋租赁合同", "租赁期限届满", "承租人继续使用", "出租人未提出异议或继续收租"],
            authority_ids=["CN-CIVIL-CODE-734", "CN-CIVIL-CODE-730"],
            protection_scope="《民法典》第734条、第730条提供期满继续使用转不定期租赁及合理期限通知解除的法定规则。",
            exceptions=["当事人另有有效约定", "出租人及时提出异议", "租赁关系因其他法定或约定事由终止"],
            overrideable=True,
            confidence="high",
            status="CLEAR_DEFAULT",
            supplied_element_ids=["post_expiry_continue_use", "no_objection_or_rent_acceptance", "reasonable_notice"],
        ),
        "excessive_deduction": DefaultRule(
            rule_id="LEASE-DEFAULT-LIQUIDATED-DAMAGES-ADJUSTMENT",
            domain="house_lease",
            proposition="约定违约金低于或过分高于造成损失的，当事人可以依法请求增加或适当减少。",
            proposition_id="lease_liquidated_damages_judicial_adjustment",
            applicability_conditions=["房屋租赁合同", "合同约定押金扣款、违约金或赔偿金额", "金额与实际损失存在明显偏离争议"],
            authority_ids=["CN-CIVIL-CODE-585"],
            protection_scope="《民法典》第585条提供违约金过高或过低时请求司法调整的救济，合同未写明不等于当然无法调整。",
            exceptions=["不存在约定违约金或约定赔偿额", "当事人未依法主张调整", "法院或仲裁机构结合损失、履行情况和过错程度裁量后不予调整"],
            overrideable=False,
            confidence="high",
            status="CLEAR_DEFAULT",
            supplied_element_ids=["adjustment"],
        ),
        "reasonable_repair_cost": DefaultRule(
            rule_id="LEASE-DEFAULT-REPAIR-COST-ADJUSTMENT",
            domain="house_lease",
            proposition="押金扣款、违约金或约定赔偿额明显偏离实际损失时，当事人可以依法请求调整；该规则不替代维修事实和实际发生金额的证明。",
            proposition_id="lease_repair_cost_reasonableness_statutory_relief",
            applicability_conditions=["房屋租赁合同", "发生维修费、押金扣款或赔偿金额争议", "约定金额与实际损失存在明显偏离"],
            authority_ids=["CN-CIVIL-CODE-585"],
            protection_scope="《民法典》第585条提供约定违约金或赔偿额明显偏离损失时的调整救济，但维修费用是否必要、合理、实际发生仍需证据证明。",
            exceptions=["没有约定违约金或约定赔偿额", "维修事实、原因和金额仍需由主张方举证", "法院或仲裁机构结合个案裁量"],
            overrideable=False,
            confidence="high",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["liquidated_damages_adjustment_remedy"],
        ),
        "force_majeure": DefaultRule(
            rule_id="LEASE-DEFAULT-FORCE-MAJEURE",
            domain="house_lease",
            proposition="不可抗力导致合同目的不能实现或影响履行时，可适用法定解除、免责或责任减轻规则。",
            proposition_id="lease_force_majeure_statutory_relief",
            applicability_conditions=["房屋租赁合同", "发生不可抗力", "不可抗力影响房屋使用或合同履行"],
            authority_ids=["CN-CC-563", "CN-CIVIL-CODE-590"],
            protection_scope="《民法典》第563条、第590条提供不可抗力导致合同目的不能实现时的解除及责任减免规则。",
            exceptions=["不可抗力与不能履行无因果关系", "迟延履行后发生不可抗力", "通知、证明、租金结算等操作事项仍需事实证明"],
            overrideable=False,
            confidence="high",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["force_majeure_statutory_relief"],
        ),
        "changed_circumstances": DefaultRule(
            rule_id="LEASE-DEFAULT-CHANGE-OF-CIRCUMSTANCES",
            domain="house_lease",
            proposition="合同基础条件发生订约时无法预见且非商业风险的重大变化，继续履行明显不公平的，受不利影响方可以重新协商；合理期限内协商不成，可请求法院或仲裁机构变更或解除合同。",
            proposition_id="lease_change_of_circumstances_judicial_relief",
            applicability_conditions=["房屋租赁合同", "合同基础条件发生重大变化", "继续履行明显不公平"],
            authority_ids=["CN-CIVIL-CODE-533"],
            protection_scope="《民法典》第533条提供情势变更时重新协商，以及合理期限内协商不成时请求人民法院或仲裁机构变更、解除合同的法定救济；合同仍可明确协商流程、通知方式及期限。",
            exceptions=["属于正常商业风险", "变化可预见或已由合同分配", "需结合个案事实及司法裁量"],
            overrideable=False,
            confidence="high",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["core_contract_arrangement"],
        ),
        "pre_delivery_defect": DefaultRule(
            rule_id="LEASE-DEFAULT-FITNESS-AND-REPAIR",
            domain="house_lease",
            proposition="出租人应按约交付租赁物并在租赁期限内保持租赁物符合约定用途，承租人可要求维修或依法处理。",
            proposition_id="lease_fitness_repair_default",
            applicability_conditions=["房屋租赁合同", "交付前或租期内存在影响使用的瑕疵"],
            authority_ids=["CN-CIVIL-CODE-708", "CN-CIVIL-CODE-713"],
            protection_scope="《民法典》第708条、第713条提供出租人适租交付和维修义务的基础规则。",
            exceptions=["瑕疵由承租人造成", "双方依法另有有效约定", "瑕疵披露、交接记录和减租结算仍需合同或证据明确"],
            overrideable=True,
            confidence="high",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["lessor_fitness_and_repair_obligation"],
        ),
        "third_party_tort": DefaultRule(
            rule_id="LEASE-DEFAULT-THIRD-PARTY-TORT-REMEDY",
            domain="house_lease",
            proposition="第三人侵害租赁物或影响使用时，受损方可依据侵权责任规则向责任方主张权利。",
            proposition_id="lease_third_party_tort_remedy",
            applicability_conditions=["房屋租赁合同", "第三方行为影响房屋使用或造成损坏"],
            authority_ids=["CN-CIVIL-CODE-1165"],
            protection_scope="侵权责任法定规则提供向实际责任第三方追责的基础救济。",
            exceptions=["第三方责任主体、过错、因果关系和损失范围需另行证明", "出租人与承租人之间的协助、押金和减租流程仍需合同明确"],
            overrideable=False,
            confidence="medium",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["third_party_tort_remedy"],
        ),
        "third_party_defect": DefaultRule(
            rule_id="LEASE-DEFAULT-THIRD-PARTY-USE-IMPAIRMENT",
            domain="house_lease",
            proposition="第三方原因影响房屋正常使用时，可结合出租人适租义务、维修义务及侵权责任规则处理。",
            proposition_id="lease_third_party_use_impairment_relief",
            applicability_conditions=["房屋租赁合同", "第三方原因影响房屋使用"],
            authority_ids=["CN-CIVIL-CODE-708", "CN-CIVIL-CODE-713", "CN-CIVIL-CODE-1165"],
            protection_scope="《民法典》第708条、第713条及侵权责任规则提供适租、维修和向责任第三方追责的基础救济。",
            exceptions=["影响程度、减租比例、报修协助和追偿证据仍需事实证明或合同细化"],
            overrideable=True,
            confidence="medium",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["third_party_use_impairment_relief"],
        ),
        "housing_safety_emergency": DefaultRule(
            rule_id="LEASE-DEFAULT-SAFETY-USE-RELIEF",
            domain="house_lease",
            proposition="租赁房屋不符合约定用途或存在严重安全风险时，承租人可结合出租人维修义务和法定解除规则获得救济。",
            proposition_id="lease_safety_risk_statutory_relief",
            applicability_conditions=["房屋租赁合同", "房屋存在严重安全隐患或无法正常使用"],
            authority_ids=["CN-CIVIL-CODE-708", "CN-CIVIL-CODE-713", "CN-CC-563"],
            protection_scope="《民法典》第708条、第713条、第563条提供适租维修和合同目的不能实现时解除的基础规则。",
            exceptions=["安全风险、影响程度、搬离费用和结算节点仍需证据及合同流程明确"],
            overrideable=True,
            confidence="medium",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["safety_risk_statutory_relief"],
        ),
        "property_damage_deposit_evidence": DefaultRule(
            rule_id="LEASE-DEFAULT-DAMAGE-DEPOSIT-EVIDENCE",
            domain="house_lease",
            proposition="承租人应妥善保管租赁物，按约定或租赁物性质使用造成的正常损耗不承担赔偿；主张损坏扣款仍需证明损坏事实、原因和金额。",
            proposition_id="lease_damage_deposit_evidence_default",
            applicability_conditions=["房屋租赁合同", "存在房屋损坏或押金扣款争议"],
            authority_ids=["CN-CIVIL-CODE-710", "CN-CIVIL-CODE-714"],
            protection_scope="《民法典》第710条、第714条提供正常损耗排除和承租人保管责任的基础规则；损坏事实、原因和金额仍需证据证明。",
            exceptions=["交接清单、照片视频、维修单据和扣款顺序仍需合同或证据细化", "具体损坏原因和金额需个案证明"],
            overrideable=True,
            confidence="high",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["normal_wear_exclusion", "tenant_custody_liability"],
        ),
        "deposit_offset_order": DefaultRule(
            rule_id="LEASE-DEFAULT-DEPOSIT-OFFSET-ORDER",
            domain="house_lease",
            proposition="押金抵扣可参照债务履行、抵充顺序和诚实信用规则处理，但具体租金、代垫费用、维修费的业务顺序仍宜合同明确。",
            proposition_id="lease_deposit_offset_order_default",
            applicability_conditions=["房屋租赁合同", "存在多项费用需以押金抵扣"],
            authority_ids=["CN-CC-509", "CN-CC-561"],
            protection_scope="《民法典》第509条、第561条提供诚信履行和债务抵充的基础规则，可部分补足押金抵扣顺序争议。",
            exceptions=["押金担保范围、特定费用优先级和双方确认程序仍需合同细化"],
            overrideable=True,
            confidence="medium",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["deposit_offset_basic_order"],
        ),
        "deposit_return_timing": DefaultRule(
            rule_id="LEASE-DEFAULT-DEPOSIT-RETURN-TIMING",
            domain="house_lease",
            proposition="租赁期满承租人返还租赁物后，押金返还应结合费用结清、诚信履行和合同约定处理。",
            proposition_id="lease_deposit_return_timing_default",
            applicability_conditions=["房屋租赁合同", "租赁终止或期满", "承租人交还房屋并结清费用"],
            authority_ids=["CN-CC-509", "CN-CIVIL-CODE-733"],
            protection_scope="《民法典》第509条、第733条提供诚信履行和租赁物返还后的基础结算规则，但不自动给出具体返还天数。",
            exceptions=["具体返还期限、账户、扣款异议期仍需合同明确"],
            overrideable=True,
            confidence="medium",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["deposit_return_after_handover_basic_rule"],
        ),
        "handover_evidence": DefaultRule(
            rule_id="LEASE-DEFAULT-HANDOVER-RETURN-STATE",
            domain="house_lease",
            proposition="租赁期满承租人应返还租赁物，返还状态应符合约定或租赁物性质使用后的状态；双方仍应按诚信原则配合交接。",
            proposition_id="lease_handover_return_state_default",
            applicability_conditions=["房屋租赁合同", "租赁期满或终止", "承租人返还房屋"],
            authority_ids=["CN-CC-509", "CN-CIVIL-CODE-733"],
            protection_scope="《民法典》第509条、第733条提供诚信协作和返还状态的基础规则，但不自动生成钥匙、表读数、照片视频等交接证据清单。",
            exceptions=["交接清单、照片视频、表读数和设施状态仍需合同或实际留痕证明"],
            overrideable=True,
            confidence="medium",
            status="PARTIAL_DEFAULT",
            supplied_element_ids=["return_state_basic_rule"],
        ),
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

TECHNOLOGY_DOMAIN_PACK = DomainPack(
    contract_type="technology",
    version="domain-pack-technology-1.0",
    pack_id="technology/common",
    parent_pack_ids=["shared"],
    subject_matter="TECHNOLOGY",
    context_defaults={
        "contract_subtype": "GENERAL_TECHNOLOGY",
        "transaction_purpose": "technology_transaction",
        "usage_scenario": "GENERAL_TECHNOLOGY",
        "payment_structure": "technology_payment",
        "delivery_structure": "technology_delivery",
    },
)

PATENT_RIGHT_TRANSFER_DOMAIN_PACK = DomainPack(
    contract_type="technology",
    version="domain-pack-patent-right-transfer-1.0",
    pack_id="technology/transfer/patent_right",
    parent_pack_ids=["shared", "technology/common"],
    subject_matter="PATENT_RIGHT",
    context_defaults={
        "contract_subtype": "TECHNOLOGY_TRANSFER",
        "transaction_purpose": "patent_right_acquisition",
        "usage_scenario": "PATENT_RIGHT_TRANSFER",
        "payment_structure": "patent_transfer_installments",
        "delivery_structure": "patent_documents_and_registration",
    },
    default_law_nodes={
        "transfer_registration_or_recordal": "CLEAR_DEFAULT",
        "transfer_right_warranty": "CLEAR_DEFAULT",
        "license_infringement_responsibility": "CLEAR_DEFAULT",
        "patent_invalidity_allocation": "PARTIAL_DEFAULT",
        "existing_license_succession": "PARTIAL_DEFAULT",
    },
    default_law_rules={
        "license_infringement_responsibility": DefaultRule(
            rule_id="TECH-DEFAULT-INFRINGEMENT-ALLOCATION",
            domain="technology/transfer/patent_right",
            proposition="受让人按照约定实施专利侵害他人合法权益的，原则上由让与人承担责任。",
            applicability_conditions=["专利权转让", "受让人按约实施", "第三方权利主张"],
            authority_ids=["PRC-CIVIL-CODE-874"],
            protection_scope="提供按约实施时的基础责任分配，不覆盖受让人超范围实施或擅自变更造成的侵权。",
            exceptions=["受让人超范围实施", "当事人依法另有有效约定"],
            overrideable=True,
            confidence="high",
            status="CLEAR_DEFAULT",
        ),
    },
    economic_ratio_keys=[*SHARED_DOMAIN_PACK.economic_ratio_keys, "prepayment_ratio", "transfer_price_ratio"],
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


LOAN_DOMAIN_PACK = DomainPack(
    contract_type="loan", version="domain-pack-loan-1.0", pack_id="loan/common",
    default_law_nodes={"loan_repayment_offset_order": "CLEAR_DEFAULT"},
    default_law_rules={
        "loan_repayment_offset_order": DefaultRule(
            rule_id="loan-default-offset-order", domain="loan",
            proposition="债务人给付不足且无另行约定时，按实现债权费用、利息、主债务的顺序抵充。",
            applicability_conditions=["给付不足以清偿全部债务", "当事人未另行约定抵充顺序"],
            authority_ids=["CN-CC-561"],
            protection_scope="法定抵充顺序补充合同未约定的顺序，无须将该默认顺序重复写入合同。",
            exceptions=["当事人另有有效约定"], overrideable=True, confidence="high",
            status="CLEAR_DEFAULT", proposition_id="loan.default.offset_order",
            supplied_element_ids=["loan_offset_order"],
        ),
    },
)


DOMAIN_PACKS: Dict[str, DomainPack] = {
    "shared": SHARED_DOMAIN_PACK,
    "loan": LOAN_DOMAIN_PACK,
    "loan/common": LOAN_DOMAIN_PACK,
    "sale": SALE_DOMAIN_PACK,
    "house_lease": HOUSE_LEASE_DOMAIN_PACK,
    "lease": HOUSE_LEASE_DOMAIN_PACK,
    "service": SERVICE_DOMAIN_PACK,
    "technology": TECHNOLOGY_DOMAIN_PACK,
    "technology/common": TECHNOLOGY_DOMAIN_PACK,
    "technology/transfer/patent_right": PATENT_RIGHT_TRANSFER_DOMAIN_PACK,
    "sale/common": SALE_COMMON_DOMAIN_PACK,
    "sale/goods/general": SALE_GOODS_GENERAL_DOMAIN_PACK,
    "sale/goods/equipment": SALE_GOODS_EQUIPMENT_DOMAIN_PACK,
    "sale/goods/framework_supply": SALE_GOODS_FRAMEWORK_SUPPLY_DOMAIN_PACK,
    "sale/real_estate/common": SALE_REAL_ESTATE_COMMON_DOMAIN_PACK,
    "sale/real_estate/residential_secondary": SALE_RESIDENTIAL_SECONDARY_DOMAIN_PACK,
}


from review_v2.priority_contract_types import PRIORITY_TYPES

for _type_key, _type_meta in PRIORITY_TYPES.items():
    DOMAIN_PACKS.setdefault(_type_meta.family.lower(), DomainPack(
        contract_type=_type_meta.family.lower(), version="priority-domain-1.0", pack_id=_type_meta.family.lower(), parent_pack_ids=["shared"]))
    DOMAIN_PACKS[_type_key] = DomainPack(
        contract_type=_type_key, version="priority-domain-1.0", pack_id=_type_key,
        parent_pack_ids=["shared", _type_meta.family.lower()], subject_matter=_type_meta.subject,
        context_defaults={"contract_subtype": _type_key.upper(), "usage_scenario": _type_meta.name,
                          "transaction_purpose": _type_key},
    )


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
