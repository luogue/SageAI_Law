import json
import pytest
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('employment',[True,False])
@pytest.mark.parametrize('complete',[True,False])
def test_report_uses_confidentiality_issue_domain(monkeypatch,employment,complete):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.engine import review_contract_v2
 parts={'public':'公开信息除外。','independent':'独立开发信息除外。','mandatory':'依法强制披露信息除外。','prior':'取得前已合法持有的信息除外。','third_party':'从无保密义务第三方合法取得的信息除外。'}
 used=list(parts) if complete else ['public','independent','mandatory']
 relation='双方为劳动用工关系。' if employment else '双方仅为商业合作主体，不存在劳动关系。'
 text='保密协议\n第一条\n甲方甲公司，乙方乙主体。'+relation+'甲方向乙方提供保密信息。保密信息为技术方案。'+''.join(parts[k] for k in used)+'\n第二条\n不得擅自披露资料。保密至公开。终止返还资料。泄露资料应赔偿损失。'
 vals=[('nda.party_one','甲公司','甲方甲公司，乙方乙主体。'),('nda.party_two','乙主体','甲方甲公司，乙方乙主体。'),('nda.employment_relationship',employment,relation),('nda.information_flow','甲方→乙方','甲方向乙方提供保密信息。'),('nda.protected_information','技术方案','保密信息为技术方案。'),('nda.use_restriction','不得擅自披露','不得擅自披露资料。'),('nda.duration','至公开','保密至公开。'),('nda.return','终止返还','终止返还资料。'),('nda.remedies','赔偿损失','泄露资料应赔偿损失。')]+[('nda.exception_'+k,True,parts[k]) for k in used]
 # Complete fixture also includes release by the information owner's written consent.
 if complete:text+='经信息所有方书面同意解除保密义务的信息除外。'
 cs=parse_contract_clauses(text)
 monkeypatch.setattr(p,'extract',lambda *a,**kw:packet(cs,[fact(cs,c,v,q) for c,v,q in vals]))
 monkeypatch.setattr(p,'verify',verified_packet)
 r=review_contract_v2(text,'confidentiality');row=next(i for i in r['items'] if i['item_id']=='NDA-01-01')
 assert row['coverage_status']==('通过' if complete else '部分覆盖')
 missing={e['element_id'] for e in row['coverage_elements'] if e['status']=='MISSING'}
 assert missing==(set() if complete else {'nda_exception_prior','nda_exception_third_party'})
 for k in ('legal_consequence_if_missing','suggested_clause_example','risk_point_description'):
  assert not any(w in str(row.get(k,'')) for w in ('劳动关系','劳动权利','竞业补偿'))
 if not complete:assert '本应排除的信息' in json.dumps(row,ensure_ascii=False)
 assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']


@pytest.mark.parametrize('node',['employment_secret_scope','employment_secret_duty','confidentiality_parties','confidentiality_remedies'])
def test_shared_confidentiality_nodes_do_not_inherit_employment_fallback(node):
 from types import SimpleNamespace
 from review_v2.engine import _specific_gap_consequence
 item=SimpleNamespace(node_id=node,coverage_status='部分覆盖',decision_trace={})
 consequence=_specific_gap_consequence(item,'本项约定')
 assert '劳动关系' not in consequence
 assert item.decision_trace['field_provenance']['legal_consequence_source']=='rule_domain:confidentiality'

def test_actual_employment_rule_keeps_its_domain():
 from types import SimpleNamespace
 from review_v2.engine import _specific_gap_consequence
 item=SimpleNamespace(node_id='employment_insurance',coverage_status='部分覆盖',decision_trace={})
 assert '劳动关系' in _specific_gap_consequence(item,'参保义务')
