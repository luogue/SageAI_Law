"""Materialize original regression sources and trace the unchanged business entry.

No filename/title-based classification, diagnostic mode, gate override or
fixture mutation. The generated DOCX contains every line of the original text.
"""
import argparse
import importlib
import json
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'backend'), str(ROOT)]
from backend.test_database_bootstrap import install
install()
from docx import Document
from review_v2.clause_parser import parse_contract_clauses, strip_non_contract_tail
from review_v2.fact_routing import resolve
from review_v2.technology_service_analysis import classify_technology_transaction


def main():
    p = argparse.ArgumentParser()
    p.add_argument('sample', choices=('industrial', 'patent', 'consulting'))
    p.add_argument('output', type=Path)
    p.add_argument('--prepare-only', action='store_true')
    p.add_argument('--trace-stages', action='store_true')
    args = p.parse_args()
    if args.sample == 'industrial':
        module = importlib.import_module('tests.test_industrial_technical_service_routing_regression')
        text, prior = module.CONTRACT, 'service'
    elif args.sample == 'patent':
        module = importlib.import_module('tests.test_patent_license_input_integrity_routing')
        text, prior = module.FULL_PATENT_LICENSE, 'sale'
    else:
        module = importlib.import_module('tests.test_technical_consulting_contract_review')
        text, prior = module.CONSULTING_CONTRACT, 'technology'
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line)
    doc.save(output / 'original.docx')
    source = strip_non_contract_tail(text)
    route = resolve(text, prior)
    trace = {'fixture_module': module.__name__, 'original_text': text,
             'source_sha256': sha256(source.encode()).hexdigest(),
             'classification': classify_technology_transaction(source),
             'selection': route.selection.to_public_dict(),
             'resolved_type': route.resolved_type,
             'clauses': [vars(c) for c in parse_contract_clauses(source)]}
    (output / 'route.json').write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding='utf8')
    if not args.prepare_only:
        transitions = []
        if args.trace_stages:
            from review_v2 import engine

            def snapshot(items):
                return {i.item_id: {
                    'coverage': i.coverage_status,
                    'elements': [{k: e.get(k) for k in ('element_id', 'status', 'required_fact_key',
                                  'source_fact_key', 'fact_id', 'fact_ids', 'supporting_evidence',
                                  'source_clause_ids', 'source_spans', 'evidence_ids')}
                                 for e in i.coverage_elements],
                    'verification': i.decision_trace.get('verified_pass_source_gate'),
                    'bindings': i.decision_trace.get('direct_fact_bindings'),
                    'evidence': [{k: e[k] for k in ('evidence_id', 'clause_id', 'quote',
                                  'source_type', 'support_type', 'supporting_element_ids') if k in e}
                                 for e in i.evidence_clauses],
                } for i in items}

            for name in ('_apply_technical_consulting_semantic_rules',
                         '_apply_composite_technology_semantic_rules',
                         '_apply_technology_shared_fact_consistency',
                         '_apply_technology_transaction_evidence_consistency',
                         '_apply_technology_confidentiality_semantic_rules',
                         '_apply_coverage_gap_consistency_guard', '_apply_review_evidence_ownership',
                         '_apply_coverage_evidence_gate', '_apply_final_technology_fact_projection',
                         '_apply_technology_common_semantic_rules', '_protect_deterministic_semantic_evidence',
                         '_apply_factual_grounding_gate', '_apply_evidence_claim_ceiling',
                         '_apply_technology_finding_consistency_gate', '_apply_final_disposition_states',
                         '_enrich_reasoning_and_citation', '_apply_element_level_narratives',
                         '_verified_pass_sources', '_apply_technology_subtype_rendering'):
                original = getattr(engine, name)

                def traced(items, *a, _name=name, _original=original, **kw):
                    before = snapshot(items)
                    result = _original(items, *a, **kw)
                    after = snapshot(result if isinstance(result, list) else items)
                    transitions.extend({'stage': _name, 'rule_id': key,
                                        'before': before.get(key), 'after': after[key]}
                                       for key in after if before.get(key) != after[key])
                    return result

                setattr(engine, name, traced)
        if args.sample == 'consulting':
            from review_v2.engine import review_contract_v2
            from review_v2.user_profile import UserRiskProfile
            report = review_contract_v2(text, prior, use_llm=False,
                                       profile=UserRiskProfile(user_identity='甲方/委托方'))
        else:
            report = module._review() if args.sample == 'industrial' else module._review_bytes(module._docx_bytes(text))
        (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
        # Preserve complete gate objects; never reduce BLOCKED to a status-only assertion.
        gates = {k: v for k, v in report.items() if 'gate' in k and isinstance(v, dict)}
        (output / 'gates.json').write_text(json.dumps(gates, ensure_ascii=False, indent=2), encoding='utf8')
        (output / 'transitions.json').write_text(json.dumps(transitions, ensure_ascii=False, indent=2), encoding='utf8')
        print(json.dumps({'type': report['contract_type'], 'gate': report['release_quality_gate'].get('status')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
