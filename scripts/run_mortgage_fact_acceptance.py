"""Full mortgage review with a per-element source/search audit."""
import json
import sys
from pathlib import Path
from collections import Counter
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from review_v2.engine import review_contract_v2
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import corpus_facts
from review_v2.report_statistics import coverage_bucket

def main():
    out = ROOT / 'artifacts' / sys.argv[1]
    out.mkdir(parents=True, exist_ok=True)
    text = '\n'.join(p.text for p in Document(ROOT / 'test_data/54 抵押合同.docx').paragraphs if p.text.strip())
    clauses = parse_contract_clauses(text)
    result = review_contract_v2(text, 'mortgage', use_llm=False)
    audit = []
    for item in result['items']:
        requirements = item['decision_trace'].get('semantic_requirements', [])
        facts = corpus_facts(clauses, requirements)
        for element in item.get('coverage_elements', []):
            audit.append(dict(rule_id=item['item_id'], element=element,
                final_coverage_status=item['coverage_status'],
                status='FOUND' if element['status']=='COVERED' else 'NOT_FOUND' if element['status']=='MISSING' else element['status'],
                evidence=facts.get(element['element_id'], []),
                search_audit=next((a for a in item['decision_trace'].get('element_absence_searches', [])
                    if a['element_id']==element['element_id']), item['decision_trace'].get('missing_proof', {})),
                searched_clauses=[dict(clause_id=c.clause_id, location=c.location, text=c.text)
                    for c in clauses if c.section_type in {'正式合同条款','附件'}]))
    checks={'statistics_match':dict(Counter(coverage_bucket(i['coverage_status']) for i in result['items']))==result['coverage_summary'],
        'statistics_gate':result['statistics_consistency_gate'],
        'risk_theme_summary':result.get('risk_theme_summary'),
        'risk_finding_summary':result.get('risk_finding_summary'),
        'release_quality_gate':result['release_quality_gate'],
        'positive_negative_conflicts':[
            {'rule_id':i['item_id'],'element_id':a['element_id']}
            for i in result['items'] for a in i['decision_trace'].get('element_absence_searches',[])
            if a['result']=='NOT_FOUND' and any(e['element_id']==a['element_id'] and e['status']=='COVERED'
                for e in i['coverage_elements'])]}
    for name, value in [('report.json',result),('element_audit.json',audit),('checks.json',checks)]:
        (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'report.md').write_text(result['result'],encoding='utf-8')
    lines=['# 抵押合同逐要素审计', '']
    for row in audit:
        search=row['search_audit']
        lines += [f"## {row['rule_id']} / {row['element']['proposition']}", '',
            f"要素：{row['status']}；最终 coverage_status：{row['final_coverage_status']}", '',
            '真实原文：', *[f"- {e['clause_id']} {e['location']}：{e['text']}" for e in row['evidence']],
            '', f"SEARCH_AUDIT：{search.get('result', '未生成专项审计')}；实际检索条款：" +
            '、'.join(search.get('searched_clause_ids', [])), '']
    (out/'element_audit.md').write_text('\n'.join(lines),encoding='utf-8')
    kinds=[{'rule_id':i['item_id'], 'coverage_status':i['coverage_status'],
            'risk_level':i['risk_level'], 'action_priority':i.get('action_priority'),
            'needs_manual_review':i.get('needs_manual_review'),
            'contract_elements':i.get('coverage_elements',[]),
            'noncontract_elements':i['decision_trace'].get('requirement_kind_assessments',[])}
           for i in result['items']]
    (out/'requirement_kinds.json').write_text(json.dumps(kinds,ensure_ascii=False,indent=2),encoding='utf-8')
    for row in audit:
        print(row['rule_id'], row['element']['proposition'], row['status'],row['final_coverage_status'])
    print(checks)

if __name__=='__main__': main()
