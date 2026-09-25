"""Separate contractual floors/formulas from actual losses and liability caps."""
from review_v2.fact_validation import FactExtractionError

KINDS = {'FIXED_AMOUNT', 'MINIMUM_AMOUNT', 'FORMULA'}
DESCRIPTION = '''每项预设责任增加liability_kind：FIXED_AMOUNT固定责任、MINIMUM_AMOUNT最低责任、FORMULA比例或公式责任。
不以条款标题或是否使用违约金称谓决定性质。实际损失责任与最低赔偿额可同时存在：分别保存worker.damage_liability与penalties.obligations。
最低责任额独立于实际损失量；超过最低额再赔差额不会消除最低额。amount_text仅保留最低/固定金额或公式原文，trigger和scope按实际触发义务确定。
只有实际损失、依法担责且没有预设金额/比例/公式时不生成penalties.obligations。
上限是责任限制，不是最低额：仅赔实际损失且设上限，保存worker.liability_limit和实际损失事实，不生成penalty。
按实际损失的约定比例赔偿属于FORMULA，保留比例及实际损失这一计算基数，不作为纯实际损失或固定金额。
不能因同段有实际损失描述覆盖最低额、固定额或比例；核验必须逐个责任组成判断。'''


def normalize(value):
    if 'liability_kind' in value and value['liability_kind'] not in KINDS:
        raise FactExtractionError('INVALID_PRESET_LIABILITY_KIND', field='penalties.obligations.liability_kind',
                                  actual=value['liability_kind'], expected=sorted(KINDS))
    return value
