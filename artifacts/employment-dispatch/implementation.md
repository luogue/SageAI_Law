# 劳动合同子类型与劳务派遣专项

## 根因与链路

原劳动规则入口仅保留 LABOR，统一事实结构没有派遣关系、岗位性质、待岗待遇及重新派遣条件，因而普通 EMP 清单无法消费这些专项事实。现在由 DeepSeek 全文抽取、独立核验和原文绑定后的 FactStore 决定子类型；用工形式与合同期限类型分别保存，劳务派遣不会被“固定期限”覆盖。

派遣子类型在普通 EMP/NC 清单基础上追加 DSP-01-01 至 DSP-08-01。规则仅读取已验证事实，代码判断枚举、极性和数值；不搜索样本标题、姓名、金额或固定句子。长期辅助性或替代性岗位不会仅因“长期”被报风险；相反条款独立保留，正向同工同酬条款不会屏蔽另条较低待遇。

## 修改文件

- backend/review_v2/employment_dispatch.py：子类型、专项事实定义、八项规则及确定性判断。
- backend/review_v2/employment_fact_schema.py、employment_fact_store.py：统一 schema、归一化和适用性。
- backend/review_v2/employment_fact_rules.py、employment_fact_pipeline.py：已验证事实消费及决策调试。
- backend/review_v2/contract_registry.py、engine.py、report_context.py：专项叠加及分类贯穿报告。
- backend/routers/review_v2.py：业务响应保留结构化子类型。
- backend/review_v2/deepseek_facts.py：全文分批概念范围一致，区分明确的归属机制和最终具体权利人；仍仅 DeepSeek。
- backend/tests/test_employment_dispatch.py 与 fixtures/dispatch_*.txt：泛化及最终报告回归。

独立专项依次覆盖主体/岗位/期限、岗位性质、同工同酬、无工作报酬、禁止收费、退回重新派遣解除、派遣协议告知、双方职责。原有质量门保持不变，原始测试文档未修改。

## 验证资料

自动化套件：144 passed，7 warnings。覆盖五类子类型、普通合同不加载派遣规则、正负极性、多个证据、长期辅助/替代岗位、最终序列化，以及 EMP-IP/14/15 原有判断。

独立 DeepSeek 完整业务流程结果保存在 protective/result.json、adverse-variants/result.json 和 ordinary-106-verified/result.json。普通合同106的20项状态与此前成功报告逐项比较。

当前浏览器业务接口 /review-v2/file 的最终响应、原文哈希和逐项验收见 acceptance.json；最终用户报告见 report.md。verify_acceptance.py 直接断言生产响应，不用中间函数结果代替最终报告。早期失败运行保留供诊断，不能视为最终验收结果。
