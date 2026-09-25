"""Source-reviewed second triage; counts hypotheses separately from confirmed causes.

Indices refer exclusively to the frozen round4 failure inventory, never to
production rule decisions. Every original failure retains its test identity and
assertion so routing/snapshot failures are not counted as alias misses.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
 'normalization / canonical mapping': {
  'canonical_schema_or_composite_contract': [1,16,19,20,49,50,51,52,53,54,64,73,85],
  'downstream_gate_requires_causal_trace': [3,7,9,13,14,15,18,23,29,40,42,46,47,48,56,57,69,70,71,75,83,84,86,97,98],
  'scenario_route_or_response_contract': [31,32,33,34,35,36,37,38,39,100,101],
  'source_identity_or_projection': [4,17,30,58,59,65,66,74,90,96,99],
  'narrative_or_metadata_not_alias': [2,5,10,12,21,43,45,55,72,76,77,79,81,89,95],
  'aggregate_membership_or_count': [6,8,24,25,26,28,41,61,87],
  'conditional_or_material_state': [11,60,67,68,78,80,94],
  'value_base_or_timing_normalization': [27,44,62,82],
  'shared_specific_state_collision': [22,63,88,91,92,93],
 },
 'extraction miss': {
  'positive_source_lost_in_adapter_or_state': [6,11,16,23,24,25,26,27,28,37,40],
  'predicate_context_or_composite_boundary': [2,3,4,8,9,14,15,18,29,30,31,49],
  'claim_event_actor_or_cross_sentence_scope': [13,21,38,39],
  'prerequisite_route_or_external_condition': [17,22,32,33,34,35,41,42,46,47,48,50],
  'projection_polarity_or_presentation_not_extraction': [1,5,7,10,12,19,20,36,43,44,45],
 },
}


def main():
    source = ROOT / 'artifacts/technology_pass_semantics/round4_clusters_final.json'
    original = json.loads(source.read_text(encoding='utf8'))
    result = {'method': 'SECOND_PASS_SOURCE_AND_ASSERTION_TRIAGE; unresolved groups are not confirmed causes',
              'source_inventory': str(source.relative_to(ROOT)), 'groups': {}, 'tests': []}
    for category, groups in GROUPS.items():
        rows = [r for r in original['tests'] if r['category'] == category]
        indices = [i for ids in groups.values() for i in ids]
        assert sorted(indices) == list(range(1, len(rows)+1))
        result['groups'][category] = {k: len(v) for k,v in groups.items()}
        for group, ids in groups.items():
            for i in ids:
                result['tests'].append(dict(rows[i-1], secondary_group=group,
                    diagnosis_status='SOURCE_REVIEWED_REQUIRES_RUNTIME_CAUSAL_CONFIRMATION'))
    output = source.with_name('round5_secondary_clusters.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(result['groups'], ensure_ascii=False))


if __name__ == '__main__': main()
