"""Versioned domain facts, independent of wording and rule verdicts."""
SCHEMA_VERSION = 'employment-facts-1.2'

# These inputs already have an explicit unresolved/manual-review route. They
# cannot establish coverage or dismiss a risk when quarantined. Other facts
# fail closed; all source-authenticity failures fail closed regardless of role.
NONCRITICAL_FACTS = {'labor_protection.hazard_exists', 'ip.assignment_scope'}

# Values describe contractual assertions, never PASS, risk, legality or coverage.
# All concepts are searched against the full document; an omitted concept is not
# an absence finding. Repeated/conflicting assertions remain separate records.
CONCEPTS = {
    'identity.employer_representative':'用人单位法定代表人或主要负责人姓名（字符串），不是普通联系人',
    'identity.worker_address':'劳动者住址（字符串），不是用人单位地址',
    'identity.employer_name': '用人单位名称（字符串）',
    'identity.employer_address': '用人单位住所（字符串）',
    'identity.worker_name': '劳动者姓名（字符串）',
    'identity.worker_id': '劳动者身份证明号码，保留遮蔽字符（字符串）',
    'contract.type': '劳动合同的期限类型，仅FIXED / INDEFINITE / TASK；不是当前文件或专项协议类别。保密、竞业等专项协议若未载明劳动合同期限类型则不抽取此事实，全文检索记录未发现；不得用OTHER或协议标题推断期限类型',
    'contract.start_date': '劳动关系/合同起始日 YYYY-MM-DD，不取签字日',
    'contract.end_date': '合同到期日 YYYY-MM-DD',
    'contract.duration_months': '合同明确约定的总期限月数（数值），不得自行猜测',
    'contract.task': '任务期限合同的具体任务（字符串）',
    'contract.task_end': '任务完成/验收终止节点（字符串）',
    'probation.arrangement': 'CURRENT 已实际约定 / NONE 明确不设 / DEFERRED 未来另议',
    'probation.start_date': '试用期开始日 YYYY-MM-DD',
    'probation.end_date': '试用期结束日 YYYY-MM-DD',
    'probation.duration_months': '试用期限月数（数值）',
    'probation.salary': '试用工资 money 对象，或明确比例 formula 对象',
    'probation.repeated': '同一劳动者同一单位重复约定试用期，布尔值',
    'job.position': '岗位名称（字符串）',
    'job.duties': '岗位职责（字符串数组）',
    'job.locations': '工作地点（字符串数组）',
    'working_hours.system': 'STANDARD / FLEXIBLE_APPROVED / COMPREHENSIVE_APPROVED / OTHER',
    'working_hours.hours_per_day': '每日约定小时数（数值）',
    'working_hours.hours_per_week': '每周约定小时数（数值）',
    'working_hours.rest': '休息休假安排（字符串）',
    'working_hours.rest_days_per_week': '明示每周休息天数（数值），不从其他工时推算',
    'working_hours.rest_waived': '明确不得休息或无休息日（布尔值）',
    'working_hours.overtime': '待遇模式 STATUTORY / REST_DAY_TIME_OFF / ALL_INCLUDED / WAIVED / HOLIDAY_TIME_OFF_ONLY / ALLOWANCE_WITH_STATUTORY_SHORTFALL；保留每个冲突模式',
    'salary.regular': '转正/通常工资标准 money或formula对象；基本、岗位、绩效分别提取，可多条，不用试用工资替代',
    'salary.payment_date': '工资发放日（字符串）',
    'salary.payment_method': 'BANK / CASH / OTHER',
    'salary.withheld_for_handover': '合同允许以未交接等理由扣留已挣得工资，布尔值；押金保证金扣款属于worker.security_payment，不因保证金退还附交接条件就等同扣留工资',
    'social_insurance.employer_enrolls': '单位承担参保办理义务，布尔值（不含员工自行办理）',
    'social_insurance.statutory_duties': '合同一般性承诺依法处理社会保险、保留单位依法应承担义务（布尔值）；不据此推断已经明确某一险种或实际完成缴费',
    'social_insurance.employer_pays': '单位承担法定单位缴费部分，布尔值；依法办理社保可显式表达该整体义务，不因未列险种否认',
    'social_insurance.employee_withheld': '个人应缴部分代扣代缴，布尔值',
    'social_insurance.cash_replacement': '用补贴替代单位法定参保缴费而由员工自行处理；布尔值，额外福利不算替代',
    'social_insurance.waived': '放弃/免除单位参保缴费义务；布尔值，员工申请也保留',
    'social_insurance.employer_share_shifted': '单位应缴部分转由员工承担，布尔值',
    'social_insurance.employer_underpays': '合同允许单位少缴法定社会保险费用（布尔值）',
    'social_insurance.employer_liability_excluded': '材料欠缺等情形下单位当然免责/全部责任转员工；不含员工仅依过错承担直接损失（布尔值）',
    'social_insurance.employee_remedy_excluded': '以未提交材料等理由排除员工因单位未依法参保而依法解除、补偿或追责的权利（布尔值）',
    'labor_protection.measures': '劳动保护/职业健康制度、条件或防护措施（字符串）',
    'labor_protection.training': '已约定安全教育培训（布尔值）',
    'labor_protection.special_training_required': '原文明确岗位涉及高危作业、特种作业或需要专门安全培训的作业条件（布尔值）；不从一般办公室岗位或条件性如有危险推断存在',
    'labor_protection.training_excluded': '合同明确排除必要安全培训或允许未经必要培训作业（布尔值）；没有单独约定培训不等于排除',
    'labor_protection.hazard_exists': '岗位是否实际存在职业危害（布尔值），仅如有危害不算实际存在',
    'labor_protection.hazard_protection': '危害告知/防护/健康检查安排（字符串）',
    'training.arrangement': '专项培训服务期 CURRENT / NONE / DEFERRED；普通安全、消防、入职、岗位培训不属于此事实；NONE引文仅可为明确不设服务期的原文，全文未约定使用absence_audits而非普通培训引文',
    'training.technical': '专项技术培训内容（字符串）；区别普通安全、消防、入职和日常岗位培训',
    'training.service_penalty': '因专项培训服务期产生的违约金安排（字符串）；区别其他违约金',
    'training.cost': '专项培训实际费用及凭证安排（字符串）',
    'training.duration_months': '服务期月数（数值）',
    'training.penalty_prorated': '按未履行服务期比例分摊且不超实际培训费用（布尔值）',
    'termination.grounds': '实际约定的辞职/解除/终止事由、协商或依法办理机制（字符串数组）',
    'termination.notice': '提前通知/解除通知方式或日期（字符串）',
    'termination.notice_days': '普通辞职提前通知天数（数值）',
    'termination.approval_required': '未经雇主批准不得辞职（布尔值）',
    'termination.employee_right_waived': '合同明示劳动者不得依法解除/辞职或放弃该权利（布尔值）',
    'termination.employer_unrestricted': '雇主可以任意无理由解除（布尔值）',
    'termination.handover': '工作交接和离职手续（字符串）',
    'economic_compensation.statutory': '解除终止的法定经济补偿/赔偿依法支付承诺或计算依据（字符串）；排除竞业、培训、加班补偿',
    'economic_compensation.settlement_deadline': '解除终止工资/经济补偿结算期限或明确结算事件（字符串）',
    'economic_compensation.waived': '合同明确免除付款义务或员工明确放弃解除终止补偿（布尔值）；没有约定、未另设补偿条款不等于免除法定义务',
    'economic_compensation.reduced': '明示低于法定标准的补偿折减（布尔值）',
    'economic_compensation.statutory_percentage': '明确按法定补偿标准的百分之几支付（数值，如50；不作是否合法判断）',
    'economic_compensation.payment_delay_months': '经济补偿明确推迟至离职后若干个月支付的月数（数值）',
    'dispute.arbitration': '允许依法申请劳动仲裁（布尔值）',
 'penalties.obligations': '每项预设违约责任单独对象：scope按实际触发义务分类为TRAINING_SERVICE_PERIOD专项培训服务期、NON_COMPETE竞业、PROJECT_TASK_PERFORMANCE工作项目任务未完成或逾期、ATTENDANCE迟到旷工等考勤、RESIGNATION_NOTICE未依法提前离职通知、CONFIDENTIALITY保密、ORDINARY_DISCIPLINE其他纪律、PROPERTY_DAMAGE固定财产损坏赔偿、OTHER其他。不得把工作任务履行泛称普通违纪。trigger保存实际触发条件；imposed必须为true，amount_text保留该义务句中的固定金额、最低金额、比例或公式。按实际损失或依法处理归worker.damage_liability，不是预设违约金；可退保证金归worker.security_payment，不跨无关义务借金额。明确未约定、不设或无需承担违约金归penalties.exclusions，不能生成本概念（包括imposed=false）；全文未发现只记录全文检索结果。',
    'non_compete.arrangement': '离职竞业 EXISTS实际约定离职后竞争从业限制 / EXPLICIT_NONE原文明示双方不设离职竞业或离职后无需承担竞业义务 / DEFERRED是否设定竞业义务本身未来另议/另签。已约束竞争从业但仅范围、期限、补偿未来确定仍为EXISTS；子参数缺失不否定父义务。保密不得限制就业、可以选择其他工作、保密不等于竞业均不能证明EXPLICIT_NONE；应另查全文是否有独立竞业条款。全文未发现时不生成任何本concept事实，只记录已搜索；NOT_FOUND/UNKNOWN是事实库检索状态，不是value。EXPLICIT_NONE必须引用明确否定竞业安排本身的原文，不得推断',
    'non_compete.personnel': '兼容旧版的合同受限人员范围（字符串）；仅说明谁承担竞业义务，不代表人员依法适格；新抽取使用person_scope',
    'non_compete.person_scope': '合同明确由谁承担竞业义务（字符串），可以是协议中特定当事人、定义清楚的人员类别。对乙方直接施加离职从业约束即可支持，无需先证明其高级管理/技术身份或实际接触秘密；跨条款主体指代可组合。未定义的相关人员等泛指不能当作明确范围，不生成已明确事实。',
    'non_compete.person_eligibility': '合同明示的受限人员适格性依据或资格类别（字符串），如高级管理人员、高级技术人员或明确负有保密义务的身份；只记录原文事实，不作法律适格结论。明确乙方受限不证明依法适格；可能接触不等于实际接触；实际接触仍独立归actual_access。未提供依据不生成事实，不影响person_scope。',
    'non_compete.secret_access': '适用人员须接触秘密的资格前提或范围声明（字符串）；不作为实际接触已经发生的证据。可能性归access_capability，已发生事实归actual_access，不在本字段混合保存。',
    'non_compete.access_capability': '岗位具备接触商业秘密的可能性或能力（布尔值）；可能、能够、有机会接触只证明能力，不代表实际接触发生。须有明确原文，未提及不生成默认值。',
    'non_compete.actual_access': '员工已经实际接触、知悉、掌握商业秘密或实际负责具体秘密事项的已发生事实（布尔值）；仅可能、能够、有机会、资格前提不能支持true，也不能推断false。false仅用于明确未实际接触的原文，全文未明确则不生成事实并保留搜索缺失状态。',
    'non_compete.businesses': '已约定可识别的竞争业务活动/行业范围（字符串数组），可跨句组合；仅概括不得到竞争企业工作且具体范围待定，只证明父义务，不生成已确定业务范围子事实',
    'non_compete.territories': '被限制地域（字符串数组）',
    'non_compete.duration_months': '离职后的竞业限制月数（数值），不要混入在职或保密期限',
    'non_compete.compensation': '离职竞业按月补偿 money或formula对象；另议/无金额不是确定标准',
    'non_compete.compensation_floor': '竞业补偿每月保底金额 money对象；仅提取明确最低金额，不用保底金额代替按工资比例的完整计算公式',
    'non_compete.salary_base': '竞业补偿公式采用的工资基数 money对象，必须带base:REGULAR_SALARY/LOCAL_MINIMUM_WAGE/PREVIOUS_AVERAGE_SALARY；必须明确实际数额及与公式基数相同的期间/口径，只有“离职前12个月平均工资”而无金额时不抽取，不能用补偿金额代替工资基数',
    'non_compete.compensation_deferred': '竞业补偿标准另议（布尔值）',
    'non_compete.compensation_waived': '离职竞业无需补偿或无偿履行（布尔值）',
    'non_compete.all_staff': '不区分秘密接触即所有员工适用竞业（布尔值）',
    'ip.assignment_scope': 'DUTY_OR_RESOURCES / ALL_DURING_EMPLOYMENT / NON_DUTY；只提取所讨论成果的形成范围，不要求确定最终权利归属，按法律及另行协议处理不影响识别职务/利用单位资源的范围',
    'ip.allocations': '每个成果归属关系单独对象：{scope:DUTY_OR_RESOURCES/ALL_DURING_EMPLOYMENT/NON_DUTY/PRE_EXISTING/UNDIFFERENTIATED_RESULTS,beneficiary:EMPLOYER/EMPLOYEE/HOST/JOINT/UNSPECIFIED,mode:AUTOMATIC/SEPARATE_AGREEMENT/STATUTORY}；PRE_EXISTING为入职前既有成果，HOST为派遣用工单位；范围、归属对象、处分方式必须来自同一安排，可跨条款引用，不能把员工自己的成果写成归单位。每个明确归属单独记录，其他成果归属待另行协议不能抹掉已明确的既有个人权利。全文未约定成果归属时不生成该事实，也不标记不确定；约定依法确定归属可用UNSPECIFIED与STATUTORY，不因未列具体权利人标记不确定；仅在真实条款歧义、冲突或引用材料缺失时标记不确定',
    'ip.personal_rights_waived': '排除员工署名等人身权（布尔值）',
}

