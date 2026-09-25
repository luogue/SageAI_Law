"""Tests for the loan-contract adjudication engine."""

from datetime import date

from adjudicate.loan_configs import get_loan_config
from adjudicate.loan_engine import adjudicate_loan


TODAY = date(2026, 7, 27)


def test_loan_config_declares_core_mapping_and_patches():
    config = get_loan_config("loan")

    assert config.key == "loan"
    assert config.fact_mapping["合同主体"] == "贷款人/借款人/保证人"
    assert config.fact_mapping["核心义务"] == "提供借款（贷款人）/ 返还借款并支付利息（借款人）"
    assert config.fact_mapping["归责原则"] == "严格责任（未按约还款即构成违约）"
    assert set(config.reused_modules) == {"管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"}

    patch_ids = {mount.patch_id for mount in config.patch_mounts}
    assert patch_ids == {f"L{i}" for i in range(1, 16)}
    for mount in config.patch_mounts:
        assert mount.node_id
        assert mount.mount_mode
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_loan_jurisdiction_question():
    output = adjudicate_loan("借款合同纠纷去哪里起诉？", today=TODAY)

    assert output["triggered_patches"] == ["管辖程序"]
    assert output["conclusion"] == "借款合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同履行地未约定或约定不明的，以接受货币一方所在地为合同履行地"
    assert output["facts"]["asks_jurisdiction"] is True


def test_l9_limitation_interrupted_by_collection():
    output = adjudicate_loan("借款人主张超过诉讼时效，但出借人在时效内书面催收，借款人也承诺还款。", today=TODAY)

    assert output["triggered_patches"] == ["诉讼时效中断"]
    assert output["conclusion"] == "诉讼时效已中断，应从中断事由发生之日起重新计算；是否超过三年需结合中断日期核定。"


def test_l1_financial_loan_classification():
    output = adjudicate_loan("银行作为金融机构向借款人发放贷款，双方争议利息规则。", today=TODAY)

    assert output["triggered_patches"] == ["金融借款与民间借贷区分"]
    assert output["conclusion"] == "本案为金融借款，适用民法典借款合同章和金融监管规定，不适用民间借贷司法解释的LPR四倍规则。"


def test_l11_sale_security_treated_as_private_lending():
    output = adjudicate_loan("双方以买卖合同作为担保，借款到期后出借人请求履行买卖合同并直接过户。", today=TODAY)

    assert output["triggered_patches"] == ["以买卖担保借款"]
    assert output["conclusion"] == "本案实质为民间借贷，应按民间借贷法律关系审理；出借人可就担保财产依法申请拍卖、变卖受偿，不能直接请求过户。"


def test_l14_natural_person_loan_not_formed_without_delivery():
    output = adjudicate_loan("自然人之间借款，贷款人没有放款，借款人没有收到借款。", today=TODAY)

    assert output["triggered_patches"] == ["自然人间借款成立时间"]
    assert output["conclusion"] == "自然人间借款合同，贷款人未提供借款，合同未成立；借款人无返还本金和支付利息义务。"


def test_l7_professional_lender_invalidates_contract():
    output = adjudicate_loan("借款人主张出借人为职业放贷人，出借人多次反复向不特定对象经常性放贷，具有营业性放贷目的。", today=TODAY)

    assert output["triggered_patches"] == ["职业放贷人认定"]
    assert output["conclusion"] == "借款合同无效，借款人应返还实际取得的本金；约定高息不予支持，资金占用损失可按LPR标准核定。"


def test_l15_enterprise_loan_for_business_need_is_valid():
    output = adjudicate_loan("公司之间借款用于生产经营需要，没有套取金融机构贷款转贷。", today=TODAY)

    assert output["triggered_patches"] == ["企业间借贷效力"]
    assert output["conclusion"] == "企业间借贷有效，应按合同约定和法定利率上限处理本金、利息及违约责任。"


def test_l13_lender_not_provide_loan():
    output = adjudicate_loan("贷款人未按约定提供借款，未足额放款，造成借款人损失20000元。", today=TODAY)

    assert output["triggered_patches"] == ["贷款人未按约定提供借款"]
    assert output["conclusion"] == "贷款人未足额提供借款的，应按实际提供金额认定本金；造成借款人损失的，应承担赔偿责任。"


