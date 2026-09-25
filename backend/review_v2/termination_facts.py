"""Termination-agreement facts and typed consumers; no source-text matching."""
CONCEPTS = {
 'exit_settlement.wage_deadline': '解除终止后工资、绩效奖金等劳动报酬的结算期限（字符串）；跨句结合前文工资清单与后文上述款项付款日，不能只提取经济补偿期限',
 'exit_settlement.compensation_deadline': '解除终止经济补偿的付款期限或事件（字符串）；与工资期限分别保存，竞业补偿不属于此字段',
 'exit_settlement.remuneration': '解除终止时应付工资、奖金等项目或核对安排（字符串）；保留结算清单，不用竞业补偿替代',
 'exit_settlement.annual_leave': '未休年休假工资结算或核对安排（字符串）；明确不支付仍保存事实，极性另记录',
 'exit_settlement.annual_leave_waived': '存在未休法定年假却明确不支付相应工资（布尔值）',
 'exit_settlement.compensation_amount': '解除终止经济补偿或赔偿金额及依据（字符串）；区别竞业补偿',
 'exit_settlement.service_basis': '用于补偿计算的工作年限或起止期间（字符串）；单独入职日期不等于已经明确计算年限',
 'exit_settlement.salary_basis': '用于补偿计算的工资基数及其明确金额（字符串）；不以月工资或竞业补偿代替',
 'exit_settlement.certificate': '单位出具解除/终止劳动关系证明的义务和时点（字符串），保留附加条件；条件不当不等于没有承诺',
 'exit_settlement.certificate_requires_handover': '出具解除/终止证明是否以完成工作交接、财物返还或交接确认作为前提（布尔值）；同段分别规定交接和出具证明不等于附条件。明确不得因未交接延迟出具为false，只有真实前置关系才为true；不从未约定推断false',
 'exit_settlement.social_transfer': '社会保险关系转移或停缴办理安排（字符串）',
 'exit_settlement.personnel_transfer': '档案、人事关系转移安排（字符串）',
 'exit_settlement.fund_transfer': '住房公积金转移、封存或停缴安排（字符串）',
 'exit_settlement.last_contribution': '约定的最后社保及公积金缴费月份/衔接安排（字符串）；不证明已经实际缴费',
 'exit_settlement.secret_scope': '离职后继续承担保密义务所涉及的秘密范围（字符串）',
 'exit_settlement.secret_continues': '明确约定离职后保密义务继续存在（布尔值）；只证明义务存续，不证明具体期限已明确',
 'exit_settlement.secret_reference': '引用另份保密协议确定离职后义务的引用关系（字符串）；引用本身不证明被引协议内容已经提供，不得推断期限',
 'exit_settlement.secret_duration': '离职后保密义务明确的时长、终止日、可识别终止事件或明示永久/无期限（字符串）。仅继续有效、继续履行只证明secret_continues，不证明期限；引用另份协议且该协议正文或附件未提供，不生成期限事实。若附件已提供，须绑定附件中真正约定期限的原文及引用关系，不用引用句代替期限证据',
 'exit_settlement.compensation_after_handover_days': '工作交接办结后额外等待支付经济补偿的天数（数值，工作日也保存其明示数值且证据保留工作日）；办结时支付为0，不从未约定生成0',
 'exit_settlement.compensation_withholding': '单位可因未完成交接而暂缓经济补偿（布尔值）；与已赚工资区分。此事实本身不等于违法，须结合办结后延期等条件审查',
 'exit_settlement.unilateral_deduction': '单位可单方直接从工资/补偿扣除争议损失或费用，无核实及法定扣减程序（布尔值）；依法核实结算不是此授权',
 'exit_settlement.remedy_waiver': '概括禁止劳动者再申请仲裁、起诉、投诉、举报或依法撤销等救济（布尔值）；仅确认已核实款项结清不等于放弃救济，否定禁止保留false',
}

ELEMENTS = {
 'termination_wage_deadline': [('exit_settlement.wage_deadline',)],
 'termination_compensation_deadline': [('exit_settlement.compensation_deadline',)],
 'employment_handover_1': [('exit_settlement.certificate',)],
 'employment_handover_2': [('exit_settlement.social_transfer','exit_settlement.personnel_transfer')],
 'employment_handover_3': [('termination.handover',)],
 'termination_settlement_1': [('exit_settlement.remuneration',)],
 'termination_settlement_2': [('exit_settlement.annual_leave',)],
 'termination_compensation_calculation_1': [('exit_settlement.compensation_amount',)],
 'termination_compensation_calculation_2': [('exit_settlement.service_basis',)],
 'termination_compensation_calculation_3': [('exit_settlement.salary_basis',)],
 'termination_insurance_stoppage_1': [('exit_settlement.social_transfer',)],
 'termination_insurance_stoppage_2': [('exit_settlement.fund_transfer',)],
 'termination_insurance_stoppage_3': [('exit_settlement.last_contribution',)],
 'termination_secrecy_1': [('exit_settlement.secret_scope',)],
 'termination_secrecy_2': [('exit_settlement.secret_continues',)],
 'termination_secrecy_3': [('exit_settlement.secret_duration',)],
}

ADVERSE_INPUTS = {
 'termination_payment_withholding': ('salary.withheld_for_handover','exit_settlement.compensation_after_handover_days','exit_settlement.compensation_withholding'),
 'termination_direct_deduction': ('exit_settlement.unilateral_deduction',),
 'termination_remedy_waiver': ('exit_settlement.remedy_waiver',),
 'termination_settlement': ('exit_settlement.annual_leave_waived',),
 'termination_certificate_condition': ('exit_settlement.certificate_requires_handover',),
}

def adverse(store, node):
 selected = []
 reasons = []
 def pick(concept, predicate, reason):
  rows = [f for f in store.get(concept,positive=False) if predicate(f['normalized_value'])]
  if rows: selected.extend(rows); reasons.append(reason)
 if node == 'termination_payment_withholding':
  pick('salary.withheld_for_handover',lambda v:v is True,'已提供劳动的到期工资不能因交接尚未完成而当然扣留。')
  pick('exit_settlement.compensation_after_handover_days',lambda v:v>0,
       '经济补偿约定在办结交接后继续延期支付，应核对第五十条办结交接时支付要求及具体结算性质；交接条件本身不当然违法。')
  if selected: selected.extend(store.get('exit_settlement.compensation_withholding'))
 if node == 'termination_direct_deduction':
  pick('exit_settlement.unilateral_deduction',lambda v:v is True,'单方扣除争议费用或损失，缺少责任、金额核实及法定扣减程序。')
 if node == 'termination_remedy_waiver':
  pick('exit_settlement.remedy_waiver',lambda v:v is True,'概括排除仲裁、诉讼、投诉举报等救济；已核实款项结清不能当然排除全部法定救济。')
 if node == 'termination_settlement':
  pick('exit_settlement.annual_leave_waived',lambda v:v is True,'仍有未休法定年假，却一概排除相应工资结算，需核对休假及依法折算安排。')
 if node == 'termination_certificate_condition':
  pick('exit_settlement.certificate_requires_handover',lambda v:v is True,
       '将解除或终止证明的出具附加于交接完成之后，可能不当延迟法定证明义务；应将出具证明与工作交接分别办理。')
 return [{**e,'reason':'；'.join(dict.fromkeys(reasons))} for e in store.evidence(
     list({f['fact_id']:f for f in selected}.values()), node+'_adverse')]
