"""Tests for the service-contract adjudication engine."""

from datetime import date

from adjudicate.service_configs import get_service_config
from adjudicate.service_engine import adjudicate_service


TODAY = date(2026, 7, 27)


def test_service_config_declares_core_mapping_and_patches():
    config = get_service_config("service")

    assert config.key == "service"
    assert config.fact_mapping["合同主体"] == "服务提供方/服务接受方"
    assert config.fact_mapping["核心义务"] == "按约定提供服务（服务方）/ 支付服务费（接受方）"
    assert config.fact_mapping["核心争议"] == "服务是否提供 → 服务质量是否达标 → 合同能否解除 → 如何退款"
    assert set(config.reused_modules) == {"管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"}

    patch_ids = {mount.patch_id for mount in config.patch_mounts}
    assert patch_ids == {f"SVC{i}" for i in range(1, 14)}
    for mount in config.patch_mounts:
        assert mount.node_id
        assert mount.mount_mode
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_service_jurisdiction_question():
    output = adjudicate_service("服务合同纠纷去哪里起诉？", today=TODAY)

    assert output["triggered_patches"] == ["管辖程序"]
    assert output["conclusion"] == "服务合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理"
    assert output["facts"]["asks_jurisdiction"] is True


def test_svc1_classifies_as_service_contract():
    output = adjudicate_service("双方对合同性质争议，实质是提供服务行为，顾客重在接受服务过程。", today=TODAY)

    assert output["triggered_patches"] == ["服务合同性质认定"]
    assert output["conclusion"] == "合同性质认定为服务合同，适用服务合同裁判规则。"


def test_svc1_diverts_work_result_to_contracting():
    output = adjudicate_service("合同名为服务合同，但核心是完成工作成果并交付成果。", today=TODAY)

    assert output["triggered_patches"] == ["服务合同性质认定"]
    assert output["conclusion"] == "合同性质认定为承揽合同，适用承揽合同裁判规则。"


def test_svc4_no_refund_format_clause_invalid():
    output = adjudicate_service("培训服务合同为模板合同，写明费用不退、不退不换。", today=TODAY)

    assert output["triggered_patches"] == ["不退不换格式条款效力"]
    assert output["conclusion"] == "‘不退不换’格式条款无效，消费者可以依法主张退款。"


def test_svc11_platform_major_terms_change_without_consent_invalid():
    output = adjudicate_service("互联网平台单方变更服务条款，减少用户重大权益，没有提示说明，也没有用户同意。", today=TODAY)

    assert output["triggered_patches"] == ["互联网平台服务条款变更"]
    assert output["conclusion"] == "平台服务条款变更无效，对用户不发生效力。"


def test_svc12_business_transfer_refusal():
    output = adjudicate_service("健身房门店转让给第三方，新店不认卡，受让方拒绝服务。", today=TODAY)

    assert output["triggered_patches"] == ["预付式消费合同转让责任"]
    assert output["conclusion"] == "经营者转让后，受让方应继续履行合同；受让方拒绝服务的，消费者可向转让方和受让方主张相应责任。"


def test_svc2_and_svc10_prepaid_closed_malicious_refund():
    output = adjudicate_service("消费者预付式消费办卡充值5000元，健身房停业并恶意逃避退款。", today=TODAY)

    assert output["triggered_patches"] == ["预付式消费特殊规则", "恶意逃避退款惩罚性赔偿"]
    assert output["conclusion"] == "本案为预付式消费，经营者未按约定提供服务，应退还预付款 5000.00 元，并适用惩罚性赔偿；赔偿金额为 15000.00 元。"


def test_svc6_unilateral_service_change_is_breach():
    output = adjudicate_service("培训机构单方变更课程内容，降低服务标准，消费者没有同意。", today=TODAY)

    assert output["triggered_patches"] == ["服务方单方变更服务内容"]
    assert output["conclusion"] == "服务提供方单方变更服务内容构成违约，服务接受方可以要求继续履行原约定或解除合同并赔偿损失。"


def test_svc7_provider_no_qualification():
    output = adjudicate_service("美容服务方没有资质，实际服务人员也与约定不符。", today=TODAY)

    assert output["triggered_patches"] == ["服务方资质缺失或人员不符"]
    assert output["conclusion"] == "服务方不具备法定资质或实际服务人员不符合约定，构成违约；服务接受方可以解除合同并要求退款、赔偿损失。"


def test_svc9_receiver_reason_termination_deducts_loss():
    output = adjudicate_service("消费者自身原因搬家要求退费，未消费金额3000元，经营者合理损失500元。", today=TODAY)

    assert output["triggered_patches"] == ["服务接受方原因解除损失赔偿"]
    assert output["conclusion"] == "服务接受方因自身原因解除合同，应承担合理损失 500.00 元，扣除后退还余额 2500.00 元。"


def test_unprovided_service_refund():
    output = adjudicate_service("服务方完全未提供服务，未提供服务金额2000元，消费者要求退款。", today=TODAY)

    assert output["conclusion"] == "服务方完全未提供服务，服务接受方可以解除合同并要求全额退款 2000.00 元。"


def test_svc13_guaranteed_result_not_achieved():
    output = adjudicate_service("培训合同承诺保过、不过全退，学员没有通过，且不是学员原因。", today=TODAY)

    assert output["triggered_patches"] == ["保过包过承诺"]
    assert output["conclusion"] == "‘保过’承诺构成合同义务，目标未实现，服务方应承担违约责任，服务接受方可以要求退款或赔偿。"


def test_svc5_quality_nonconform_breach():
    output = adjudicate_service("服务质量不达标，不符合合同约定标准，消费者要求减少费用。", today=TODAY)

    assert output["triggered_patches"] == ["服务质量标准认定"]
    assert output["conclusion"] == "服务质量不符合约定或行业标准，服务提供方构成违约；服务接受方可以要求继续履行、采取补救措施、减少费用或赔偿损失。"


def test_svc3_health_change_termination_no_breach():
    output = adjudicate_service("消费者因身体健康原因无法继续健身，有医院证明和医嘱，订约时无法预见，继续履行明显不公平，未使用余额4000元。", today=TODAY)

    assert output["triggered_patches"] == ["身体健康原因解除"]
    assert output["conclusion"] == "消费者因身体健康原因解除合同，不构成违约，不应承担违约金，应退还款项 4000.00 元。"


def test_svc8_indefinite_service_with_notice_valid():
    output = adjudicate_service("长期持续服务未约定服务期限，消费者提前一个月通知解除。", today=TODAY)

    assert output["triggered_patches"] == ["不定期继续性服务合同任意解除"]
    assert output["conclusion"] == "不定期继续性服务合同，当事人可以随时解除，已在合理期限前通知，解除有效；退款按实际接受服务情况计算。"