# Disjunction of conjunctions. Every binding is to domain concepts, not text.
ELEMENTS = {
    'employment_ip_ownership_1': [('ip.allocations',)],
    'employment_identity_1': [('identity.employer_address',)],
    'employment_identity_name': [('identity.employer_name',)],
    'employment_identity_2': [('identity.worker_name', 'identity.worker_id')],
    'employment_term_1': [('contract.type',)],
    'employment_term_start': [('contract.start_date',)],
    'employment_term_end': [('contract.end_date',)],
    'employment_term_task': [('contract.task',)],
    'employment_term_task_end': [('contract.task_end',)],
    'employment_probation_1': [('probation.duration_months',), ('probation.start_date', 'probation.end_date')],
    'employment_probation_2': [('probation.salary',)],
    'employment_work_1': [('job.position',), ('job.duties',)],
    'employment_work_2': [('job.locations',)],
    'employment_hours_1': [('working_hours.system',)],
    'employment_hours_2': [('working_hours.rest',)],
    'employment_hours_3': [('working_hours.overtime',)],
    'employment_wage_1': [('salary.regular',)],
    'employment_wage_2': [('salary.payment_date',)],
    'employment_wage_3': [('salary.payment_method',)],
    'employment_insurance_1': [('social_insurance.employer_enrolls', 'social_insurance.employer_pays')],
    'employment_insurance_2': [('social_insurance.employee_withheld',)],
    'employment_safety_1': [('labor_protection.measures',)],
    'employment_safety_2': [('labor_protection.hazard_protection',)],
    'employment_safety_training': [('labor_protection.training',)],
    'employment_training_service_1': [('training.cost',)],
    'employment_training_service_2': [('training.duration_months',)],
    'employment_training_service_3': [('training.penalty_prorated',)],
    'employment_exit_1': [('termination.grounds',)],
    'employment_exit_2': [('termination.notice',), ('termination.notice_days',)],
    'employment_compensation_1': [('economic_compensation.statutory',)],
    'employment_compensation_2': [('economic_compensation.settlement_deadline',)],
    'employment_dispute_1': [('dispute.arbitration',)],
    'employment_noncompete_scope_1': [('non_compete.person_scope',), ('non_compete.personnel',)],
    'employment_noncompete_scope_2': [('non_compete.businesses',)],
    'employment_noncompete_scope_3': [('non_compete.territories',)],
    'employment_noncompete_term_1': [('non_compete.duration_months',)],
    'employment_noncompete_term_2': [('non_compete.compensation',)],
}

