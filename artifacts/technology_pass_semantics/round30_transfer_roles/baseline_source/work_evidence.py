"""Commissioned-result propositions bound to sentence-level canonical sources."""
import re
from review_v2.sale_evidence import atom, extract, PROFILES as GOODS_PROFILES

SPECS = {
 'contract_type_identification': ('按定作要求完成加工工作', r'定作[人方].{0,15}委托.{0,20}(?:加工|制作)|承揽[人方].{0,60}(?:生产加工|加工制作)'),
 'specific_work_purpose': ('按图纸样品完成特定成果', r'按照.{0,60}(?:图纸|样品).{0,30}(?:加工|生产|制作)'),
 'sale_distinction': ('根据定作要求加工而非标准产品交易', r'按照.{0,60}(?:图纸|样品).{0,30}(?:加工|生产|制作)'),
 'nature_confusing_standard_product': ('仅转让现货标准产品而不完成定作工作', r'仅.{0,15}(?:采购|销售|交付).{0,10}(?:现货|标准产品)|无需.{0,10}(?:定作|加工)'),
 'contractor_capacity': ('承揽人名称及主体身份', r'承揽[人方][：:].{2,}'),
 'professional_license': ('承揽人履行工作所需专业许可', r'承揽[人方].{0,25}(?:持有|具备|提供).{0,15}(?:资质|许可证|执业资格)'),
 'equipment_technology_labor': ('承揽人完成工作的自身设备技术人员', r'承揽[人方].{0,20}(?:自己的|自有|具备).{0,15}(?:设备|技术|人员)'),
 'safety_compliance': ('承揽工作安全环保义务', r'承揽[人方].{0,30}(?:安全生产|环境保护|环保|操作规范)'),
 'personal_completion_main_work': ('主要工作亲自完成或禁止未经同意转交', r'亲自完成.{0,12}主要工作|未经定作[人方].{0,15}同意.{0,35}不得.{0,30}(?:主要加工任务|主要工作).{0,15}(?:转包|分包)'),
 'main_subcontract_consent': ('主要工作转包须经定作人同意', r'未经定作[人方].{0,15}同意.{0,40}不得.{0,30}(?:转包|分包)'),
 'auxiliary_subcontract_liability': ('辅助分包仍由承揽人负责', r'辅助工作', r'第三[人方]|分包', r'承揽[人方].{0,20}(?:负责|责任)'),
 'illegal_total_subcontract': ('未经同意允许全部转包', r'(?:有权|可以|允许).{0,18}(?:全部转包|肢解转包)'),
 'customer_assistance_scope': ('定作人提供资料等协助事项', r'定作[人方].{0,40}(?:提供|提交).{0,30}(?:图纸|技术|样品|资料)'),
 'customer_assistance_deadline': ('定作人提供协助的期限', r'定作[人方].{0,40}(?:日前|日内).{0,30}(?:提供|提交)'),
 'assistance_urge_extension': ('定作人未协助时催告及顺延', r'协助|提供资料|提供图纸', r'催告', r'顺延|延长'),
 'assistance_rescission': ('催告后未履行协助义务可解除', r'协助|提供资料|提供图纸', r'催告', r'解除'),
 'customer_change_procedure': ('定作要求变更的书面程序', r'定作[人方].{0,20}(?:变更|修改)', r'书面|确认'),
 'change_cost_adjustment': ('变更工作要求导致费用调整', r'变更|修改要求', r'费用|报酬|价款', r'增加|调整|承担'),
 'change_period_extension': ('变更工作要求导致工期调整', r'变更|修改要求', r'工期|工作期限', r'顺延|调整|延长'),
 'change_loss_compensation': ('定作变更造成损失补偿', r'变更|修改要求', r'损失', r'赔偿|补偿'),
 'material_provider': ('承揽材料由哪方提供', r'承揽[人方]|定作[人方]', r'提供原材料|原材料.{0,12}(?:提供|采购)'),
 'customer_material_inspection_notice': ('定作人来料检验及异常通知', r'定作[人方].{0,8}提供.{0,8}材料', r'检验|检查', r'通知'),
 'material_defect_liability': ('材料瑕疵责任归属', r'材料', r'瑕疵|不合格|质量问题', r'承担|赔偿|责任'),
 'material_result_custody': ('承揽人妥善保管定作资料或成果', r'承揽[人方].{0,15}(?:妥善保管|保管义务)', r'资料|样品|图纸|材料|成果'),
 'quality_standard': ('加工产品的质量标准', r'产品|成品|成果', r'质量标准|技术规范|企业标准|国家标准|尺寸公差'),
 'sample_drawing_standard': ('按定作图纸样品确定成果标准', r'按照.{0,60}(?:图纸|样品).{0,30}(?:加工|生产|制作)'),
 'known_defect_acceptance': ('明知瑕疵接收后的责任安排', r'明知|已知', r'瑕疵|缺陷', r'接收|接受|验收'),
 'defect_repair': ('成果质量不符合约定时修理', r'质量|瑕疵|不合格|有权要求|负责修整|应当修整', r'修理|维修|修整'),
 'defect_remake': ('成果质量不符合约定时重作', r'质量|瑕疵|不合格|有权要求', r'重作|重新制作|重新加工|重做|返工'),
 'reduce_remuneration': ('质量瑕疵时减少报酬', r'质量|瑕疵|不合格|有权要求|按质论价|[酌酬]减酬金', r'减少报酬|减价|减少价款|[酌酬]减(?:酬金|价款)|按质论价'),
 'defect_compensation': ('质量瑕疵造成损失赔偿', r'质量|瑕疵|不合格|由此造成的损失', r'赔偿.{0,10}损失|承担.{0,10}损失|损失.{0,16}(?:赔偿|承担)'),
 'customer_arbitrary_termination_before_completion': ('定作人完成前任意解除', r'定作[人方]', r'完成前|完成之前|随时', r'解除'),
 'arbitrary_termination_loss_scope': ('任意解除或中途废止的赔偿范围', r'中途废止|任意解除|提前解除', r'赔偿|偿付|补偿'),
 'arbitrary_termination_boundary': ('完成后不再任意解除', r'完成后|交付后|完成前', r'任意解除|不得解除|解除权'),
 'termination_notice_settlement': ('解除后的通知及清点结算', r'解除', r'书面通知', r'结算|清点'),
 'contractor_lien_condition': ('未付报酬时依法留置成果', r'未支付|未付款|欠付|拖欠', r'留置'),
 'lien_notice_scope': ('留置通知及相当价值范围', r'留置', r'通知', r'相当价值|范围|不得超额'),
 'lien_exclusion': ('明确排除成果留置', r'不得留置|排除留置|禁止扣留'),
 'improper_lien': ('允许任意或超额留置', r'有权|可以|允许', r'超额留置|任意扣留|扣留全部成果'),
 'drawing_attachment': ('图纸技术规范资料交付', r'图纸|技术规范', r'提供|提交|附件'),
 'sample_attachment': ('样品样板封存确认', r'样品|样板', r'封存|签署确认单'),
 'material_acceptance_attachment': ('材料检验交付验收记录保存', r'材质证明|检测报告|验收单|交接单', r'提交|提供|保存|履行证据'),
 'attachment_priority': ('附件效力及冲突适用顺序', r'附件|图纸|技术规范', r'同等效力', r'优先|顺序|不一致'),
}
PROFILES = {'work_'+key: [atom('work_'+key, label, *patterns)] for key, (label, *patterns) in SPECS.items()}
for key in ('defect_repair', 'defect_remake', 'reduce_remuneration', 'defect_compensation'):
    remedy = SPECS[key][-1]
    PROFILES['work_'+key][0]['negative_patterns'] = [
        rf'(?:不得|无权|不能|无需|不承担|不负责|不予).{{0,12}}(?:{remedy})',
    ]
