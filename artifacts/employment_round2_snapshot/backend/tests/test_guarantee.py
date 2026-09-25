"""Tests for the guarantee-contract adjudication engine."""

from datetime import date

from adjudicate.guarantee_configs import get_guarantee_config
from adjudicate.guarantee_engine import adjudicate_guarantee


TODAY = date(2026, 7, 27)


def test_guarantee_config_declares_core_mapping_and_patches():
    config = get_guarantee_config("guarantee")

    assert config.key == "guarantee"
    assert config.fact_mapping["合同主体"] == "债权人/保证人/债务人"
    assert config.fact_mapping["核心义务"] == "债务人不履行债务时，保证人代为履行或承担责任"
    assert config.fact_mapping["核心争议"] == "保证方式（一般/连带）→ 保证期间是否已过 → 债权人是否在保证期间内行使权利 → 主合同变更是否影响保证责任"
    assert set(config.reused_modules) == {"管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"}

    patch_ids = {mount.patch_id for mount in config.patch_mounts}
    assert patch_ids == {f"G{i}" for i in range(1, 16)}
    for mount in config.patch_mounts:
        assert mount.node_id
        assert mount.mount_mode
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_guarantee_jurisdiction_question():
    output = adjudicate_guarantee("保证合同纠纷去哪里起诉？", today=TODAY)

    assert output["triggered_patches"] == ["管辖程序"]
    assert output["conclusion"] == "保证合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理"
    assert output["facts"]["asks_jurisdiction"] is True


def test_g12_special_guarantor_invalid():
    output = adjudicate_guarantee("政府机关担保，机关法人作为保证人。", today=TODAY)

    assert output["triggered_patches"] == ["保证人主体资格特殊规定"]
    assert output["conclusion"] == "保证人不具备保证人资格，保证合同无效。"


def test_g11_company_guarantee_good_faith_valid():
    output = adjudicate_guarantee("公司对外担保，债权人已合理审查董事会决议，属于相对人善意。", today=TODAY)

    assert output["triggered_patches"] == ["公司对外担保效力"]
    assert output["conclusion"] == "公司对外担保，相对人善意，担保合同对公司发生效力。"


def test_g9_main_contract_invalid_invalidates_guarantee():
    output = adjudicate_guarantee("主合同无效，但保证合同约定担保独立，主合同无效仍承担保证责任。", today=TODAY)

    assert output["triggered_patches"] == ["保证合同无效后责任承担"]
    assert output["conclusion"] == "保证合同无效，各方按过错承担责任。一般保证人仍享有先诉抗辩权。"


def test_g1_unclear_guarantee_type_presumed_general():
    output = adjudicate_guarantee("保证合同只写担保人签字，未约定保证方式，债权人要求保证人直接承担责任。", today=TODAY)

    assert output["triggered_patches"] == ["保证方式约定不明推定"]
    assert output["conclusion"] == "保证方式约定不明，依法推定为一般保证。一般保证人享有先诉抗辩权，债权人须先向债务人主张权利。"


def test_g2_unclear_period_defaults_to_six_months():
    output = adjudicate_guarantee("保证合同未约定保证期间，保证期间不明。", today=TODAY)

    assert output["triggered_patches"] == ["保证期间确定规则"]
    assert output["conclusion"] == "保证期间为主债务履行期限届满之日起六个月。保证期间不发生中止、中断和延长。"


def test_g8_maximum_guarantee_period_rule():
    output = adjudicate_guarantee("最高额保证合同，最高额保证未约定期间。", today=TODAY)

    assert output["triggered_patches"] == ["最高额保证特殊规则"]
    assert output["conclusion"] == "最高额保证，保证期间为最高额保证终止之日或收到终止通知之日起六个月。"


def test_g4_general_guarantee_no_action_extinguishes_liability():
    output = adjudicate_guarantee("一般保证，保证期间已过，债权人未在保证期间内对债务人提起诉讼。", today=TODAY)

    assert output["triggered_patches"] == ["保证期间内行使权利认定"]
    assert output["conclusion"] == "债权人未在保证期间内依法行使权利，保证责任消灭。"


