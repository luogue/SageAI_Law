"""Predicate-level evidence: a topic mention never proves an adverse act.

Profiles describe acts, while polarity and source binding are shared. Negation
is scoped to the proposition, not to the whole document or a keyword window.
"""
from __future__ import annotations

import re


def proposition_polarity(text: str, start: int, end: int, *, context_before: str = '') -> str:
    prefix, suffix = text[:start], text[end:]
    # An exception/contrast opens a new proposition; an earlier ban cannot
    # immunize a later permission. Commas alone do not terminate a shared ban.
    prefix = re.split(r"但(?:是)?|然而|不过|除外|；|;", prefix)[-1]
    # A new contract-level temporal proposition is not governed by a ban
    # on the actor's different, preceding conduct.
    prefix = re.split(r"[,，](?=(?:本|该)(?:合同|协议))", prefix)[-1]
    prefix = re.split(r"[,，](?=(?:双方|发包人|承包人|甲方|乙方)?(?:可|允许|有权|同意|应当|必须|放弃|将|另行|签订))", prefix)[-1]
    if re.search(r"(?:并非|不是|不属于).{0,8}$", prefix):
        return "NEGATED"
    if re.search(r"(?:不得不|不能不|并非不得|不禁止|不限制)", prefix):
        return "AFFIRMED"
    if re.search(r"不得|不允许|不准|禁止|严禁|不得以|不再|不进行|不予|不应|不签订|承诺不|保证不|没有|不存在|未发生|未进行|未签订|杜绝|防止|避免|不能|不$", prefix):
        return "NEGATED"
    if re.search(r"^(?:的)?(?:行为|安排|条款)?(?:无效|不生效|被禁止|不予认可|不予支持|不被允许|是禁止的)", suffix):
        return "NEGATED"
    permission = bool(re.search(r'(?:允许|同意|可以|可|准许|有权)[^。；]{0,20}$', prefix))
    # A breach tariff or conditional remedy describes consequences of an act,
    # not permission to perform it. Keep express permission/exception clauses
    # separate even when they also allocate consequences.
    if not permission and re.search(r'解除|终止|赔偿|违约金|罚款|承担[^。；]{0,12}责任', suffix):
        if re.search(r'存在|发生|若|如|一旦|擅自|违法|违规|未经', prefix) or re.match(r'[^。；]{0,24}(?:时|的[，,]|[：:]|属于违约|构成违约)', suffix):
            return 'PREVENTIVE'
    if not permission and re.search(r"(?:如|若|如果|一旦|发生|发现|存在).*$", prefix) and re.search(r"违约|赔偿|解除|责任|处罚|纠正", suffix):
        return "PREVENTIVE"
    # A list item inherits the controlling sanction from its actual introduction.
    # A later independent permission/exception starts a new proposition instead.
    if not permission:
        introductions = list(re.finditer(r'(?:发生|存在|出现|有)?(?:以下|下列|如下)[^。\n]{0,100}(?:解除|终止|赔偿|违约|处罚|罚款|纠正|承担[^。\n]{0,12}责任)[^。\n]*[：:]', context_before))
        if introductions:
            tail = context_before[introductions[-1].end():]
            if not re.search(r'[。！？]|(?:但是|然而|不过)|\n\s*(?:第[一二三四五六七八九十\d]+条|[一二三四五六七八九十]+、)', tail):
                return 'PREVENTIVE'
    return "AFFIRMED"


def direct_evidence(clauses, predicates, *, require_assertion=True):
    """Return affirmative and counter evidence with untruncated source quotes."""
    positive, counter = [], []
    preceding = ""
    for clause in clauses:
        if clause.section_type not in {"正式合同条款", "附件"}:
            continue
        inherited = preceding
        preceding = (preceding + "\n" + clause.text)[-2000:]
        for sentence in re.finditer(r"[^。；;！？\n]+[。；;！？]?", clause.text):
            quote = sentence.group().strip()
            if require_assertion and not re.search(r"发包人|承包人|分包人|分包单位|甲方|乙方|双方|存在|擅自|违约金|罚款|不得|禁止|不再|允许|有权|已|应|须|同意|将|签订|放弃", quote):
                continue
            for proposition in re.split(r"(?=但(?:是)?|然而|不过)", quote):
                for predicate in predicates:
                    match = re.search(predicate, proposition, re.I)
                    if not match:
                        continue
                    group = "act" if "act" in match.groupdict() else 0
                    polarity = proposition_polarity(proposition, match.start(group), match.end(group),
                        context_before=inherited + "\n" + clause.text[:sentence.start()])
                    row = {"clause_id": clause.clause_id, "location": clause.location,
                           "title": clause.title, "text": proposition, "quote": proposition,
                           "section_type": clause.section_type, "block_type": clause.block_type,
                           "predicate": match.group(group), "polarity": polarity}
                    if polarity == 'PREVENTIVE' and ':' in clause.text[:sentence.start()].replace('：', ':'):
                        row['polarity_context'] = clause.text[:sentence.end()]
                    target = positive if polarity == "AFFIRMED" else counter
                    if row not in target:
                        target.append(row)
    return positive, counter
