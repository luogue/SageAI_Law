"""Tests for the gift-contract adjudication engine."""

from datetime import date

from adjudicate.gift_configs import get_gift_config
from adjudicate.gift_engine import adjudicate_gift


TODAY = date(2026, 7, 27)


def test_gift_config_declares_core_mapping_and_patches():
    config = get_gift_config("gift")

    assert config.key == "gift"
    assert config.fact_mapping["核心争议"].startswith("合同性质认定")
    assert config.enabled_patches == tuple(f"G{i}" for i in range(1, 16))
    assert config.patch_mount("G2").node_id == "arbitrary_revocation"


def test_gift_jurisdiction_question():
    output = adjudicate_gift("赠与合同纠纷去哪里起诉？", today=TODAY)

    assert "被告住所地或者合同履行地" in output["conclusion"]
    assert "管辖程序" in output["triggered_patches"]


def test_g15_revocation_deadline_one_year():
    output = adjudicate_gift("赠与人想知道撤销期限，知道撤销事由后超过一年，是否还能撤销？", today=TODAY)

    assert "一年除斥期间" in output["conclusion"]
    assert "已超过" in output["conclusion"]
    assert "赠与合同纠纷的诉讼时效与除斥期间区分" in output["triggered_patches"]


def test_g1_classifies_gift_contract():
    output = adjudicate_gift("双方有合同性质争议，赠与人无偿给予财产，受赠人表示接受，没有对价。", today=TODAY)

    assert "合同性质认定为赠与合同" in output["conclusion"]
    assert "赠与合同的性质认定" in output["triggered_patches"]


def test_g1_classifies_sale_when_consideration_exists():
    output = adjudicate_gift("合同性质争议，名为赠与，但受赠人支付价款并付款购买。", today=TODAY)

    assert "更接近买卖合同" in output["conclusion"]


def test_no_acceptance_contract_not_established():
    output = adjudicate_gift("赠与人表示赠与财产，但受赠人未表示接受。", today=TODAY)

    assert "赠与合同不成立" in output["conclusion"]


def test_g12_donee_predeceased_terminates_contract():
    output = adjudicate_gift("受赠人先于赠与人死亡，交付前受赠人死亡。", today=TODAY)

    assert "赠与合同终止" in output["conclusion"]
    assert "受赠人先于赠与人死亡的处理" in output["triggered_patches"]


def test_g10_registration_required_not_done():
    output = adjudicate_gift("赠与财产是不动产房屋，需要登记，但未办理登记，尚未过户。", today=TODAY)

    assert "未办理登记手续" in output["conclusion"]
    assert "财产权利尚未转移" in output["conclusion"]
    assert "赠与财产需办理登记手续的处理" in output["triggered_patches"]


def test_g8_poverty_defense_established():
    output = adjudicate_gift("赠与人主张穷困抗辩，经济状况显著恶化，已经严重影响家庭生活和生产经营。", today=TODAY)

    assert "穷困抗辩权成立" in output["conclusion"]
    assert "可以不再履行赠与义务" in output["conclusion"]


def test_g14_general_gift_heirs_need_not_perform():
    output = adjudicate_gift("赠与人死亡后，受赠人请求继承人继续履行一般赠与义务。", today=TODAY)

    assert "继承人不应继续履行一般赠与义务" in output["conclusion"]
    assert "赠与人的继承人是否应继续履行赠与义务" in output["triggered_patches"]


def test_g14_notarized_gift_heirs_perform_within_estate():
    output = adjudicate_gift("赠与人死亡后，受赠人请求继承人继续履行，赠与合同经过公证。", today=TODAY)

    assert "继承人应在遗产范围内继续履行" in output["conclusion"]


def test_g11_termination_recharacterized_as_revocation():
    output = adjudicate_gift("赠与人要求解除赠与合同。", today=TODAY)

    assert "应定性为‘撤销’" in output["conclusion"]
    assert "赠与合同的任意解除 vs 撤销" in output["triggered_patches"]


def test_g2_arbitrary_revocation_before_transfer():
    output = adjudicate_gift("赠与人反悔撤销赠与，动产尚未交付，财产权利未转移，也没有公证。", today=TODAY)

    assert "任意撤销权成立" in output["conclusion"]
    assert "可以撤销赠与" in output["conclusion"]


