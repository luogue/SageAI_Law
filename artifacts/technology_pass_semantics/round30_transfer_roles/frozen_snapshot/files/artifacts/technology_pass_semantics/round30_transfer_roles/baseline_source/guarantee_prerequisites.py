"""Shared factual prerequisites for joint guarantors and prior-suit waiver."""
import re
from types import SimpleNamespace
from review_v2.guarantee_mode import extract_mode
from review_v2.guarantee_party_facts import extract_guarantee_parties

JOINT_NODES = {'multiple_guarantors_identification', 'guarantee_share_agreed',
               'joint_guarantor_internal_recourse', 'partial_action_against_guarantors'}
GENERAL_NODES = {'prior_lawsuit_defense_rule', 'prior_lawsuit_defense_exception',
                 'waiver_prior_lawsuit_written', 'oral_waiver_prior_lawsuit'}


def operative_parts(text):
    for part in re.split(r'[。；;\n]', text):
        part = re.sub(r'\s+', '', part)
        if '本合同' in part:
            part = part[part.rfind('本合同'):]
        if not re.search(r'法律规定|民法典|例如|历史|原合同|旧合同|假如|如果', part):
            yield part


def prerequisite(text, node, parties=None):
    from review_v2.guarantee_scenarios import CONDITIONS, extract, applicable
    if node in CONDITIONS:
        active=applicable(node,extract(text))
        return active, CONDITIONS[node]+'；'+('已触发。' if active else '本合同未触发。')
    if node in JOINT_NODES | {'company_guarantor_authority','company_guarantee_resolution'}:
        parties=parties if parties is not None else extract_guarantee_parties(text)
        if node in JOINT_NODES:
            return parties['joint_guarantee'], '多个保证人或共同保证时适用；'+('已触发。' if parties['joint_guarantee'] else '本合同未触发。')
        company=any(p['party_type']=='COMPANY' for p in parties['guarantors'])
        return company, '公司保证人时适用；'+('已触发。' if company else '本合同未触发。')
    if node not in GENERAL_NODES:
        return None
    parts = list(operative_parts(text))
    mode = extract_mode([SimpleNamespace(text=text, clause_id='body', location='全文')])['mode']
    if mode != 'GENERAL':
        return False, '未确认实际选择一般保证，不启动一般保证先诉抗辩专项分支。'
    if node in {'prior_lawsuit_defense_rule', 'prior_lawsuit_defense_exception'}:
        return True, '一般保证的法定权利及例外提示，不要求合同逐项复述。'
    waiver = any(re.search(r'放弃.{0,6}先诉抗辩权|先诉抗辩权.{0,8}放弃', p)
                 and not re.search(r'(?:不得|不予|未|不|没有|无需).{0,4}放弃|不视为放弃', p) for p in parts)
    if node == 'oral_waiver_prior_lawsuit':
        waiver = waiver and any(re.search(r'口头放弃|默认放弃|视为放弃|未反对即放弃', p)
                                and not re.search(r'不得|不视为|不构成', p) for p in parts)
    return waiver, '存在实际放弃安排，核验其形式。' if waiver else '未约定本项放弃安排，不要求保证人主动放弃先诉抗辩权。'


def enforce(items, text):
    from review_v2.engine import _set_item_not_applicable
    parties=extract_guarantee_parties(text)
    for item in items:
        result = prerequisite(text, item.node_id, parties)
        if result is None:
            continue
        item.decision_trace['guarantee_prerequisite'] = {'applicable': result[0], 'reason': result[1]}
        if not result[0]:
            _set_item_not_applicable(item, result[1])
            if result[1].find('时适用') >= 0:
                item.applicable_if=result[1].split('；')[0]
                item.applicability.update(condition=item.applicable_if,triggered=False)
            item.decision_trace['review_nature'] = 'CONTRACTUAL_REQUIREMENT'
            item.decision_trace.pop('non_contractual_review', None)
            item.related_risks = []
            item.suggested_clause_example = ''
            item.needs_manual_review = False
    return items
