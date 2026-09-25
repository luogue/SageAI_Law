from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_elements import elements


@pytest.mark.parametrize('condition',['如需','若需','如需要','若需要'])
def test_conditional_component_arrangement_is_scoped_and_searchable(condition):
    text=f'技术服务合同\n第一条 第三方组件\n项目中{condition}使用第三方软件、开源组件，乙方应事先告知甲方。'
    rows={e['element_id']:e for e in elements('component_inventory',parse_contract_clauses(text))}
    assert rows['third_party_component_dependency']['status']=='COVERED'
    for key in ('third_party_component_inventory','third_party_license_and_authorization'):
        assert rows[key]['status']=='MISSING'
        assert rows[key]['search_targets']
        assert rows[key]['source_fact_key']


def test_component_inventory_and_authorization_are_not_always_missing():
    text='技术服务合同\n第一条 第三方组件\n乙方可以使用第三方软件。乙方应提供第三方软件清单。乙方应提供对应许可证。'
    assert all(e['status']=='COVERED' for e in elements('component_inventory',parse_contract_clauses(text)))


@pytest.mark.parametrize('party',['甲方','乙方'])
def test_current_service_final_gate_and_narrative(party):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text=(Path(__file__).parent/'fixtures/round37_service.txt').read_text(encoding='utf8')
    r=review_contract_v2(text,'technology',use_llm=False,profile=UserRiskProfile(user_identity=party))
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
    items={i['item_id']:i for i in r['items']}
    claim=items['TC-12-02']
    assert len(claim['legal_consequence_if_missing'].strip('。； '))>10
    assert {e['element_id'] for e in claim['coverage_elements']} >= {'notification_requirement','defense_control'}
    for rule in ('TC-03-04','TC-13-02'):
        inventory=next(e for e in items[rule]['coverage_elements'] if e['element_id']=='third_party_component_inventory')
        assert inventory['status']=='MISSING'
        assert inventory['search_targets']
