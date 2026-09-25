"""Relational employment conditions; code evaluates verified assertions, never raw keywords."""
from review_v2.fact_validation import FactExtractionError
CONCEPTS = {
 'worker.liability_limit': '劳动者按实际损失承担责任但设最高责任额的责任限制对象：kind=CAP；amount_text为上限金额原文；basis为计算或限制方式，trigger为责任触发条件。上限不是最低额，不生成预设最低责任；与实际损失事实同时保留。',
 'penalties.exclusions': '明示否定预设违约金的事实对象，kind:EXPLICIT_ABSENCE；scope保存被否定的义务范围原文（字符串），basis保存明确否定表述（字符串）。未约定固定金额仅否定该范围，不能推断不存在比例或其他范围违约金；全文未发现不是明示否定，不生成此对象。与实际损失赔偿worker.damage_liability及其他范围正向penalties.obligations分别保存，不得互相覆盖。',
 'economic_compensation.statutory': '解除终止劳动关系的补偿安排对象，kind必须明确为STATUTORY_PAY（依法支付承诺）、WAIVED（劳动者放弃）、EXCLUDED（不支付或免除）、CALCULATION_RULE（补偿计算方式）；basis保存对应原文表达。不得把无需支付、不予、放弃、免除、终止不产生补偿抽成依法支付；同一合同正负条款分别保存。排除竞业/培训/加班补偿；全文未发现不生成对象，以全文搜索ABSENT或UNCERTAIN保存NOT_FOUND/UNKNOWN状态，禁止默认填支付或免除。',
 'salary.settlement_period': '每一个工资归属区间单独对象，分别提取earning_period_start_day、earning_period_end_day、payment_deadline_day（字符串1至31或MONTH_END）；earning_period_end_month_offset、payment_month_offset为相对于工资期间起始月份的非负整数，当月0、次月1；原文明示当月或完整当月区间时对应offset必须填写0，这是明示关系而非猜测；不得因0而省略。必须保留原文每一段，不从每月两次支付猜区间；X日前按最迟X日记录，不推定提前实际支付；未明确字段省略，不补默认日期。仅列发薪日而无对应工资期间时不创建完整区间，cycle_kind归PAY_DATES_ONLY；固定分段和概括频率并存须均保留。',
 'worker.damage_liability': '每项非预设金额的劳动者责任分别提取对象：kind:ACTUAL_DAMAGE_COMPENSATION按实际发生损失赔偿 / STATUTORY_LIABILITY仅依法处理或依法承担责任；trigger责任发生条件原文（字符串）；basis赔偿范围或法定依据原文（字符串）。按法律规定及实际损失处理优先归ACTUAL_DAMAGE_COMPENSATION。不属于penalties.obligations，不借用同段押金或其他义务金额；固定金额、最低金额、比例或按日预设金额归违约金事实。',
 'job.change_terms': '每项岗位/薪酬变更机制分别一个对象，仅按原文填写：consent:REQUIRED/NOT_REQUIRED，unilateral_position:布尔，position_scope:ANY/BOUNDED，unilateral_pay_cut:布尔，salary_floor_percent:原工资保留百分比数值，refusal_is_misconduct:布尔。未提字段省略，不得默认false；合理协商不得提取为单方；单方调岗不等于降薪，必须分别有证据。',
 'discipline.dismissal_terms': '每项行为及对应违纪解除安排分别一个对象：behavior:MINOR_ATTENDANCE/SUBSTANTIVE_SERIOUS/OTHER，automatic_serious:布尔（机械视为严重违纪），regardless_impact:布尔（不论时间长短/情节后果），immediate_dismissal:布尔，compensation_waived:布尔，policy_basis:布尔，occurrence_threshold:次数数值。不能因合同自己称严重就把轻微考勤行为归为SUBSTANTIVE_SERIOUS；普通严重违纪依法解除不等于不论情节。未明示字段省略；分别引用行为和后果证据，不能跨无关行为拼接。'
}
FIELDS={
 'worker.liability_limit':{'kind':{'CAP'},'amount_text':str,'basis':str,'trigger':str},
 'penalties.exclusions':{'kind':{'EXPLICIT_ABSENCE'},'scope':str,'basis':str},
 'economic_compensation.statutory':{'kind':{'STATUTORY_PAY','WAIVED','EXCLUDED','CALCULATION_RULE'},'basis':str},
 'salary.settlement_period':{'earning_period_start_day':set(map(str,range(1,32)))|{'MONTH_END'},'earning_period_end_day':set(map(str,range(1,32)))|{'MONTH_END'},'payment_deadline_day':set(map(str,range(1,32)))|{'MONTH_END'},'earning_period_end_month_offset':float,'payment_month_offset':float},
 'worker.damage_liability':{'kind':{'ACTUAL_DAMAGE_COMPENSATION','STATUTORY_LIABILITY'},'trigger':str,'basis':str},
 'job.change_terms':{'consent':{'REQUIRED','NOT_REQUIRED'},'unilateral_position':bool,'position_scope':{'ANY','BOUNDED'},'unilateral_pay_cut':bool,'salary_floor_percent':float,'refusal_is_misconduct':bool},
 'discipline.dismissal_terms':{'behavior':{'MINOR_ATTENDANCE','SUBSTANTIVE_SERIOUS','OTHER'},'automatic_serious':bool,'regardless_impact':bool,'immediate_dismissal':bool,'compensation_waived':bool,'policy_basis':bool,'occurrence_threshold':float}
}
def normalize(concept,value):
 fields=FIELDS[concept]
 if not isinstance(value,dict) or not value or set(value)-set(fields):raise FactExtractionError('INVALID_EMPLOYMENT_RELATION')
 for k,v in value.items():
  t=fields[k]
  valid=(isinstance(v,str) and bool(v.strip())) if t is str else (type(v)is bool) if t is bool else (type(v)in (int,float) and __import__('math').isfinite(v) and v>=0 and (k!='salary_floor_percent' or v<=100)) if t is float else isinstance(v,str) and v in t
  if not valid:raise FactExtractionError('INVALID_EMPLOYMENT_RELATION_FIELD:'+k)
 if concept=='penalties.exclusions' and not {'kind','scope','basis'} <= set(value):raise FactExtractionError('MISSING_PENALTY_EXCLUSION_SCOPE')
 if concept=='economic_compensation.statutory' and not {'kind','basis'} <= set(value):raise FactExtractionError('MISSING_COMPENSATION_DISPOSITION')
 if concept=='dispatch.return_terms':
  if 'disposition' not in value:raise FactExtractionError('MISSING_RETURN_DISPOSITION')
  if value['disposition']!='ALLOWED_RETURN_REASON' and 'basis' in value:raise FactExtractionError('RETURN_DISPOSITION_BASIS_CONFLICT')
 return dict(value)
