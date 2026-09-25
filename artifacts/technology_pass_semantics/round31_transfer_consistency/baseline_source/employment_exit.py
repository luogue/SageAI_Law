"""Classify employer termination predicates with their governing list heading.

No article numbers, employers or dates determine classification. A list item
inherits the actor and permission/prohibition, never a sibling's conditions.
"""
import re


def classify_exit_clauses(clauses):
    rows = []
    for clause in clauses:
        if clause.section_type not in {'正式合同条款', '附件'}:
            continue
        parents = list(clause.heading_path or [])
        heading = parents[0] if len(parents) > 1 else ''
        text = clause.text
        context = heading or text
        protective = bool(re.search(r'(?:甲方|用人单位)不得[^。；\n]{0,60}解除', context))
        permission = bool(re.search(r'(?:甲方|用人单位)[^。；\n]{0,80}(?:可以|有权|可)解除', context))
        if not (protective or permission):
            continue
        if not heading and re.search(r'下列情形|以下情形', text) and text.rstrip().endswith(('：', ':')):
            continue
        category, reason = 'MANUAL_VERIFICATION', '需核实事实、适用法律及解除条件，不直接推定违法。'
        if protective:
            category, reason = 'PROTECTIVE', '限制用人单位解除，属于劳动者保护条款。'
        elif re.search(r'被证明不符合录用条件|被依法追究刑事责任', text):
            category, reason = 'STATUTORY', '对应法定解除事由，实际适用仍需事实证明。'
        elif re.search(r'不能胜任工作', text) and re.search(r'(?:培训|调整工作岗位|调岗).{0,15}仍不能胜任', text):
            category, reason = 'STATUTORY', '保留培训或调岗后仍不能胜任的前置条件。'
        elif re.search(r'客观情况.{0,10}重大变化', text) and re.search(r'协商', text) and re.search(r'未能|不成|无法达成', text):
            category, reason = 'STATUTORY', '保留客观情况重大变化及协商变更不成的前置条件。'
        elif re.search(r'同时与其他用人单位建立劳动关系', text) and re.search(r'严重影响|拒不改正', text):
            category, reason = 'STATUTORY', '保留双重劳动关系造成严重影响或拒不改正条件。'
        elif re.search(r'医疗期满', text) and re.search(r'不能从事原工作', text):
            category = 'STATUTORY' if re.search(r'不能从事.{0,20}另行安排', text) else 'EXPANDED_RIGHT'
            reason = '核对原岗位及另行安排工作均不能从事；仅前者不足以成立该解除权。'
        elif re.search(r'构成严重违纪|严重违反.{0,15}(?:依法制定|公示).{0,15}(?:规章制度|制度)', text):
            category, reason = 'DISCIPLINARY_VERIFICATION', '已限定严重违纪，仍须核验制度合法制定、公示及实际严重程度。'
        elif re.search(r'不服从.{0,12}管理|拒绝参加考核|违反.{0,10}计划生育|行政拘留', text):
            category, reason = 'EXPANDED_RIGHT', '该事项被单独设为解除事由，未限定为有合法制度及事实支持的严重违纪，不等同于法定即时解除事由。'
        elif re.search(r'(?:项目)?负责人.{0,12}调离|经费来源终止|年度考核不合格', text):
            category, reason = 'EXPANDED_RIGHT', '单独扩张解除条件；通知或代通知金不能替代不能胜任或客观情况变化的法定前提。'
        elif re.search(r'严重违反.{0,15}规章制度|旷工|擅自离岗|擅自出国|逾期不归', text):
            category, reason = 'DISCIPLINARY_VERIFICATION', '可能属于严重违纪；须核验制度合法制定、公示、严重程度及行为证据。'
        elif re.search(r'失职|营私舞弊', text) and re.search(r'重大损害', text):
            category, reason = 'MANUAL_VERIFICATION', '核实是否达到严重失职或营私舞弊并造成重大损害，不能只凭事故或一般失职解除。'
        rows.append({'clause_id': clause.clause_id, 'location': clause.location,
                     'text': text, 'quote': text, 'heading': heading,
                     'section_type': clause.section_type, 'source_type': 'CONTRACT_TEXT',
                     'classification': category, 'reason': reason,
                     'polarity': 'PROTECTIVE' if protective else 'AFFIRMED'})
    return rows


def exit_adverse_evidence(clauses):
    return [row for row in classify_exit_clauses(clauses) if row['classification'] == 'EXPANDED_RIGHT']
