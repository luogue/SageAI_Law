"""Production-route legal ON/OFF and source-bound record requirements."""
from copy import deepcopy
from dataclasses import replace
from types import SimpleNamespace
import pytest
from review_v2.legal_enrichment_boundary import enrich, enrichment_mode, business_snapshot
from review_v2.shared_fact_concepts import pool, register
from review_v2.clause_parser import parse_contract_clauses
from review_v2.safekeeping_contract_checklist import SAFEKEEPING_REVIEW_CHECKLIST
from review_v2.priority_contract_review import judge
from review_v2 import llm_semantic_reviewer as llm
from test_legal_basis_production_path import upload


def business(item):
    keys=('status','coverage_status','risk_level','risk_severity','action_priority','issue_type',
          'applicability','coverage_elements','risk_point_description','formal_recommendation',
          'review_judgment','action_suggestion','residual_risk','needs_manual_review')
    data={k:deepcopy(item.get(k)) for k in keys}
    data['evidence']=[{k:e.get(k) for k in ('evidence_id','clause_id','quote','supports','supporting_element_ids','source_span')}
                      for e in item.get('evidence_clauses',[])]
    data['search_audit']=deepcopy(item['decision_trace'].get('element_absence_searches'))
    for key in ('shared_concept_facts','semantic_requirements','element_evidence_truth','narrative_elements'):
        data[key]=deepcopy(item['decision_trace'].get(key))
    return data


@pytest.fixture(scope='module')
def ab():
    with enrichment_mode(False): a=upload()
    with enrichment_mode(True): b=upload()
    return a,b


def test_production_all_fifty_business_results_identical(ab):
    a,b=ab
    assert len(a['items'])==len(b['items'])==50
    for x,y in zip(a['items'],b['items']):
        assert x['item_id']==y['item_id']
        assert business(x)==business(y),x['item_id']
    assert b['release_quality_gate']['status']=='REPORT_READY'


@pytest.mark.parametrize('rid',['D-07-03','D-11-03','D-12-02'])
def test_actual_file_positive_atoms_survive_legal_stage(ab,rid):
    for report in ab:
        row=next(i for i in report['items'] if i['item_id']==rid)
        assert row['coverage_status']=='通过'
        boundary=row['decision_trace']['legal_enrichment_boundary']
        assert boundary['hash_before']==boundary['hash_after']
        assert all(e['status']=='COVERED' and e['evidence_ids'] for e in row['coverage_elements'])
        assert all(a['result']=='FOUND' for a in row['decision_trace']['element_absence_searches'])


@pytest.mark.parametrize('node,text,expected',[
 ('safekeeping_loss_cause_evidence','接收方应建立货物出入库记录，并保存监控资料六十天。','通过'),
 ('safekeeping_loss_cause_evidence','接收方应建立物品交接台账。','部分覆盖'),
 ('safekeeping_return_procedure','接收方应出具双方签字的交接单。委托人取回时须出示凭证。','通过'),
 ('safekeeping_photo_video_attachment','验收后出具验收记录。接收方应留存照片记录备查。','通过'),
 ('safekeeping_photo_video_attachment','验收后出具验收记录。','部分覆盖'),
 ('safekeeping_loss_cause_evidence','仓库设有摄像设备。','缺失'),
])
def test_reusable_business_concepts_on_off(node,text,expected):
    rule=next(c for c in SAFEKEEPING_REVIEW_CHECKLIST if c.node_id==node)
    clauses=parse_contract_clauses(text)
    for enabled in (False,True):
        with enrichment_mode(enabled):
            assert judge(rule,clauses).coverage_status==expected


@pytest.mark.parametrize('concept,text',[
 ('movement_records','无需建立出入库记录。'),
 ('retained_visual_records','无需保存视频监控资料。'),
 ('signed_handover_record','双方通过邮箱签收法律通知。'),
 ('retrieval_workflow','甲方可随时领取货物。'),
 ('acceptance_record','物品包装外观完好。'),
])
def test_related_words_and_negation_do_not_create_facts(concept,text):
    assert not pool(parse_contract_clauses(text),[concept])[concept]