def discipline_risk(v):
 return v.get('immediate_dismissal') is True and v.get('automatic_serious') is True and (v.get('regardless_impact') is True or v.get('behavior')=='MINOR_ATTENDANCE')
def change_risk(v):
 return v.get('consent')=='NOT_REQUIRED' and (v.get('unilateral_pay_cut') is True or (v.get('unilateral_position') is True and (v.get('position_scope')=='ANY' or v.get('refusal_is_misconduct') is True)))

# Actor/recipient relationships, return grounds and payment nature are distinct facts.
CONCEPTS.update({
 'dispatch.onward_assignment': '每个再次安排工作的机制一个对象：agency派遣单位原文称谓、host当前用工单位、recipient新实际用工主体（字符串）；actor:HOST/AGENCY；recipient_relation:SAME_ENTITY/OTHER_ENTITY/UNCERTAIN（子公司等独立企业与内部部门区别，未具名可保留主体类别）；permitted布尔；procedure:HOST_DIRECT_CONTINUATION/AGENCY_NEW_ARRANGEMENT/UNSPECIFIED。HOST_DIRECT_CONTINUATION表示用工单位直接安排并视原派遣延续，不是派遣单位依法另办。仅有地点/岗位变化不等于新用工主体。',
 'dispatch.return_terms': '每项退回理由及其极性单独对象，必须包含disposition:ALLOWED_RETURN_REASON（合同允许作为退回事由）/PROHIBITED_RETURN_REASON（禁止或不当然构成退回事由）/LEGAL_REFERENCE_ONLY（仅引用法律允许情形，未列具体事由）。同一条款允许和禁止的理由分别保存；并列列举的每个独立理由均单独一个对象，不把多个理由拼成一个reason。禁止中的名词不得转成允许。仅概括援引法律、未列具体行为或事件时必须使用LEGAL_REFERENCE_ONLY，绝不能使用ALLOWED_RETURN_REASON或STATUTORY_CONDITIONED代替，即使原文写法律规定可以退回。法律概括引用不得虚构具体法定事由。仅允许型可以使用basis，禁止型与法律引用型省略basis；未知子字段省略。可以、有权等保留允许语义；不得、禁止、不能、不应、不构成、不当然等保留否定的作用范围，不得只抽取其后的理由名词。reason原文理由字符串；reason_type:ORDINARY_PERFORMANCE/SUBJECTIVE_MISMATCH/ORGANIZATION_CHANGE/SERIOUS_MISCONDUCT/STATUTORY_OTHER；basis:STATUTORY_CONDITIONED/REASON_ALONE/UNCERTAIN。STATUTORY_CONDITIONED必须有具体法定事实和程序限制（不能胜任需培训或调岗后仍不能胜任等），仅称依法不掩盖单项理由即可退回的独立授权；REASON_ALONE表示合同直接允许仅凭该理由退回；threshold数值（如明确）。不从缺少法条号推断非法。',
 'worker.security_payment': '每笔向劳动者收取的押金/保证金一个对象：nature:REFUNDABLE_SECURITY/NONREFUNDABLE_FEE；collector:AGENCY/HOST/EMPLOYER；required布尔（true为要求收费，false为明确禁止收费；禁止条款可以形成required=false的保护事实，不是要求收费）；nature等未明示属性省略，不因禁止收费就推断费用是否可退还；deducted_from_wage布尔；amount_text原文金额字符串；refund_condition原文退款条件字符串（如有）。不得把可退保证金抽作penalties.obligations；只有额外规定因违约没收或支付固定赔偿时另行提取违约责任。保证金扣工资不等于salary.withheld_for_handover。不同费用分别抽取，同一收费的支付和退款证据跨句合并。'
})
FIELDS.update({
 'dispatch.onward_assignment':{'agency':str,'host':str,'recipient':str,'actor':{'HOST','AGENCY'},'recipient_relation':{'SAME_ENTITY','OTHER_ENTITY','UNCERTAIN'},'permitted':bool,'procedure':{'HOST_DIRECT_CONTINUATION','AGENCY_NEW_ARRANGEMENT','UNSPECIFIED'}},
 'dispatch.return_terms':{'disposition':{'ALLOWED_RETURN_REASON','PROHIBITED_RETURN_REASON','LEGAL_REFERENCE_ONLY'},'reason':str,'reason_type':{'ORDINARY_PERFORMANCE','SUBJECTIVE_MISMATCH','ORGANIZATION_CHANGE','SERIOUS_MISCONDUCT','STATUTORY_OTHER'},'basis':{'STATUTORY_CONDITIONED','REASON_ALONE','UNCERTAIN'},'threshold':float},
 'worker.security_payment':{'nature':{'REFUNDABLE_SECURITY','NONREFUNDABLE_FEE'},'collector':{'AGENCY','HOST','EMPLOYER'},'required':bool,'deducted_from_wage':bool,'amount_text':str,'refund_condition':str}
})
def onward_risk(v):
 return v.get('permitted') is True and v.get('actor')=='HOST' and v.get('recipient_relation')=='OTHER_ENTITY' and v.get('procedure')=='HOST_DIRECT_CONTINUATION' and all(v.get(k) for k in ('agency','host','recipient'))
def return_risk(v):
 return v.get('disposition')=='ALLOWED_RETURN_REASON' and v.get('basis')=='REASON_ALONE' and v.get('reason_type') in {'ORDINARY_PERFORMANCE','SUBJECTIVE_MISMATCH','ORGANIZATION_CHANGE'}
def charge_risk(v):
 return v.get('required') is True and v.get('collector') in {'AGENCY','HOST','EMPLOYER'}
