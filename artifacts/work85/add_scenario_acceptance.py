from pathlib import Path
p=Path('backend/tests/test_work_scenario_gates.py')
s=p.read_text(encoding='utf8')+'''

def test_fixed_work_contract_final_scenarios():
 from pathlib import Path
 from review_v2.engine import review_contract_v2
 text=(Path(__file__).resolve().parents[2]/'artifacts/work85/source.txt').read_text(encoding='utf8')
 result=review_contract_v2(text,'work',use_llm=False)
 rows={r['item_id']:r for r in result['items']}
 for key in ['COMMON-23-01','W-03-03','W-10-03']:
  assert rows[key]['coverage_status']=='不适用'
 assert rows['W-03-04']['applicability']['applicable']
 for key in ['W-04-03','W-04-04']:
  assert rows[key]['coverage_status']=='部分覆盖'
 assert result['release_quality_gate']['status']=='REPORT_READY'
'''
p.write_text(s,encoding='utf8')