PROFILES['work_acceptance_period_method'] = [
 atom('goods_inspection_deadline', '到货后检验验收期限', r'(?:收到|到货|到达|交付|验收期限)', r'(?:日|天)内(?:组织|完成|进行)?[^。；]{0,18}(?:验收|检验)'),
 atom('work_acceptance_method', '工作成果验收方法和标准', r'(?:按|依据)[^。；]{0,100}(?:图纸|质量要求|质量标准|技术标准|样品|封样)[^。；]{0,40}(?:验收|检验)|抽检比例.{0,30}%')]

# Independent legal atoms preserve partial coverage; every pattern in an atom
# must hold in the same operative source, not just the neighboring chapter.
MAIN=r'主要(?:加工)?(?:工作|任务)'
TRANSFER=r'转包|分包|(?:转交|交由|交给)[^。；]{0,12}第三[人方][^。；]{0,8}(?:完成|处理)'
CONSENT=r'(?:未经定作[人方][^。；]{0,12}同意[^。；]{0,25}不得|(?:须|应当|应|必须)[^。；]{0,12}(?:取得|经)[^。；]{0,12}同意)'
MAIN_CONSENT=atom('work_main_subcontract_consent','主要工作交第三人完成须经同意',MAIN,TRANSFER,CONSENT)
PROFILES['work_main_subcontract_consent']=[MAIN_CONSENT]
PROFILES['work_personal_completion_main_work']=[atom('work_personal_completion_main_work','主要工作亲自完成或禁止未经同意转交',
 r'(?:亲自完成[^。；]{0,12}'+MAIN+r'|'+MAIN+r'[^。；]{0,25}亲自完成|(?=[^。；]*'+MAIN+r')(?=[^。；]*(?:'+TRANSFER+r'))(?=[^。；]*'+CONSENT+r')[^。；]+)')]
