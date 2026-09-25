"""General drafting rules shared by equity transactions, without goods rules."""
from review_v2.priority_checklist_helpers import required as R
from review_v2.sale_contract_checklist import SALE_REVIEW_CHECKLIST

ROWS = tuple(c for c in SALE_REVIEW_CHECKLIST if c.node_id in {
    'common_effective_clause', 'common_notice_delivery', 'common_jurisdiction',
}) + (
    R('COMMON', 26, 'common_contract_termination', '合同解除与终止机制', ('解除', '终止', '通知'), '《民法典》第563条、第565条、第566条', [
        ('解除终止事由及通知程序', (r'(?:解除|终止)[^。\n]{0,70}(?:通知|协商一致)|通知[^。\n]{0,40}(?:解除|终止)',)),
        ('解除终止后的结算及存续义务', (r'(?:解除|终止)[^。\n]{0,70}(?:结算|清算|存续|继续有效)',)),
    ]),
    R('COMMON', 27, 'common_enforcement_costs', '实现权利费用承担', ('律师费', '保全费', '诉讼费'), '《民法典》第584条', [
        ('合理实现权利费用承担', (r'(?:承担|支付|赔偿)[^。\n]{0,70}(?:律师费|保全费|诉讼费)|律师费[^。\n]{0,70}承担',)),
    ], risk='低'),
    R('COMMON', 28, 'common_uncontrollable_events', '不可抗力通知、证明及履行后果', ('不可抗力',), '《民法典》第590条', [
        ('不可抗力通知与合理期限证明', (r'不可抗力[^。\n]{0,100}(?:通知|证明)',)),
        ('影响范围内的履行后果', (r'不可抗力[^。\n]{0,100}(?:延期|免责|解除|免除)',)),
    ], trigger=('不可抗力',), risk='低'),
    R('COMMON', 23, 'common_general_breach', '一般违约责任及损失赔偿', ('违约', '赔偿', '损失'), '《民法典》第577条、第584条', [
        ('违反合同义务的救济与损失赔偿', (r'违约[^。\n]{0,100}(?:赔偿|损失|违约金)|违反[^。\n]{0,100}赔偿',)),
    ]),
    R('COMMON', 24, 'common_penalty_loss', '违约金与损失赔偿衔接', ('违约金', '损失'), '《民法典》第585条', [
        ('约定违约金的口径及与损失赔偿衔接', (r'违约金[^。\n]{0,100}(?:损失|调整|不足|补足)|损失[^。\n]{0,60}违约金',)),
    ], trigger=('违约金',)),
    R('COMMON', 25, 'common_attachment_effect', '附件与合同文件效力及冲突顺位', ('附件', '附页', '补充协议'), '《民法典》第466条、第510条', [
        ('附件或补充文件效力', (r'(?:附件|补充协议|附页)[^。\n]{0,70}(?:法律效力|组成部分|同等效力)',)),
        ('合同文件冲突处理', (r'(?:附件|补充协议|文件)[^。\n]{0,80}(?:冲突|不一致|为准|优先)',)),
    ], trigger=('附件', '附页', '补充协议'), risk='低'),
)


def compose(rows):
    nodes = {r.node_id for r in rows}
    return tuple(rows) + tuple(r for r in ROWS if r.node_id not in nodes)
