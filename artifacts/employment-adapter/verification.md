# 劳动合同：分类到规则适配

## 根因

分类已独立记录用工形式与期限类型，但此前清单主要采用“普通EMP全量 + 专项追加”。没有非全日制替代表，也没有任务期限禁用试用工资覆盖规则，导致子类型正确而法律前提仍按普通劳动合同执行。

## 统一矩阵

| 类型 | 普通规则 | 禁用/替代 | 追加/调整 |
|---|---|---|---|
| 普通劳动合同 | 保留EMP/NC及原有条件适用性 | 无 | 按固定期限计算试用期上限 |
| 劳务派遣 | 保留EMP/NC | 无 | 追加DSP八项，期限类型独立处理 |
| 无固定期限 | 保留EMP/NC | 不要求固定终止日期 | 追加OET期限限制风险，六个月试用上限 |
| 任务期限 | 保留其余EMP/NC | 禁用EMP-03，不补试用工资 | EMP-02检查任务及完成节点，EMP-15禁止试用，既有任务终止风险继续执行 |
| 非全日制 | 保留主体、岗位、安全、条件型培训/竞业、争议、普通违约金及IP | EMP-02/03/05/06/07/10/11/13/15/16由PT专项替代 | PT-01禁止试用；PT-02日周工时；PT-03计酬及15日周期；PT-04工伤等义务；PT-05已提供劳动工资结算；PT-06关系及起点；PT-07劳动者随时通知终止权 |

单位自愿承担较长提前通知义务没有被视为对劳动者的不利约定。非全日制不因缺少普通经济补偿或全部社保代扣条款报缺失；违法离职违约金仍由EMP-14审查。没有删除法定工伤保障或已挣得工资结清义务。

分类仍从DeepSeek抽取且已核验的FactStore读取。法律阈值及周工时乘法由代码计算；不用合同标题、句子或金额关键词决定适配。

适配矩阵返回retained、disabled、replaced、added。生产管线再次比较最终规则ID集合，缺规则或混入规则均以EMPLOYMENT_RULE_ADAPTATION_MISMATCH阻断；成功结果包含EMPLOYMENT_RULE_ADAPTATION=PASS。

## 修改文件

- backend/review_v2/employment_rule_adapter.py：集中适配矩阵、PT定义与事实阈值。
- contract_registry.py：真实清单入口统一调用adapter。
- employment_fact_schema.py、employment_fact_store.py：新增周期、工作天数、通知主体和工伤事实；相应归一化及适用性。
- employment_fact_rules.py：PT规则消费统一事实。
- deepseek_facts.py：允许小时计酬单位。
- employment_fact_pipeline.py、backend/routers/review_v2.py：清单一致性门及调试响应保留。
- backend/tests/test_employment_rule_adapter.py：22项适配、阈值、主体区分、缺规则阻断测试。
- 原分类测试更新非全日制应使用PT-01的预期；三个抽取修复测试的空引擎桩改为满足清单协议的引擎桩，原事实修复断言保留。

## 回归

整组200项通过；最后增加缺清单阻断断言后，专项22项再次全部通过。

fixtures目录中五类各正常/风险一份，共10份不同措辞文本及DOCX；matrix目录保留各自新调用DeepSeek的原始抽取、验证及业务响应。verify_matrix.py逐项断言分类、清单集合、不可加载规则、正常样本无不利条款风险、风险样本精确命中及证据真实绑定：全部通过，10份均REPORT_READY。

原110非全日制文档未修改，经重启后的PID18388本地HTTP /review-v2/file重跑：17项规则，PT-01/02/03/07与EMP-14五项真实风险命中；不再出现普通试用工资缺失、普通经济补偿缺失；工伤与工资结清通过，EMP-IP通过。EMP-08仅保留实际职业病危害因素核验。

最终HTTP 200，release_quality_gate=REPORT_READY，EMPLOYMENT_RULE_ADAPTATION=PASS。见live/report.md、live/response.json和acceptance.json。

法律依据核对：[劳动合同法第68—72条](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_0abfdd261c03417b949df19d869add8d.html)。
