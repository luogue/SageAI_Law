# 第66份任务期限劳动合同验收

输入为同一份 test_data/66 完成一定工作任务为期限的劳动合同.docx；未替换合同正文。

|规则|修复前|修复后|理由|
|---|---|---|---|
|EMP-01-01|部分覆盖|通过|合同原文覆盖全部专项要素。|
|EMP-02-01|部分覆盖|通过|合同原文覆盖全部专项要素。|
|EMP-03-01|缺失|不适用|未建立实际试用期安排；明确不设试用期或任务期限合同不要求补充试用期要素。|
|EMP-15-01|通过|通过|全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。|
|EMP-06-01|部分覆盖|通过|合同原文覆盖全部专项要素。|
|EMP-09-01|不适用|不适用|未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。|
|EMP-11-01|缺失|通过|合同原文覆盖本项核心法定义务；可选完善项未单独作为实际风险：解除终止后工资及补偿结算期限。|
|NC-01-01|不适用|不适用|未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。|
|NC-02-01|不适用|不适用|未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。|
|NC-03-01|不适用|不适用|未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。|

## 全文、查询和证据

- actual_rule_chunks.json：逐规则实际收到的完整 chunks。
- actual_applicability_inputs.json：实际适用性 corpus 和结论。
- actual_element_inputs.json：逐规则 corpus、element_queries、candidate_evidence、judge_evidence、final_evidence、search_audits 和负向审计条件。
- requested_source_checks.json：指定七段原句在 EMP-01、06、11 实际 corpus 中逐项验证，全为 true；仅忽略排版空格。
- diagnostics.md：全部规则最终状态、证据和 SEARCH_AUDIT。

根因：正文没有丢失。原签章角色模式未接受括号，工资模式未接受排版空格及税前限定，经济补偿模式漏掉依法支付的倒装语序；编号选项期限漏分支，否定试用期仍被主题词触发。

修复：角色限定的签章要素匹配、带排版空格及税前/税后限定的工资事实、依法补偿语序；任务期限独立审查生效日、具体任务、可判断终止节点；显式无试用期先行过滤，另有实际试用期时保留审查及任务期限的禁止性检查。

复用并测试 SEARCH_AUDIT_ELEMENT_CONFLICT 门禁；没有关闭门禁、用预计项目日期代替固定终止日期、或把类型标题当成具体任务。

## 四份实际合同

|合同|实际风险数|质量门|
|---|---|---|
|61 正常固定期限|0|REPORT_READY|
|64 正常无固定期限|0|REPORT_READY|
|66 当前任务期限|0|REPORT_READY|
|63 复杂劳动合同|6|REPORT_READY|

复杂合同全部规则状态、严重度和优先级与上一轮一致，解除权扩张、社保转嫁及知识产权风险仍然命中。

## 测试及文件

252项回归分批验证通过：首轮237通过，1个任务内容边界反例修复后通过；测试期间共享后端源码变化影响运行时及接口测试，后续13项专项/运行时测试及12项上传接口测试复跑通过（包含1项新增实际第66份合同测试）。日志：../task_term_regression.log、../task_term_recheck.log、../task_api_recheck.log。

修改：employment_facts.py、employment_contract_checklist.py、priority_contract_review.py；新增 test_employment_task_term.py，更新 test_employment_term_branches.py；run_employment_file_acceptance.py 补充实际查询/证据诊断记录。

法律依据：[劳动合同法第15、19条](https://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/fl/202011/t20201102_394622_wap.html)。