ENUMS = {
    'contract.type': {'FIXED','INDEFINITE','TASK'},
    **{k: {'CURRENT','NONE','DEFERRED'} for k in ('probation.arrangement','training.arrangement')},
    'non_compete.arrangement': {'EXISTS','EXPLICIT_NONE','DEFERRED'},
    'working_hours.system': {'STANDARD','FLEXIBLE_APPROVED','COMPREHENSIVE_APPROVED','OTHER'},
    'working_hours.overtime': {'STATUTORY','REST_DAY_TIME_OFF','ALL_INCLUDED','WAIVED','HOLIDAY_TIME_OFF_ONLY','ALLOWANCE_WITH_STATUTORY_SHORTFALL'},
    'salary.payment_method': {'BANK','CASH','OTHER'},
    'ip.assignment_scope': {'DUTY_OR_RESOURCES','ALL_DURING_EMPLOYMENT','NON_DUTY'},
}

# Additional facts share the same source binding and verification protocol.
from review_v2.employment_dispatch import CONCEPTS as DISPATCH_CONCEPTS, ELEMENTS as DISPATCH_ELEMENTS, ENUMS as DISPATCH_ENUMS
CONCEPTS.update(DISPATCH_CONCEPTS)
ELEMENTS.update(DISPATCH_ELEMENTS)
ENUMS.update(DISPATCH_ENUMS)

