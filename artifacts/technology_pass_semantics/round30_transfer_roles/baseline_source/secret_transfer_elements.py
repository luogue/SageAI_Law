"""Secret-transfer requirements in the shared canonical atomic fact pipeline.

Each predicate describes an arrangement, not an incidental mention of its
object. Sources retain list introductions, conditions and exact parser spans.
Rights warranties and documentary proof are deliberately separate facts.
"""
import re

from review_v2.obligation_detail_elements import _element, _DURATION
from review_v2.technology_service_elements import sources

ASSET = r'(?:技术秘密|专有技术|非公开技术信息|核心技术|合同技术)'
ACTOR = r'(?:甲方|乙方|让与方|转让方|受让方|出让方|买方|卖方)'
FAMILIES = {
    'secret_transfer_scope': (
        ('transferred_subject', '转让的技术秘密标的', r'(?:转让的?|核心标的是)[^。；]{0,20}' + ASSET + r'[^。；]{0,15}(?:包括|范围|内容)|(?:技术秘密|专有技术)(?:内容|范围)[：:]'),
        ('transferee_use_right', '受让方自行使用技术的权利', ACTOR+r'[^。；]{0,8}(?:有权|可以|可)[^。；]{0,8}(?:自行)?使用'),
        ('transferee_improvement_right', '受让方改进技术的权利', ACTOR+r'[^。；]{0,8}(?:有权|可以|可)[^。；]{0,18}改进'),
        ('production_commercialization_right', '受让方生产和商业化权利', ACTOR+r'[^。；]{0,8}(?:有权|可以|可)[^。；]{0,65}(?:生产|制造)[^。；]{0,12}销售'),
        ('transferor_retransfer_restriction', '让与方再次转让限制', ACTOR+r'不得[^。；]{0,45}(?:转让|让与)[^。；]{0,8}第三方'),
        ('transferor_post_transfer_use_restriction', '让与方转让后使用限制', ACTOR+r'不得[^。；]{0,30}(?:继续|直接)使用[^。；]{0,20}(?:核心技术|技术秘密)'),
        ('retained_general_knowhow', '保留通用经验和公开知识的边界', ACTOR+r'(?:仍)?(?:可以|可|有权)[^。；]{0,65}(?:通用工程经验|通用知识|公开知识|通用工具)'),
        ('historical_customer_continued_use_boundary', '历史客户继续使用的边界', r'(?:历史客户|既有客户)[^。；]{0,25}(?:可继续|可以继续|应停止|不得继续)[^。；]{0,25}使用'),
    ),
    'secret_transfer_warranty': (
        ('transferor_authority', '让与方处分和转让权限保证', r'有权[^。；]{0,10}(?:处分|转让|让与)[^。；]{0,12}'+ASSET),
        ('lawful_source', '技术秘密合法来源保证', ASSET+r'[^。；]{0,12}(?:来源合法|合法取得)|(?:并非|不是|未通过)[^。；]{0,30}(?:盗窃|欺诈|违反保密义务)[^。；]{0,18}取得'),
        ('no_conflicting_transfer', '不存在冲突的既有整体转让', r'(?:未曾|未|没有|不曾)[^。；]{0,20}(?:同一技术秘密|合同技术|该技术)[^。；]{0,10}(?:整体)?转让[^。；]{0,8}第三方'),
        ('no_conflicting_exclusive_license', '不存在冲突的既有独占许可', r'(?:未曾|未|没有|不曾)[^。；]{0,40}(?:授予|设立)[^。；]{0,45}(?:独占|排他)'),
        ('historical_use_disclosure', '历史客户取得权利的披露', r'(?:客户|第三方)[^。；]{0,12}(?:仅|只)[^。；]{0,8}(?:取得|获得)[^。；]{0,15}使用权'),
        ('documentary_chain_proof', '完整权利链证明附件', r'(?:附有|已提供|提交了|附件包括)[^。；]{0,35}(?:权利链证明|技术来源证明|权属证明)'),
    ),
    'secret_transfer_loss': (
        ('secrecy_loss_trigger', '技术秘密公开或丧失秘密性的触发条件', ASSET+r'[^。；]{0,30}(?:公开|丧失秘密性)|(?:第三方独立研发|合法公开出版)[^。；]{0,70}公共领域'),
        ('transferor_fault_secrecy_loss_liability', '让与方导致秘密性丧失的责任', r'(?:违反[^。；]{0,8}保密义务|泄密)[^。；]{0,30}公开[^。；]{0,40}(?:赔偿|损失)'),
        ('lawful_public_domain_trigger', '合法进入公共领域的触发条件', r'(?:第三方独立研发|合法公开出版|合法公开)[^。；]{0,70}(?:公共领域|公开)'),
        ('post_secrecy_loss_adjustment', '秘密性丧失后的价款或权利调整', r'(?:秘密价值|秘密性|公共领域)[^。；]{0,45}(?:协商|调整|结算|解除)'),
        ('remaining_price_after_total_loss', '全部秘密性丧失后的剩余转让价款', r'(?:全部|所有)[^。；]{0,35}(?:公开|丧失秘密性)[^。；]{0,100}(?:应继续支付|仍应支付|无需支付|不再支付|停止支付|免除)[^。；]{0,30}(?:价款|转让费)|(?:剩余转让价款|未付转让价款)[^。；]{0,15}(?:免除|不再支付|继续支付)'),
        ('secrecy_loss_notice', '知悉技术秘密公开后的通知义务', r'知悉[^。；]{0,30}(?:公开|丧失秘密性)[^。；]{0,20}(?:应|须)[^。；]{0,8}通知'),
        ('notice_deadline', '秘密性变化的具体通知期限', r'知悉[^。；]{0,30}(?:公开|丧失秘密性)[^。；]{0,15}'+_DURATION+r'内[^。；]{0,10}通知'),
    ),
}
FAMILIES['secret_transfer_subject'] = FAMILIES['secret_transfer_scope'][:1]


