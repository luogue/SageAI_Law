"""Tests for the unified review-v2 contract checklist registry."""

import pytest

from review_v2.agency_contract_checklist import AGENCY_REVIEW_CHECKLIST
from review_v2.brokerage_contract_checklist import BROKERAGE_REVIEW_CHECKLIST
from review_v2.commission_agency_contract_checklist import COMMISSION_AGENCY_REVIEW_CHECKLIST
from review_v2.construction_contract_checklist import CONSTRUCTION_REVIEW_CHECKLIST
from review_v2.contract_registry import (
    CONTRACT_CHECKLISTS,
    CONTRACT_TYPE_META,
    ContractType,
    UnsupportedContractTypeError,
    get_checklist,
    get_contract_meta,
    supported_contract_types,
    validate_all_checklists,
)
from review_v2.finance_lease_contract_checklist import FINANCE_LEASE_REVIEW_CHECKLIST
from review_v2.gift_contract_checklist import GIFT_REVIEW_CHECKLIST
from review_v2.guarantee_contract_checklist import GUARANTEE_REVIEW_CHECKLIST
from review_v2.house_lease_checklist import HOUSE_LEASE_REVIEW_CHECKLIST, ReviewCheckpoint
from review_v2.loan_contract_checklist import LOAN_REVIEW_CHECKLIST
from review_v2.safekeeping_contract_checklist import SAFEKEEPING_REVIEW_CHECKLIST
from review_v2.sale_contract_checklist import SALE_REVIEW_CHECKLIST
from review_v2.service_contract_checklist import SERVICE_REVIEW_CHECKLIST
from review_v2.technology_contract_checklist import TECHNOLOGY_REVIEW_CHECKLIST
from review_v2.transportation_contract_checklist import TRANSPORTATION_REVIEW_CHECKLIST
from review_v2.utility_supply_contract_checklist import UTILITY_SUPPLY_REVIEW_CHECKLIST
from review_v2.warehouse_contract_checklist import WAREHOUSE_REVIEW_CHECKLIST
from review_v2.work_contract_checklist import WORK_CONTRACT_REVIEW_CHECKLIST
from review_v2.engine import review_contract_v2


def test_contract_registry_declares_all_implemented_checklists():
    assert set(supported_contract_types()) == {"lease", "sale", "gift", "deposit", "work_contract", "transportation", "agency", "loan", "service", "guarantee", "finance_lease", "warehouse", "construction", "technology", "commission_agency", "utility_supply", "brokerage"}
    assert CONTRACT_CHECKLISTS == {
        "lease": HOUSE_LEASE_REVIEW_CHECKLIST,
        "sale": SALE_REVIEW_CHECKLIST,
        "gift": GIFT_REVIEW_CHECKLIST,
        "deposit": SAFEKEEPING_REVIEW_CHECKLIST,
        "work_contract": WORK_CONTRACT_REVIEW_CHECKLIST,
        "transportation": TRANSPORTATION_REVIEW_CHECKLIST,
        "agency": AGENCY_REVIEW_CHECKLIST,
        "loan": LOAN_REVIEW_CHECKLIST,
        "service": SERVICE_REVIEW_CHECKLIST,
        "guarantee": GUARANTEE_REVIEW_CHECKLIST,
        "finance_lease": FINANCE_LEASE_REVIEW_CHECKLIST,
        "warehouse": WAREHOUSE_REVIEW_CHECKLIST,
        "construction": CONSTRUCTION_REVIEW_CHECKLIST,
        "technology": TECHNOLOGY_REVIEW_CHECKLIST,
        "commission_agency": COMMISSION_AGENCY_REVIEW_CHECKLIST,
        "utility_supply": UTILITY_SUPPLY_REVIEW_CHECKLIST,
        "brokerage": BROKERAGE_REVIEW_CHECKLIST,
    }
    assert CONTRACT_TYPE_META[ContractType.LEASE].response_key == "house_lease"


