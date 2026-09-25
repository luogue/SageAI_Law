"""Tests for the second-version housing lease adjudication engine."""

from datetime import date

from adjudicate.engine_v2 import adjudicate_deposit_v2, extract_facts
from adjudicate.lease_configs import get_lease_config


def test_tenant_death_with_cohabitant_continues_contract():
    output = adjudicate_deposit_v2(
        "租客在租赁期限内去世，其共同居住人愿意继续承租。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "承租人死亡，存在共同居住人或共同经营人，原租赁合同继续有效，押金不退，合同由该人接替履行。"
    assert output["triggered_patches"] == ["补丁一：承租人死亡"]
    assert output["path"][-1] == "补丁一：承租人死亡"
    assert "押金结算" not in output["path"]
    assert "触发补丁：补丁一：承租人死亡" in output["result"]


def test_tenant_death_without_cohabitant_ends_contract():
    output = adjudicate_deposit_v2(
        "承租人死亡，没有共同居住人，也没有共同经营人。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "承租人死亡，无共同居住人或共同经营人，租赁合同终止，押金应退还承租人的继承人。"
    assert output["triggered_patches"] == ["补丁一：承租人死亡"]


def test_tenant_death_without_cohabitant_coordinated_negation():
    output = adjudicate_deposit_v2(
        "承租人死亡，无共同居住人或共同经营人。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "承租人死亡，无共同居住人或共同经营人，租赁合同终止，押金应退还承租人的继承人。"
    assert output["facts"]["cohabitant_or_cooperator"] is False


def test_changed_circumstances_patch_only_says_can_claim():
    output = adjudicate_deposit_v2(
        "疫情封控属于订约时无法预见，也不属于商业风险，继续履行原租金明显不公平。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "可主张情势变更，建议先与对方协商减免租金或延长租期；协商不成可起诉请求变更或解除合同。"
    assert output["triggered_patches"] == ["补丁二：情势变更"]
    assert "必然胜诉" not in output["result"]


def test_changed_circumstances_incomplete_does_not_short_circuit():
    output = adjudicate_deposit_v2(
        "租客说疫情影响收入，想少交租金。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] != ["补丁二：情势变更"]
    assert output["conclusion"].startswith("事实要素不足")


def test_illegal_building_invalid_contract_patch():
    output = adjudicate_deposit_v2(
        "租赁房屋是违法建筑，没有建设工程规划许可证，租客要求退押金和剩余租金。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "租赁物为违法建筑，合同无效，押金应返还，使用费另计，损失可主张赔偿。"
    assert output["triggered_patches"] == ["补丁三：违法建筑"]
    assert "使用费另计" in output["result"]


def test_sublease_chain_uses_contract_privity():
    output = adjudicate_deposit_v2(
        "A租给B，B未经A同意转租给C，C造成房屋损坏，A想直接找C赔。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "转租链条断裂适用合同相对性原则：A向B主张，B向C追偿，互不穿透。B对A的责任不变；若B未经A同意擅自转租，A可解除与B的租赁合同。"
    assert output["triggered_patches"] == ["补丁四：转租链条断裂"]
    assert "押金结算" not in output["path"]


def test_landlord_death_contract_continues():
    output = adjudicate_deposit_v2(
        "房东去世，继承人要求租客搬走并拒绝继续履行合同。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "出租人死亡，合同由继承人继续履行，押金处理不受影响；继承人拒绝履行的，承租人可起诉要求继续履行或主张违约赔偿。"
    assert output["triggered_patches"] == ["补丁五：出租人死亡"]


def test_edge_patch_runs_after_procedure_review_but_before_deposit_tree():
    output = adjudicate_deposit_v2(
        "租房押金纠纷应该去哪里起诉？房东去世，继承人不认合同。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["补丁五：出租人死亡"]
    assert output["procedure_findings"] == ["租赁合同纠纷由房屋所在地人民法院处理"]
    assert output["path"][-1] == "补丁五：出租人死亡"
    assert "押金结算" not in output["path"]


def test_indefinite_lease_patch_short_circuits_before_deposit_tree():
    output = adjudicate_deposit_v2(
        "租赁合同固定期限已满，租客到期后继续居住，房东继续收租，双方没有签新合同。"
        "房东主张提前退租不退押金。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "租赁期满后双方未续签合同，但租客继续居住房屋、房东继续收租，原合同转为不定期租赁。任何一方可随时解除合同，但应提前合理期限（通常1个月）通知对方。押金退还按实际损坏情况处理，不适用提前退租违约金条款。"
    assert output["triggered_patches"] == ["不定期租赁"]
    assert output["path"][-1] == "补丁六：不定期租赁"
    assert "押金结算" not in output["path"]
    assert "触发补丁：不定期租赁" in output["result"]


def test_indefinite_lease_can_use_expired_contract_end_date():
    output = adjudicate_deposit_v2(
        "合同于2026年1月1日到期，租客到期后继续居住，房东没有提出异议，双方未签新合同。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["不定期租赁"]
    assert output["facts"]["fixed_term_expired"] is True
    assert output["facts"]["indefinite_lease"] is True


def test_incomplete_indefinite_lease_facts_do_not_trigger_patch():
    output = adjudicate_deposit_v2(
        "合同期满后，租客继续居住，房东继续收租。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] != ["不定期租赁"]
    assert output["facts"]["indefinite_lease"] is False


def test_third_party_intercept():
    output = adjudicate_deposit_v2("退租时邻居把门砸坏，房东要求租客赔押金。", today=date(2026, 7, 27))

    assert output["conclusion"] == "本案涉及侵权责任，非合同纠纷，不适用本合同裁判引擎"
    assert output["facts"]["has_third_party"] is True


def test_jurisdiction_question_returns_house_location_court():
    output = adjudicate_deposit_v2("租房押金纠纷应该去哪里起诉？", today=date(2026, 7, 27))

    assert output["conclusion"] == "租赁合同纠纷由房屋所在地人民法院处理"
    assert "管辖程序" in output["triggered_patches"]


def test_wife_signer_defendant_question():
    output = adjudicate_deposit_v2("租房合同由房东妻子代签，我应该告谁？", today=date(2026, 7, 27))

    assert output["conclusion"] == "应列房东妻子为被告，而非房东本人"
    assert output["facts"]["signer_not_landlord"] is True


def test_wife_signer_without_entity_facts_returns_defendant_result():
    output = adjudicate_deposit_v2("租房合同由房东妻子代签。", today=date(2026, 7, 27))

    assert output["conclusion"] == "应列房东妻子为被告，而非房东本人"
    assert "管辖程序" in output["triggered_patches"]


def test_contract_termination_for_serious_rent_arrears_short_circuits_deposit_tree():
    output = adjudicate_deposit_v2(
        "租客拖欠租金3期，房东要求解除合同并扣押金。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "合同依法解除，根据解除原因处理押金，违约方承担相应责任"
    assert "合同解除权" in output["triggered_patches"]
    assert "押金结算" not in output["path"]


def test_contract_termination_right_expires_after_one_year():
    output = adjudicate_deposit_v2(
        "租客擅自转租，房东2024年5月1日知道后一直没处理，现在要求解除合同。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "解除权已经消灭，不能再以该事由单方解除合同"
    assert "合同解除权" in output["triggered_patches"]


def test_lease_before_sale_tenant_can_stay():
    output = adjudicate_deposit_v2(
        "租赁期间出售房屋，新房主要求租客马上搬走。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "租赁合同对新房主继续有效，租客无需搬走，押金事宜仍按原合同执行"
    assert "买卖不破租赁" in output["triggered_patches"]


def test_sale_before_lease_invalid_and_tenant_can_claim_compensation():
    output = adjudicate_deposit_v2(
        "房东先卖后租，已经卖了还出租给租客，现在新业主不认可合同。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "租赁合同无效，租客可向原房东主张违约赔偿"
    assert "买卖不破租赁" in output["triggered_patches"]


def test_pre_delivery_leak_landlord_repairs_and_rent_reduction():
    output = adjudicate_deposit_v2(
        "房屋入住前漏水，租客入住后无法正常使用，要求房东处理。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "房东承担修复责任，租客可以主张减租"
    assert "房屋自身瑕疵" in output["triggered_patches"]


def test_demolition_ends_contract_and_returns_deposit():
    output = adjudicate_deposit_v2(
        "租赁期间房屋被政府征收，租客要求退押金。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "合同自动终止，押金全额退还，补偿款归房东"
    assert "房屋自身瑕疵" in output["triggered_patches"]


def test_limitation_period_intercept():
    output = adjudicate_deposit_v2(
        "租赁合同于2020年6月1日终止，租客现在起诉要求返还押金。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "诉讼时效已过，驳回请求"
    assert output["facts"]["contract_end_date"] == "2020-06-01"


def test_any_damage_clause_and_unproven_damage_returns_deposit():
    output = adjudicate_deposit_v2(
        "合同于2026年5月1日终止。房东称墙面损坏，合同写任何损坏均由租客赔偿，"
        "但房东无法证明是谁造成的。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "押金全额返还"
    assert any("扩大租客损坏赔偿责任" in patch for patch in output["triggered_patches"])


def test_agreed_deduction_over_130_percent_is_reduced_to_actual_loss():
    output = adjudicate_deposit_v2(
        "租客提前退租，合同约定提前退租扣押金2000元，实际损失1000元。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "提前退租按合同约定处理，扣除1000.00元后返还余额"
    assert any("百分之一百三十" in patch for patch in output["triggered_patches"])


def test_notified_defect_at_check_in_blocks_deduction():
    output = adjudicate_deposit_v2(
        "退租时房东以地板裂缝扣押金。该裂缝入住时告知房东，房东知情未异议。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "押金全额返还"
    assert any("入住时已告知瑕疵" in patch for patch in output["triggered_patches"])


def test_extracts_tenant_fault_and_amounts():
    facts = extract_facts("租客使用不当造成家具损坏，维修费800元，房东扣款900元。")

    assert facts.damage_reason == "tenant_fault"
    assert facts.actual_loss == 800
    assert facts.agreed_deduction == 900


def test_vehicle_lease_uses_same_core_tree_with_vehicle_config():
    output = adjudicate_deposit_v2(
        "车辆租期届满，承租人到期后仍然使用车辆，出租人继续收租，双方没有签新合同。"
        "出租人又主张提前返还扣押金。",
        today=date(2026, 7, 27),
        contract_type="vehicle",
    )

    assert output["triggered_patches"] == ["不定期租赁"]
    assert output["facts"]["contract_type"] == "vehicle"
    assert "车辆" in output["conclusion"]
    assert "不适用提前返还违约金条款" in output["conclusion"]
    assert "押金结算" not in output["path"]


def test_equipment_lease_uses_same_core_tree_with_equipment_config():
    output = adjudicate_deposit_v2(
        "设备交付前故障，承租方使用后无法正常运行，要求出租方维修并减租。",
        today=date(2026, 7, 27),
        contract_type="equipment",
    )

    assert output["triggered_patches"] == ["设备自身故障"]
    assert output["facts"]["contract_type"] == "equipment"
    assert output["conclusion"] == "出租方承担修复责任，承租方可以主张减租"


def test_vehicle_illegal_asset_patch_loaded_from_vehicle_config():
    output = adjudicate_deposit_v2(
        "出租的车辆是报废车，依法不能上路，承租人要求返还押金。",
        today=date(2026, 7, 27),
        contract_type="vehicle",
    )

    assert output["triggered_patches"] == ["补丁三：违法租赁标的"]
    assert output["conclusion"] == "租赁车辆依法不能上路或属于违法车辆，合同无效，押金应返还，已实际使用期间的使用费另计，损失可主张赔偿。"


def test_new_lease_type_extension_point_is_configuration_table():
    config = get_lease_config("equipment")

    assert config.key == "equipment"
    assert "indefinite_lease" in config.enabled_patches
    assert "设备" in config.get_terms("asset")


def test_each_configured_patch_declares_mount_position():
    for contract_type in ("house", "vehicle", "equipment"):
        config = get_lease_config(contract_type)

        assert config.patch_mounts
        for mount in config.patch_mounts:
            assert mount.patch_id
            assert mount.node_id
            assert mount.mount_mode in ("前置", "后置", "替换")


def test_vehicle_and_equipment_special_patches_have_full_metadata():
    required_patch_ids = {"V1", "V2", "V3", "V4", "E1", "E2", "E3"}
    mounts = [
        mount
        for contract_type in ("vehicle", "equipment")
        for mount in get_lease_config(contract_type).patch_mounts
        if mount.patch_id in required_patch_ids
    ]

    assert {mount.patch_id for mount in mounts} == required_patch_ids
    for mount in mounts:
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_vehicle_traffic_accident_patch_mounts_after_damage_cause():
    config = get_lease_config("vehicle")
    mount = next(mount for mount in config.patch_mounts if mount.patch_id == "traffic_accident_liability")

    assert mount.node_id == "damage_cause"
    assert mount.mount_mode == "后置"


def test_vehicle_traffic_accident_patch_runs_before_amount_calculation():
    output = adjudicate_deposit_v2(
        "车辆发生交通事故，对方全责，出租人仍要求扣押金3000元。",
        today=date(2026, 7, 27),
        contract_type="vehicle",
    )

    assert output["triggered_patches"] == ["交通事故责任"]
    assert output["facts"]["traffic_accident"] is True
    assert output["facts"]["traffic_accident_other_responsible"] is True
    assert output["conclusion"] == "交通事故由对方或第三方承担责任，出租人不得以该事故为由扣押金；出租人可向责任方或保险渠道追偿"


def test_vehicle_v1_stoppage_loss_after_amount_calculation():
    output = adjudicate_deposit_v2(
        "车辆因承租人造成损坏，正在维修，出租人主张停运损失。日租金300元，维修5天。",
        today=date(2026, 7, 27),
        contract_type="vehicle",
    )

    assert output["triggered_patches"] == ["停运损失"]
    assert output["facts"]["repair_days"] == 5
    assert output["facts"]["daily_rent"] == 300
    assert output["conclusion"] == "承租人承担停运损失 1500.00 元，计算依据为日租金300.00元 × 维修天数5天。"


def test_vehicle_v2_financing_lease_short_circuits_entry():
    output = adjudicate_deposit_v2(
        "双方签订以租代购合同，约定租赁期满后车辆所有权归承租人，承租人逾期支付租金。",
        today=date(2026, 7, 27),
        contract_type="vehicle",
    )

    assert output["triggered_patches"] == ["以租代购"]
    assert output["conclusion"] == "以租代购合同，适用融资租赁规则：所有权归出租人，违约可收回车辆，已付租金不予退还。"
    assert "押金结算" not in output["path"]


def test_vehicle_v3_lessor_driver_qualification_review():
    output = adjudicate_deposit_v2(
        "承租人无证驾驶造成事故，出租人未审查驾驶证。",
        today=date(2026, 7, 27),
        contract_type="vehicle",
    )

    assert output["triggered_patches"] == ["出租人审查义务"]
    assert output["facts"]["vehicle_no_driving_qualification"] is True
    assert output["conclusion"] == "出租人审查义务判断：未审查或明知无资格仍出租，过错成立，责任承担比例按出租人过错程度和损害原因确定。"


def test_vehicle_v4_contract_privity_for_actual_driver():
    output = adjudicate_deposit_v2(
        "承租人与出租人签了车辆租赁合同，车是朋友开的，承租人说车不是我开的，我不该赔。",
        today=date(2026, 7, 27),
        contract_type="vehicle",
    )

    assert output["triggered_patches"] == ["合同相对性原则例外-车辆"]
    assert output["conclusion"] == "合同相对性原则适用：承租人向出租人承担全部责任，可另行向实际使用人追偿。"


def test_equipment_e1_failure_to_prevent_loss_expansion():
    output = adjudicate_deposit_v2(
        "设备故障后承租方未及时通知出租方，仍继续使用，导致损失扩大，损失8000元。",
        today=date(2026, 7, 27),
        contract_type="equipment",
    )

    assert output["triggered_patches"] == ["承租人防止损失扩大义务"]
    assert output["conclusion"] == "承租人防止损失扩大义务：未履行，对扩大损失承担8000.00元。"


def test_equipment_e2_total_loss_rent_payment():
    output = adjudicate_deposit_v2(
        "设备在租赁期间因承租方保管不善未锁门被偷，设备完全灭失，灭失前租金2000元，损失10000元。",
        today=date(2026, 7, 27),
        contract_type="equipment",
    )

    assert output["triggered_patches"] == ["租赁物灭失后的租金支付"]
    assert output["conclusion"] == "设备灭失：灭失前已产生租金2000.00元仍需支付，未来租金不再支付，可归责于承租方，赔偿责任为10000.00元。"


def test_equipment_e3_actual_user_tort_liability():
    output = adjudicate_deposit_v2(
        "承租方签订设备租赁合同后交给第三人使用，第三人操作造成设备损毁。",
        today=date(2026, 7, 27),
        contract_type="equipment",
    )

    assert output["triggered_patches"] == ["实际使用人直接担责"]
    assert output["conclusion"] == "实际使用人侵权责任成立，出租人可向承租人主张合同责任，也可直接向实际使用人主张侵权责任。"