def elements(family, clauses):
    from review_v2.technology_service_analysis import build_technology_fact_registry
    from review_v2.proposition_scope import predicate_is_operative
    parties = build_technology_fact_registry('\n'.join(c.text for c in clauses))['third_party_claim']['response_party_patterns']
    result = []
    for key, label, predicate in FAMILIES[family]:
        actor_key = ('recipient' if key in {'transferee_use_right', 'transferee_improvement_right', 'production_commercialization_right'} else 'provider')
        predicate = predicate.replace(ACTOR, parties[actor_key])
        proof = sources(clauses, predicate, inherit_lists=True)
        if family == 'secret_transfer_warranty':
            # A warranty states an existing status, unlike a hypothetical
            # infringement/authority condition in a remedy clause.
            proof = [s for s in proof if not s.get('condition')]
        if key in {'transferee_use_right', 'transferee_improvement_right', 'production_commercialization_right'}:
            proof = [s for s in proof if any(predicate_is_operative(s['quote'], m.start(), m.end())
                                            for m in re.finditer(predicate, s['quote']))]
        # A timing reference to the transferred asset is not its definition.
        if key == 'transferred_subject':
            proof = [s for s in proof if re.search(r'包括|内容|范围', s['quote'])]
        atom = _element(key, label, proof, source_fact_key='technology.'+family+'.'+key)
        if key == 'post_secrecy_loss_adjustment' and proof and all(
                re.search(r'协商', s['quote']) and not re.search(r'(?:免除|退还|减免|扣减|有权解除)', s['quote']) for s in proof):
            gap = '协商不成时的价款及权利调整办法'
            atom.update(status='PARTIALLY_COVERED', residual_gap=gap, search_targets=[gap],
                        proposition='已约定秘密性变化后协商，'+gap+'尚未明确。',
                        component_coverage=[dict(element_id='negotiation', status='COVERED', required_fact='协商机制', supporting_evidence=proof),
                                            dict(element_id='adjustment_outcome', status='MISSING', required_fact=gap, supporting_evidence=[])])
        result.append(atom)
    return result