ASSIST=r'(?:未[^。；]{0,30}提供[^。；]{0,25}(?:原材料|技术资料|图纸)|未[^。；]{0,25}(?:协助|辅助工作)|不履行[^。；]{0,12}协助)'
PROFILES['work_assistance_urge_extension']=[
 atom('work_assistance_urge','协助不足时催告履行',r'协助|辅助工作|提供[^。；]{0,12}(?:资料|图纸|原材料)',r'催告|限期[^。；]{0,8}(?:提供|履行)'),
 atom('work_assistance_extension','协助不足时顺延交付',ASSIST,r'顺延|延长',r'期限|工期')]
PROFILES['work_assistance_rescission']=[
 atom('work_assistance_cure','协助不足时催告或补救期限',r'协助|辅助工作|提供[^。；]{0,12}(?:资料|图纸|原材料)',r'催告|限期[^。；]{0,8}(?:提供|履行)'),
 atom('work_assistance_exit','未协助造成停工的解除权',r'停工|未履行协助',r'承揽[人方][^。；]{0,12}有权解除')]
PROFILES['work_quality_standard']=[atom('work_quality_standard','加工产品的质量标准',
 r'(?:产品|成品|成果)[^。；]{0,50}(?:质量标准|技术规范|企业标准|国家标准|合格率|装配和连续运行要求)|(?:尺寸公差|加工尺寸|膜厚)[^。；]{0,25}\d+(?:\.\d+)?\s*(?:mm|μm|um)|(?:表面)[^。；]{0,30}(?:不得存在|不得有)[^。；]{0,30}(?:裂纹|划痕|变形)')]
PROFILES['work_sample_attachment']=[atom('work_sample_attachment','样品样板封存确认',r'(?:样品|样板)[^。；]{0,20}(?:封存|签署确认单)|(?:双方|定作[人方])[^。；]{0,8}确认的?封样')]
PROFILES['work_material_defect_liability']=[
 atom('work_own_material_defect','承揽人自备材料缺陷补救',r'承揽[人方]',r'原材料',r'缺陷|不符合',r'重作|修理|退货|减少价款|赔偿'),
 atom('work_customer_material_defect','定作人来料检验通知失责责任',r'定作[人方][^。；]{0,10}提供的?原材料',r'未[^。；]{0,35}(?:检验|通知)',r'承揽[人方][^。；]{0,25}承担责任')]
PROFILES['work_material_result_custody']=[
 atom('work_material_custody','定作人材料等物品保管责任',r'定作[人方][^。；]{0,15}(?:材料|设备|物品)',r'保管',r'妥善|保管不善[^。；]{0,65}赔偿'),
 atom('work_result_custody','承揽工作成果保管义务',r'承揽[人方][^。；]{0,20}(?:妥善保管|负责保管)[^。；]{0,15}(?:成果|定作物|成品)')]
