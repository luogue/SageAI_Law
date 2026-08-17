"""Single source of truth for the reviewed party's perspective."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


PERSPECTIVE_RESOLVER_VERSION = "perspective-resolver-6.7-freeze-1.0"

ROLE_COMPATIBILITY = {
    "SALE": ("BUYER", "SELLER"),
    "HOUSE_LEASE": ("LESSOR", "LESSEE"),
    "LEASE": ("LESSOR", "LESSEE"),
    "SERVICE": ("SERVICE_PROVIDER", "SERVICE_RECIPIENT"),
}

DISPLAY_ROLES = {
    "BUYER": "买方 / 需方",
    "SELLER": "卖方 / 供方",
    "LESSOR": "出租人",
    "LESSEE": "承租人",
    "SERVICE_PROVIDER": "服务提供方",
    "SERVICE_RECIPIENT": "服务接受方",
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
    domain_role: str
    canonical_role: str
    display_role: str
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
    )
    for terms, role in mapping:
        if any(term in value for term in terms):
            rows.append(role)
    return list(dict.fromkeys(rows))


def resolve_perspective(requested_role: str, contract_family: str, previous_context_role: str = "") -> PerspectiveResolution:
    family = (contract_family or "").upper()
    compatible = ROLE_COMPATIBILITY.get(family, ("OTHER",))
    candidates = _candidate_roles(requested_role)
    previous = (_candidate_roles(previous_context_role) or [previous_context_role.upper() if previous_context_role else ""])[0]
    accepted = next((role for role in candidates if role in compatible), "")
    if not accepted:
        accepted = compatible[0] if compatible else "OTHER"
    rejected = [role for role in candidates if role != accepted]
    if previous and previous not in compatible and previous not in rejected:
        rejected.append(previous)
    confidence = "high" if accepted in compatible else "low"
    reasons = [f"Resolved domain family permits roles: {', '.join(compatible)}."]
    if rejected:
        reasons.append(f"Rejected incompatible carried roles: {', '.join(rejected)}.")
    reasons.append("The renderer consumes only canonical_role and never merges profile labels.")
    return PerspectiveResolution(
        requested_role=requested_role,
        previous_context_role=previous_context_role,
        contract_family=family,
        domain_role=accepted,
        canonical_role=accepted,
        display_role=DISPLAY_ROLES.get(accepted, DISPLAY_ROLES["OTHER"]),
        candidate_roles=candidates,
        rejected_roles=rejected,
        confidence=confidence,
        reasons=reasons,
    )


def perspective_domain_consistency_gate(resolution: PerspectiveResolution) -> Dict[str, Any]:
    compatible = ROLE_COMPATIBILITY.get(resolution.contract_family, ("OTHER",))
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
