# 当前复杂劳动合同：三项风险门槛复验

最终相关回归：418 passed（包含本轮新增24项门槛/负例测试）。日志：../labor_threshold_final_regression.log。

已重启实际后端并在原页面点击重审，仍为63号文件。实际服务日志确认 runtime=CURRENT、release_quality_gate=REPORT_READY、failures=[]；页面显示4项中等风险/建议处理，社保和经济补偿均PASS。

输入仍为 63 劳动合同.docx，normalized 与上轮逐字相同。
normalized SHA256：7999fe6e14419da8390ccfaf5964522cbbe4d30729c1a77723e99478bdc05818
release_quality_gate：REPORT_READY

本轮生产代码修改：employment_contract_checklist.py、priority_contract_review.py、engine.py。没有修改全文检索、附件绑定、日期计算、培训/竞业适用性及解除条款分类器。

## 指定六项规则

|规则|覆盖|严重度|处理优先级|
|---|---|---|---|
|EMP-01-01|PARTIAL|MEDIUM|B_PRACTICAL|
|EMP-05-01|PARTIAL|MEDIUM|B_PRACTICAL|
|EMP-07-01|PASS|NONE|NONE|
|EMP-08-01|MISSING|MEDIUM|B_PRACTICAL|
|EMP-10-01|RISK|MEDIUM|B_PRACTICAL|
|EMP-11-01|PASS|NONE|NONE|

## EMP-01-01

未找到明确约定：用人单位住所。

|要素|状态|原文证据|
|---|---|---|
|用人单位住所|MISSING|无直接证据；未补造原文|
|劳动者姓名与身份证明|COVERED|第二条 乙方李明远，性别男，户籍类型：非农业 ☑、农业 □。<br>居民身份证号码：110101199505168832。<br>家庭住址：北京市海淀区学院路88号院3号楼1202室。<br>邮政编码：100083。<br>在京居住地址：北京市海淀区西三旗街道清河小营东路26号。<br>邮政编码：100085。<br>户口所在地：北京市海淀区中关村街道。|
|用人单位名称|COVERED|工号：BNU-TEST-2026-0908-017<br>劳 动 合 同 书<br>（固定期限）<br>甲方：北京师范大学<br>乙方：李明远<br>签订日期：2026年9月8日<br>根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》等法律、法规以及北京师范大学有关管理规定，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。|

SEARCH_AUDIT：

```json
[
  {
    "element_id": "employment_identity_1",
    "result": "NOT_FOUND",
    "search_targets": [
      "用人单位住所"
    ]
  },
  {
    "element_id": "employment_identity_2",
    "result": "FOUND",
    "search_targets": [
      "劳动者姓名与身份证明"
    ]
  },
  {
    "element_id": "employment_identity_name",
    "result": "FOUND",
    "search_targets": [
      "用人单位名称"
    ]
  }
]
```

## EMP-05-01

未找到明确约定：工时制度及工作时间、加班报酬或依法调休。

|要素|状态|原文证据|
|---|---|---|
|工时制度及工作时间|MISSING|无直接证据；未补造原文|
|休息休假安排|COVERED|第七条 甲方对乙方实行的休假制度有国家法定节假日、公休日及带薪年假，带薪年假根据《职工带薪年休假条例》执行，一般应利用寒暑假期间休假。|
|加班报酬或依法调休|MISSING|无直接证据；未补造原文|

SEARCH_AUDIT：

```json
[
  {
    "element_id": "employment_hours_1",
    "result": "NOT_FOUND",
    "search_targets": [
      "工时制度及工作时间"
    ]
  },
  {
    "element_id": "employment_hours_2",
    "result": "FOUND",
    "search_targets": [
      "休息休假安排"
    ]
  },
  {
    "element_id": "employment_hours_3",
    "result": "NOT_FOUND",
    "search_targets": [
      "加班报酬或依法调休"
    ]
  }
]
```

## EMP-07-01

合同原文覆盖本项核心法定义务；可选完善项未单独作为实际风险：个人应缴部分及代扣代缴。

|要素|状态|原文证据|
|---|---|---|
|用人单位依法办理参保并缴费|COVERED|第九条 甲乙双方按国家和北京市的规定参加社会保险。|
|个人应缴部分及代扣代缴|MISSING|无直接证据；未补造原文|

SEARCH_AUDIT：

```json
[
  {
    "element_id": "employment_insurance_1",
    "result": "FOUND",
    "search_targets": [
      "用人单位依法办理参保并缴费"
    ]
  },
  {
    "element_id": "employment_insurance_2",
    "result": "NOT_FOUND",
    "search_targets": [
      "个人应缴部分及代扣代缴"
    ]
  }
]
```

## EMP-08-01

未找到明确约定：劳动防护和安全培训。岗位职业危害情况待核实，未将条件不明的专项义务判为合同缺失。

|要素|状态|原文证据|
|---|---|---|
|劳动防护和安全培训|MISSING|无直接证据；未补造原文|
|核实岗位是否存在职业病危害因素，再确定告知和职业健康保护义务。|CONDITION_UNRESOLVED|无直接证据；未补造原文|

SEARCH_AUDIT：

```json
[
  {
    "element_id": "employment_safety_1",
    "result": "NOT_FOUND",
    "search_targets": [
      "劳动防护和安全培训"
    ]
  }
]
```

## EMP-10-01

发现与本项法定保护相冲突的直接不利约定。该事项被单独设为解除事由，未限定为有合法制度及事实支持的严重违纪，不等同于法定即时解除事由。；核对原岗位及另行安排工作均不能从事；仅前者不足以成立该解除权。；单独扩张解除条件；通知或代通知金不能替代不能胜任或客观情况变化的法定前提。

|要素|状态|原文证据|
|---|---|---|
|解除终止条件和程序存在直接不利约定|ADVERSE|（二）不服从用人单位管理或拒绝参加考核的；|

SEARCH_AUDIT：

```json
[]
```

## EMP-11-01

合同原文覆盖全部专项要素。

|要素|状态|原文证据|
|---|---|---|
|经济补偿依法处理、计算依据或正常结算安排|COVERED|如需支付经济补偿，则甲方在乙方工作交接结束后支付。|
|解除终止后工资及补偿结算期限|COVERED|如需支付经济补偿，则甲方在乙方工作交接结束后支付。|

SEARCH_AUDIT：

```json
[
  {
    "element_id": "employment_compensation_1",
    "result": "FOUND",
    "search_targets": [
      "经济补偿依法处理、计算依据或正常结算安排"
    ]
  },
  {
    "element_id": "employment_compensation_2",
    "result": "FOUND",
    "search_targets": [
      "解除终止后工资及补偿结算期限"
    ]
  }
]
```

## 回归不变性

以下16项的覆盖、严重度、处理优先级及要素原文均与上轮一致：
EMP-01-01, EMP-02-01, EMP-03-01, EMP-15-01, EMP-04-01, EMP-05-01, EMP-06-01, EMP-09-01, EMP-10-01, EMP-12-01, EMP-13-01, EMP-16-01, EMP-14-01, NC-01-01, NC-02-01, NC-03-01

EMP-10 的逐款分类与上轮完全一致，第二十二条不进入不利证据。

## 聚合统计

```json
{
  "total": 4,
  "must_change": 0,
  "should_change": 4,
  "optional_improvement": 0,
  "keep_current": 0,
  "do_not_add": 0,
  "manual_review": 0,
  "actionable": 4,
  "protected_no_change": 0
}
```

完整证据与诊断见同目录 diagnostics.md、result.json、actual_rule_chunks.json。
