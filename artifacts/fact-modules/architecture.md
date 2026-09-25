# 事实抽取架构核查与修复

## 核查结果
engine.review_contract_v2 将 labor、non_compete、confidentiality 交给 employment_fact_pipeline.run；其他合同类型仍走既有审查入口，本轮没有宣称迁移全部合同。
此前三类协议复用同一 DeepSeek transport 和 employment_fact_schema.CONCEPTS 全量目录。contract_type 到事实抽取完成后才用于规则适配。按35个字段分批并非按合同类型选 schema；上一轮依赖约束只限制输出，仍发送不适用字段定义。Verifier 最终集合检查也固定读取全目录。

## 本轮实际链路
合同原文及 contract_type → 请求独立 AGREEMENT 上下文 → DeepSeek 全文识别父关系 → fact_modules.select 根据合同类型、当前用工形式、当前竞业安排选字段 → 只发送激活模块的字段定义与完整原文 → FactStore 内规范化、绑定原文 → DeepSeek 独立验证当前字段集合 → verified_store 重建已验证事实与覆盖状态 → 确定性规则 → 报告及门禁。

公共主体、责任等事实复用。员工保密协议加载 NDA 字段及公共字段；独立竞业加载竞业及公共字段；劳动合同加载普通劳动事实，派遣/非全日制字段随实际关系加载。竞业参数依赖 EXISTS，保密接触能力等背景与当前竞业义务分开。若核验纠正父关系而改变模块集合，重新规划抽取，超出既有一次修复预算仍阻断。

## 职责及状态
- Schema：全项目字段注册目录及类型；不等于每次模型输入清单。
- Module selector：确定当前 active_concepts；从合同类型和结构化父关系选择，不匹配样本句子。
- Extractor：仅产生有原文依据、符合 schema 的实际值。未发现只做搜索声明，不生成正向占位事实。
- Normalizer：执行现有类型与数值格式检查；不把未约定转换成数值、null或默认值。
- FactStore：保存 normalized_value、证据、位置、置信度、明示/推断类型；隔离每次请求。
- Verifier：逐事实检查及当前范围全文遗漏审计；不能添加不在范围的事实。
- Coverage：已验证事实投影；ABSENT 是已搜索未发现，NOT_APPLICABLE 是未加载模块，UNCERTAIN 是仍不能确认。
- 明示否定：EXPLICIT_NONE 或 penalties.exclusions 等具有真实引文的否定事实；DEFERRED 是未来安排，不是当前义务，也不是完全没有任何表述。
- Rules：只消费已验证事实和模块状态，继续执行现有法律阈值、极性、金额、期限与风险判断。

## 验收
当前原合同未修改。CR-20260912-152521-D118F4：32个 active_concepts 与 verifier searched_concepts 完全一致，122个不适用字段；dispatch 字段不加载；竞业期限、范围、补偿、工资基数不加载。保留 arrangement 与3个秘密接触背景概念。首次抽取与验证通过，诊断为空，REPORT_READY。
回归：91项基础/保密/竞业/模块测试通过；另84项派遣测试通过（扩展运行中含重复模块测试，按独立用例合计175项）。
