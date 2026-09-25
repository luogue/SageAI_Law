"""Check captured *final business responses*, not just intermediate extraction."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_result(result):
    debug = result['structured_fact_debug']
    assert debug['provider'] == 'deepseek'
    assert all(p['provider'] == 'deepseek' for p in debug['deepseek_raw_results'])
    assert debug['semantic_verification']['provider'] == 'deepseek'
    assert debug['source_sha256'] == hashlib.sha256(debug['input']['text'].encode()).hexdigest()
    clauses = {c['clause_id']: c for c in debug['input']['clauses']}
    facts = []

    def collect(value):
        if isinstance(value, list):
            facts.extend(value)
        else:
            for child in value.values():
                collect(child)

    collect(debug['employment'])
    valid = set()
    for fact in facts:
        for evidence in fact['evidence']:
            clause = clauses[evidence['clause_id']]
            span = evidence['evidence_span']
            assert clause['text'][span['start']:span['end']] == evidence['quote']
            if fact['assertion'] == 'EXPLICIT' and fact['confidence'] >= .75:
                valid.add((evidence['clause_id'], evidence['quote']))
    for row in result['items']:
        if row['item_id'].startswith(('EMP-', 'NC-')):
            if row['coverage_status'] != '不适用':
                assert row['judge_source'] == 'structured_facts'
            for element in row.get('coverage_elements', []):
                if element['status'] == 'COVERED':
                    evidence = element.get('supporting_evidence', [])
                    assert evidence, (row['item_id'], element['element_id'])
                    assert all((e['clause_id'], e['quote']) in valid for e in evidence)
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    return len(facts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=Path, default=ROOT/'artifacts/employment-fact-holdouts')
    parser.add_argument('--suffix', default='schema-final')
    args = parser.parse_args()
    cases = json.loads((ROOT/'backend/tests/fixtures/employment_fact_holdouts.json').read_text(encoding='utf8'))
    manifest = json.loads((args.directory/'input-manifest.json').read_text(encoding='utf8'))
    summary = []
    for case in cases:
        directory = args.directory/(case['id']+'-'+args.suffix)
        source_hash = hashlib.sha256((args.directory/(case['id']+'.docx')).read_bytes()).hexdigest()
        assert source_hash == manifest[case['id']], 'Regression input was changed'
        capture = json.loads((directory/'acceptance.json').read_text(encoding='utf8'))
        assert capture['fresh_deepseek'], 'Replay is not fresh model acceptance'
        result = json.loads((directory/'result.json').read_text(encoding='utf8'))
        count = check_result(result)
        rows = {r['item_id']:r for r in result['items']}
        for rule, expected in case['expected'].items():
            assert rows[rule]['coverage_status'] == expected, (case['id'], rule, rows[rule]['coverage_status'])
        summary.append({'case':case['id'], 'unchanged':True, 'source_sha256':source_hash,
            'fresh_deepseek':True, 'gate':'REPORT_READY', 'fact_count':count,
            'assertions':'final statuses, exact source spans, covered-element evidence, provider, input hash'})
    (args.directory/'final-acceptance.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'{len(summary)} complete business responses verified')


if __name__ == '__main__':
    main()
