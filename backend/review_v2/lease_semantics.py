"""Declarative lease requirements evaluated once against the complete corpus.

No review IDs or document-specific text: shared fact keys identify a legal
relationship, and consumers receive the same source-bound evidence.
"""
import re
import hashlib
import json
from copy import deepcopy


def evidence_identity(source):
    row = deepcopy(source)
    quote = next((str(row[k]) for k in ('quoted_text', 'quote', 'text', 'original_excerpt') if row.get(k)), '')
    row['quoted_text'] = quote
    row['clause_node_id'] = row.get('clause_node_id') or row.get('clause_id')
    row['clause_number'] = row.get('clause_number') or row.get('location')
    identity = [row['clause_node_id'], row['clause_number'], quote,
                sorted(row.get('supporting_element_ids') or row.get('supports_element_ids') or [])]
    if not row.get('evidence_id') or str(row['evidence_id']) == 'None':
        row['evidence_id'] = 'SYN-' + hashlib.sha256(json.dumps(identity, ensure_ascii=False).encode()).hexdigest()[:20]
    return row


def rule_evidence_package(item):
    """Project atomic proof, never a related theme's entire evidence pool."""
    requirements = {r['element_id']: r for r in (item.decision_trace or {}).get('semantic_requirements', [])}
    audits = {r['element_id']: r for r in (item.decision_trace or {}).get('element_absence_searches', [])}
    rows = []
    for element in item.coverage_elements:
        key = element['element_id']
        audit = audits.get(key, {})
        if element.get('status') == 'MISSING' and audit.get('result') == 'NOT_FOUND' and not audit.get('supporting_evidence'):
            rows.append(evidence_identity({'source_type': 'SEARCH_AUDIT', 'supporting_element_ids': [key],
                'supporting_review_ids': [item.item_id], 'location': '全文逐要素检索',
                'text': '未找到正向事实：' + str(element.get('proposition') or key),
                'result': 'no_positive_fact', 'searched_document_hash': audit.get('searched_document_hash'),
                'search_targets': audit.get('search_targets', [])}))
        if element.get('status') not in {'COVERED', 'PARTIALLY_COVERED', 'ADVERSE', 'CONFLICTING'}:
            continue
        for source in item.evidence_clauses:
            bound = source.get('supports_element_ids') or source.get('supporting_element_ids') or []
            if key in requirements:
                valid = supports(requirements[key], source)
            else:
                valid = key in bound and source.get('clause_id') and source.get('location')
            if not valid or source.get('source_type') == 'SEARCH_AUDIT':
                continue
            row = evidence_identity(source)
            if key in requirements:
                # Verify and publish the same selected span. Retrieval context
                # is not an interchangeable source of neighbouring sentences.
                proof_text = str(source.get('quote') or source.get('text') or '')
                if requirements[key].get('preserve_full_quote'):
                    original = str(source.get('raw_text') or (source.get('source_span') or {}).get('raw_text') or proof_text)
                    if supports(requirements[key], {**source, 'text': original, 'quote': original}):
                        proof_text = original
                row.update(text=proof_text, quote=proof_text, quoted_text=proof_text, original_excerpt=proof_text)
                for sentence in re.findall(r'[^。]+[。]?', proof_text):
                    if requirements[key].get('preserve_full_quote'):
                        break
                    if supports(requirements[key], {**source, 'text': sentence, 'quote': sentence}):
                        row.update(text=sentence, quote=sentence, quoted_text=sentence, original_excerpt=sentence)
                        break
            row.update(supporting_element_ids=[key], supports_element_ids=[key], element_ids=[key],
                       supporting_review_ids=[item.item_id], support_labels=[element.get('proposition') or key])
            # Identity includes exact atomic ownership, not the source pool's tags.
            row.pop('evidence_id', None)
            rows.append(evidence_identity(row))
    unique = {r['evidence_id']: r for r in rows}
    return {'bundle_id': 'RULE-' + item.item_id, 'items': sorted(unique.values(), key=lambda r: -r.get('entailment_score', 0))}


def requirement(key, description, *patterns):
    return dict(element_id=key, proposition=description, semantic_patterns=patterns)


TRIGGER = requirement('termination_trigger', '合同约定解除事由或触发条件',
    r'(?:逾期|欠租|违约|催告|擅自|无法).{0,100}(?:有权|可以|可).{0,12}解除(?:本)?合同',
    r'(?:有下列情形|发生下列情形).{0,50}(?:有权|可以|可).{0,8}(?:解除|终止)')
EARLY = requirement('early_exit', '提前退租或提前收回的条件与后果',
    r'(?:提前退租|提前收回).{0,100}(?:通知|违约金|赔偿|同意)',
    r'(?:承租人|乙方).{0,20}(?:需|要求|拟)提前解除.{0,70}(?:通知|违约金|同意)')
