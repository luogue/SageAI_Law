"""Shared factual prerequisites for joint guarantors and prior-suit waiver."""
import re
from types import SimpleNamespace
from review_v2.guarantee_mode import extract_mode

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


def prerequisite(text, node):
    if node not in JOINT_NODES | GENERAL_NODES:
        return None
    parts = list(operative_parts(text))
    if node in JOINT_NODES:
        joint = any(re.search(r'共同保证|共同担保|(?:多个|两个以上|两名|两位)保证人', p)
                    and not re.search(r'(?:无|不存在|不构成|不涉及|并非).{0,5}(?:共同保证|共同担保|多个保证人)', p)
                    for p in parts)
        labels = set(re.findall(r'保证人[（(]?([一二三四五六七八九十ABＣC123456789])[）)]?\s*[:：]', text))
        joint = joint or len(labels) >= 2 or any(re.search(r'保证人[:：][^。；]+[、及与][^。；]+', p) for p in parts)
        return bool(joint), '已识别共同保证或多个保证人。' if joint else '未识别共同保证或两个以上保证人，共同保证专项分支不适用。'
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
    for item in items:
        result = prerequisite(text, item.node_id)
        if result is None:
            continue
        item.decision_trace['guarantee_prerequisite'] = {'applicable': result[0], 'reason': result[1]}
        if not result[0]:
            _set_item_not_applicable(item, result[1])
            item.decision_trace['review_nature'] = 'CONTRACTUAL_REQUIREMENT'
            item.decision_trace.pop('non_contractual_review', None)
            item.related_risks = []
            item.suggested_clause_example = ''
            item.needs_manual_review = False
    return items
