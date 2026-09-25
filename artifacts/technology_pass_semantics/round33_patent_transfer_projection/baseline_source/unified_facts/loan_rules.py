"""All 48 ordinary-loan decisions over verified facts. No source-text argument.

The checklist, atomic propositions, applicability and LPR policy remain the
existing business definitions. This module replaces their extraction inputs.
"""
from review_v2.loan_contract_checklist import get_loan_checklist
from review_v2.loan_facts import PROFILES, OPTIONAL_NODES
from review_v2.loan_costs import EXTERNAL_FACT_NODES
from review_v2.unified_facts.loan import project_shared
from review_v2.unified_facts.loan_bindings import node_concepts, COST_CONCEPTS
from review_v2.unified_facts.loan_costs import analyze, evidence
from review_v2.unified_facts.store import rule_context

PENDING = {'UNKNOWN', 'UNCERTAIN', 'CONFLICT', 'DEFERRED'}


def evaluate(store):
    from review_v2.engine import ReviewItemResult
    with rule_context(store):
        shared, costs = project_shared(store), analyze(store)
        items = []
        for checkpoint in get_loan_checklist():
            node = checkpoint.node_id
            concepts = node_concepts(node)
            if node in {'loan_early_repayment_right', 'loan_unreasonable_early_repayment_penalty'}:
                concepts = tuple(dict.fromkeys((*concepts, 'loan.early_permission', 'loan.early_prohibited')))
            applicability = shared.applicability(node)
            states = {k: store.state(k) for k in concepts}
            values = {k: store.scalar(k, consumer=node) for k in concepts if not store.schema.concepts[k].multiple}
            rows = evidence(store, concepts, node)
            covered = {k for k in concepts if states[k] == 'PRESENT' and
                       (store.schema.concepts[k].kind != 'boolean' or values.get(k) is True)}
            uncertain = {k for k in concepts if states[k] in PENDING}
            permission_conflict = (values.get('loan.early_permission') is True and values.get('loan.early_prohibited') is True)
            trace = {'verified_factstore_only': True, 'input_concepts': list(concepts),
                'fact_states': states, 'review_polarity': checkpoint.polarity,
                'loan_shared_facts': shared.values, 'review_nature': checkpoint.review_nature}
            reason = ''
            if applicability['applicable'] is False:
                status, reason = '不适用', applicability['reason']
                rows = []
            elif applicability['applicable'] is None:
                status, reason = '待核验', applicability['reason']
            elif permission_conflict:
                status, reason = '待核验', '已核验事实同时包含允许和绝对禁止提前还款，存在冲突，需确认适用范围。'
                trace['derived_fact_state'] = 'CONFLICT'
            elif node == 'loan_financial_private_distinction':
                status = '通过' if covered else '待核验'
                reason = '已核验贷款人主体性质，用于金融借款与民间借贷分流。' if covered else '贷款人主体性质尚未确定，不能确认专项规则适用；不要求合同添加法律分类语句。'
            elif node in EXTERNAL_FACT_NODES:
                status = '风险条款' if covered else '待核验'
                reason = ('合同文本发现需核验的风险线索，外部事实尚未核实。' if covered else
                    '合同文本未发现异常，相关实际事实需结合资金来源、历史放贷行为、实际用途等核验；不能据此确认相关风险事实不存在。')
                trace['external_fact_assessment'] = {'external_fact_status': 'NOT_VERIFIED',
                    'text_assessment': 'RISK_INDICATOR_FOUND' if covered else 'UNRESOLVED' if uncertain else 'NO_RISK_INDICATOR_FOUND',
                    'evidence': rows, 'reason': reason}
                trace['review_nature'] = 'EXTERNAL_FACT_VERIFICATION'
            elif node == 'loan_interest_lpr_cap':
                assessment = costs['judicial_protection']
                status = {'PASS': '通过', 'RISK': '风险条款', 'PENDING': '待核验'}[assessment['status']]
                reason = assessment['reason']
                trace['loan_cost_assessment'] = costs
                rows = costs['evidence']
            elif checkpoint.kind == 'forbidden':
                if node == 'loan_unreasonable_early_repayment_penalty':
                    covered.discard('loan.early_permission')
                    if states.get('loan.early_permission') == 'PRESENT' and values.get('loan.early_permission') is False:
                        covered.add('loan.early_permission')
                # Presence of a financing charge is a risk indicator, not a
                # model finding that it exceeds the statutory cap.
                status = '风险条款' if covered else '待核验' if uncertain else '通过'
                if node == 'loan_hidden_fee_over_cap':
                    reason = ('发现具体融资收费安排，应核算与利息合计的实际融资成本；存在收费本身不等于已经超限。'
                              if covered else '全文核验未发现实际收取融资费用的安排。')
                elif not covered and not uncertain:
                    reason = '全文事实核验未发现该项不利约定；否定风险的表述不作为正向风险证据。'
                if not covered:
                    rows = []
                else:
                    rows = [r for r in rows if set(r['supports_element_ids']) & covered]
            else:
                required = set(node_concepts(node))
                status = '通过' if required <= covered else '部分覆盖' if covered & required or rows else '待核验' if uncertain else '缺失'
                if uncertain and not covered:
                    status = '待核验'
                if node == 'loan_principal_amount' and values.get('loan.principal'):
                    if values['loan.principal']['amount'] <= 0:
                        status, reason = '风险条款', '借款本金非正数，需核对合同金额。'
                if node == 'loan_early_repayment_right' and states['loan.early_permission'] == 'PRESENT' and values['loan.early_permission'] is False:
                    status, reason = '风险条款', checkpoint.risk_point_missing
                if node == 'loan_early_repayment_right' and values.get('loan.early_prohibited') is True:
                    status, reason = '风险条款', checkpoint.risk_point_missing
            # Overdue contractual completeness is independent of LPR review.
            # The latter must not turn a complete charge clause into a gap.
            if node in {'loan_repayment_deadline', 'loan_limitation_start'}:
                trace['shared_fact_consumption'] = {'fact_id': 'loan.maturity',
                    'source_review': 'L-06-01', 'evidence_ids': [e['evidence_id'] for e in rows]}
            optional = node in OPTIONAL_NODES and (node == 'loan_repayment_offset_order' or not shared.values['limitation_risk'])
            trace['optional_without_specific_exposure'] = optional
            if node == 'loan_repayment_offset_order':
                trace['default_law_assessment'] = {'status': 'CLEAR_DEFAULT', 'source': '民法典第561条'}
            # Preserve the existing low residual severity when service address
            # and change notice are covered but a collection channel is absent.
            if node == 'loan_notice_service_method' and status == '部分覆盖':
                optional = {'loan.element.loan_service_address', 'loan.element.loan_address_change_notice'} <= covered
            active_risk = status in {'缺失', '部分覆盖', '风险条款'}
            severity = ('LOW' if optional else {'高': 'HIGH', '中': 'MEDIUM', '低': 'LOW'}[checkpoint.risk_level]) if active_risk else 'NONE'
            priority = {'HIGH': 'A_CORE', 'MEDIUM': 'B_PRACTICAL', 'LOW': 'C_OPTIMIZATION', 'NONE': 'NONE'}[severity]
            if status == '通过':
                reason = reason or f'已核验事实覆盖“{checkpoint.title}”的合同安排。'
            elif status == '缺失':
                reason = reason or checkpoint.risk_point_missing
            elif status == '部分覆盖':
                reason = reason or '已存在相关安排，尚未确认：' + '、'.join(store.schema.concepts[k].description for k in concepts if k not in covered)
            elif status == '待核验':
                reason = reason or '已核验的抽取结果仍存在未知、冲突或未来待定安排，不能判定为完全缺失或通过。'
            else:
                reason = reason or checkpoint.risk_point_present
            elements = [{'element_id': k, 'proposition': store.schema.concepts[k].description,
                'status': 'COVERED' if k in covered else 'NOT_APPLICABLE' if status == '不适用' else 'UNKNOWN' if states.get(k) in PENDING else 'MISSING',
                'fact_state': store.state(k),
                'fact_ids': [f['fact_id'] for f in store.snapshot() if f['concept'] == k]}
                for k in node_concepts(node)]
            if checkpoint.kind == 'forbidden' or node in EXTERNAL_FACT_NODES or 'loan_cost_assessment' in trace:
                elements = []  # These are predicates/assessments, not required clauses.
            issue = '外部事实核验' if trace['review_nature'] == 'EXTERNAL_FACT_VERIFICATION' and status == '待核验' else {
                '缺失': '完全缺失', '部分覆盖': '条款缺陷'}.get(status, status)
            item = ReviewItemResult(item_id=checkpoint.item_id, node_id=node, title=checkpoint.title,
                risk_level={'HIGH': '高', 'MEDIUM': '中', 'LOW': '低', 'NONE': '低'}[severity],
                status=status, risk_point_description=reason,
                suggested_clause_example=checkpoint.suggested_clause if active_risk else '',
                legal_basis_index=checkpoint.legal_basis,
                legal_consequence_if_missing=checkpoint.legal_consequence_if_missing if active_risk else '',
                applicable_if=checkpoint.applicable_if, matched_terms=[], coverage_status=status,
                issue_type=issue, evidence_clauses=rows,
                evidence_location='；'.join(dict.fromkeys(e['location'] for e in rows)),
                reasoning_summary=reason, judge_source='verified_facts', applicability=applicability,
                decision_trace=trace, coverage_elements=elements, risk_severity=severity,
                action_priority=priority, needs_manual_review=status == '待核验',
                coverage_presence={'通过': 'PRESENT', '部分覆盖': 'PARTIAL', '缺失': 'MISSING', '不适用': 'NOT_APPLICABLE'}.get(status, 'UNKNOWN'),
                risk_status='RISK' if active_risk else 'UNKNOWN' if status == '待核验' else 'NONE',
                fact_dependencies=list(concepts), risk_group=node)
            store.record_decision(node, 'RULE_DECISION', {'status': status, 'severity': severity,
                'elements': elements, 'evidence_ids': [e['evidence_id'] for e in rows]}, concepts)
            items.append(item)
        return items, costs
