"""Record final verification while keeping the unconfirmed live request open."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/technology_pass_semantics/round19_secret_diagnosis'


def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8-sig'))


def main():
    comparison = read('full58_comparison.json')
    guards = read('guards_final.json')
    diagnosis = read('diagnosis_final.json')
    result = dict(
        status='NOT_CLOSED',
        original_request_verification='NOT_VERIFIED',
        original_input_verification='EXTRACTED_TEXT_SHA256_MATCHES_ORIGINAL_REQUEST_LOG',
        original_llm_execution='CLOUD_CALLS_OBSERVED_IN_ORIGINAL_REQUEST_TRACE',
        required_user_information=['original review party', 'original request form parameters if available'],
        full_test_comparison=comparison,
        guards=guards,
        guard_count=len(guards),
        guards_ready=sum(row['gate'] == 'REPORT_READY' and not row['failures'] for row in guards.values()),
        candidate_local_diagnostic=dict(
            mode=diagnosis['mode'], assumed_parameters=diagnosis['assumed_parameters'],
            gate=diagnosis['gate'], raw_reject_count=diagnosis['raw_reject_count'],
            expanded_reject_count=diagnosis['expanded_reject_count'],
            item_states={key: row['coverage_status'] for key, row in diagnosis['items'].items()},
            rejects=diagnosis['rejects']),
        final_code=read('run_manifest_final.json'),
        prior_full57_new_regression='Fixed without changing the existing test assertion; see Full58 comparison.',
    )
    (OUT / 'final_summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(dict(status=result['status'], tests=comparison['current'],
                         newly_failing=comparison['newly_failing'], recovered=comparison['recovered'],
                         guards_ready=result['guards_ready'], candidate_gate=diagnosis['gate']), ensure_ascii=False))


if __name__ == '__main__':
    main()
