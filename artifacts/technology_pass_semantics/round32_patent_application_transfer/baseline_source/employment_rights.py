"""Employment rights: scoped legal effects, rather than topic mentions.

An employee's cooperation duty is not an employer exemption. Likewise a
work-related IP allocation is not a blanket assignment of personal creations.
"""
import re
from review_v2.adverse_evidence import proposition_polarity


def rights_evidence(node, clauses):
    rows = []
    for clause in clauses:
        if clause.section_type not in {'正式合同条款', '附件'}:
            continue
        heading = ' '.join(clause.heading_path or [])
        for sentence in re.finditer(r'[^。！？\n]+[。！？]?', clause.text):
            text = sentence.group().strip()
            effects = []
            if node == 'employment_illegal_waiver':
                if not re.search(r'社会保险|社保|参保', text):
                    continue
                limited = bool(re.search(r'仅.{0,20}(?:损失|过错)|限于.{0,20}(?:损失|过错)|不免除.{0,25}(?:甲方|用人单位)|(?:甲方|用人单位)仍.{0,20}(?:缴纳|参保|承担)', text))
                transfer = re.search(r'(?:社会保险|社保|参保).{0,35}?(?P<act>(?:全部|所有)?责任(?:全部|均)?由(?:乙方|劳动者|个人)(?:全部|自行)?承担)', text)
                exemption = re.search(r'(?:未.{0,12}(?:材料|资料)|未配合).{0,45}?(?P<act>(?:甲方|用人单位)(?:当然|一概|全部)?(?:免责|不承担.{0,12}责任|免除.{0,12}责任))', text)
                for match, effect in [(transfer, 'BLANKET_EMPLOYER_LIABILITY_TRANSFER'), (exemption, 'AUTOMATIC_EMPLOYER_EXEMPTION')]:
                    if match and not limited and proposition_polarity(text, match.start('act'), match.end('act')) == 'AFFIRMED':
                        effects.append(effect)
                employee_remedy = bool(re.search(r'(?:乙方|劳动者).{0,12}(?:可以|有权).{0,8}解除', heading + text))
                if employee_remedy and re.search(r'未依法.{0,15}缴纳.{0,10}(?:社会保险|社保)', text) and re.search(r'(?:未提交|未提供).{0,20}(?:材料|资料).{0,12}(?:除外|不适用)', text):
                    effects.append('STATUTORY_REMEDY_EXCLUSION')
                denied = re.search(r'(?:乙方|劳动者)(?P<act>不得|无权).{0,25}(?:未缴|欠缴|不缴).{0,10}(?:社会保险|社保).{0,20}(?:解除|补偿|追责)', text)
                if denied and proposition_polarity(text, denied.start('act'), denied.end('act')) == 'AFFIRMED':
                    effects.append('STATUTORY_REMEDY_EXCLUSION')
            elif node == 'employment_ip_ownership':
                if not re.search(r'成果|发明|作品|著作|论文|署名|知识产权', text):
                    continue
                # Work nexus must qualify the allocation itself, not merely be
                # mentioned in an unrelated neighboring provision.
                nexus = bool(re.search(r'仅限|(?<!不)限于|执行.{0,12}(?:单位|甲方).{0,8}任务|完成.{0,12}工作任务|主要利用.{0,15}物质技术条件|依法认定的职务|非职务.{0,12}除外|不包括.{0,12}非职务', text))
                if re.search(r'无论|不论|不管|与.{0,30}(?:工作|任务).{0,10}无关', text):
                    nexus = False
                temporal = bool(re.search(r'(?:合同期内|合同期限内|在职期间|任职期间|劳动关系存续期间)', text))
                allocation = re.search(r'(?P<act>均属|均为|均视为|都是|一概认定为|一律认定为|全部属于|一律属于|全部归|一律归|皆归|均归|均由).{0,20}(?:职务|甲方|单位|用人单位)', text)
                if allocation and temporal and not nexus and proposition_polarity(text, allocation.start('act'), allocation.end('act')) == 'AFFIRMED':
                    effects.append('TIME_ONLY_BLANKET_SERVICE_RESULTS')
                nonservice = re.search(r'(?:非职务(?:发明|成果|作品)|与.{0,35}(?:本职工作|单位任务).{0,20}无关.{0,20}(?:发明|成果|作品)).{0,35}?(?P<act>(?:也|仍|全部|均)?(?:归|属于|由)).{0,12}(?:甲方|单位|用人单位)', text)
                if nonservice and proposition_polarity(text, nonservice.start('act'), nonservice.end('act')) == 'AFFIRMED' and not re.search(r'另行.{0,12}(?:转让|协议)|自愿.{0,12}转让', text):
                    effects.append('NONSERVICE_RESULTS_APPROPRIATION')
                personal = re.search(r'(?:乙方|劳动者|作者).{0,15}?(?P<act>放弃|转让).{0,12}署名权|署名权(?P<assignment>全部归|归|属于).{0,8}(?:甲方|单位)', text)
                if personal:
                    group = 'act' if personal.groupdict().get('act') else 'assignment'
                    if proposition_polarity(text, personal.start(group), personal.end(group)) == 'AFFIRMED':
                        effects.append('AUTHORSHIP_RIGHT_DEPRIVATION')
                if allocation and not nexus and re.search(r'所有作品|全部作品|全部论文|所有著作', text) and proposition_polarity(text, allocation.start('act'), allocation.end('act')) == 'AFFIRMED':
                    effects.append('UNDIFFERENTIATED_COPYRIGHT_ALLOCATION')
                if allocation and not nexus and sum(bool(re.search(p, text)) for p in (r'专利',r'著作|论文',r'经费',r'奖励')) >= 3:
                    if proposition_polarity(text, allocation.start('act'), allocation.end('act')) == 'AFFIRMED':
                        effects.append('MIXED_LEGAL_ASSETS_BLANKET_ALLOCATION')
            if effects:
                rows.append({'clause_id': clause.clause_id, 'location': clause.location,
                             'title': clause.title, 'text': text, 'quote': text,
                             'section_type': clause.section_type, 'source_type': 'CONTRACT_TEXT',
                             'heading_path': list(clause.heading_path or []),
                             'legal_effects': sorted(set(effects)), 'polarity': 'AFFIRMED'})
    return rows


EFFECT_REASONS = {
    'employment_illegal_waiver': '原文概括转嫁社保未缴责任或以材料欠缺排除法定救济；配合提交材料义务不等于用人单位当然免责。应保留法定参保缴费责任及劳动者救济，具体过错和损失另行依法核验。',
    'employment_ip_ownership': '原文将成果归属作一揽子分配，未按单位任务、工作关联及物质技术条件区分职务与非职务成果。专利、作品财产权、署名等人身权及经费奖励应分别界定；仅署作者单位不等于剥夺个人署名权。',
}
