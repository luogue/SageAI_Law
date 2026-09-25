"""Ordinary-loan V2 entry. Legacy extraction/review/postprocessors are not called."""
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
from uuid import uuid4
from review_v2.clause_parser import parse_contract_clauses, strip_non_contract_tail
from review_v2.unified_facts.pipeline import extract_verified
from review_v2.unified_facts.loan import schema
from review_v2.unified_facts.loan_rules import evaluate
from review_v2.unified_facts.normalization import wire
from review_v2.unified_facts.store import VerifiedFactStore, fail, rule_context


def validate_report(store, items, findings, recommendations):
    """Reject unknown fact IDs, changed quotations, cross-rule evidence or drift."""
    if not isinstance(store, VerifiedFactStore):
        fail('VERIFIED_STORE_REQUIRED')
    facts = {f['fact_id']: f for f in store.snapshot()}
    by_id = {i.item_id: i for i in items}
    from review_v2.loan_contract_checklist import LOAN_REVIEW_CHECKLIST
    if {i.node_id for i in items} != {c.node_id for c in LOAN_REVIEW_CHECKLIST}:
        fail('INCOMPLETE_LOAN_RULE_SET')
    for item in items:
        decisions = store.debug['rule_decisions'][item.node_id]
        decision = next(d for d in reversed(decisions) if d['stage'] == 'RULE_DECISION')
        if decision['decision']['status'] != item.coverage_status or decision['decision']['severity'] != item.risk_severity:
            fail('REPORT_RULE_DECISION_DRIFT', item.item_id)
        for ref in item.evidence_clauses:
            ids = ref.get('structured_fact_ids', [])
            if not ids or not set(ids) <= set(decision['input_fact_ids']):
                fail('REPORT_FACT_PROVENANCE_BYPASS', item.item_id)
            for fact_id in ids:
                if not any(all(ref.get(k) == e.get(k) for k in ('quote', 'clause_id', 'source_start', 'source_end'))
                           for e in facts[fact_id]['evidence']):
                    fail('REPORT_EVIDENCE_SPAN_DRIFT', item.item_id)
        if item.coverage_status == '缺失' and any(store.state(k) not in {'ABSENT', 'NOT_APPLICABLE'} for k in item.fact_dependencies):
            fail('MISSING_WITH_NONABSENT_FACT', item.item_id)
    for finding in findings:
        source = [by_id[k] for k in finding.source_review_ids]
        if any(i.coverage_status not in {'缺失', '部分覆盖', '风险条款'} for i in source):
            fail('FINDING_WITHOUT_RULE_RISK', finding.finding_id)
        allowed = [e for i in source for e in i.evidence_clauses]
        if any(e not in allowed for e in finding.evidence):
            fail('FINDING_EVIDENCE_BYPASS', finding.finding_id)
    for rec in recommendations:
        if any(by_id[k].coverage_status not in {'缺失', '部分覆盖', '风险条款'} for k in rec.target_review_ids):
            fail('RECOMMENDATION_WITHOUT_VERIFIED_DECISION', rec.recommendation_id)
    return {'status': 'REPORT_READY', 'failures': [],
        'gate_results': {'VERIFIED_LOAN_FACT_PROVENANCE': 'PASS', 'ALL_48_LOAN_CONSUMERS': 'PASS'}}