EARLY_PRESENCE = {**deepcopy(EARLY), 'element_id': 'early_exit_presence', 'proposition': '存在提前退出约定'}
# Conjunctive requirements must be proved in a single bounded clause. A
# monetary clause elsewhere (rent, deposit, late payment) cannot complete it.
EARLY['evidence_unit'] = 'clause'
EARLY['required_fact_patterns'] = {
    'exit_condition': [r'(?:提前退租|提前收回|提前解除).{0,100}(?:通知|同意|提前\s*\d+日)',
                       r'(?:中途|提前)?擅自(?:退租|收回房屋)'],
    'exit_consequence': [r'(?:应|须|需).{0,90}(?:支付|承担).{0,25}(?:违约金|赔偿)',
                         r'(?:无需|不必|免于).{0,15}(?:支付|承担).{0,20}(?:违约金|赔偿)',
                         r'(?:提前退租|提前收回|提前解除).{0,120}(?:退还押金|结清租金|返还剩余租金)',
                         r'(?:提前退租|提前收回|提前解除).{0,120}(?:按|以).{0,40}(?:实际使用|未结费用|空置损失).{0,40}结算'],
}
PROFILES = {
    'use_restriction': [requirement('agreed_use_obligation', '承租人按约定用途使用房屋的约束', r'(?:乙方|承租人).{0,20}(?:不得|禁止).{0,10}变更.{0,8}(?:租赁)?用途', r'(?:乙方|承租人).{0,20}(?:按照|按).{0,10}(?:租赁)?用途.{0,10}使用')],
    'sale_notice_preemption': [
        requirement('sale_notice', '出租房屋出售时通知承租人', r'(?:甲方|出租人).{0,35}(?:出卖|出售).{0,40}(?:通知|告知).{0,12}(?:乙方|承租人)(?!解除|终止)'),
        requirement('preemption_right', '承租人同等条件优先购买权', r'(?:乙方|承租人).{0,25}享有.{0,30}同等条件.{0,15}优先购买')],
    'move_in_defect_notice': [requirement('initial_defect_notice', '入住或交接时瑕疵的告知及记录', r'(?:入住|交接|交付).{0,35}(?:发现|已有).{0,15}(?:瑕疵|缺陷|损坏).{0,40}(?:告知|通知|记录|列明)')],
    'landlord_no_objection': [requirement('initial_defect_objection', '出租人收到既有瑕疵通知后的异议或核验安排', r'(?:甲方|出租人).{0,30}(?:瑕疵|缺陷|损坏).{0,40}(?:异议|核验|未反馈)', r'(?:瑕疵|缺陷|损坏).{0,35}(?:甲方|出租人).{0,30}(?:未提出异议|核验|未反馈)')],
    'burden_of_proof': [requirement('damage_proof_burden', '出租人扣款时证明损坏事实、原因和金额的责任', r'(?:甲方|出租人).{0,35}(?:扣款|扣除|损坏).{0,45}(?:举证|提供.{0,15}证据|证明.{0,20}(?:原因|金额|事实))')],
    'deposit_amount': [
        requirement('deposit_obligation', '约定租赁押金收付义务', r'(?:支付|交纳|缴纳|交付).{0,15}押金|押金.{0,25}(?:支付|交纳|缴纳|交付)', r'收到押金.{0,35}出具.{0,15}(?:凭证|收据)'),
        requirement('deposit_sum', '明确押金金额', r'押金(?:为|是|人民币|金额|：|:|\s)*[\d,，]+(?:\.\d+)?元|押金.{0,12}[一二三四五六七八九十两]+个月.{0,8}租金')],
    'procedure_jurisdiction': [requirement('dispute_forum', '约定争议管辖法院或仲裁机构', r'(?:向|由).{0,45}(?:人民法院|仲裁委员会).{0,25}(?:起诉|诉讼|管辖|仲裁)')],
    'ownership_authority': [requirement('ownership_document', '列明房屋权属证明及权利人', r'所有权人为.{2,60}', r'(?:权属证明编号|产证编号|不动产权证号).{0,50}\d+')],
    'sublease_rule': [requirement('sublease_consent', '转租的出租人同意条件', r'(?:未经|经).{0,15}(?:甲方|出租人).{0,10}同意.{0,10}转租')],
    'rent_arrears_breach': [requirement('arrears_remedy', '欠租催告及违约救济', r'(?:逾期|未足额支付).{0,70}(?:催告|解除|违约责任)')],
    'termination_period': [requirement('termination_exercise_period', '解除权行使期限', r'(?:知道|应当知道).{0,70}(?:六个月|一年|\d+日).{0,30}解除', r'解除权.{0,35}(?:期限|期间|消灭)')],
    'expropriation_demolition': [requirement('expropriation_event', '房屋征收征用的终止事由', r'房屋被依法(?:征收|征用)', r'(?:征收|征用|拆迁).{0,40}(?:终止|解除)')],
    'maintenance_duty': [requirement('landlord_repair', '出租人对正常使用情况下房屋设施的维修义务', r'(?:甲方|出租人).{0,90}承担.{0,70}维修义务', r'(?:正常损耗|自然老化).{0,45}(?:甲方|出租人).{0,15}(?:维修|修理)')],
    'contract_validity': [requirement('severability', '无效条款与其他合同条款效力的关系', r'部分条款无效.{0,40}不影响其他条款.{0,10}效力')],
    'natural_wear': [requirement('wear_exclusion', '正常使用的自然损耗不属于承租人赔偿损坏', r'(?:正常使用|自然损耗|自然使用痕迹).{0,35}(?:除外|不视为|不承担|不属于)')],
    'rent_payment': [requirement('rent_payment_arrangement', '租金支付方式及履行节点', r'(?:转账|支付租金|付清租金).{0,50}(?:到账|每月|日前|付款)', r'(?:每月|每季).{0,40}(?:支付|付清).{0,10}租金')],
    'attachments': [requirement('annex_reference', '合同列明房屋交接等附件', r'详见附件.{0,20}(?:交割单|交接单|清单)')],
    'no_damage_return': [
        requirement('deposit_return', '押金返还义务', r'押金.{0,100}(?:返还|退还)|(?:返还|退还).{0,20}押金'),
        requirement('undamaged_return', '房屋无损坏或扣除有依据费用后返还押金', r'(?:无损坏|没有损坏|无欠费).{0,60}(?:押金|保证金).{0,25}(?:返还|退还)', r'(?:抵扣|扣除)后.{0,20}剩余.{0,35}返还')],
    'damage_definition': [
        requirement('wear_exclusion', '正常使用的自然损耗不属于承租人赔偿损坏', r'(?:正常使用|自然损耗|自然使用痕迹).{0,35}(?:除外|不视为|不承担|不属于)'),
        requirement('fault_damage', '保管或使用不当造成损坏的责任', r'(?:乙方|承租人).{0,15}(?:保管|使用)不当.{0,25}(?:毁坏|损坏).{0,45}(?:维修|更换|赔偿)')],
    'tenant_fault_damage': [requirement('fault_damage', '保管或使用不当造成损坏的责任', r'(?:乙方|承租人).{0,15}(?:保管|使用)不当.{0,25}(?:毁坏|损坏).{0,45}(?:维修|更换|赔偿)')],
    'reasonable_repair_cost': [
        requirement('repair_necessary', '维修费用限于必要支出', r'(?:维修|修理).{0,15}(?:费用|支出).{0,25}必要|必要.{0,10}(?:维修|修理).{0,10}(?:费用|支出)'),
        requirement('repair_reasonable', '维修费用合理性约束', r'合理.{0,8}(?:维修|修理)费用|(?:维修|修理)费用.{0,25}合理'),
        requirement('repair_actual', '维修费用以实际发生为限', r'(?:维修|修理)费用.{0,35}(?:实际发生|实际支付|实际支出)|实际(?:发生|支付|支出).{0,15}(?:维修|修理)费用'),
        requirement('repair_voucher', '维修费用单据向相对方提供或核验', r'(?:提供|提交|出示|核验).{0,30}(?:维修|修理).{0,20}(?:发票|单据|凭证|报价单)|(?:维修|修理).{0,20}(?:发票|单据|凭证|报价单).{0,20}(?:提供|提交|出示|核验)')],
    'handover_evidence': [requirement('signed_handover', '双方确认房屋交接清单作为交付返还证据', r'(?:双方|甲乙双方).{0,50}(?:交割单|交接单|交接清单).{0,30}(?:签名|签字|盖章|确认)', r'(?:交割单|交接清单).{0,40}双方.{0,15}(?:签字|确认)')],
    'agreed_termination': [TRIGGER],
    'termination_notice': [TRIGGER,
        requirement('termination_notice_delivery', '解除通知的书面方式或送达渠道', r'(?:解除|退租).{0,40}(?:书面|通知)', r'(?:通知|送达).{0,50}(?:专人|邮寄|电子邮件|快递|书面)'),
        requirement('termination_effective_time', '解除通知到达或解除生效节点', r'(?:解除|通知|送达).{0,80}(?:到达|签收|生效|视为送达)')],
    'early_surrender': [EARLY],
    'illegal_building': [requirement('lawful_lease_basis', '出租人保证房屋合法出租', r'(?:出租|房屋).{0,50}(?:不违反法律|不存在.{0,15}限制出租|合法出租|不属于违法建筑)')],
    'excessive_deduction': [
        requirement('loss_basis', '赔偿或扣款与实际损失对应', r'(?:赔偿金额|赔偿额|违约金|扣款).{0,50}(?:相当于|以).{0,20}损失'),
        requirement('adjustment', '过高违约金的调整机制', r'(?:违约金|扣款|约定金额).{0,70}(?:过高|超过损失|高于实际损失).{0,40}(?:调整|调减)')],
    'term_expiry_settlement': [
        requirement('expiry_settlement', '合同终止后的费用及押金结算', r'(?:合同终止|租期届满).{0,90}(?:结清|结算|返还押金)'),
        requirement('expiry_handover', '到期或终止时的房屋交接', r'(?:返还|交还|交接).{0,25}房屋|房屋.{0,40}(?:返还|交割单)')],
    'deposit_return_deadline': [
        requirement('deposit_return', '押金返还义务', r'押金.{0,100}(?:返还|退还)|(?:返还|退还).{0,20}押金'),
        requirement('return_deadline', '押金返还的具体期限',
                    r'(?:\d+|[一二三四五六七八九十百]+)(?:个)?(?:工作)?日内.{0,35}(?:返还|退还).{0,20}押金',
                    r'押金.{0,45}(?:\d+|[一二三四五六七八九十百]+)(?:个)?(?:工作)?日内.{0,35}(?:返还|退还)',
                    r'(?:\d+|[一二三四五六七八九十百]+)(?:个)?(?:工作)?日内.{0,12}(?:将|把)?押金.{0,35}(?:返还|退还)')],
    'indefinite_lease': [
        requirement('post_expiry_continue_use', '期满后继续使用房屋', r'(?:届满|期满).{0,35}(?:继续使用|继续居住|继续承租)'),
        requirement('no_objection_or_rent_acceptance', '期满继续使用时出租人未异议或继续收租', r'(?:届满|期满|继续使用|不定期).{0,80}(?:未提出异议|没有异议|继续收租|接受租金)'),
        requirement('reasonable_notice', '不定期租赁解除的通知安排', r'不定期.{0,80}(?:提前|合理期限|通知)')],
    'force_majeure': [
        requirement('force_event', '不可抗力造成不能使用时的处理',
                    r'不可抗力.{0,90}(?:不能|无法).{0,12}使用.{0,70}(?:有权|可以|可).{0,30}(?:解除|终止)合同',
                    r'不可抗力.{0,40}协商.{0,25}(?:延期履行|部分履行|终止|解除)'),
        requirement('force_notice', '不可抗力的通知和证明', r'不可抗力.{0,180}(?:提供|提交|出具).{0,20}证明'),
        requirement('force_settlement', '不可抗力后的费用结算', r'不可抗力.{0,130}(?:结算|返还|退还|减免)')],
    'deposit_offset_order': [
        requirement('offset_items', '押金可抵扣的费用项目', r'(?:未结清|欠付|欠费|费用|租金).{0,70}押金.{0,20}(?:抵扣|扣除)', r'押金.{0,20}(?:抵扣|扣除).{0,60}(?:租金|费用|维修)'),
        requirement('offset_order', '押金抵扣顺序', r'(?:押金|抵扣).{0,50}(?:依次|首先|先抵扣|抵扣顺序|扣除顺序)')],
    'safety_risk': [
        requirement('safety_trigger', '房屋危及人身财产安全时的保护', r'(?:房屋|该房屋).{0,25}(?:危及|安全隐患|危险).{0,30}(?:安全|人身|财产|搬离)'),
        requirement('safety_notice', '安全风险发生时的通知或避险', r'(?:安全隐患|危及|危险房屋).{0,90}(?:通知|搬离|避险|安置)'),
        requirement('safety_settlement', '安全风险退出后的费用结算', r'(?:安全隐患|危及|危险房屋).{0,100}(?:结算|返还|退还)')],
}

