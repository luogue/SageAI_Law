"""Merge modeled adverse facts, never rule names or coincident source clauses.

A parent may cover several atoms. Connected components absorb child findings
only through an identical scoped fact/exposure/remedy, retaining every atom.
Unmodeled findings continue through the existing conservative projection.
"""
import hashlib
import json

IDENTITY = ('fact', 'scope', 'actor', 'object', 'legal_exposure', 'remedy')


def atoms(finding):
    rows = (finding.aggregation_signals or {}).get('adverse_fact_atoms', [])
    valid = [r for r in rows if all(r.get(k) and str(r[k]).lower() not in {'unknown', 'unspecified'} for k in IDENTITY) and r.get('evidence_ids')]
    return valid if len(valid) == len(rows) else []


def key(atom):
    return tuple(str(atom[k]) for k in IDENTITY)


def groups(findings):
    components = []
    remaining = []
    for finding in findings:
        rows = atoms(finding)
        if not rows:
            remaining.append(finding)
            continue
        identities = {key(r) for r in rows}
        matches = [c for c in components if c['keys'] & identities]
        members = [finding]
        for c in matches:
            members.extend(c['members']); identities.update(c['keys'])
            components.remove(c)
        components.append({'keys': identities, 'members': members})
    result = []
    for component in components:
        members = component['members']
        by_fact = {}
        for member in members:
            for atom in atoms(member):
                by_fact.setdefault(key(atom), atom)
        rows = list(by_fact.values())
        parents = {r.get('parent_title') for r in rows}
        title = rows[0]['title'] if len(rows) == 1 else (next(iter(parents)) if len(parents)==1 and None not in parents else '；'.join(dict.fromkeys(r['title'] for r in rows)))
        digest = hashlib.sha256(json.dumps(sorted(component['keys']),ensure_ascii=False).encode()).hexdigest()[:16]
        result.append({'group_id': 'adverse-facts::'+digest, 'members': members,
            'merge_basis': 'SCOPED_ADVERSE_FACT_EXPOSURE_AND_REMEDY',
            'cluster': {'title': title, 'summary': '；'.join(dict.fromkeys(r['summary'] for r in rows)),
                'recommendation': '建议'+'；'.join(dict.fromkeys(r['recommendation'].rstrip('。；') for r in rows))+'。',
                'fact_keys': [list(k) for k in sorted(component['keys'])]}})
    return result, remaining
