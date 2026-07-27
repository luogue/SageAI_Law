"""Tests for the sale-contract adjudication engine."""

from datetime import date

from adjudicate.sale_configs import get_sale_config
from adjudicate.sale_engine import adjudicate_sale


def test_sale_config_declares_core_mapping_and_patches():
    config = get_sale_config("sale")

    assert config.key == "sale"
    assert config.fact_mapping["合同主体"] == "出卖人/买受人"
    assert config.fact_mapping["核心义务"] == "转移所有权 + 交付符合质量要求的标的物"
    assert config.fact_mapping["三重逻辑"] == "所有权转移 + 风险负担 + 瑕疵担保"
    assert set(config.reused_modules) == {"管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"}

    patch_ids = {mount.patch_id for mount in config.patch_mounts}
    assert patch_ids == {f"B{i}" for i in range(1, 16)}
    for mount in config.patch_mounts:
        assert mount.node_id
        assert mount.mount_mode
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_sale_jurisdiction_question_uses_defendant_or_performance_place():
    output = adjudicate_sale(
        "买卖合同纠纷去哪里起诉？",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "买卖合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理"
    assert output["triggered_patches"] == ["管辖程序"]
    assert output["facts"]["asks_jurisdiction"] is True


def test_no_written_contract_can_be_proven_by_delivery_documents():
    output = adjudicate_sale(
        "双方没有书面合同，但有送货单、收货单、结算单和发票，长期按交易习惯供货。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "虽无书面合同，但存在送货单、收货单、结算单、发票或交易习惯等证据，可以综合认定买卖合同关系成立。"
    assert output["path"][-1] == "合同成立认定"


def test_b13_vat_invoice_alone_does_not_prove_delivery():
    output = adjudicate_sale(
        "出卖人仅以增值税专用发票和税款抵扣资料证明已经交付，买受人不认可。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["发票的证明效力"]
    assert output["conclusion"] == "发票不足以单独证明交付事实；出卖人应补充送货单、签收单、物流记录、对账单等其他证据。"


def test_b7_exemption_clause_invalid_if_seller_intentionally_hid_defect():
    output = adjudicate_sale(
        "合同有免除瑕疵责任的免责条款，但出卖人明知瑕疵仍故意隐瞒瑕疵。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["免责条款效力审查"]
    assert output["conclusion"] == "免责条款无效，出卖人仍应承担瑕疵担保责任。"


def test_b1_installment_sale_allows_full_price_or_rescission():
    output = adjudicate_sale(
        "分期付款买卖，总价款10000元，买受人未支付到期价款3000元，出卖人经催告后买受人在合理期限内仍未支付。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["分期付款买卖"]
    assert output["conclusion"] == "分期付款买卖，未付价款达总价款的 30%，经催告后仍未在合理期限内支付，出卖人可以请求支付全部价款或解除合同；解除时可请求支付标的物使用费。"


def test_b2_b14_trial_sale_risk_stays_with_seller():
    output = adjudicate_sale(
        "试用买卖中，试用期间标的物毁损灭失。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["试用买卖", "试用买卖中标的物风险负担"]
    assert output["conclusion"] == "试用期内标的物毁损灭失，风险由出卖人承担，买受人不因该风险负担付款义务。"


def test_b3_title_retention_retake_after_urge():
    output = adjudicate_sale(
        "买卖合同约定所有权保留，未付清前所有权属于出卖人，买受人未支付价款，出卖人催告后仍未付款，出卖人要求取回标的物，所有权保留已登记。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["所有权保留买卖"]
    assert "出卖人有权取回标的物" in output["conclusion"]
    assert output["facts"]["title_retention"] is True


def test_b4_sample_sale_nonconformity_is_quality_breach():
    output = adjudicate_sale(
        "双方凭样品买卖，样品已封存，交付标的物与样品不一致。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["凭样品买卖"]
    assert output["conclusion"] == "凭样品买卖，交付标的物不符合样品质量，出卖人应承担相应违约责任。"


def test_b15_tender_or_auction_uses_special_law():
    output = adjudicate_sale(
        "该买卖通过招标投标方式订立，双方对中标后的交付义务发生争议。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["招标投标买卖与拍卖"]
    assert output["conclusion"] == "招标投标买卖/拍卖，优先适用招标投标法、拍卖法等特别法规定；特别法未规定的，适用民法典买卖合同一般规则。"


def test_b11_electronic_information_product_delivery():
    output = adjudicate_sale(
        "买卖标的物为电子信息产品软件，交付方式约定不明，买受人已经收到激活码和权利凭证。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["电子信息产品的交付"]
    assert output["conclusion"] == "电子信息产品，交付方式约定不明，自买受人收到电子信息产品或权利凭证时完成交付。"


def test_b12_over_delivery_rejected_custody_fee_paid_by_seller():
    output = adjudicate_sale(
        "出卖人多交标的物，买受人拒绝接收多交部分并代为保管，代为保管费用500元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["多交标的物的处理"]
    assert output["conclusion"] == "多交标的物，买受人拒绝接收多交部分的，可以代为保管，合理保管费用由出卖人承担；已识别费用为 500.00 元。"


def test_risk_before_delivery_is_borne_by_seller():
    output = adjudicate_sale(
        "标的物交付前毁损灭失，双方争议风险负担。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "标的物交付前毁损、灭失的风险由出卖人承担。"
    assert output["path"][-1] == "风险负担"


def test_risk_after_delivery_does_not_bar_quality_claim():
    output = adjudicate_sale(
        "标的物交付后毁损，但买受人同时主张质量不合格。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "标的物交付后毁损、灭失的风险由买受人承担；但若同时存在质量瑕疵，买受人仍可请求出卖人承担违约责任。"


def test_b10_signed_delivery_note_presumes_external_inspection():
    output = adjudicate_sale(
        "货物质量不合格，买受人已签收送货单，送货单载明数量型号规格，争议属于外观瑕疵。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["买受人检验期限的推定"]
    assert output["conclusion"] == "买受人已签收载明数量/型号/规格的单据，推定已完成数量和外观瑕疵检验；买受人可提供相反证据推翻，该推定不适用于隐蔽瑕疵。"


def test_b9_serious_quality_defect_allows_rescission():
    output = adjudicate_sale(
        "买受人收到货物后发现质量不合格，及时通知出卖人，严重瑕疵导致无法正常使用，合同目的不能实现，买受人要求解除合同。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["合同目的不能实现的认定标准"]
    assert output["conclusion"] == "合同目的已落空，买受人可以拒绝接受标的物或解除合同，并请求返还价款、赔偿损失。"


def test_b6_and_b8_expected_profit_and_deposit_penalty_relation():
    output = adjudicate_sale(
        "货物质量不合格，买受人在合理期限内通知，要求赔偿损失，实际损失2000元，可得利益3000元，可预见范围6000元，合同同时约定定金和违约金。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["可得利益损失", "定金与违约金、赔偿损失的关系"]
    assert "可得利益损失成立，赔偿金额为实际损失与可得利益合计 5000.00 元" in output["conclusion"]
    assert "定金与违约金不可以并用" in output["conclusion"]


def test_right_defect_allows_suspending_payment_or_rescission():
    output = adjudicate_sale(
        "标的物存在第三人抵押权，买受人订立合同时不知道，出卖人未提供担保。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "买受人可以中止支付相应价款；第三人权利导致买受人无法取得所有权的，买受人可以解除合同并请求赔偿。"
    assert output["path"][-1] == "权利瑕疵"


def test_b5_multi_sale_priority_by_first_delivery():
    output = adjudicate_sale(
        "出卖人一物数卖，将同一标的物卖给多人，其中买受人甲先行受领交付。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["一物数卖"]
    assert output["conclusion"] == "一物数卖，按先行受领交付规则，应向先受领交付的买受人履行交付或确认履行效果；其他买受人可向出卖人主张违约责任。"
