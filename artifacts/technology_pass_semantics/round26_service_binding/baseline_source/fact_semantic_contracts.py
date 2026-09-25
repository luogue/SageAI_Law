"""Shared proposition boundaries, not lexical matching of contract text.

Extraction and independent verification see the same predicates. Each positive
verification must attest every predicate against that fact's own quoted spans.
Overlap is allowed only when the source actually entails both propositions.
"""
from review_v2.fact_validation import FactExtractionError

BOUNDARIES = {
    'exit_settlement.secret_duration': {
        'actual_duration_source': '所绑定原文必须明确保密时长、终止日、终止事件或明示永久/无期限；仅离职后继续有效不能支持。引用未提供的其他协议不能推断其期限；已提供附件须引用实际期限条款。',
    },
    'exit_settlement.certificate_requires_handover': {
        'conditional_relationship_and_polarity': 'true须由原文明示交接等完成是出具证明前提；仅并列义务不成立。明确禁止因交接延期出具应为false。保留原文条件方向与肯否极性。',
    },
    'identity.worker_address': {
        'worker_residence': '证据明确载明劳动者本人居住地址，不能用单位住所、岗位、电话、身份证号码或其编码推断劳动者住址。',
    },
    'non_compete.person_scope': {
        'identified_obligor': '竞业条款明确约束具体当事人或可识别的人员类别；协议乙方可通过全文主体指代识别。无需证明该人已接触秘密。未定义的相关人员不是可识别的范围。',
    },
    'non_compete.person_eligibility': {
        'express_qualification_basis': '原文明确提供受限人员的资格类别或保密义务身份依据；仅写乙方承担竞业义务本身不能证明其适格性。不得推定实际接触已经发生。',
    },
    'penalties.obligations': {
        'preset_liability': '该具体义务设有固定金额、最低金额或比例/公式责任，而不只是赔偿实际损失或最高责任额。最低赔偿无需冠以违约金名称；实际损失超过最低额再补足不消除最低责任。',
        'obligation_amount_binding': '金额或公式由该责任条款及明确关联语句支持；不得借用保证金等其他义务金额。',
    },
    'non_compete.businesses': {
        'specified_competitive_activities': '原文已约定可识别的竞争业务活动或行业范围；仅概括不得到竞争企业工作且具体范围待定，只证明父义务存在，不能证明业务范围参数已确定。',
    },
    'nda.exception_public': {
        'public_status': '信息已合法公开或进入公共领域；这是信息的公开状态，不是接受方已知悉。',
        'excluded': '该类信息被排除在保密义务之外。',
    },
    'nda.exception_prior': {
        'recipient_prior_knowledge': '接受方在此次取得前已经合法知悉、拥有或持有该信息；时间在先的公开状态本身不证明接受方知悉。',
        'excluded': '该接受方原已知悉或持有的信息被排除在保密义务之外。',
    },
    'nda.remedies': {
        'breach_legal_relief': '违反保密义务后的损害赔偿责任、违约责任或可请求的停止侵害等法律救济；仅报告安全事件、协助补救或减少损失不蕴含赔偿责任或请求权。',
    },
    'nda.incident_response': {
        'incident_handling': '发现信息安全事件时的报告、处置、协助或减损义务；不推定损害赔偿责任。',
    },
}
ARRANGEMENT = {
    'EXISTS': {'current_restriction': '合同已经对竞争从业施加约束（包括原则性约束）；范围、期限、补偿以后确定只影响子参数，不消除该约束。'},
    'DEFERRED': {'future_obligation_decision': '是否设定竞业义务本身留待以后协商或另签，当前未施加竞争从业约束；仅参数延期不满足。'},
    'EXPLICIT_NONE': {'explicit_no_obligation': '原文明示不设竞业义务；保密不妨碍就业或未发现竞业参数不能替代。'},
}


def criteria(concept, value):
    if concept == 'non_compete.arrangement':
        return ARRANGEMENT.get(value, {}) if isinstance(value, str) else {}
    return BOUNDARIES.get(concept, {})


def definitions(keys):
    return {k: (ARRANGEMENT if k == 'non_compete.arrangement' else BOUNDARIES[k])
            for k in keys if k in BOUNDARIES or k == 'non_compete.arrangement'}


INSTRUCTIONS = '''semantic_contracts是逐事实语义边界，不是关键词。父义务存在与子参数完整性分别判断，不能反向推导。
同一引文可支持多个事实仅当它独立蕴含每个事实所需的命题。公开不蕴含接受方已知；减损不蕴含损害赔偿。相近词、同章节、同时间前缀均不足。
对semantic_contracts涵盖的候选，checks若supported=true，必须同时返回semantic_checks对象：以对应value的每个判据键为key，值为{"supported":true,"reason":"说明谁承担什么义务/哪个事实状态，不能只说有关键词","evidence_indices":[0]}。索引从0开始，仅指该候选的evidence，不得借其他事实证据。
任何判据不成立时必须supported=false并具体解释，进入现有受控纠正，不可无依据认可。additional_facts中相同概念也须携带同样semantic_checks，绑定该新增事实自己的evidence。
未找到事实不生成候选；不得为满足判据虚构事实。一个引文只支持部分命题时只保留有依据的事实，其余做全文检索。'''


def validate_checks(candidates, data):
    checks = {c['fact_id']: c for c in data['checks']}
    pairs = [(f, checks[f['fact_id']]) for f in candidates]
    pairs += [(f, dict(f, supported=True)) for f in data.get('additional_facts', [])]
    for fact, check in pairs:
        required = criteria(fact['concept'], fact.get('value', fact.get('normalized_value')))
        if not required or check.get('supported') is not True:
            continue
        claims = check.get('semantic_checks', {})
        invalid = []
        for key in required:
            row = claims.get(key, {}) if isinstance(claims, dict) else {}
            indices = row.get('evidence_indices') if isinstance(row, dict) else None
            if (not isinstance(row, dict) or row.get('supported') is not True
                or not isinstance(row.get('reason'), str) or not row['reason'].strip()
                or not isinstance(indices, list) or not indices
                or any(type(i) is not int or i < 0 or i >= len(fact['evidence']) for i in indices)):
                invalid.append(key)
        if invalid:
            raise FactExtractionError('SEMANTIC_ENTAILMENT_INCOMPLETE', failed_stage='FACT_VERIFICATION',
                fact_id=fact.get('fact_id'), field=fact['concept'], model_raw_value=check,
                evidence=fact['evidence'], expected=required, actual={'invalid_predicates': invalid})
