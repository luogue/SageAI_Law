"""Production display labels resolved from the classified contract domain."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class DomainDisplayLabel:
    family: str
    subject_matter: str
    transaction_structure: str
    subtype: str
    report_title: str
    usage_scenario_label: str
    contract_type_label: str


@dataclass(frozen=True)
class ReportContext:
    family: str
    subject_matter: str
    transaction_structure: str
    subtype: str
    product_category: str
    asset_usage: str
    perspective: str
    user_role: str
    contract_type_label: str
    scenario_label: str
    usage_scenario_label: str
    report_title: str

    def to_public_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["contract_family"] = self.family
        value["contract_subtype"] = self.subtype
        return value


DISPLAY_LABEL_REGISTRY: Tuple[DomainDisplayLabel, ...] = (
    DomainDisplayLabel(
        family="SALE",
        subject_matter="GOODS",
        transaction_structure="FRAMEWORK_SUPPLY",
        subtype="FRAMEWORK_SUPPLY",
        report_title="长期供货合同审查报告",
        usage_scenario_label="长期供货 / 框架采购",
        contract_type_label="长期供货合同",
    ),
    DomainDisplayLabel(
        family="SALE",
        subject_matter="REAL_ESTATE",
        transaction_structure="SINGLE_TRANSACTION",
        subtype="RESIDENTIAL_SECONDARY_REAL_ESTATE_SALE",
        report_title="住宅二手房地产买卖合同审查报告",
        usage_scenario_label="二手住宅房地产买卖",
        contract_type_label="住宅二手房地产买卖合同",
    ),
    DomainDisplayLabel(
        family="SALE",
        subject_matter="REAL_ESTATE",
        transaction_structure="SINGLE_TRANSACTION",
        subtype="COMMERCIAL_REAL_ESTATE_SALE",
        report_title="商业房地产买卖合同审查报告",
        usage_scenario_label="商业房地产买卖",
        contract_type_label="商业房地产买卖合同",
    ),
    DomainDisplayLabel(
        family="SALE",
        subject_matter="REAL_ESTATE",
        transaction_structure="SINGLE_TRANSACTION",
        subtype="REAL_ESTATE_SALE",
        report_title="房地产买卖合同审查报告",
        usage_scenario_label="房地产买卖",
        contract_type_label="房地产买卖合同",
    ),
    DomainDisplayLabel(
        family="SALE",
        subject_matter="EQUIPMENT",
        transaction_structure="SINGLE_TRANSACTION",
        subtype="EQUIPMENT_SALE",
        report_title="设备买卖合同审查报告",
        usage_scenario_label="设备买卖",
        contract_type_label="设备买卖合同",
    ),
    DomainDisplayLabel(
        family="SALE",
        subject_matter="GOODS",
        transaction_structure="SINGLE_TRANSACTION",
        subtype="GENERAL_GOODS_SALE",
        report_title="买卖合同审查报告",
        usage_scenario_label="商品买卖",
        contract_type_label="买卖合同",
    ),
    DomainDisplayLabel(
        family="LEASE",
        subject_matter="REAL_ESTATE",
        transaction_structure="SINGLE_TRANSACTION",
        subtype="RESIDENTIAL_LEASE",
        report_title="房屋租赁合同审查报告",
        usage_scenario_label="住宅租赁",
        contract_type_label="房屋租赁合同",
    ),
    DomainDisplayLabel(
        family="SERVICE",
        subject_matter="SERVICE",
        transaction_structure="SERVICE",
        subtype="GENERAL_SERVICE",
        report_title="服务合同审查报告",
        usage_scenario_label="一般服务合同",
        contract_type_label="服务合同",
    ),
    DomainDisplayLabel(
        family="TECHNOLOGY",
        subject_matter="TECHNICAL_SERVICE",
        transaction_structure="B2B_TECHNICAL_SERVICE",
        subtype="TECHNICAL_SERVICE",
        report_title="技术服务合同审查报告",
        usage_scenario_label="技术服务",
        contract_type_label="技术服务合同",
    ),
    DomainDisplayLabel(
        family="TECHNOLOGY",
        subject_matter="PATENT_RIGHT",
        transaction_structure="B2B_PATENT_RIGHT_TRANSFER",
        subtype="TECHNOLOGY_TRANSFER",
        report_title="专利权转让合同审查报告",
        usage_scenario_label="专利权转让",
        contract_type_label="技术合同—技术转让合同—专利权转让合同",
    ),
    DomainDisplayLabel(
        family="TECHNOLOGY",
        subject_matter="PATENT_LICENSE",
        transaction_structure="B2B_PATENT_LICENSE_WITH_COMMISSIONED_DEVELOPMENT",
        subtype="TECHNOLOGY_LICENSE",
        report_title="专利实施许可合同审查报告",
        usage_scenario_label="专利实施许可（含委托开发模块）",
        contract_type_label="技术合同—技术许可合同—专利实施许可（含委托开发模块）",
    ),
    DomainDisplayLabel(
        family="TECHNOLOGY",
        subject_matter="PATENT_LICENSE",
        transaction_structure="B2B_PATENT_LICENSE",
        subtype="TECHNOLOGY_LICENSE",
        report_title="专利实施许可合同审查报告",
        usage_scenario_label="专利实施许可",
        contract_type_label="技术合同—技术许可合同—专利实施许可",
    ),
    DomainDisplayLabel(
        family="TECHNOLOGY",
        subject_matter="TECHNOLOGY",
        transaction_structure="B2B_COOPERATIVE_DEVELOPMENT",
        subtype="COOPERATIVE_DEVELOPMENT",
        report_title="合作开发合同审查报告",
        usage_scenario_label="合作开发",
        contract_type_label="技术合同—技术开发合同—合作开发合同",
    ),
)


def _resolve_display_label(
    family: str,
    subject: str,
    transaction_structure: str,
    subtype: str,
) -> DomainDisplayLabel:
    # The registry order encodes the display priority: transaction structure,
    # subtype, subject, then family fallback.
    for label in DISPLAY_LABEL_REGISTRY:
        if (
            label.family == family
            and label.subject_matter == subject
            and label.transaction_structure == transaction_structure
            and label.subtype == subtype
        ):
            return label
    if transaction_structure == "FRAMEWORK_SUPPLY" and family == "SALE":
        return DISPLAY_LABEL_REGISTRY[0]
    if family == "SALE" and subject == "REAL_ESTATE":
        return DISPLAY_LABEL_REGISTRY[3]
    if family == "SALE" and (subject == "EQUIPMENT" or subtype == "EQUIPMENT_SALE"):
        return DISPLAY_LABEL_REGISTRY[4]
    if family == "SALE":
        return DISPLAY_LABEL_REGISTRY[5]
    if family in {"LEASE", "HOUSE_LEASE"}:
        return DISPLAY_LABEL_REGISTRY[6]
    if family == "SERVICE" or transaction_structure == "SERVICE":
        return DISPLAY_LABEL_REGISTRY[7]
    return DomainDisplayLabel(
        family=family,
        subject_matter=subject,
        transaction_structure=transaction_structure,
        subtype=subtype,
        report_title="合同审查报告",
        usage_scenario_label="一般合同",
        contract_type_label="合同",
    )


def build_report_context(contract_context: Dict[str, Any]) -> ReportContext:
    subtype = str(contract_context.get("contract_subtype") or "")
    subject = str(contract_context.get("subject_matter") or "")
    family = str(contract_context.get("contract_family") or contract_context.get("contract_type") or "").upper()
    transaction_structure = str(contract_context.get("transaction_structure") or "SINGLE_TRANSACTION")
    label = _resolve_display_label(family, subject, transaction_structure, subtype)
    if family == "TECHNOLOGY" and subtype == "TECHNICAL_SERVICE" and str(contract_context.get("usage_scenario") or "").startswith("UNIVERSITY_RESEARCH_DATA"):
        label = DomainDisplayLabel(
            family=family,
            subject_matter=subject,
            transaction_structure=transaction_structure,
            subtype=subtype,
            report_title="技术服务合同审查报告",
            usage_scenario_label="高校科研数据治理技术服务",
            contract_type_label="技术服务合同",
        )
    if family == "TECHNOLOGY" and subtype == "TECHNOLOGY_TRANSFER" and str(contract_context.get("usage_scenario") or "").startswith("UNIVERSITY_TECH_ACHIEVEMENT"):
        label = DomainDisplayLabel(
            family=family,
            subject_matter=subject,
            transaction_structure=transaction_structure,
            subtype=subtype,
            report_title="专利权转让合同审查报告",
            usage_scenario_label="高校科技成果向企业协议转让",
            contract_type_label="技术合同—技术转让合同—专利权转让合同",
        )
    user_role = str(contract_context.get("user_role") or contract_context.get("user_perspective") or "neutral")
    return ReportContext(
        family=family,
        subject_matter=subject,
        transaction_structure=transaction_structure,
        subtype=subtype,
        product_category=str(contract_context.get("product_category") or ""),
        asset_usage=str(contract_context.get("asset_usage") or ""),
        perspective=str(contract_context.get("user_perspective") or "neutral"),
        user_role=user_role,
        contract_type_label=label.contract_type_label,
        scenario_label=label.usage_scenario_label,
        usage_scenario_label=label.usage_scenario_label,
        report_title=label.report_title,
    )
