"""Conservative dangling predicate checks, independent of the contract domain."""
import re
from review_v2.priority_checklist_helpers import forbidden
PATTERN=r'[^。；\n]{0,80}(?:应当|必须|应)[^。；\n]{0,60}(?:导致|造成|承担如下责任|支付金额为)[。；\s]*$'
CHECKPOINT=forbidden('COMMON',22,'common_dangling_obligation','未完成的义务或责任条款',('必须','导致','造成'),
 '《民法典》第466条、第510条', (PATTERN,), '建议补全该条的行为、条件及责任后果，确认双方真实意思后再签署。')
def fragments(text):
    return [s for s in text.splitlines() if re.search(PATTERN,s)]
def augment(checklist,text):
    return tuple(checklist)+(CHECKPOINT,) if fragments(text) and not any(c.node_id==CHECKPOINT.node_id for c in checklist) else tuple(checklist)
