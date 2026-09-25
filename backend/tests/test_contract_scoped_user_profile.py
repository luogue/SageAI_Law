import asyncio
import json

import pytest

from review_v2.profile_catalog import PROFILE_OPTIONS, profile_catalog, profile_options
from review_v2.user_profile import UserRiskProfile, normalize_profile, get_priority_checkpoints
from review_v2.perspective_resolution import resolve_perspective, perspective_domain_consistency_gate


CASES = [
    ("house_lease", "房屋租赁合同\n出租人甲将房屋出租给承租人乙用于居住，租期一年，月租金3000元，押金3000元。", "承租人", "LESSEE"),
    ("work_contract", "承揽合同\n定作方甲委托承揽方乙加工设备10台，报酬10万元，甲方提供材料，乙方于十日内交付工作成果，甲方负责验收。", "定作方", "WORK_CUSTOMER"),
    ("transportation", "运输合同\n托运人甲委托承运人乙运输货物，货物为设备10件，起运地上海，目的地北京，运费1000元，乙方于三日内交付收货人丙并取得签收凭证。", "托运人", "CONSIGNOR"),
    ("investment", "投资协议\n投资方甲向融资方乙投入100万元取得目标公司10%股权，双方约定投资款于交割日支付，公司承诺完成股权登记。", "投资方", "INVESTOR"),
    ("shareholders", "股东协议\n股东甲和股东乙约定目标公司的表决权、董事会席位及公司治理安排。股东会按实缴出资比例分红，股东退出应事先通知其他股东。", "股东", "SHAREHOLDER"),
    ("labor", "劳动合同\n用人单位甲聘用劳动者乙，工作岗位为工程师，月工资10000元，每周工作五日，每日八小时，依法缴纳社会保险。", "劳动者", "WORKER"),
]


@pytest.mark.parametrize("key", PROFILE_OPTIONS)
def test_legacy_defaults_scoped_for_every_supported_type(key):
    old = UserRiskProfile.from_dict({"user_identity": "个人租客/买方", "contract_scenario": "居住用途",
                                    "risk_appetite": "激进", "bargaining_position": "弱势方"})
    effective = normalize_profile(old, key)
    assert effective.user_identity == profile_options(key)["identities"][0]
    assert effective.risk_appetite == "激进"
    assert effective.bargaining_position == "弱势方"
    assert old.user_identity == "个人租客/买方"  # request copy, no shared mutation
    if key != "house_lease":
        assert "居住用途" not in effective.contract_scenario
        assert not get_priority_checkpoints(effective)


@pytest.mark.parametrize("key", PROFILE_OPTIONS)
def test_omitted_profile_gets_visible_contract_default_after_routing(key):
    p = normalize_profile(None, key, previous_type=key)
    assert p.user_identity == profile_options(key)["identities"][0]
    neutral = normalize_profile(UserRiskProfile(contract_type=key), key, previous_type=key)
    assert neutral.user_identity == "合同当事人"


@pytest.mark.parametrize("key,text,identity,canonical", CASES)
def test_real_engine_profile_matches_effective_review_parameters(key, text, identity, canonical):
    from review_v2.engine import review_contract_v2
    profile = UserRiskProfile.from_dict({"user_identity": "个人租客/买方", "contract_scenario": "居住用途",
                                         "risk_appetite": "保守", "bargaining_position": "弱势方"})
    result = review_contract_v2(text, key, use_llm=False, profile=profile)
    assert result["success"]
    assert result["contract_type"] == key
    assert result["profile"]["user_identity"] == identity
    assert result["profile"]["risk_appetite"] == "保守"
    assert result["profile"]["bargaining_position"] == "弱势方"
    assert result["perspective_resolution"]["canonical_role"] == canonical
    assert result["contract_context"]["user_role"] == canonical.lower()
    assert result["profile"]["user_identity"] == result["perspective_resolution"]["display_role"]
    for item in result["items"]:
        trace = item.get("decision_trace") or {}
        if "user_perspective" in trace:
            assert trace["user_perspective"] == canonical
    if key != "house_lease":
        visible = json.dumps({"profile": result["profile"], "report": result["result"]}, ensure_ascii=False)
        assert not any(word in visible for word in ("个人租客", "居住用途", "投资/转租"))


@pytest.mark.parametrize("key,text,identity,canonical", CASES[1:])
def test_reclassification_discards_lease_context_keeps_preferences(key, text, identity, canonical):
    from review_v2.engine import review_contract_v2
    old = UserRiskProfile.conservative_individual_tenant()
    result = review_contract_v2(text, "house_lease", use_llm=False, profile=old)
    assert result["contract_type"] == key
    assert result["profile"]["user_identity"] == identity
    assert result["profile"]["contract_type"] == key
    assert result["profile"]["risk_appetite"] == "保守"
    assert result["perspective_resolution"]["canonical_role"] == canonical


