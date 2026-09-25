"""Summarize the explicitly assumed local diagnostic, not a live acceptance."""
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/technology_pass_semantics/round19_secret_diagnosis'


def main():
    report = json.loads((OUT / 'candidate_local_final3_assumed_licensee.json').read_text(encoding='utf8'))
    selected = {row['item_id']: row for row in report['items']
                if row['item_id'] in {'TC-02-02', 'TC-12-01', 'TC-12-02', 'TC-11-04'}}
    rejects = []
    for failure in report['release_quality_gate']['failures']:
        for detail in failure.get('details') or [failure]:
            rule = detail.get('review_id') or detail.get('entity_id') or failure.get('entity_id')
            item = selected.get(rule, {})
            element = next((row for row in item.get('coverage_elements', [])
                            if row.get('element_id') == detail.get('element_id')), {})
            rejects.append(dict(
                code=failure.get('requirement'), stage=failure.get('failure_stage'),
                rule_id=rule, element_id=detail.get('element_id'), fact_id=element.get('fact_id'),
                polarity=element.get('polarity'), condition=element.get('condition'),
                source_clause_ids=element.get('source_clause_ids') or None,
                source_spans=element.get('source_spans') or None,
                evidence_ids=element.get('evidence_ids') or None,
                report_evidence=item.get('evidence_clauses') or None,
                final_coverage=item.get('coverage_status'), detail=detail))
    source = OUT / 'candidate_input/original.docx'
    result = dict(
        mode='LOCAL_DIAGNOSTIC_ONLY', original_request='NOT_VERIFIED',
        candidate_source=str(source), candidate_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        assumed_parameters=dict(contract_type='technology', use_llm=False, user_identity='乙方/被许可方'),
        gate=report['release_quality_gate']['status'], raw_reject_count=len(report['release_quality_gate']['failures']),
        expanded_reject_count=len(rejects), rejects=rejects,
        items=selected,
        risk_findings=[row for row in report.get('risk_findings', [])
                       if any(rule in json.dumps(row, ensure_ascii=False) for rule in selected)],
        source_hashes={str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                       for path in [ROOT / 'backend/review_v2' / name for name in
                                    ('engine.py', 'proposition_scope.py', 'technology_adverse_evidence.py', 'technology_service_analysis.py')]},
    )
    (OUT / 'diagnosis_final.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k: result[k] for k in ('mode', 'gate', 'raw_reject_count', 'expanded_reject_count')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
