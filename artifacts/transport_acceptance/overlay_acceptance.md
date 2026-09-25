# 经营合作专项叠加复测

## 结果

同一文件 `84 危险品运输合同.docx` 从文件生产入口完整重跑。主交易仍为 operating_cooperation，主清单 OP 系列及通用完整性检查未回退；不加载单票运输清单。

启用 DANGEROUS_ROAD_TRANSPORT 专项。监管资料核验与合同义务覆盖分开：经营及实际承运主体许可、实际车辆证件、驾驶/押运/装卸人员资格、实际保险、安全管理及事故报告体系共5项待核验。合同要求审核/投保不证明已获证或已投保。

当前18项：通过1、部分覆盖7、风险条款5、待核验5；风险主题12，人工复核5。原10倍赔偿、预期业务额5%责任、三年经营限制、责任转嫁、残句风险全部保留。

## 金额

原文第一年业务基数600万元已提取为6000000；“上交部分由乙方补足”的对象不确定，未把另一条7%上交比例自动移植。公式状态 AMBIGUOUS，单列 COMMON-23-01，要求明确补足对象、基数及比例，并明确业务额统计、对账及争议确认机制。

明确“年度基数1000万元，未完成部分按8%补足”可构造 `max(0,10000000-actual_period_turnover)*0.08`。这不是实际应付款，仍需输入经确认的实际业务额。

倍数、固定金额、按比例违约责任分别解析，金额可计算不等于金额合理；固定金额及普通百分比不自动套用高倍数等级，应结合损失和履约事实。

## 法律依据

10倍及预接洽业务责任使用民法典584、585条及合同编通则司法解释65条。合同称“罚款”的表述按约定违约责任分析，不视作行政处罚权。核对成交状态、预期金额、实际损失、履行利益及司法调整可能性。

- [最高人民法院合同编通则解释](https://gongbao.court.gov.cn/Details/f4722cf61c92a585f04b2ecd334f5b.html)
- [现行道路危险货物运输管理规定](https://xxgk.mot.gov.cn/gz/202602/t20260213_4200295.html)
- [现行道路运输从业人员管理规定](https://xxgk.mot.gov.cn/gz/202602/t20260213_4200291.html)

## 实现

- business_overlays.py：声明式监管业务包，与主清单叠加；包括危险货运和食品经营准入核验。
- requirement_kinds/priority_contract_review：复用 EXTERNAL_VERIFICATION 待核验状态，不把承诺当现实获证。
- settlement_formula.py：补足公式和违约责任表达式解析，保留未确定变量。
- operating_cooperation.py：直接违约金法律依据及责任性质。
- domain_selection.py/lease_semantics.py：遗漏专项、遗漏金额检查、外部未核验却PASS、歧义公式PASS、违约金缺直接依据阻断。
- engine.py：生产清单及最终状态接入。

## 测试

`test_business_overlays.py` 新增7项，覆盖：危险业务+主交易、普通物流不触发、食品加盟专项、车辆要求有证仍待核验、明确差额公式、模糊损失无法唯一计算、违约金直接法律依据及三种表达分类。危险业务测试同时验证错误改为PASS被质量门拦截。

与 `test_operating_carriage_scope.py`、`test_transport_atomic_evidence.py` 联合运行：36 passed。包括旧主交易识别、证据绑定及文件生产入口。

文件生产重跑结果 `overlay_final.json`，报告 `overlay_final.md`；release_quality_gate=REPORT_READY，blocking_reasons为空。该状态只表示报告一致性允许发布，不表示5项外部材料已核验通过。
