"""Reproduce regressions with this task's profile changes reverted in memory.

Preserves all pre-existing workspace edits. No source or database is modified.
"""
import inspect
import subprocess
import sys
import types
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(root / "backend"), str(root / "backend/tests")]
from review_v2 import engine, user_profile, perspective_resolution as perspective

old_profile = types.ModuleType("profile_before_fix")
sys.modules[old_profile.__name__] = old_profile
# user_profile.py had no pre-existing edits when this task started.
exec(subprocess.check_output(["git", "show", "HEAD:backend/review_v2/user_profile.py"], cwd=root).decode("utf-8"), old_profile.__dict__)
engine.UserRiskProfile = old_profile.UserRiskProfile

def old_scoped(profile, contract_type):
    source = profile.to_dict() if profile is not None else old_profile.UserRiskProfile.default().to_dict()
    normalized = dict(source)
    if contract_type == "sale" and normalized.get("contract_scenario") in {"", "居住用途", "投资/转租"}:
        normalized["contract_scenario"] = "商品买卖"
    elif contract_type in {"house_lease", "lease"} and not normalized.get("contract_scenario"):
        normalized["contract_scenario"] = "居住用途"
    return old_profile.UserRiskProfile.from_dict(normalized)
engine._request_scoped_profile = old_scoped

source = inspect.getsource(engine.review_contract_v2)
source = source.replace('    from review_v2.user_profile import normalize_profile\n    profile = normalize_profile(profile, type_meta.response_key, previous_type=user_selected_type)', '''    if profile is not None and resolved_type != user_selected_type and profile.contract_scenario == get_contract_meta(user_selected_type).display_name:
        profile = UserRiskProfile.from_dict({**profile.to_dict(), 'contract_scenario': type_meta.display_name})
    profile = _request_scoped_profile(profile, type_meta.response_key)''')
source = source.replace('    profile.user_identity = perspective_resolution.display_role\n', '')
start = source.index('    counterpart = {')
end = source.index('    if technology_classification:', start)
source = source[:start] + source[end:]
source = source.replace('    if (domain_resolution.contract_subtype not in {"GENERAL_CONTRACT", "RESIDENTIAL_LEASE"}\n            and profile.contract_scenario != report_context["scenario_label"]):', '    if profile.contract_scenario != report_context["scenario_label"]:')
exec(compile(source, '<profile-before-fix-engine>', 'exec'), engine.__dict__)

original_families = {"EMPLOYMENT", "SECURITY_PROPERTY", "EQUITY_INVESTMENT", "SALE", "HOUSE_LEASE", "LEASE", "SERVICE", "TECHNOLOGY"}
for family in list(perspective.ROLE_COMPATIBILITY):
    if family not in original_families:
        del perspective.ROLE_COMPATIBILITY[family]
def old_compatible(family, subtype):
    family = (family or '').upper()
    if family == 'TECHNOLOGY':
        return perspective._technology_subtype_roles(subtype)
    return perspective.ROLE_COMPATIBILITY.get(family, ('OTHER',))
perspective._compatible_roles = old_compatible
source = inspect.getsource(perspective.resolve_perspective)
source = source.replace('    candidates = [role for role in compatible if DISPLAY_ROLES.get(role, "\\0") in requested_role] + candidates\n', '')
source = source.replace('"TARGET_COMPANY": ("目标公司", "融资方", "公司"),', '"TARGET_COMPANY": ("目标公司",),')
source = source.replace('    if requested_role == "合同当事人":\n        accepted = "OTHER"\n', '')
start = source.index('    if accepted == "TARGET_COMPANY" and requested_role')
end = source.index('    review_party_label =', start)
source = source[:start] + source[end:]
exec(compile(source, '<profile-before-fix-perspective>', 'exec'), perspective.__dict__)
engine.resolve_perspective = perspective.resolve_perspective

import pytest
sys.exit(pytest.main(sys.argv[1:]))
