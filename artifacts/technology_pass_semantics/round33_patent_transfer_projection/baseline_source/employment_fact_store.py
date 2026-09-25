"""Request-local, source-verified facts consumed by every EMP/NC rule stage."""
from contextvars import ContextVar
from copy import deepcopy
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
import re

from review_v2.deepseek_facts import FactExtractionError
from review_v2.employment_fact_schema import CONCEPTS, ELEMENTS, ENUMS, SCHEMA_VERSION

CURRENT = ContextVar('employment_fact_store', default=None)


def current():
    return CURRENT.get()


def number(value):
    from review_v2.fact_number_normalization import number as shared_number
    return shared_number(value)


def normalize(concept, value):
    if value is None or value == '' or value == []:
        raise FactExtractionError('EMPTY_EXTRACTED_VALUE:' + concept)
    from review_v2.employment_conditions import FIELDS, normalize as normalize_condition
    if concept in FIELDS:
        return normalize_condition(concept, value)
    from review_v2.fact_scalar_normalization import unwrap_scalar
    numeric = concept in {'working_hours.days_per_week','salary.cycle_days'} or concept.endswith((
        'compensation_after_handover_days','duration_months','hours_per_day','hours_per_week','notice_days',
        'rest_days_per_week','statutory_percentage','payment_delay_months'))
    if numeric:
        value = unwrap_scalar(concept, value, 'number')
        if type(value) not in (int, float, str, Decimal):
            raise FactExtractionError('INVALID_NUMERIC_TYPE:' + concept)
    elif concept.endswith('_date') and concept != 'salary.payment_date':
        value = unwrap_scalar(concept, value, 'date')
        if not isinstance(value, str):
            raise FactExtractionError('INVALID_DATE_TYPE:' + concept)
    elif '布尔值' in CONCEPTS[concept]:
        value = unwrap_scalar(concept, value, 'boolean')
    if concept in ENUMS:
        from review_v2.fact_enum_normalization import enum_value
        value = enum_value(concept,value,ENUMS[concept])
    if concept.endswith('_date') and concept != 'salary.payment_date':
        return date.fromisoformat(value).isoformat()
    if concept in {'working_hours.days_per_week','salary.cycle_days'}:
        n=number(value)
        if not n.is_finite() or n<0: raise FactExtractionError('INVALID_NONNEGATIVE_NUMBER')
        return float(n)
    if concept.endswith(('compensation_after_handover_days','duration_months','hours_per_day','hours_per_week','notice_days',
                          'rest_days_per_week','statutory_percentage','payment_delay_months')):
        n = number(value)
        if n < 0 or not n.is_finite():
            raise FactExtractionError('INVALID_DURATION:' + concept)
        return float(n)
    if concept in {'probation.salary','salary.regular','non_compete.compensation','non_compete.compensation_floor','non_compete.salary_base','dispatch.comparator_pay'}:
        if concept == 'non_compete.salary_base' and (not isinstance(value,dict) or value.get('base') not in {'REGULAR_SALARY','LOCAL_MINIMUM_WAGE','PREVIOUS_AVERAGE_SALARY'}):
            raise FactExtractionError('INVALID_COMPENSATION_BASE:' + concept)
        if not isinstance(value, dict):
            raise FactExtractionError('INVALID_MONEY:' + concept)
        if 'amount_text' in value:
            try:
                n = number(value['amount_text'])
            except FactExtractionError:
                # Preserve unquantified remuneration as context, not as a
                # calculable wage. A variable component cannot erase a valid
                # fixed amount extracted elsewhere.
                return {**value,'amount':None,'determinate':False}
            if n < 0 or not n.is_finite():
                raise FactExtractionError('INVALID_MONEY:' + concept)
            unit = {'元/月':'CNY/MONTH','MONTH':'CNY/MONTH','元/件':'CNY/PIECE'}.get(value.get('unit'),value.get('unit'))
            return {**value, 'amount': float(n), 'unit':unit,'determinate':bool(unit)}
        if not value.get('formula'):
            raise FactExtractionError('UNDEFINED_CALCULATION:' + concept)
        formula = value['formula']
        determinate = (isinstance(formula,dict) and formula.get('kind') == 'PERCENT_OF_BASE'
                       and formula.get('base') in {'REGULAR_SALARY','LOCAL_MINIMUM_WAGE','PREVIOUS_AVERAGE_SALARY'}
                       and 'percent' in formula and 0 < number(formula['percent']) <= 100)
        return {**value,'determinate':bool(determinate)}
    if '布尔值' in CONCEPTS[concept] and not isinstance(value, bool):
        raise FactExtractionError('INVALID_BOOLEAN:' + concept)
    if '字符串数组' in CONCEPTS[concept]:
        # A model may emit separate scalar records for an array-valued concept.
        # Wrapping a nonempty string changes representation, never its meaning.
        if isinstance(value,str) and value.strip():
            value = [value]
        if not isinstance(value,list) or not all(isinstance(v,str) and v.strip() for v in value):
            raise FactExtractionError('INVALID_LIST:' + concept)
    if concept == 'penalties.obligations' and (not isinstance(value,dict) or value.get('scope') not in
       {'ORDINARY_RESIGNATION','CONFIDENTIALITY','ORDINARY_DISCIPLINE','PROPERTY_DAMAGE','SPECIAL_TRAINING','NON_COMPETE','ACTUAL_DAMAGE','TRAINING_SERVICE_PERIOD','PROJECT_TASK_PERFORMANCE','WORK_TASK_COMPLETION','ATTENDANCE','RESIGNATION_NOTICE','OTHER'}):
        raise FactExtractionError('INVALID_PENALTY_SCOPE')
    if concept == 'penalties.obligations' and value.get('imposed') is not True:
        raise FactExtractionError('INVALID_OBLIGATION_POLARITY')
    if concept == 'penalties.obligations':
        from review_v2.penalty_liability_semantics import normalize as normalize_liability
        value = normalize_liability(value)
    if concept == 'ip.allocations' and (not isinstance(value,dict) or
        value.get('scope') not in {'DUTY_OR_RESOURCES','ALL_DURING_EMPLOYMENT','NON_DUTY','PRE_EXISTING','UNDIFFERENTIATED_RESULTS'} or
        value.get('beneficiary') not in {'EMPLOYER','EMPLOYEE','HOST','JOINT','UNSPECIFIED'} or
        value.get('mode') not in {'AUTOMATIC','SEPARATE_AGREEMENT','STATUTORY'}):
        raise FactExtractionError('INVALID_IP_ALLOCATION')
    return deepcopy(value)


