# 劳动合同逐项证据诊断

输入文件：64 无固定期限劳动合同.docx
输入 SHA256：67c747d6f531e1d270aad216eb715b85e0516704bb4f0928f49023150219e39e
normalized SHA256：34828400e04977596c1dae0bcc1a25b0f45980131b3e432cafd572382a8fc8a6

| rule_id | 最终状态 | 理由 |
|---|---|---|
| EMP-01-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-02-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-03-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-15-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| EMP-04-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-05-01 | PARTIAL | 未找到明确约定：加班报酬或依法调休。 |
| EMP-06-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-07-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-08-01 | PASS | 合同原文覆盖全部专项要素。岗位职业危害情况待核实，未将条件不明的专项义务判为合同缺失。 |
| EMP-09-01 | N/A | 未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。 |
| EMP-10-01 | PASS | 合同原文覆盖本项核心法定义务；可选完善项未单独作为实际风险：解除通知方式或明确解除日期。 |
| EMP-11-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-12-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-13-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| EMP-16-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| EMP-14-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| NC-01-01 | N/A | 未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。 |
| NC-02-01 | N/A | 未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。 |
| NC-03-01 | N/A | 未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。 |
| EMP-IP-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |

## 全部 SEARCH_AUDIT NOT FOUND

```json
[
  {
    "rule_id": "EMP-05-01",
    "element_id": "employment_hours_3",
    "review_id": "EMP-05-01",
    "search_targets": [
      "加班报酬或依法调休"
    ],
    "query_patterns": [
      "加班.{0,40}(?:依法支付|加班工资|补休|调休)",
      "依法安排[^。；\\n]{0,20}(?:补休|调休)或支付加班工资",
      "(?:支付|发放)加班工资"
    ],
    "query_semantic_target": "加班报酬或依法调休",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021",
      "C0022",
      "C0023",
      "C0024",
      "C0025",
      "C0026",
      "C0027",
      "C0028",
      "C0029",
      "C0030",
      "C0031",
      "C0032",
      "C0033",
      "C0034",
      "C0035",
      "C0036",
      "C0037",
      "C0038",
      "C0039"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
      },
      {
        "clause_id": "C0002",
        "location": "一、劳动合同双方当事人基本情况",
        "title": "劳动合同双方当事人基本情况",
        "section_type": "正式合同条款",
        "heading_path": [
          "一、劳动合同双方当事人基本情况"
        ],
        "text": "一、劳动合同双方当事人基本情况"
      },
      {
        "clause_id": "C0003",
        "location": "第一条",
        "title": "第一条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
      },
      {
        "clause_id": "C0004",
        "location": "第二条",
        "title": "第二条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
      },
      {
        "clause_id": "C0005",
        "location": "二、劳动合同期限",
        "title": "劳动合同期限",
        "section_type": "正式合同条款",
        "heading_path": [
          "二、劳动合同期限"
        ],
        "text": "二、劳动合同期限"
      },
      {
        "clause_id": "C0006",
        "location": "第三条",
        "title": "第三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
      },
      {
        "clause_id": "C0007",
        "location": "三、工作内容和工作地点",
        "title": "工作内容和工作地点",
        "section_type": "正式合同条款",
        "heading_path": [
          "三、工作内容和工作地点"
        ],
        "text": "三、工作内容和工作地点"
      },
      {
        "clause_id": "C0008",
        "location": "第四条",
        "title": "第四条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条"
        ],
        "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
      },
      {
        "clause_id": "C0009",
        "location": "第五条",
        "title": "第五条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条"
        ],
        "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
      },
      {
        "clause_id": "C0010",
        "location": "第六条",
        "title": "第六条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条"
        ],
        "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
      },
      {
        "clause_id": "C0011",
        "location": "四、工作时间和休息休假",
        "title": "工作时间和休息休假",
        "section_type": "正式合同条款",
        "heading_path": [
          "四、工作时间和休息休假"
        ],
        "text": "四、工作时间和休息休假"
      },
      {
        "clause_id": "C0012",
        "location": "第七条",
        "title": "第七条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条"
        ],
        "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
      },
      {
        "clause_id": "C0013",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
      },
      {
        "clause_id": "C0014",
        "location": "五、劳动报酬",
        "title": "劳动报酬",
        "section_type": "正式合同条款",
        "heading_path": [
          "五、劳动报酬"
        ],
        "text": "五、劳动报酬"
      },
      {
        "clause_id": "C0015",
        "location": "第九条",
        "title": "第九条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第九条"
        ],
        "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
      },
      {
        "clause_id": "C0016",
        "location": "第十条",
        "title": "第十条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十条"
        ],
        "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
      },
      {
        "clause_id": "C0017",
        "location": "六、社会保险及其他保险福利待遇",
        "title": "社会保险及其他保险福利待遇",
        "section_type": "正式合同条款",
        "heading_path": [
          "六、社会保险及其他保险福利待遇"
        ],
        "text": "六、社会保险及其他保险福利待遇"
      },
      {
        "clause_id": "C0018",
        "location": "第十一条",
        "title": "第十一条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十一条"
        ],
        "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
      },
      {
        "clause_id": "C0019",
        "location": "第十二条",
        "title": "第十二条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十二条"
        ],
        "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
      },
      {
        "clause_id": "C0020",
        "location": "第十三条",
        "title": "第十三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十三条"
        ],
        "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
      },
      {
        "clause_id": "C0021",
        "location": "第十四条",
        "title": "第十四条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十四条"
        ],
        "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
      },
      {
        "clause_id": "C0022",
        "location": "七、劳动保护、劳动条件和职业危害防护",
        "title": "劳动保护、劳动条件和职业危害防护",
        "section_type": "正式合同条款",
        "heading_path": [
          "七、劳动保护、劳动条件和职业危害防护"
        ],
        "text": "七、劳动保护、劳动条件和职业危害防护"
      },
      {
        "clause_id": "C0023",
        "location": "第十五条",
        "title": "第十五条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十五条"
        ],
        "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
      },
      {
        "clause_id": "C0024",
        "location": "第十六条",
        "title": "第十六条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十六条"
        ],
        "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
      },
      {
        "clause_id": "C0025",
        "location": "第十七条",
        "title": "第十七条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十七条"
        ],
        "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
      },
      {
        "clause_id": "C0026",
        "location": "八、劳动合同的解除、终止和经济补偿",
        "title": "劳动合同的解除、终止和经济补偿",
        "section_type": "正式合同条款",
        "heading_path": [
          "八、劳动合同的解除、终止和经济补偿"
        ],
        "text": "八、劳动合同的解除、终止和经济补偿"
      },
      {
        "clause_id": "C0027",
        "location": "第十八条",
        "title": "第十八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十八条"
        ],
        "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
      },
      {
        "clause_id": "C0028",
        "location": "第十九条",
        "title": "第十九条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十九条"
        ],
        "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
      },
      {
        "clause_id": "C0029",
        "location": "第二十条",
        "title": "第二十条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十条"
        ],
        "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
      },
      {
        "clause_id": "C0030",
        "location": "九、当事人约定的其他内容",
        "title": "当事人约定的其他内容",
        "section_type": "正式合同条款",
        "heading_path": [
          "九、当事人约定的其他内容"
        ],
        "text": "九、当事人约定的其他内容"
      },
      {
        "clause_id": "C0031",
        "location": "第二十一条",
        "title": "第二十一条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十一条"
        ],
        "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
      },
      {
        "clause_id": "C0032",
        "location": "十、劳动争议处理及其它",
        "title": "劳动争议处理及其它",
        "section_type": "正式合同条款",
        "heading_path": [
          "十、劳动争议处理及其它"
        ],
        "text": "十、劳动争议处理及其它"
      },
      {
        "clause_id": "C0033",
        "location": "第二十二条",
        "title": "第二十二条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十二条"
        ],
        "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
      },
      {
        "clause_id": "C0034",
        "location": "第二十三条",
        "title": "第二十三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十三条"
        ],
        "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
      },
      {
        "clause_id": "C0035",
        "location": "第二十四条",
        "title": "第二十四条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十四条"
        ],
        "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
      },
      {
        "clause_id": "C0036",
        "location": "第二十五条",
        "title": "第二十五条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十五条"
        ],
        "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0037",
        "location": "甲方（公章）：北京远航智能科技有限公司",
        "title": "甲方（公章）：北京远航智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十五条"
        ],
        "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
      },
      {
        "clause_id": "C0038",
        "location": "乙方（签字或盖章）：赵晨",
        "title": "乙方（签字或盖章）：赵晨",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十五条"
        ],
        "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
      },
      {
        "clause_id": "C0039",
        "location": "附件",
        "title": "附件一：岗位职责说明书",
        "section_type": "附件",
        "heading_path": [
          "附件一：岗位职责说明书"
        ],
        "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "一、劳动合同双方当事人基本情况",
        "title": "劳动合同双方当事人基本情况",
        "section_type": "正式合同条款",
        "heading_path": [
          "一、劳动合同双方当事人基本情况"
        ],
        "text": "一、劳动合同双方当事人基本情况",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第一条",
        "title": "第一条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "第二条",
        "title": "第二条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0005",
        "location": "二、劳动合同期限",
        "title": "劳动合同期限",
        "section_type": "正式合同条款",
        "heading_path": [
          "二、劳动合同期限"
        ],
        "text": "二、劳动合同期限",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0006",
        "location": "第三条",
        "title": "第三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "text": "第三条\n本合同为无固定期限劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0006",
        "location": "第三条",
        "title": "第三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0007",
        "location": "三、工作内容和工作地点",
        "title": "工作内容和工作地点",
        "section_type": "正式合同条款",
        "heading_path": [
          "三、工作内容和工作地点"
        ],
        "text": "三、工作内容和工作地点",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-10-01",
    "element_id": "employment_exit_2",
    "review_id": "EMP-10-01",
    "search_targets": [
      "解除通知方式或明确解除日期"
    ],
    "query_patterns": [
      "(?:解除|终止).{0,40}(?:书面通知|\\d{4}年\\d{1,2}月\\d{1,2}日)|提前.{0,8}(?:三十|30)日.{0,8}书面通知"
    ],
    "query_semantic_target": "解除通知方式或明确解除日期",
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "SEMANTIC_REQUIREMENT",
    "searched_clause_ids": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021",
      "C0022",
      "C0023",
      "C0024",
      "C0025",
      "C0026",
      "C0027",
      "C0028",
      "C0029",
      "C0030",
      "C0031",
      "C0032",
      "C0033",
      "C0034",
      "C0035",
      "C0036",
      "C0037",
      "C0038",
      "C0039"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
      },
      {
        "clause_id": "C0002",
        "location": "一、劳动合同双方当事人基本情况",
        "title": "劳动合同双方当事人基本情况",
        "section_type": "正式合同条款",
        "heading_path": [
          "一、劳动合同双方当事人基本情况"
        ],
        "text": "一、劳动合同双方当事人基本情况"
      },
      {
        "clause_id": "C0003",
        "location": "第一条",
        "title": "第一条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
      },
      {
        "clause_id": "C0004",
        "location": "第二条",
        "title": "第二条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
      },
      {
        "clause_id": "C0005",
        "location": "二、劳动合同期限",
        "title": "劳动合同期限",
        "section_type": "正式合同条款",
        "heading_path": [
          "二、劳动合同期限"
        ],
        "text": "二、劳动合同期限"
      },
      {
        "clause_id": "C0006",
        "location": "第三条",
        "title": "第三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
      },
      {
        "clause_id": "C0007",
        "location": "三、工作内容和工作地点",
        "title": "工作内容和工作地点",
        "section_type": "正式合同条款",
        "heading_path": [
          "三、工作内容和工作地点"
        ],
        "text": "三、工作内容和工作地点"
      },
      {
        "clause_id": "C0008",
        "location": "第四条",
        "title": "第四条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条"
        ],
        "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
      },
      {
        "clause_id": "C0009",
        "location": "第五条",
        "title": "第五条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五条"
        ],
        "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
      },
      {
        "clause_id": "C0010",
        "location": "第六条",
        "title": "第六条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第六条"
        ],
        "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
      },
      {
        "clause_id": "C0011",
        "location": "四、工作时间和休息休假",
        "title": "工作时间和休息休假",
        "section_type": "正式合同条款",
        "heading_path": [
          "四、工作时间和休息休假"
        ],
        "text": "四、工作时间和休息休假"
      },
      {
        "clause_id": "C0012",
        "location": "第七条",
        "title": "第七条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第七条"
        ],
        "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
      },
      {
        "clause_id": "C0013",
        "location": "第八条",
        "title": "第八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第八条"
        ],
        "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
      },
      {
        "clause_id": "C0014",
        "location": "五、劳动报酬",
        "title": "劳动报酬",
        "section_type": "正式合同条款",
        "heading_path": [
          "五、劳动报酬"
        ],
        "text": "五、劳动报酬"
      },
      {
        "clause_id": "C0015",
        "location": "第九条",
        "title": "第九条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第九条"
        ],
        "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
      },
      {
        "clause_id": "C0016",
        "location": "第十条",
        "title": "第十条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十条"
        ],
        "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
      },
      {
        "clause_id": "C0017",
        "location": "六、社会保险及其他保险福利待遇",
        "title": "社会保险及其他保险福利待遇",
        "section_type": "正式合同条款",
        "heading_path": [
          "六、社会保险及其他保险福利待遇"
        ],
        "text": "六、社会保险及其他保险福利待遇"
      },
      {
        "clause_id": "C0018",
        "location": "第十一条",
        "title": "第十一条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十一条"
        ],
        "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
      },
      {
        "clause_id": "C0019",
        "location": "第十二条",
        "title": "第十二条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十二条"
        ],
        "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
      },
      {
        "clause_id": "C0020",
        "location": "第十三条",
        "title": "第十三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十三条"
        ],
        "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
      },
      {
        "clause_id": "C0021",
        "location": "第十四条",
        "title": "第十四条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十四条"
        ],
        "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
      },
      {
        "clause_id": "C0022",
        "location": "七、劳动保护、劳动条件和职业危害防护",
        "title": "劳动保护、劳动条件和职业危害防护",
        "section_type": "正式合同条款",
        "heading_path": [
          "七、劳动保护、劳动条件和职业危害防护"
        ],
        "text": "七、劳动保护、劳动条件和职业危害防护"
      },
      {
        "clause_id": "C0023",
        "location": "第十五条",
        "title": "第十五条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十五条"
        ],
        "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
      },
      {
        "clause_id": "C0024",
        "location": "第十六条",
        "title": "第十六条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十六条"
        ],
        "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
      },
      {
        "clause_id": "C0025",
        "location": "第十七条",
        "title": "第十七条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十七条"
        ],
        "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
      },
      {
        "clause_id": "C0026",
        "location": "八、劳动合同的解除、终止和经济补偿",
        "title": "劳动合同的解除、终止和经济补偿",
        "section_type": "正式合同条款",
        "heading_path": [
          "八、劳动合同的解除、终止和经济补偿"
        ],
        "text": "八、劳动合同的解除、终止和经济补偿"
      },
      {
        "clause_id": "C0027",
        "location": "第十八条",
        "title": "第十八条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十八条"
        ],
        "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
      },
      {
        "clause_id": "C0028",
        "location": "第十九条",
        "title": "第十九条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第十九条"
        ],
        "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
      },
      {
        "clause_id": "C0029",
        "location": "第二十条",
        "title": "第二十条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十条"
        ],
        "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
      },
      {
        "clause_id": "C0030",
        "location": "九、当事人约定的其他内容",
        "title": "当事人约定的其他内容",
        "section_type": "正式合同条款",
        "heading_path": [
          "九、当事人约定的其他内容"
        ],
        "text": "九、当事人约定的其他内容"
      },
      {
        "clause_id": "C0031",
        "location": "第二十一条",
        "title": "第二十一条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十一条"
        ],
        "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
      },
      {
        "clause_id": "C0032",
        "location": "十、劳动争议处理及其它",
        "title": "劳动争议处理及其它",
        "section_type": "正式合同条款",
        "heading_path": [
          "十、劳动争议处理及其它"
        ],
        "text": "十、劳动争议处理及其它"
      },
      {
        "clause_id": "C0033",
        "location": "第二十二条",
        "title": "第二十二条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十二条"
        ],
        "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
      },
      {
        "clause_id": "C0034",
        "location": "第二十三条",
        "title": "第二十三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十三条"
        ],
        "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
      },
      {
        "clause_id": "C0035",
        "location": "第二十四条",
        "title": "第二十四条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十四条"
        ],
        "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
      },
      {
        "clause_id": "C0036",
        "location": "第二十五条",
        "title": "第二十五条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十五条"
        ],
        "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
      },
      {
        "clause_id": "C0037",
        "location": "甲方（公章）：北京远航智能科技有限公司",
        "title": "甲方（公章）：北京远航智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十五条"
        ],
        "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
      },
      {
        "clause_id": "C0038",
        "location": "乙方（签字或盖章）：赵晨",
        "title": "乙方（签字或盖章）：赵晨",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二十五条"
        ],
        "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
      },
      {
        "clause_id": "C0039",
        "location": "附件",
        "title": "附件一：岗位职责说明书",
        "section_type": "附件",
        "heading_path": [
          "附件一：岗位职责说明书"
        ],
        "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0002",
        "location": "一、劳动合同双方当事人基本情况",
        "title": "劳动合同双方当事人基本情况",
        "section_type": "正式合同条款",
        "heading_path": [
          "一、劳动合同双方当事人基本情况"
        ],
        "text": "一、劳动合同双方当事人基本情况",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0003",
        "location": "第一条",
        "title": "第一条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0004",
        "location": "第二条",
        "title": "第二条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0005",
        "location": "二、劳动合同期限",
        "title": "劳动合同期限",
        "section_type": "正式合同条款",
        "heading_path": [
          "二、劳动合同期限"
        ],
        "text": "二、劳动合同期限",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0006",
        "location": "第三条",
        "title": "第三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "text": "第三条\n本合同为无固定期限劳动合同。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0006",
        "location": "第三条",
        "title": "第三条",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      },
      {
        "clause_id": "C0007",
        "location": "三、工作内容和工作地点",
        "title": "工作内容和工作地点",
        "section_type": "正式合同条款",
        "heading_path": [
          "三、工作内容和工作地点"
        ],
        "text": "三、工作内容和工作地点",
        "score": 0.0,
        "accepted": false,
        "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
        "matched_semantic_patterns": [],
        "matched_contextual_patterns": [],
        "matched_excluded_patterns": [],
        "required_fact_groups": {},
        "stage_trace": {
          "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
          "rerank": "score=0; semantic_hits=0; contextual_hits=0",
          "threshold": "REJECT",
          "contradiction_filter": "PASS"
        }
      }
    ],
    "stage_results": {
      "normalize": "PASS",
      "rerank": "PASS",
      "threshold": "NOT_FOUND",
      "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
    },
    "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  }
]
```

