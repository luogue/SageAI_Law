"""Tests for the agency-contract adjudication engine."""

from datetime import date

from adjudicate.agency_configs import get_agency_config
from adjudicate.agency_engine import adjudicate_agency


TODAY = date(2026, 7, 27)


def test_agency_config_declares_core_mapping_and_patches():
    config = get_agency_config("agency")

    assert config.key == "agency"
    assert config.fact_mapping["合同主体"] == "委托人/受托人"
    assert config.fact_mapping["核心义务"] == "按指示处理委托事务（受托人）/ 支付报酬和费用（委托人）"
    assert config.fact_mapping["归责原则"] == "有偿=一般过失；无偿=故意或重大过失；越权=绝对责任"
    assert set(config.reused_modules) == {"管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"}

    patch_ids = {mount.patch_id for mount in config.patch_mounts}
    assert patch_ids == {f"A{i}" for i in range(1, 17)}
    for mount in config.patch_mounts:
        assert mount.node_id
        assert mount.mount_mode
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_agency_jurisdiction_question():
    output = adjudicate_agency("委托合同纠纷去哪里起诉？", today=TODAY)

    assert output["triggered_patches"] == ["管辖程序"]
    assert output["conclusion"] == "委托合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理"
    assert output["facts"]["asks_jurisdiction"] is True


def test_a1_classifies_substance_as_agency():
    output = adjudicate_agency("双方对合同性质争议，合同名为服务协议，实质是受托人代为处理委托事务。", today=TODAY)

    assert output["triggered_patches"] == ["委托合同性质认定"]
    assert output["conclusion"] == "按实质内容认定为委托合同，继续适用委托合同裁判规则。"


def test_a1_diverts_contracting_substance():
    output = adjudicate_agency("合同名为委托合同，但核心是完成工作成果并交付工作成果。", today=TODAY)

    assert output["triggered_patches"] == ["委托合同性质认定"]
    assert output["conclusion"] == "本案更接近承揽合同，应适用承揽合同裁判规则。"


def test_a14_invalid_unreasonable_format_clause():
    output = adjudicate_agency("委托合同使用格式条款，未提示说明，并免除受托人重大过失责任。", today=TODAY)

    assert output["triggered_patches"] == ["格式条款效力审查"]
    assert output["conclusion"] == "格式条款无效，不能作为免除主要义务、免除重大过错责任或不合理加重对方责任的依据。"


def test_principal_reimburses_necessary_expenses():
    output = adjudicate_agency("受托人为处理委托事务垫付必要费用3000元，要求委托人偿还。", today=TODAY)

    assert output["conclusion"] == "委托人应偿还必要费用并支付相应利息；非必要或不合理扩大支出的费用不予支持。"
    assert output["path"][-1] == "委托人义务"


def test_a15_remuneration_when_unfinished_not_trustee_fault():
    output = adjudicate_agency("有偿委托事务因客观原因不能完成，不可归责于受托人，受托人请求相应报酬。", today=TODAY)

    assert output["triggered_patches"] == ["不可归责受托人的报酬请求"]
    assert output["conclusion"] == "委托人应向受托人支付相应报酬；具体数额按已完成事务比例、约定报酬和实际履行情况核定。"


def test_a8_separate_entrustment_caused_loss():
    output = adjudicate_agency("委托人又委托他人处理同一事务，另行委托造成损失5000元。", today=TODAY)

    assert output["triggered_patches"] == ["委托人另行委托"]
    assert output["conclusion"] == "另行委托造成原受托人损失的，委托人应赔偿相应损失。"


def test_a11_instruction_breach():
    output = adjudicate_agency("有偿委托中，受托人未按指示办理事务，造成实际损失5000元。", today=TODAY)

    assert output["triggered_patches"] == ["受托人指示遵守义务"]
    assert output["conclusion"] == "受托人违反指示义务，应赔偿因此造成的损失，已识别损失为 5000.00 元。"


def test_a4_self_agency_without_consent_is_ineffective():
    output = adjudicate_agency("受托人与自己交易，构成自己代理，委托人没有同意或追认。", today=TODAY)

    assert output["triggered_patches"] == ["自己代理与双方代理"]
    assert output["conclusion"] == "自己代理或双方代理未经同意或追认的，对委托人不发生效力；造成损失的，受托人应赔偿。"