def report(store, *, profile=None, include_low_risk=True):
    # Only the report serializer/data models are reused from the old engine.
    # No old fact graph, semantic reviewer or raw-text postprocessor is called.
    from review_v2 import engine as e
    from review_v2.user_profile import normalize_profile
    profile = normalize_profile(profile, 'loan')
    with rule_context(store):
        items, costs = evaluate(store)
        from review_v2.unified_facts.loan_formulas import build as build_formulas
        formulas=build_formulas(store)
        perspective = {'canonical_role': {'出借人': 'LENDER', '借款人': 'BORROWER'}.get(profile.user_identity, 'UNCERTAIN'),
            'display_role': profile.user_identity, 'source': 'USER_PROFILE'}
        e._apply_profile_rules(items, profile, perspective)
        findings, recommendations = [], []
        grouping = {'loan_actual_disbursement_evidence': 'loan_disbursement_proof',
            'loan_transfer_voucher_attachment': 'loan_disbursement_proof',
            'loan_collection_ack_limitation_interruption': 'loan_collection_evidence_preservation',
            'loan_collection_record_attachment': 'loan_collection_evidence_preservation'}
        groups = {}
        for item in items:
            if item.coverage_status in {'缺失', '部分覆盖', '风险条款'}:
                groups.setdefault(grouping.get(item.node_id, item.node_id), []).append(item)
        for group, rows in groups.items():
            item = max(rows, key=lambda i: {'NONE': 0, 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}[i.risk_severity])
            fid = 'VF-' + item.item_id
            refs = list({r['evidence_id']: r for i in rows for r in i.evidence_clauses}.values())
            finding = e.RiskFinding(finding_id=fid, risk_group=group, title=item.title,
                severity=item.risk_severity, priority=item.action_priority,
                source_review_ids=[i.item_id for i in rows], facts=[i.reasoning_summary for i in rows],
                evidence=deepcopy(refs), source_clause_ids=list(dict.fromkeys(r['clause_id'] for r in refs)),
                issue=item.risk_point_description, consequence=item.legal_consequence_if_missing,
                recommendation=item.suggested_clause_example, verification_status='VERIFIED',
                risk_category=item.title, issue_type='ADVERSE' if item.coverage_status == '风险条款' else 'MISSING' if item.coverage_status == '缺失' else 'PARTIAL',
                provenance={'source': 'VerifiedFactStore', 'fact_ids': list(dict.fromkeys(f for r in refs for f in r['structured_fact_ids']))},
                evidence_bundle={'items': deepcopy(refs)},
                final_missing_elements=[x for i in rows for x in i.coverage_elements if x['status'] == 'MISSING'])
            findings.append(finding)
            rec = e.Recommendation(recommendation_id='VR-' + item.item_id, type='补充条款' if item.coverage_status == '缺失' else '修改条款',
                priority=item.action_priority, source_finding_ids=[fid], target_clause=item.evidence_location,
                target_risk_ids=[fid], rationale=item.reasoning_summary, suggested_text=item.suggested_clause_example,
                target_review_ids=[i.item_id for i in rows], clauses=deepcopy(refs), status='VERIFIED')
            recommendations.append(rec)
            for i in rows:
                store.record_decision(i.node_id, 'FINDING_AND_RECOMMENDATION',
                    {'finding_id': fid, 'recommendation_id': rec.recommendation_id}, i.fact_dependencies)
        gate = validate_report(store, items, findings, recommendations)
        metadata = {'pipeline_version': e.PIPELINE_VERSION, 'rule_version': e.RULE_VERSION,
            'evaluator_version': e.EVALUATOR_VERSION, 'fact_pipeline': 'loan-verified-1', 'provider': 'deepseek'}
        dispositions = e._build_final_dispositions(findings, recommendations, [])
        assessment = e._overall_assessment('借款合同', findings, items, dispositions, e._manual_review_records(items))
        # This function is the existing pure serializer; supplied decisions are
        # complete so it never needs source text or another extraction pass.
        markdown = e._format_markdown_v2('借款合同', deepcopy(items), profile,
            risk_findings=deepcopy(findings), recommendations=deepcopy(recommendations),
            release_quality_gate=gate, system_metadata=metadata,
            final_dispositions=deepcopy(dispositions), overall_assessment=assessment,
            perspective_resolution=perspective)
        if formulas['formulas']:
            markdown+='\n\n### 已核验事实生成的计息表达\n\n'
            markdown+='\n'.join('- '+f.get('charge_key',f['kind'])+'：'+
                (f['expression'] if f['state']=='PRESENT' else '待核验：'+f['reason']) for f in formulas['formulas'])
        validate_report(store, items, findings, recommendations)
        public_items = [asdict(i) for i in items]
        coverage = dict(Counter(i.coverage_status for i in items))
        result = wire({'success': True, 'contract_type': 'loan', 'contract_type_name': '借款合同',
            'deterministic_interest_formulas':formulas,
            'selected_contract_type': 'loan', 'contract_review_trace_id': uuid4().hex,
            'message': '已通过统一事实层完成借款合同48项审查。', 'items': public_items,
            'all_items_count': len(items), 'all_rule_statuses': public_items,
            'coverage_summary': coverage, 'summary': e._risk_summary(items),
            'issue_type_summary': dict(Counter(i.issue_type for i in items)),
            'risk_findings': [asdict(f) for f in findings], 'risk_themes': [asdict(f) for f in findings],
            'risk_theme_count': len(findings), 'finding_count': len(findings), 'aggregated_risk_count': len(findings),
            'risk_finding_summary': e._risk_finding_summary(findings, items),
            'final_dispositions': [asdict(d) for d in dispositions],
            'final_disposition_summary': e._final_disposition_summary(dispositions),
            'final_overview_summary': e._final_overview_summary(findings, dispositions, items),
            'overall_assessment': assessment, 'perspective_resolution': perspective,
            'recommendations': [asdict(r) for r in recommendations],
            'manual_review_items': [asdict(i) for i in items if i.needs_manual_review],
            'manual_review_summary': {'manual_review_count': sum(i.needs_manual_review for i in items)},
            'result': markdown, 'profile': profile.to_dict(), 'release_quality_gate': gate,
            'loan_shared_fact_consistency_gate': gate, 'system_metadata': metadata,
            'structured_fact_debug': store.public(), 'contract_facts': {'source': 'VerifiedFactStore', 'facts': store.snapshot()},
            'deterministic_analysis': {'loan_costs': costs},
            'fact_migration': {'contract_type': 'loan', 'mode': 'VERIFIED_FACTS',
                'verified_factstore_only': True, 'unmigrated_nodes': [], 'legacy_stages_called': []},
            'llm_enabled': True, 'llm_status': {'provider': 'deepseek', 'mode': 'STRUCTURED_FACTS'},
            'judge_source_summary': {'verified_facts': len(items)},
            'clause_count': len(store.clause_ids),
            'report_generation_decision': {'status': 'GENERATED'},
            'production_path_trace': {'run_mode': 'review', 'pipeline': 'loan_verified', 'fact_source': 'VerifiedFactStore'}})
        from review_v2.report_statistics import statistics_gate
        result['statistics_consistency_gate'] = statistics_gate(result)
        if result['statistics_consistency_gate']['status'] != 'REPORT_READY':
            fail('LOAN_REPORT_STATISTICS_DRIFT', actual=result['statistics_consistency_gate']['failures'])
        return result


def run(text, contract_type='loan', **kwargs):
    source = strip_non_contract_tail(text)
    clauses = parse_contract_clauses(source)
    store = extract_verified(source, clauses, schema())
    result = report(store, profile=kwargs.get('profile'), include_low_risk=kwargs.get('include_low_risk', True))
    from review_v2.fact_routing import CURRENT_ROUTE
    route = CURRENT_ROUTE.get()
    if route is not None:
        result['selected_contract_type'] = route.selected_type
        result['domain_selection_resolution'] = route.selection.to_public_dict()
    return result
