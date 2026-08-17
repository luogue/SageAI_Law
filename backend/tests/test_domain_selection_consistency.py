from review_v2.domain_selection import resolve_domain_selection
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2


FRAMEWORK_SUPPLY = """
长期供货合同
甲方（采购方）与乙方（供应商）签订本框架采购合同。
本合同期限为两年，双方建立长期供货关系，不约定最低采购数量。
甲方根据实际生产需求下达正式采购订单，采购订单经乙方确认后生效，并确定每批产品名称、规格型号、预计采购数量和交货期限。
乙方应按确认订单分批供货，双方以自然月为一个结算周期并每月对账，按实际供货数量结算货款，交货地点以订单为准。
"""

HOUSE_LEASE = """
房屋租赁合同
甲方（出租人）将住宅出租给乙方（承租人）居住使用。
租赁期限为两年，月租金为人民币5000元，承租人按月支付租金。
租赁押金为人民币10000元，退租交接后七日内退还押金。
"""


def test_high_confidence_framework_document_overrides_house_lease_selection():
    result = review_contract_v2(FRAMEWORK_SUPPLY, "house_lease", use_llm=False)
    resolution = result["domain_selection_resolution"]
    ids = [item["item_id"] for item in result["items"]]

    assert resolution["resolution"] == "DOCUMENT_OVERRIDE"
    assert resolution["document_domain"]["family"] == "SALE"
    assert resolution["document_domain"]["subject_matter"] == "GOODS"
    assert resolution["document_domain"]["transaction_structure"] == "FRAMEWORK_SUPPLY"
    assert resolution["selected_domain"] == "SALE"
    assert not [item_id for item_id in ids if item_id.startswith("HL-")]
    assert [item_id for item_id in ids if item_id.startswith("S-")]
    assert len([item_id for item_id in ids if item_id.startswith("FS-")]) == 14
    assert result["domain_selection_consistency_gate"]["gate_status"] == "PASS"
    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert result["report_context"]["transaction_structure"] == "FRAMEWORK_SUPPLY"


def test_high_confidence_house_lease_document_overrides_sale_selection():
    result = review_contract_v2(HOUSE_LEASE, "sale", use_llm=False)
    resolution = result["domain_selection_resolution"]
    ids = [item["item_id"] for item in result["items"]]

    assert resolution["resolution"] == "DOCUMENT_OVERRIDE"
    assert resolution["document_domain"]["family"] == "HOUSE_LEASE"
    assert resolution["selected_domain"] == "HOUSE_LEASE"
    assert [item_id for item_id in ids if item_id.startswith("HL-")]
    assert not [item_id for item_id in ids if item_id.startswith(("S-", "FS-", "RE-"))]
    assert result["domain_selection_consistency_gate"]["gate_status"] == "PASS"
    assert result["release_quality_gate"]["status"] == "REPORT_READY"


def test_weak_document_evidence_keeps_user_selection_as_prior():
    text = "双方就标的、价款和履行事项达成如下约定。"
    resolution, _, routed_type = resolve_domain_selection("sale", text, parse_contract_clauses(text))
    assert resolution.resolution == "USER_SELECTION_ACCEPTED"
    assert resolution.confidence == "low"
    assert routed_type == "sale"
