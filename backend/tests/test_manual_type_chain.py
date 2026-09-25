import pytest
from review_v2.fact_routing import resolve, CURRENT_ROUTE, TYPE_STAGES, finalize
from review_v2.contract_registry import get_checklist_for_resolution

TEXT = '信息管理协议。公司向员工提供采购计划、销售资料，员工承担保密义务，离职时返还设备和材料。'

@pytest.mark.parametrize('kind', ['confidentiality', 'sale', 'labor', 'non_compete', 'confidentiality'])
def test_manual_selection_controls_pipeline_and_checklist(kind):
    route = resolve(TEXT, kind)
    assert route.selected_type == route.resolved_type == kind
    rows = get_checklist_for_resolution(kind, route.domain)
    ids = [r.item_id for r in rows]
    prefix = {'confidentiality': 'NDA-', 'sale': 'S-', 'labor': 'EMP-', 'non_compete': 'NC-'}[kind]
    assert any(i.startswith(prefix) for i in ids)
    if kind != 'sale':
        assert not any(i.startswith('S-01-') for i in ids)

@pytest.mark.parametrize('bad_stage', ['canonical', 'facts_pipeline', 'checklist', 'report', None])
def test_final_gate_reconciles_actual_stage_types(bad_stage):
    route = resolve(TEXT, 'confidentiality')
    token = CURRENT_ROUTE.set(route)
    stages = {k: 'confidentiality' for k in ['request', 'canonical', 'facts_pipeline', 'checklist']}
    if bad_stage and bad_stage != 'report': stages[bad_stage] = 'sale'
    st = TYPE_STAGES.set(stages)
    try:
        result = finalize({'contract_type': 'sale' if bad_stage == 'report' else 'confidentiality',
                           'result': 'report', 'release_quality_gate': {'status': 'REPORT_READY'}})
        assert result['release_quality_gate']['status'] == ('BLOCKED' if bad_stage else 'REPORT_READY')
        if bad_stage: assert result['report_generation_decision']['report_generated'] is False
    finally:
        TYPE_STAGES.reset(st)
        CURRENT_ROUTE.reset(token)
