import json
from pathlib import Path
from functools import lru_cache
from copy import deepcopy
import pytest
from docx import Document
from review_v2.engine import review_contract_v2
from review_v2.clause_parser import parse_contract_clauses
from review_v2.equity_transaction_facts import corpus_consistency_gate, structure_evidence
from review_v2.lease_semantics import corpus_facts
from review_v2.priority_checklist_helpers import PROFILES

ROOT=Path(__file__).resolve().parents[2]
TEXT='\n'.join(p.text for p in Document(ROOT/'test_data/81 增资扩股协议.docx').paragraphs)
@lru_cache(None)
def result():return review_contract_v2(TEXT,'capital_increase',use_llm=False)

@pytest.mark.parametrize('rule,element',[
 ('EQT-01-01','equity_title_3'),('EQT-02-01','equity_contribution_liability_1'),
 ('EQT-02-01','equity_contribution_liability_3'),('EQT-04-01','equity_price_payment_1'),
 ('EQT-05-01','equity_closing_registration_5'),('EQT-08-01','equity_valuation_2'),
 ('EQT-11-01','equity_warranties_remedies_3'),('S-00-03','general_notice_method')])
def test_actual_atomic_fact_not_absent(rule,element):
 i=next(i for i in result()['items'] if i['item_id']==rule)
 e=next(e for e in i['coverage_elements'] if e['element_id']==element)
 assert e['status']=='COVERED'
 assert e['supporting_evidence']
 assert not any(a['element_id']==element and a['result']=='NOT_FOUND' for a in i['decision_trace'].get('element_absence_searches',[]))
 assert i['coverage_status']!='缺失'


def test_three_structural_conflicts_have_direct_sources():
 for key in ('EQT-14-01','EQT-15-01','EQT-16-01'):
  i=next(i for i in result()['items'] if i['item_id']==key)
  assert i['coverage_status']=='风险条款' and i['evidence_clauses']
 assert result()['release_quality_gate']['status']=='REPORT_READY',result()['release_quality_gate']['failures']


def test_corpus_gate_blocks_injected_absence_even_without_positive_bundle():
 rows=deepcopy(result()['items']);i=next(x for x in rows if x['item_id']=='EQT-04-01')
 i['coverage_elements'][0]['status']='MISSING';i['evidence_clauses']=[]
 i['decision_trace']['element_absence_searches']=[{'element_id':'equity_price_payment_1','result':'NOT_FOUND'}]
 assert corpus_consistency_gate(rows,parse_contract_clauses(TEXT))['status']=='BLOCKED'

@pytest.mark.parametrize('amount,days,asset',[('三百万元','二十','设备'),('800,000元','25','知识产权')])
def test_non_cash_synonyms_without_sample_entities(amount,days,asset):
 cs=parse_contract_clauses('增资协议\n第一条 乙方以'+asset+'作价人民币'+amount+'投入目标公司。\n第二条 乙方应于'+days+'日内将'+asset+'交付给目标公司。')
 f=corpus_facts(cs,PROFILES['equity_price_payment'])
 assert all(f.values())


def test_valid_cross_reference_and_consistent_asset_no_conflict():
 cs=parse_contract_clauses('增资协议\n第一条 乙方以房产所有权作价300万元投入目标公司。\n第二条 声明保证\n乙方向甲方作出声明：\n投入目标公司的房产所有权不存在任何抵押。\n第三条 依本合同第二条履行。')
 assert not structure_evidence('equity_contribution_warranty_alignment',cs)
 assert not structure_evidence('equity_invalid_cross_reference',cs)


def test_explicit_mixed_transaction_is_not_automatically_conflict():
 cs=parse_contract_clauses('增资协议\n第一条 乙方作价300万元投入目标公司。\n第二条 乙方向甲方受让10%股权。增资与转让分别约定对价。')
 assert not structure_evidence('equity_transaction_structure',cs)
