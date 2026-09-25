"""Legal relation variants and nearby-but-unrelated counterexamples."""
from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.work_evidence import evidence_for,applicability
from review_v2.contract_references import analyze as references
from review_v2.penalty_base import analyze as penalties

@pytest.mark.parametrize('node,text,found',[
 ('personal_completion_main_work','未经定作人同意，承揽人不得将主要加工任务交由第三人完成。',True),
 ('main_subcontract_consent','未经定作方书面同意，承揽方不得把主要加工工作转交第三方完成。',True),
 ('main_subcontract_consent','未经定作方同意，不得向第三方披露图纸。',False),
 ('main_subcontract_consent','承揽方可将辅助工作分包。',False),
 ('quality_standard','主要加工尺寸公差为±0.08mm。',True),
 ('quality_standard','产品合格率不得低于99%。',True),
 ('quality_standard','表面处理膜厚不低于20μm。',True),
 ('quality_standard','违约金为合同总价的20%。',False),
 ('quality_standard','验收后20日内支付款项。',False),
 ('acceptance_period_method','定作人收到定作物后7个工作日内完成数量及外观验收。',True),
 ('acceptance_period_method','按照技术标准及确认封样作为验收标准。',True),
 ('acceptance_period_method','验收后5日内完成付款。',False),
 ('sample_attachment','以双方确认封样为准。',True),
 ('sample_attachment','双方以后另行讨论样品。',False),
 ('assistance_urge_extension','定作方未提供原材料，承揽方可以顺延工期。',True),
 ('assistance_urge_extension','承揽方设备故障，交付期限顺延。',False),
 ('material_result_custody','由于保管不善致使定作方提供的材料毁损，承揽方应赔偿损失。',True),
 ('customer_arbitrary_termination_before_completion','定作方因市场需求变化可以提前十日通知承揽方解除合同。',True),
 ('customer_arbitrary_termination_before_completion','定作方不得随时解除合同。',False),
 ('customer_arbitrary_termination_before_completion','承揽方若发生严重违约，定作方可以提前解除合同。',False),
 ('arbitrary_termination_loss_scope','定作人中途废止合同的，应承担专用材料实际损失。',True),
 ('arbitrary_termination_loss_scope','承揽方迟延交货应承担损失。',False),
])
def test_fact_relations(node,text,found):
    assert bool(evidence_for('work_'+node,parse_contract_clauses(text)))==found

def test_consent_gate_uses_the_same_evidence():
    clauses=parse_contract_clauses('未经定作方同意，承揽方不得将主要加工工作转交第三方完成。')
    hits=evidence_for('work_main_subcontract_consent',clauses)
    gate=applicability('work_main_subcontract_consent',clauses)
    assert gate['applicable'] and {e['evidence_id'] for e in hits}=={e['evidence_id'] for e in gate['trigger_evidence']}

@pytest.mark.parametrize('target,expected',[
 ('第七条 交付日期\n签收货物之日为实际交货日期。','VALID'),
 ('第七条 争议解决\n争议提交仲裁。','INVALID'),
 ('第八条 交付日期\n签收之日为实际交货日期。','INVALID'),
])
def test_reference_target_not_neighbor_notice(target,expected):
    text='第三条 材料\n材料不合格应通知定作方。\n交提材料日期计算，参照第七条执行。\n'+target+'\n第九条 责任\n七、违约赔偿。'
    assert references(parse_contract_clauses(text))['common_internal_references'][0]['status']==expected

@pytest.mark.parametrize('pricing,expected',[
 ('单价：人民币80元/件。合同总价：人民币8000元。','DETERMINABLE'),
 ('单价待另行协商。合同总价尚未确定。','UNDEFINED'),
])
def test_partial_price_formula(pricing,expected):
    rows=penalties(pricing+'不能交付的，按照不能交付部分价款总值的12%支付违约金。')
    assert rows and rows[0]['status']==expected

def test_current_work_file_is_unchanged_and_elements_are_separate():
    from layers.input_layer import InputLayer
    from review_v2.engine import review_contract_v2
    path=next((Path(__file__).resolve().parents[2]/'test_data').glob('85 *.docx'))
    result=review_contract_v2(InputLayer()._extract_from_docx_content(path.read_bytes()),'work',use_llm=False)
    rows={r['item_id']:r for r in result['items']}
    for key in ['W-03-01','W-03-02','W-07-01','W-07-03','W-11-02','W-06-03','W-09-01','W-09-02','COMMON-20-01','COMMON-21-01']:
        assert rows[key]['coverage_status']=='通过',key
    for key in ['W-04-03','W-04-04','W-06-04']:
        assert rows[key]['coverage_status']=='部分覆盖',key
        assert {r['status'] for r in rows[key]['coverage_elements']}=={'COVERED','MISSING'}
    for key in ['W-03-01','W-03-02','W-07-01','W-07-03','W-11-02','W-06-03','W-09-01','W-09-02']:
        for audit in rows[key]['decision_trace']['work_element_searches']:
            assert audit['result']=='FOUND' and audit['supporting_evidence']
            assert all(e.get('normalization_reason') for e in audit['supporting_evidence'])
    assert result['release_quality_gate']['status']=='REPORT_READY',result['release_quality_gate']['failures']
