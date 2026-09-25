"""A data-use permission is the tuple (actor, data object, purpose, condition)."""
import re
from review_v2.proposition_scope import arrangement_matches, PERMISSION_MODAL


def data_use_permissions(clauses):
    result = []
    actor = r'(?:[甲乙丙]方|服务方|服务提供方|受托方|接收方)'
    # The permission must govern retention/use, not an incidental noun or a
    # prohibition. A different sentence's object/purpose cannot fill the tuple.
    pattern = actor + r'\s*' + PERMISSION_MODAL + r'[^。；;]{0,100}(?:使用|保留|保存|用于)'
    for clause in clauses:
        for row in arrangement_matches(pattern, clause.text):
            q = row['quote']
            if not re.search(r'数据|信息', q):
                continue
            operative = q[row['match_start']:]
            purpose = re.search(r'(?:用于|用作|使用于)([^。；;]+)', operative)
            if not purpose:
                continue
            obj = operative[:purpose.start()]
            actor_name = re.match(actor, operative)[0]
            anonymous = bool(re.search(r'匿名化(?:的)?统计(?:数据|信息)|无法识别[^。；;]{0,55}(?:匿名化|(?:汇总)?统计(?:数据|信息))', obj))
            # The sentence actor is not automatically the data's owner. Bind
            # the possessor inside the object phrase, before its data noun.
            owned = re.search(r'(?P<owner>甲方|乙方|委托方|客户|对方)(?:的)?'
                              r'(?:(?:原始|生产|运行|测试|设备|项目|客户|经营|业务|统计|个人|提供的|提供|掌握的|收集的)){0,5}数据', obj)
            owner = owned['owner'] if owned else None
            object_type = ('ANONYMOUS_STATISTICS' if anonymous else 'OWN_DATA' if owner == actor_name
                           else 'COUNTERPARTY_DATA' if owner else 'UNSPECIFIED_DATA')
            external = bool(re.search(r'模型训练|训练[^。；;]{0,25}模型|算法优化|产品优化|其他客户|其他项目|科研|融资|技术展示', purpose[1]))
            result.append(dict(clause_id=clause.clause_id, quote=q, location=clause.location,
                               actor=actor_name, data_object=object_type, data_owner=owner,
                               purpose=purpose[1], proposition_polarity='AFFIRMATIVE',
                               external_use=external, condition=row.get('condition','')))
    return result