PROFILES['force_majeure'][1]['required_fact_patterns'] = {
    'event_notification': [r'(?:应|须|及时).{0,12}通知(?:另|对)一?方'],
    'event_proof': [r'(?:提供|提交|出具).{0,20}证明'],
}

# Equivalent affirmative allocation of natural wear to the landlord.
for _node in ('natural_wear', 'damage_definition'):
    _wear = next(e for e in PROFILES[_node] if e['element_id'] == 'wear_exclusion')
    _wear['semantic_patterns'] += (r'(?:自然老化|正常损耗).{0,60}(?:甲方|出租人).{0,20}(?:维修|承担费用)',)

# Applicability is declarative; the evaluator can consume any fact key or role.
# The costs assessed here are tenant damage deductions, not reimbursement of
# the landlord's own maintenance obligation. All predicates bind one sentence.
for _cost_requirement in PROFILES['reasonable_repair_cost']:
    _cost_requirement['scenario_patterns'] = [r'(?:押金|保证金).{0,35}(?:扣|抵)|(?:扣|抵).{0,35}(?:押金|保证金)']
    _cost_requirement['responsibility_patterns'] = [r'(?:乙方|承租人).{0,35}(?:造成|导致|损坏|损害|赔偿)|(?:损坏|损害).{0,25}(?:乙方|承租人)']
    _cost_requirement['excluded_scenario_patterns'] = [r'(?:甲方|出租人).{0,12}维修责任']