def test_a12_report_duty_breach():
    output = adjudicate_agency("受托人拒绝报告委托事务处理情况，并隐瞒情况。", today=TODAY)

    assert output["triggered_patches"] == ["受托人报告义务"]
    assert output["conclusion"] == "受托人违反报告义务；因此造成委托人损失的，应承担赔偿责任。"


def test_a13_property_transfer_duty_breach():
    output = adjudicate_agency("受托人处理委托事务取得财产10000元后拒不转交给委托人。", today=TODAY)

    assert output["triggered_patches"] == ["取得财产转交义务"]
    assert output["conclusion"] == "受托人应返还取得财产并赔偿损失，已识别金额为 10000.00 元。"


def test_a9_joint_trustees_joint_liability():
    output = adjudicate_agency("两个受托人共同处理委托事务，造成损失后委托人要求他们承担责任。", today=TODAY)

    assert output["triggered_patches"] == ["共同受托人连带责任"]
    assert output["conclusion"] == "共同受托人对委托人承担连带责任；内部责任可按各自过错和约定另行分担。"


def test_a2_over_authority_direct_liability():
    output = adjudicate_agency("受托人超越权限处理事务，造成实际损失8000元。", today=TODAY)

    assert output["triggered_patches"] == ["有偿/无偿委托责任标准"]
    assert output["conclusion"] == "受托人越权造成损失的，应直接向委托人赔偿，已识别损失为 8000.00 元。"


def test_a2_unpaid_agency_without_gross_fault_not_liable():
    output = adjudicate_agency("无偿委托中事务处理造成损失，受托人能证明无故意或重大过失，仅一般过失。", today=TODAY)

    assert output["triggered_patches"] == ["有偿/无偿委托责任标准"]
    assert output["conclusion"] == "无偿委托中未能识别受托人故意或重大过失，委托人要求受托人赔偿的请求不予支持。"


def test_a5_intervention_right_with_a16_defense():
    output = adjudicate_agency(
        "受托人以自己名义签约，第三人不知道委托关系，第三人违约不履行，受托人披露第三人，委托人主张介入权，第三人继续主张原有抗辩。",
        today=TODAY,
    )

    assert output["triggered_patches"] == ["委托人介入权", "介入权/选择权后的抗辩延续"]
    assert output["conclusion"] == "委托人介入权成立，可以向第三人主张受托人原本享有的合同权利；第三人原可向受托人主张的抗辩继续存在。"


def test_a6_third_party_choice_right():
    output = adjudicate_agency(
        "受托人以自己名义签约，第三人不知道委托关系，委托人违约导致不能履行，受托人披露委托人，第三人选择委托人主张。",
        today=TODAY,
    )

    assert output["triggered_patches"] == ["第三人选择权"]
    assert output["conclusion"] == "第三人选择权成立，可以选择委托人主张权利；一经选定不得变更，原合同抗辩继续存在。"


def test_a7_paid_arbitrary_termination_compensates_expected_profit():
    output = adjudicate_agency("有偿委托中委托人任意解除委托，解除造成损失，实际损失2000元，可得利益3000元。", today=TODAY)

    assert output["triggered_patches"] == ["任意解除权及赔偿范围"]
    assert output["conclusion"] == "有偿委托解除造成损失的，解除方赔偿直接损失和可得利益，已识别金额为 5000.00 元。"


def test_a3_unauthorized_sub_entrustment_full_responsibility():
    output = adjudicate_agency("受托人未经委托人同意擅自转委托，把事务交给第三人办理。", today=TODAY)

    assert output["triggered_patches"] == ["转委托责任"]
    assert output["conclusion"] == "未经委托人同意或追认的转委托不符合规则，受托人应对第三人的行为向委托人承担责任。"


def test_a10_continue_after_principal_death_to_protect_interest():
    output = adjudicate_agency("委托人死亡，停止会损害委托人利益，受托人必须继续处理等待继承人接手。", today=TODAY)

    assert output["triggered_patches"] == ["终止后的继续处理义务"]
    assert output["conclusion"] == "委托合同虽发生终止事由，但立即停止会损害委托人利益，受托人应继续处理至继承人、遗产管理人或清算人接手。"