from review_v2.employment_indefinite import CONCEPTS as TERM_CONCEPTS, ENUMS as TERM_ENUMS
CONCEPTS.update(TERM_CONCEPTS)
ENUMS.update(TERM_ENUMS)

from review_v2.employment_rule_adapter import CONCEPTS as ADAPTER_CONCEPTS, ENUMS as ADAPTER_ENUMS, ELEMENTS as ADAPTER_ELEMENTS
CONCEPTS.update(ADAPTER_CONCEPTS)
ENUMS.update(ADAPTER_ENUMS)
ELEMENTS.update(ADAPTER_ELEMENTS)

# Explicit semantic search scope for document-level negative arrangement facts.
ABSENCE_SCOPES = {'training.arrangement': ('training.technical', 'training.cost', 'training.duration_months', 'training.service_penalty')}
ABSENCE_SCOPES['non_compete.arrangement'] = tuple(k for k in CONCEPTS if k.startswith('non_compete.') and k != 'non_compete.arrangement')
# Search these contextual facts, but their existence alone does not establish
# a non-compete obligation (they also occur in ordinary confidentiality duties).
ABSENCE_CONTEXT_FACTS = {'non_compete.arrangement': {
    'non_compete.secret_access', 'non_compete.access_capability', 'non_compete.actual_access'}}