CONDITIONS = {
    'tenant_death_successor': {'party': 'tenant', 'types': ['NATURAL_PERSON']},
    'tenant_death_settlement': {'party': 'tenant', 'types': ['NATURAL_PERSON']},
    'lessor_death': {'party': 'landlord', 'types': ['NATURAL_PERSON']},
    'no_early_clause_fallback': {'absent_fact': 'early_exit_presence'},
}


def supports(element, row):
    from review_v2.employment_fact_store import current
    store = current()
    if store is not None and element['element_id'].startswith(('employment_','confidentiality_','nda_','termination_')):
        return store.supports(element, row)
    context = '\n'.join([str(row.get('title') or ''), *row.get('heading_path', [])])
    if any(re.search(p, context) for p in element.get('excluded_context_patterns', ())):
        return False
    if element.get('polarity_policy') == 'PROTECTIVE_RIGHT':
        from review_v2.shareholder_transaction_facts import protection_polarity
        fact = protection_polarity(row.get('quote') or row.get('text', '')) or {}
        if row.get('polarity') in {'RESTRICTIVE','ADVERSE','NEUTRAL'} or fact.get('polarity') in {'RESTRICTIVE','ADVERSE','NEUTRAL'}:
            return False
    if element.get('required_section_types') and row.get('section_type') not in element['required_section_types']:
        return False
    if any(row.get(k) == 'SEARCH_AUDIT' for k in ('source_type', 'evidence_type', 'support_type')) or not row.get('clause_id') or not row.get('location'):
        return False
    bound = row.get('supports_element_ids') or row.get('supporting_element_ids')
    if bound and element['element_id'] not in bound:
        return False
    # A report row may carry the full retrieval clause in text and its selected
    # exact evidence in quote. Verify the published span, not neighbouring text.
    text = row.get('quote') or row.get('text', '')
    # DOCX emphasis markers are presentation metadata. They may be retained in
    # a verified original span, but cannot interrupt the legal predicate being
    # matched (for example, a bold calculation base inside a formula).
    text = re.sub(r'\*\*|__', '', text)
    context = element.get('required_context')
    if context and not re.search(context['direct'], text):
        if not (re.search(context['anaphor'], text)
                and re.search(context['antecedent'], row.get('semantic_parent_context', ''))):
            return False
    if element.get('preceding_context_pattern') and not re.search(element['preceding_context_pattern'], text+'\n'+row.get('semantic_parent_context','')):
        return False
    if any(re.search(p, text, re.S) for p in element.get('excluded_patterns', [])):
        return False
    if not all(any(re.search(p, text, re.S) for p in patterns)
               for patterns in element.get('required_fact_patterns', {}).values()):
        return False
    if not any(element.get(k) for k in ('scenario_patterns', 'responsibility_patterns', 'excluded_scenario_patterns')):
        return (any(re.search(p, text, re.S) for p in element['semantic_patterns'])
                or any(re.search(p['context'], '\n'.join(row.get('heading_path') or []))
                       and re.search(p['predicate'], text, re.S)
                       for p in element.get('contextual_patterns', [])))
    for sentence in re.split(r'[。；;]', text):
        if any(re.search(p, sentence, re.S) for p in element.get('excluded_scenario_patterns', [])):
            continue
        if not all(not element.get(field) or any(re.search(p, sentence, re.S) for p in element[field])
                   for field in ('scenario_patterns', 'responsibility_patterns')):
            continue
        if any(re.search(p, sentence, re.S) for p in element['semantic_patterns']):
            return True
    return False


