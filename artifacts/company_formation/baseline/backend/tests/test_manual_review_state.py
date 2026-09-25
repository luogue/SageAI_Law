from copy import deepcopy
from types import SimpleNamespace
from pathlib import Path
import pytest
from review_v2.report_presentation import verification_projection
from review_v2.report_statistics import report_status, coverage_counts, requires_verification, statistics_gate


def make(status, manual=False, unresolved=False, node='generic'):
    return SimpleNamespace(item_id=node, node_id=node, coverage_status=status, status=status,
        needs_manual_review=manual, coverage_elements=[{'status':'COVERED','proposition':'合同文本义务'}] +
            ([{'status':'CONDITION_UNRESOLVED','verification_instruction':'核实实际履行条件'}] if unresolved else []),
        action_suggestion='已覆盖，无需修改', narrative_state={}, decision_trace={}, risk_severity='NONE')


@pytest.mark.parametrize('status,manual,unresolved,expected', [
    ('通过',False,False,'通过'), ('通过',True,False,'待核验'),
    ('通过',False,True,'待核验'), ('部分覆盖',True,True,'部分覆盖'),
    ('INSUFFICIENT_CONTEXT',False,False,'待核验'), ('不适用',True,False,'不适用'),
    ('风险条款',True,True,'风险条款')])
@pytest.mark.parametrize('node',['employment_safety','construction_qualification','loan_authority'])
def test_generic_state_precedence_and_nonmutation(status,manual,unresolved,expected,node):
    original=make(status,manual,unresolved,node)
    before=deepcopy(original.__dict__)
    projected=verification_projection(original)
    assert report_status(projected)==expected
    assert original.__dict__==before
    assert projected.risk_severity==original.risk_severity
    if status=='通过' and expected=='待核验':
        assert '无需修改' not in projected.reasoning_summary
        assert '人工核验' in projected.action_suggestion
    if expected=='不适用':
        assert not projected.needs_manual_review


def test_statistics_and_detail_close_and_reject_raw_pass():
    items=[make('通过'),make('通过',unresolved=True),make('部分覆盖',True),make('风险条款',True),make('不适用')]
    rows=[{'item_id':str(n),'coverage_status':report_status(i),'needs_manual_review':requires_verification(i),'risk_level':'低'} for n,i in enumerate(items)]
    manual=[{'item_id':r['item_id'],'source_rules':[r['item_id']]} for r in rows if r['needs_manual_review']]
    report={'items':rows,'all_rule_statuses':rows,'all_items_count':5,'coverage_summary':coverage_counts(items),
      'summary':{'高':0,'中':0,'低':4},'manual_review_items':manual,
      'manual_review_summary':{'manual_review_count':3},'final_overview_summary':{'manual_review':3,'major_risk':0,'medium_risk':0,'low_risk':0},
      'risk_finding_summary':{'人工复核':3,'重大风险':0,'中等风险':0,'低风险':0},'risk_findings':[]}
    assert sum(report['coverage_summary'].values())==5
    assert statistics_gate(report)['status']=='REPORT_READY'
    report['items'][1]['coverage_status']='通过'
    assert any(f['requirement']=='MANUAL_REVIEW_PASS_CONTRADICTION' for f in statistics_gate(report)['failures'])


def test_current_labor_report_has_one_pending_no_new_risk():
    from test_employment_fact_semantics import review, item
    text=(Path(__file__).resolve().parents[2]/'artifacts/task_term_after/normalized_input.txt').read_text(encoding='utf-8')
    result=review(text)
    row=item(result,'EMP-08-01')
    assert row['coverage_status']=='待核验'
    assert '劳动防护和安全培训' in row['reasoning_summary']
    assert '职业病危害' in row['reasoning_summary']
    detail=result['result'].split('劳动保护与职业危害（EMP-08-01）',1)[1].split('---',1)[0]
    assert '已覆盖，无需修改' not in detail
    assert '覆盖状态：待核验' in detail
    assert result['coverage_summary']=={'通过':14,'待核验':1,'不适用':5}
    assert result['manual_review_summary']['manual_review_count']==1
    assert result['final_disposition_summary']['actionable']==0
    assert result['statistics_consistency_gate']['status']=='REPORT_READY'
    assert result['release_quality_gate']['status']=='REPORT_READY'