PROFILES['work_customer_arbitrary_termination_before_completion']=[atom('work_customer_arbitrary_termination_before_completion','定作人提前结束定作的权利',
 r'定作[人方]',r'可以|有权',r'随时|完成前|提前',r'解除',r'^(?!.*(?:不得|无权)[^。；]{0,10}解除)')]
PROFILES['work_customer_arbitrary_termination_before_completion'][0]['negative_patterns']=[r'(?:因|若|如|发生)[^。；]{0,18}(?:违约|不合格|迟延|逾期)']
PROFILES['work_arbitrary_termination_loss_scope']=[atom('work_arbitrary_termination_loss_scope','定作人中途解除的损失承担',
 r'定作[人方]',r'中途[^。；]{0,10}(?:解除|废止)|提前[^。；]{0,20}解除|任意解除',r'承担[^。；]{0,12}损失|赔偿|偿付|补偿')]
FORBIDDEN = {'work_'+x for x in ('nature_confusing_standard_product','illegal_total_subcontract','improper_lien')}


def transaction_facts(clauses):
    """Shared role-bound transfer and mutually exclusive lien scenarios."""
    profiles = {
      'transfer': [atom('transfer', '承揽工作交第三人', r'承揽[人方]', TRANSFER)],
      'auxiliary': [atom('auxiliary', '承揽人辅助工作外交', r'承揽[人方][^。；]{0,30}(?:将|把|可|负责)', r'辅助工作', TRANSFER+r'|外协')],
      'customer_assistance': [atom('customer_assistance', '定作人协助', r'定作[人方][^。；]{0,90}完成[^。；]{0,10}辅助工作')],
      'lien_excluded': [atom('lien_excluded', '排除留置', r'不得留置|排除留置|禁止扣留|无条件交付')],
      'lien_reserved': [atom('lien_reserved', '保留留置', r'有权[^。；]{0,8}留置|可以[^。；]{0,8}留置|保留留置权')],
    }
    return {key: extract(key,clauses,profiles) for key in profiles}


def applicability(node, clauses):
    facts = transaction_facts(clauses)
    def gate(active, condition, reason, evidence):
        return {'status':'APPLICABLE' if active else 'NOT_APPLICABLE',
                'applicable':active,'triggered':active,'condition':condition,
                'reason':reason,'trigger_evidence':evidence,'shared_transaction_facts':facts}
    if node == 'work_main_subcontract_consent':
        evidence=extract(node,clauses,PROFILES)
        if evidence or facts['transfer']:
            return gate(True,'MAIN_WORK_TRANSFER','正文存在承揽工作转交安排，检查主要工作同意要求。',evidence or facts['transfer'])
    if node == 'work_auxiliary_subcontract_liability':
        active=bool(facts['auxiliary'])
        return gate(active,'CONTRACTOR_AUXILIARY_TRANSFER',
          '承揽人将辅助工作交第三人完成，审查其责任。' if active else '未发现承揽人辅助工作交第三人完成；定作人完成辅助工作属于协助义务，不触发辅助分包责任。',facts['auxiliary'])
    if node == 'work_illegal_total_subcontract':
        active=bool(facts['transfer'])
        return gate(active,'CONTRACTOR_WORK_TRANSFER',
          '已识别承揽工作转交第三人，进一步检查是否允许未经同意全部或肢解转包。' if active else '未发现承揽工作交第三人完成的事实。',facts['transfer'])
    if node in {'work_contractor_lien_condition','work_lien_notice_scope','work_lien_exclusion'}:
        excluded=bool(facts['lien_excluded'])
        # Neutral silence keeps the statutory retention option, never recommends
        # adding both retention and its exclusion. Express exclusion wins routing.
        active=excluded if node=='work_lien_exclusion' else not excluded
        return gate(active,'LIEN_EXCLUSION' if node=='work_lien_exclusion' else 'LIEN_RETENTION',
          ('已选择排除留置方案，不再建议增加留置权。' if excluded else '未选择排除留置方案；仅审查留置条件及范围，不建议同时补充排除留置。'),
          facts['lien_excluded'] or facts['lien_reserved'])
    if node != 'work_professional_license':
        return None
    evidence = [c for c in clauses if re.search(r'(?:承揽|加工|工作|作业|制造|安装|检验).{0,35}(?:依法.{0,8}(?:许可|资质|认证)|特种设备|压力容器|医疗器械|危险化学品|强制认证)|(?:特种设备|压力容器|医疗器械).{0,15}(?:制造|维修|安装)', c.text)
                and not re.search(r'无需专项|不涉及特种', c.text)]
    active = bool(evidence)
    return {'status': 'APPLICABLE' if active else 'NOT_APPLICABLE', 'applicable': active, 'triggered': active,
            'condition': 'REGULATED_WORK', 'reason': '工作内容存在专项许可或资质核验触发事实。' if active else '未发现承揽工作涉及专项许可、特种设备或强制认证的触发事实；不据普通加工身份认定资质缺失。',
            'trigger_evidence': [{'clause_id': c.clause_id, 'quote': c.text, 'location': c.location} for c in evidence]}


