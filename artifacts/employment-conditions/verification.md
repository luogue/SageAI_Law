# 普通劳动合同劳动条件变更与违纪解除风险

根因：原事实库欠缺岗位变更权限、是否降薪及“具体行为→机械严重违纪→直接解除”的关系事实。原EMP覆盖规则主要确认内容存在，不能凭这些存在性事实判断授权和解除条件合理性。

修改文件：
- backend/review_v2/employment_conditions.py：结构化岗位变更与违纪处理对象及严格字段验证；纯事实谓词判定，不搜索合同关键词，不按特定比例或次数设阈值。
- backend/review_v2/employment_fact_schema.py：注册两类关系事实供DeepSeek全文抽取和独立验证。
- backend/review_v2/employment_fact_store.py：关系对象归一化类型校验，后续仍执行原文证据绑定。
- backend/review_v2/employment_fact_rules.py：EMP-04识别变更权限过宽；EMP-10识别机械严重违纪解除；EMP-16要求该行为同时有明确免补偿事实，不能跨无关行为拼接。
- backend/review_v2/employment_risk_semantics.py：风险事实主题标注，复用现有聚合及标题/证据一致性校验。
- backend/tests/test_employment_conditions.py：协商调岗、受限不降薪、不同降薪比例、偶发轻微行为、严重违纪制度依据、机械预设严重违纪，以及最终报告证据、聚合和子类型隔离。

法律依据核对：[劳动合同法第35条、第39条](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2023/art_0abfdd261c03417b949df19d869add8d.html)。单方调岗并非一概违法；受限合理调整不因“单方”一词自动报风险，明确不经协商任意调岗、降薪或惩罚拒绝不合理变更才进入本规则风险。

实测：未修改112劳动合同，POST /review-v2/file通过DeepSeek全文抽取→FactStore→Verifier→确定性规则→报告；HTTP200 / REPORT_READY。岗位变更事实保留原工资比例及拒绝调岗后果；迟到条件原文独立绑定。EMP-04、EMP-10、EMP-16为风险条款；同一违纪事实聚合，3个命中对应2个主题。EMP-IP、EMP-14、EMP-15通过，没有PT/DSP/OET污染。EMP-08既有部分覆盖保留，未为清零风险修改规则。

163项相关测试通过，见tests.txt。当前完整报告见live/report.md，原始JSON见live/response.json。前端及数据库未改动。
