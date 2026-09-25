"""The original input prior must not undo accepted document classification."""
import pytest

from review_v2.fact_routing import CURRENT_ROUTE, TYPE_STAGES, finalize, resolve


@pytest.mark.parametrize('prior', ['sale', 'service'])
def test_body_transaction_controls_dispatch_without_a_technology_title(prior):
    text = ('合作协议\n甲方授予乙方非独占专利实施许可，乙方可使用该专利制造产品，'
            '不得向第三方再许可。乙方按照产品净销售额的4%支付许可使用费。'
            '甲方交付设计图纸及操作手册，专利所有权仍归甲方。')
    route = resolve(text, prior)
    assert route.selected_type == prior
    assert route.resolved_type == 'technology'
    assert route.selection.resolution == 'DOCUMENT_OVERRIDE'
    assert route.domain.contract_family == 'TECHNOLOGY'


@pytest.mark.parametrize('bad_stage', [None, 'facts_pipeline', 'checklist', 'report'])
def test_reclassification_gate_validates_resolved_execution_not_input_prior(bad_stage):
    text = ('甲方授予乙方专利实施许可，乙方按销售额5%支付许可使用费。'
            '甲方提供设计图纸和技术指导，乙方无权转让专利权。')
    route = resolve(text, 'sale')
    assert route.resolved_type == 'technology'
    token = CURRENT_ROUTE.set(route)
    stages = dict(request='sale', canonical='technology', facts_pipeline='technology',
                  checklist='technology')
    if bad_stage and bad_stage != 'report':
        stages[bad_stage] = 'sale'
    stage_token = TYPE_STAGES.set(stages)
    try:
        result = finalize({'contract_type': 'sale' if bad_stage == 'report' else 'technology',
                           'release_quality_gate': {'status': 'REPORT_READY'}})
        assert result['release_quality_gate']['status'] == ('BLOCKED' if bad_stage else 'REPORT_READY')
    finally:
        TYPE_STAGES.reset(stage_token)
        CURRENT_ROUTE.reset(token)


@pytest.mark.parametrize('rights,consideration', [
    ('许可方（卖方）授予被许可方（买方）非独占专利实施许可，买方有权使用该专利制造产品，不得转让专利权。',
     '买方按合同产品销售额5%向卖方支付许可使用费，卖方应交付技术资料并提供技术指导。'),
    ('让与人（卖方）向受让人（买方）转让本项发明创造的全部专利申请权。买方取得专利申请权，卖方配合办理权利转移登记。',
     '专利申请权转让价款总额为一百万元，买方向卖方支付转让价款。卖方应交付技术资料及图纸，买方组织验收。'),
])
def test_transaction_rights_outrank_generic_buyer_seller_goods_vocabulary(rights, consideration):
    # This is the strong operative-model precedence case, not a test of
    # extracting an unspecified "technical transaction price".
    text = ('合作协议\n' + rights + '\n' + consideration + '\n'
            '买方使用本技术生产设备，技术资料记载产品名称及规格型号。')
    route = resolve(text, 'sale')
    assert route.resolved_type == 'technology'
    model = route.selection.classification_context['primary_transaction_model']
    assert model['dominant_family'] == 'TECHNOLOGY'


def test_goods_purchase_is_not_displaced_by_incidental_patent_words():
    text = ('设备采购合同。买方向卖方购买十台设备，型号A，每台单价五万元。'
            '卖方交付设备后买方支付货款，设备所有权转移给买方。'
            '卖方保证设备不侵犯第三方专利权，并提供安装技术服务。')
    route = resolve(text, 'sale')
    assert route.resolved_type == 'sale'
