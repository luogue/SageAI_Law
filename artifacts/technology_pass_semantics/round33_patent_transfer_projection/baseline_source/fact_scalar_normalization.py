"""Unwrap representation only; semantic types and evidence remain independently validated."""
from review_v2.fact_validation import FactExtractionError


def unwrap_scalar(concept, raw, kind):
    if not isinstance(raw, dict):
        return raw
    leaf = concept.rsplit('.', 1)[-1]
    keys = {'value', leaf}
    # Unit/role aliases are derived from the schema field, never contract text.
    for suffix in ('scope', 'mode', 'type', 'date'):
        if leaf.endswith('_' + suffix):
            keys.add(suffix)
    if leaf.endswith('duration_months'):
        keys.add('months')
    if leaf.endswith(('notice_days', 'cycle_days')):
        keys.add('days')
    if len(raw) != 1 or next(iter(raw), None) not in keys:
        raise FactExtractionError('INVALID_SCALAR_WRAPPER', failed_stage='NORMALIZATION',
            field='value', model_raw_value=raw, actual=raw,
            expected={'single_field_keys': sorted(keys), 'type': kind})
    value = next(iter(raw.values()))
    if value is None or isinstance(value, (dict, list)):
        raise FactExtractionError('INVALID_SCALAR_WRAPPER_VALUE', failed_stage='NORMALIZATION',
            field='value', model_raw_value=raw, actual=value, expected=kind)
    return value
