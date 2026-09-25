# 当前复杂劳动合同：社保及知识产权补强验收

输入：`test_data/63 劳动合同.docx`，北京师范大学固定期限劳动合同，normalized input 3426 字；与上一轮输入一致。

normalized SHA256：`ccd5b86398a0bdc42c73070fb201117646bc4f99c191669e33f111d65ccb7441`。

## 最终判断

| 规则 | 状态 | 严重度 | 证据及理由 |
|---|---|---|---|
| EMP-13-01 | RISK | HIGH | 第九条：“乙方应及时提交参加社会保险所需材料，因乙方原因造成社会保险无法及时缴纳的责任由乙方承担。”后半句概括转嫁缴费责任；第十九条（二）：“未依法为劳动者缴纳社会保险费的（因乙方未提交参保所需材料情形除外）”，在劳动者解除救济事由中设置当然例外。单纯提交材料义务不构成风险。 |
| EMP-IP-01 | RISK | HIGH | 第十四条：“乙方在合同期内所取得的教学、科研和管理等成果均属职务成果，在合同期内发表的论文、著作，所获得的奖励、专利、科研项目及经费须署甲方名称，即以甲方为作者单位和相应权利的享有者。”仅以时间范围一概认定职务成果，混合不同法律性质的权利作整体归属；未限定为工作任务、职责或单位物质技术条件相关成果。仅标注作者单位不单独认定为侵害署名权。 |

原有四项保留：EMP-01 PARTIAL、EMP-05 PARTIAL、EMP-08 MISSING、EMP-10 RISK，均 MEDIUM / B_PRACTICAL。EMP-10 逐款分类与上一轮一致，第二十二条保护性条款不作为负面证据。

除补强的 EMP-13 外，原有18项规则覆盖状态、严重度及优先级与上一轮一致。EMP-07 仍 PASS / NONE，与 EMP-13 的同条款风险存在关联，但不新增重复风险。

共20项规则、6项风险：HIGH 2 / MEDIUM 4 / LOW 0；优先处理2、建议处理4。

release_quality_gate = REPORT_READY，failures = []，各一致性门禁通过。

## 验证

- 28项新增正反例覆盖合作义务、有限过错责任、免责、法定救济排除、依法限定职务成果、单独自愿转让、署名、非职务及混合资产归属。
- 446项相关回归：整组445通过，1项检测到运行期间无关供水模块源文件变化；该漂移测试在新进程单独复跑通过。日志：`../bnu_rights_regression.log`、`../bnu_rights_drift_recheck.log`。
- 原文件经真实上传路由复跑，生成 result.json、report.md、report.docx、report.pdf；全部证据及检索诊断见 diagnostics.md。
- 本地8016服务已重启；原浏览器页面保留同一上传文件重新审查，显示20项、2高风险及4中风险。

## 本轮涉及文件

- backend/review_v2/employment_rights.py：新增有方向和作用范围的法律效果识别。
- backend/review_v2/employment_contract_checklist.py：注册 EMP-IP-01。
- backend/review_v2/priority_contract_review.py：接入负面证据及理由；隔离 EMP-07 基本义务与 EMP-13 新增法律效果。
- backend/routers/review_v2.py：新增模块纳入劳动合同运行时源代码漂移检查。
- backend/tests/test_employment_rights.py：新增回归。
- backend/tests/test_employment_standard_contract.py：规则数量更新为20。
- backend/tests/test_employment_complex_prose.py：验证新增社保风险关联确实来自 EMP-13，基本义务仍 PASS。

## 法律边界

参照[最高法劳动争议司法解释（二）](https://gongbao.court.gov.cn/Details/bb72019c45453f84d920bd6375573e.html)、[专利法](https://www.samr.gov.cn/zfjcj/tzgg/art/2023/art_ff4a80ad7d7b46bc908ea03e96f272c3.html)及[著作权法](https://wb.flk.npc.gov.cn/flfg/PDF/3d00c03d87cf4863878081a3e1b54638.pdf)。

实现采用可解释的上下文、否定作用域和法律效果组合判断，不依赖学校、人名、日期或条款序号。对于新的复杂表达仍需要持续扩展正反例；HIGH 是合同审查分级，不代替具体争议中的司法效力认定。