def test_shared_records_reused_with_independent_identity():
    rule=next(c for c in SAFEKEEPING_REVIEW_CHECKLIST if c.node_id=='safekeeping_loss_cause_evidence')
    other=replace(rule,item_id='NEW-RECORD',node_id='independent_record_review')
    register(other.node_id,other.fact_concepts)
    clauses=parse_contract_clauses('接收方应建立货物交接记录，并保存监控录像一年。')
    facts=pool(clauses,rule.fact_concepts)
    assert judge(rule,clauses,shared_facts=facts).evidence_clauses==judge(other,clauses,shared_facts=facts).evidence_clauses


@pytest.mark.parametrize('field',['coverage_status','coverage_elements','evidence_clauses','applicability'])
def test_illegal_business_mutation_is_blocked_not_committed(field):
    item=SimpleNamespace(item_id='ANY',coverage_status='通过',coverage_elements=[{'status':'COVERED'}],
        evidence_clauses=[{'clause_id':'real'}],applicability={'applicable':True},
        legal_basis_index='',legal_references=[],decision_trace={})
    before=business_snapshot(item)
    def bad(items,checkpoints):
        setattr(items[0],field,'corrupt')
        return {'status':'REPORT_READY','failures':[]}
    result=enrich([item],[],bad)
    assert result['status']=='BLOCKED'
    assert business_snapshot(item)==before
    assert item.decision_trace['legal_enrichment_boundary']['changed_fields']==[field]


@pytest.mark.parametrize('builder',['single','batch'])
def test_legal_metadata_cannot_change_business_prompt(builder):
    rule=SAFEKEEPING_REVIEW_CHECKLIST[0]
    clauses=parse_contract_clauses('合同成立后按约交接物品。')
    initial=llm.judge_checkpoint(rule,clauses)
    def prompt(checkpoint):
        if builder=='single':return llm._build_prompt(checkpoint,clauses,initial)
        return llm._build_batch_prompt([{'checkpoint':checkpoint,'candidates':clauses,'rule_judgment':initial}])
    changed=replace(rule,legal_basis='unrelated law',legal_basis_topics=('different_proposition',),legal_basis_domain='other')
    assert prompt(rule)==prompt(changed)


def test_legal_trace_does_not_alias_business_elements():
    from review_v2.legal_basis_trace import snapshot
    rule=SAFEKEEPING_REVIEW_CHECKLIST[0]
    item=SimpleNamespace(node_id=rule.node_id,legal_basis_index='',legal_references=[],
         coverage_elements=[{'status':'COVERED'}],decision_trace={})
    snapshot([item],'BEFORE',[rule])
    item.coverage_elements[0]['status']='MISSING'
    assert item.decision_trace['legal_basis_runtime_trace']['required_elements'][0]['status']=='COVERED'


def test_legal_stage_cannot_rebuild_checkpoint_requirements():
    rule=SAFEKEEPING_REVIEW_CHECKLIST[0]
    original=rule.pass_criteria
    def bad(items,checkpoints):
        object.__setattr__(checkpoints[0],'pass_criteria','a legal proposition replacing the business requirement')
        return {'status':'REPORT_READY','failures':[]}
    gate=enrich([], [rule],bad)
    assert gate['status']=='BLOCKED'
    assert gate['failures'][0]['requirement']=='LEGAL_ENRICHMENT_CHECKPOINT_IMMUTABILITY'
    assert rule.pass_criteria==original


def test_legal_stage_cannot_remove_business_rows():
    rule=SAFEKEEPING_REVIEW_CHECKLIST[0]
    def bad(items,checkpoints):
        checkpoints.clear()
        return {'status':'REPORT_READY','failures':[]}
    assert enrich([], [rule],bad)['status']=='BLOCKED'


@pytest.mark.parametrize('conflict',['rule','element','search'])
def test_positive_fact_cannot_become_missing(conflict):
    from review_v2.legal_enrichment_boundary import positive_consistency
    row={'item_id':'ANY','coverage_status':'缺失' if conflict=='rule' else '通过',
         'coverage_elements':[{'element_id':'record','status':'MISSING' if conflict=='element' else 'COVERED','evidence_ids':['source']}],
         'decision_trace':{'shared_concept_facts':{'record':[{'clause_id':'source','quote':'应留存记录'}]},
           'element_absence_searches':[{'element_id':'record','result':'NOT_FOUND' if conflict=='search' else 'FOUND'}]}}
    assert positive_consistency([row])['status']=='BLOCKED'
