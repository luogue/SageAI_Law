"""Source-bound cross references and conservative versioned statute validation.

Only verified statute topics are resolved locally. Unknown versions/articles
require external verification; they are never inferred to be invalid.
"""
import re
from dataclasses import replace
from review_v2.priority_checklist_helpers import required as R
from review_v2.lease_semantics import requirement

NUM = r'[0-9零〇一二两三四五六七八九十百千]+'
LEGAL = re.compile(r'《([^》]+)》\s*第(' + NUM + r')条')
REF = re.compile(r'(?:(?:本协议|本合同|合同|协议)\s*)?第(' + NUM + r')条(?:\s*第?(' + NUM + r')(款|项))?')
HEAD = re.compile(r'^\s*(?:第(' + NUM + r')条|([' + '一二三四五六七八九十百' + r']+)[、．.])\s*(.*)')
DECIMAL_HEAD = re.compile(r'^\s*(\d+)(?:[.．](\d+))?(?:[.．、]\s*|\s+)(\S[^\n]*)')
TOPICS = {
    '违约责任': r'违约|赔偿|违约金|补偿损失',
    '通知送达': r'送达|通知地址|联系方式',
    '争议解决': r'仲裁|管辖|诉讼|争议解决',
    '重大事项': r'重大事项|股东会|表决|决议',
    '日期计算': r'(?:日期|时间)[^。；]{0,8}计算|实际交货日期|签收[^。；]{0,15}日期',
}
# Current law verified against NPC published 2023 revision, effective 2024-07-01.
STATUTES = {
    '公司法': {'version': '2023修订', 'effective_from': '2024-07-01',
        'source': 'https://www.npc.gov.cn/npc/c2/c30834/202312/t20231229_433999.html',
        'articles': {38: ('分公司设立登记', r'分公司|登记'), 58: ('股东会组成', r'股东会|全体股东'),
                     59: ('股东会职权及书面一致决定', r'重大事项|股东会|决定|决议|职权'),
                     60: ('只有一个股东的公司', r'一个股东|一人公司|唯一股东')}},
}


def number(s):
    if s.isdigit():
        return int(s)
    digits = {c: i for i, c in enumerate('零一二三四五六七八九')}
    digits.update({'〇': 0, '两': 2})
    total = current = 0
    for c in s:
        if c in '十百千':
            total += (current or 1) * {'十': 10, '百': 100, '千': 1000}[c]
            current = 0
        else:
            current = digits[c]
    return total + current


