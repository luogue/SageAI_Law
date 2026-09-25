"""Exercise the actual absence-search entrypoint and preserve source lineage."""
import hashlib
import io
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import pytest
from layers.input_layer import InputLayer
from review_v2 import engine
from review_v2.clause_parser import parse_contract_clauses
from review_v2.work_evidence import PROFILES, evidence_for


@pytest.mark.parametrize('text,key', [
    ('定作方有权要求重作、修理、减少价款或退货。', 'defect_remake'),
    ('定作方有权要求重作、修理、减少价款或退货。', 'defect_repair'),
    ('应当负责修整或调换。', 'defect_repair'),
    ('定作方有权要求重作、修理、减少价款或退货。', 'reduce_remuneration'),
    ('应当按质论价，酌减酬金或价款。', 'reduce_remuneration'),
    ('质量不合格时酬减酬金。', 'reduce_remuneration'),
    ('由此造成的损失由承揽方赔偿。', 'defect_compensation'),
])
def test_actual_search_audit_uses_same_positive_matcher(text, key):
    node='work_'+key
    clauses=parse_contract_clauses('第十二条 承揽方的违约责任\n'+text)
    requirement=PROFILES[node][0]
    item=SimpleNamespace(node_id=node,item_id='W-08-test',decision_trace={})
    audit=engine._search_final_element(item,{**requirement,'status':'MISSING'},clauses)
    assert audit['result']=='FOUND'
    assert audit['search_mode']=='WORK_CANONICAL_REQUIREMENT'
    assert audit['supporting_evidence']==evidence_for(node,clauses)
    assert all(text in e['quote'] and '第十二条' in e['location'] for e in audit['supporting_evidence'])


def test_negative_and_exchange_only_do_not_prove_remake():
    node='work_defect_remake'
    item=SimpleNamespace(node_id=node,item_id='W-08-02',decision_trace={})
    for text in ('质量不合格时不得要求重作。','应当负责修整或调换。'):
        assert engine._search_final_element(item,{**PROFILES[node][0],'status':'MISSING'},parse_contract_clauses(text))['result']=='NOT_FOUND'


def test_original_document_reaches_fact_extractor_and_every_work_search():
    path=Path(__file__).resolve().parents[2]/'test_data/56 承揽合同.docx'
    text,_=InputLayer().extract_text_with_diagnostics(SimpleNamespace(filename=path.name,file=io.BytesIO(path.read_bytes())))
    seen={}
    original_apply=engine.apply_work_evidence
    original_search=engine._search_final_element
    def capture(stage,clauses):
        corpus='\n'.join(c.text for c in clauses)
        assert corpus==text
        seen[stage]=hashlib.sha256(corpus.encode()).hexdigest()
        assert any('第十二条' in c.location and '逾期交付定作物' in c.text for c in clauses)
    def apply(items,clauses):
        capture('extractor',clauses)
        return original_apply(items,clauses)
    def search(item,element,clauses):
        if item.item_id.startswith('W-08-'): capture(item.item_id,clauses)
        return original_search(item,element,clauses)
    with patch.object(engine,'apply_work_evidence',apply),patch.object(engine,'_search_final_element',search):
        result=engine.review_contract_v2(text,'work_contract',use_llm=False)
    assert set(seen)=={'extractor','W-08-01','W-08-02','W-08-03','W-08-04'}
    assert len(set(seen.values()))==1
    assert result['release_quality_gate']['status']=='REPORT_READY'
    identity=next(i for i in result['items'] if i['item_id']=='W-02-01')
    assert identity['evidence_location']=='全文'
    assert len(identity['evidence_clauses'])==1
    assert identity['coverage_elements'][0]['source_locations']==['全文']
