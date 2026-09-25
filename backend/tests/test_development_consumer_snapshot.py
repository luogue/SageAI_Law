from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import (_atomic_requirement_family, _register_atomic_family_facts,
    extract_semantic_field_value)
from review_v2.contract_facts import ContractFactGraph
from review_v2.development_exit import development_exit_elements
from review_v2.material_disposition import extract_scoped_material_disposition_facts, material_disposition_elements
from review_v2.data_use_scope import data_use_permissions
from review_v2.obligation_detail_elements import confidentiality_detail_elements

TEXT=(Path(__file__).parent/'fixtures/round35_entrusted_development.txt').read_text(encoding='utf8')
CLAUSES=parse_contract_clauses(TEXT)

@pytest.mark.parametrize('family,key,status',[
 ('development_subject','project_identity','COVERED'),
 ('development_subject','functional_scope','COVERED'),
 ('development_subject','performance_scope','COVERED'),
 ('development_scope','commissioned_project_and_objective','COVERED'),
 ('development_scope','functional_and_technical_scope','COVERED'),
 ('development_scope','schedule_and_milestones','COVERED'),
 ('development_scope','acceptance','COVERED'),
 ('development_acceptance','acceptance_metrics','COVERED'),
 ('development_acceptance','acceptance_deadline','COVERED'),
 ('development_acceptance','rectification_obligation','COVERED'),
 ('development_acceptance','rectification_deadline','COVERED'),
 ('development_acceptance','reinspection_procedure','COVERED'),
 ('development_acceptance','test_report_delivery','MISSING'),
 ('development_acceptance','acceptance_dispute_verification','MISSING'),
 ('development_failure','no_fault_technical_risk_allocation','COVERED'),
 ('development_failure','failed_development_incurred_cost_settlement','COVERED'),
 ('development_failure','paid_fee_refund','MISSING'),
 ('development_creator','inventor_contribution_attribution','COVERED'),
 ('entrusted_patent','inventor_authorship','COVERED'),
 ('development_creator','creator_reward_arrangement','MISSING'),
 ('development_proof','employee_ownership_documents','PARTIALLY_COVERED'),
 ('development_proof','employee_ownership_document_obligation','COVERED'),
 ('confidentiality_detail','confidential_information_scope','COVERED'),
 ('confidentiality_detail','during_contract_confidentiality','COVERED'),
 ('confidentiality_detail','confidentiality_duration','COVERED'),
 ('confidentiality_detail','confidentiality_exceptions','COVERED'),
 ('confidentiality_detail','prior_notice_when_legally_permitted','COVERED')])
def test_current_atomic_sources(family,key,status):
    e=next(e for e in _atomic_requirement_family(family,CLAUSES) if e['element_id']==key)
    assert e['status']==status
    assert bool(e['supporting_evidence'])==(status!='MISSING')
    for s in e['supporting_evidence']:
        assert s['quote'] in next(c.text for c in CLAUSES if c.clause_id==s['clause_id'])

def test_same_semantics_share_keys_and_sources():
    by={f:{e['source_fact_key']:e for e in _atomic_requirement_family(f,CLAUSES)}
        for f in ('development_subject','development_scope','development_acceptance')}
    for key in ('project','functions','schedule'):
        a,b=(by[f]['technology.transaction.'+key] for f in ('development_subject','development_scope'))
        assert a['status']==b['status']=='COVERED'
        assert a['supporting_evidence']==b['supporting_evidence']
    assert by['development_acceptance']['technology.transaction.acceptance']['status']=='COVERED'

def test_verified_same_key_cannot_be_missing_in_any_consumer():
    from review_v2.contract_facts import canonical_fact_key
    g=ContractFactGraph()
    families=('development_subject','development_scope','development_acceptance','development_exit','entrusted_patent',
              'development_proof','development_creator','confidentiality_core','confidentiality_detail')
    for f in families:_register_atomic_family_facts(g,f,CLAUSES)
    for atoms in g.atomic_family_snapshots.values():
        for e in atoms:
            if g.facts.get(canonical_fact_key(e['source_fact_key'])):
                assert e['status']!='MISSING'

@pytest.mark.parametrize('text',[
 '第十条 发明人署名\n专利申请时应按照实际技术贡献确定发明人。',
 '完成人有权署名。',
 '实际完成人享有发明人署名权。'])
def test_attribution_is_shared_by_creator_and_patent_consumers(text):
    cs=parse_contract_clauses(text)
    creator=next(e for e in _atomic_requirement_family('development_creator',cs) if e['element_id']=='inventor_contribution_attribution')
    patent=next(e for e in _atomic_requirement_family('entrusted_patent',cs) if e['element_id']=='inventor_authorship')
    assert creator['status']==patent['status']=='COVERED'
    assert creator['source_fact_key']==patent['source_fact_key']=='technology.creator.attribution'
    assert {(s['clause_id'],s['quote']) for s in creator['supporting_evidence']} <= {(s['clause_id'],s['quote']) for s in patent['supporting_evidence']}

def test_source_heading_is_not_report_proposition():
    cs=parse_contract_clauses('第十条 发明人署名\n专利申请时应按照实际技术贡献确定发明人。')
    e=next(e for e in _atomic_requirement_family('entrusted_patent',cs) if e['element_id']=='inventor_authorship')
    assert '第十条' in e['supporting_evidence'][0]['quote']
    assert '第十条' not in e['proposition']
    assert '实际技术贡献' in e['proposition']