def test_g2_arbitrary_revocation_not_allowed_after_transfer():
    output = adjudicate_gift("赠与人主张撤销赠与，但财产权利已转移，动产已交付。", today=TODAY)

    assert "任意撤销权不成立" in output["conclusion"]


def test_g13_waiver_revocation_blocks_arbitrary_revocation():
    output = adjudicate_gift("赠与人反悔撤销赠与，但合同约定不得撤销，赠与人放弃任意撤销权。", today=TODAY)

    assert "不得行使任意撤销权" in output["conclusion"]
    assert "赠与人与受赠人约定不得撤销的效力" in output["triggered_patches"]


def test_g3_statutory_revocation_with_return():
    output = adjudicate_gift("受赠人严重侵害赠与人，赠与人依法撤销赠与，在一年内主张法定撤销。", today=TODAY)

    assert "法定撤销权成立" in output["conclusion"]
    assert "请求返还财产" in output["conclusion"]
    assert "赠与合同撤销后的财产返还" in output["triggered_patches"]


def test_g3_statutory_revocation_expired():
    output = adjudicate_gift("受赠人不履行扶养义务，赠与人主张法定撤销，但知道撤销事由已超过一年。", today=TODAY)

    assert "一年除斥期间已超过" in output["conclusion"]


def test_g4_heir_revocation_established():
    output = adjudicate_gift("受赠人违法行为致赠与人死亡，继承人主张撤销，并在六个月内行使。", today=TODAY)

    assert "继承人/法定代理人撤销权成立" in output["conclusion"]
    assert "请求返还财产" in output["conclusion"]


def test_g4_heir_revocation_expired():
    output = adjudicate_gift("受赠人违法行为致赠与人死亡，继承人主张撤销，但超过六个月。", today=TODAY)

    assert "六个月除斥期间已超过" in output["conclusion"]


def test_g5_notarized_delivery_claim():
    output = adjudicate_gift("赠与合同经过公证，赠与人拒绝交付赠与财产，受赠人请求交付。", today=TODAY)

    assert "赠与人应交付赠与财产" in output["conclusion"]
    assert "公证/公益赠与的强制履行与赔偿责任" in output["triggered_patches"]


def test_g5_property_destroyed_by_intent_or_gross_negligence():
    output = adjudicate_gift("公益赠与中赠与人拒绝交付，赠与财产灭失，因赠与人故意或者重大过失造成损失9000元。", today=TODAY)

    assert "赠与人应承担赔偿责任" in output["conclusion"]
    assert "9000.00 元" in output["conclusion"]


def test_g6_obligation_attached_unfulfilled_allows_revocation():
    output = adjudicate_gift("附义务赠与中，受赠人不履行约定义务，赠与人要求处理。", today=TODAY)

    assert "受赠人未履行约定义务" in output["conclusion"]
    assert "可依法主张法定撤销权" in output["conclusion"]


def test_g6_obligation_attached_defect_warranty_limit():
    output = adjudicate_gift("附义务赠与中，受赠人已履行约定义务，但赠与财产有瑕疵。", today=TODAY)

    assert "附义务限度内" in output["conclusion"]
    assert "瑕疵担保责任" in output["conclusion"]


def test_g7_general_defect_no_liability():
    output = adjudicate_gift("一般赠与财产有瑕疵，受赠人要求赠与人赔偿。", today=TODAY)

    assert "赠与人不承担瑕疵担保责任" in output["conclusion"]
    assert "不承担赔偿责任" in output["conclusion"]


def test_g7_defect_with_deliberate_non_disclosure_liability():
    output = adjudicate_gift("赠与财产有瑕疵，赠与人故意不告知瑕疵，造成损失4000元。", today=TODAY)

    assert "赠与人承担赔偿责任" in output["conclusion"]
    assert "4000.00 元" in output["conclusion"]


def test_g9_return_after_revocation_with_value_compensation():
    output = adjudicate_gift("撤销权成立，已经撤销赠与，赠与财产无法返还，财产价值6000元，请求返还。", today=TODAY)

    assert "受赠人应折价赔偿" in output["conclusion"]
    assert "6000.00 元" in output["conclusion"]
