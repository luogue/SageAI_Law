import pytest
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('actual,months,all_staff,expected', [
    (False,18,False,'待核验'),
    (True,18,False,'通过'),
    (True,30,False,'风险条款'),
    (True,18,True,'风险条款'),
])
def test_prerequisites_final_report(monkeypatch,actual,months,all_staff,expected):
    from review_v2 import employment_fact_pipeline as pipeline
    from review_v2.engine import review_contract_v2
    text='竞业限制协议\n第一条\n双方约定离职竞业限制。\n适用人员为研发主管。岗位可以接触秘密。\n员工已掌握客户底价和源代码。\n第二条\n竞争业务为数据库软件，地域为杭州。\n第三条\n竞业期限为'+str(months)+'个月。每月补偿6000元。\n第四条\n所有员工均须承担竞业限制。'
    vals=[('non_compete.arrangement','EXISTS','双方约定离职竞业限制。'),
          ('non_compete.personnel','研发主管','适用人员为研发主管。'),
          ('non_compete.access_capability',True,'岗位可以接触秘密。'),
          ('non_compete.businesses','数据库软件','竞争业务为数据库软件，地域为杭州。'),
          ('non_compete.territories','杭州','竞争业务为数据库软件，地域为杭州。'),
          ('non_compete.duration_months',months,'竞业期限为'+str(months)+'个月。'),
          ('non_compete.compensation',{'amount_text':'6000','unit':'CNY/MONTH'},'每月补偿6000元。')]
    if actual: vals.append(('non_compete.actual_access',True,'员工已掌握客户底价和源代码。'))
    else: text=text.replace('员工已掌握客户底价和源代码。','')
    if all_staff: vals.append(('non_compete.all_staff',True,'所有员工均须承担竞业限制。'))
    else: text=text.replace('所有员工均须承担竞业限制。','')
    cs=parse_contract_clauses(text)
    monkeypatch.setattr(pipeline,'extract',lambda *a,**k:packet(cs,[fact(cs,c,v,q) for c,v,q in vals]))
    monkeypatch.setattr(pipeline,'verify',verified_packet)
    result=review_contract_v2(text,'non_compete')
    rows={r['item_id']:r for r in result['items']}; nc=rows['NC-03-01']
    assert nc['coverage_status']==expected
    assert 'employment_noncompete_scope_1' not in result['result']
    assert 'non_compete.actual_access' not in result['result']
    assert '已覆盖：人员范围及实际接触秘密' not in result['result']
    assert '支持要素：人员范围及实际接触秘密' not in result['result']
    if not actual:
        assessment=nc['decision_trace']['noncompete_prerequisite_assessment']
        assert len(assessment['missing_facts'])==1
        assert '实际接触' in assessment['missing_facts'][0]
        assert sum(f['covered'] for f in assessment['facts'])==5
        assert rows['NC-01-01']['coverage_status']=='通过'
        assert all('actual_access' not in e['element_id'] for e in rows['NC-01-01']['coverage_elements'])
        assert rows['NC-01-01']['action_priority']=='NONE'
        assert rows['NC-01-01']['issue_type']!='条款缺陷'
    assert result['release_quality_gate']['status']=='REPORT_READY',result['release_quality_gate']

