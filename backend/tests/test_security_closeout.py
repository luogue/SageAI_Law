import pytest
from review_v2.requirement_kinds import partition,EXTERNAL_FACT_TYPES

@pytest.mark.parametrize('kind',sorted(EXTERNAL_FACT_TYPES))
def test_external_statements_never_verify_world(kind):
 terms, assessments=partition([{'element_id':'test','proposition':'甲方确认已经完成','fact_type':kind}])
 assert not terms
 assert assessments[0]['external_fact_status']=='UNVERIFIED'

@pytest.mark.parametrize('text',[
 '本合同由法定代表人或授权代理人签署。',
 '甲方应提交股东会决议及授权材料。',
 '甲方确认已取得股东会批准。',
 '附件一：股东会决议。全体股东同意本次担保。',
 '双方签订合同。',
])
def test_authority_text_does_not_verify_external_facts(text):
 from review_v2.engine import review_contract_v2
 r=review_contract_v2('动产质押合同\n出质人：甲有限公司\n主合同债务人：乙有限公司\n'+text,'movable_pledge',use_llm=False)
 i=next(i for i in r['items'] if i['item_id']=='SEC-10-01')
 assert len(i['coverage_elements'])==2
 external=i['decision_trace']['requirement_kind_assessments']
 assert len(external)==2
 assert all(e['external_fact_status']=='UNVERIFIED' for e in external)
 assert '合同原文覆盖全部专项要素' not in i['reasoning_summary']

def test_current_contract_final_projection():
 from docx import Document
 from pathlib import Path
 from review_v2.engine import review_contract_v2
 text='\n'.join(p.text for p in Document(Path(__file__).resolve().parents[2]/'test_data/68 动产质押合同.docx').paragraphs)
 r=review_contract_v2(text,'movable_pledge',use_llm=False)
 i=next(i for i in r['items'] if i['item_id']=='SEC-03-01')
 rows=[e for e in i['evidence_clauses'] if '均为甲方合法所有并有权处分' in e.get('text','')]
 assert rows
 for e in rows:
  assert set(e['supports_element_ids'])==set(e['supporting_element_ids'])=={'security_title_authority_1','security_title_authority_2'}
 assert r['release_quality_gate']['status']=='REPORT_READY'

def test_external_verification_gate_rejects_contract_statement():
 from review_v2.final_context_consistency import verify
 report={'items':[{'item_id':'TEST','decision_trace':{'requirement_kind_assessments':[{'element_id':'authorization','requirement_kind':'EXTERNAL_VERIFICATION','external_fact_status':'VERIFIED','status':'VERIFIED','external_verification':{'source_type':'CONTRACT_STATEMENT'}}]}}]}
 assert verify(report)['status']=='BLOCKED'
