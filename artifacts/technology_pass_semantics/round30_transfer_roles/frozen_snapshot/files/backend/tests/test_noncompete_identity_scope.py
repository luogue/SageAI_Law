import pytest
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('kind,address,expected',[('non_compete',False,'通过'),('labor',False,'部分覆盖'),('labor',True,'通过')])
def test_identity_scope(monkeypatch,kind,address,expected):
 from review_v2 import employment_fact_pipeline as pipeline
 from review_v2.engine import review_contract_v2
 q='甲方：乙科技有限公司；住所：南城路八号；法定代表人：刘明。\n乙方：周禾；身份证：110101199001011234。'
 if address:q+='\n劳动者住址：北城路九号。'
 text=('竞业限制协议' if kind=='non_compete' else '劳动合同')+'\n第一条 主体\n'+q
 cs=parse_contract_clauses(text)
 vals=[('identity.employer_name','乙科技有限公司','甲方：乙科技有限公司'),('identity.employer_address','南城路八号','住所：南城路八号'),('identity.employer_representative','刘明','法定代表人：刘明'),('identity.worker_name','周禾','乙方：周禾'),('identity.worker_id','110101199001011234','身份证：110101199001011234')]
 if address:vals.append(('identity.worker_address','北城路九号','劳动者住址：北城路九号'))
 monkeypatch.setattr(pipeline,'extract',lambda *a,**k:packet(cs,[fact(cs,c,v,e) for c,v,e in vals]))
 monkeypatch.setattr(pipeline,'verify',verified_packet)
 r=review_contract_v2(text,kind);i=next(x for x in r['items'] if x['item_id']=='EMP-01-01')
 assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
 assert i['coverage_status']==expected
 addr=[x for x in i['coverage_elements'] if x['element_id']=='employment_identity_4']
 if kind=='non_compete':
  assert not addr and '劳动者住址' not in i['risk_point_description']
  assert r['employment_classification']['subtype']=='NON_COMPETE'
 elif not address:assert addr and all(x['status']!='COVERED' for x in addr)
