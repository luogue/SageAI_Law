import pytest
from review_v2.engine import review_contract_v2
from review_v2.parameter_validation import extract_parameters, compare


def review(text, identifier):
    result = review_contract_v2("供用电合同。" + text, "utility_supply", use_llm=False)
    return next(i for i in result["items"] if i["item_id"] == identifier)


@pytest.mark.parametrize("text, expected", [
    ("欠费原因消除后24小时内恢复供电。", "通过"),
    ("缴清费用后三个工作日内恢复供电。", "风险条款"),
    ("缴费后甲方视情况恢复供电。", "风险条款"),
    ("缴清费用后四十八小时内恢复供电。", "风险条款"),
    ("缴清费用后1天内恢复供电。", "通过"),
])
def test_restoration_parameter_validation(text, expected):
    assert review(text, "US-04-04")["coverage_status"] == expected


@pytest.mark.parametrize("text, expected", [
    ("工业用户当年欠付电费，自逾期之日起每日按千分之二支付违约金。", "通过"),
    ("居民用户欠付电费，自逾期之日起每日按0.1%支付违约金。", "通过"),
    ("工业用户跨日历年欠付电费，自逾期之日起每日按3‰支付违约金。", "通过"),
    ("工业用户当年欠付电费，自逾期之日起每日按3‰支付违约金。", "风险条款"),
    ("工业用户欠付电费，自逾期之日起每日按5‰支付违约金。", "风险条款"),
    ("工业用户逾期欠付电费应承担违约金。", "部分覆盖"),
    ("用户逾期欠付电费每日按千分之一支付违约金。", "部分覆盖"),
])
def test_daily_rate_conditions(text, expected):
    assert review(text, "US-07-02")["coverage_status"] == expected


@pytest.mark.parametrize("text, passed", [
    ("第二条 用电地址为工业园1号，用电容量500千伏安。", False),
    ("附件一：用户用电地址及容量表。用电地址为工业园1号，用电容量500千伏安。", True),
])
def test_address_capacity_attachment_entity(text, passed):
    assert (review(text, "US-12-01")["coverage_status"] == "通过") == passed


def test_all_material_unilateral_termination_sources_collected():
    item = review("第五条 甲方认为继续供电不经济即可解除合同。\n第十二条 甲方认为继续履行增加经营成本，可以提前3日通知解除合同。", "US-11-01")
    source = "\n".join(e["text"] for e in item["evidence_clauses"])
    assert "不经济" in source and "增加经营成本" in source


def test_numeric_units_are_generic_and_conditions_are_not_assumed():
    for text, maximum, expected in [("48小时", 24, "ADVERSE"), ("2天", 24, "ADVERSE"),
                                     ("0.3%", .002, "ADVERSE"), ("千分之二", .002, "COVERED"),
                                     ("500万元", 3000000, "ADVERSE"), ("三次", 2, "ADVERSE")]:
        parameter = extract_parameters(text)[0]
        assert compare(parameter, maximum) == expected
        assert compare(parameter, maximum, condition=None) == "CONDITION_UNRESOLVED"


def test_parameter_gate_rejects_tampered_pass():
    from review_v2.utility_supply_evidence import consistency_gate
    item = review("工业用户逾期电费每日按3‰支付违约金。", "US-07-02")
    item["coverage_status"] = "通过"
    assert consistency_gate([item])["status"] == "BLOCKED"
