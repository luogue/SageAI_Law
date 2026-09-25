# 正常标准劳动合同：根因修复与复审

输入为 `test_data/61 劳动合同.docx`，未经修改或补写。上传文件 SHA256 为 `7f879d57ebb1596e36dcc09a565a187cf361ee2e6dba36314337d08fdd54aa03`；规范化输入 SHA256 为 `9f45a87202eb6316e2c14bf6431c766f5bc96aec5a23802ac8a2626f5ef714a0`。

通过 FastAPI TestClient 的真实 multipart 路由及响应模型复审；认证只在独立测试应用覆盖，没有改动运行中服务的认证。启用 `use_llm=true`，专项规则仍走项目已有确定性核验路径。此操作没有替换浏览器内已显示的旧报告。

## 复现与根因

修复前相同文件报告有 5 项高风险，质量门却为 REPORT_READY。此次没有关闭或降低门禁。

| 环节 | 根因与修复 |
|---|---|
| 提取、分块 | 正文完整，分类、条款解析、规则、SEARCH_AUDIT 输入哈希一致；不是缺页或只读标题。保留既有分块架构。 |
| 身份字段 | 原匹配不接受括号后“名称/姓名”、注册登记地及身份字段间的其他信息。补充角色绑定的字段句式，仍禁止借用劳动者地址证明单位住所。 |
| 工资、岗位、社保、劳动保护 | 原匹配限制词序、距离和同义表述。补充“试用期期间的工资标准”、金额空格、银行转账在工资之前、安排在某岗位、甲乙双方依法参保、乙方个人承担及代扣代缴等句式。原文引用保持不变。 |
| 正式工资 | 按句子排除试用期金额；试用期满后的工资可以证明正式工资。试用工资不得替代正式工资。 |
| 试用期 | 原日期解析未识别“固定期限。自…”，回退时又把未选中的任务期限选项当成生效事实。现在识别分段固定期限，排除“不适用”的任务期限分支，按日历与含首尾日期计算。当前合同 2026-09-10 至 2029-09-09，满三年；试用期至 2026-12-09 为三个月，未超过六个月上限。重复试用仍须直接证据。 |
| 条件适用 | 区分另行签订的预备性协议与已约定的服务期、竞业义务；其他条款确立实际义务时仍触发。岗位“如存在危害”不是存在危害的事实；一般保护持续审查。 |
| 经济补偿 | “依法支付”的明确义务可以覆盖法定依据，不再要求每份普通劳动合同写死金额。结算期限仍独立审查。 |
| 后果文案 | 通用关键词“防护”误选运输包装后果。劳动领域先按自身规则域生成后果，并记录来源，其他领域分支不变。 |
| 门禁 | 复用已有同要素正向证据/NOT_FOUND 冲突校验，增加负向风险无直接事实、未触发条件元素升级风险的失败检查，并以突变测试验证门禁会拒绝。 |

法律核对：[《劳动合同法》第19、22—24、46—50条](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_0abfdd261c03417b949df19d869add8d.html)。

## 最终结果

19 项中，13 项 PASS，4 项 N/A，2 项 PARTIAL。没有 RISK 或 MISSING 规则。

保留的 NOT FOUND 只有：

- EMP-10-01 / employment_exit_2：解除通知方式或明确解除日期。已有依法通知义务，但具体方式/日期未明确。
- EMP-11-01 / employment_compensation_2：解除终止后工资及补偿结算期限。已有依法补偿义务，不再判金额依据完全缺失。

EMP-08-01 的一般保护通过；岗位是否实际存在职业病危害仍为条件待核实，未生成缺失风险。

release_quality_gate 为 `REPORT_READY`（项目的可发布状态），failures 为空。统计：重大 0、中等 2、低 0；优先处理 0、建议处理 2；总体建议修改后签署。质量门通过不意味着强行把合理缺口改成 PASS。

## 文件

- [19 项状态、每个 element/evidence、全部检索诊断](./diagnostics.md)
- [规范化原文](./normalized_input.txt)
- [全部 NOT FOUND 原始数据](./not_found.json)
- [完整响应](./result.json)
- [证据来源、统计与导出核验](./verification.json)
- [报告 Markdown](./report.md)、[Word](./report.docx)、[PDF](./report.pdf)

## 本轮修改范围

- `backend/review_v2/priority_contract_types.py`：无标题保密协议需披露方/接收方角色证据；不能仅凭三个附带保密主题词抢占技术咨询主类型。

- `backend/review_v2/employment_contract_checklist.py`：要素匹配、正式/试用工资隔离、补偿法定依据、通知缺口名称。
- `backend/review_v2/employment_facts.py`：分段期限解析、可选协议及职业危害条件事实。
- `backend/review_v2/priority_contract_review.py`：条件适用、试用期任务期限回退。
- `backend/review_v2/engine.py`：劳动领域后果文案隔离。
- `backend/review_v2/lease_semantics.py`：现有共享一致性门禁中追加限定专项规则的校验。
- `backend/tests/test_employment_standard_contract.py`：20 项新增回归，含独立姓名/金额/日期句式、违法变体、门禁突变及当前原文件。
- `backend/tests/test_employment_round2_semantics.py`：依法补偿与交接结算均覆盖时预期为通过。
- `scripts/run_employment_file_acceptance.py`：可复用的 multipart 复审、规范化输入和全部规则证据诊断输出。

其他并行任务留下的工作区修改未回滚。本轮没有新增合同类型、删除规则或修改其他合同专项判断。

## 测试

劳动、新增类型及相关回归，另含两个技术咨询生产接口回归：167 passed（`artifacts/labor_standard_focused_verified.txt`）。包括原有正向、负向、条件要素、12 类正常/缺失/风险、上传与导出测试。

广泛回归与历史对照的最终结果单独保存在相邻测试日志及 `regression_summary.json` 中；不把有失败的全量运行标记为通过。

广泛回归原始结果：729 passed / 122 failed，共 851 项。19 项失败在最终代码的新进程中复跑通过（18 项源码变化导致保护拦截，1 项无标题技术咨询被保密类型抢占，已修复）。其余 103 项在禁用新增适配器的独立对照进程中仍失败，未修改其他合同规则或测试预期来消除这些失败。详见 `regression_summary.json`。
