# 竞业限制本轮收口验收

实际输入：`test_data/60 竞业限制协议.docx`；使用完整上传入口重新执行，生成 Markdown、Word、PDF。输入及证据诊断均在本目录。

## 修改文件

- `backend/review_v2/noncompete_reasonableness.py`（新增）：全国/全球范围的经营地域、秘密接触及理由核验；真实竞业持续期与补偿比例组合审查；提前解除与额外补偿法律提示；区分单位解除和劳动者救济。
- `backend/review_v2/noncompete_semantics.py`：综合核验接入既有 NC-03，提示未解决时不得无条件 PASS；保留 NC-01/02 的事实存在判断及既有直接风险。
- `backend/review_v2/employment_contract_checklist.py`：移除“甲方＋任意文字＋公司”宽泛名称模式，要求主体定义语法；同一共享用工主体要素作用于劳动、竞业等清单。
- `backend/review_v2/report_presentation.py`：展示组合核验的实际触发原文，明确这些证据证明触发事实，不证明范围已经合理。
- `backend/routers/review_v2.py`：新模块纳入运行时代码版本检查。
- `backend/tests/test_noncompete_closeout.py`（新增）：18项参数展开用例，含全国/全球、支持事实、不同期限和比例组合、额外补偿已约定、劳动者保护性解除、代称不证明实名、明确名称、跨规则矛盾和完整文件。

## 结果

|规则|状态|
|---|---|
|EMP-01-01|PASS|
|NC-01-01|PARTIAL|
|NC-02-01|PASS|
|NC-03-01|待核验|
|EMP-12-01|PASS|
|EMP-14-01|PASS|

NC-03 含三个独立的证据核验主题：

1. 全国范围：缺少相应经营地域、岗位及实际秘密接触支持，核验必要性和合理性。
2. 24个月＋30%：触发期限与补偿匹配性审查。阈值来自合规指引，属于审查基准，不自动认定违法或无效。
3. 单位提前通知解除：提示正常履行期间补偿与提前解除额外补偿的区别。没有写明额外补偿不等于劳动者法定请求权消失，也不被判成竞业期限缺失。劳动者因欠付补偿享有的解除权已排除在单位解除证据之外。

EMP-01 仍通过，名称证据不再含1.2、1.3竞争条款。NC-02仍能显示期限与补偿两项真实证据。当前一致性门禁无失败。

release_quality_gate = REPORT_READY；failures=[]。

## 测试

- 竞业专题32项通过（本轮新增18项＋既有14项）。
- 劳动合同、复杂合同、报告表达及一致性170项通过。
- 合计202项通过。日志：`artifacts/noncompete_closeout_tests.log`、`artifacts/noncompete_closeout_regression.log`。

## 法律依据与判断边界

超过一年时50%的比例是合规审查基准，不能直接当作合同无效红线；参见[企业实施竞业限制合规指引](https://app.www.gov.cn/govdata/gov/202509/13/536638/article.html)。额外三个月补偿提示依据[劳动争议司法解释（一）第39条](https://www.court.gov.cn/fabu/xiangqing/282121.html)。范围与秘密接触相适应的审查依据[劳动争议司法解释（二）第13条](https://gongbao.court.gov.cn/Details/bb72019c45453f84d920bd6375573e.html)。

本轮指定能力及回归范围通过；岗位、秘密内容、实际经营地域真实性仍需人工材料核验。仅有绝对金额而无工资基数或当地标准时，不武断推定补偿充足或违法。
