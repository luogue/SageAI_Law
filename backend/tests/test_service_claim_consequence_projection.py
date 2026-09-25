from pathlib import Path

import pytest
from review_v2.technology_service_elements import claim_missing_consequence


def test_claim_consequence_uses_only_unresolved_dimensions():
    rows=[{'element_id':'notification_requirement'}, {'element_id':'refund_remedy'}]
    consequence=claim_missing_consequence(rows)
    assert '证据保全' in consequence
    assert '已付款项' in consequence
    assert '律师选择' not in consequence
    assert '可能对相关义务的履行及权利行使产生争议' not in consequence


@pytest.mark.parametrize('party',['甲方','乙方'])
def test_current_service_consequence_survives_finding_and_markdown(party):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text=(Path(__file__).parent/'fixtures/round37_service.txt').read_text(encoding='utf8')
    report=review_contract_v2(text,'technology',use_llm=False,profile=UserRiskProfile(user_identity=party))
    assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']
    item=next(i for i in report['items'] if i['item_id']=='TC-12-02')
    assert item['coverage_status']=='缺失'
    consequence=item['legal_consequence_if_missing']
    assert all(term in consequence for term in ('索赔','通知','抗辩','费用','授权','退款'))
    assert '可能对相关义务的履行及权利行使产生争议' not in consequence
    finding=next(f for f in report['risk_findings'] if 'TC-12-02' in f['source_review_ids'])
    assert finding['consequence']==consequence
    detail=report['result'].split('（TC-12-02）',1)[1].split('\n---',1)[0]
    assert '- 【缺失的法律后果】：'+consequence in detail
    assert report['release_quality_gate']['gate_results']['REVIEW_EVIDENCE_ELEMENT_MISMATCH']=='PASS'