def evidence_for(node, clauses, requirements=None):
    rows = extract(node, clauses, {node: requirements} if requirements is not None else PROFILES)
    for row in rows:
        row['normalization_reason']='原文同时满足对应法律要素的行为、对象及责任条件；非规则标题匹配。'
        row['matched_requirements']=[r for r in (requirements or PROFILES.get(node,[])) if r['element_id'] in row['supported_elements']]
    if node == 'work_contractor_capacity':
        # Repeating the same party declaration in the signature block does not
        # create a second identity fact. Keep its first canonical occurrence.
        unique = {}
        for row in rows:
            unique.setdefault(re.sub(r'\s+', '', row['quote']), row)
        rows = list(unique.values())
    return rows


def apply(items, clauses):
    store = {}
    def retain(rows):
        for row in rows:
            record = store.setdefault(row['evidence_id'], {**row, 'supported_elements': []})
            record['supported_elements'] = sorted(set(record['supported_elements']) | set(row['supported_elements']))
    for node in ('sale_warranty_period', 'sale_inspection_period', 'sale_subject_quantity_unit', 'common_effective_clause'):
        retain(extract(node, clauses))
    for item in items:
        if item.node_id not in PROFILES or item.coverage_status == '不适用':
            continue
        evidence = evidence_for(item.node_id, clauses)
        required = list(PROFILES[item.node_id])
        if item.node_id == 'work_quality_standard':
            # An expressly agreed warranty is a positive fact even when there
            # is no separate repair obligation. Do not require a warranty in
            # contracts which do not promise one.
            warranty = extract('sale_warranty_period', clauses)
            duration = GOODS_PROFILES['sale_warranty_period'][0]
            warranty = [e for e in warranty if duration['element_id'] in e['supported_elements']]
            if warranty:
                required.append(duration)
                evidence.extend(warranty)
        item.decision_trace['work_required_elements'] = required
        item.evidence_clauses = evidence
        retain(evidence)
        item.evidence_location = '；'.join(dict.fromkeys(e['location'] for e in evidence))
        item.decision_trace['work_atomic_corpus'] = {'searched_clause_ids': [c.clause_id for c in clauses], 'evidence_count':len(evidence)}
        # Persist successful searches too: absence-only logs cannot explain
        # which normalization actually supplied a final positive element.
        from review_v2.engine import _search_final_element
        item.decision_trace['work_element_searches'] = [
            _search_final_element(item, requirement, clauses) for requirement in required]
        if item.node_id in FORBIDDEN:
            item.coverage_status = '风险条款' if evidence else '通过'
            item.issue_type = item.coverage_status
            item.status = '发现不利安排' if evidence else '文本未发现该不利安排'
            item.reasoning_summary = item.risk_point_description = item.status
            continue
        covered = {key for e in evidence for key in e['supported_elements']}
        missing = [a['proposition'] for a in required if a['element_id'] not in covered]
        item.coverage_status = ('部分覆盖' if covered else '缺失') if missing else '通过'
        item.status, item.issue_type = item.coverage_status, ('条款缺陷' if covered else '完全缺失') if missing else '通过'
        item.reasoning_summary = item.risk_point_description = ('原文尚未覆盖：' + '、'.join(missing)) if missing else '原文直接覆盖：' + '、'.join(a['proposition'] for a in required)
    return {'version': 'canonical-source-spans-1', 'facts': list(store.values())}