def analyze(clauses):
    rows = [c for c in clauses if c.section_type in {'正式合同条款', '附件'}]
    sections, contexts, current = {}, {}, None
    explicit_articles=any(re.match(r'^\s*第'+NUM+r'条',c.text) for c in rows)
    for c in rows:
        heading = HEAD.match(c.text)
        decimal = DECIMAL_HEAD.match(c.text) if not explicit_articles else None
        if heading and explicit_articles and not heading[1]:heading=None
        if heading or decimal:
            current = number(heading[1] or heading[2]) if heading else int(decimal[1])
            sections.setdefault(current, []).append(c)
        elif current is not None:
            sections[current].append(c)
        contexts[c.clause_id] = current
    output = {'common_internal_references': [], 'common_legal_references': []}
    for index, c in enumerate(rows):
        parent = sections.get(contexts[c.clause_id], [c])
        context = '\n'.join(x.text for x in parent)
        legal_spans = []
        for m in LEGAL.finditer(c.text):
            legal_spans.append(m.span())
            law = m[1].removeprefix('中华人民共和国')
            entry = STATUTES.get(law)
            article = entry and entry['articles'].get(number(m[2]))
            status, reason = 'UNVERIFIED', '本地版本化法规库尚不能可靠确认该条引用内容及适用版本，请人工核验；不直接认定引用无效。'
            if article:
                if re.search(article[1], c.text):
                    status, reason = 'VALID', '引用语义与本地现行版本条文主题一致。'
                elif re.search(TOPICS['重大事项'], c.text) and not re.search(TOPICS['重大事项'], article[0]):
                    status, reason = 'INVALID', f'所引{law}第{number(m[2])}条在{entry["version"]}版规定{article[0]}，与此处股东重大事项职权不对应，存在旧模板条号或错引风险；应核对现行职权条款及合同适用时间。'
            output['common_legal_references'].append({'source': c, 'reference': m.group(), 'status': status, 'reason': reason,
                'version': entry['version'] if entry else None, 'source_url': entry['source'] if entry else None})
        for m in REF.finditer(c.text):
            if any(a <= m.start() < b or a < m.end() <= b for a, b in legal_spans):
                continue
            if HEAD.match(c.text) and m.start() == len(c.text) - len(c.text.lstrip()):
                continue
            target = sections.get(number(m[1]), [])
            status, reason = 'VALID', '被引用条款及对应层级存在，未发现明确语义冲突。'
            target_text = '\n'.join(x.text for x in target)
            if not target:
                status, reason = 'INVALID', '被引用条款不存在。'
            elif m[2]:
                markers = list(re.finditer(r'(?:^|\n)\s*[（(]?(' + NUM + r')[）)、.．]', target_text))
                found = next((i for i, p in enumerate(markers) if number(p[1]) == number(m[2]) and (m[3] == '项' or not p.group().lstrip().startswith(('（', '(')))), None)
                if found is None:
                    status, reason = 'INVALID', '被引用条款存在，但指定款/项层级不存在。'
                else:
                    level = 2 if markers[found].group().lstrip().startswith(('（', '(')) else 1
                    end = next((p.start() for p in markers[found+1:] if (2 if p.group().lstrip().startswith(('（', '(')) else 1) <= level), len(target_text))
                    target_text = target_text[markers[found].start():end]
            # Only the referring sentence supplies the purpose. Other duties
            # in this parsed article (e.g. material inspection notice) do not.
            start=max(c.text.rfind(mark,0,m.start()) for mark in ('。','；','\n'))+1
            ends=[p for mark in ('。','；','\n') if (p:=c.text.find(mark,m.end()))>=0]
            referring_sentence=c.text[start:min(ends) if ends else len(c.text)]
            intended = [name for name, pattern in TOPICS.items() if re.search(pattern, referring_sentence)]
            for name in intended:
                if target and not re.search(TOPICS[name], target_text) and any(re.search(p, target_text) for p in TOPICS.values()):
                    heading = target[0].text.splitlines()[0]
                    status, reason = 'INVALID', reason + f'引用目的为{name}，但目标条款“{heading}”内容属于其他事项，与引用语义不对应。'
            resolution = {
                'source_type': 'REFERENCE_AUDIT',
                'cross_reference_exists': True,
                'referenced_target_unresolved': not bool(target),
                'target_number': number(m[1]),
                'indexed_article_numbers': sorted(sections),
                'target_clause_ids': [x.clause_id for x in target],
                'searched_clause_ids': [x.clause_id for x in rows],
                'reference': m.group(),
                'result': status,
                'reason': reason,
            }
            output['common_internal_references'].append({'source': c, 'reference': m.group(), 'status': status, 'reason': reason, 'target_ids': [x.clause_id for x in target], 'reference_audit': resolution})
        for m in re.finditer(r'(?:详见|参见|见|按照|依据)\s*附件(?:\s*(' + NUM + r'))?', c.text):
            targets = [x for x in rows if x.section_type == '附件' and (
                re.match(r'^\s*附件\s*' + re.escape(m[1]) + r'(?:\s|[：:、.])', x.text) if m[1]
                else re.match(r'^\s*附件(?:\s|$)',x.text))]
            attached = len(targets) == 1
            output['common_internal_references'].append({'source': c, 'reference': m.group(), 'status': 'VALID' if attached else 'UNVERIFIED', 'reason': '附件可定位。' if attached else '未能唯一定位所引用附件，需核验附件完整性；不认定附件不存在。', 'target_ids':[x.clause_id for x in targets]})
        for m in re.finditer(r'按照前款|依据上述第(' + NUM + r')项', c.text):
            previous = [x for x in rows[:index] if contexts[x.clause_id] == contexts[c.clause_id] and not HEAD.match(x.text)]
            target = previous[-1:] if not m[1] else [x for x in previous if re.match(r'^\s*[（(]?'+re.escape(m[1])+r'[）)、.．]', x.text)]
            status, reason = 'UNVERIFIED', '相对引用尚不能可靠定位到独立前款或前项，需结合完整条款层级人工复核。'
            if target:
                target_text = '\n'.join(x.text for x in target)
                status, reason = 'VALID', '在当前条文内定位到相对引用目标，未发现明确语义冲突。'
                for name, pattern in TOPICS.items():
                    if re.search(pattern, c.text) and not re.search(pattern, target_text) and any(re.search(p, target_text) for p in TOPICS.values()):
                        status, reason = 'INVALID', f'相对引用目的为{name}，但前款或前项属于其他事项，与引用语义不对应。'
            output['common_internal_references'].append({'source': c, 'reference': m.group(), 'status': status, 'reason': reason, 'target_ids': [x.clause_id for x in target]})
    return output


CHECKPOINTS = tuple(replace(R('COMMON', n, node, title, terms, '《民法典》第142条、第466条', [
    ('引用对象与语义一致', (r'(?!)',)),
], suggestion=suggestion), applicable_if='合同正文出现显式引用时适用。', legal_basis_topics=('intent_interpretation','interpretation')) for n, node, title, terms, suggestion in (
    (21, 'common_internal_references', '合同条款交叉引用一致性', ('第', '条', '附件', '前款'), '逐项核对条、款、项和附件的实际编号及内容，修正不存在或指向无关事项的引用。'),
    (22, 'common_legal_references', '法律条文引用有效性', ('公司法', '民法典', '条'), '核对所引法规的有效版本、条号和内容，修正错引；适用时间或条文内容不能可靠确认时人工复核。'),
))


def augment(checklist, text):
    from review_v2.clause_parser import parse_contract_clauses
    findings = analyze(parse_contract_clauses(text))
    nodes = {c.node_id for c in checklist}
    return tuple(checklist) + tuple(c for c in CHECKPOINTS if findings[c.node_id] and c.node_id not in nodes)


def requirements(node, clauses):
    result = []
    for i, row in enumerate(analyze(clauses)[node]):
        element = requirement(node + '_' + str(i+1), row['reference'] + '引用核验', re.escape(row['source'].text))
        element.update(evidence_unit='clause',reference_resolution={k:v for k,v in row.items() if k!='source'})
        element['evidence_unit'] = 'clause'
        if row['status'] == 'UNVERIFIED':
            element.update(requirement_kind='EXTERNAL_VERIFICATION', verification_instruction=row['reference'] + '：' + row['reason'], risk_relevant=False)
        result.append(element)
    return result


def adverse(node, clauses):
    return [{**row['source'].to_public_dict(), 'quote': row['source'].text, 'quoted_text': row['source'].text, 'original_excerpt': row['source'].text, 'reason': row['reference'] + '：' + row['reason']}
            for row in analyze(clauses)[node] if row['status'] == 'INVALID']
