from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import pytest
from docx import Document
from review_v2.engine import review_contract_v2
from review_v2.lease_semantics import consistency_failures
from review_v2.nda_semantics import scenario


def review(text):
    return review_contract_v2(text,'confidentiality',use_llm=False)


def item(r,key):
    return next(i for i in r['items'] if i['item_id']==key)


def test_institutional_document_full_pipeline():
    source=Path(__file__).resolve().parents[2]/'test_data/71 保密协议.docx'
    r=review('\n'.join(p.text for p in Document(source).paragraphs))
    assert len(r['items'])==9
    assert item(r,'COMMON-20-01')['coverage_status']=='部分覆盖'
    for key in ['NDA-01-01','NDA-03-01','NDA-04-01']:
        i=item(r,key)
        assert i['coverage_status']=='通过'
        assert not any(a['result']=='NOT_FOUND' for a in i['decision_trace']['element_absence_searches'])
        assert i['decision_trace']['nda_scenario']['variant']=='INSTITUTIONAL_NDA'
    duty=item(r,'NDA-02-01')
    assert duty['coverage_status']=='部分覆盖'
    assert [e['proposition'] for e in duty['coverage_elements'] if e['status']=='MISSING']==['资料返还或销毁安排']
    assert item(r,'EMP-14-01')['coverage_status']=='不适用'
    for text in [duty['legal_consequence_if_missing'],duty['narrative_state'].get('consequence','')]:
        assert not any(s in text for s in ['劳动关系','劳动者','用人单位','法定劳动权利'])
    assert r['release_quality_gate']['status']=='REPORT_READY'


@pytest.mark.parametrize('numbering',[False,True])
def test_alternative_exclusions_and_numbered_lists(numbering):
    clauses=['已进入公共领域的信息','接收方原已知悉的信息','从合法第三人取得的信息','接收方自行研发的信息','依法院、监管机构要求披露的信息']
    body='\n'.join((f'{n+1}）' if numbering else '')+s+'；' for n,s in enumerate(clauses))
    r=review('保密信息包括技术资料。\n保密信息不包括：\n'+body)
    assert item(r,'NDA-01-01')['coverage_status']=='通过'


@pytest.mark.parametrize('phrase',['赔偿全部实际损失','承担损害赔偿责任','补偿守约方因此受到的损失','有权要求停止侵害并追究赔偿责任'])
def test_remedy_synonyms(phrase):
    r=review('第三章 违约责任\n接受方违反保密义务时，'+phrase+'。')
    assert item(r,'NDA-04-01')['coverage_status']=='通过'


def test_employment_variant_is_preserved():
    r=review('员工保密协议。甲方：远航有限公司。乙方：王宇。双方建立劳动关系。甲方向乙方提供商业秘密。')
    assert item(r,'NDA-02-01')['decision_trace']['nda_scenario']['variant']=='EMPLOYMENT_NDA'
    assert '劳动关系' in item(r,'NDA-02-01')['narrative_state']['consequence']
    assert item(r,'EMP-14-01')['coverage_status']!='不适用'


def test_employees_in_information_definition_not_relationship():
    assert scenario('双方合作研发，保密信息包括客户、雇员、财务及人事信息。')=='INSTITUTIONAL_NDA'


def test_waiver_is_not_positive_remedy():
    r=review('接受方违反保密义务时无需赔偿任何损失。')
    assert item(r,'NDA-04-01')['coverage_status']!='通过'


def test_positive_exclusion_cannot_coexist_with_not_found():
    r=review('保密信息不包括已公开信息、原已知悉信息、独立研发信息、合法第三人取得信息及依法院要求披露的信息。')
    i=deepcopy(item(r,'NDA-01-01'))
    audit=next(a for a in i['decision_trace']['element_absence_searches'] if a['result']=='FOUND')
    audit['result']='NOT_FOUND'
    assert any(f['requirement']=='SEARCH_AUDIT_ELEMENT_CONFLICT' for f in consistency_failures([SimpleNamespace(**i)]))