def consistency_failures(items):
    from review_v2.shareholder_transaction_facts import source_consistency_failures
    failures, shared = source_consistency_failures(items), {}
    from review_v2.noncompete_semantics import consistency_failures as prerequisite_failures
    failures.extend(prerequisite_failures(items))
    from review_v2.contract_effects import consistency_failures as effect_failures
    failures.extend(effect_failures(items))
    for item in items:
        trace = item.decision_trace or {}
        declared_law=trace.get('applicable_legal_proposition')
        if declared_law:
            expected_articles={r['article'] for r in declared_law['references']}
            actual_articles=set(re.findall(r'第\d+条',getattr(item,'legal_basis_index','')))
            if actual_articles != expected_articles:
                failures.append({'requirement':'SCENARIO_LEGAL_BASIS_CONFLICT','root_cause':item.item_id})
        external = [a for a in trace.get('requirement_kind_assessments',[]) if a.get('status')=='PENDING_VERIFICATION']
        if external and (item.coverage_status in {'通过','PASS','COVERED'} or not getattr(item,'needs_manual_review',False)):
            failures.append({'requirement':'UNVERIFIED_EXTERNAL_FACT_PASSED','root_cause':item.item_id})
        formulas = trace.get('settlement_formula_analysis',[])
        if any(f['status']=='AMBIGUOUS' for f in formulas) and item.coverage_status in {'通过','PASS','不适用'}:
            failures.append({'requirement':'AMBIGUOUS_SETTLEMENT_PASSED','root_cause':item.item_id})
        if item.node_id in {'operation_multiple_penalty','operation_prospective_penalty'} and item.coverage_status=='风险条款':
            if '585' not in str(getattr(item,'legal_basis_index','')):
                failures.append({'requirement':'PENALTY_DIRECT_AUTHORITY_MISSING','root_cause':item.item_id})
        clear_default = trace.get('clear_default_narrative')
        if clear_default:
            for field in ('risk_point_description','legal_consequence_if_missing','reasoning_summary'):
                if re.search(r'(?:能否|权利是否存在|法律关系)[^。；]{0,25}(?:不清|不明确|不确定)', str(getattr(item,field,'') or '')):
                    failures.append({'requirement':'CLEAR_DEFAULT_FALSE_LEGAL_UNCERTAINTY','root_cause':item.item_id+':'+field})
        if (getattr(item, 'applicability', {}) or {}).get('applicability_state') == 'CONDITIONAL_NOT_TRIGGERED':
            if item.coverage_status != '不适用':
                failures.append({'requirement':'UNTRIGGERED_RULE_HAS_COVERAGE_RISK','root_cause':item.item_id})

        for concept_id, source_rows in trace.get('shared_concept_facts', {}).items():
            projected = next((e for e in item.coverage_elements if e.get('element_id') == concept_id), None)
            if projected and source_rows and projected.get('status') not in {'COVERED', 'FOUND'}:
                failures.append({'requirement': 'SHARED_FACT_LOST_IN_FINAL_ELEMENT', 'root_cause': item.item_id,
                                 'element_id': concept_id, 'source_clause_ids': [r['clause_id'] for r in source_rows]})
            if projected and projected.get('status') in {'COVERED','FOUND'} and not source_rows:
                failures.append({'requirement': 'FINAL_ELEMENT_WITHOUT_SHARED_FACT', 'root_cause': item.item_id, 'element_id': concept_id})
        if trace.get('priority_positive_adverse_verification'):
            if item.coverage_elements and all(e.get('status') == 'ADVERSE' for e in item.coverage_elements):
                for field in ('reasoning_summary', 'risk_point_description', 'legal_consequence_if_missing', 'suggested_clause_example'):
                    value = str(getattr(item, field, '') or '')
                    if re.search(r'(?:未约定|未列明|未设置|完全缺失)[^。；]{0,30}(?:规则|条款|安排|程序|事由)', value):
                        failures.append({'requirement': 'EXISTING_ADVERSE_CLAUSE_ABSENCE_NARRATIVE', 'root_cause': item.item_id + ':' + field})
            verified = set(trace['priority_positive_adverse_verification'].get('source_clause_ids') or [])
            adverse_rows = [r for r in item.evidence_clauses if r.get('clause_id') in verified and r.get('source_type') != 'SEARCH_AUDIT']
            if not adverse_rows or any(r.get('polarity') == 'PROTECTIVE' or r.get('classification') == 'PROTECTIVE' for r in adverse_rows):
                failures.append({'requirement': 'ADVERSE_RULE_WITHOUT_DIRECT_FACT', 'root_cause': item.item_id})
            protected = {r['clause_id'] for r in trace.get('employment_exit_classification', []) if r.get('classification') == 'PROTECTIVE'}
            if protected & verified:
                failures.append({'requirement': 'PROTECTIVE_CLAUSE_AS_ADVERSE_EVIDENCE', 'root_cause': item.item_id})
            if item.coverage_status == '风险条款' and not getattr(item, 'related_risks', []):
                failures.append({'requirement': 'RISK_CLAUSE_WITHOUT_FINDING', 'root_cause': item.item_id})
        if trace.get('priority_specialized_evaluation') and trace.get('review_mode') == 'ABSENCE_REQUIRED' and item.coverage_status == '风险条款':
            verification = trace.get('priority_adverse_verification') or {}
            ids = set(verification.get('source_clause_ids') or [])
            if not ids or not any(r.get('clause_id') in ids and r.get('text') and r.get('source_type') != 'SEARCH_AUDIT' for r in item.evidence_clauses):
                failures.append({'requirement': 'ADVERSE_RULE_WITHOUT_DIRECT_FACT', 'root_cause': item.item_id})
        for conditional in trace.get('priority_conditional_elements', []):
            if conditional.get('prerequisite_status') == 'FALSE':
                projected = next((e for e in item.coverage_elements if e['element_id'] == conditional['element_id']), {})
                if projected.get('status') != 'NOT_APPLICABLE' or projected.get('risk_relevant') is not False:
                    failures.append({'requirement': 'UNTRIGGERED_CONDITIONAL_ELEMENT_RISK', 'root_cause': item.item_id})
        if trace.get('semantic_contract_domain') == 'lease' and item.coverage_status == '通过' and trace.get('review_mode') != 'ABSENCE_REQUIRED':
            if not any(e.get('status') in {'COVERED', 'PARTIALLY_COVERED'} and e.get('source_spans') and e.get('source_locations') for e in item.coverage_elements):
                failures.append({'requirement': 'PASS_WITHOUT_POSITIVE_ELEMENT_EVIDENCE', 'root_cause': item.item_id})
        if item.coverage_status == '不适用':
            if item.needs_manual_review or item.related_risks:
                failures.append({'requirement': 'NA_HAS_ACTIONABLE_STATE', 'root_cause': item.item_id})
            continue
        requirements = trace.get('semantic_requirements', [])
        for requirement in requirements:
            key = requirement['element_id']
            positive = [r for r in item.evidence_clauses if supports(requirement, r)]
            element = next((e for e in item.coverage_elements if e['element_id'] == key), {})
            for row in item.evidence_clauses:
                bound = row.get('supports_element_ids') or row.get('supporting_element_ids') or []
                if key not in bound or row.get('source_type') == 'SEARCH_AUDIT':
                    continue
                # The displayed quote must independently entail the bound fact,
                # even when a longer internal text contains valid evidence.
                for field in ('quote', 'quoted_text', 'original_excerpt'):
                    if row.get(field) and not supports(requirement, {**row, 'text': row[field], 'quote': row[field]}):
                        failures.append({'requirement': 'DISPLAY_QUOTE_ELEMENT_CONFLICT', 'root_cause': item.item_id + ':' + key})
            expected = ('ADVERSE' if trace.get('priority_positive_adverse_verification') else 'COVERED') if positive else 'MISSING'
            shared.setdefault(key, set()).add(element.get('status'))
            if element.get('status') != expected:
                failures.append({'requirement': 'SHARED_ELEMENT_EVIDENCE_CONFLICT', 'root_cause': item.item_id + ':' + key})
            for audit in trace.get('element_absence_searches', []):
                if audit.get('element_id') == key and ((audit.get('result') == 'FOUND') != bool(positive)):
                    failures.append({'requirement': 'SEARCH_AUDIT_ELEMENT_CONFLICT', 'root_cause': item.item_id + ':' + key})
        if requirements and trace.get('review_mode') != 'ABSENCE_REQUIRED':
            statuses = [e.get('status') for e in item.coverage_elements
                        if e.get('status') != 'NOT_APPLICABLE' and e.get('risk_relevant') is not False]
            any_covered = any(e.get('status') == 'COVERED' for e in item.coverage_elements)
            expected = '风险条款' if trace.get('priority_positive_adverse_verification') and 'ADVERSE' in statuses else '通过' if statuses and all(s == 'COVERED' for s in statuses) else '部分覆盖' if any_covered else '缺失'
            pending_external = any(a.get('requirement_kind') == 'EXTERNAL_VERIFICATION'
                and a.get('status') == 'PENDING_VERIFICATION'
                for a in trace.get('requirement_kind_assessments', []))
            if expected == '通过' and pending_external and item.needs_manual_review:
                expected = 'INSUFFICIENT_CONTEXT'
            if item.coverage_status != expected:
                failures.append({'requirement': 'COVERAGE_ELEMENT_STATE_CONFLICT', 'root_cause': item.item_id})
        if item.risk_severity == 'HIGH' and trace.get('economic_evidence_ceiling'):
            assessment = trace.get('economic_evidence_assessment', {})
            if assessment.get('ceiling') != 'HIGH' or not assessment.get('evidence'):
                failures.append({'requirement': 'ECONOMIC_SEVERITY_EXCEEDS_EVIDENCE', 'root_cause': item.item_id})
    for key, statuses in shared.items():
        if {'COVERED', 'MISSING'} <= statuses:
            failures.append({'requirement': 'CROSS_RULE_FACT_STATUS_CONFLICT', 'root_cause': key})
    return [{**f, 'current_status': 'FAIL', 'failure_stage': 'Semantic consistency'} for f in failures]