from review_v2.employment_conditions import CONCEPTS as CONDITION_CONCEPTS
CONCEPTS.update(CONDITION_CONCEPTS)

ELEMENTS.update({'employment_identity_3':[('identity.employer_representative',)],'employment_identity_4':[('identity.worker_address',)],
 'employment_remuneration_1':[('salary.regular',)],'employment_remuneration_2':[('salary.payment_date',)],'employment_remuneration_3':[('salary.payment_method',)]})

# Confidentiality agreements share the source-verified fact pipeline.
from review_v2.penalty_liability_semantics import DESCRIPTION as LIABILITY_DESCRIPTION
CONCEPTS['penalties.obligations'] += LIABILITY_DESCRIPTION
CONCEPTS['worker.damage_liability'] += '实际损失责任与预设最低责任可并存，必须分别保存；最低额及超过最低额补差部分不能合并抹去最低责任。最高责任额另归worker.liability_limit。'

CONCEPTS.update({
 'nda.employment_relationship':'全文能确认双方为用人单位与员工、因任职承担义务的劳动关系（布尔值）；跨条款组合，不要求固定称谓；企业间合作不等于劳动关系',
 'nda.party_one':'协议第一方真实主体名称（字符串）',
 'nda.party_two':'协议第二方真实主体名称（字符串）',
 'nda.information_flow':'保密信息所有/提供方到因任职或合作接触并承担义务方的流向（字符串，例如甲方→乙方或双向）；可从全文关联确定，不要求披露方/接受方称谓，绑定所有支持方向的原文',
 'nda.protected_information':'合同定义的受保护保密信息范围（字符串）',
 'nda.exception_public':'合法公开信息不受保密义务约束（布尔值）；公开是信息状态，不证明接受方已知悉，不能替代exception_prior',
 'nda.exception_prior':'接受方在从信息来源取得前已经合法知悉或持有的信息除外（布尔值）；证明责任不改变此例外含义。必须支持接受方个人在先知悉/持有，不能从信息已经公开推导',
 'nda.exception_independent':'接受方独立开发取得的信息除外（布尔值）',
 'nda.exception_third_party':'从不负保密义务第三方合法取得的信息除外（布尔值）',
 'nda.exception_mandatory':'因法律或有权机关强制披露的信息除外（布尔值）',
 'nda.use_restriction':'合同明确限制保密信息使用/披露及接触权限（字符串）',
 'nda.duration':'保密义务期限或终止事件（字符串）',
 'nda.return':'保密资料返还或销毁安排（字符串）',
 'nda.remedies':'违反保密义务后的损害赔偿责任、约定违约责任或请求停止侵害等法律救济（字符串）；仅发现事件后报告/补救/减损不是赔偿责任，另归incident_response。绑定真实追责条款',
 'nda.incident_response':'发现信息安全事件后的通知报告、协助处置、减少损失义务（字符串）；不得据此推导损害赔偿责任',
})
ELEMENTS.update({
 'employment_secret_scope_1':[('nda.protected_information',)],
 'confidentiality_parties_1':[('nda.party_one',)],
 'confidentiality_parties_2':[('nda.party_two',)],
 'confidentiality_information_flow':[('nda.information_flow',)],
 'employment_secret_duty_1':[('nda.use_restriction',)],
 'employment_secret_duty_2':[('nda.duration',)],
 'employment_secret_duty_3':[('nda.return',)],
 'confidentiality_remedies_1':[('nda.remedies',)],
 **{'nda_exception_'+k:[('nda.exception_'+k,)] for k in ('public','prior','independent','third_party','mandatory')},
})

from review_v2.termination_facts import CONCEPTS as EXIT_CONCEPTS, ELEMENTS as EXIT_ELEMENTS
CONCEPTS.update(EXIT_CONCEPTS)
ELEMENTS.update(EXIT_ELEMENTS)
