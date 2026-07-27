"""Tests for the work-contract adjudication engine."""

from datetime import date

from adjudicate.work_contract_configs import get_work_contract_config
from adjudicate.work_contract_engine import adjudicate_work_contract


def test_work_contract_config_declares_core_mapping_and_patches():
    config = get_work_contract_config("work_contract")

    assert config.key == "work_contract"
    assert config.fact_mapping["合同主体"] == "承揽人/定作人"
    assert config.fact_mapping["核心义务"] == "完成工作、交付符合质量要求的工作成果"
    assert config.fact_mapping["核心争议"] == "工作成果是否符合质量要求 → 瑕疵程度 → 定作人选择何种救济方式"
    assert set(config.reused_modules) == {"管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"}

    patch_ids = {mount.patch_id for mount in config.patch_mounts}
    assert patch_ids == {"C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"}
    for mount in config.patch_mounts:
        assert mount.node_id
        assert mount.mount_mode
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_work_contract_jurisdiction_question_uses_defendant_or_performance_place():
    output = adjudicate_work_contract(
        "承揽合同纠纷去哪里起诉？",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "承揽合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理"
    assert output["triggered_patches"] == ["管辖程序"]
    assert output["facts"]["asks_jurisdiction"] is True


def test_pure_third_party_tort_is_diverted_at_entry():
    output = adjudicate_work_contract(
        "陌生人损坏了定作物，定作人要求赔偿。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "本案涉及侵权责任，非承揽合同纠纷，不适用本承揽合同裁判引擎"
    assert output["facts"]["third_party_tort"] is True


def test_limitation_period_over_three_years_is_rejected():
    output = adjudicate_work_contract(
        "承揽人于2020年1月1日交付工作成果，定作人现在起诉质量瑕疵。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "诉讼时效已过，驳回请求"
    assert output["path"][-1] == "诉讼时效"


def test_c6_unauthorized_main_work_subcontract_allows_termination():
    output = adjudicate_work_contract(
        "承揽人未经定作人同意，将主要工作交给第三人完成。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "主要工作未经定作人同意转包，定作人可以解除合同；承揽人仍应对已完成成果及因此造成的损失承担责任。"
    assert output["triggered_patches"] == ["转包/分包的效力"]
    assert output["facts"]["main_work_subcontract"] is True


def test_c7_classifies_by_substance_not_contract_name():
    output = adjudicate_work_contract(
        "合同名为买卖合同，但实质是按定作人要求定制并完成特定工作，双方存在合同性质争议。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["承揽/买卖合同定性争议"]
    assert output["conclusion"] == "根据合同实质内容，倾向认定为承揽合同；应继续按工作成果质量、交付、报酬、材料和解除规则审查。"


def test_c9_illegal_total_subcontract_makes_contractor_fully_responsible_for_defect():
    output = adjudicate_work_contract(
        "承揽人未经定作人同意，将全部工作转包给第三人，导致质量不合格。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["转包/分包的效力", "违法分包/转包"]
    assert output["conclusion"] == "未经同意违法转包，定作人可以解除合同；违法转包导致工作成果质量问题的，承揽人承担全部责任。"


def test_customer_assistance_failure_after_urge_allows_contractor_termination():
    output = adjudicate_work_contract(
        "定作人未提供图纸且不配合，承揽人已经催告，定作人逾期仍不履行。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "定作人逾期不履行协助义务，承揽人可以解除合同，并可主张因此受到的损失。"
    assert output["path"][-1] == "定作人协助义务审查"


def test_customer_change_request_requires_compensation_for_contractor_loss():
    output = adjudicate_work_contract(
        "定作人中途变更设计，造成承揽人返工费3000元。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "定作人中途变更承揽要求有效，但应赔偿承揽人损失 3000.00 元。"
    assert output["facts"]["contractor_loss"] == 3000


def test_c4_customer_material_defect_with_notice_is_customer_responsibility():
    output = adjudicate_work_contract(
        "定作人提供的材料不合格，承揽人及时检验并通知定作人更换。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "材料瑕疵责任由定作人承担；定作人应更换、补齐或采取补救措施。"
    assert output["triggered_patches"] == ["定作人提供的材料瑕疵"]


def test_c5_improper_custody_requires_compensation():
    output = adjudicate_work_contract(
        "定作人提供材料在承揽人保管期间受潮，承揽人存放不当，实际损失2000元。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "承揽人保管未尽到妥善保管义务，承担赔偿责任 2000.00 元。"
    assert output["triggered_patches"] == ["承揽人保管义务"]


def test_contractor_lien_for_unpaid_remuneration():
    output = adjudicate_work_contract(
        "定作人未支付报酬8000元，承揽人留置工作成果。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "承揽人对完成的工作成果享有留置权或者有权拒绝交付。"
    assert output["path"][-1] == "承揽人留置权"


def test_c3_customer_arbitrary_termination_before_completion():
    output = adjudicate_work_contract(
        "承揽人尚未完成工作，定作人要求解除合同，承揽人已投入材料费5000元。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "定作人任意解除权成立，解除有效，应赔偿承揽人损失 5000.00 元。"
    assert output["triggered_patches"] == ["定作人任意解除权"]


def test_c8_arbitrary_termination_can_be_limited_near_completion():
    output = adjudicate_work_contract(
        "承揽人尚未完成工作，但已经接近完成且投入绝大部分成本，定作人要求解除合同，承揽人损失9000元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["定作人任意解除权", "定作人任意解除权的行使边界"]
    assert output["conclusion"] == "定作人任意解除权行使可能受限；如解除被支持，定作人仍应赔偿承揽人实际损失 9000.00 元。"


def test_c1_c2_minor_defect_uses_repair_first():
    output = adjudicate_work_contract(
        "承揽人已交付工作成果，但质量不合格，瑕疵轻微可修复，定作人要求修理。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["质量瑕疵认定标准", "定作人救济方式的选择权"]
    assert output["conclusion"] == "定作人合理选择修理，承揽人应负责修复瑕疵并承担修复费用；修理仍不合格的，定作人可再要求减少报酬或赔偿损失。"


def test_c1_known_defect_and_acceptance_blocks_quality_defense():
    output = adjudicate_work_contract(
        "承揽人已交付工作成果，定作人明知瑕疵仍接收成果且未提出异议。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "工作成果质量视为定作人认可，瑕疵抗辩不成立；定作人应支付相应报酬。"
    assert output["triggered_patches"] == ["质量瑕疵认定标准"]


def test_severe_defect_can_trigger_remake():
    output = adjudicate_work_contract(
        "承揽人已交付工作成果，但质量不合格，瑕疵严重无法修复，定作人要求重作。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "定作人合理选择重作，承揽人应重新完成工作，原不合格成果按实际情况处理，重作费用由承揽人承担。"
    assert output["facts"]["serious_defect"] is True


def test_delivered_and_qualified_result_requires_full_payment():
    output = adjudicate_work_contract(
        "承揽人已交付工作成果，验收合格，定作人拒付报酬12000元。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "定作人应支付报酬 12000.00 元。"
    assert output["path"][-1] == "报酬支付"