def corpus_facts(clauses, requirements, *, audit=None):
    from review_v2.employment_fact_store import current
    store = current()
    if store is not None and requirements and all(r['element_id'].startswith(('employment_','confidentiality_','nda_','termination_')) for r in requirements):
        return store.corpus_facts(requirements, audit=audit)
    facts = {}
    for element in requirements:
        key = element['element_id']
        if key in facts:
            continue
        evidence = []
        candidates = []
        for clause_index,clause in enumerate(clauses):
            if clause.section_type not in {'正式合同条款', '附件'}:
                continue
            pattern = r'[\s\S]+' if element.get('evidence_unit') == 'clause' else r'[^。]+[。]?'
            for match in re.finditer(pattern, clause.text):
                quote = match.group().strip()
                row = dict(clause_id=clause.clause_id, location=clause.location, title=clause.title,
                           text=quote, quote=quote, original_excerpt=quote, section_type=clause.section_type,
                           heading_path=list(clause.heading_path or []),
                           source_start=match.start(), source_end=match.end(),
                           supports_element_ids=[key], source_type='CONTRACT_TEXT')
                if element.get('preceding_context_pattern'):
                    for parent in reversed(clauses[:clause_index]):
                        if (parent.heading_path or [''])[0] != (clause.heading_path or [''])[0]:break
                        if re.match(r'\s*[（(][一二三四五六七八九十]+[）)]',parent.text):
                            if re.search(element['preceding_context_pattern'],parent.text):
                                row['semantic_parent_context']=parent.text
                                row['semantic_parent_context_location']=parent.location
                                row['semantic_parent_context_id']=parent.clause_id
                            break
                context = element.get('required_context')
                if context and re.search(context['anaphor'], quote) and not re.search(context['direct'], quote):
                    # Resolve a continuation only to the nearest matching
                    # antecedent in the same enumerated block, never a chapter
                    # title or an arbitrary preceding monetary provision.
                    for parent in reversed(clauses[max(0,clause_index-4):clause_index]):
                        if (parent.heading_path or [''])[0] != (clause.heading_path or [''])[0]:
                            if not (not parent.article_number and not clause.article_number
                                    and parent is clauses[clause_index-1]):break
                        if re.match(r'\s*\d+[、.]', parent.text):break
                        if re.search(context['antecedent'], parent.text):
                            row.update(semantic_parent_context=parent.text,
                                       semantic_parent_context_location=parent.location,
                                       semantic_parent_context_id=parent.clause_id)
                            break
                if element.get('polarity_policy') == 'PROTECTIVE_RIGHT':
                    from review_v2.shareholder_transaction_facts import protection_polarity
                    row.update(protection_polarity(quote) or {})
                accepted = supports(element, row)
                if audit is not None:
                    from review_v2.semantic_relations import slot_trace
                    candidates.append({**deepcopy(row), 'accepted': accepted,
                        'score': 1.0 if accepted else 0.0, 'threshold': 'ALL_REQUIRED_RELATIONS',
                        'relation_slots': slot_trace(element, quote),
                        'matched_patterns': [p for p in element['semantic_patterns'] if re.search(p,quote,re.S)],
                        'rejected_patterns': [p for p in element.get('excluded_patterns',[]) if re.search(p,quote,re.S)],
                        'decision_function': 'review_v2.lease_semantics.supports',
                        'result': 'FOUND' if accepted else 'NOT_FOUND'})
                if accepted:
                    if element.get('quote_match_only'):
                        matches=[m for p in element['semantic_patterns'] if (m:=re.search(p,quote,re.S))]
                        if matches:
                            proof=max(matches,key=lambda m:len(m.group()))
                            row.update(text=proof.group(),quote=proof.group(),original_excerpt=proof.group(),
                                       source_start=match.start()+proof.start(),source_end=match.start()+proof.end())
                    direct=any(re.search(p,quote,re.S) for p in element['semantic_patterns'])
                    heading_only=quote.strip()==str(clause.title or '').strip()
                    numeric=bool(re.search(r'\d|[一二两三四五六七八九十]+(?:年|月|日)',quote))
                    row['entailment_score']=10 if heading_only else (100 if numeric else 95) if direct else 60
                    row['selection_reason']='HEADING_ONLY' if heading_only else 'DIRECT_OPERATIVE_WITH_VALUE' if direct and numeric else 'DIRECT_SEMANTIC_SUPPORT' if direct else 'EXPLICIT_CONTEXT_SUPPORT'
                    evidence.append(row)
        preferred = [row for row in evidence if any(re.search(p, row['text']) for p in element.get('preferred_patterns', []))]
        # A fact may be split across parser clauses/sentences (e.g. a party
        # name on one line and the ID on the next, or non-compete scope and
        # territory in adjacent sentences).  Reuse the full contract corpus
        # as a retrieval fallback while binding the resulting quote back to
        # the real clause that contains its start offset.  This keeps SEARCH
        # _AUDIT and all downstream rules on the same source-bound fact.
        if not evidence:
            corpus = "\n".join(c.text for c in clauses
                               if c.section_type in {'正式合同条款', '附件'})
            for pattern in element.get('semantic_patterns', ()):
                match = re.search(pattern, corpus, re.S)
                if not match:
                    continue
                start, end = match.span()
                # Retain the enclosing statement, including qualifiers before
                # a lexical hit. Trimming to "wage ... amount", for example,
                # must not discard the probation scope and bypass exclusions.
                left = max(corpus.rfind(mark, 0, start) for mark in ('。', '；', ';', '\n'))
                right = [pos for mark in ('。', '；', ';', '\n')
                         if (pos := corpus.find(mark, end)) >= 0]
                start = left + 1
                end = min(right) if right else len(corpus)
                offset = 0
                owner = next((c for c in clauses
                              if c.section_type in {'正式合同条款', '附件'}
                              and (offset := offset + len(c.text) + 1) >= start), None)
                if owner is None:
                    owner = next((c for c in clauses if c.section_type in {'正式合同条款', '附件'}), None)
                quote = corpus[start:end].strip()
                candidate = dict(clause_id=owner.clause_id if owner else 'FULL_CORPUS',
                    location=owner.location if owner else '', title=owner.title if owner else '',
                    text=quote, quote=quote, original_excerpt=quote,
                    section_type=owner.section_type if owner else '正式合同条款',
                    heading_path=list(owner.heading_path or []) if owner else [],
                    source_start=start, source_end=end, supports_element_ids=[key],
                    source_type='CONTRACT_TEXT', entailment_score=95,
                    selection_reason='FULL_CORPUS_SEMANTIC_SUPPORT')
                # A retrieval hit cannot bypass the normal semantic predicate
                # or manufacture a source by spanning unrelated clauses.
                from review_v2.verified_source import bind_original
                candidate = bind_original(candidate, clauses)
                if not candidate['verified_original'] or not supports(element, candidate):
                    continue
                evidence.append(candidate)
                break
        facts[key] = sorted(preferred or evidence,key=lambda r:-r['entailment_score'])[:4]
        if audit is not None:
            audit[key] = {'candidates': candidates, 'accepted_evidence': deepcopy(facts[key])}
    return facts


