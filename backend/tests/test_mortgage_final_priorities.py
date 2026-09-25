from pathlib import Path
import json
from docx import Document
from review_v2.engine import review_contract_v2

def test_mortgage_final_priority_and_observation_consistency():
    root=Path(__file__).resolve().parents[2]
    text='\n'.join(p.text for p in Document(root/'test_data/54 抵押合同.docx').paragraphs)
    report=review_contract_v2(text,'mortgage',use_llm=False)
    out=root/'artifacts/mortgage_final_priorities';out.mkdir(exist_ok=True)
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'report.md').write_text(report['result'],encoding='utf-8')
    by={i['item_id']:i for i in report['items']}
    external=by['SEC-04-01']
    assert external['coverage_status'] in {'INSUFFICIENT_CONTEXT','待核验'}
    assert external['needs_manual_review']
    manual=next(r for r in report['manual_review_items'] if r['item_id']=='SEC-04-01')
    assert manual['materiality']=='MEDIUM'
    assert '登记前' in manual['review_instruction']
    notice=by['S-00-03']
    assert notice['coverage_status']=='缺失'
    # A real drafting gap is an optional improvement, not a suppressed observation.
    assert notice['action_priority']=='C_OPTIMIZATION'
    assert notice['coverage_elements']
    assert all(e['status']=='MISSING' for e in notice['coverage_elements'])
    assert report['risk_theme_summary']['must_change']==0
    assert report['risk_theme_summary']['should_change']==0
    assert report['risk_theme_summary']['total']==1
    assert report['risk_theme_summary']['optional_improvement']==1
    assert report['statistics_consistency_gate']['status']=='REPORT_READY'
    assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']
    out=root/'artifacts/mortgage_final_priorities';out.mkdir(exist_ok=True)
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'report.md').write_text(report['result'],encoding='utf-8')