def test_get_checklist_supports_canonical_keys_and_aliases():
    assert get_checklist("lease") is HOUSE_LEASE_REVIEW_CHECKLIST
    assert get_checklist("house_lease") is HOUSE_LEASE_REVIEW_CHECKLIST
    assert get_checklist("房屋租赁合同") is HOUSE_LEASE_REVIEW_CHECKLIST
    assert get_checklist("sale") is SALE_REVIEW_CHECKLIST
    assert get_checklist("gift") is GIFT_REVIEW_CHECKLIST
    assert get_checklist("safekeeping") is SAFEKEEPING_REVIEW_CHECKLIST
    assert get_checklist("work_contract") is WORK_CONTRACT_REVIEW_CHECKLIST
    assert get_checklist("承揽合同") is WORK_CONTRACT_REVIEW_CHECKLIST
    assert get_checklist("transportation") is TRANSPORTATION_REVIEW_CHECKLIST
    assert get_checklist("运输合同") is TRANSPORTATION_REVIEW_CHECKLIST
    assert get_checklist("agency") is AGENCY_REVIEW_CHECKLIST
    assert get_checklist("委托合同") is AGENCY_REVIEW_CHECKLIST
    assert get_checklist("loan") is LOAN_REVIEW_CHECKLIST
    assert get_checklist("借款合同") is LOAN_REVIEW_CHECKLIST
    assert get_checklist("service") is SERVICE_REVIEW_CHECKLIST
    assert get_checklist("服务合同") is SERVICE_REVIEW_CHECKLIST
    assert get_checklist("guarantee") is GUARANTEE_REVIEW_CHECKLIST
    assert get_checklist("finance_lease") is FINANCE_LEASE_REVIEW_CHECKLIST
    assert get_checklist("financial_lease") is FINANCE_LEASE_REVIEW_CHECKLIST
    assert get_checklist("warehouse") is WAREHOUSE_REVIEW_CHECKLIST
    assert get_checklist("storage") is WAREHOUSE_REVIEW_CHECKLIST
    assert get_checklist("construction") is CONSTRUCTION_REVIEW_CHECKLIST
    assert get_checklist("construction_contract") is CONSTRUCTION_REVIEW_CHECKLIST
    assert get_checklist("technology") is TECHNOLOGY_REVIEW_CHECKLIST
    assert get_checklist("tech") is TECHNOLOGY_REVIEW_CHECKLIST
    assert get_checklist("commission_agency") is COMMISSION_AGENCY_REVIEW_CHECKLIST
    assert get_checklist("commission") is COMMISSION_AGENCY_REVIEW_CHECKLIST
    assert get_checklist("utility_supply") is UTILITY_SUPPLY_REVIEW_CHECKLIST
    assert get_checklist("power_supply") is UTILITY_SUPPLY_REVIEW_CHECKLIST
    assert get_checklist("brokerage") is BROKERAGE_REVIEW_CHECKLIST
    assert get_checklist("broker") is BROKERAGE_REVIEW_CHECKLIST
    assert get_checklist("保证合同") is GUARANTEE_REVIEW_CHECKLIST
    assert get_contract_meta("寄存合同").key is ContractType.DEPOSIT


def test_get_checklist_rejects_unsupported_type_with_clear_error():
    with pytest.raises(UnsupportedContractTypeError, match="不支持的合同类型"):
        get_checklist("unknown_contract")


def test_registered_checklists_share_review_checkpoint_schema():
    for checklist in CONTRACT_CHECKLISTS.values():
        assert checklist
        assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_registered_checklists_pass_integrity_validation():
    warnings = validate_all_checklists()

    assert set(warnings) == {"lease", "sale", "gift", "deposit", "work_contract", "transportation", "agency", "loan", "service", "guarantee", "finance_lease", "warehouse", "construction", "technology", "commission_agency", "utility_supply", "brokerage"}
    assert all(isinstance(items, tuple) for items in warnings.values())


def test_review_engine_uses_registry_alias_without_breaking_response_key():
    output = review_contract_v2("出租人将房屋出租给承租人，押金为3000元。", "lease", use_llm=False)

    assert output["success"] is True
    assert output["contract_type"] == "house_lease"
    assert output["contract_type_name"] == "房屋租赁合同"
    assert output["all_items_count"] == 50