def party_types(text):
    result = {}
    for role, label in [('landlord', r'(?:甲方[（(]出租人[）)]|出租人)'), ('tenant', r'(?:乙方[（(]承租人[）)]|承租人)')]:
        match = re.search(label + r'\s*[:：]\s*([^\n；;]+)', text)
        name = match.group(1).strip() if match else ''
        kind = ('LEGAL_PERSON' if re.search(r'公司|合作社|事业单位', name) else
                'UNINCORPORATED_ORGANIZATION' if re.search(r'合伙|事务所|个人独资', name) else
                'NATURAL_PERSON' if re.fullmatch(r'[\u4e00-\u9fff·]{2,12}', name) and not re.search(r'姓名|名称|填写', name) else 'UNKNOWN')
        result[role] = {'type': kind, 'evidence': match.group() if match else ''}
    return result


def applicability(condition, facts, parties):
    if condition.get('absent_fact') and facts.get(condition['absent_fact']):
        return False, '合同已有直接证据确认前置约定，无约定时的补位规则不适用。'
    if condition.get('party'):
        kind = parties[condition['party']]['type']
        if kind != 'UNKNOWN' and kind not in condition['types']:
            return False, '已识别相关主体为法人或非法人组织，仅适用于自然人的规则不适用。'
    return True, ''


def economic_exposure(clauses):
    """The exit event and monetary predicate must occur in the same clause."""
    rows, multiples = [], []
    for clause in clauses:
        if clause.section_type not in {'正式合同条款', '附件'} or not re.search(r'提前退租|提前收回', clause.text):
            continue
        match = re.search(r'(?:按照|支付|为).{0,15}?(?<!\d)([\d.]+|两|二|三|六|十二)个月.{0,8}租金.{0,65}违约金|违约金.{0,15}?(?<!\d)([\d.]+)倍.{0,8}(?:月租|租金)', clause.text)
        if not match:
            continue
        raw = match.group(1) or match.group(2)
        number = {'两': 2, '二': 2, '三': 3, '六': 6, '十二': 12}.get(raw)
        number = number if number is not None else float(raw)
        multiples.append(number)
        rows.append(dict(clause_id=clause.clause_id, location=clause.location, title=clause.title,
                         text=clause.text, original_excerpt=clause.text, section_type=clause.section_type,
                         source_type='CONTRACT_TEXT', supports_element_ids=['early_exit'], monthly_multiple=number))
    multiple = max(multiples, default=0)
    return {'evidence': rows, 'monthly_multiple': multiple or None,
            'ceiling': 'HIGH' if multiple >= 6 else 'MEDIUM' if multiple else 'LOW',
            'basis': '约定金额与月租比例，仅用于合同经济暴露筛查，不推定违约金违法或法院必然调减。'}


