"""Single source of truth for the reviewed party's perspective."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List


PERSPECTIVE_RESOLVER_VERSION = "perspective-resolver-6.7-freeze-1.3"

ROLE_COMPATIBILITY = {
    "WORK_CONTRACT": ("WORK_CUSTOMER", "WORK_CONTRACTOR"),
    "TRANSPORTATION": ("CONSIGNOR", "CARRIER", "CONSIGNEE"),
    "GIFT": ("DONOR", "DONEE"),
    "DEPOSIT": ("DEPOSITOR", "CUSTODIAN"),
    "AGENCY": ("PRINCIPAL", "AGENT"),
    "LOAN": ("BORROWER", "LENDER"),
    "GUARANTEE": ("GUARANTOR", "CREDITOR"),
    "FINANCE_LEASE": ("LESSEE", "LESSOR"),
    "WAREHOUSE": ("WAREHOUSE_DEPOSITOR", "CUSTODIAN"),
    "CONSTRUCTION": ("EMPLOYER", "CONTRACTOR"),
    "COMMISSION_AGENCY": ("PRINCIPAL", "COMMISSION_AGENT"),
    "UTILITY_SUPPLY": ("UTILITY_USER", "UTILITY_SUPPLIER"),
    "BROKERAGE": ("PRINCIPAL", "BROKER"),
    "EMPLOYMENT": ("EMPLOYMENT_PARTY", "LABOR_EMPLOYER", "WORKER", "INFORMATION_DISCLOSER", "INFORMATION_RECIPIENT"),
    "SECURITY_PROPERTY": ("SECURITY_PARTY", "SECURITY_PROVIDER", "SECURED_CREDITOR"),
    "EQUITY_INVESTMENT": ("EQUITY_PARTY", "INVESTOR", "EQUITY_TRANSFEROR", "EQUITY_TRANSFEREE", "SHAREHOLDER", "TARGET_COMPANY"),
    "SALE": ("BUYER", "SELLER"),
    "HOUSE_LEASE": ("LESSOR", "LESSEE"),
    "LEASE": ("LESSOR", "LESSEE"),
    "SERVICE": ("SERVICE_PROVIDER", "SERVICE_RECIPIENT"),
    "TECHNOLOGY": (
        "PATENT_TRANSFEREE", "PATENT_TRANSFEROR", "PATENT_LICENSEE", "PATENT_LICENSOR",
        "SERVICE_PROVIDER", "SERVICE_RECIPIENT", "COOPERATIVE_DEVELOPER",
        "CONSULTING_CLIENT", "TECHNICAL_CONSULTANT",
    ),
}

DISPLAY_ROLES = {
    "WORK_CUSTOMER": "定作方", "WORK_CONTRACTOR": "承揽方",
    "CONSIGNOR": "托运人", "CARRIER": "承运人", "CONSIGNEE": "收货人",
    "DONOR": "赠与人", "DONEE": "受赠人", "DEPOSITOR": "寄存人", "CUSTODIAN": "保管人",
    "PRINCIPAL": "委托人", "AGENT": "受托人", "BORROWER": "借款人", "LENDER": "贷款人",
    "GUARANTOR": "保证人", "CREDITOR": "债权人", "WAREHOUSE_DEPOSITOR": "存货人",
    "COMMISSION_AGENT": "行纪人", "UTILITY_USER": "用能人", "UTILITY_SUPPLIER": "供能人",
    "BROKER": "中介人",
    "EMPLOYMENT_PARTY": "协议当事人",
    "LABOR_EMPLOYER": "用人单位",
    "WORKER": "劳动者",
    "INFORMATION_DISCLOSER": "信息披露方",
    "INFORMATION_RECIPIENT": "信息接收方",
    "SECURITY_PARTY": "担保合同当事人",
    "SECURITY_PROVIDER": "抵押人 / 出质人",
    "SECURED_CREDITOR": "抵押权人 / 质权人",
    "EQUITY_PARTY": "股权协议当事人",
    "INVESTOR": "投资方",
    "EQUITY_TRANSFEROR": "股权转让方",
    "EQUITY_TRANSFEREE": "股权受让方",
    "SHAREHOLDER": "股东",
    "TARGET_COMPANY": "目标公司",
    "BUYER": "买方 / 需方",
    "SELLER": "卖方 / 供方",
    "LESSOR": "出租人",
    "LESSEE": "承租人",
    "SERVICE_PROVIDER": "服务提供方",
    "SERVICE_RECIPIENT": "服务接受方",
    "PATENT_TRANSFEREE": "专利权受让方",
    "PATENT_TRANSFEROR": "专利权让与方",
    "PATENT_LICENSEE": "被许可方 / 付款方",
    "PATENT_LICENSOR": "许可方",
    "COOPERATIVE_DEVELOPER": "合作开发方",
    "COMMISSIONING_PARTY": "委托方",
    "DEVELOPMENT_CONTRACTOR": "开发方",
    "ENTRUSTED_DEVELOPMENT_PARTY": "委托开发合同当事人",
    "CONSULTING_CLIENT": "委托方",
    "TECHNICAL_CONSULTANT": "受托方",
    "EMPLOYER": "发包人",
    "CONTRACTOR": "承包人",
    "OTHER": "合同当事人",
    "UNCERTAIN": "待确认",
}


@dataclass(frozen=True)
class PerspectiveResolution:
    requested_role: str
    previous_context_role: str
    contract_family: str
    contract_subtype: str
    party_side: str
    review_party_identity: str
    review_party_label: str
    domain_role: str
    transaction_role: str
    canonical_role: str
    display_role: str
    transaction_type: str
    review_party: str
    legal_role: str
    contract_display_role: str
    candidate_roles: List[str]
    rejected_roles: List[str]
    confidence: str
    reasons: List[str]

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _candidate_roles(identity: str) -> List[str]:
    value = (identity or "").upper()
    rows: List[str] = []
    mapping = (
        (("BUYER", "买方", "买受人", "需方"), "BUYER"),
        (("SELLER", "卖方", "出卖人", "供方"), "SELLER"),
        (("LESSEE", "TENANT", "租客", "承租人"), "LESSEE"),
        (("LESSOR", "LANDLORD", "房东", "出租人"), "LESSOR"),
        (("SERVICE_PROVIDER", "服务提供方"), "SERVICE_PROVIDER"),
        (("SERVICE_RECIPIENT", "服务接受方"), "SERVICE_RECIPIENT"),
        (("PATENT_TRANSFEREE", "专利权受让方", "受让方"), "PATENT_TRANSFEREE"),
        (("PATENT_TRANSFEROR", "专利权让与方", "让与方", "让与人"), "PATENT_TRANSFEROR"),
        (("PATENT_LICENSEE", "被许可方"), "PATENT_LICENSEE"),
        (("PATENT_LICENSOR", "许可方"), "PATENT_LICENSOR"),
        (("COOPERATIVE_DEVELOPER", "合作开发方"), "COOPERATIVE_DEVELOPER"),
        (("CONSULTING_CLIENT", "技术咨询委托方", "咨询委托方"), "CONSULTING_CLIENT"),
        (("TECHNICAL_CONSULTANT", "技术咨询受托方", "咨询受托方"), "TECHNICAL_CONSULTANT"),
        (("COMMISSIONING_PARTY", "委托方", "委托人"), "COMMISSIONING_PARTY"),
        (("DEVELOPMENT_CONTRACTOR", "开发方", "研究开发方", "研究开发人"), "DEVELOPMENT_CONTRACTOR"),
    )
    for terms, role in mapping:
        if any(term in value for term in terms):
            rows.append(role)
    return list(dict.fromkeys(rows))


def _technology_subtype_roles(contract_subtype: str) -> tuple[str, ...]:
    subtype = (contract_subtype or "").upper()
    if subtype == "COOPERATIVE_DEVELOPMENT":
        return ("COOPERATIVE_DEVELOPER",)
    if subtype == "ENTRUSTED_DEVELOPMENT":
        return ("COMMISSIONING_PARTY", "DEVELOPMENT_CONTRACTOR", "ENTRUSTED_DEVELOPMENT_PARTY")
    if subtype in {"PATENT_RIGHT_TRANSFER", "PATENT_APPLICATION_RIGHT_TRANSFER"}:
        return ("PATENT_TRANSFEREE", "PATENT_TRANSFEROR")
    if subtype in {"PATENT_LICENSE", "TECHNOLOGY_LICENSE", "TECHNICAL_SECRET_LICENSE"}:
        return ("PATENT_LICENSEE", "PATENT_LICENSOR")
    if subtype in {"TECHNICAL_SERVICE", "TECHNOLOGY_SERVICE"}:
        return ("SERVICE_PROVIDER", "SERVICE_RECIPIENT")
    if subtype == "TECHNICAL_CONSULTING":
        return ("CONSULTING_CLIENT", "TECHNICAL_CONSULTANT")
    return ROLE_COMPATIBILITY["TECHNOLOGY"]


def _legal_role(canonical_role: str) -> str:
    return {
        "PATENT_LICENSEE": "LICENSEE",
        "PATENT_LICENSOR": "LICENSOR",
        "PATENT_TRANSFEREE": "TRANSFEREE",
        "PATENT_TRANSFEROR": "TRANSFEROR",
    }.get(canonical_role, canonical_role)


def _transaction_type(contract_family: str, contract_subtype: str) -> str:
    subtype = (contract_subtype or "").upper()
    if subtype in {"PATENT_LICENSE", "TECHNOLOGY_LICENSE", "TECHNICAL_SECRET_LICENSE"}:
        return "TECHNOLOGY_LICENSE"
    if subtype in {"PATENT_RIGHT_TRANSFER", "PATENT_APPLICATION_RIGHT_TRANSFER", "TECHNOLOGY_TRANSFER", "TECHNICAL_SECRET_TRANSFER"}:
        return "TECHNOLOGY_TRANSFER"
    return subtype or (contract_family or "OTHER").upper()


def _license_contract_display_role(requested_role: str, canonical_role: str) -> str:
    value = requested_role or ""
    if canonical_role == "PATENT_LICENSEE":
        if "受让方" in value and "被许可方" not in value:
            return "受让方（被许可方）"
        return "被许可方"
    if canonical_role == "PATENT_LICENSOR":
        if "出让方" in value and "许可方" not in value:
            return "出让方（许可方）"
        return "许可方"
    return DISPLAY_ROLES.get(canonical_role, DISPLAY_ROLES["OTHER"])


def _requested_party_side(requested_role: str) -> str:
    value = (requested_role or "").upper()
    if "甲方" in value or "PARTY_A" in value:
        return "PARTY_A"
    if "乙方" in value or "PARTY_B" in value:
        return "PARTY_B"
    return "UNKNOWN"


def _contract_defined_role(contract_text: str, party_side: str, contract_subtype: str) -> tuple[str, str]:
    """Resolve the legal role from an explicit Party A/B definition.

    Party letters are drafting labels, not stable transaction roles.  This
    resolver intentionally reads only the short role label next to the party
    definition (for example ``甲方（服务提供方）``); it does not infer a role
    from which party happens to perform an obligation elsewhere in the text.
    """
    party = "甲方" if party_side == "PARTY_A" else "乙方" if party_side == "PARTY_B" else ""
    if not party or not contract_text:
        return "", ""
    labels = [
        re.sub(r"\s+", "", match.group("label"))
        for match in re.finditer(
            rf"{party}\s*[（(]\s*(?P<label>[^）)\n：:]{{1,24}})\s*[）)]",
            contract_text,
        )
    ]
    if not labels:
        return "", ""
    label = labels[0]
    subtype = (contract_subtype or "").upper()
    mappings: tuple[tuple[tuple[str, ...], str], ...]
    if subtype in {"TECHNICAL_SERVICE", "TECHNOLOGY_SERVICE"}:
        mappings = (
            (("服务提供方", "技术服务提供方", "服务方"), "SERVICE_PROVIDER"),
            (("服务接受方", "服务接收方", "客户", "委托方"), "SERVICE_RECIPIENT"),
        )
    elif subtype == "TECHNICAL_CONSULTING":
        mappings = (
            (("咨询方", "技术咨询方", "受托方"), "TECHNICAL_CONSULTANT"),
            (("委托方", "咨询委托方"), "CONSULTING_CLIENT"),
        )
    elif subtype == "ENTRUSTED_DEVELOPMENT":
        mappings = (
            (("开发方", "研究开发方", "研究开发人"), "DEVELOPMENT_CONTRACTOR"),
            (("委托方", "委托人"), "COMMISSIONING_PARTY"),
        )
    elif subtype in {"PATENT_LICENSE", "TECHNOLOGY_LICENSE", "TECHNICAL_SECRET_LICENSE"}:
        mappings = (
            (("许可方", "出让方"), "PATENT_LICENSOR"),
            (("被许可方", "受让方"), "PATENT_LICENSEE"),
        )
    elif subtype in {"PATENT_RIGHT_TRANSFER", "PATENT_APPLICATION_RIGHT_TRANSFER", "TECHNOLOGY_TRANSFER", "TECHNICAL_SECRET_TRANSFER"}:
        mappings = (
            (("转让方", "让与方", "让与人"), "PATENT_TRANSFEROR"),
            (("受让方", "受让人"), "PATENT_TRANSFEREE"),
        )
    else:
        mappings = tuple()
    # A longer declared role (e.g. 被许可方) cannot match its suffix 许可方.
    mappings = tuple(sorted(mappings, key=lambda row: max(map(len, row[0])), reverse=True))
    for aliases, role in mappings:
        if any(alias in label for alias in aliases):
            return role, label
    return "", label


def _compatible_roles(contract_family: str, contract_subtype: str) -> tuple[str, ...]:
    family = (contract_family or "").upper()
    if family == "TECHNOLOGY":
        return (*_technology_subtype_roles(contract_subtype), "OTHER")
    return tuple(dict.fromkeys((*ROLE_COMPATIBILITY.get(family, ()), "OTHER")))


def resolve_perspective(
    requested_role: str,
    contract_family: str,
    previous_context_role: str = "",
    contract_subtype: str = "",
    contract_text: str = "",
) -> PerspectiveResolution:
    family = (contract_family or "").upper()
    subtype = (contract_subtype or "").upper()
    compatible = _compatible_roles(family, subtype)
    candidates = _candidate_roles(requested_role)
    # Exact catalog roles and their party-qualified labels are valid only in
    # the resolved family. Do not silently discard work/transport roles.
    candidates = [role for role in compatible if DISPLAY_ROLES.get(role, "\0") in requested_role] + candidates
    if family in {"EMPLOYMENT", "SECURITY_PROPERTY", "EQUITY_INVESTMENT"}:
        specific_aliases = {
            "LABOR_EMPLOYER": ("用人单位", "雇主"), "WORKER": ("劳动者", "员工"),
            "INFORMATION_DISCLOSER": ("披露方",), "INFORMATION_RECIPIENT": ("接收方",),
            "SECURED_CREDITOR": ("抵押权人", "质权人", "债权人"), "SECURITY_PROVIDER": ("抵押人", "出质人"),
            "INVESTOR": ("投资方",), "EQUITY_TRANSFEROR": ("转让方",), "EQUITY_TRANSFEREE": ("受让方",),
            "SHAREHOLDER": ("股东",), "TARGET_COMPANY": ("目标公司", "融资方", "公司"),
        }
        candidates = [role for role, aliases in specific_aliases.items() if role in compatible and
                      (role in requested_role.upper() or any(alias in requested_role for alias in aliases))] + candidates
    party_side = _requested_party_side(requested_role)
    contract_defined_role, contract_defined_label = _contract_defined_role(
        contract_text, party_side, subtype,
    )
    if family == "TECHNOLOGY" and subtype in {"PATENT_LICENSE", "TECHNOLOGY_LICENSE", "TECHNICAL_SECRET_LICENSE"}:
        # “受让方/出让方”是部分许可合同沿用的原始称谓，不代表专利权发生转移。
        # 在许可交易中先映射为许可法律角色，再保留原称谓用于展示。
        requested_value = requested_role or ""
        if "受让方" in requested_value and "专利权受让方" not in requested_value:
            candidates = ["PATENT_LICENSEE", *candidates]
        if "出让方" in requested_value and "专利权让与方" not in requested_value:
            candidates = ["PATENT_LICENSOR", *candidates]
        candidates = list(dict.fromkeys(candidates))
    previous = (_candidate_roles(previous_context_role) or [previous_context_role.upper() if previous_context_role else ""])[0]
    accepted = contract_defined_role if contract_defined_role in compatible else next(
        (role for role in candidates if role in compatible), ""
    )
    if not accepted and family == "TECHNOLOGY" and subtype == "COOPERATIVE_DEVELOPMENT":
        accepted = "COOPERATIVE_DEVELOPER"
    if not accepted and family == "TECHNOLOGY" and subtype == "ENTRUSTED_DEVELOPMENT":
        accepted = (
            "COMMISSIONING_PARTY" if party_side == "PARTY_A"
            else "DEVELOPMENT_CONTRACTOR" if party_side == "PARTY_B"
            else "ENTRUSTED_DEVELOPMENT_PARTY"
        )
    if not accepted and family == "TECHNOLOGY" and subtype == "TECHNICAL_CONSULTING":
        accepted = (
            "CONSULTING_CLIENT" if party_side == "PARTY_A"
            else "TECHNICAL_CONSULTANT" if party_side == "PARTY_B"
            else "CONSULTING_CLIENT"
        )
    if not accepted and family == "TECHNOLOGY" and subtype in {"TECHNICAL_SERVICE", "TECHNOLOGY_SERVICE"}:
        accepted = (
            "SERVICE_RECIPIENT" if party_side == "PARTY_A"
            else "SERVICE_PROVIDER" if party_side == "PARTY_B"
            else "SERVICE_PROVIDER"
        )
    if not accepted:
        accepted = compatible[0] if compatible else "OTHER"
    if requested_role == "合同当事人":
        accepted = "OTHER"
    rejected = [role for role in candidates if role != accepted]
    if previous and previous not in compatible and previous not in rejected:
        rejected.append(previous)
    confidence = "high" if accepted in compatible else "low"
    reasons = [f"Resolved {family}/{subtype or 'GENERAL'} permits roles: {', '.join(compatible)}."]
    if contract_defined_role:
        reasons.append(
            f"Explicit {party_side} contract definition '{contract_defined_label}' resolved to {contract_defined_role}."
        )
    if rejected:
        reasons.append(f"Rejected incompatible carried roles: {', '.join(rejected)}.")
    reasons.append("Party identity is retained separately from the canonical transaction role.")
    display_role = DISPLAY_ROLES.get(accepted, DISPLAY_ROLES["OTHER"])
    if accepted == "TARGET_COMPANY" and requested_role in {"融资方", "公司"}:
        display_role = requested_role
    elif family == "EQUITY_INVESTMENT" and requested_role in {"转让方", "受让方", "原股东"}:
        display_role = requested_role
    review_party_label = "甲方" if party_side == "PARTY_A" else "乙方" if party_side == "PARTY_B" else ""
    if accepted in {"PATENT_TRANSFEREE", "PATENT_TRANSFEROR"} and review_party_label:
        display_role = f"{review_party_label} / {DISPLAY_ROLES[accepted]}"
    elif accepted == "COOPERATIVE_DEVELOPER" and party_side in {"PARTY_A", "PARTY_B"}:
        display_role = f"{review_party_label} / 合作开发方"
    elif accepted in {"COMMISSIONING_PARTY", "DEVELOPMENT_CONTRACTOR"} and review_party_label:
        display_role = f"{review_party_label} / {DISPLAY_ROLES[accepted]}"
    elif accepted in {"CONSULTING_CLIENT", "TECHNICAL_CONSULTANT"} and review_party_label:
        display_role = f"{review_party_label} / {DISPLAY_ROLES[accepted]}"
    elif accepted in {"SERVICE_RECIPIENT", "SERVICE_PROVIDER"} and review_party_label:
        service_label = DISPLAY_ROLES[accepted]
        display_role = f"{review_party_label} / {service_label}"
    contract_display_role = DISPLAY_ROLES.get(accepted, DISPLAY_ROLES["OTHER"])
    if subtype == "PATENT_APPLICATION_RIGHT_TRANSFER" and accepted in {"PATENT_TRANSFEREE", "PATENT_TRANSFEROR"}:
        contract_display_role = "专利申请权受让方" if accepted == "PATENT_TRANSFEREE" else "专利申请权让与方"
        display_role = f"{review_party_label} / {contract_display_role}" if review_party_label else contract_display_role
    if subtype == "TECHNICAL_SECRET_TRANSFER" and accepted in {"PATENT_TRANSFEREE", "PATENT_TRANSFEROR"}:
        contract_display_role = "技术秘密受让方" if accepted == "PATENT_TRANSFEREE" else "技术秘密转让方"
        display_role = f"{review_party_label} / {contract_display_role}" if review_party_label else contract_display_role
    if accepted in {"PATENT_LICENSEE", "PATENT_LICENSOR"} and subtype in {
        "PATENT_LICENSE", "TECHNOLOGY_LICENSE", "TECHNICAL_SECRET_LICENSE",
    }:
        contract_display_role = _license_contract_display_role(requested_role, accepted)
        display_role = f"{review_party_label} / {contract_display_role}" if review_party_label else contract_display_role
    return PerspectiveResolution(
        requested_role=requested_role,
        previous_context_role=previous_context_role,
        contract_family=family,
        contract_subtype=subtype,
        party_side=party_side,
        review_party_identity=party_side,
        review_party_label=review_party_label,
        domain_role=accepted,
        transaction_role=accepted,
        canonical_role=accepted,
        display_role=display_role,
        transaction_type=_transaction_type(family, subtype),
        review_party=party_side,
        legal_role=_legal_role(accepted),
        contract_display_role=contract_display_role,
        candidate_roles=candidates,
        rejected_roles=rejected,
        confidence=confidence,
        reasons=reasons,
    )


def perspective_domain_consistency_gate(resolution: PerspectiveResolution) -> Dict[str, Any]:
    compatible = _compatible_roles(resolution.contract_family, resolution.contract_subtype)
    passed = resolution.canonical_role in compatible
    failures = [] if passed else [{
        "requirement": "PERSPECTIVE_DOMAIN_CONSISTENCY_GATE",
        "failure_stage": "Perspective Resolution",
        "root_cause": f"Role {resolution.canonical_role} is incompatible with {resolution.contract_family}.",
        "responsible_function": "resolve_perspective",
        "current_status": "FAIL",
    }]
    return {
        "status": "REPORT_READY" if passed else "BLOCKED",
        "failures": failures,
        "gate_results": {"PERSPECTIVE_DOMAIN_CONSISTENCY_GATE": "PASS" if passed else "FAIL"},
        "wrong_perspective_tokens": resolution.rejected_roles,
    }