def test_snapshot_is_contract_local_and_has_exact_facts():
    g=ContractFactGraph()
    _register_atomic_family_facts(g,'development_acceptance',CLAUSES)
    g.freeze('test')
    assert g.atomic_family_snapshots['development_acceptance'][0]['status']=='COVERED'
    with pytest.raises(RuntimeError): _register_atomic_family_facts(g,'development_acceptance',CLAUSES)
    empty=ContractFactGraph()
    _register_atomic_family_facts(empty,'development_acceptance',parse_contract_clauses('双方未约定验收标准。'))
    assert empty.atomic_family_snapshots['development_acceptance'][0]['status']=='MISSING'

def test_registry_preserves_exact_raw_span_with_blank_lines():
    cs=parse_contract_clauses('第一条 验收\n原型准确率达到95%以上。\n\n乙方应在十个工作日内整改。')
    g=ContractFactGraph()
    raw=cs[0].raw_text
    g.add('test.original_span',raw,cs[0],source_span=raw)
    assert g.facts['test.original_span'][0].source_spans==[raw]

def test_payment_consequence_registered_before_freeze():
    g=ContractFactGraph();_register_atomic_family_facts(g,'development_exit',CLAUSES)
    assert g.facts.get('payment_delay_liability')
    e=next(e for e in g.atomic_family_snapshots['development_exit'] if e['element_id']=='payment_delay_liability')
    assert e['status']=='COVERED'

@pytest.mark.parametrize('actor',['甲方','乙方','开发方'])
def test_existing_termination_does_not_erase_other_trigger_gap(actor):
    cs=parse_contract_clauses('第一条 项目退出\n守约方可以解除合同。\n合同未明确：\n'+actor+'在长期无法继续开发时是否享有解除权。')
    e=next(e for e in development_exit_elements(cs) if e['element_id']=='development_termination_mechanism')
    assert e['status']=='PARTIALLY_COVERED'
    assert e['supporting_evidence'] and actor in e['residual_gap']
    assert e['explicit_absence_evidence']

@pytest.mark.parametrize('trigger',['甲方未按期支付开发费用','委托方逾期付款','甲方延迟支付价款'])
@pytest.mark.parametrize('separator',['：\n','：','，'])
def test_payment_event_and_consequence_remain_together(trigger,separator):
    e=next(e for e in development_exit_elements(parse_contract_clauses(trigger+separator+'每迟延一日按未付金额支付违约金。'))
           if e['element_id']=='payment_delay_liability')
    assert e['status']=='COVERED'

@pytest.mark.parametrize('intro',['双方应对以下信息保密：','双方应对下列资料保密：'])
def test_confidential_scope_list_and_missing_neighbour(intro):
    cs=parse_contract_clauses('第一条 保密\n'+intro+'\n生产数据；\n源代码。\n双方未约定保密期限。')
    rows={e['element_id']:e for e in confidentiality_detail_elements(cs,extract_field=extract_semantic_field_value)}
    assert rows['confidential_information_scope']['status']=='COVERED'
    assert rows['during_contract_confidentiality']['status']=='COVERED'
    assert rows['confidentiality_duration']['status']=='MISSING'

@pytest.mark.parametrize('event',['项目完成','合同终止','项目结束'])
@pytest.mark.parametrize('days',['15','十'])
def test_disposal_lists_keep_actor_deadline_and_object(event,days):
    cs=parse_contract_clauses(event+'时：\n双方应在'+days+'个工作日内：\n返还项目资料；\n删除电子副本；\n删除可恢复备份；\n销毁无需依法保存的纸质资料；\n出具书面删除或销毁确认。')
    fs=extract_scoped_material_disposition_facts(cs)
    assert not any(f['action']=='retain' for f in fs)
    assert all(e['status']=='COVERED' for e in material_disposition_elements(cs,actor='双方'))

@pytest.mark.parametrize('text',[
 '乙方不得将甲方生产数据用于其他客户项目。',
 '乙方可以保留不包含甲方数据的通用工具。甲方应提供模型训练工具。',
 '乙方可以将不包含甲方生产数据的通用工具用于模型训练。',
 '乙方可以将不含甲方数据的通用开发框架用于其他客户项目。',
 '乙方应删除电子备份。双方未约定是否允许乙方将甲方数据用于其他客户。',
 '乙方可以将匿名化统计信息用于改善通用分析方法。',
 '双方未约定：\n乙方可将甲方原始数据用于模型训练。'])
def test_no_cross_proposition_data_permission(text):
    assert not [p for p in data_use_permissions(parse_contract_clauses(text))
                if p['external_use'] and p['data_object']=='COUNTERPARTY_DATA']

@pytest.mark.parametrize('purpose',['模型训练','算法训练','其他客户项目'])
def test_real_data_permission_survives(purpose):
    p=data_use_permissions(parse_contract_clauses('乙方可以将甲方生产数据用于'+purpose+'。'))
    assert len(p)==1 and p[0]['external_use'] and p[0]['data_object']=='COUNTERPARTY_DATA'

def test_proof_promise_does_not_prove_provided_document():
    es=_atomic_requirement_family('development_proof',parse_contract_clauses('乙方应确保员工签署职务成果归属文件。'))
    states={e['element_id']:e['status'] for e in es}
    assert states['employee_ownership_document_obligation']=='COVERED'
    assert states['employee_ownership_documents']=='MISSING'

def test_current_no_false_data_reuse_and_all_disposal_components():
    assert not [p for p in data_use_permissions(CLAUSES) if p['external_use'] and p['data_object']=='COUNTERPARTY_DATA']
    assert all(e['status']=='COVERED' for e in material_disposition_elements(CLAUSES,actor='双方'))
