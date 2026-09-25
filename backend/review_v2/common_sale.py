"""Shared sale-review context, product applicability, and satisfaction paths."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Sequence

from review_v2.clause_parser import ParsedClause


@dataclass(frozen=True)
class SatisfactionPath:
    path_id: str
    applicable_when: Dict[str, Any]
    required_elements: List[str]
    optional_elements: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CoverageRequirement:
    review_id: str
    satisfaction_paths: List[SatisfactionPath]

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "satisfaction_paths": [path.to_public_dict() for path in self.satisfaction_paths],
        }


@dataclass(frozen=True)
class ProductDocumentationProfile:
    product_category: str
    complexity: str
    installation_required: bool
    operation_required: bool
    maintenance_required: bool
    regulated_document_required: bool
    requires_user_manual: bool
    requires_operation_manual: bool
    requires_maintenance_manual: bool
    requires_warranty_card: bool
    requires_certificate_of_conformity: bool
    requires_test_report: bool
    requires_regulatory_certificate: bool
    positive_triggers: List[str]
    negative_triggers: List[str]
    source_clause_ids: List[str]
    source_reason: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewExecutionContext:
    contract_context: Dict[str, Any]
    domain_resolution: Dict[str, Any]
    transaction_structure: str
    product_context: Dict[str, Any]
    fact_graph_version: str
    claim_graph_version: str
    applicable_default_law: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


INSTALLATION_TRIGGERS = ("安装", "现场组装", "装配", "调试", "试运行")
OPERATION_TRIGGERS = ("操作", "运行", "开机", "控制系统", "用户界面", "软件许可", "操作培训")
MAINTENANCE_TRIGGERS = ("维护", "保养", "检修", "维修手册", "维护手册")
REGULATED_TRIGGERS = ("强制认证", "CCC", "行政许可", "特种设备", "医疗器械", "监管证书")
QUALITY_DOCUMENT_TRIGGERS = ("质量标准", "技术质量标准", "出厂检验", "检测报告", "合格证", "认证证书")


def _matched_terms(text: str, terms: Sequence[str]) -> List[str]:
    return [term for term in terms if term in text]


def build_product_documentation_profile(
    text: str,
    clauses: Sequence[ParsedClause],
    domain_resolution: Any,
) -> ProductDocumentationProfile:
    installation = _matched_terms(text, INSTALLATION_TRIGGERS)
    operation = _matched_terms(text, OPERATION_TRIGGERS)
    maintenance = _matched_terms(text, MAINTENANCE_TRIGGERS)
    regulated = _matched_terms(text, REGULATED_TRIGGERS)
    quality = _matched_terms(text, QUALITY_DOCUMENT_TRIGGERS)
    positive = list(dict.fromkeys(installation + operation + maintenance + regulated + quality))
    source_clause_ids = [
        clause.clause_id for clause in clauses
        if any(term in clause.text for term in positive)
    ]
    product_category = str(getattr(domain_resolution, "product_category", "UNKNOWN") or "UNKNOWN")
    complex_product = bool(installation or operation or maintenance)
    manual_required = complex_product
    quality_document_required = bool(quality or regulated or product_category in {"EQUIPMENT", "INDUSTRIAL_COMPONENTS"})
    negative = []
    if product_category == "INDUSTRIAL_COMPONENTS" and not complex_product:
        negative.append("ordinary_component_without_installation_operation_or_maintenance_trigger")
    reason = (
        "合同出现安装、操作或维护触发事实，产品使用资料具有实质必要性。"
        if manual_required else
        "未发现安装、独立操作或维护触发事实，保修卡和操作手册不作为当前产品的强制审查要求。"
    )
    return ProductDocumentationProfile(
        product_category=product_category,
        complexity="COMPLEX" if complex_product else "STANDARD",
        installation_required=bool(installation),
        operation_required=bool(operation),
        maintenance_required=bool(maintenance),
        regulated_document_required=bool(regulated),
        requires_user_manual=manual_required,
        requires_operation_manual=bool(operation or installation),
        requires_maintenance_manual=bool(maintenance),
        requires_warranty_card=manual_required and "质保" in text,
        requires_certificate_of_conformity=quality_document_required,
        requires_test_report=bool(regulated or "出厂检验" in text or "检测报告" in text),
        requires_regulatory_certificate=bool(regulated),
        positive_triggers=positive,
        negative_triggers=negative,
        source_clause_ids=list(dict.fromkeys(source_clause_ids)),
        source_reason=reason,
    )


def product_review_applicability(node_id: str, profile: ProductDocumentationProfile) -> Dict[str, Any] | None:
    if node_id == "sale_warranty_manual":
        applicable = any((
            profile.requires_user_manual,
            profile.requires_operation_manual,
            profile.requires_maintenance_manual,
            profile.requires_warranty_card,
        ))
        return {
            "applicable": applicable,
            "status": "APPLICABLE" if applicable else "NOT_APPLICABLE",
            "reason": profile.source_reason,
            "positive_triggers": profile.positive_triggers,
            "negative_triggers": profile.negative_triggers,
        }
    if node_id == "sale_inspection_report_certificate":
        applicable = any((
            profile.requires_certificate_of_conformity,
            profile.requires_test_report,
            profile.requires_regulatory_certificate,
        ))
        return {
            "applicable": applicable,
            "status": "APPLICABLE" if applicable else "NOT_APPLICABLE",
            "reason": (
                "产品质量、检测或监管触发事实要求提供至少一种可验证质量文件。"
                if applicable else
                "未发现质量文件或监管文件的实质适用触发事实。"
            ),
            "positive_triggers": profile.positive_triggers,
            "negative_triggers": profile.negative_triggers,
        }
    return None


def _claim_element(
    element_id: str, proposition: str, claim_id: str, *,
    legal_proposition_id: str = "", atomic: bool = True,
) -> Dict[str, Any]:
    return {
        "element_id": element_id,
        "proposition": proposition,
        "required_claim": claim_id,
        "terms": [],
        "atomic": atomic,
        "child_elements": [],
        "legal_proposition_ids": [legal_proposition_id] if legal_proposition_id else [],
    }


def common_sale_coverage_requirement(node_id: str, element_context=None) -> Dict[str, Any] | None:
    definitions: Dict[str, Dict[str, Any]] = {
        "common_termination_procedure": {
            "elements": [
                _claim_element("termination_trigger", "合同明确解除事由或触发条件。", "contract.termination.trigger"),
                _claim_element("notice_or_demand", "合同明确解除通知及送达机制。", "contract.termination.notice_or_demand"),
                _claim_element("cure_period", "合同明确违约后的补救期限。", "contract.termination.cure_period"),
                _claim_element("right_to_terminate", "合同明确条件满足后的解除权。", "contract.termination.right"),
                _claim_element("convenience_termination_notice", "长期合作可通过提前通知终止。", "contract.termination.convenience_notice"),
                _claim_element("settlement_after_termination", "合同明确终止或解除后的结算安排。", "contract.termination.settlement"),
                _claim_element("existing_order_effect", "合同明确终止后已确认订单继续履行。", "framework.confirmed_orders_survive"),
            ],
            "paths": [
                SatisfactionPath("MATERIAL_BREACH_CURE", {}, ["termination_trigger", "notice_or_demand", "cure_period", "right_to_terminate"]),
                SatisfactionPath("EXPRESS_TERMINATION_NOTICE", {}, ["termination_trigger", "notice_or_demand", "right_to_terminate"]),
                SatisfactionPath("FRAMEWORK_MASTER_TERMINATION", {"transaction_structure": "FRAMEWORK_SUPPLY"}, ["convenience_termination_notice", "existing_order_effect", "termination_trigger", "right_to_terminate"]),
            ],
        },
        "common_force_majeure": {
            "elements": [
                _claim_element("event_definition_or_scope", "合同明确不可抗力事件或适用范围。", "contract.force_majeure.event"),
                _claim_element("notice", "受影响方承担及时通知义务。", "contract.force_majeure.notice"),
                _claim_element("evidence", "受影响方承担证明义务。", "contract.force_majeure.evidence"),
                _claim_element("mitigation", "合同明确减损或调整履行措施。", "contract.force_majeure.mitigation"),
                _claim_element("suspension_or_extension", "合同明确延期、中止或延长履行。", "contract.force_majeure.suspension_or_extension"),
                _claim_element("prolonged_event_termination", "长期不可抗力导致目的不能实现时可以解除。", "contract.force_majeure.prolonged_termination"),
                _claim_element("payment_settlement", "合同明确不可抗力后的费用或已履行部分结算。", "contract.force_majeure.payment_settlement"),
            ],
            "paths": [
                SatisfactionPath("NOTICE_EVIDENCE_ADJUSTMENT", {}, ["event_definition_or_scope", "notice", "evidence", "mitigation", "prolonged_event_termination"], ["suspension_or_extension", "payment_settlement"]),
            ],
        },
        "sale_expectation_loss": {
            "elements": [
                _claim_element("lost_profit_recognized", "合同承认可依法主张可得利益损失。", "damages.lost_profit_recognized"),
                _claim_element("causation_requirement", "可得利益赔偿以违约因果关系为前提。", "damages.lost_profit_causation"),
                _claim_element(
                    "foreseeability_limit", "合同明确可预见性边界。",
                    "damages.lost_profit_foreseeability",
                    legal_proposition_id="legal.damages.foreseeability_limit",
                ),
                _claim_element(
                    "proof_or_evidentiary_requirement", "合同明确可得利益损失的证明与证据要求。",
                    "damages.lost_profit_proof_requirement",
                    legal_proposition_id="legal.damages.proof_requirement",
                ),
                _claim_element("exclusion_or_cap", "合同明确可得利益排除或责任上限。", "damages.lost_profit_exclusion_or_cap"),
                _claim_element("recovery_scope", "合同明确可得利益属于损失赔偿范围。", "damages.lost_profit_recovery_scope"),
            ],
            "paths": [
                SatisfactionPath(
                    "RECOGNITION_WITH_SCOPE", {},
                    ["lost_profit_recognized", "recovery_scope", "foreseeability_limit"],
                    ["proof_or_evidentiary_requirement", "causation_requirement", "exclusion_or_cap"],
                ),
            ],
        },
        "sale_packaging_requirement": {
            "elements": [
                _claim_element("packaging_method_or_standard", "合同明确包装方式或包装标准。", "goods.packaging_standard"),
            ],
            "optional": [
                _claim_element("documentation_requirement", "合同明确随货资料或产品文件。", "goods.documentation_delivery"),
                _claim_element("packaging_cost", "合同价格包含包装费用。", "goods.packaging_cost_included"),
            ],
            "paths": [SatisfactionPath("PACKAGING_STANDARD", {}, ["packaging_method_or_standard"], ["documentation_requirement", "packaging_cost"])],
        },
        "sale_risk_buyer_delay_acceptance": {
            "elements": [
                _claim_element("refusal_liability", "买方无正当理由拒绝受领时承担责任。", "goods.buyer_refusal_liability"),
                _claim_element("storage_cost", "迟延受领产生的合理仓储费用由买方承担。", "goods.delay_acceptance_storage_cost"),
                _claim_element("retransport_cost", "迟延受领产生的二次运输费用由买方承担。", "goods.delay_acceptance_retransport_cost"),
                _claim_element("insurance_cost", "迟延受领产生的合理保险费用由买方承担。", "goods.delay_acceptance_insurance_cost"),
                _claim_element("risk_transfer_on_delay", "买方迟延受领后货物风险转移。", "goods.delay_acceptance_risk_transfer"),
                _claim_element("preservation_duty", "卖方在迟延受领期间承担合理保管或保全义务。", "goods.delay_acceptance_preservation_duty"),
            ],
            "paths": [SatisfactionPath("DELAY_ACCEPTANCE_RISK", {}, ["refusal_liability", "risk_transfer_on_delay"], ["storage_cost", "retransport_cost", "insurance_cost", "preservation_duty"])],
        },
        "sale_ip_compliance": {
            "elements": [
                _claim_element("non_infringement_warranty", "出卖人作出不侵害第三方知识产权保证。", "goods.non_infringement_warranty"),
                _claim_element("third_party_claim_handling", "合同明确第三方权利主张的处理责任。", "goods.third_party_claim_handling"),
                _claim_element("indemnification", "合同明确侵害第三方权益后的赔偿责任。", "goods.infringement_indemnity"),
                _claim_element("right_to_use_embedded_software", "合同明确随附或嵌入软件的使用权。", "goods.embedded_software_right"),
                _claim_element("drawings_and_technical_material_rights", "合同明确图纸及技术资料权利。", "goods.technical_material_right"),
                _claim_element("trademark_or_brand_authorization", "合同明确商标或品牌授权。", "goods.brand_authorization"),
            ],
            "paths": [SatisfactionPath("NON_INFRINGEMENT_AND_REMEDY", {}, ["non_infringement_warranty", "third_party_claim_handling", "indemnification"], ["right_to_use_embedded_software", "drawings_and_technical_material_rights", "trademark_or_brand_authorization"])],
        },
        "sale_right_defect_no_third_party": {
            "elements": [
                _claim_element("third_party_rights_free", "出卖人保证标的物不存在第三方权利负担。", "goods.third_party_rights_free"),
                _claim_element("title_warranty", "出卖人保证有权处分且权属清晰。", "goods.title_warranty"),
            ],
            "paths": [SatisfactionPath("TITLE_WARRANTY", {}, ["third_party_rights_free"], ["title_warranty"])],
        },
        "sale_right_defect_notice": {
            "elements": [
                _claim_element("right_defect_disclosure", "出卖人承担权利瑕疵或第三方权利披露义务。", "goods.right_defect_disclosure"),
            ],
            "paths": [SatisfactionPath("RIGHT_DEFECT_DISCLOSURE", {}, ["right_defect_disclosure"])],
        },
        "sale_right_defect_remedy": {
            "elements": [
                _claim_element("third_party_claim_remedy", "合同明确第三方权利主张的处理或赔偿措施。", "goods.third_party_claim_remedy"),
            ],
            "paths": [SatisfactionPath("THIRD_PARTY_CLAIM_REMEDY", {}, ["third_party_claim_remedy"])],
        },
        "sale_inspection_report_certificate": {
            "elements": [
                _claim_element("certificate_of_conformity", "交付时提供产品合格证明。", "goods.certificate_of_conformity"),
                _claim_element("factory_test_report", "交付时提供出厂检验报告。", "goods.factory_test_report"),
                _claim_element("third_party_test_report", "交付时提供第三方检测报告。", "goods.third_party_test_report"),
                _claim_element("mandatory_certification", "受监管产品提供强制认证文件。", "goods.mandatory_certificate"),
            ],
            "paths": [
                SatisfactionPath("CONFORMITY_CERTIFICATE", {}, ["certificate_of_conformity"]),
                SatisfactionPath("FACTORY_TEST_REPORT", {}, ["factory_test_report"]),
                SatisfactionPath("REGULATED_PRODUCT", {"regulated_document_required": True}, ["mandatory_certification", "third_party_test_report"]),
            ],
        },
        "sale_warranty_manual": {
            "elements": [
                _claim_element("user_manual", "交付时提供使用说明书。", "goods.user_manual"),
                _claim_element("operation_manual", "交付时提供操作手册。", "goods.operation_manual"),
                _claim_element("maintenance_manual", "交付时提供维护手册。", "goods.maintenance_manual"),
                _claim_element("warranty_card", "交付时提供保修卡。", "goods.warranty_card"),
            ],
            "paths": [SatisfactionPath("MATERIAL_PRODUCT_DOCUMENTATION", {}, ["user_manual"], ["operation_manual", "maintenance_manual", "warranty_card"])],
        },
    }
    definition = definitions.get(node_id)
    if not definition:
        return None
    if node_id == "common_termination_procedure" and element_context is not None:
        prerequisites = {"convenience_termination_notice": "ongoing_transaction",
                         "existing_order_effect": "ongoing_transaction",
                         "cure_period": "cure_based_termination"}
        excluded = {key for key, condition in prerequisites.items() if not element_context.get(condition)}
        definition["elements"] = [e for e in definition["elements"] if e["element_id"] not in excluded]
        # Disabled conditional elements must not remain in an alternative path
        # as implicit MISSING requirements, or make a disabled path vacuously pass.
        definition["paths"] = [p for p in definition["paths"]
                               if not set(p.required_elements).intersection(excluded)]
    return {
        "review_id": node_id,
        "required_elements": definition["elements"],
        "optional_elements": definition.get("optional", []),
        "satisfaction_paths": [path.to_public_dict() for path in definition.get("paths", [])],
    }