@pytest.mark.parametrize("key,family,role,canonical", [
    ("work_contract", "WORK_CONTRACT", "承揽方", "WORK_CONTRACTOR"),
    ("transportation", "TRANSPORTATION", "承运人", "CARRIER"),
    ("investment", "EQUITY_INVESTMENT", "融资方", "TARGET_COMPANY"),
    ("labor", "EMPLOYMENT", "用人单位", "LABOR_EMPLOYER"),
    ("equity_transfer", "EQUITY_INVESTMENT", "受让方", "EQUITY_TRANSFEREE"),
    ("sale", "SALE", "卖方", "SELLER"),
    ("house_lease", "LEASE", "出租人", "LESSOR"),
])
def test_selected_counterparty_role_is_not_replaced(key, family, role, canonical):
    p = normalize_profile(UserRiskProfile.from_dict({"review_role": role, "user_identity": "个人租客/买方"}), key)
    assert p.user_identity == role
    resolution = resolve_perspective(p.user_identity, family)
    assert resolution.canonical_role == canonical
    assert perspective_domain_consistency_gate(resolution)["status"] == "REPORT_READY"


def test_unknown_and_explicit_neutral_are_neutral():
    p = normalize_profile(UserRiskProfile.conservative_individual_tenant(), "unknown")
    assert p.user_identity == "合同当事人"
    assert p.contract_scenario == "一般合同"
    for family in ("SALE", "WORK_CONTRACT", "OTHER"):
        r = resolve_perspective("合同当事人", family)
        assert r.canonical_role == "OTHER"
        assert perspective_domain_consistency_gate(r)["status"] == "REPORT_READY"


@pytest.mark.parametrize("scenario", ["居住用途", "住宅租赁", "房屋租赁合同", "商铺租赁", "投资/转租"])
def test_legacy_report_scenarios_cannot_leak(scenario):
    p = normalize_profile(UserRiskProfile(contract_scenario=scenario), "work_contract")
    assert p.contract_scenario == "承揽加工"


def test_catalog_endpoint_matches_backend_options():
    from routers.review_v2 import review_v2_profile_options
    assert asyncio.run(review_v2_profile_options(current_user={})) == profile_catalog()


@pytest.mark.parametrize("key,text,identity,canonical", CASES)
def test_file_http_entry_returns_same_scoped_profile(key, text, identity, canonical):
    from io import BytesIO
    from docx import Document
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as router
    app = FastAPI()
    app.include_router(router.router)
    app.dependency_overrides[router.get_current_user] = lambda: {"id": 1}
    document = Document()
    for line in text.splitlines():
        document.add_paragraph(line)
    content = BytesIO()
    document.save(content)
    with TestClient(app) as client:
        response = client.post("/review-v2/file", files={"file": ("contract.docx", content.getvalue(),
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
                               data={"contract_type": key, "use_llm": "false", "profile_json": json.dumps({
                                   "user_identity": "个人租客/买方", "contract_scenario": "居住用途",
                                   "risk_appetite": "激进", "bargaining_position": "强势方"})})
    assert response.status_code == 200, response.text[:400]
    result = response.json()
    assert result["profile"]["user_identity"] == identity
    assert result["profile"]["contract_type"] == key
    assert result["profile"]["risk_appetite"] == "激进"
    assert result["perspective_resolution"]["canonical_role"] == canonical
    if key != "house_lease":
        assert "居住用途" not in result["profile"]["contract_scenario"]


@pytest.mark.parametrize("key,alias,expected", [
    ("sale", "甲方/供方", "甲方/卖方"), ("work_contract", "乙方/承揽人", "乙方/承揽方"),
    ("transportation", "承运方", "承运人"), ("house_lease", "房东", "出租人"),
])
def test_scoped_role_aliases(key, alias, expected):
    assert normalize_profile(UserRiskProfile(user_identity=alias), key).user_identity == expected


@pytest.mark.parametrize("endpoint,analyzer", [
    ("review_v2_litigation_analysis", "litigation_analyzer"),
    ("review_v2_negotiation_analysis", "negotiation_analyzer"),
    ("review_v2_jurisdiction_prediction", "jurisdiction_analyzer"),
])
def test_auxiliary_endpoints_use_effective_profile(monkeypatch, endpoint, analyzer):
    from routers import review_v2 as router
    effective = normalize_profile(UserRiskProfile(risk_appetite="激进"), "work_contract").to_dict()
    monkeypatch.setattr(router, "review_contract_v2", lambda *a, **kw: {"success": True, "items": [], "profile": effective})
    result = asyncio.run(getattr(router, endpoint)(router.ReviewV2Input(contract_text="承揽合同", contract_type="work_contract"), current_user={}))
    assert result["profile"] == effective