class FactStore:
    def __init__(self, source, clauses, raw):
        self.source = source
        self.clauses = clauses
        self.raw = raw
        self.hash = hashlib.sha256(source.encode()).hexdigest()
        scopes=[set(p['active_concepts']) for p in raw if 'active_concepts' in p]
        self.active_concepts=set.union(*scopes) if scopes else set(CONCEPTS)
        if not self.active_concepts <= set(CONCEPTS):raise FactExtractionError('UNKNOWN_ACTIVE_CONCEPT')
        self.facts = []
        self.coverage = {}
        self.decisions = {}
        self.by_id = {}
        self.adverse_cache = {}
        self.element_specs = deepcopy(ELEMENTS)
        self.normalization_events = []
        from review_v2.employment_fact_schema import NONCRITICAL_FACTS
        self.validation_diagnostics = []
        self.quarantined_concepts = set()
        searched_concepts = set()
        unresolved_concepts = set()
        by_clause = {c.clause_id: c for c in clauses}
        for packet_index, packet in enumerate(raw):
            data = packet.get('response') if isinstance(packet, dict) else None
            if not isinstance(data, dict):
                self._schema_error('INVALID_FACT_ENVELOPE', 'response', data, 'object')
            if data.get('schema_version') != SCHEMA_VERSION:
                self._schema_error('SCHEMA_VERSION_MISMATCH', 'schema_version', data.get('schema_version'), SCHEMA_VERSION)
            reviewed = data.get('reviewed_clause_ids')
            if not isinstance(reviewed, list) or not all(isinstance(c,str) for c in reviewed) or set(reviewed) != set(by_clause):
                self._schema_error('INCOMPLETE_FULL_TEXT_COVERAGE', 'reviewed_clause_ids', reviewed, sorted(by_clause))
            coverage = data.get('coverage')
            if 'searched_concepts' in data:
                searched = data['searched_concepts']
                uncertain = data.get('unresolved_concepts',[])
                if not isinstance(searched,list) or not all(isinstance(c,str) and c in CONCEPTS for c in searched):
                    self._schema_error('INVALID_SEARCH_SCOPE','searched_concepts',searched,sorted(CONCEPTS))
                # Every topic batch reads the same full document. Cross-batch
                # uncertainty is retained globally; unknown concepts still fail.
                if not isinstance(uncertain,list) or not all(isinstance(c,str) and c in CONCEPTS for c in uncertain):
                    self._schema_error('INVALID_UNRESOLVED_SCOPE','unresolved_concepts',uncertain,sorted(CONCEPTS))
                searched_concepts.update(searched)
                unresolved_concepts.update(uncertain)
                coverage = {c:'UNCERTAIN' for c in searched}
            if not isinstance(coverage, dict):
                self._schema_error('INVALID_COVERAGE_TYPE', 'coverage', coverage, 'concept -> extraction status mapping')
            self.coverage.update(coverage)
            if not isinstance(data.get('facts'), list):
                self._schema_error('INVALID_FACTS_TYPE', 'facts', data.get('facts'), 'array')
            for index, fact in enumerate(data['facts']):
                concept = fact.get('concept') if isinstance(fact, dict) else None
                try:
                    row = self._validate_fact(fact, by_clause, coverage)
                except FactExtractionError as exc:
                    for diagnostic in exc.diagnostics:
                        diagnostic.update(fact_id=(fact.get('fact_id') if isinstance(fact,dict) else None) or f'candidate-{packet_index}-{index}',
                                          concept=concept, model_raw_value=fact,
                                          evidence=fact.get('evidence') if isinstance(fact,dict) else None)
                        diagnostic.update(fact_key=concept,raw_value=fact.get('value') if isinstance(fact,dict) else fact,normalized_value=None,
                            allowed_values=sorted(ENUMS[concept]) if concept in ENUMS else None,
                            source_clause=[{'clause_id':e.get('clause_id'),'section':by_clause[e['clause_id']].location,'text':by_clause[e['clause_id']].text} for e in (fact.get('evidence',[]) if isinstance(fact,dict) else []) if isinstance(e,dict) and e.get('clause_id') in by_clause])
                        if concept in NONCRITICAL_FACTS and diagnostic['failed_stage'] in {'NORMALIZATION','FACT_SCHEMA'}:
                            diagnostic['disposition'] = 'QUARANTINE_AND_MANUAL_REVIEW'
                            self.quarantined_concepts.add(concept)
                        self.validation_diagnostics.append(diagnostic)
                    continue
                if row['fact_id'] not in self.by_id:
                    self.facts.append(row)
                    self.by_id[row['fact_id']] = row
                else:
                    previous = self.by_id[row['fact_id']]
                    rank = lambda f: (f['assertion']=='EXPLICIT', f['confidence'])
                    if rank(row) > rank(previous):
                        # Identical value/source duplicates must not let an
                        # earlier inferred or low-confidence record win by order.
                        previous.update(row)
        if set(self.coverage) != self.active_concepts:
            self._schema_error('INCOMPLETE_CONCEPT_COVERAGE', 'coverage.keys', sorted(self.coverage), sorted(CONCEPTS))
        for key, status in self.coverage.items():
            if key in self.quarantined_concepts:
                self.coverage[key] = 'UNCERTAIN'
                continue
            if key in searched_concepts:
                rows = [f for f in self.facts if f['concept']==key]
                self.coverage[key] = ('EXTRACTED' if any(f['assertion']=='EXPLICIT' and f['confidence']>=.75 for f in rows)
                    else 'UNCERTAIN' if rows or key in unresolved_concepts else 'ABSENT')
                continue
            if isinstance(status,str) and status in ENUMS.get(key, set()) and any(f['concept']==key and f['normalized_value']==status for f in self.facts):
                self.normalization_events.append({'concept':key,'field':'coverage','from':status,'to':'EXTRACTED'})
                self.coverage[key] = status = 'EXTRACTED'
            if status not in ('EXTRACTED','ABSENT','UNCERTAIN'):
                self.validation_diagnostics.append(self._diagnostic('INVALID_EXTRACTION_COVERAGE', 'coverage.'+key, status, ['EXTRACTED','ABSENT','UNCERTAIN']))
            elif status != 'UNCERTAIN' and (status == 'EXTRACTED') != any(f['concept'] == key for f in self.facts):
                self.validation_diagnostics.append(self._diagnostic('CONTRADICTORY_EXTRACTION', 'coverage.'+key, status, 'EXTRACTED iff validated fact exists; otherwise ABSENT or UNCERTAIN'))
        self.coverage.update({c:'NOT_APPLICABLE' for c in CONCEPTS if c not in self.active_concepts})
        if any(d['disposition'] == 'BLOCK' for d in self.validation_diagnostics):
            exc = FactExtractionError('FACT_STORE_VALIDATION_FAILED', diagnostics=self.validation_diagnostics)
            exc.raw_output = raw
            raise exc

    @staticmethod
    def _diagnostic(rule, field, actual, expected, stage='FACT_SCHEMA'):
        return FactExtractionError(rule, failed_stage=stage, field=field,
                                   model_raw_value=actual, actual=actual, expected=expected).diagnostics[0]

    def _schema_error(self, rule, field, actual, expected):
        raise FactExtractionError(rule, diagnostics=[self._diagnostic(rule,field,actual,expected)])

    def _validate_fact(self, fact, by_clause, coverage):
        from review_v2.fact_validation import bind_quote
        if not isinstance(fact,dict):
            self._schema_error('INVALID_FACT_TYPE', 'fact', fact, 'object')
        fact = deepcopy(fact)
        if 'normalized_value' in fact:
            if 'value' in fact and json.dumps(fact['value'],sort_keys=True) != json.dumps(fact['normalized_value'],sort_keys=True):
                self._schema_error('CONFLICTING_VALUE_FIELDS','normalized_value',fact,'one unambiguous value')
            fact['value'] = fact['normalized_value']
        for field in ('concept','evidence'):
            if field not in fact:
                if field == 'evidence':
                    raise FactExtractionError('MISSING_REQUIRED_FIELD', failed_stage='EVIDENCE_BINDING',
                                              field=field, actual='MISSING',expected='source excerpts')
                self._schema_error('MISSING_REQUIRED_FIELD', field, 'MISSING', 'present field')
        concept = fact.get('concept')
        if not isinstance(concept,str) or concept not in self.active_concepts or concept not in coverage:
            self._schema_error('UNKNOWN_FACT_CONCEPT', 'concept', concept, sorted(CONCEPTS))
        # Bind before normalizing: noncritical value quarantine must never hide
        # a fabricated source quote or an unrelated/missing clause identifier.
        evidence = fact.get('evidence')
        if not isinstance(evidence,list) or not evidence:
            raise FactExtractionError('FACT_WITHOUT_EVIDENCE', failed_stage='EVIDENCE_BINDING', field='evidence',
                                      actual=evidence, expected='one or more source-bound excerpts')
        bound = []
        for ev in evidence:
            clause = by_clause.get(ev.get('clause_id')) if isinstance(ev,dict) and isinstance(ev.get('clause_id'),str) else None
            if clause is None:
                raise FactExtractionError('UNKNOWN_EVIDENCE_CLAUSE', failed_stage='EVIDENCE_BINDING', field='evidence.clause_id',
                                          actual=ev, expected=sorted(by_clause))
            if not clause.location or clause.section_type not in {'正式合同条款','附件'}:
                raise FactExtractionError('NON_OPERATIVE_EVIDENCE', failed_stage='EVIDENCE_BINDING', field='evidence.section',
                                          actual={'section':clause.location,'type':clause.section_type}, expected='operative clause or annex with section')
            start, end, mode = bind_quote(clause.text,ev.get('quote'))
            quote = clause.text[start:end]
            if mode != 'EXACT':
                self.normalization_events.append({'concept':concept,'field':'evidence.quote',
                    'clause_id':clause.clause_id,'from':ev.get('quote'),'to':quote,'alignment_mode':mode})
            clause_start = self.source.find(clause.text) if self.source.count(clause.text) == 1 else -1
            doc_start = (clause_start + start if clause_start >= 0 else
                         self.source.find(quote) if self.source.count(quote) == 1 else -1)
            bound.append({**clause.to_public_dict(), 'text':quote,'quote':quote,'original_excerpt':quote,
                'model_quote':ev.get('quote'), 'alignment_mode':mode,'source_type':'CONTRACT_TEXT',
                'source_start':start,'source_end':end,'evidence_span':{'basis':'clause.text','start':start,'end':end},
                'document_span':{'start':doc_start,'end':doc_start+len(quote)} if doc_start>=0 else None,
                'verified_original':True,'fact_concept':concept})
        for field in ('value','confidence','assertion'):
            if field not in fact:
                self._schema_error('MISSING_REQUIRED_FIELD', field, 'MISSING', 'present field')
        if fact.get('assertion') not in ('EXPLICIT','INFERRED'):
            self._schema_error('INVALID_FACT_ASSERTION', 'assertion', fact.get('assertion'), ['EXPLICIT','INFERRED'])
        confidence = fact.get('confidence')
        if type(confidence) not in (int,float) or not 0 <= confidence <= 1:
            self._schema_error('INVALID_CONFIDENCE', 'confidence', confidence, 'finite number in [0,1]')
        try:
            value = normalize(concept, fact.get('value'))
        except (FactExtractionError,ValueError,TypeError,OverflowError,InvalidOperation) as exc:
            raise FactExtractionError(str(exc) if isinstance(exc,FactExtractionError) else 'INVALID_FACT_VALUE',
                failed_stage='NORMALIZATION',field='value',model_raw_value=fact.get('value'),
                expected=sorted(ENUMS[concept]) if concept in ENUMS else CONCEPTS[concept],
                actual=exc.diagnostics[0].get('actual') if isinstance(exc,FactExtractionError) else None) from exc
        if isinstance(fact['value'], dict) and not isinstance(value, (dict, list)):
            self.normalization_events.append({'concept':concept,'field':'value','from':fact['value'],
                'to':value,'transformation':'SINGLE_FIELD_SCALAR_UNWRAP'})
        if concept in ENUMS and fact['value'] != value:
            self.normalization_events.append({'concept':concept,'field':'value','from':fact['value'],'to':value,'transformation':'ENUM_CANONICALIZATION'})
        if isinstance(fact['value'],str) and isinstance(value,list):
            self.normalization_events.append({'concept':concept,'field':'value','from':fact['value'],
                                             'to':value,'transformation':'SINGLETON_ARRAY'})
        fact_id = 'EF-' + hashlib.sha256((concept+repr(value)+repr([(e['clause_id'],e['quote']) for e in bound])).encode()).hexdigest()[:16]
        for ev in bound:
            ev['structured_fact_id'] = fact_id
        return {'fact_id':fact_id,'origin_fact_id':fact.get('origin_fact_id'),'concept':concept,'normalized_value':value,
                'confidence':confidence,'assertion':fact['assertion'],'evidence':bound}

    def get(self, concept, positive=True):
        rows = [f for f in self.facts if f['concept'] == concept and self.coverage[concept] != 'UNCERTAIN'
                and f['assertion'] == 'EXPLICIT' and f['confidence'] >= 0.75]
        if positive:
            rows = [f for f in rows if f['normalized_value'] is not False]
            rows = [f for f in rows if not isinstance(f['normalized_value'],dict) or f['normalized_value'].get('determinate') is not False]
            if concept == 'economic_compensation.statutory':
                rows = [f for f in rows if f['normalized_value']['kind'] in {'STATUTORY_PAY','CALCULATION_RULE'}]
            if concept == 'working_hours.overtime':
                rows = [f for f in rows if f['normalized_value'] in {'STATUTORY','REST_DAY_TIME_OFF','ALLOWANCE_WITH_STATUTORY_SHORTFALL'}]
            if concept == 'non_compete.compensation':
                rows = [f for f in rows if f['normalized_value'].get('unit')=='CNY/MONTH']
        return rows

    def values(self, key):
        state = getattr(self, 'verification_states', {}).get(key, {})
        if state.get('absence_audit') and state.get('verification_state') == 'VERIFIED_ABSENT':
            return [state['verified_absence_value']]
        return [f['normalized_value'] for f in self.get(key, positive=False)]

    def evidence(self, rows, key):
        result = []
        for fact in rows:
            for original in fact['evidence']:
                row = deepcopy(original)
                row.update(supports_element_ids=[key], supporting_element_ids=[key],
                           selection_reason='STRUCTURED_FACT_BINDING', entailment_score=100)
                result.append(row)
        return result

    def element(self, key):
        if key.endswith('_adverse'):
            node = key.removesuffix('_adverse')
            return self.adverse(node)
        options = self.element_specs.get(key)
        if options is None:
            raise FactExtractionError('UNMAPPED_EMPLOYMENT_ELEMENT:' + key)
        for option in options:
            groups = [self.get(k) for k in option]
            if all(groups):
                return self.evidence([f for group in groups for f in group], key)
        return []

    def unresolved(self, key):
        if self.element(key):
            return False
        return any(self.coverage[c] == 'UNCERTAIN' or any(f['concept'] == c and
                   (f['assertion'] != 'EXPLICIT' or f['confidence'] < 0.75) for f in self.facts)
                   for option in self.element_specs.get(key,[]) for c in option)

    def supports(self, element, row):
        key = element['element_id']
        matches = self.element(key)
        return any(e['clause_id'] == row.get('clause_id')
                   and e['text'] == (row.get('text') or row.get('quote')) for e in matches)

    def corpus_facts(self, requirements, audit=None):
        result = {}
        for req in requirements:
            key = req['element_id']
            hits = self.element(key)
            result[key] = hits
            if audit is not None:
                audit[key] = {'candidates': [{**e,'score':1,'accepted':True} for e in hits],
                              'extraction_coverage':self.coverage, 'source_hash': self.hash}
        return result

    def applicability(self, node):
        if node == 'employment_general_penalty' and getattr(self,'agreement_type','labor') == 'confidentiality':
            if self.coverage['nda.employment_relationship']=='UNCERTAIN':
                raise FactExtractionError('UNRESOLVED_EMPLOYMENT_RELATIONSHIP', failed_stage='VERIFIED_APPLICABILITY', field='nda.employment_relationship')
            return True in self.values('nda.employment_relationship'), '劳动者违约金规则以全文已验证劳动关系为适用前提。'
        if node.startswith('employment_part_time_'):
            from review_v2.employment_dispatch import classify
            return classify(self)['employment_form']=='PART_TIME', '仅在已验证非全日制关系下使用本专项规则。'
        if node == "employment_open_ended_limit":
            yes = "INDEFINITE" in self.values("contract.type")
            return yes, "仅适用于已验证声明无固定期限的劳动合同。"
        if node.startswith('employment_dispatch_'):
            from review_v2.employment_dispatch import classify
            yes = classify(self)['employment_form'] == 'DISPATCH'
            return yes, '已验证当前劳动关系属于劳务派遣。' if yes else '未证明存在当前劳务派遣关系，不执行派遣专项规则。'
        if node == 'employment_probation_limit' and 'TASK' in self.values('contract.type') and self.coverage['probation.arrangement'] != 'UNCERTAIN':
            return True, '任务期限合同执行不得约定试用期的禁止性检查，不适用普通期限上限。'
        concept = {'employment_probation':'probation.arrangement',
                   'employment_probation_limit':'probation.arrangement',
                   'employment_training_service':'training.arrangement'}.get(node)
        if node.startswith('employment_noncompete'):
            concept = 'non_compete.arrangement'
        if concept:
            if self.coverage[concept] == 'UNCERTAIN':
                raise FactExtractionError('UNRESOLVED_APPLICABILITY',failed_stage='VERIFIED_APPLICABILITY',
                    field=concept,actual=getattr(self,'verification_states',{}).get(concept),
                    expected='verified current, deferred, none, or verified absence')
            yes = ('EXISTS' if concept == 'non_compete.arrangement' else 'CURRENT') in self.values(concept)
            return yes, '统一事实库确认当前已约定该安排。' if yes else '全文抽取未发现当前生效安排；不以未来另签或明确不设触发。'
        return True, '劳动合同通用适用事项；事实来自已完成的全文抽取。'

    def negative_support(self, node):
        """Optional protective quotes; absence proof remains a separate audit."""
        concepts = {'employment_part_time_exit': ('part_time.exit_permission',)}.get(node, ())
        return self.evidence([f for c in concepts for f in self.get(c)], node + '_protection')

    def negative_search_audit(self, node):
        if node != 'employment_part_time_exit':
            return None
        from review_v2.employment_rule_adapter import EXIT_SEARCH_CONCEPTS, adverse
        return {
            'source_sha256': self.hash,
            'searched_concepts': list(EXIT_SEARCH_CONCEPTS),
            'verification_states': {c: getattr(self, 'verification_states', {}).get(c) for c in EXIT_SEARCH_CONCEPTS},
            'coverage': {c: self.coverage[c] for c in EXIT_SEARCH_CONCEPTS},
            'result': 'PENDING' if self.pending_reason(node) else ('ADVERSE_FOUND' if adverse(self,node) else 'NO_ADVERSE_FOUND'),
        }

    def pending_reason(self, node):
        fields = {
            'employment_worker_charge':['worker.security_payment'],
            'employment_illegal_waiver':[k for k in CONCEPTS if k.startswith('social_insurance.')],
            'employment_general_penalty':['penalties.obligations'],
            'employment_arbitrary_exit':['termination.employer_unrestricted','economic_compensation.waived'],
            'employment_ip_ownership':['ip.allocations','ip.personal_rights_waived'],
            'employment_probation_limit':['probation.repeated'],
        }.get(node,[])
        if node == 'employment_part_time_probation': fields=['probation.arrangement']
        if node == 'employment_part_time_exit':
            from review_v2.employment_rule_adapter import EXIT_SEARCH_CONCEPTS
            # The legal predicate is a restriction, not a numerical zero.
            # Its independent full-document search must be conclusive; an
            # unresolved restriction still goes to verification. No numeric
            # value or coverage state is synthesized here.
            fields = list(EXIT_SEARCH_CONCEPTS)
        if node == 'employment_open_ended_limit':
            fields = ['contract.term_limit_mode','contract.term_limit_date','contract.term_limit_months']
        if node == 'employment_arbitrary_exit':
            fields += [k for k in CONCEPTS if k.startswith('capability.')]
        from review_v2.termination_facts import ADVERSE_INPUTS
        fields += list(ADVERSE_INPUTS.get(node, ()))
        uncertain = [k for k in fields if self.coverage[k]=='UNCERTAIN']
        if uncertain:
            if node == 'employment_open_ended_limit':
                return '合同声明的期限性质与到期安排尚无法确认，请核对具体终止条件及其是否仅指其他安排的期限。'
            if node == 'employment_arbitrary_exit' and any(k.startswith('capability.') for k in uncertain):
                return '不能胜任解除的考核依据、培训或调岗、再次考核及通知补偿安排存在语义不确定，请核对相应解除条款。'
            if node == 'employment_ip_ownership':
                return '劳动成果的归属范围、权利人或处分方式尚无法确认，请结合相关条款及引用文件核验；未约定归属本身不构成人工复核理由。'
            return '全文抽取仍有不确定事实，需核验：' + '；'.join(CONCEPTS[k].split('；')[0] for k in uncertain)
        if node == 'employment_probation_limit' and 'CURRENT' in self.values('probation.arrangement'):
            duration = bool(self.get('probation.duration_months') or
                            (self.get('probation.start_date') and self.get('probation.end_date')))
            basis = bool(self.get('contract.duration_months') or
                         (self.get('contract.start_date') and self.get('contract.end_date')) or
                         any(k in {'INDEFINITE','TASK'} for k in self.values('contract.type')))
            if not duration or not basis:
                return '试用期上限计算缺少可确认的合同期限或试用期限，需要核验具体日期/长度。'
        return ''

    def public(self):
        from review_v2.noncompete_financial import assess
        from review_v2.noncompete_semantics import person_assessment
        nested = {}
        for key in CONCEPTS:
            target = nested
            parts = key.split('.')
            for part in parts[:-1]:
                target = target.setdefault(part, {})
            target[parts[-1]] = [f for f in self.facts if f['concept'] == key]
        return {'schema_version':SCHEMA_VERSION,'provider':'deepseek','source_sha256':self.hash,
                'input':{'text':self.source,'clauses':[{'clause_id':c.clause_id,'section':c.location,'text':c.text} for c in self.clauses]},
                'active_concepts':sorted(self.active_concepts),'inactive_concepts':sorted(set(CONCEPTS)-self.active_concepts),
                'extraction_coverage':self.coverage,'employment':nested,
                'noncompete_financial':assess(self)[0],
                'noncompete_person':person_assessment(self),
                'verified_coverage':self.coverage,
                'verification_states':getattr(self,'verification_states',{}),
                'coverage_reconciliation':getattr(self,'coverage_reconciliation',[]),
                'deepseek_raw_results':self.raw,'semantic_verification':getattr(self,'verification',None),
                'normalization_events':self.normalization_events,'rule_decisions':self.decisions,
                'validation_diagnostics':self.validation_diagnostics,
                'validation_attempts':getattr(self,'validation_attempts',[])}

    def absence_proof(self, key):
        if self.unresolved(key):
            raise FactExtractionError('UNRESOLVED_FACT_CANNOT_PROVE_ABSENCE:' + key)
        concepts = sorted({c for option in self.element_specs.get(key,[]) for c in option})
        return {'source_sha256':self.hash, 'concepts':concepts,
                'coverage':{c:self.coverage[c] for c in concepts},
                'reviewed_clause_ids':[c.clause_id for c in self.clauses],
                'matching_fact_count':len(self.element(key))}

    def adverse(self, node):
        from review_v2.employment_fact_rules import adverse
        if node not in self.adverse_cache:
            self.adverse_cache[node] = adverse(self, node)
        return deepcopy(self.adverse_cache[node])


def completed_absence_audit(audit):
    store = current()
    if store is None or audit.get('result') != 'NOT_FOUND':
        return False
    key = audit.get('element_id')
    if key not in store.element_specs:
        return False
    expected = store.absence_proof(key)
    return expected['matching_fact_count'] == 0 and bool(expected['concepts']) and audit.get('structured_fact_query') == expected