def apply(items, clauses, text, mark_na):
    facts = corpus_facts(clauses, [e for values in PROFILES.values() for e in values] + [EARLY_PRESENCE])
    parties = party_types(text)
    exposure = economic_exposure(clauses)
    # Economic quantification is not a substitute for the complete legal fact.
    # Coverage and SEARCH_AUDIT consume the same conjunctive corpus evaluator.
    for item in items:
        item.decision_trace['semantic_contract_domain'] = 'lease'
        if item.node_id == 'proper_party' and item.fallback_reason != '案件文书摘录来源豁免' and all(p['type'] == 'UNKNOWN' for p in parties.values()):
            # Bare role words do not identify either contracting person.
            if not re.search(r'(?:甲方|乙方|出租人|承租人)[^\n]{0,20}[:：]\s*[^\s_\n]{2,}', text):
                item.coverage_status = item.status = '缺失'
                item.issue_type = '完全缺失'
                item.evidence_clauses = []
                item.evidence_location = ''
                item.reasoning_summary = item.risk_point_description = '未找到双方可识别的姓名或名称，角色名称本身不能证明主体身份。'
        formula_sources = [c for c in clauses if re.search(r'(?:剩余租期|提前退租天数).{0,30}租金.{0,10}\d+(?:\.\d+)?倍.{0,20}违约金', c.text)]
        proven_scenario = bool(formula_sources and item.scenario_analysis)
        if item.node_id in {'early_surrender', 'excessive_deduction'} and not proven_scenario:
            item.decision_trace['economic_evidence_assessment'] = deepcopy(exposure)
            item.decision_trace['economic_evidence_ceiling'] = exposure['ceiling'] if item.node_id == 'early_surrender' else 'LOW'
            item.risk_level = {'HIGH': '高', 'MEDIUM': '中', 'LOW': '低'}[item.decision_trace['economic_evidence_ceiling']]
            item.economic_impact = exposure['ceiling'].lower() if exposure['evidence'] and item.node_id == 'early_surrender' else 'none'
            item.scenario_analysis = {}
            item.economic_impact_detail = {'level': item.economic_impact, 'monthly_payment_multiple': exposure['monthly_multiple'], 'source_evidence': exposure['evidence']}
            item.decision_trace['targeted_economic_recommendation'] = (
                f"已约定提前退出违约金为{exposure['monthly_multiple']:g}个月租金；结合解除原因及可证明的损失核验承担范围，避免重复扣款。"
                if exposure['evidence'] else "仅核对违约责任与可证明损失的关系；现有材料不足以认定高额违约金，不提出金额或倍数调整建议。")
        condition = CONDITIONS.get(item.node_id)
        if condition:
            allowed, reason = applicability(condition, facts, parties)
            item.decision_trace['semantic_applicability'] = {'condition': condition, 'parties': parties, 'applicable': allowed}
            if not allowed:
                mark_na(item, reason)
                item.applicable_if = ('相关主体为自然人' if condition.get('party') else '合同未约定前置事实：' + condition['absent_fact'])
                item.applicability['condition'] = item.applicable_if
                item.coverage_elements = []
                item.needs_manual_review = False
                item.suggested_clause_example = ''
                item.related_risks = []
                item.decision_trace.pop('element_evidence_truth', None)
                continue
        requirements = deepcopy(PROFILES.get(item.node_id))
        if proven_scenario and item.node_id == 'excessive_deduction':
            requirements.append(requirement('penalty_formula', '提前退出违约金的计费公式', r'(?:剩余租期|提前退租天数).{0,30}租金.{0,10}\d+(?:\.\d+)?倍.{0,20}违约金'))
            facts.update(corpus_facts(clauses, [requirements[-1]]))
        if item.node_id == 'early_surrender' and any(re.search(r'提前\s+日|按照\s+的标准|_{2,}', r['text']) for r in facts['early_exit']):
            requirements.append(requirement('early_detail', '填写提前通知期限及违约责任计算标准', r'提前\d+日.{0,50}(?:\d+元|\d+倍)'))
            facts.update(corpus_facts(clauses, [requirements[-1]]))
        if not requirements or item.coverage_status == '不适用':
            continue
        item.decision_trace['semantic_requirements'] = deepcopy(requirements)
        item.decision_trace['shared_semantic_facts'] = {e['element_id']: deepcopy(facts[e['element_id']]) for e in requirements}
        rows = [r for e in requirements for r in facts[e['element_id']]]
        item.evidence_clauses = deepcopy(rows)
        item.evidence_location = '；'.join(dict.fromkeys(r['location'] for r in rows))
        covered = [e['proposition'] for e in requirements if facts[e['element_id']]]
        missing = [e['proposition'] for e in requirements if not facts[e['element_id']]]
        item.coverage_status = '通过' if not missing else '部分覆盖' if covered else '缺失'
        item.status = '已覆盖' if item.coverage_status == '通过' else item.coverage_status
        item.issue_type = ('通过' if not missing else '模板空白' if covered and item.issue_type == '模板空白'
                           else '条款缺陷' if covered else '完全缺失')
        item.reasoning_summary = item.risk_point_description = ('已验证：' + '、'.join(covered) + '。' if covered else '') + ('未找到：' + '、'.join(missing) + '。' if missing else '')
        if item.issue_type == '模板空白':
            item.reasoning_summary += '相关字段存在空白，需填写后复核。'
        if item.node_id == 'indefinite_lease' and missing:
            item.reasoning_summary += '本项依据《民法典》第734条核对不定期租赁安排，属于建议性补充条款。'
        item.needs_manual_review = False
        item.decision_trace.pop('element_evidence_truth', None)
        item.decision_trace['negative_evidence'] = {'result': 'NOT_FOUND' if not covered else 'PARTIAL_FOUND' if missing else 'FOUND', 'missing_elements': missing}
    return items



