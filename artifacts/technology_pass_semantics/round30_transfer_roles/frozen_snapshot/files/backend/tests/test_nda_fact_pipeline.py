import pytest
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('prior,flow',[
 ('乙方能够证明在从甲方取得之前已经合法知悉的信息不属于保密信息。','甲方拥有研发资料，乙方因任职可以接触该资料并负保密义务。'),
 ('受领信息以前受领人已合法持有的资料除外。','公司持有客户资料，员工履行工作职责时接触资料并承诺保守秘密。'),
])
def test_nda_semantic_facts(monkeypatch,prior,flow):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.engine import review_contract_v2
 text='保密协议\n第一条\n甲方：星辰公司。乙方：林某。\n'+flow+'\n第二条\n保密信息包括研发资料、客户资料。公开信息除外。独立研发信息除外。从不负保密义务第三方合法取得的信息除外。'+prior+'\n第三条\n不得披露或擅自使用资料。保密义务至信息公开。离职时返还资料。泄密应停止侵害并赔偿损失。违反保密义务支付20000元违约金。'
 vals=[('nda.party_one','星辰公司','甲方：星辰公司。'),('nda.party_two','林某','乙方：林某。'),('nda.employment_relationship',True,flow),('nda.information_flow','甲方→乙方',flow),('nda.protected_information','研发资料、客户资料','保密信息包括研发资料、客户资料。'),('nda.exception_public',True,'公开信息除外。'),('nda.exception_prior',True,prior),('nda.exception_independent',True,'独立研发信息除外。'),('nda.exception_third_party',True,'从不负保密义务第三方合法取得的信息除外。'),('nda.use_restriction','限制披露及使用','不得披露或擅自使用资料。'),('nda.duration','至公开','保密义务至信息公开。'),('nda.return','离职返还','离职时返还资料。'),('nda.remedies','停止侵害及赔偿','泄密应停止侵害并赔偿损失。'),('penalties.obligations',{'scope':'CONFIDENTIALITY','imposed':True,'amount_text':'20000'},'违反保密义务支付20000元违约金。')]
 cs=parse_contract_clauses(text);monkeypatch.setattr(p,'extract',lambda *a,**k:packet(cs,[fact(cs,c,v,q) for c,v,q in vals]));monkeypatch.setattr(p,'verify',verified_packet)
 r=review_contract_v2(text,'confidentiality');rows={i['item_id']:i for i in r['items']}
 assert rows['NDA-03-01']['coverage_status']=='通过'
 assert [e['element_id'] for e in rows['NDA-01-01']['coverage_elements'] if e['status']=='MISSING']==['nda_exception_mandatory']
 assert rows['EMP-14-01']['coverage_status']=='风险条款'
 assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']

@pytest.mark.parametrize('concept,value,conflict',[('non_compete.access_capability',True,False),('non_compete.actual_access',True,False),('non_compete.duration_months',12,True)])
def test_absence_context_is_not_obligation(concept,value,conflict):
 from review_v2.employment_fact_store import FactStore
 from review_v2.fact_verification import verified_store
 from review_v2.fact_validation import FactExtractionError
 from review_v2.employment_fact_schema import ABSENCE_SCOPES
 text='第一条\n员工接触商业秘密。竞业期限12个月。';cs=parse_contract_clauses(text)
 s=FactStore(text,cs,packet(cs,[fact(cs,concept,value,cs[-1].text)]));v=verified_packet(cs,s)
 v['verification']['absence_audits']=[{'concept':'non_compete.arrangement','result':'ABSENT','reason':'已完成全文审计，无竞业义务。','reviewed_clause_ids':[c.clause_id for c in cs],'searched_concepts':['non_compete.arrangement',*ABSENCE_SCOPES['non_compete.arrangement']]}]
 if conflict:
  with pytest.raises(FactExtractionError,match='CONFLICTING_ABSENCE_AUDIT'):verified_store(s,v)
 else:
  checked=verified_store(s,v);assert checked.applicability('employment_noncompete_scope')[0] is False
  assert checked.get(concept)
