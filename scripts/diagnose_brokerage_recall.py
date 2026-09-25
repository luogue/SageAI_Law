"""Standalone input-first recall diagnostic; never generates or changes a report.

Run each invocation in a fresh Python process. Content hashes remain truthful.
Missing source assertions stop the real-file retrieval path. --probe separately
exercises supplied positive sentences, never merges them into the document.
"""
import argparse
import hashlib
import io
import json
import re
import sys
import uuid
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.brokerage_facts import requirements
from review_v2.lease_semantics import supports, corpus_facts

SENTENCES = [
    '甲方有权要求乙方如实告知与订立合同有关的信息及情况',
    '乙方应当尽到必要、审慎的核实义务，向甲方提供与订立合同有关的完整、准确、真实的信息及情况',
    '甲方应当对乙方提供必要的协助',
    '甲方应当向乙方提供自身与订立合同有关的真实信息',
    '乙方故意隐瞒与订立合同有关的重要事实或者提供虚假情况',
    '不得请求支付服务费用',
    '乙方应当承担损失赔偿责任',
]
RULES = {
    'BR-03-01': ('truthful_report_obligation', [0, 1], ['如实', '告知', '真实', '信息', '情况']),
    'BR-03-02': ('important_fact_disclosure', [1, 4], ['重要事实', '隐瞒', '真实', '完整', '准确']),
    'BR-04-02': ('principal_cooperation_obligation', [2], ['协助', '配合', '必要']),
    'BR-04-03': ('principal_information_accuracy', [3], ['真实信息', '信息真实']),
    'BR-09-01': ('truthful_report_breach_consequence', [4, 5, 6], ['隐瞒', '虚假', '服务费用', '损失赔偿']),
}


def diagnose(text, raw_text=None):
    chunks = parse_contract_clauses(text)
    presence = [dict(text=s, exists=s in text, index=text.find(s),
                     raw_xml_exists=None if raw_text is None else s in raw_text,
                     chunks=[dict(chunk_id=c.clause_id, text=c.text, location=c.location)
                             for c in chunks if s in c.text]) for s in SENTENCES]
    result = dict(task_id=str(uuid.uuid4()), contract_hash=hashlib.sha256(text.encode()).hexdigest(),
                  corpus_length=len(text), corpus=text, presence=presence, rules={},
                  cache='Fresh process; direct pure functions; no persisted review/cache reads')
    profiles = requirements(text)
    for code, (node, indices, keywords) in RULES.items():
        missing = [i for i in indices if not presence[i]['exists']]
        row = result['rules'][code] = dict(requirements=profiles[node], missing_substrings=missing)
        if missing:
            row.update(first_failure='INPUT_SUBSTRING_ASSERT',
                       stages={k: 'NOT_RUN_INPUT_ASSERT_FAILED' for k in 'ABCDEFGH'},
                       decision='NOT_RUN', source_absent=all(presence[i]['raw_xml_exists'] is False for i in missing))
            continue
        # Imported only after input validation; no report entry point is called.
        from review_v2.engine import _search_final_element
        row['elements'] = []
        for spec in profiles[node]:
            candidates = []
            for c in chunks:
                for unit in re.findall(r'[^。]+[。]?', c.text):
                    evidence = dict(clause_id=c.clause_id, location=c.location,
                                    heading_path=list(c.heading_path or []), text=unit,
                                    source_type='CONTRACT_TEXT', supports_element_ids=[spec['element_id']])
                    positive = [p for p in spec['semantic_patterns'] if re.search(p, unit, re.S)]
                    negative = [p for p in spec.get('excluded_patterns', []) if re.search(p, unit, re.S)]
                    relaxed = {**spec, 'excluded_patterns': []}
                    candidates.append(dict(evidence=evidence, keyword_hits=[k for k in keywords if k in unit],
                        formal_pattern_hits=positive, negative_hits=negative,
                        direct_support=supports(spec, evidence), without_exclusion=supports(relaxed, evidence)))
            facts = corpus_facts(chunks, [spec])[spec['element_id']]
            item = SimpleNamespace(item_id=code, node_id=node, decision_trace={'semantic_requirements': profiles[node]})
            audit = _search_final_element(item, {**spec, 'status': 'MISSING'}, chunks)
            row['elements'].append(dict(element=spec,
                formal_top20=sorted(candidates, key=lambda c: len(c['formal_pattern_hits']), reverse=True)[:20],
                loose_top20=sorted(candidates, key=lambda c: len(c['keyword_hits']), reverse=True)[:20],
                semantic_score=None, threshold=None,
                score_explanation='Production supports() is boolean pattern entailment, not a scored semantic model. Audit scores are post-decision diagnostics, not acceptance thresholds.',
                role_check='Embedded in semantic patterns; no independently switchable role filter',
                evidence=facts, search_audit=audit,
                element_decision='COVERED' if facts else 'MISSING',
                wrapper_agrees=(audit['result'] == 'FOUND') == bool(facts),
                final_adjudicator='NOT_RUN: standalone harness excludes report adjudication'))
        row['decision'] = 'PASS' if all(e['evidence'] for e in row['elements']) else 'MISSING'
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--probe', action='store_true')
    args = parser.parse_args()
    data = args.source.read_bytes()
    text, _ = InputLayer().extract_text_with_diagnostics(SimpleNamespace(filename=args.source.name, file=io.BytesIO(data)))
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        raw = '\n'.join(''.join(ET.fromstring(z.read(n)).itertext()) for n in z.namelist()
                        if n.startswith('word/') and n.endswith('.xml'))
    result = diagnose(text, raw)
    result.update(source=str(args.source.resolve()), file_sha256=hashlib.sha256(data).hexdigest())
    if args.probe:
        probe = '中介合同\n甲方（委托人）：客户公司\n乙方（中介人）：咨询公司\n'
        probe += '。\n'.join(SENTENCES[:4]) + '。\n' + '；'.join(SENTENCES[4:]) + '。'
        result['separate_positive_probe'] = diagnose(probe)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['task_id', 'contract_hash', 'corpus_length', 'presence']}, ensure_ascii=False))
    print('FILE', {k: v['decision'] for k, v in result['rules'].items()})
    if args.probe:
        print('SEPARATE_PROBE', {k: v['decision'] for k, v in result['separate_positive_probe']['rules'].items()})
    return 2 if any(not p['exists'] for p in result['presence']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
