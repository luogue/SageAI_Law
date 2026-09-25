"""Development provenance: a contractual promise is not a supplied document."""
import re
from review_v2.obligation_detail_elements import _element, _segments
from review_v2.technology_service_elements import sources

FAMILIES = ('development_creator', 'development_proof')


def inventor_attribution_sources(clauses):
    proof = sources(clauses,
        r'(?:应|须|按照|根据)[^。；]{0,25}(?:实际|实质)[^。；]{0,8}(?:技术)?贡献[^。；]{0,18}(?:确定|确认|列明)发明人|'
        r'(?:发明人|设计人|完成.{0,8}人员|完成人).{0,25}(?:署名权|有权署名)|享有.{0,8}发明人署名权')
    for row in proof:
        # Keep the operative proposition separate from its evidentiary heading.
        # Report prose must not promote source metadata to a new factual claim.
        row['proposition'] = row['quote']
        clause = next(c for c in clauses if c.clause_id == row['clause_id'])
        prefix = clause.text[:clause.text.find(row['quote'])]
        if re.search(r'发明人署名', prefix) and not re.search(r'未.*署名', prefix):
            row['quote'] = prefix + row['quote']
    return proof


def elements(family, clauses):
    def find(pattern, **kwargs):
        return sources(clauses, pattern, **kwargs)
    if family == 'development_creator':
        specs = [
            ('inventor_contribution_attribution', '实际完成人的发明人署名安排', inventor_attribution_sources(clauses)),
            ('creator_reward_arrangement', '实际完成人的奖励报酬安排',
             find(r'(?:应|须|有权)[^。；]{0,25}(?:奖励|报酬)|(?:奖励|报酬)[^。；]{0,20}(?:支付|发放|享有)', context=r'发明人|完成人|研发人员')),
        ]
        keys = {'inventor_contribution_attribution':'technology.creator.attribution',
                'creator_reward_arrangement':'technology.creator.reward_arrangement'}
        return [_element(k, label, proof, source_fact_key=keys[k])
                for k, label, proof in specs]
    specs = [
        ('background_technology_statement', '背景技术范围及归属声明', 'contractual_statement',
         find(r'(?:背景技术|既有技术)[^。；]{0,30}(?:归|包括|所列)|(?:保留|拥有)[^。；]{0,25}背景技术', inherit_lists=True)),
        ('project_application_ownership_statement', '项目专利申请权归属声明', 'contractual_statement',
         find(r'专利申请权[^。；]{0,20}归[^。；]{0,15}所有')),
        ('employee_ownership_document_obligation', '研发人员职务成果归属文件义务', 'documentary_proof_obligation',
         find(r'(?:应|须)[^。；]{0,60}签署[^。；]{0,18}职务成果归属文件')),
        ('employee_ownership_documents', '研发人员职务成果证明链', 'documentary_proof',
         find(r'(?:目前|已经|已)[^。；]{0,30}(?:提供|持有)[^。；]{0,35}(?:完整|签署)[^。；]{0,18}(?:职务成果|归属)(?:归属)?文件')),
        ('third_party_license_documents', '第三方组件许可证及限制材料义务', 'documentary_proof_obligation',
         find(r'(?:许可证类型|商业使用限制|第三方组件清单)', inherit_lists=True)),
        ('development_source_records', '研发来源及人员记录提供义务', 'documentary_proof_obligation',
         find(r'(?:研发过程记录|技术来源证明|研发人员记录)', inherit_lists=True)),
    ]
    result = []
    for key, label, layer, proof in specs:
        if layer == 'documentary_proof_obligation':
            proof = [s for s in proof if re.search(r'应|须|提供|提交|签署', s['quote'])]
        row = _element(key, label, proof, source_fact_key='technology.development_proof.' + key,
                       proof_layer=layer)
        if key == 'employee_ownership_documents' and proof:
            gaps = [dict(clause_id=c.clause_id, quote=q) for c, _, q in _segments(clauses)
                    if re.search(r'(?:无法|未能|不能|尚未)[^。；]{0,15}提供[^。；]{0,45}(?:归属确认|职务成果|权属)', q)]
            if gaps:
                row.update(status='PARTIALLY_COVERED', residual_gap='未获完整确认人员的职务成果归属证明材料',
                           search_targets=['研发人员职务成果归属确认材料完整性'],
                           explicit_absence_evidence=gaps)
        result.append(row)
    return result
