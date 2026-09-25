from itertools import permutations
from types import SimpleNamespace
import pytest
from review_v2.legal_basis_selection import select,ARTICLE_METADATA

def evaluate(topics,status='通过'):
    item=SimpleNamespace(coverage_status=status,legal_basis_index='《民法典》第510条、第577条',
        decision_trace={'legal_basis_runtime_trace':{'stages':[]}})
    # Deliberately arbitrary identity: selection cannot depend on a rule id/title.
    checkpoint=SimpleNamespace(item_id='arbitrary',legal_basis_topics=topics,legal_basis=item.legal_basis_index)
    select(item,checkpoint)
    return item.decision_trace['legal_basis_runtime_trace']

@pytest.mark.parametrize('topics',list(permutations(('liquidated_damages_calculation','general_breach_liability','unclear_contract_terms'))))
def test_special_beats_general_independent_of_candidate_order(topics):
    t=evaluate(topics)
    assert t['primary_basis']==['第585条']
    assert t['selected_basis'].startswith('《中华人民共和国民法典》第585条')
    assert '第510条' not in t['selected_basis']
    assert t['selection_complete'] and t['special_over_general_passed']

def test_custody_fee_obligation_and_time_are_both_primary():
    t=evaluate(('performance_cooperation','unclear_contract_terms','custody_fee_obligation','remuneration_payment'))
    assert t['primary_basis']==['第889条','第902条']
    assert t['secondary_basis']==['第509条']

@pytest.mark.parametrize('status,trigger',[('通过',False),('部分覆盖',True),('缺失',True)])
def test_supplementary_trigger_never_beats_special(status,trigger):
    t=evaluate(('unclear_contract_terms','liquidated_damages_calculation','general_breach_liability'),status)
    c=next(c for c in t['candidate_articles'] if c['article']=='第510条')
    assert c['trigger_satisfied'] is trigger
    assert ('第510条' in t['selected_basis']) is trigger
    assert t['primary_basis']==['第585条']

def test_no_topic_overlap_cannot_recall_special_law():
    t=evaluate(('performance_cooperation',))
    assert '第585条' not in t['selected_basis']
    assert '第889条' not in t['selected_basis']

def test_article_metadata_describes_normative_object_not_just_words():
    for article in ('第585条','第577条','第510条','第889条','第902条'):
        assert {'article_id','legal_domain','contract_type','proposition_tags','normative_object','trigger_conditions','effect_type','specificity_level'} <= ARTICLE_METADATA[article].keys()
    assert ARTICLE_METADATA['第510条']['trigger_conditions']==['unclear_terms']
