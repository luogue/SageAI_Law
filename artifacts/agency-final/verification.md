# 委托合同本阶段回归 PASS

本次使用原77、80 DOCX以及原简版COMMERCIAL文本，通过真实 /review-v2/file 重跑，三个响应均来自 worker PID 11456。原始77/80文件哈希与修复前一致。

## 根因与修改

- 四项原有宽泛匹配混淆了结算/预付、应急继续处理/转委托、一般指示/选任指示责任、权限/附件文件。
- agency_facts.py 的 specs() 为不同法律关系设置独立的主体、行为、对象和责任条件；apply() 沿用 corpus_facts、supports、最终逐要素校验，保留既有 N/A 门禁。
- 有偿委托明确援引依法解除赔偿时识别法定范围；存在排除可得利益或仅赔直接损失的限制，不接受该正向路径。没有改风险等级配置或 renderer。

## 测试

- 95 passed，包含新增27例边界/法定援引/错绑门禁测试。
- 上一轮失败的专项适用性用例本次通过；另以 PYTHONHASHSEED=1/2/3 独立复跑，3/3通过。
- 四类错误核心证据均由发布校验返回 BLOCKED，未关闭或放宽质量门禁。

## 生产结果

|样本|条数|PASS|PARTIAL|MISSING|N/A|门禁|
|---|---:|---:|---:|---:|---:|---|
|77 委托合同.docx|43|29|1|2|11|REPORT_READY|
|80 委托合同.docx|42|25|1|5|11|REPORT_READY|
|商业委托泛化回归.docx|42|21|0|8|13|REPORT_READY|

GF结构样本为43项（含其触发的通用规则），当前样本与简版各42项，未删除规则以统一数量。

## 目标规则证据

A-04-01：缺失；C_OPTIMIZATION
A-08-02：通过；NONE
第五条第8项：
经委托人同意的转委托，不免除受托人依法应承担的选任及指示责任
A-08-03：缺失；C_OPTIMIZATION
A-12-02：通过；NONE
第七条（3）：（3）因解除时间不当或者其他可归责于解除方的原因给对方造成损失的，解除方应按照法律规定承担赔偿责任。
第七条（3）：（3）因解除时间不当或者其他可归责于解除方的原因给对方造成损失的，解除方应按照法律规定承担赔偿责任。
A-14-01：缺失；C_OPTIMIZATION

## 文件

- backend/review_v2/agency_facts.py：关系约束和法定援引。
- backend/tests/test_agency_final_boundaries.py：新增27例。
- backend/tests/test_agency_generalization.py：校准当前样本预期。
- scripts/run_agency_generalization.py：原文件真实入口、基线diff、生产trace。

完整状态和证据diff：42-rule-diff.json / 42-rule-diff.md。
生产逐要素轨迹：production-element-trace.json。
结论仅针对本阶段三份委托样本及相关95项测试，不表示全仓库测试全部通过。本阶段收口，不继续按PASS数量调参。