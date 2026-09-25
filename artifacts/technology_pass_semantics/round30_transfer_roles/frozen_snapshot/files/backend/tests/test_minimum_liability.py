import os
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore
from review_v2.fact_verification import verified_store
from review_v2.fact_validation import FactExtractionError
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet

CASES = [
 ('违反保密义务应赔偿实际损失。', None, True, False),
 ('违反保密义务赔偿金额不得低于十万元。', 'MINIMUM_AMOUNT', False, False),
 ('违反保密义务应付违约金十万元。', 'FIXED_AMOUNT', False, False),
 ('违反保密义务赔偿实际损失，但最低五万元。', 'MINIMUM_AMOUNT', True, False),
 ('违反保密义务赔偿实际损失，上限十万元。', None, True, True),
 ('违反保密义务按实际损失的百分之三十赔偿。', 'FORMULA', False, False),
]

@pytest.mark.parametrize('text,kind,damage,cap', CASES)
def test_distinct_liability_consumers(text, kind, damage, cap):
 cs=parse_contract_clauses(text); fs=[]
 if kind:fs.append(fact(cs,'penalties.obligations',{'scope':'CONFIDENTIALITY','imposed':True,'trigger':'违反保密义务','liability_kind':kind,'amount_text':'实际损失的30%' if kind=='FORMULA' else ('50000' if '五万元' in text else '100000')},text))
 if damage:fs.append(fact(cs,'worker.damage_liability',{'kind':'ACTUAL_DAMAGE_COMPENSATION','trigger':'违反保密义务','basis':'实际损失'},text))
 if cap:fs.append(fact(cs,'worker.liability_limit',{'kind':'CAP','amount_text':'十万元','basis':'最高责任','trigger':'违反保密义务'},text))
 s=FactStore(text,cs,packet(cs,fs));s=verified_store(s,verified_packet(cs,s))
 assert bool(s.adverse('employment_general_penalty')) is bool(kind)
 assert bool(s.get('worker.damage_liability')) is damage
 assert bool(s.get('worker.liability_limit')) is cap

@pytest.mark.parametrize('kind',['CAP','ACTUAL_DAMAGE',None,3])
def test_invalid_penalty_kind_is_not_coerced(kind):
 from review_v2.penalty_liability_semantics import normalize
 with pytest.raises(FactExtractionError):normalize({'liability_kind':kind})

@pytest.mark.skipif(os.getenv('RUN_DEEPSEEK_REGRESSION')!='1',reason='live provider test')
@pytest.mark.parametrize('text,kind,damage,cap', CASES)
def test_live_extraction_and_verifier(text,kind,damage,cap):
 from review_v2.deepseek_facts import extract,verify
 cs=parse_contract_clauses('员工保密协议\n甲方为用人单位，乙方为员工。\n第一条\n'+text)
 source='\n'.join(c.text for c in cs)
 keys=['penalties.obligations','penalties.exclusions','worker.damage_liability','worker.liability_limit']
 raw=extract(cs,concept_keys=keys);s=FactStore(source,cs,raw);s=verified_store(s,verify(cs,s))
 assert bool(s.adverse('employment_general_penalty')) is bool(kind)
 if kind:assert all(f['normalized_value']['liability_kind']==kind for f in s.get('penalties.obligations'))
 assert bool(s.get('worker.damage_liability')) is damage
 assert bool(s.get('worker.liability_limit')) is cap