def test_g13_waiver_prior_lawsuit_allows_direct_claim():
    output = adjudicate_guarantee("一般保证中，保证人书面放弃先诉抗辩权，债权人要求保证人承担责任。", today=TODAY)

    assert output["triggered_patches"] == ["放弃先诉抗辩权效力"]
    assert output["conclusion"] == "保证人已书面放弃先诉抗辩权，债权人可以直接向保证人主张权利。"


def test_g3_general_guarantor_has_prior_lawsuit_defense():
    output = adjudicate_guarantee("一般保证，保证人主张先诉抗辩权，债务人财产尚未强制执行。", today=TODAY)

    assert output["triggered_patches"] == ["一般保证人先诉抗辩权"]
    assert output["conclusion"] == "一般保证人享有先诉抗辩权，债权人应先就债务人财产强制执行。如存在例外情形，先诉抗辩权消灭。"


def test_only_sue_general_guarantor_rejected():
    output = adjudicate_guarantee("一般保证，债权人仅起诉一般保证人，未起诉债务人。", today=TODAY)

    assert output["conclusion"] == "债权人仅起诉一般保证人的，应当驳回起诉。"


def test_g4_joint_guarantee_action_within_period_preserves_liability():
    output = adjudicate_guarantee("连带责任保证，债权人在保证期间内请求保证人承担责任。", today=TODAY)

    assert output["triggered_patches"] == ["保证期间内行使权利认定"]
    assert output["conclusion"] == "债权人已在保证期间内依法行使权利，保证责任不消灭；债权人可以请求债务人履行，也可以请求保证人在保证范围内承担责任。"


def test_g5_main_contract_change_aggravated_without_consent():
    output = adjudicate_guarantee("主合同变更，提高利率加重债务，未经保证人书面同意。", today=TODAY)

    assert output["triggered_patches"] == ["主合同变更未经保证人同意"]
    assert output["conclusion"] == "主合同变更未经保证人书面同意，保证人对加重部分不承担保证责任。"


def test_g6_credit_assignment_without_notice_no_effect_on_guarantor():
    output = adjudicate_guarantee("债权转让，但未通知保证人，受让人要求保证人承担责任。", today=TODAY)

    assert output["triggered_patches"] == ["债权转让与债务转移影响"]
    assert output["conclusion"] == "债权转让未通知保证人，该转让对保证人不发生效力，保证人对受让人不承担保证责任。"


def test_g10_guarantor_recourse_after_payment():
    output = adjudicate_guarantee("保证人已承担保证责任，保证人代偿100000元后向债务人追偿并主张代位权。", today=TODAY)

    assert output["triggered_patches"] == ["保证人追偿权与代位权"]
    assert output["conclusion"] == "保证人已承担保证责任 100000.00 元，有权向债务人追偿，并代位行使债权人对债务人的权利。"


def test_g7_joint_guarantee_without_share():
    output = adjudicate_guarantee("同一债务有两个以上保证人，多个保证人共同保证，没有约定保证份额。", today=TODAY)

    assert output["triggered_patches"] == ["共同保证责任承担"]
    assert output["conclusion"] == "共同保证，无约定保证份额，债权人可以请求任何一个保证人在其保证范围内承担保证责任；向部分保证人行权的效力不当然及于其他保证人。"


def test_g14_post_period_signature_does_not_restore_liability():
    output = adjudicate_guarantee("保证期间届满后签字，保证人只是在催收通知上签字，没有新的保证合同。", today=TODAY)

    assert output["triggered_patches"] == ["保证期间届满后签字效力"]
    assert output["conclusion"] == "保证期间已过，保证人签字不构成新的保证合同，保证责任不恢复。"


def test_g15_main_debt_limitation_known_by_guarantor():
    output = adjudicate_guarantee("主债务诉讼时效届满后，保证人知道时效届满仍提供保证。", today=TODAY)

    assert output["triggered_patches"] == ["主债务诉讼时效届满影响"]
    assert output["conclusion"] == "保证人知道主债务诉讼时效已届满，不得以时效届满为由拒绝承担保证责任。"