def test_l5_transfer_record_only_borrowing_established_without_rebuttal():
    output = adjudicate_loan("原告仅有转账凭证，没有借条只有转账，被告说不是借款但不能证明其他用途。", today=TODAY)

    assert output["triggered_patches"] == ["仅有转账凭证的借贷关系认定"]
    assert output["conclusion"] == "仅有转账凭证，被告不能证明转账系其他用途，借贷关系成立。"


def test_l10_voucher_without_creditor_holder_qualified():
    output = adjudicate_loan("原告持有借条，但借条没有写出借人，债权凭证未载明债权人，被告没有反证。", today=TODAY)

    assert output["triggered_patches"] == ["债权凭证未载明债权人"]
    assert output["conclusion"] == "债权凭证未载明债权人，持有人可初步证明债权人资格；被告不能提出充分反证的，原告债权人资格成立。"


def test_l2_deducted_interest_sets_actual_principal():
    output = adjudicate_loan("借款合同中借条金额100万元，借款人实际收到95万元，5万元为砍头息。", today=TODAY)

    assert output["triggered_patches"] == ["砍头息认定"]
    assert output["conclusion"] == "存在砍头息 50000.00 元，本金应认定为实际借款数额 950000.00 元，利息也应以该实际借款数额为基数计算。"


def test_l4_partial_repayment_offsets_cost_interest_principal():
    output = adjudicate_loan("借款人部分还款50000元，不足以清偿。实现债权费用10000元，利息20000元，尚欠本金100000元。", today=TODAY)

    assert output["triggered_patches"] == ["还款冲抵顺序"]
    assert output["conclusion"] == "部分还款 50000.00 元，按费用、利息、本金顺序冲抵，尚欠本金 80000.00 元。"


def test_l8_spousal_debt_not_joint_when_beyond_family_need():
    output = adjudicate_loan("出借人主张夫妻共同债务，但该大额借款明显超出家庭日常生活，未用于夫妻共同生活。", today=TODAY)

    assert output["triggered_patches"] == ["夫妻共同债务认定"]
    assert output["conclusion"] == "本案借款超出家庭日常生活需要，且未识别到共同生活、共同经营或共同意思表示，不属于夫妻共同债务，不应由夫妻双方共同偿还。"


def test_l12_misuse_loan_allows_early_recovery():
    output = adjudicate_loan("借款人未按约定用途使用借款，将经营周转借款挪作他用。", today=TODAY)

    assert output["triggered_patches"] == ["未按约定用途使用借款"]
    assert output["conclusion"] == "借款人未按约定用途使用借款，贷款人可以停止发放借款、提前收回借款或解除合同。"


def test_l3_interest_cap_adjusts_excessive_rate():
    output = adjudicate_loan("借款合同约定年利率18%，一年期LPR为3.85%。", today=TODAY)

    assert output["triggered_patches"] == ["利率上限审查"]
    assert output["conclusion"] == "合同成立时一年期LPR为 3.85%，四倍为 15.40%。约定利率 18.00% 超过上限，应按 15.40% 计算。"


def test_no_interest_agreed_denies_period_interest():
    output = adjudicate_loan("借款合同没有约定利息，出借人要求支付借期内利息。", today=TODAY)

    assert output["conclusion"] == "出借人主张借期内利息的，不予支持；逾期后的资金占用损失可依法另行审查。"


def test_early_repayment_without_forbidden_clause_not_breach():
    output = adjudicate_loan("借款人提前还款，合同没有禁止提前还款的约定。", today=TODAY)

    assert output["conclusion"] == "提前还款不构成违约，除另有约定外，应按实际借款期间计算利息。"


def test_extension_requires_lender_consent():
    output = adjudicate_loan("借款人在还款期限届满前申请展期，出借人同意展期。", today=TODAY)

    assert output["conclusion"] == "借款展期成立，应按展期协议履行；展期利率有约定按约定，无约定参照原合同利率，但不得超过法定上限。"


def test_l6_old_for_new_same_guarantor_bears_liability():
    output = adjudicate_loan("存在保证人，借新还旧，新旧贷为同一保证人。", today=TODAY)

    assert output["triggered_patches"] == ["借新还旧中保证人责任"]
    assert output["conclusion"] == "借新还旧，保证人知道或新贷与旧贷为同一保证人，保证人应承担保证责任。"


def test_general_guarantee_when_unclear():
    output = adjudicate_loan("借款合同有保证人，但没有约定保证方式。", today=TODAY)

    assert output["conclusion"] == "保证方式为一般保证，或未约定、约定不明而依法按一般保证处理；保证人享有先诉抗辩权。"