## EMP-01-01

```json
{
  "rule_id": "EMP-01-01",
  "applicability": {
    "review_id": "EMP-01-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。",
  "coverage_elements": [
    {
      "review_id": "EMP-01-01",
      "element_id": "employment_identity_1",
      "proposition": "用人单位住所",
      "status": "COVERED",
      "evidence_ids": [
        "C0003"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0003"
      ],
      "source_spans": [
        "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
      ],
      "source_locations": [
        "第一条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0003"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0003"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0003",
          "quote": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        }
      ]
    },
    {
      "review_id": "EMP-01-01",
      "element_id": "employment_identity_2",
      "proposition": "劳动者姓名与身份证明",
      "status": "COVERED",
      "evidence_ids": [
        "C0004"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0004"
      ],
      "source_spans": [
        "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
      ],
      "source_locations": [
        "第二条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0004"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0004"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0004",
          "quote": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        }
      ]
    },
    {
      "review_id": "EMP-01-01",
      "element_id": "employment_identity_name",
      "proposition": "用人单位名称",
      "status": "COVERED",
      "evidence_ids": [
        "C0001"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0001"
      ],
      "source_spans": [
        "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
      ],
      "source_locations": [
        "全文"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0001"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0001"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "quote": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_identity_1",
      "review_id": "EMP-01-01",
      "search_targets": [
        "用人单位住所"
      ],
      "query_patterns": [
        "(?:用人单位|劳务派遣单位)[）)]?\\s*(?:名称|姓名)?\\s*[：:]\\s*[^\\n，；。_]{2,60}(?:公司|企业|事务所)(?:(?!乙方|劳动者|用工单位).){0,300}(?:住所|地址|注册地|注册登记地|实际经营地)[：:]\\s*[^\\n，；。_]{3,60}",
        "甲方[：:]\\s*[^\\n，；。_]{2,60}(?:(?!乙方)[\\s\\S]){0,120}(?:住所|地址)[：:]\\s*[^\\n，；。_]{3,60}"
      ],
      "query_semantic_target": "用人单位住所",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "甲方[：:]\\s*[^\\n，；。_]{2,60}(?:(?!乙方)[\\s\\S]){0,120}(?:住所|地址)[：:]\\s*[^\\n，；。_]{3,60}"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "quote": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "original_excerpt": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 96,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_identity_2",
      "review_id": "EMP-01-01",
      "search_targets": [
        "劳动者姓名与身份证明"
      ],
      "query_patterns": [
        "劳动者[）)]?\\s*(?:名称|姓名)?\\s*[：:]\\s*[\\u4e00-\\u9fff·]{2,12}[^。；]{0,160}(?:居民身份证号码|身份证(?:号码)?|证件号码)[：:]?\\s*[0-9Xx]{8,18}",
        "乙方[：:]?\\s*[\\u4e00-\\u9fff·]{2,12}[\\s\\S]{0,180}(?:居民身份证号码|身份证号码|证件号码)[：:]\\s*[0-9Xx]{8,18}"
      ],
      "query_semantic_target": "劳动者姓名与身份证明",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "乙方[：:]?\\s*[\\u4e00-\\u9fff·]{2,12}[\\s\\S]{0,180}(?:居民身份证号码|身份证号码|证件号码)[：:]\\s*[0-9Xx]{8,18}"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "quote": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "original_excerpt": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 187,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_identity_name",
      "review_id": "EMP-01-01",
      "search_targets": [
        "用人单位名称"
      ],
      "query_patterns": [
        "甲方[：:]\\s*[^\\n，；。_]{2,60}",
        "甲方[^\\n，；。_]{2,60}(?:大学|学院|医院|公司|研究所|中心)",
        "(?:用人单位|劳务派遣单位)[）)]?\\s*(?:名称)?\\s*[：:]\\s*[^\\n，；。_]{2,60}"
      ],
      "query_semantic_target": "用人单位名称",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "甲方[：:]\\s*[^\\n，；。_]{2,60}",
            "甲方[^\\n，；。_]{2,60}(?:大学|学院|医院|公司|研究所|中心)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=2; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "甲方[：:]\\s*[^\\n，；。_]{2,60}",
            "甲方[^\\n，；。_]{2,60}(?:大学|学院|医院|公司|研究所|中心)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=2; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "甲方[^\\n，；。_]{2,60}(?:大学|学院|医院|公司|研究所|中心)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "甲方[^\\n，；。_]{2,60}(?:大学|学院|医院|公司|研究所|中心)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "quote": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "original_excerpt": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 117,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "quote": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "original_excerpt": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 96,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "text": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。",
          "quote": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。",
          "original_excerpt": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "source_start": 65,
          "source_end": 127,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日",
          "quote": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日",
          "original_excerpt": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "source_start": 0,
          "source_end": 57,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0001",
      "location": "全文",
      "title": "全文",
      "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
      "quote": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
      "original_excerpt": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 0,
      "source_end": 117,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "全文",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
      "source_span": {
        "start_offset": 0,
        "end_offset": 117,
        "raw_text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0001",
        "section": "全文",
        "sentence_index": 1,
        "quote": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_name"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_name"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0003",
      "location": "第一条",
      "title": "第一条",
      "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
      "quote": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
      "original_excerpt": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
      "section_type": "正式合同条款",
      "heading_path": [
        "第一条"
      ],
      "source_start": 134,
      "source_end": 230,
      "supports_element_ids": [
        "employment_identity_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第一条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
      "source_span": {
        "start_offset": 134,
        "end_offset": 230,
        "raw_text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0003",
        "section": "第一条",
        "sentence_index": 1,
        "quote": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0003",
      "location": "第一条",
      "title": "第一条",
      "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
      "quote": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
      "original_excerpt": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
      "section_type": "正式合同条款",
      "heading_path": [
        "第一条"
      ],
      "source_start": 134,
      "source_end": 230,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第一条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
      "source_span": {
        "start_offset": 134,
        "end_offset": 230,
        "raw_text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0003",
        "section": "第一条",
        "sentence_index": 1,
        "quote": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0004",
      "location": "第二条",
      "title": "第二条",
      "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
      "quote": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
      "original_excerpt": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二条"
      ],
      "source_start": 231,
      "source_end": 418,
      "supports_element_ids": [
        "employment_identity_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
      "source_span": {
        "start_offset": 231,
        "end_offset": 418,
        "raw_text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0004",
        "section": "第二条",
        "sentence_index": 1,
        "quote": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0037",
      "location": "甲方（公章）：北京远航智能科技有限公司",
      "title": "甲方（公章）：北京远航智能科技有限公司",
      "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日",
      "quote": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日",
      "original_excerpt": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二十五条"
      ],
      "source_start": 2422,
      "source_end": 2479,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "甲方（公章）：北京远航智能科技有限公司",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日",
      "source_span": {
        "start_offset": 2422,
        "end_offset": 2479,
        "raw_text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0037",
        "section": "甲方（公章）：北京远航智能科技有限公司",
        "sentence_index": 1,
        "quote": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [],
      "canonical_fact_keys": [],
      "relevance_score": 0.0,
      "selection_reason": "Contextual retrieval evidence does not directly support a resolved ReviewElementTruth.",
      "review_id": "EMP-01-01",
      "element_ids": [],
      "support_type": "CONTEXTUAL",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0015",
      "location": "第九条",
      "title": "第九条",
      "text": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。",
      "quote": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。",
      "original_excerpt": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第九条"
      ],
      "source_start": 1051,
      "source_end": 1112,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第九条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。",
      "source_span": {
        "start_offset": 1051,
        "end_offset": 1112,
        "raw_text": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0015",
        "section": "第九条",
        "sentence_index": 1,
        "quote": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [],
      "canonical_fact_keys": [],
      "relevance_score": 0.0,
      "selection_reason": "Contextual retrieval evidence does not directly support a resolved ReviewElementTruth.",
      "review_id": "EMP-01-01",
      "element_ids": [],
      "support_type": "CONTEXTUAL",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-02-01

```json
{
  "rule_id": "EMP-02-01",
  "applicability": {
    "review_id": "EMP-02-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。",
  "coverage_elements": [
    {
      "review_id": "EMP-02-01",
      "element_id": "employment_term_1",
      "proposition": "期限类型",
      "status": "COVERED",
      "evidence_ids": [
        "C0001"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0001"
      ],
      "source_spans": [
        "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
      ],
      "source_locations": [
        "全文"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0001"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0001"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "quote": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        }
      ]
    },
    {
      "review_id": "EMP-02-01",
      "element_id": "employment_term_start",
      "proposition": "生效或起始日期",
      "status": "COVERED",
      "evidence_ids": [
        "C0006"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0006"
      ],
      "source_spans": [
        "第三条\n本合同为无固定期限劳动合同。",
        "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
      ],
      "source_locations": [
        "第三条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0006"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0006"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0006",
          "quote": "第三条\n本合同为无固定期限劳动合同。"
        },
        {
          "clause_id": "C0006",
          "quote": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_term_1",
      "review_id": "EMP-02-01",
      "search_targets": [
        "期限类型"
      ],
      "query_patterns": [
        "(?:固定期限|无固定期限|以完成.{1,30}工作任务为期限)"
      ],
      "query_semantic_target": "期限类型",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:固定期限|无固定期限|以完成.{1,30}工作任务为期限)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:固定期限|无固定期限|以完成.{1,30}工作任务为期限)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "quote": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "original_excerpt": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 117,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "quote": "第三条\n本合同为无固定期限劳动合同。",
          "original_excerpt": "第三条\n本合同为无固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 18,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_term_start",
      "review_id": "EMP-02-01",
      "search_targets": [
        "生效或起始日期"
      ],
      "query_patterns": [
        "(?:本合同|劳动合同|合同期限)(?:于|自|生效日期[为：:]?|起始日期[为：:]?)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "^\\s*自(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "(?:本合同|合同期限)\\s*[：:]?\\s*自?(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "起始日期[为：:]?\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
      ],
      "query_semantic_target": "生效或起始日期",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:本合同|劳动合同|合同期限)(?:于|自|生效日期[为：:]?|起始日期[为：:]?)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "quote": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "original_excerpt": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 18,
          "source_end": 54,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0001",
      "location": "全文",
      "title": "全文",
      "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
      "quote": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
      "original_excerpt": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 0,
      "source_end": 117,
      "supports_element_ids": [
        "employment_term_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "全文",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
      "source_span": {
        "start_offset": 0,
        "end_offset": 117,
        "raw_text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0001",
        "section": "全文",
        "sentence_index": 1,
        "quote": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_term_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-02-01",
      "element_ids": [
        "employment_term_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0006",
      "location": "第三条",
      "title": "第三条",
      "text": "第三条\n本合同为无固定期限劳动合同。",
      "quote": "第三条\n本合同为无固定期限劳动合同。",
      "original_excerpt": "第三条\n本合同为无固定期限劳动合同。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第三条"
      ],
      "source_start": 428,
      "source_end": 446,
      "supports_element_ids": [
        "employment_term_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第三条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
      "source_span": {
        "start_offset": 428,
        "end_offset": 446,
        "raw_text": "第三条\n本合同为无固定期限劳动合同。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0006",
        "section": "第三条",
        "sentence_index": 1,
        "quote": "第三条\n本合同为无固定期限劳动合同。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第三条\n本合同为无固定期限劳动合同。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_term_start"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-02-01",
      "element_ids": [
        "employment_term_start"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0006",
      "location": "第三条",
      "title": "第三条",
      "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
      "quote": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
      "original_excerpt": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第三条"
      ],
      "source_start": 447,
      "source_end": 482,
      "supports_element_ids": [
        "employment_term_start"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第三条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
      "source_span": {
        "start_offset": 447,
        "end_offset": 482,
        "raw_text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0006",
        "section": "第三条",
        "sentence_index": 1,
        "quote": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_term_start"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-02-01",
      "element_ids": [
        "employment_term_start"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-03-01

```json
{
  "rule_id": "EMP-03-01",
  "applicability": {
    "review_id": "EMP-03-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "medium",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "合同已触发“出现试用期安排时适用”这一适用条件。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "出现试用期安排时适用",
    "triggered": true,
    "condition_text": "出现试用期安排时适用"
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。",
  "coverage_elements": [
    {
      "review_id": "EMP-03-01",
      "element_id": "employment_probation_1",
      "proposition": "试用期长度",
      "status": "COVERED",
      "evidence_ids": [
        "C0006"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0006"
      ],
      "source_spans": [
        "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
      ],
      "source_locations": [
        "第三条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0006"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0006"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0006",
          "quote": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        }
      ]
    },
    {
      "review_id": "EMP-03-01",
      "element_id": "employment_probation_2",
      "proposition": "试用期工资标准",
      "status": "COVERED",
      "evidence_ids": [
        "C0015"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0015"
      ],
      "source_spans": [
        "乙方在试用期期间的工资为人民币12000元。"
      ],
      "source_locations": [
        "第九条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0015"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0015"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0015",
          "quote": "乙方在试用期期间的工资为人民币12000元。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_probation_1",
      "review_id": "EMP-03-01",
      "search_targets": [
        "试用期长度"
      ],
      "query_patterns": [
        "试用期(?:为|：|:)?\\s*[一二三四五六七八九十\\d]+个?月",
        "试用期[：:]?\\s*自?\\d{4}[年/-]\\d{1,2}[月/-]\\d{1,2}日?起?至\\d{4}[年/-]\\d{1,2}[月/-]\\d{1,2}日?",
        "本合同自\\d{4}年\\d{1,2}月\\d{1,2}日起?至\\d{4}年\\d{1,2}月\\d{1,2}日止?，其中试用期至\\d{4}年\\d{1,2}月\\d{1,2}日",
        "(?:其中\\s*)?试用期(?:截止|结束)?(?:至|于)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
      ],
      "query_semantic_target": "试用期长度",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:其中\\s*)?试用期(?:截止|结束)?(?:至|于)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "quote": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "original_excerpt": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 18,
          "source_end": 54,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_probation_2",
      "review_id": "EMP-03-01",
      "search_targets": [
        "试用期工资标准"
      ],
      "query_patterns": [
        "试用期(?:期间的|月)?(?:正常工作时间)?工资[^\\n。；]{0,12}\\d+(?:\\.\\d+)?\\s*元",
        "试用期.{0,30}(?:百分之八十|80%).{0,40}最低工资",
        "试用期(?:期间的|月)?(?:基本)?工资(?:标准)?(?:为|：|:)?\\s*(?:人民币)?\\s*\\d+(?:\\.\\d+)?\\s*元"
      ],
      "query_semantic_target": "试用期工资标准",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "乙方在试用期期间的工资为人民币12000元。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "试用期(?:期间的|月)?(?:正常工作时间)?工资[^\\n。；]{0,12}\\d+(?:\\.\\d+)?\\s*元",
            "试用期(?:期间的|月)?(?:基本)?工资(?:标准)?(?:为|：|:)?\\s*(?:人民币)?\\s*\\d+(?:\\.\\d+)?\\s*元"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=2; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "text": "乙方在试用期期间的工资为人民币12000元。",
          "quote": "乙方在试用期期间的工资为人民币12000元。",
          "original_excerpt": "乙方在试用期期间的工资为人民币12000元。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "source_start": 42,
          "source_end": 65,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0006",
      "location": "第三条",
      "title": "第三条",
      "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
      "quote": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
      "original_excerpt": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第三条"
      ],
      "source_start": 447,
      "source_end": 482,
      "supports_element_ids": [
        "employment_probation_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第三条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
      "source_span": {
        "start_offset": 447,
        "end_offset": 482,
        "raw_text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0006",
        "section": "第三条",
        "sentence_index": 1,
        "quote": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_probation_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-03-01",
      "element_ids": [
        "employment_probation_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0015",
      "location": "第九条",
      "title": "第九条",
      "text": "乙方在试用期期间的工资为人民币12000元。",
      "quote": "乙方在试用期期间的工资为人民币12000元。",
      "original_excerpt": "乙方在试用期期间的工资为人民币12000元。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第九条"
      ],
      "source_start": 1028,
      "source_end": 1050,
      "supports_element_ids": [
        "employment_probation_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第九条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。",
      "source_span": {
        "start_offset": 1028,
        "end_offset": 1050,
        "raw_text": "乙方在试用期期间的工资为人民币12000元。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0015",
        "section": "第九条",
        "sentence_index": 1,
        "quote": "乙方在试用期期间的工资为人民币12000元。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "乙方在试用期期间的工资为人民币12000元。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_probation_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-03-01",
      "element_ids": [
        "employment_probation_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-15-01

```json
{
  "rule_id": "EMP-15-01",
  "applicability": {
    "review_id": "EMP-15-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-15-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021",
      "C0022",
      "C0023",
      "C0024",
      "C0025",
      "C0026",
      "C0027",
      "C0028",
      "C0029",
      "C0030",
      "C0031",
      "C0032",
      "C0033",
      "C0034",
      "C0035",
      "C0036",
      "C0037",
      "C0038",
      "C0039"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-04-01

```json
{
  "rule_id": "EMP-04-01",
  "applicability": {
    "review_id": "EMP-04-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。",
  "coverage_elements": [
    {
      "review_id": "EMP-04-01",
      "element_id": "employment_work_1",
      "proposition": "具体工作岗位或职责",
      "status": "COVERED",
      "evidence_ids": [
        "C0008"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0008"
      ],
      "source_spans": [
        "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
      ],
      "source_locations": [
        "第四条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0008"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0008"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0008",
          "quote": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        }
      ]
    },
    {
      "review_id": "EMP-04-01",
      "element_id": "employment_work_2",
      "proposition": "具体工作地点",
      "status": "COVERED",
      "evidence_ids": [
        "C0009"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0009"
      ],
      "source_spans": [
        "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
      ],
      "source_locations": [
        "第五条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0009"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0009"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0009",
          "quote": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_work_1",
      "review_id": "EMP-04-01",
      "search_targets": [
        "具体工作岗位或职责"
      ],
      "query_patterns": [
        "(?:工作岗位|工作内容|岗位)[为：:][^，。；_]{2,35}|安排(?:乙方|劳动者)在[^，。；_]{2,40}岗位|从事[^，。；_]{2,60}(?:开发|维护|测试|工作)",
        "(?:担任|从事)[^。；\\n]{2,60}岗位",
        "(?:负责|参与|承担)[^。；\\n]{2,80}(?:研发|开发|测试|维护|研究|设计|整理|编写)"
      ],
      "query_semantic_target": "具体工作岗位或职责",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:担任|从事)[^。；\\n]{2,60}岗位"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:负责|参与|承担)[^。；\\n]{2,80}(?:研发|开发|测试|维护|研究|设计|整理|编写)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
          "quote": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
          "original_excerpt": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 31,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。",
          "quote": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。",
          "original_excerpt": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "source_start": 0,
          "source_end": 182,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_work_2",
      "review_id": "EMP-04-01",
      "search_targets": [
        "具体工作地点"
      ],
      "query_patterns": [
        "工作地点[为：:][^，。；_]{3,60}"
      ],
      "query_semantic_target": "具体工作地点",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "工作地点[为：:][^，。；_]{3,60}"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。",
          "quote": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。",
          "original_excerpt": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "source_start": 0,
          "source_end": 51,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0009",
      "location": "第五条",
      "title": "第五条",
      "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。",
      "quote": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。",
      "original_excerpt": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第五条"
      ],
      "source_start": 527,
      "source_end": 578,
      "supports_element_ids": [
        "employment_work_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第五条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。",
      "source_span": {
        "start_offset": 527,
        "end_offset": 578,
        "raw_text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0009",
        "section": "第五条",
        "sentence_index": 1,
        "quote": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_work_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-04-01",
      "element_ids": [
        "employment_work_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0008",
      "location": "第四条",
      "title": "第四条",
      "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
      "quote": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
      "original_excerpt": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第四条"
      ],
      "source_start": 495,
      "source_end": 526,
      "supports_element_ids": [
        "employment_work_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第四条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
      "source_span": {
        "start_offset": 495,
        "end_offset": 526,
        "raw_text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0008",
        "section": "第四条",
        "sentence_index": 1,
        "quote": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_work_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-04-01",
      "element_ids": [
        "employment_work_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0039",
      "location": "附件",
      "title": "附件一：岗位职责说明书",
      "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。",
      "quote": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。",
      "original_excerpt": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。",
      "section_type": "附件",
      "heading_path": [
        "附件一：岗位职责说明书"
      ],
      "source_start": 2508,
      "source_end": 2690,
      "supports_element_ids": [
        "employment_work_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/appendix",
      "document_type": "APPENDIX",
      "source_document_type": "APPENDIX",
      "evidence_block_type": "ANNEX",
      "document_name": "合同附件/补充文件",
      "section": "附件",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日",
      "source_span": {
        "start_offset": 2508,
        "end_offset": 2690,
        "raw_text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。"
      },
      "source_document": "contract_package/appendix",
      "original_document_reference": "contract_package/appendix",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/appendix",
        "document_type": "APPENDIX",
        "document_name": "合同附件/补充文件",
        "clause_id": "C0039",
        "section": "附件",
        "sentence_index": 1,
        "quote": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。",
        "confidence": "high",
        "evidence_block_type": "ANNEX",
        "evidence_type": "ATTACHMENT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [],
      "canonical_fact_keys": [],
      "relevance_score": 0.0,
      "selection_reason": "Contextual retrieval evidence does not directly support a resolved ReviewElementTruth.",
      "review_id": "EMP-04-01",
      "element_ids": [],
      "support_type": "CONTEXTUAL",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-05-01

```json
{
  "rule_id": "EMP-05-01",
  "applicability": {
    "review_id": "EMP-05-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "部分覆盖",
  "reason": "未找到明确约定：加班报酬或依法调休。",
  "coverage_elements": [
    {
      "review_id": "EMP-05-01",
      "element_id": "employment_hours_1",
      "proposition": "工时制度及工作时间",
      "status": "COVERED",
      "evidence_ids": [
        "C0012"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0012"
      ],
      "source_spans": [
        "第七条\n甲方安排乙方执行标准工时制度。",
        "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
        "每周休息日为星期六、星期日。"
      ],
      "source_locations": [
        "第七条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0012"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0012"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0012",
          "quote": "第七条\n甲方安排乙方执行标准工时制度。"
        },
        {
          "clause_id": "C0012",
          "quote": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。"
        },
        {
          "clause_id": "C0012",
          "quote": "每周休息日为星期六、星期日。"
        }
      ]
    },
    {
      "review_id": "EMP-05-01",
      "element_id": "employment_hours_2",
      "proposition": "休息休假安排",
      "status": "COVERED",
      "evidence_ids": [
        "C0012"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0012"
      ],
      "source_spans": [
        "第七条\n甲方安排乙方执行标准工时制度。",
        "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
        "每周休息日为星期六、星期日。"
      ],
      "source_locations": [
        "第七条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0012"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0012"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0012",
          "quote": "第七条\n甲方安排乙方执行标准工时制度。"
        },
        {
          "clause_id": "C0012",
          "quote": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。"
        },
        {
          "clause_id": "C0012",
          "quote": "每周休息日为星期六、星期日。"
        }
      ]
    },
    {
      "review_id": "EMP-05-01",
      "element_id": "employment_hours_3",
      "proposition": "加班报酬或依法调休",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_hours_1",
      "review_id": "EMP-05-01",
      "search_targets": [
        "工时制度及工作时间"
      ],
      "query_patterns": [
        "(?:标准工时|每天.{0,5}[八8]小时|每周.{0,5}40小时)",
        "(?:综合计算工时|不定时工作制).{0,45}(?:审批|批准)"
      ],
      "query_semantic_target": "工时制度及工作时间",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:标准工时|每天.{0,5}[八8]小时|每周.{0,5}40小时)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:标准工时|每天.{0,5}[八8]小时|每周.{0,5}40小时)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "text": "第七条\n甲方安排乙方执行标准工时制度。",
          "quote": "第七条\n甲方安排乙方执行标准工时制度。",
          "original_excerpt": "第七条\n甲方安排乙方执行标准工时制度。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_hours_1"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "text": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
          "quote": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
          "original_excerpt": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "source_start": 19,
          "source_end": 57,
          "supports_element_ids": [
            "employment_hours_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_hours_2",
      "review_id": "EMP-05-01",
      "search_targets": [
        "休息休假安排"
      ],
      "query_patterns": [
        "(?:每周.{0,10}休息|(?:依法享有|依法享受).{0,15}(?:休假|年休假)|法定节假日.{0,10}休息)",
        "(?:休假制度|享受|享有)[^。；\\n]{0,40}(?:法定节假日|公休日|带薪年假)"
      ],
      "query_semantic_target": "休息休假安排",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "每周休息日为星期六、星期日。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:每周.{0,10}休息|(?:依法享有|依法享受).{0,15}(?:休假|年休假)|法定节假日.{0,10}休息)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:休假制度|享受|享有)[^。；\\n]{0,40}(?:法定节假日|公休日|带薪年假)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "text": "每周休息日为星期六、星期日。",
          "quote": "每周休息日为星期六、星期日。",
          "original_excerpt": "每周休息日为星期六、星期日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "source_start": 103,
          "source_end": 118,
          "supports_element_ids": [
            "employment_hours_2"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。",
          "quote": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。",
          "original_excerpt": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "source_start": 0,
          "source_end": 62,
          "supports_element_ids": [
            "employment_hours_2"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_hours_3",
      "review_id": "EMP-05-01",
      "search_targets": [
        "加班报酬或依法调休"
      ],
      "query_patterns": [
        "加班.{0,40}(?:依法支付|加班工资|补休|调休)",
        "依法安排[^。；\\n]{0,20}(?:补休|调休)或支付加班工资",
        "(?:支付|发放)加班工资"
      ],
      "query_semantic_target": "加班报酬或依法调休",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0012",
      "location": "第七条",
      "title": "第七条",
      "text": "第七条\n甲方安排乙方执行标准工时制度。",
      "quote": "第七条\n甲方安排乙方执行标准工时制度。",
      "original_excerpt": "第七条\n甲方安排乙方执行标准工时制度。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第七条"
      ],
      "source_start": 740,
      "source_end": 759,
      "supports_element_ids": [
        "employment_hours_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第七条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。",
      "source_span": {
        "start_offset": 740,
        "end_offset": 759,
        "raw_text": "第七条\n甲方安排乙方执行标准工时制度。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0012",
        "section": "第七条",
        "sentence_index": 1,
        "quote": "第七条\n甲方安排乙方执行标准工时制度。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第七条\n甲方安排乙方执行标准工时制度。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_hours_1",
        "employment_hours_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-05-01",
      "element_ids": [
        "employment_hours_1",
        "employment_hours_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0012",
      "location": "第七条",
      "title": "第七条",
      "text": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
      "quote": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
      "original_excerpt": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第七条"
      ],
      "source_start": 760,
      "source_end": 797,
      "supports_element_ids": [
        "employment_hours_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第七条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。",
      "source_span": {
        "start_offset": 760,
        "end_offset": 797,
        "raw_text": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0012",
        "section": "第七条",
        "sentence_index": 1,
        "quote": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_hours_1",
        "employment_hours_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-05-01",
      "element_ids": [
        "employment_hours_1",
        "employment_hours_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0012",
      "location": "第七条",
      "title": "第七条",
      "text": "每周休息日为星期六、星期日。",
      "quote": "每周休息日为星期六、星期日。",
      "original_excerpt": "每周休息日为星期六、星期日。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第七条"
      ],
      "source_start": 844,
      "source_end": 858,
      "supports_element_ids": [
        "employment_hours_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第七条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。",
      "source_span": {
        "start_offset": 844,
        "end_offset": 858,
        "raw_text": "每周休息日为星期六、星期日。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0012",
        "section": "第七条",
        "sentence_index": 1,
        "quote": "每周休息日为星期六、星期日。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "每周休息日为星期六、星期日。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_hours_1",
        "employment_hours_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-05-01",
      "element_ids": [
        "employment_hours_1",
        "employment_hours_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0013",
      "location": "第八条",
      "title": "第八条",
      "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。",
      "quote": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。",
      "original_excerpt": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第八条"
      ],
      "source_start": 915,
      "source_end": 977,
      "supports_element_ids": [
        "employment_hours_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第八条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。",
      "source_span": {
        "start_offset": 915,
        "end_offset": 977,
        "raw_text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0013",
        "section": "第八条",
        "sentence_index": 1,
        "quote": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [],
      "canonical_fact_keys": [],
      "relevance_score": 0.0,
      "selection_reason": "Contextual retrieval evidence does not directly support a resolved ReviewElementTruth.",
      "review_id": "EMP-05-01",
      "element_ids": [],
      "support_type": "CONTEXTUAL",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-06-01

```json
{
  "rule_id": "EMP-06-01",
  "applicability": {
    "review_id": "EMP-06-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。",
  "coverage_elements": [
    {
      "review_id": "EMP-06-01",
      "element_id": "employment_wage_1",
      "proposition": "工资金额或可计算标准",
      "status": "COVERED",
      "evidence_ids": [
        "C0015"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0015"
      ],
      "source_spans": [
        "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
      ],
      "source_locations": [
        "第九条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0015"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0015"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0015",
          "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
        }
      ]
    },
    {
      "review_id": "EMP-06-01",
      "element_id": "employment_wage_2",
      "proposition": "工资支付日期",
      "status": "COVERED",
      "evidence_ids": [
        "C0015"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0015"
      ],
      "source_spans": [
        "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
      ],
      "source_locations": [
        "第九条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0015"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0015"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0015",
          "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
        }
      ]
    },
    {
      "review_id": "EMP-06-01",
      "element_id": "employment_wage_3",
      "proposition": "工资支付方式",
      "status": "COVERED",
      "evidence_ids": [
        "C0015"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0015"
      ],
      "source_spans": [
        "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
      ],
      "source_locations": [
        "第九条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0015"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0015"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0015",
          "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_wage_1",
      "review_id": "EMP-06-01",
      "search_targets": [
        "工资金额或可计算标准"
      ],
      "query_patterns": [
        "(?<!试用期)(?:月工资|月正常工作时间工资|基本工资|工资标准)[为：:]?\\s*(?:人民币)?\\d+(?:\\.\\d+)?\\s*元"
      ],
      "query_semantic_target": "工资金额或可计算标准",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?<!试用期)(?:月工资|月正常工作时间工资|基本工资|工资标准)[为：:]?\\s*(?:人民币)?\\d+(?:\\.\\d+)?\\s*元"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "original_excerpt": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "source_start": 0,
          "source_end": 42,
          "supports_element_ids": [
            "employment_wage_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_wage_2",
      "review_id": "EMP-06-01",
      "search_targets": [
        "工资支付日期"
      ],
      "query_patterns": [
        "每月\\d{1,2}日.{0,20}(?:发放|支付|银行)|工资.{0,20}每月\\d{1,2}日",
        "每月[一二三四五六七八九十\\d]{1,3}日(?:前|内)?[^。；\\n]{0,30}支付[^。；\\n]{0,20}工资"
      ],
      "query_semantic_target": "工资支付日期",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "每月\\d{1,2}日.{0,20}(?:发放|支付|银行)|工资.{0,20}每月\\d{1,2}日",
            "每月[一二三四五六七八九十\\d]{1,3}日(?:前|内)?[^。；\\n]{0,30}支付[^。；\\n]{0,20}工资"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=2; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "original_excerpt": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "source_start": 0,
          "source_end": 42,
          "supports_element_ids": [
            "employment_wage_2"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_wage_3",
      "review_id": "EMP-06-01",
      "search_targets": [
        "工资支付方式"
      ],
      "query_patterns": [
        "工资.{0,40}(?:银行转账|银行账户|现金支付)|(?:银行转账|银行账户|现金支付)[^。；]{0,40}工资",
        "以货币形式支付[^。；\\n]{0,20}工资"
      ],
      "query_semantic_target": "工资支付方式",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "工资.{0,40}(?:银行转账|银行账户|现金支付)|(?:银行转账|银行账户|现金支付)[^。；]{0,40}工资"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "original_excerpt": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "source_start": 0,
          "source_end": 42,
          "supports_element_ids": [
            "employment_wage_3"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0015",
      "location": "第九条",
      "title": "第九条",
      "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
      "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
      "original_excerpt": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第九条"
      ],
      "source_start": 985,
      "source_end": 1027,
      "supports_element_ids": [
        "employment_wage_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第九条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。",
      "source_span": {
        "start_offset": 985,
        "end_offset": 1027,
        "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0015",
        "section": "第九条",
        "sentence_index": 1,
        "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_wage_1",
        "employment_wage_2",
        "employment_wage_3"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-06-01",
      "element_ids": [
        "employment_wage_1",
        "employment_wage_2",
        "employment_wage_3"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0015",
      "location": "第九条",
      "title": "第九条",
      "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
      "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
      "original_excerpt": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第九条"
      ],
      "source_start": 985,
      "source_end": 1027,
      "supports_element_ids": [
        "employment_wage_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第九条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。",
      "source_span": {
        "start_offset": 985,
        "end_offset": 1027,
        "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0015",
        "section": "第九条",
        "sentence_index": 1,
        "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_wage_1",
        "employment_wage_2",
        "employment_wage_3"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-06-01",
      "element_ids": [
        "employment_wage_1",
        "employment_wage_2",
        "employment_wage_3"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0015",
      "location": "第九条",
      "title": "第九条",
      "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
      "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
      "original_excerpt": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第九条"
      ],
      "source_start": 985,
      "source_end": 1027,
      "supports_element_ids": [
        "employment_wage_3"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第九条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。",
      "source_span": {
        "start_offset": 985,
        "end_offset": 1027,
        "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0015",
        "section": "第九条",
        "sentence_index": 1,
        "quote": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_wage_1",
        "employment_wage_2",
        "employment_wage_3"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-06-01",
      "element_ids": [
        "employment_wage_1",
        "employment_wage_2",
        "employment_wage_3"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-07-01

```json
{
  "rule_id": "EMP-07-01",
  "applicability": {
    "review_id": "EMP-07-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。",
  "coverage_elements": [
    {
      "review_id": "EMP-07-01",
      "element_id": "employment_insurance_1",
      "proposition": "用人单位依法办理参保并缴费",
      "status": "COVERED",
      "evidence_ids": [
        "C0018"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0018"
      ],
      "source_spans": [
        "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
        "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
      ],
      "source_locations": [
        "第十一条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0018"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0018"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0018",
          "quote": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。"
        },
        {
          "clause_id": "C0018",
          "quote": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        }
      ]
    },
    {
      "review_id": "EMP-07-01",
      "element_id": "employment_insurance_2",
      "proposition": "个人应缴部分及代扣代缴",
      "status": "COVERED",
      "evidence_ids": [
        "C0018"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0018"
      ],
      "source_spans": [
        "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
        "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
      ],
      "source_locations": [
        "第十一条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0018"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "gap_risk_level": "中",
      "recommendation_action": "OPTIONAL",
      "residual_gap": "法定个人缴费及代扣代缴机制无需在普通劳动合同中重复列明",
      "risk_relevant": false,
      "evidence_refs": [
        "C0018"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0018",
          "quote": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。"
        },
        {
          "clause_id": "C0018",
          "quote": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_insurance_1",
      "review_id": "EMP-07-01",
      "search_targets": [
        "用人单位依法办理参保并缴费"
      ],
      "query_patterns": [
        "(?:用人单位|甲方|甲乙双方).{0,80}(?:依法|按月).{0,15}(?:缴纳|缴付).{0,60}(?:社会保险|社保)",
        "(?:社会保险|社保)缴纳主体[：:]\\s*[^\\n，；。_]{2,60}(?:公司|企业|事务所)",
        "(?:甲乙双方|用人单位|甲方)(?:按|按照)[^。；\\n]{0,35}规定参加社会保险"
      ],
      "query_semantic_target": "用人单位依法办理参保并缴费",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:甲乙双方|用人单位|甲方)(?:按|按照)[^。；\\n]{0,35}规定参加社会保险"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
          "quote": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
          "original_excerpt": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "source_start": 0,
          "source_end": 26,
          "supports_element_ids": [
            "employment_insurance_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_insurance_2",
      "review_id": "EMP-07-01",
      "search_targets": [
        "个人应缴部分及代扣代缴"
      ],
      "query_patterns": [
        "(?:个人|劳动者|乙方).{0,15}(?:应缴|承担).{0,40}(?:代扣|代缴)|(?:代扣代缴).{0,45}(?:社会保险|社保).{0,15}个人缴费部分"
      ],
      "query_semantic_target": "个人应缴部分及代扣代缴",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:个人|劳动者|乙方).{0,15}(?:应缴|承担).{0,40}(?:代扣|代缴)|(?:代扣代缴).{0,45}(?:社会保险|社保).{0,15}个人缴费部分"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "text": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
          "quote": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
          "original_excerpt": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "source_start": 59,
          "source_end": 88,
          "supports_element_ids": [
            "employment_insurance_2"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0018",
      "location": "第十一条",
      "title": "第十一条",
      "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
      "quote": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
      "original_excerpt": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第十一条"
      ],
      "source_start": 1203,
      "source_end": 1229,
      "supports_element_ids": [
        "employment_insurance_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第十一条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
      "source_span": {
        "start_offset": 1203,
        "end_offset": 1229,
        "raw_text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0018",
        "section": "第十一条",
        "sentence_index": 1,
        "quote": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_insurance_1",
        "employment_insurance_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-07-01",
      "element_ids": [
        "employment_insurance_1",
        "employment_insurance_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0018",
      "location": "第十一条",
      "title": "第十一条",
      "text": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
      "quote": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
      "original_excerpt": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第十一条"
      ],
      "source_start": 1263,
      "source_end": 1291,
      "supports_element_ids": [
        "employment_insurance_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第十一条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
      "source_span": {
        "start_offset": 1263,
        "end_offset": 1291,
        "raw_text": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0018",
        "section": "第十一条",
        "sentence_index": 1,
        "quote": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_insurance_1",
        "employment_insurance_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-07-01",
      "element_ids": [
        "employment_insurance_1",
        "employment_insurance_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-08-01

```json
{
  "rule_id": "EMP-08-01",
  "applicability": {
    "review_id": "EMP-08-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。岗位职业危害情况待核实，未将条件不明的专项义务判为合同缺失。",
  "coverage_elements": [
    {
      "review_id": "EMP-08-01",
      "element_id": "employment_safety_1",
      "proposition": "劳动防护和安全培训",
      "status": "COVERED",
      "evidence_ids": [
        "C0023"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0023"
      ],
      "source_spans": [
        "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
      ],
      "source_locations": [
        "第十五条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0023"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0023"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0023",
          "quote": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        }
      ]
    },
    {
      "element_id": "employment_safety_2",
      "status": "CONDITION_UNRESOLVED",
      "proposition": "核实岗位是否存在职业病危害因素，再确定告知和职业健康保护义务。",
      "required_fact": "职业危害告知和健康保护",
      "conditional_element": true,
      "prerequisite_status": "UNKNOWN",
      "prerequisite_fact": "工作岗位存在职业病危害因素",
      "verification_instruction": "核实岗位是否存在职业病危害因素，再确定告知和职业健康保护义务。",
      "risk_relevant": false,
      "bound_evidence_ids": [],
      "prerequisite_evidence": [],
      "source_clause_ids": [],
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_safety_1",
      "review_id": "EMP-08-01",
      "search_targets": [
        "劳动防护和安全培训"
      ],
      "query_patterns": [
        "(?:提供|配备).{0,60}(?:劳动保护|劳动防护用品|防护用品)|安全(?:生产)?(?:教育和)?培训"
      ],
      "query_semantic_target": "劳动防护和安全培训",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:提供|配备).{0,60}(?:劳动保护|劳动防护用品|防护用品)|安全(?:生产)?(?:教育和)?培训"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。",
          "quote": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。",
          "original_excerpt": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "source_start": 0,
          "source_end": 60,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0023",
      "location": "第十五条",
      "title": "第十五条",
      "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。",
      "quote": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。",
      "original_excerpt": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第十五条"
      ],
      "source_start": 1492,
      "source_end": 1552,
      "supports_element_ids": [
        "employment_safety_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第十五条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。",
      "source_span": {
        "start_offset": 1492,
        "end_offset": 1552,
        "raw_text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0023",
        "section": "第十五条",
        "sentence_index": 1,
        "quote": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_safety_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-08-01",
      "element_ids": [
        "employment_safety_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-09-01

```json
{
  "rule_id": "EMP-09-01",
  "applicability": {
    "review_id": "EMP-09-01",
    "applicable": false,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。",
    "confidence": "medium",
    "status": "NOT_APPLICABLE",
    "machine_reason": "未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。",
    "user_reason": "未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "出现服务期、专项培训安排时适用",
    "triggered": false,
    "condition_text": "出现服务期、专项培训安排时适用"
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "不适用",
  "reason": "未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。",
  "coverage_elements": [],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-10-01

```json
{
  "rule_id": "EMP-10-01",
  "applicability": {
    "review_id": "EMP-10-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖本项核心法定义务；可选完善项未单独作为实际风险：解除通知方式或明确解除日期。",
  "coverage_elements": [
    {
      "review_id": "EMP-10-01",
      "element_id": "employment_exit_1",
      "proposition": "解除终止事由或协商一致",
      "status": "COVERED",
      "evidence_ids": [
        "C0027"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0027"
      ],
      "source_spans": [
        "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
      ],
      "source_locations": [
        "第十八条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0027"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0027"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0027",
          "quote": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        }
      ]
    },
    {
      "review_id": "EMP-10-01",
      "element_id": "employment_exit_2",
      "proposition": "解除通知方式或明确解除日期",
      "status": "MISSING",
      "evidence_ids": [],
      "entailment": "NOT_RELEVANT",
      "verifier_confidence": "medium",
      "reason": "未找到可支撑该元素的合同证据。",
      "claim_id": "",
      "source_clause_ids": [],
      "source_spans": [],
      "source_locations": [],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "未找到可支撑该元素的合同证据。",
      "recommendation_action": "OPTIONAL",
      "residual_gap": "可选完善解除通知方式或未来解除日期确认机制",
      "risk_relevant": false,
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_exit_1",
      "review_id": "EMP-10-01",
      "search_targets": [
        "解除终止事由或协商一致"
      ],
      "query_patterns": [
        "协商一致.{0,20}(?:解除|终止)|(?:解除|终止).{0,40}(?:法定条件|劳动合同法|法定事由)",
        "(?:解除|终止)[^。；\\n]{0,40}(?:按照|依照|根据|按)[^。；\\n]{0,10}法律法规[^。；\\n]{0,10}(?:执行|办理)",
        "(?:派遣.{0,10}(?:届满|期满)|依法退回)[^。；]{0,100}(?:重新派遣|另行安排.{0,20}派遣|依法解除)"
      ],
      "query_semantic_target": "解除终止事由或协商一致",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "协商一致.{0,20}(?:解除|终止)|(?:解除|终止).{0,40}(?:法定条件|劳动合同法|法定事由)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。",
          "quote": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。",
          "original_excerpt": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "source_start": 0,
          "source_end": 49,
          "supports_element_ids": [
            "employment_exit_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_exit_2",
      "review_id": "EMP-10-01",
      "search_targets": [
        "解除通知方式或明确解除日期"
      ],
      "query_patterns": [
        "(?:解除|终止).{0,40}(?:书面通知|\\d{4}年\\d{1,2}月\\d{1,2}日)|提前.{0,8}(?:三十|30)日.{0,8}书面通知"
      ],
      "query_semantic_target": "解除通知方式或明确解除日期",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "NOT_FOUND",
        "contradiction_filter": "NO_ACCEPTED_CANDIDATE"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0027",
      "location": "第十八条",
      "title": "第十八条",
      "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。",
      "quote": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。",
      "original_excerpt": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第十八条"
      ],
      "source_start": 1774,
      "source_end": 1823,
      "supports_element_ids": [
        "employment_exit_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第十八条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。",
      "source_span": {
        "start_offset": 1774,
        "end_offset": 1823,
        "raw_text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0027",
        "section": "第十八条",
        "sentence_index": 1,
        "quote": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_exit_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-10-01",
      "element_ids": [
        "employment_exit_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-11-01

```json
{
  "rule_id": "EMP-11-01",
  "applicability": {
    "review_id": "EMP-11-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。",
  "coverage_elements": [
    {
      "review_id": "EMP-11-01",
      "element_id": "employment_compensation_1",
      "proposition": "经济补偿依法处理、计算依据或正常结算安排",
      "status": "COVERED",
      "evidence_ids": [
        "C0029"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0029"
      ],
      "source_spans": [
        "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
      ],
      "source_locations": [
        "第二十条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0029"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0029"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0029",
          "quote": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        }
      ]
    },
    {
      "review_id": "EMP-11-01",
      "element_id": "employment_compensation_2",
      "proposition": "解除终止后工资及补偿结算期限",
      "status": "COVERED",
      "evidence_ids": [
        "C0029"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0029"
      ],
      "source_spans": [
        "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
      ],
      "source_locations": [
        "第二十条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0029"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "recommendation_action": "OPTIONAL",
      "residual_gap": "可选完善解除终止后工资及经济补偿结算期限",
      "risk_relevant": false,
      "evidence_refs": [
        "C0029"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0029",
          "quote": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_compensation_1",
      "review_id": "EMP-11-01",
      "search_targets": [
        "经济补偿依法处理、计算依据或正常结算安排"
      ],
      "query_patterns": [
        "经济补偿.{0,60}(?:第46条|第47条|第四十六条|第四十七条|\\d+元|工作年限|月工资)|(?:甲方|用人单位)(?:应当|应|须)?依法(?:应当|应)?(?:向乙方|向劳动者)?支付经济补偿",
        "经济补偿[^。；\\n]{0,30}(?:办结|完成|办理完毕)工作交接(?:时|后当日)[^。；\\n]{0,8}(?:支付|结清)",
        "经济补偿[^。；\\n]{0,30}工作交接(?:结束|完成|办结)后[^。；\\n]{0,8}支付"
      ],
      "query_semantic_target": "经济补偿依法处理、计算依据或正常结算安排",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "经济补偿[^。；\\n]{0,30}(?:办结|完成|办理完毕)工作交接(?:时|后当日)[^。；\\n]{0,8}(?:支付|结清)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
          "quote": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
          "original_excerpt": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "source_start": 23,
          "source_end": 51,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_compensation_2",
      "review_id": "EMP-11-01",
      "search_targets": [
        "解除终止后工资及补偿结算期限"
      ],
      "query_patterns": [
        "(?:解除|终止).{0,70}(?:\\d+日内|当日).{0,35}(?:支付|结清)|(?:补偿|工资).{0,40}\\d+日内.{0,20}(?:结清|支付)",
        "经济补偿[^。；\\n]{0,30}(?:办结|完成|办理完毕)工作交接(?:时|后当日)[^。；\\n]{0,8}(?:支付|结清)",
        "经济补偿[^。；\\n]{0,30}工作交接(?:结束|完成|办结)后[^。；\\n]{0,8}支付"
      ],
      "query_semantic_target": "解除终止后工资及补偿结算期限",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "经济补偿[^。；\\n]{0,30}(?:办结|完成|办理完毕)工作交接(?:时|后当日)[^。；\\n]{0,8}(?:支付|结清)"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "本合同于2026年9月10日生效，其中试用期至2026年12月9日止。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
          "quote": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
          "original_excerpt": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "source_start": 23,
          "source_end": 51,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0029",
      "location": "第二十条",
      "title": "第二十条",
      "text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
      "quote": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
      "original_excerpt": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二十条"
      ],
      "source_start": 1914,
      "source_end": 1941,
      "supports_element_ids": [
        "employment_compensation_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二十条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
      "source_span": {
        "start_offset": 1914,
        "end_offset": 1941,
        "raw_text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0029",
        "section": "第二十条",
        "sentence_index": 1,
        "quote": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_compensation_1",
        "employment_compensation_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-11-01",
      "element_ids": [
        "employment_compensation_1",
        "employment_compensation_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0029",
      "location": "第二十条",
      "title": "第二十条",
      "text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
      "quote": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
      "original_excerpt": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二十条"
      ],
      "source_start": 1914,
      "source_end": 1941,
      "supports_element_ids": [
        "employment_compensation_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二十条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
      "source_span": {
        "start_offset": 1914,
        "end_offset": 1941,
        "raw_text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0029",
        "section": "第二十条",
        "sentence_index": 1,
        "quote": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_compensation_1",
        "employment_compensation_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-11-01",
      "element_ids": [
        "employment_compensation_1",
        "employment_compensation_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-12-01

```json
{
  "rule_id": "EMP-12-01",
  "applicability": {
    "review_id": "EMP-12-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。",
  "coverage_elements": [
    {
      "review_id": "EMP-12-01",
      "element_id": "employment_dispute_1",
      "proposition": "劳动争议依法申请劳动仲裁",
      "status": "COVERED",
      "evidence_ids": [
        "C0033"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0033"
      ],
      "source_spans": [
        "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。",
        "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
      ],
      "source_locations": [
        "第二十二条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0033"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0033"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0033",
          "quote": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0033",
          "quote": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_dispute_1",
      "review_id": "EMP-12-01",
      "search_targets": [
        "劳动争议依法申请劳动仲裁"
      ],
      "query_patterns": [
        "(?:劳动争议|劳动合同争议).{0,60}(?:劳动仲裁|劳动(?:人事)?争议仲裁委员会)",
        "申请(?:调解或|调解、)?仲裁",
        "劳动争议仲裁机构[：:]\\s*[^。；\\n]{2,50}劳动人事争议仲裁委员会"
      ],
      "query_semantic_target": "劳动争议依法申请劳动仲裁",
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "SEMANTIC_REQUIREMENT",
      "searched_clause_ids": [
        "C0001",
        "C0002",
        "C0003",
        "C0004",
        "C0005",
        "C0006",
        "C0007",
        "C0008",
        "C0009",
        "C0010",
        "C0011",
        "C0012",
        "C0013",
        "C0014",
        "C0015",
        "C0016",
        "C0017",
        "C0018",
        "C0019",
        "C0020",
        "C0021",
        "C0022",
        "C0023",
        "C0024",
        "C0025",
        "C0026",
        "C0027",
        "C0028",
        "C0029",
        "C0030",
        "C0031",
        "C0032",
        "C0033",
        "C0034",
        "C0035",
        "C0036",
        "C0037",
        "C0038",
        "C0039"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。"
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况"
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室"
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道"
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限"
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。\n本合同于2026年9月10日生效，其中试用期至2026年12月9日止。"
        },
        {
          "clause_id": "C0007",
          "location": "三、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作内容和工作地点"
          ],
          "text": "三、工作内容和工作地点"
        },
        {
          "clause_id": "C0008",
          "location": "第四条",
          "title": "第四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "text": "第四条\n乙方同意根据甲方工作需要，担任软件开发工程师岗位工作。"
        },
        {
          "clause_id": "C0009",
          "location": "第五条",
          "title": "第五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "text": "第五条\n根据甲方的岗位作业特点，乙方的工作区域或工作地点为北京市海淀区中关村东路66号A座1208室。"
        },
        {
          "clause_id": "C0010",
          "location": "第六条",
          "title": "第六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "text": "第六条\n乙方工作应达到以下标准：\n按照甲方研发计划完成软件系统需求分析、程序设计、编码、测试和维护工作；\n按时完成岗位工作任务，并保证交付成果符合甲方规定的技术和质量要求；\n遵守甲方依法制定并公示的研发管理、信息安全、数据安全及劳动纪律制度；\n妥善保管工作中接触的技术资料、源代码及其他工作资料。"
        },
        {
          "clause_id": "C0011",
          "location": "四、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、工作时间和休息休假"
          ],
          "text": "四、工作时间和休息休假"
        },
        {
          "clause_id": "C0012",
          "location": "第七条",
          "title": "第七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "text": "第七条\n甲方安排乙方执行标准工时制度。\n执行标准工时制度的，乙方每天工作时间不超过8小时，每周工作不超过40小时。\n具体工作时间原则上为周一至周五9:00至18:00，其中12:00至13:00为休息时间。\n每周休息日为星期六、星期日。\n甲方安排乙方执行综合计算工时工作制度或者不定时工作制度的，应当事先取得劳动行政部门特殊工时制度的行政许可决定。"
        },
        {
          "clause_id": "C0013",
          "location": "第八条",
          "title": "第八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "text": "第八条\n甲方对乙方实行的休假制度有：国家法定节假日、带薪年休假、婚假、丧假、产假、陪产假、育儿假以及法律法规规定的其他休假。"
        },
        {
          "clause_id": "C0014",
          "location": "五、劳动报酬",
          "title": "劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、劳动报酬"
          ],
          "text": "五、劳动报酬"
        },
        {
          "clause_id": "C0015",
          "location": "第九条",
          "title": "第九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "text": "第九条\n甲方每月10日前以银行转账形式支付乙方上月工资，月工资为人民币15000元。\n乙方在试用期期间的工资为人民币12000元。\n甲乙双方对工资的其他约定：\n甲方根据乙方工作绩效、公司经营状况及依法制定的绩效管理制度，可以向乙方发放绩效奖金及年终奖金。绩效奖金及年终奖金不属于固定工资。"
        },
        {
          "clause_id": "C0016",
          "location": "第十条",
          "title": "第十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "text": "第十条\n甲方生产工作任务不足使乙方待工的，甲方按照国家及北京市有关工资支付规定向乙方支付待岗期间工资或者生活费。"
        },
        {
          "clause_id": "C0017",
          "location": "六、社会保险及其他保险福利待遇",
          "title": "社会保险及其他保险福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、社会保险及其他保险福利待遇"
          ],
          "text": "六、社会保险及其他保险福利待遇"
        },
        {
          "clause_id": "C0018",
          "location": "第十一条",
          "title": "第十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "text": "第十一条\n甲乙双方按国家和北京市的规定参加社会保险。\n甲方为乙方办理有关社会保险手续，并依法承担相应社会保险缴费义务。\n依法应由乙方个人承担的社会保险费用，由甲方依法代扣代缴。"
        },
        {
          "clause_id": "C0019",
          "location": "第十二条",
          "title": "第十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十二条"
          ],
          "text": "第十二条\n乙方患病或非因工负伤的医疗待遇按国家、北京市有关规定执行。\n甲方按照国家及北京市有关工资支付和医疗期规定支付乙方病假工资。"
        },
        {
          "clause_id": "C0020",
          "location": "第十三条",
          "title": "第十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十三条"
          ],
          "text": "第十三条\n乙方患职业病或因工负伤的待遇按国家和北京市的有关规定执行。"
        },
        {
          "clause_id": "C0021",
          "location": "第十四条",
          "title": "第十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十四条"
          ],
          "text": "第十四条\n甲方为乙方提供以下福利待遇：\n工作日午餐补贴人民币20元/日；\n每年度一次员工健康体检；\n法定节假日福利；\n根据甲方福利制度提供通讯、交通等补贴。"
        },
        {
          "clause_id": "C0022",
          "location": "七、劳动保护、劳动条件和职业危害防护",
          "title": "劳动保护、劳动条件和职业危害防护",
          "section_type": "正式合同条款",
          "heading_path": [
            "七、劳动保护、劳动条件和职业危害防护"
          ],
          "text": "七、劳动保护、劳动条件和职业危害防护"
        },
        {
          "clause_id": "C0023",
          "location": "第十五条",
          "title": "第十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十五条"
          ],
          "text": "第十五条\n甲方根据生产岗位的需要，按照国家有关劳动安全、卫生的规定为乙方配备必要的安全防护措施，发放必要的劳动保护用品。"
        },
        {
          "clause_id": "C0024",
          "location": "第十六条",
          "title": "第十六条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "text": "第十六条\n甲方根据国家有关法律、法规，建立安全生产制度；乙方应当严格遵守甲方的劳动安全制度，严禁违章作业，防止劳动过程中的事故，减少职业危害。\n甲方应根据乙方岗位情况对乙方进行必要的劳动安全和职业健康教育培训。"
        },
        {
          "clause_id": "C0025",
          "location": "第十七条",
          "title": "第十七条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十七条"
          ],
          "text": "第十七条\n甲方应当建立、健全职业病防治责任制度，加强对职业病防治的管理，提高职业病防治水平。\n乙方岗位如存在依法需要告知的职业病危害因素，甲方应依法履行告知、职业健康检查及其他职业病防护义务。"
        },
        {
          "clause_id": "C0026",
          "location": "八、劳动合同的解除、终止和经济补偿",
          "title": "劳动合同的解除、终止和经济补偿",
          "section_type": "正式合同条款",
          "heading_path": [
            "八、劳动合同的解除、终止和经济补偿"
          ],
          "text": "八、劳动合同的解除、终止和经济补偿"
        },
        {
          "clause_id": "C0027",
          "location": "第十八条",
          "title": "第十八条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十八条"
          ],
          "text": "第十八条\n甲乙双方解除、终止劳动合同应当依照《中华人民共和国劳动合同法》和国家及地方有关规定执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第十九条",
          "title": "第十九条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十九条"
          ],
          "text": "第十九条\n甲方应当在解除或者终止本合同时，为乙方出具解除或者终止劳动合同的证明，并在十五日内为乙方办理档案和社会保险关系转移手续。"
        },
        {
          "clause_id": "C0029",
          "location": "第二十条",
          "title": "第二十条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十条"
          ],
          "text": "第二十条\n乙方应当按照双方约定，办理工作交接。\n依法应当支付经济补偿的，甲方在办结工作交接时依法支付。"
        },
        {
          "clause_id": "C0030",
          "location": "九、当事人约定的其他内容",
          "title": "当事人约定的其他内容",
          "section_type": "正式合同条款",
          "heading_path": [
            "九、当事人约定的其他内容"
          ],
          "text": "九、当事人约定的其他内容"
        },
        {
          "clause_id": "C0031",
          "location": "第二十一条",
          "title": "第二十一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "text": "第二十一条\n甲乙双方约定本合同增加以下内容：\n甲方依法制定并向乙方公示或者告知的规章制度，乙方应当遵守。\n乙方联系方式、居住地址等发生变化的，应及时通知甲方。\n乙方因履行工作职责接触甲方商业秘密、技术秘密或者其他保密信息的，应依法承担保密义务。\n如甲方为乙方提供专项培训费用进行专业技术培训，需要约定服务期的，由双方另行签订专项培训及服务期协议。\n如乙方属于依法可以约定竞业限制的人员且确有必要约定竞业限制的，由双方另行签订竞业限制协议。\n本条约定不得排除或者限制乙方依法享有的劳动权利。"
        },
        {
          "clause_id": "C0032",
          "location": "十、劳动争议处理及其它",
          "title": "劳动争议处理及其它",
          "section_type": "正式合同条款",
          "heading_path": [
            "十、劳动争议处理及其它"
          ],
          "text": "十、劳动争议处理及其它"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        {
          "clause_id": "C0034",
          "location": "第二十三条",
          "title": "第二十三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "text": "第二十三条\n本合同的附件如下：\n岗位职责说明书；\n员工规章制度签收确认书。"
        },
        {
          "clause_id": "C0035",
          "location": "第二十四条",
          "title": "第二十四条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十四条"
          ],
          "text": "第二十四条\n本合同未尽事宜或与今后国家、北京市有关规定相悖的，按有关规定执行。"
        },
        {
          "clause_id": "C0036",
          "location": "第二十五条",
          "title": "第二十五条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "第二十五条\n本合同一式两份，甲乙双方各执一份，具有同等法律效力。"
        },
        {
          "clause_id": "C0037",
          "location": "甲方（公章）：北京远航智能科技有限公司",
          "title": "甲方（公章）：北京远航智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "甲方（公章）：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0038",
          "location": "乙方（签字或盖章）：赵晨",
          "title": "乙方（签字或盖章）：赵晨",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十五条"
          ],
          "text": "乙方（签字或盖章）：赵晨\n签订日期：2026年9月8日"
        },
        {
          "clause_id": "C0039",
          "location": "附件",
          "title": "附件一：岗位职责说明书",
          "section_type": "附件",
          "heading_path": [
            "附件一：岗位职责说明书"
          ],
          "text": "附件一：岗位职责说明书\n员工姓名：赵晨\n岗位名称：软件开发工程师\n部门：研发中心\n主要工作职责：\n负责企业软件系统的需求分析、设计、开发、测试及维护；\n根据项目计划完成软件模块开发及技术文档编写；\n参与软件系统性能优化、故障排查和技术改进；\n配合产品、测试及其他部门完成项目交付；\n遵守公司源代码、数据和信息安全管理制度；\n完成与本岗位职责相关的其他合理工作任务。\n乙方确认已阅读并理解上述岗位职责。\n乙方签字：赵晨\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:劳动争议|劳动合同争议).{0,60}(?:劳动仲裁|劳动(?:人事)?争议仲裁委员会)",
            "申请(?:调解或|调解、)?仲裁"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=2; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "text": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "申请(?:调解或|调解、)?仲裁"
          ],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=1; contextual_hits=0",
            "threshold": "PASS",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "无固定期限劳动合同\n甲方：北京远航智能科技有限公司\n乙方：赵晨\n签订日期：2026年9月8日\n根据《中华人民共和国劳动法》、《中华人民共和国劳动合同法》和有关法律、法规，甲乙双方经平等自愿、协商一致签订本合同，共同遵守本合同所列条款。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0002",
          "location": "一、劳动合同双方当事人基本情况",
          "title": "劳动合同双方当事人基本情况",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同双方当事人基本情况"
          ],
          "text": "一、劳动合同双方当事人基本情况",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0003",
          "location": "第一条",
          "title": "第一条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "text": "第一条\n甲方：北京远航智能科技有限公司\n法定代表人（主要负责人）或委托代理人：陈志远\n注册地址：北京市海淀区中关村东路66号A座1208室\n经营地址：北京市海淀区中关村东路66号A座1208室",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0004",
          "location": "第二条",
          "title": "第二条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "text": "第二条\n乙方：赵晨\n性别：男\n户籍类型：非农业\n居民身份证号码：110108199304186518\n其他有效证件名称：无\n证件号码：无\n在甲方工作起始时间：2026年9月10日\n家庭住址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n在京居住地址：北京市朝阳区望京西路38号院5号楼902室\n邮政编码：100102\n户口所在地：北京市海淀区中关村街道",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0005",
          "location": "二、劳动合同期限",
          "title": "劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、劳动合同期限"
          ],
          "text": "二、劳动合同期限",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        },
        {
          "clause_id": "C0006",
          "location": "第三条",
          "title": "第三条",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "text": "第三条\n本合同为无固定期限劳动合同。",
          "score": 0.0,
          "accepted": false,
          "reject_reason": "REJECTED: 未命中语义目标或上下文谓词。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=0; semantic_hits=0; contextual_hits=0",
            "threshold": "REJECT",
            "contradiction_filter": "PASS"
          }
        }
      ],
      "stage_results": {
        "normalize": "PASS",
        "rerank": "PASS",
        "threshold": "PASS",
        "contradiction_filter": "PASS"
      },
      "searched_document_hash": "d52ca519f5435ef161271d7f01d1ef1fbaba8737adda678cbb48a2d253ad7df2",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。",
          "quote": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。",
          "original_excerpt": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "source_start": 0,
          "source_end": 68,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0033",
          "location": "第二十二条",
          "title": "第二十二条",
          "text": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
          "quote": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
          "original_excerpt": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十二条"
          ],
          "source_start": 68,
          "source_end": 98,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0033",
      "location": "第二十二条",
      "title": "第二十二条",
      "text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。",
      "quote": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。",
      "original_excerpt": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二十二条"
      ],
      "source_start": 2212,
      "source_end": 2280,
      "supports_element_ids": [
        "employment_dispute_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二十二条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
      "source_span": {
        "start_offset": 2212,
        "end_offset": 2280,
        "raw_text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0033",
        "section": "第二十二条",
        "sentence_index": 1,
        "quote": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_dispute_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-12-01",
      "element_ids": [
        "employment_dispute_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0033",
      "location": "第二十二条",
      "title": "第二十二条",
      "text": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
      "quote": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
      "original_excerpt": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二十二条"
      ],
      "source_start": 2281,
      "source_end": 2310,
      "supports_element_ids": [
        "employment_dispute_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二十二条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第二十二条\n双方因履行本合同发生争议，当事人可以向甲方劳动争议调解委员会申请调解；调解不成的，可以依法向劳动人事争议仲裁委员会申请仲裁。\n当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
      "source_span": {
        "start_offset": 2281,
        "end_offset": 2310,
        "raw_text": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0033",
        "section": "第二十二条",
        "sentence_index": 1,
        "quote": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "当事人一方也可以直接依法向劳动人事争议仲裁委员会申请仲裁。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_dispute_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-12-01",
      "element_ids": [
        "employment_dispute_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    }
  ],
  "termination_classification": []
}
```

## EMP-13-01

```json
{
  "rule_id": "EMP-13-01",
  "applicability": {
    "review_id": "EMP-13-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-13-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021",
      "C0022",
      "C0023",
      "C0024",
      "C0025",
      "C0026",
      "C0027",
      "C0028",
      "C0029",
      "C0030",
      "C0031",
      "C0032",
      "C0033",
      "C0034",
      "C0035",
      "C0036",
      "C0037",
      "C0038",
      "C0039"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-16-01

```json
{
  "rule_id": "EMP-16-01",
  "applicability": {
    "review_id": "EMP-16-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-16-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021",
      "C0022",
      "C0023",
      "C0024",
      "C0025",
      "C0026",
      "C0027",
      "C0028",
      "C0029",
      "C0030",
      "C0031",
      "C0032",
      "C0033",
      "C0034",
      "C0035",
      "C0036",
      "C0037",
      "C0038",
      "C0039"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-14-01

```json
{
  "rule_id": "EMP-14-01",
  "applicability": {
    "review_id": "EMP-14-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-14-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021",
      "C0022",
      "C0023",
      "C0024",
      "C0025",
      "C0026",
      "C0027",
      "C0028",
      "C0029",
      "C0030",
      "C0031",
      "C0032",
      "C0033",
      "C0034",
      "C0035",
      "C0036",
      "C0037",
      "C0038",
      "C0039"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## NC-01-01

```json
{
  "rule_id": "NC-01-01",
  "applicability": {
    "review_id": "NC-01-01",
    "applicable": false,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
    "confidence": "high",
    "status": "NOT_APPLICABLE",
    "machine_reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
    "user_reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "SCENARIO:employment_noncompete_scope",
    "triggered": false,
    "condition_text": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。"
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "不适用",
  "reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
  "coverage_elements": [],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## NC-02-01

```json
{
  "rule_id": "NC-02-01",
  "applicability": {
    "review_id": "NC-02-01",
    "applicable": false,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
    "confidence": "medium",
    "status": "NOT_APPLICABLE",
    "machine_reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
    "user_reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "出现离职、解除、终止安排时适用",
    "triggered": false,
    "condition_text": "出现离职、解除、终止安排时适用"
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "不适用",
  "reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
  "coverage_elements": [],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## NC-03-01

```json
{
  "rule_id": "NC-03-01",
  "applicability": {
    "review_id": "NC-03-01",
    "applicable": false,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
    "confidence": "high",
    "status": "NOT_APPLICABLE",
    "machine_reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
    "user_reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "SCENARIO:employment_noncompete_adverse",
    "triggered": false,
    "condition_text": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。"
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "不适用",
  "reason": "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "NC-03-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021",
      "C0022",
      "C0023",
      "C0024",
      "C0025",
      "C0026",
      "C0027",
      "C0028",
      "C0029",
      "C0030",
      "C0031",
      "C0032",
      "C0033",
      "C0034",
      "C0035",
      "C0036",
      "C0037",
      "C0038",
      "C0039"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "不适用"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## EMP-IP-01

```json
{
  "rule_id": "EMP-IP-01",
  "applicability": {
    "review_id": "EMP-IP-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "专项清单及合同场景适用。",
    "confidence": "high",
    "status": "APPLICABLE",
    "machine_reason": "专项清单及合同场景适用。",
    "user_reason": "该审查事项适用于当前合同。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "通过",
  "reason": "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。",
  "coverage_elements": [],
  "negative_clause_check": {
    "review_id": "EMP-IP-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "NO_ADVERSE_CLAUSE_FOUND",
    "description": "未发现对应禁止性/不利约定。",
    "searched_scope": [
      "C0001",
      "C0002",
      "C0003",
      "C0004",
      "C0005",
      "C0006",
      "C0007",
      "C0008",
      "C0009",
      "C0010",
      "C0011",
      "C0012",
      "C0013",
      "C0014",
      "C0015",
      "C0016",
      "C0017",
      "C0018",
      "C0019",
      "C0020",
      "C0021",
      "C0022",
      "C0023",
      "C0024",
      "C0025",
      "C0026",
      "C0027",
      "C0028",
      "C0029",
      "C0030",
      "C0031",
      "C0032",
      "C0033",
      "C0034",
      "C0035",
      "C0036",
      "C0037",
      "C0038",
      "C0039"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "通过"
  },
  "element_absence_searches": [],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## release_quality_gate

```json
{
  "status": "REPORT_READY",
  "failures": [],
  "priority_consistency_verification": {
    "executed": true,
    "high_finding_count": 0,
    "core_priority_count": 0,
    "consistency": "CONSISTENT",
    "explanations": [],
    "needs_recalibration": false
  },
  "context_consistency": {
    "status": "PASS",
    "failures": [],
    "contract_type": "labor",
    "domain_pack": "priority-domain-1.0"
  },
  "gate_results": {
    "PASS_EVIDENCE_PROVENANCE_GATE": "PASS",
    "PARTIAL_ELEMENT_NARRATIVE_GATE": "PASS",
    "COVERAGE_SENTENCE_CONSISTENCY_GATE": "PASS",
    "ELEMENT_STATUS_CONTRADICTION": "PASS",
    "EVIDENCE_MONOTONICITY_VIOLATION": "PASS",
    "FINDING_EVIDENCE_GATE": "PASS",
    "CROSS_LAYER_CONSISTENCY_GATE": "PASS",
    "DEFAULT_LAW_COMPLETENESS_GATE": "PASS",
    "DEFAULT_LAW_EFFECTIVE_GAP_GATE": "PASS",
    "NARRATIVE_ELEMENT_CONSISTENCY_GATE": "PASS",
    "NARRATIVE_TRUTH_GATE": "PASS",
    "PRIORITY_CONSISTENCY_GATE": "PASS",
    "SIGNABILITY_GATE": "PASS",
    "CONFIDENCE_VALIDATION_GATE": "PASS",
    "DOMAIN_SUBTYPE_GATE": "PASS",
    "DOMAIN_REVIEW_ISOLATION_GATE": "PASS",
    "DOMAIN_MATERIAL_COVERAGE_GATE": "PASS",
    "TRANSACTION_STRUCTURE_GATE": "PASS",
    "FRAMEWORK_DOMAIN_GATE": "PASS",
    "ORDER_RELATION_GATE": "PASS",
    "DYNAMIC_QUANTITY_GATE": "PASS",
    "PRICE_MECHANISM_GATE": "PASS",
    "ALTERNATIVE_SATISFACTION_GATE": "PASS",
    "FALSE_RISK_EXISTENCE_GATE": "PASS",
    "FACT_REGISTRY_SNAPSHOT_CONSISTENCY": "PASS",
    "FACT_REGISTRY_CONFLICTING_FACT": "PASS",
    "CROSS_REVIEW_FACT_CONFLICT": "PASS",
    "FACT_TRUTH_OVERRIDE_VIOLATION": "PASS",
    "FACT_CONSUMER_MAPPING_MISSING": "PASS",
    "RISK_EVIDENCE_MISMATCH": "PASS",
    "REVIEW_EVIDENCE_ELEMENT_MISMATCH": "PASS",
    "APPLICABILITY_PRECONDITION_GATE": "PASS",
    "SHARED_CLAIM_CONSISTENCY_GATE": "PASS",
    "FINDING_PRECONDITION_GATE": "PASS",
    "REPORT_CONTEXT_GATE": "PASS",
    "REPORT_TRANSACTION_TRUTH_GATE": "PASS",
    "CROSS_REVIEW_CONSISTENCY_GATE": "PASS",
    "RECOMMENDATION_NON_DEGRADATION_GATE": "PASS",
    "COMMON_REVIEW_SATISFACTION_GATE": "PASS",
    "ELEMENT_IDENTITY_CONTRADICTION_GATE": "PASS",
    "PRODUCT_APPLICABILITY_GATE": "PASS",
    "SHARED_CLAIM_REUSE_GATE": "PASS",
    "FINDING_INDEPENDENCE_GATE": "PASS",
    "TECHNOLOGY_TRANSACTION_CONSISTENCY": "NOT_APPLICABLE",
    "PERSPECTIVE_DOMAIN_CONSISTENCY_GATE": "PASS",
    "PATENT_TRANSFER_QUALITY_GATE": "NOT_APPLICABLE",
    "PRODUCTION_FACT_POLARITY_GATE": "PASS",
    "RECOMMENDATION_SOURCE_UNMAPPED": "PASS",
    "RECOMMENDATION_ELEMENT_LEAKAGE": "PASS",
    "RECOMMENDATION_COVERED_ELEMENT_REINTRODUCED": "PASS",
    "RECOMMENDATION_PLACEHOLDER_TEXT": "PASS",
    "RECOMMENDATION_FINAL_DISPOSITION_MISMATCH": "PASS",
    "CLIENT_INTEREST_GATE": "PASS",
    "RISK_STATISTICS_INVARIANT": "PASS",
    "FINAL_DISPOSITION_INVARIANT": "PASS",
    "FORMAL_RECOMMENDATION_FINAL_DISPOSITION_INVARIANT": "PASS",
    "RECOMMENDATION_OWNERSHIP_INVARIANT": "PASS",
    "HIGH_NON_MUST_CHANGE_REASON_INVARIANT": "PASS",
    "OPTIONAL_IMPROVEMENT_VISIBILITY_INVARIANT": "PASS",
    "ACTIONABLE_RECOMMENDATION_COMPLETENESS_INVARIANT": "PASS",
    "LEGAL_AUTHORITY_DEDUP_GATE": "PASS",
    "LEGAL_AUTHORITY_SELECTION_GATE": "PASS",
    "CITATION_ENTAILMENT_GATE": "PASS",
    "LEGAL_DEFAULT_LAW_CONSISTENCY_GATE": "PASS",
    "ATOMIC_LEGAL_ELEMENT_GATE": "PASS",
    "DEFAULT_LAW_NARRATIVE_TRUTH_GATE": "PASS",
    "NOT_APPLICABLE_NARRATIVE_GATE": "PASS",
    "NOT_APPLICABLE_GAP_GATE": "PASS",
    "REVIEW_POLARITY_NARRATIVE_GATE": "PASS",
    "NEGATIVE_CHECK_PASS_GATE": "PASS",
    "CROSS_REVIEW_SHARED_CLAIM_GATE": "PASS",
    "NARRATIVE_EVIDENCE_GATE": "PASS",
    "EXACT_ELEMENT_REPORT_INVARIANT": "PASS",
    "PRODUCTION_INTERNAL_TOKEN_GATE": "PASS",
    "DEFAULT_LAW_PROVENANCE_GATE": "PASS",
    "RECOMMENDATION_SINGLE_SOURCE_GATE": "PASS",
    "RECOMMENDATION_CROSS_RENDERER_CONSISTENCY_GATE": "PASS",
    "REPORT_TEXT_VALIDATION": "PASS",
    "REPORT_DISPOSITION_PROJECTION_INVARIANT": "PASS",
    "EVIDENCE_BUNDLE_ENTAILMENT_GATE": "PASS",
    "RECOMMENDATION_SEMANTIC_BINDING_GATE": "PASS",
    "SUMMARY_DETAIL_RISK_ID_GATE": "PASS",
    "ISSUE_TYPE_NARRATIVE_GATE": "PASS",
    "OPTIONAL_REPORT_COUNT_GATE": "PASS",
    "REPORT_ROLE_PLACEHOLDER_GATE": "PASS",
    "ACTIONABLE_RECOMMENDATION_VISIBILITY_GATE": "PASS",
    "CLAIM_EVIDENCE_COVERAGE_GATE": "PASS",
    "EVIDENCE_FACT_ROLE_GATE": "PASS",
    "SINGLE_EVIDENCE_SOURCE_GATE": "PASS",
    "EVIDENCE_BUNDLE_RENDER_GATE": "PASS",
    "APPLICABILITY_DISPLAY_CONSISTENCY_GATE": "PASS",
    "ISSUE_TYPE_CONSISTENCY_GATE": "PASS",
    "PARTIAL_MISSING_ELEMENT_GATE": "PASS",
    "SUMMARY_TRUNCATION_DISCLOSURE_GATE": "PASS",
    "TECHNICAL_REPORT_PLACEHOLDER_GATE": "PASS",
    "FINAL_RISK_EVIDENCE_BUNDLE_GATE": "PASS",
    "EVIDENCE_ITEM_UNIQUENESS_GATE": "PASS",
    "CLAUSE_NODE_CONSISTENCY_GATE": "PASS",
    "MISSING_RISK_ABSENCE_EVIDENCE_GATE": "PASS",
    "COVERAGE_RISK_ACTION_CONSISTENCY_GATE": "PASS",
    "PATENT_ROLE_TERMINOLOGY_GATE": "PASS",
    "DUPLICATE_TEMPLATE_PHRASE_GATE": "PASS",
    "EVIDENCE_PROPOSITION_MATCH_GATE": "PASS",
    "PASS_EVIDENCE_PROPOSITION_MATCH_GATE": "PASS",
    "CANONICAL_RISK_COVERAGE_INVARIANT": "PASS",
    "CONSULTING_REPORT_CONTEXT_GATE": "PASS",
    "TERMINOLOGY_CONSISTENCY_GATE": "PASS",
    "APPLICABILITY_AND_EVIDENCE_BOUNDARY": "PASS"
  },
  "blocking_rules": [],
  "blocking_stage": "",
  "blocking_entities": [],
  "blocking_reasons": [],
  "post_render_status": "REPORT_READY"
}
```