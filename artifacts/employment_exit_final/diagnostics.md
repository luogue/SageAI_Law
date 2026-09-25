# 劳动合同逐项证据诊断

输入文件：95 劳动合同.docx
输入 SHA256：8d557cd26ce6b978aff539008b32f97b0e7243ebc84c5aa4353cd6620cd93a37
normalized SHA256：edc5e046ed1a825d459c76509ad9676c00cc21f88e24a1366da20bcb00a4f974

| rule_id | 最终状态 | 理由 |
|---|---|---|
| EMP-01-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-02-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-03-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-15-01 | RISK | 发现试用期超过法定上限或重复约定的直接约定，存在效力或履行风险，需结合适用法律及具体事实核验。 |
| EMP-04-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-05-01 | RISK | 发现与本项法定保护相冲突的直接不利约定。 |
| EMP-06-01 | RISK | 发现与本项法定保护相冲突的直接不利约定。 |
| EMP-07-01 | RISK | 发现与本项法定保护相冲突的直接不利约定。 |
| EMP-08-01 | MISSING | 未找到明确约定：劳动防护和安全培训。专项要素的适用前提待核实，未将条件不明的义务判为合同缺失。 |
| EMP-09-01 | N/A | 未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。 |
| EMP-10-01 | RISK | 发现与本项法定保护相冲突的直接不利约定。 |
| EMP-11-01 | MISSING | 未找到明确约定：经济补偿依法处理、计算依据或正常结算安排。 |
| EMP-12-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-13-01 | RISK | 发现免除或放弃法定社会保险义务的直接约定，存在效力或履行风险，需结合适用法律及具体事实核验。 |
| EMP-16-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| EMP-14-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| NC-01-01 | PARTIAL | 未找到明确约定：人员范围及实际接触秘密、明确约定竞业地域范围。 |
| NC-02-01 | RISK | 发现与本项法定保护相冲突的直接不利约定。 |
| NC-03-01 | RISK | 发现竞业范围或补偿明显不当的直接约定，存在效力或履行风险，需结合适用法律及具体事实核验。 |
| EMP-IP-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |

## 全部 SEARCH_AUDIT NOT FOUND

```json
[
  {
    "rule_id": "EMP-08-01",
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
      "C0039",
      "C0040"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "text": "劳动合同（通用）",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "text": "一、劳动合同期限",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0011",
        "location": "四、劳动报酬",
        "text": "四、劳动报酬",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0012",
        "location": "第五条",
        "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0013",
        "location": "第六条",
        "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0014",
        "location": "第七条",
        "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0015",
        "location": "五、社会保险和福利待遇",
        "text": "五、社会保险和福利待遇",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0016",
        "location": "第八条",
        "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0017",
        "location": "第九条",
        "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0018",
        "location": "六、职业培训和劳动保护",
        "text": "六、职业培训和劳动保护",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0019",
        "location": "第十条",
        "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0020",
        "location": "第十一条",
        "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0021",
        "location": "七、劳动合同的变更、解除和终止",
        "text": "七、劳动合同的变更、解除和终止",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0022",
        "location": "第十二条",
        "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0023",
        "location": "第十三条",
        "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0024",
        "location": "第十四条",
        "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0025",
        "location": "八、保密及竞业限制",
        "text": "八、保密及竞业限制",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0026",
        "location": "第十五条",
        "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0027",
        "location": "第十六条",
        "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0028",
        "location": "九、知识产权",
        "text": "九、知识产权",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0029",
        "location": "第十七条",
        "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0030",
        "location": "十、双方约定的其他事项",
        "text": "十、双方约定的其他事项",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0031",
        "location": "第十八条",
        "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0032",
        "location": "第十九条",
        "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0033",
        "location": "第二十条",
        "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0034",
        "location": "十一、劳动争议处理",
        "text": "十一、劳动争议处理",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0035",
        "location": "第二十一条",
        "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0036",
        "location": "十二、其他",
        "text": "十二、其他",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0037",
        "location": "第二十二条",
        "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0038",
        "location": "第二十三条",
        "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0039",
        "location": "甲方（盖章）：深圳市启明智能科技有限公司",
        "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0040",
        "location": "乙方（签字）：陈泽宇",
        "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "text": "劳动合同（通用）",
        "quote": "劳动合同（通用）",
        "original_excerpt": "劳动合同（通用）",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 141,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "title": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 195,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "title": "劳动合同期限",
        "text": "一、劳动合同期限",
        "quote": "一、劳动合同期限",
        "original_excerpt": "一、劳动合同期限",
        "section_type": "正式合同条款",
        "heading_path": [
          "一、劳动合同期限"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 0,
        "source_end": 21,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
        "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 21,
        "source_end": 51,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 51,
        "source_end": 86,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "title": "工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "quote": "二、工作内容和工作地点",
        "original_excerpt": "二、工作内容和工作地点",
        "section_type": "正式合同条款",
        "heading_path": [
          "二、工作内容和工作地点"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。",
        "quote": "第二条\n乙方工作岗位为软件开发工程师。",
        "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 0,
        "source_end": 19,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 19,
        "source_end": 113,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "乙方主要工作地点为深圳市南山区。",
        "quote": "乙方主要工作地点为深圳市南山区。",
        "original_excerpt": "乙方主要工作地点为深圳市南山区。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 113,
        "source_end": 130,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 130,
        "source_end": 197,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 197,
        "source_end": 239,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "title": "工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "quote": "三、工作时间和休息休假",
        "original_excerpt": "三、工作时间和休息休假",
        "section_type": "正式合同条款",
        "heading_path": [
          "三、工作时间和休息休假"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。",
        "quote": "第三条\n乙方实行标准工时工作制。",
        "original_excerpt": "第三条\n乙方实行标准工时工作制。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 0,
        "source_end": 16,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 16,
        "source_end": 48,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 48,
        "source_end": 84,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 84,
        "source_end": 134,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "甲方可根据项目情况安排乙方调休。",
        "quote": "甲方可根据项目情况安排乙方调休。",
        "original_excerpt": "甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 134,
        "source_end": 151,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "title": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条"
        ],
        "source_start": 0,
        "source_end": 32,
        "supports_element_ids": [
          "employment_safety_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      }
    ],
    "candidate_count": 64,
    "stage_results": {
      "normalize": "CANONICAL_CANDIDATE",
      "threshold": "NOT_FOUND"
    },
    "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-11-01",
    "element_id": "employment_compensation_1",
    "review_id": "EMP-11-01",
    "search_targets": [
      "经济补偿依法处理、计算依据或正常结算安排"
    ],
    "query_patterns": [
      "经济补偿.{0,60}(?:第46条|第47条|第四十六条|第四十七条|\\d+元|工作年限|月工资)|(?:甲方|用人单位)(?:应当|应|须)?依法(?:应当|应)?(?:向乙方|向劳动者)?支付经济补偿",
      "依法(?:需要|应当|应)?[^。；\\n]{0,20}支付经济补偿[^。；\\n]{0,15}(?:甲方|用人单位)(?:按照|依照|按)法律规定支付",
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
      "C0039",
      "C0040"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "text": "劳动合同（通用）",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "text": "一、劳动合同期限",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0011",
        "location": "四、劳动报酬",
        "text": "四、劳动报酬",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0012",
        "location": "第五条",
        "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0013",
        "location": "第六条",
        "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0014",
        "location": "第七条",
        "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0015",
        "location": "五、社会保险和福利待遇",
        "text": "五、社会保险和福利待遇",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0016",
        "location": "第八条",
        "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0017",
        "location": "第九条",
        "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0018",
        "location": "六、职业培训和劳动保护",
        "text": "六、职业培训和劳动保护",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0019",
        "location": "第十条",
        "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0020",
        "location": "第十一条",
        "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0021",
        "location": "七、劳动合同的变更、解除和终止",
        "text": "七、劳动合同的变更、解除和终止",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0022",
        "location": "第十二条",
        "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0023",
        "location": "第十三条",
        "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0024",
        "location": "第十四条",
        "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0025",
        "location": "八、保密及竞业限制",
        "text": "八、保密及竞业限制",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0026",
        "location": "第十五条",
        "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0027",
        "location": "第十六条",
        "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0028",
        "location": "九、知识产权",
        "text": "九、知识产权",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0029",
        "location": "第十七条",
        "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0030",
        "location": "十、双方约定的其他事项",
        "text": "十、双方约定的其他事项",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0031",
        "location": "第十八条",
        "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0032",
        "location": "第十九条",
        "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0033",
        "location": "第二十条",
        "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0034",
        "location": "十一、劳动争议处理",
        "text": "十一、劳动争议处理",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0035",
        "location": "第二十一条",
        "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0036",
        "location": "十二、其他",
        "text": "十二、其他",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0037",
        "location": "第二十二条",
        "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0038",
        "location": "第二十三条",
        "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0039",
        "location": "甲方（盖章）：深圳市启明智能科技有限公司",
        "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0040",
        "location": "乙方（签字）：陈泽宇",
        "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "text": "劳动合同（通用）",
        "quote": "劳动合同（通用）",
        "original_excerpt": "劳动合同（通用）",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 141,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "title": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 195,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "title": "劳动合同期限",
        "text": "一、劳动合同期限",
        "quote": "一、劳动合同期限",
        "original_excerpt": "一、劳动合同期限",
        "section_type": "正式合同条款",
        "heading_path": [
          "一、劳动合同期限"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 0,
        "source_end": 21,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
        "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 21,
        "source_end": 51,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 51,
        "source_end": 86,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "title": "工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "quote": "二、工作内容和工作地点",
        "original_excerpt": "二、工作内容和工作地点",
        "section_type": "正式合同条款",
        "heading_path": [
          "二、工作内容和工作地点"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。",
        "quote": "第二条\n乙方工作岗位为软件开发工程师。",
        "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 0,
        "source_end": 19,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 19,
        "source_end": 113,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "乙方主要工作地点为深圳市南山区。",
        "quote": "乙方主要工作地点为深圳市南山区。",
        "original_excerpt": "乙方主要工作地点为深圳市南山区。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 113,
        "source_end": 130,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 130,
        "source_end": 197,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 197,
        "source_end": 239,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "title": "工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "quote": "三、工作时间和休息休假",
        "original_excerpt": "三、工作时间和休息休假",
        "section_type": "正式合同条款",
        "heading_path": [
          "三、工作时间和休息休假"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。",
        "quote": "第三条\n乙方实行标准工时工作制。",
        "original_excerpt": "第三条\n乙方实行标准工时工作制。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 0,
        "source_end": 16,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 16,
        "source_end": 48,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 48,
        "source_end": 84,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 84,
        "source_end": 134,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "甲方可根据项目情况安排乙方调休。",
        "quote": "甲方可根据项目情况安排乙方调休。",
        "original_excerpt": "甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 134,
        "source_end": 151,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "title": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条"
        ],
        "source_start": 0,
        "source_end": 32,
        "supports_element_ids": [
          "employment_compensation_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      }
    ],
    "candidate_count": 64,
    "stage_results": {
      "normalize": "CANONICAL_CANDIDATE",
      "threshold": "NOT_FOUND"
    },
    "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "EMP-11-01",
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
      "C0039",
      "C0040"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "text": "劳动合同（通用）",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "text": "一、劳动合同期限",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0011",
        "location": "四、劳动报酬",
        "text": "四、劳动报酬",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0012",
        "location": "第五条",
        "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0013",
        "location": "第六条",
        "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0014",
        "location": "第七条",
        "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0015",
        "location": "五、社会保险和福利待遇",
        "text": "五、社会保险和福利待遇",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0016",
        "location": "第八条",
        "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0017",
        "location": "第九条",
        "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0018",
        "location": "六、职业培训和劳动保护",
        "text": "六、职业培训和劳动保护",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0019",
        "location": "第十条",
        "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0020",
        "location": "第十一条",
        "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0021",
        "location": "七、劳动合同的变更、解除和终止",
        "text": "七、劳动合同的变更、解除和终止",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0022",
        "location": "第十二条",
        "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0023",
        "location": "第十三条",
        "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0024",
        "location": "第十四条",
        "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0025",
        "location": "八、保密及竞业限制",
        "text": "八、保密及竞业限制",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0026",
        "location": "第十五条",
        "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0027",
        "location": "第十六条",
        "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0028",
        "location": "九、知识产权",
        "text": "九、知识产权",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0029",
        "location": "第十七条",
        "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0030",
        "location": "十、双方约定的其他事项",
        "text": "十、双方约定的其他事项",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0031",
        "location": "第十八条",
        "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0032",
        "location": "第十九条",
        "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0033",
        "location": "第二十条",
        "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0034",
        "location": "十一、劳动争议处理",
        "text": "十一、劳动争议处理",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0035",
        "location": "第二十一条",
        "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0036",
        "location": "十二、其他",
        "text": "十二、其他",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0037",
        "location": "第二十二条",
        "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0038",
        "location": "第二十三条",
        "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0039",
        "location": "甲方（盖章）：深圳市启明智能科技有限公司",
        "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0040",
        "location": "乙方（签字）：陈泽宇",
        "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "text": "劳动合同（通用）",
        "quote": "劳动合同（通用）",
        "original_excerpt": "劳动合同（通用）",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 141,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "title": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 195,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "title": "劳动合同期限",
        "text": "一、劳动合同期限",
        "quote": "一、劳动合同期限",
        "original_excerpt": "一、劳动合同期限",
        "section_type": "正式合同条款",
        "heading_path": [
          "一、劳动合同期限"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 0,
        "source_end": 21,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
        "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 21,
        "source_end": 51,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 51,
        "source_end": 86,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "title": "工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "quote": "二、工作内容和工作地点",
        "original_excerpt": "二、工作内容和工作地点",
        "section_type": "正式合同条款",
        "heading_path": [
          "二、工作内容和工作地点"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。",
        "quote": "第二条\n乙方工作岗位为软件开发工程师。",
        "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 0,
        "source_end": 19,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 19,
        "source_end": 113,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "乙方主要工作地点为深圳市南山区。",
        "quote": "乙方主要工作地点为深圳市南山区。",
        "original_excerpt": "乙方主要工作地点为深圳市南山区。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 113,
        "source_end": 130,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 130,
        "source_end": 197,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 197,
        "source_end": 239,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "title": "工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "quote": "三、工作时间和休息休假",
        "original_excerpt": "三、工作时间和休息休假",
        "section_type": "正式合同条款",
        "heading_path": [
          "三、工作时间和休息休假"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。",
        "quote": "第三条\n乙方实行标准工时工作制。",
        "original_excerpt": "第三条\n乙方实行标准工时工作制。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 0,
        "source_end": 16,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 16,
        "source_end": 48,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 48,
        "source_end": 84,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 84,
        "source_end": 134,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "甲方可根据项目情况安排乙方调休。",
        "quote": "甲方可根据项目情况安排乙方调休。",
        "original_excerpt": "甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 134,
        "source_end": 151,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "title": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条"
        ],
        "source_start": 0,
        "source_end": 32,
        "supports_element_ids": [
          "employment_compensation_2"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      }
    ],
    "candidate_count": 64,
    "stage_results": {
      "normalize": "CANONICAL_CANDIDATE",
      "threshold": "NOT_FOUND"
    },
    "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NC-01-01",
    "element_id": "employment_noncompete_scope_1",
    "review_id": "NC-01-01",
    "search_targets": [
      "人员范围及实际接触秘密"
    ],
    "query_patterns": [
      "(?:劳动者|乙方).{0,40}(?:实际接触|知悉|掌握).{0,35}(?:商业秘密|保密事项)"
    ],
    "query_semantic_target": "人员范围及实际接触秘密",
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
      "C0039",
      "C0040"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "text": "劳动合同（通用）",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "text": "一、劳动合同期限",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0011",
        "location": "四、劳动报酬",
        "text": "四、劳动报酬",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0012",
        "location": "第五条",
        "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0013",
        "location": "第六条",
        "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0014",
        "location": "第七条",
        "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0015",
        "location": "五、社会保险和福利待遇",
        "text": "五、社会保险和福利待遇",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0016",
        "location": "第八条",
        "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0017",
        "location": "第九条",
        "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0018",
        "location": "六、职业培训和劳动保护",
        "text": "六、职业培训和劳动保护",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0019",
        "location": "第十条",
        "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0020",
        "location": "第十一条",
        "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0021",
        "location": "七、劳动合同的变更、解除和终止",
        "text": "七、劳动合同的变更、解除和终止",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0022",
        "location": "第十二条",
        "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0023",
        "location": "第十三条",
        "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0024",
        "location": "第十四条",
        "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0025",
        "location": "八、保密及竞业限制",
        "text": "八、保密及竞业限制",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0026",
        "location": "第十五条",
        "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0027",
        "location": "第十六条",
        "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0028",
        "location": "九、知识产权",
        "text": "九、知识产权",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0029",
        "location": "第十七条",
        "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0030",
        "location": "十、双方约定的其他事项",
        "text": "十、双方约定的其他事项",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0031",
        "location": "第十八条",
        "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0032",
        "location": "第十九条",
        "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0033",
        "location": "第二十条",
        "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0034",
        "location": "十一、劳动争议处理",
        "text": "十一、劳动争议处理",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0035",
        "location": "第二十一条",
        "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0036",
        "location": "十二、其他",
        "text": "十二、其他",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0037",
        "location": "第二十二条",
        "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0038",
        "location": "第二十三条",
        "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0039",
        "location": "甲方（盖章）：深圳市启明智能科技有限公司",
        "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0040",
        "location": "乙方（签字）：陈泽宇",
        "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "text": "劳动合同（通用）",
        "quote": "劳动合同（通用）",
        "original_excerpt": "劳动合同（通用）",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 141,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "title": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 195,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "title": "劳动合同期限",
        "text": "一、劳动合同期限",
        "quote": "一、劳动合同期限",
        "original_excerpt": "一、劳动合同期限",
        "section_type": "正式合同条款",
        "heading_path": [
          "一、劳动合同期限"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 0,
        "source_end": 21,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
        "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 21,
        "source_end": 51,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 51,
        "source_end": 86,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "title": "工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "quote": "二、工作内容和工作地点",
        "original_excerpt": "二、工作内容和工作地点",
        "section_type": "正式合同条款",
        "heading_path": [
          "二、工作内容和工作地点"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。",
        "quote": "第二条\n乙方工作岗位为软件开发工程师。",
        "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 0,
        "source_end": 19,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 19,
        "source_end": 113,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "乙方主要工作地点为深圳市南山区。",
        "quote": "乙方主要工作地点为深圳市南山区。",
        "original_excerpt": "乙方主要工作地点为深圳市南山区。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 113,
        "source_end": 130,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 130,
        "source_end": 197,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 197,
        "source_end": 239,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "title": "工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "quote": "三、工作时间和休息休假",
        "original_excerpt": "三、工作时间和休息休假",
        "section_type": "正式合同条款",
        "heading_path": [
          "三、工作时间和休息休假"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。",
        "quote": "第三条\n乙方实行标准工时工作制。",
        "original_excerpt": "第三条\n乙方实行标准工时工作制。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 0,
        "source_end": 16,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 16,
        "source_end": 48,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 48,
        "source_end": 84,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 84,
        "source_end": 134,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "甲方可根据项目情况安排乙方调休。",
        "quote": "甲方可根据项目情况安排乙方调休。",
        "original_excerpt": "甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 134,
        "source_end": 151,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "title": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条"
        ],
        "source_start": 0,
        "source_end": 32,
        "supports_element_ids": [
          "employment_noncompete_scope_1"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      }
    ],
    "candidate_count": 64,
    "stage_results": {
      "normalize": "CANONICAL_CANDIDATE",
      "threshold": "NOT_FOUND"
    },
    "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NC-01-01",
    "element_id": "employment_noncompete_scope_3",
    "review_id": "NC-01-01",
    "search_targets": [
      "明确约定竞业地域范围"
    ],
    "query_patterns": [
      "竞业(?:限制|禁止).{0,25}(?:地域|地区|区域)范围\\s*(?:为|包括|限于|：|:)[^。；_]{2,80}"
    ],
    "query_semantic_target": "明确约定竞业地域范围",
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
      "C0039",
      "C0040"
    ],
    "search_corpus_chunks": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "text": "劳动合同（通用）",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "text": "一、劳动合同期限",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0011",
        "location": "四、劳动报酬",
        "text": "四、劳动报酬",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0012",
        "location": "第五条",
        "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0013",
        "location": "第六条",
        "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0014",
        "location": "第七条",
        "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0015",
        "location": "五、社会保险和福利待遇",
        "text": "五、社会保险和福利待遇",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0016",
        "location": "第八条",
        "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0017",
        "location": "第九条",
        "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0018",
        "location": "六、职业培训和劳动保护",
        "text": "六、职业培训和劳动保护",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0019",
        "location": "第十条",
        "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0020",
        "location": "第十一条",
        "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0021",
        "location": "七、劳动合同的变更、解除和终止",
        "text": "七、劳动合同的变更、解除和终止",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0022",
        "location": "第十二条",
        "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0023",
        "location": "第十三条",
        "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0024",
        "location": "第十四条",
        "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0025",
        "location": "八、保密及竞业限制",
        "text": "八、保密及竞业限制",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0026",
        "location": "第十五条",
        "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0027",
        "location": "第十六条",
        "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0028",
        "location": "九、知识产权",
        "text": "九、知识产权",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0029",
        "location": "第十七条",
        "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0030",
        "location": "十、双方约定的其他事项",
        "text": "十、双方约定的其他事项",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0031",
        "location": "第十八条",
        "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0032",
        "location": "第十九条",
        "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0033",
        "location": "第二十条",
        "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0034",
        "location": "十一、劳动争议处理",
        "text": "十一、劳动争议处理",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0035",
        "location": "第二十一条",
        "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0036",
        "location": "十二、其他",
        "text": "十二、其他",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0037",
        "location": "第二十二条",
        "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0038",
        "location": "第二十三条",
        "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0039",
        "location": "甲方（盖章）：深圳市启明智能科技有限公司",
        "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      },
      {
        "clause_id": "C0040",
        "location": "乙方（签字）：陈泽宇",
        "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
        "section_type": "正式合同条款"
      }
    ],
    "top_k_candidates": [
      {
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "text": "劳动合同（通用）",
        "quote": "劳动合同（通用）",
        "original_excerpt": "劳动合同（通用）",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0002",
        "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 141,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0003",
        "location": "乙方（劳动者）：陈泽宇",
        "title": "乙方（劳动者）：陈泽宇",
        "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "source_start": 0,
        "source_end": 195,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0004",
        "location": "一、劳动合同期限",
        "title": "劳动合同期限",
        "text": "一、劳动合同期限",
        "quote": "一、劳动合同期限",
        "original_excerpt": "一、劳动合同期限",
        "section_type": "正式合同条款",
        "heading_path": [
          "一、劳动合同期限"
        ],
        "source_start": 0,
        "source_end": 8,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 0,
        "source_end": 21,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
        "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 21,
        "source_end": 51,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一条"
        ],
        "source_start": 51,
        "source_end": 86,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0006",
        "location": "二、工作内容和工作地点",
        "title": "工作内容和工作地点",
        "text": "二、工作内容和工作地点",
        "quote": "二、工作内容和工作地点",
        "original_excerpt": "二、工作内容和工作地点",
        "section_type": "正式合同条款",
        "heading_path": [
          "二、工作内容和工作地点"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "第二条\n乙方工作岗位为软件开发工程师。",
        "quote": "第二条\n乙方工作岗位为软件开发工程师。",
        "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 0,
        "source_end": 19,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 19,
        "source_end": 113,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "乙方主要工作地点为深圳市南山区。",
        "quote": "乙方主要工作地点为深圳市南山区。",
        "original_excerpt": "乙方主要工作地点为深圳市南山区。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 113,
        "source_end": 130,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 130,
        "source_end": 197,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0007",
        "location": "第二条",
        "title": "第二条",
        "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二条"
        ],
        "source_start": 197,
        "source_end": 239,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0008",
        "location": "三、工作时间和休息休假",
        "title": "工作时间和休息休假",
        "text": "三、工作时间和休息休假",
        "quote": "三、工作时间和休息休假",
        "original_excerpt": "三、工作时间和休息休假",
        "section_type": "正式合同条款",
        "heading_path": [
          "三、工作时间和休息休假"
        ],
        "source_start": 0,
        "source_end": 11,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "第三条\n乙方实行标准工时工作制。",
        "quote": "第三条\n乙方实行标准工时工作制。",
        "original_excerpt": "第三条\n乙方实行标准工时工作制。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 0,
        "source_end": 16,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 16,
        "source_end": 48,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 48,
        "source_end": 84,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 84,
        "source_end": 134,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0009",
        "location": "第三条",
        "title": "第三条",
        "text": "甲方可根据项目情况安排乙方调休。",
        "quote": "甲方可根据项目情况安排乙方调休。",
        "original_excerpt": "甲方可根据项目情况安排乙方调休。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三条"
        ],
        "source_start": 134,
        "source_end": 151,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      },
      {
        "clause_id": "C0010",
        "location": "第四条",
        "title": "第四条",
        "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四条"
        ],
        "source_start": 0,
        "source_end": 32,
        "supports_element_ids": [
          "employment_noncompete_scope_3"
        ],
        "source_type": "CONTRACT_TEXT",
        "accepted": false,
        "score": 0.0,
        "threshold": "ALL_REQUIRED_RELATIONS",
        "relation_slots": [],
        "matched_patterns": [],
        "rejected_patterns": [],
        "decision_function": "review_v2.lease_semantics.supports",
        "result": "NOT_FOUND"
      }
    ],
    "candidate_count": 64,
    "stage_results": {
      "normalize": "CANONICAL_CANDIDATE",
      "threshold": "NOT_FOUND"
    },
    "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
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
        "SRC-834c6ba16675be2ee6ae",
        "SRC-834c6ba16675be2ee6ae"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0002"
      ],
      "source_spans": [
        "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236"
      ],
      "source_locations": [
        "甲方（用人单位）：深圳市启明智能科技有限公司"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0002"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-834c6ba16675be2ee6ae",
        "SRC-834c6ba16675be2ee6ae"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-834c6ba16675be2ee6ae",
        "SRC-834c6ba16675be2ee6ae"
      ],
      "bound_evidence_ids": [
        "SRC-834c6ba16675be2ee6ae",
        "SRC-834c6ba16675be2ee6ae"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0002",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236"
        }
      ]
    },
    {
      "review_id": "EMP-01-01",
      "element_id": "employment_identity_2",
      "proposition": "劳动者姓名与身份证明",
      "status": "COVERED",
      "evidence_ids": [
        "SRC-6bc859043b529f2615bb"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0003"
      ],
      "source_spans": [
        "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。"
      ],
      "source_locations": [
        "乙方（劳动者）：陈泽宇"
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
        "SRC-6bc859043b529f2615bb"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-6bc859043b529f2615bb"
      ],
      "bound_evidence_ids": [
        "SRC-6bc859043b529f2615bb"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0003",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。"
        }
      ]
    },
    {
      "review_id": "EMP-01-01",
      "element_id": "employment_identity_name",
      "proposition": "用人单位名称",
      "status": "COVERED",
      "evidence_ids": [
        "SRC-834c6ba16675be2ee6ae",
        "SRC-834c6ba16675be2ee6ae",
        "SRC-4961fb9c50893adbae91"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0002"
      ],
      "source_spans": [
        "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236"
      ],
      "source_locations": [
        "甲方（用人单位）：深圳市启明智能科技有限公司"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0002"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-834c6ba16675be2ee6ae",
        "SRC-834c6ba16675be2ee6ae",
        "SRC-4961fb9c50893adbae91"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-834c6ba16675be2ee6ae",
        "SRC-834c6ba16675be2ee6ae",
        "SRC-4961fb9c50893adbae91"
      ],
      "bound_evidence_ids": [
        "SRC-834c6ba16675be2ee6ae",
        "SRC-834c6ba16675be2ee6ae",
        "SRC-4961fb9c50893adbae91"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0002",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236"
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
        "甲方(?:[（(][^）)\\n]{1,15}[）)])?[：:]\\s*[^\\n，；。_]{2,80}(?:(?!乙方)[\\s\\S]){0,200}(?:注册地址|经营地址|住所)[：:]\\s*[^\\n，；。_]{3,80}",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "(?:用人单位|劳务派遣单位)[）)]?\\s*(?:名称|姓名)?\\s*[：:]\\s*[^\\n，；。_]{2,60}(?:公司|企业|事务所)(?:(?!乙方|劳动者|用工单位).){0,300}(?:住所|地址|注册地|注册登记地|实际经营地)[：:]\\s*[^\\n，；。_]{3,60}",
            "甲方(?:[（(][^）)\\n]{1,15}[）)])?[：:]\\s*[^\\n，；。_]{2,80}(?:(?!乙方)[\\s\\S]){0,200}(?:注册地址|经营地址|住所)[：:]\\s*[^\\n，；。_]{3,80}"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_identity_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
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
        "乙方(?:[（(][^）)\\n]{1,15}[）)])?[：:]\\s*[\\u4e00-\\u9fff·]{2,12}(?:(?!甲方)[\\s\\S]){0,180}(?:居民身份证号码|身份证号码)[：:]\\s*[0-9Xx]{18}",
        "乙方[：:]?\\s*[\\u4e00-\\u9fff·]{2,12}[\\s\\S]{0,180}(?:居民身份证号码|身份证号码|证件号码)[：:]\\s*[0-9Xx]{8,18}",
        "乙方(?:[（(][^）)\\n]{1,15}[）)])?\\s*[：:]\\s*[\\u4e00-\\u9fff·]{2,12}(?:(?!甲方)[\\s\\S]){0,180}身份证号(?:码)?\\s*[：:]\\s*[0-9Xx*＊]{15,18}"
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "劳动者[）)]?\\s*(?:名称|姓名)?\\s*[：:]\\s*[\\u4e00-\\u9fff·]{2,12}[^。；]{0,160}(?:居民身份证号码|身份证(?:号码)?|证件号码)[：:]?\\s*[0-9Xx]{8,18}",
            "乙方(?:[（(][^）)\\n]{1,15}[）)])?[：:]\\s*[\\u4e00-\\u9fff·]{2,12}(?:(?!甲方)[\\s\\S]){0,180}(?:居民身份证号码|身份证号码)[：:]\\s*[0-9Xx]{18}",
            "乙方(?:[（(][^）)\\n]{1,15}[）)])?\\s*[：:]\\s*[\\u4e00-\\u9fff·]{2,12}(?:(?!甲方)[\\s\\S]){0,180}身份证号(?:码)?\\s*[：:]\\s*[0-9Xx*＊]{15,18}"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 86,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 239,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "quote": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 151,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "title": "劳动报酬",
          "text": "四、劳动报酬",
          "quote": "四、劳动报酬",
          "original_excerpt": "四、劳动报酬",
          "section_type": "正式合同条款",
          "heading_path": [
            "四、劳动报酬"
          ],
          "source_start": 0,
          "source_end": 6,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "title": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "quote": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "original_excerpt": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五条"
          ],
          "source_start": 0,
          "source_end": 153,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "title": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "quote": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "original_excerpt": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "source_start": 0,
          "source_end": 25,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "title": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "quote": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "original_excerpt": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第七条"
          ],
          "source_start": 0,
          "source_end": 53,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "title": "社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "quote": "五、社会保险和福利待遇",
          "original_excerpt": "五、社会保险和福利待遇",
          "section_type": "正式合同条款",
          "heading_path": [
            "五、社会保险和福利待遇"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "title": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "quote": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "original_excerpt": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "source_start": 0,
          "source_end": 111,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "title": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "quote": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "original_excerpt": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第九条"
          ],
          "source_start": 0,
          "source_end": 27,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "title": "职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "quote": "六、职业培训和劳动保护",
          "original_excerpt": "六、职业培训和劳动保护",
          "section_type": "正式合同条款",
          "heading_path": [
            "六、职业培训和劳动保护"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "title": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "quote": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "original_excerpt": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十条"
          ],
          "source_start": 0,
          "source_end": 75,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "title": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "quote": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "original_excerpt": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十一条"
          ],
          "source_start": 0,
          "source_end": 56,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 40,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_identity_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
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
        "甲方(?:[（(][^）)\\n]{1,20}[）)])?\\s*[：:]\\s*[^\\n，；。_]{2,60}",
        "甲方\\s*(?:名称|为|系)\\s*[：:]?\\s*[^\\n，；。_]{2,60}(?:大学|学院|医院|公司|研究所|中心)",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "甲方(?:[（(][^）)\\n]{1,20}[）)])?\\s*[：:]\\s*[^\\n，；。_]{2,60}",
            "(?:用人单位|劳务派遣单位)[）)]?\\s*(?:名称)?\\s*[：:]\\s*[^\\n，；。_]{2,60}"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "title": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "quote": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "original_excerpt": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "source_start": 0,
          "source_end": 52,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "甲方(?:[（(][^）)\\n]{1,20}[）)])?\\s*[：:]\\s*[^\\n，；。_]{2,60}"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "title": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "quote": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "original_excerpt": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十三条"
          ],
          "source_start": 0,
          "source_end": 52,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0002",
      "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
      "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
      "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 9,
      "source_end": 150,
      "supports_element_ids": [
        "employment_identity_1",
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "甲方（用人单位）：深圳市启明智能科技有限公司",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "source_span": {
        "start_offset": 9,
        "end_offset": 150,
        "raw_text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0002",
        "section": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "sentence_index": 1,
        "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 9,
          "end_offset": 150,
          "raw_text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0002",
          "clause_sha256": "34d3817a107c88cec155450fd3ed069e642a065af6fa7432b42f597bb7ddf838",
          "local_start": 0,
          "local_end": 141,
          "locator": "甲方（用人单位）：深圳市启明智能科技有限公司"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_1",
        "employment_identity_name"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_1",
        "employment_identity_name"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-834c6ba16675be2ee6ae",
      "quoted_text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0002",
        "clause_sha256": "34d3817a107c88cec155450fd3ed069e642a065af6fa7432b42f597bb7ddf838",
        "local_start": 0,
        "local_end": 141,
        "locator": "甲方（用人单位）：深圳市启明智能科技有限公司"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_identity_1",
          "employment_identity_name"
        ]
      },
      "supported_propositions": [
        "用人单位住所",
        "用人单位名称"
      ],
      "support_summary": "证明合同已约定相关合同要素、相关合同要素。"
    },
    {
      "clause_id": "C0002",
      "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
      "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
      "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 9,
      "source_end": 150,
      "supports_element_ids": [
        "employment_identity_1",
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "甲方（用人单位）：深圳市启明智能科技有限公司",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "source_span": {
        "start_offset": 9,
        "end_offset": 150,
        "raw_text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0002",
        "section": "甲方（用人单位）：深圳市启明智能科技有限公司",
        "sentence_index": 1,
        "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 9,
          "end_offset": 150,
          "raw_text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0002",
          "clause_sha256": "34d3817a107c88cec155450fd3ed069e642a065af6fa7432b42f597bb7ddf838",
          "local_start": 0,
          "local_end": 141,
          "locator": "甲方（用人单位）：深圳市启明智能科技有限公司"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_1",
        "employment_identity_name"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_1",
        "employment_identity_name"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-834c6ba16675be2ee6ae",
      "quoted_text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0002",
        "clause_sha256": "34d3817a107c88cec155450fd3ed069e642a065af6fa7432b42f597bb7ddf838",
        "local_start": 0,
        "local_end": 141,
        "locator": "甲方（用人单位）：深圳市启明智能科技有限公司"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_identity_1",
          "employment_identity_name"
        ]
      },
      "supported_propositions": [
        "用人单位住所",
        "用人单位名称"
      ],
      "support_summary": "证明合同已约定相关合同要素、相关合同要素。"
    },
    {
      "clause_id": "C0003",
      "location": "乙方（劳动者）：陈泽宇",
      "title": "乙方（劳动者）：陈泽宇",
      "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
      "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
      "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 151,
      "source_end": 346,
      "supports_element_ids": [
        "employment_identity_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "乙方（劳动者）：陈泽宇",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
      "source_span": {
        "start_offset": 151,
        "end_offset": 346,
        "raw_text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0003",
        "section": "乙方（劳动者）：陈泽宇",
        "sentence_index": 1,
        "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 151,
          "end_offset": 346,
          "raw_text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0003",
          "clause_sha256": "991255ccff81ac6404f739363436a682807b52db56d159db95c3282e2aa9998c",
          "local_start": 0,
          "local_end": 195,
          "locator": "乙方（劳动者）：陈泽宇"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_2"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-6bc859043b529f2615bb",
      "quoted_text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0003",
        "clause_sha256": "991255ccff81ac6404f739363436a682807b52db56d159db95c3282e2aa9998c",
        "local_start": 0,
        "local_end": 195,
        "locator": "乙方（劳动者）：陈泽宇"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_identity_2"
        ]
      },
      "supported_propositions": [
        "劳动者姓名与身份证明"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0039",
      "location": "甲方（盖章）：深圳市启明智能科技有限公司",
      "title": "甲方（盖章）：深圳市启明智能科技有限公司",
      "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
      "quote": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
      "original_excerpt": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二十三条"
      ],
      "source_start": 2495,
      "source_end": 2547,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Contextual retrieval evidence does not directly support a resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "甲方（盖章）：深圳市启明智能科技有限公司",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
      "source_span": {
        "start_offset": 2495,
        "end_offset": 2547,
        "raw_text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0039",
        "section": "甲方（盖章）：深圳市启明智能科技有限公司",
        "sentence_index": 1,
        "quote": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 2495,
          "end_offset": 2547,
          "raw_text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0039",
          "clause_sha256": "edec8c0bed2de5cdad4994b80dc8a3aa0071e363f533fc4379dc0ace6dbbf0f6",
          "local_start": 0,
          "local_end": 52,
          "locator": "甲方（盖章）：深圳市启明智能科技有限公司"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_name"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 0.0,
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_name"
      ],
      "support_type": "CONTEXTUAL",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-4961fb9c50893adbae91",
      "quoted_text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0039",
        "clause_sha256": "edec8c0bed2de5cdad4994b80dc8a3aa0071e363f533fc4379dc0ace6dbbf0f6",
        "local_start": 0,
        "local_end": 52,
        "locator": "甲方（盖章）：深圳市启明智能科技有限公司"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_identity_name"
        ]
      },
      "supported_propositions": [
        "用人单位名称"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
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
        "SRC-e143c432b366a6e4f3b2"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0005"
      ],
      "source_spans": [
        "第一条\n甲乙双方约定采用固定期限劳动合同。"
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
        "C0005"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-e143c432b366a6e4f3b2"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-e143c432b366a6e4f3b2"
      ],
      "bound_evidence_ids": [
        "SRC-e143c432b366a6e4f3b2"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。"
        }
      ]
    },
    {
      "review_id": "EMP-02-01",
      "element_id": "employment_term_start",
      "proposition": "生效或起始日期",
      "status": "COVERED",
      "evidence_ids": [
        "SRC-80bfc61b0dd1c9588fbd",
        "SRC-80bfc61b0dd1c9588fbd"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0005"
      ],
      "source_spans": [
        "合同期限自2026年9月15日起至2028年9月14日止。"
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
        "C0005"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-80bfc61b0dd1c9588fbd",
        "SRC-80bfc61b0dd1c9588fbd"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-80bfc61b0dd1c9588fbd",
        "SRC-80bfc61b0dd1c9588fbd"
      ],
      "bound_evidence_ids": [
        "SRC-80bfc61b0dd1c9588fbd",
        "SRC-80bfc61b0dd1c9588fbd"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。"
        }
      ]
    },
    {
      "review_id": "EMP-02-01",
      "element_id": "employment_term_end",
      "proposition": "终止日期",
      "status": "COVERED",
      "evidence_ids": [
        "SRC-80bfc61b0dd1c9588fbd",
        "SRC-80bfc61b0dd1c9588fbd"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0005"
      ],
      "source_spans": [
        "合同期限自2026年9月15日起至2028年9月14日止。"
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
        "C0005"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-80bfc61b0dd1c9588fbd",
        "SRC-80bfc61b0dd1c9588fbd"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-80bfc61b0dd1c9588fbd",
        "SRC-80bfc61b0dd1c9588fbd"
      ],
      "bound_evidence_ids": [
        "SRC-80bfc61b0dd1c9588fbd",
        "SRC-80bfc61b0dd1c9588fbd"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。"
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "(?:固定期限|无固定期限|以完成.{1,30}工作任务为期限)"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_term_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 95,
          "selection_reason": "DIRECT_SEMANTIC_SUPPORT"
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "(?:本合同|劳动合同|合同期限)(?:于|自|生效日期[为：:]?|起始日期[为：:]?)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
            "(?:本合同|合同期限)\\s*[：:]?\\s*自?(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_term_start"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    },
    {
      "element_id": "employment_term_end",
      "review_id": "EMP-02-01",
      "search_targets": [
        "终止日期"
      ],
      "query_patterns": [
        "^\\s*自(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "(?:本合同|合同期限)\\s*[：:]?\\s*自?(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?",
        "(?:终止日期|到期日期|合同至|期限至)[为：:]?\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
      ],
      "query_semantic_target": "终止日期",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "(?:本合同|合同期限)\\s*[：:]?\\s*自?(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?起?\\s*(?:至|到)\\s*(\\d{4})[年/-](\\d{1,2})[月/-](\\d{1,2})日?"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_term_end"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0005",
      "location": "第一条",
      "title": "第一条",
      "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
      "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
      "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第一条"
      ],
      "source_start": 356,
      "source_end": 377,
      "supports_element_ids": [
        "employment_term_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 95,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第一条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "source_span": {
        "start_offset": 356,
        "end_offset": 377,
        "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0005",
        "section": "第一条",
        "sentence_index": 1,
        "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 356,
          "end_offset": 377,
          "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0005",
          "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
          "local_start": 0,
          "local_end": 21,
          "locator": "第一条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_term_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-02-01",
      "element_ids": [
        "employment_term_1"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-e143c432b366a6e4f3b2",
      "quoted_text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0005",
        "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
        "local_start": 0,
        "local_end": 21,
        "locator": "第一条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_term_1"
        ]
      },
      "supported_propositions": [
        "期限类型"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0005",
      "location": "第一条",
      "title": "第一条",
      "text": "合同期限自2026年9月15日起至2028年9月14日止。",
      "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
      "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第一条"
      ],
      "source_start": 378,
      "source_end": 407,
      "supports_element_ids": [
        "employment_term_start",
        "employment_term_end"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第一条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "source_span": {
        "start_offset": 378,
        "end_offset": 407,
        "raw_text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0005",
        "section": "第一条",
        "sentence_index": 1,
        "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 378,
          "end_offset": 407,
          "raw_text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0005",
          "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
          "local_start": 22,
          "local_end": 51,
          "locator": "第一条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_term_start",
        "employment_term_end"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-02-01",
      "element_ids": [
        "employment_term_start",
        "employment_term_end"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-80bfc61b0dd1c9588fbd",
      "quoted_text": "合同期限自2026年9月15日起至2028年9月14日止。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0005",
        "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
        "local_start": 22,
        "local_end": 51,
        "locator": "第一条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_term_start",
          "employment_term_end"
        ]
      },
      "supported_propositions": [
        "生效或起始日期",
        "终止日期"
      ],
      "support_summary": "证明合同已约定相关合同要素、相关合同要素。"
    },
    {
      "clause_id": "C0005",
      "location": "第一条",
      "title": "第一条",
      "text": "合同期限自2026年9月15日起至2028年9月14日止。",
      "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
      "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第一条"
      ],
      "source_start": 378,
      "source_end": 407,
      "supports_element_ids": [
        "employment_term_start",
        "employment_term_end"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第一条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "source_span": {
        "start_offset": 378,
        "end_offset": 407,
        "raw_text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0005",
        "section": "第一条",
        "sentence_index": 1,
        "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 378,
          "end_offset": 407,
          "raw_text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0005",
          "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
          "local_start": 22,
          "local_end": 51,
          "locator": "第一条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_term_start",
        "employment_term_end"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-02-01",
      "element_ids": [
        "employment_term_start",
        "employment_term_end"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-80bfc61b0dd1c9588fbd",
      "quoted_text": "合同期限自2026年9月15日起至2028年9月14日止。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0005",
        "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
        "local_start": 22,
        "local_end": 51,
        "locator": "第一条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_term_start",
          "employment_term_end"
        ]
      },
      "supported_propositions": [
        "生效或起始日期",
        "终止日期"
      ],
      "support_summary": "证明合同已约定相关合同要素、相关合同要素。"
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
    "applicability_state": "CONDITIONAL_TRIGGERED",
    "premise_evidence": [],
    "premise_fact_ids": [],
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
        "SRC-2f1080c8421252494beb"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0005"
      ],
      "source_spans": [
        "试用期自2026年9月15日起至2026年12月14日止，共3个月。"
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
        "C0005"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-2f1080c8421252494beb"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-2f1080c8421252494beb"
      ],
      "bound_evidence_ids": [
        "SRC-2f1080c8421252494beb"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。"
        }
      ]
    },
    {
      "review_id": "EMP-03-01",
      "element_id": "employment_probation_2",
      "proposition": "试用期工资标准",
      "status": "COVERED",
      "evidence_ids": [
        "SRC-3bd67fced777e7442f91"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0013"
      ],
      "source_spans": [
        "第六条\n乙方试用期工资为人民币14,000元/月。"
      ],
      "source_locations": [
        "第六条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0013"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-3bd67fced777e7442f91"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-3bd67fced777e7442f91"
      ],
      "bound_evidence_ids": [
        "SRC-3bd67fced777e7442f91"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0013",
          "quote": "第六条\n乙方试用期工资为人民币14,000元/月。"
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "试用期[：:]?\\s*自?\\d{4}[年/-]\\d{1,2}[月/-]\\d{1,2}日?起?至\\d{4}[年/-]\\d{1,2}[月/-]\\d{1,2}日?"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_probation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0013",
          "location": "第六条",
          "title": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "quote": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "original_excerpt": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "source_start": 0,
          "source_end": 25,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "试用期(?:期间的|月)?(?:正常工作时间)?工资[^\\n。；]{0,12}\\d+(?:\\.\\d+)?\\s*元"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0013",
          "location": "第六条",
          "title": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "quote": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "original_excerpt": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第六条"
          ],
          "source_start": 0,
          "source_end": 25,
          "supports_element_ids": [
            "employment_probation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0005",
      "location": "第一条",
      "title": "第一条",
      "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第一条"
      ],
      "source_start": 408,
      "source_end": 442,
      "supports_element_ids": [
        "employment_probation_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第一条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "source_span": {
        "start_offset": 408,
        "end_offset": 442,
        "raw_text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0005",
        "section": "第一条",
        "sentence_index": 1,
        "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 408,
          "end_offset": 442,
          "raw_text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0005",
          "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
          "local_start": 52,
          "local_end": 86,
          "locator": "第一条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_probation_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-03-01",
      "element_ids": [
        "employment_probation_1"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-2f1080c8421252494beb",
      "quoted_text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0005",
        "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
        "local_start": 52,
        "local_end": 86,
        "locator": "第一条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_probation_1"
        ]
      },
      "supported_propositions": [
        "试用期长度"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0013",
      "location": "第六条",
      "title": "第六条",
      "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
      "quote": "第六条\n乙方试用期工资为人民币14,000元/月。",
      "original_excerpt": "第六条\n乙方试用期工资为人民币14,000元/月。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第六条"
      ],
      "source_start": 1053,
      "source_end": 1078,
      "supports_element_ids": [
        "employment_probation_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第六条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第六条\n乙方试用期工资为人民币14,000元/月。",
      "source_span": {
        "start_offset": 1053,
        "end_offset": 1078,
        "raw_text": "第六条\n乙方试用期工资为人民币14,000元/月。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0013",
        "section": "第六条",
        "sentence_index": 1,
        "quote": "第六条\n乙方试用期工资为人民币14,000元/月。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 1053,
          "end_offset": 1078,
          "raw_text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0013",
          "clause_sha256": "7da31850fe2e9ea9dd849908eced980c3e4a23276d0c9aebeb838a802eec76dc",
          "local_start": 0,
          "local_end": 25,
          "locator": "第六条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_probation_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-03-01",
      "element_ids": [
        "employment_probation_2"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-3bd67fced777e7442f91",
      "quoted_text": "第六条\n乙方试用期工资为人民币14,000元/月。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0013",
        "clause_sha256": "7da31850fe2e9ea9dd849908eced980c3e4a23276d0c9aebeb838a802eec76dc",
        "local_start": 0,
        "local_end": 25,
        "locator": "第六条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_probation_2"
        ]
      },
      "supported_propositions": [
        "试用期工资标准"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "风险条款",
  "reason": "发现试用期超过法定上限或重复约定的直接约定，存在效力或履行风险，需结合适用法律及具体事实核验。",
  "coverage_elements": [
    {
      "review_id": "EMP-15-01",
      "element_id": "employment_probation_limit_adverse",
      "proposition": "试用期超过法定上限或重复约定",
      "status": "COVERED",
      "evidence_ids": [
        "SYN-656f93a9ccb88375b5ae",
        "SYN-e62997cf1209c872734c"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0005"
      ],
      "source_spans": [
        "合同期限自2026年9月15日起至2028年9月14日止。",
        "试用期自2026年9月15日起至2026年12月14日止，共3个月。"
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
        "C0005"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SYN-656f93a9ccb88375b5ae",
        "SYN-e62997cf1209c872734c"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。"
        },
        {
          "clause_id": "C0005",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。"
        }
      ],
      "supporting_evidence_ids": [
        "SYN-656f93a9ccb88375b5ae",
        "SYN-e62997cf1209c872734c"
      ]
    }
  ],
  "negative_clause_check": {
    "review_id": "EMP-15-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "ADVERSE_CLAUSE_FOUND",
    "description": "发现对应禁止性/不利约定。",
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
      "C0039",
      "C0040"
    ],
    "candidate_adverse_clauses": [
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "section_type": "正式合同条款",
        "level": 1,
        "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "normalized_text": "第一条甲乙双方约定采用固定期限劳动合同。合同期限自2026年9月15日起至2028年9月14日止。试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "option_groups": [],
        "source": "body",
        "section_path": [
          "正式合同条款",
          "第一条"
        ],
        "heading": "第一条",
        "clause_number": "第一条",
        "paragraph_index": 4,
        "block_type": "OPERATIVE_CLAUSE",
        "parties": [],
        "dates": [
          "2026年9月15日",
          "2028年9月14日",
          "2026年9月15日",
          "2026年12月14日"
        ],
        "amounts": [],
        "percentages": [],
        "durations": [
          "2026年",
          "9月",
          "15日",
          "2028年",
          "9月",
          "14日",
          "2026年",
          "9月",
          "15日",
          "2026年",
          "12月",
          "14日",
          "3个月"
        ],
        "cross_references": [
          "第一条"
        ],
        "node_id": "C0005",
        "document_id": "contract_package/main",
        "heading_path": [
          "第一条"
        ],
        "article_number": "第一条",
        "section_number": "",
        "item_number": "",
        "sentence_index": 1,
        "start_offset": 356,
        "end_offset": 442,
        "source_type": "BODY",
        "party_obligation": true,
        "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
        "supports_element_ids": [
          "employment_probation_limit_adverse"
        ],
        "document_type": "MAIN_CONTRACT",
        "source_document_type": "MAIN_CONTRACT",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "document_name": "合同正文",
        "section": "第一条",
        "confidence": "high",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 378,
          "end_offset": 407,
          "raw_text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "source_start": 378,
        "source_end": 407,
        "source_document": "contract_package/main",
        "original_document_reference": "contract_package/main",
        "derived_or_original": "ORIGINAL",
        "evidence_source": {
          "document_id": "contract_package/main",
          "document_type": "MAIN_CONTRACT",
          "document_name": "合同正文",
          "clause_id": "C0005",
          "section": "第一条",
          "sentence_index": 1,
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "confidence": "high",
          "evidence_block_type": "OPERATIVE_CLAUSE",
          "evidence_type": "CONTRACT_TEXT",
          "source_span": {
            "start_offset": 378,
            "end_offset": 407,
            "raw_text": "合同期限自2026年9月15日起至2028年9月14日止。",
            "coordinate_system": "DOCUMENT_TEXT"
          },
          "derived_or_original": "ORIGINAL",
          "source_ref": {
            "document_id": "contract_package/main",
            "clause_id": "C0005",
            "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
            "local_start": 22,
            "local_end": 51,
            "locator": "第一条"
          },
          "verified_original": true
        },
        "evidence_polarity": "NEUTRAL",
        "entailment_status": "SUPPORTS",
        "supporting_element_ids": [
          "employment_probation_limit_adverse"
        ],
        "canonical_fact_keys": [],
        "relevance_score": 1.0,
        "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
        "review_id": "EMP-15-01",
        "element_ids": [
          "employment_probation_limit_adverse"
        ],
        "support_type": "DIRECT",
        "verified_original": true,
        "source_verification": {
          "status": "PASS",
          "errors": [],
          "method": "EXACT_PARSER_SOURCE_SPAN"
        },
        "evidence_id": "SRC-80bfc61b0dd1c9588fbd",
        "quoted_text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0005",
          "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
          "local_start": 22,
          "local_end": 51,
          "locator": "第一条"
        },
        "provenance_validation": {
          "status": "PASS",
          "evidence_type": "CONTRACT_TEXT",
          "errors": []
        }
      },
      {
        "clause_id": "C0005",
        "location": "第一条",
        "title": "第一条",
        "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "section_type": "正式合同条款",
        "level": 1,
        "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "normalized_text": "第一条甲乙双方约定采用固定期限劳动合同。合同期限自2026年9月15日起至2028年9月14日止。试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "option_groups": [],
        "source": "body",
        "section_path": [
          "正式合同条款",
          "第一条"
        ],
        "heading": "第一条",
        "clause_number": "第一条",
        "paragraph_index": 4,
        "block_type": "OPERATIVE_CLAUSE",
        "parties": [],
        "dates": [
          "2026年9月15日",
          "2028年9月14日",
          "2026年9月15日",
          "2026年12月14日"
        ],
        "amounts": [],
        "percentages": [],
        "durations": [
          "2026年",
          "9月",
          "15日",
          "2028年",
          "9月",
          "14日",
          "2026年",
          "9月",
          "15日",
          "2026年",
          "12月",
          "14日",
          "3个月"
        ],
        "cross_references": [
          "第一条"
        ],
        "node_id": "C0005",
        "document_id": "contract_package/main",
        "heading_path": [
          "第一条"
        ],
        "article_number": "第一条",
        "section_number": "",
        "item_number": "",
        "sentence_index": 1,
        "start_offset": 356,
        "end_offset": 442,
        "source_type": "BODY",
        "party_obligation": true,
        "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "supports_element_ids": [
          "employment_probation_limit_adverse"
        ],
        "document_type": "MAIN_CONTRACT",
        "source_document_type": "MAIN_CONTRACT",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "document_name": "合同正文",
        "section": "第一条",
        "confidence": "high",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 408,
          "end_offset": 442,
          "raw_text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "source_start": 408,
        "source_end": 442,
        "source_document": "contract_package/main",
        "original_document_reference": "contract_package/main",
        "derived_or_original": "ORIGINAL",
        "evidence_source": {
          "document_id": "contract_package/main",
          "document_type": "MAIN_CONTRACT",
          "document_name": "合同正文",
          "clause_id": "C0005",
          "section": "第一条",
          "sentence_index": 1,
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "confidence": "high",
          "evidence_block_type": "OPERATIVE_CLAUSE",
          "evidence_type": "CONTRACT_TEXT",
          "source_span": {
            "start_offset": 408,
            "end_offset": 442,
            "raw_text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
            "coordinate_system": "DOCUMENT_TEXT"
          },
          "derived_or_original": "ORIGINAL",
          "source_ref": {
            "document_id": "contract_package/main",
            "clause_id": "C0005",
            "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
            "local_start": 52,
            "local_end": 86,
            "locator": "第一条"
          },
          "verified_original": true
        },
        "evidence_polarity": "NEUTRAL",
        "entailment_status": "SUPPORTS",
        "supporting_element_ids": [
          "employment_probation_limit_adverse"
        ],
        "canonical_fact_keys": [],
        "relevance_score": 1.0,
        "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
        "review_id": "EMP-15-01",
        "element_ids": [
          "employment_probation_limit_adverse"
        ],
        "support_type": "DIRECT",
        "verified_original": true,
        "source_verification": {
          "status": "PASS",
          "errors": [],
          "method": "EXACT_PARSER_SOURCE_SPAN"
        },
        "evidence_id": "SRC-2f1080c8421252494beb",
        "quoted_text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0005",
          "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
          "local_start": 52,
          "local_end": 86,
          "locator": "第一条"
        },
        "provenance_validation": {
          "status": "PASS",
          "evidence_type": "CONTRACT_TEXT",
          "errors": []
        }
      }
    ],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": true,
    "confidence": "high",
    "coverage_result": "风险条款"
  },
  "element_absence_searches": [
    {
      "element_id": "employment_probation_limit_adverse",
      "review_id": "EMP-15-01",
      "search_targets": [
        "试用期超过法定上限或重复约定"
      ],
      "query_patterns": [
        "合同期限自2026年9月15日起至2028年9月14日止。",
        "试用期自2026年9月15日起至2026年12月14日止，共3个月。"
      ],
      "query_semantic_target": "试用期超过法定上限或重复约定",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "合同期限自2026年9月15日起至2028年9月14日止。"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "试用期自2026年9月15日起至2026年12月14日止，共3个月。"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_probation_limit_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0005",
      "location": "第一条",
      "title": "第一条",
      "text": "合同期限自2026年9月15日起至2028年9月14日止。",
      "section_type": "正式合同条款",
      "level": 1,
      "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "normalized_text": "第一条甲乙双方约定采用固定期限劳动合同。合同期限自2026年9月15日起至2028年9月14日止。试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "option_groups": [],
      "source": "body",
      "section_path": [
        "正式合同条款",
        "第一条"
      ],
      "heading": "第一条",
      "clause_number": "第一条",
      "paragraph_index": 4,
      "block_type": "OPERATIVE_CLAUSE",
      "parties": [],
      "dates": [
        "2026年9月15日",
        "2028年9月14日",
        "2026年9月15日",
        "2026年12月14日"
      ],
      "amounts": [],
      "percentages": [],
      "durations": [
        "2026年",
        "9月",
        "15日",
        "2028年",
        "9月",
        "14日",
        "2026年",
        "9月",
        "15日",
        "2026年",
        "12月",
        "14日",
        "3个月"
      ],
      "cross_references": [
        "第一条"
      ],
      "node_id": "C0005",
      "document_id": "contract_package/main",
      "heading_path": [
        "第一条"
      ],
      "article_number": "第一条",
      "section_number": "",
      "item_number": "",
      "sentence_index": 1,
      "start_offset": 356,
      "end_offset": 442,
      "source_type": "BODY",
      "party_obligation": true,
      "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
      "supports_element_ids": [
        "employment_probation_limit_adverse"
      ],
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第一条",
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "source_span": {
        "start_offset": 378,
        "end_offset": 407,
        "raw_text": "合同期限自2026年9月15日起至2028年9月14日止。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_start": 378,
      "source_end": 407,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0005",
        "section": "第一条",
        "sentence_index": 1,
        "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 378,
          "end_offset": 407,
          "raw_text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0005",
          "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
          "local_start": 22,
          "local_end": 51,
          "locator": "第一条"
        },
        "verified_original": true
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_probation_limit_adverse"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-15-01",
      "element_ids": [
        "employment_probation_limit_adverse"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-80bfc61b0dd1c9588fbd",
      "quoted_text": "合同期限自2026年9月15日起至2028年9月14日止。",
      "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0005",
        "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
        "local_start": 22,
        "local_end": 51,
        "locator": "第一条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "试用期超过法定上限或重复约定"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0005",
      "location": "第一条",
      "title": "第一条",
      "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "section_type": "正式合同条款",
      "level": 1,
      "raw_text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "normalized_text": "第一条甲乙双方约定采用固定期限劳动合同。合同期限自2026年9月15日起至2028年9月14日止。试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "option_groups": [],
      "source": "body",
      "section_path": [
        "正式合同条款",
        "第一条"
      ],
      "heading": "第一条",
      "clause_number": "第一条",
      "paragraph_index": 4,
      "block_type": "OPERATIVE_CLAUSE",
      "parties": [],
      "dates": [
        "2026年9月15日",
        "2028年9月14日",
        "2026年9月15日",
        "2026年12月14日"
      ],
      "amounts": [],
      "percentages": [],
      "durations": [
        "2026年",
        "9月",
        "15日",
        "2028年",
        "9月",
        "14日",
        "2026年",
        "9月",
        "15日",
        "2026年",
        "12月",
        "14日",
        "3个月"
      ],
      "cross_references": [
        "第一条"
      ],
      "node_id": "C0005",
      "document_id": "contract_package/main",
      "heading_path": [
        "第一条"
      ],
      "article_number": "第一条",
      "section_number": "",
      "item_number": "",
      "sentence_index": 1,
      "start_offset": 356,
      "end_offset": 442,
      "source_type": "BODY",
      "party_obligation": true,
      "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "supports_element_ids": [
        "employment_probation_limit_adverse"
      ],
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第一条",
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "source_span": {
        "start_offset": 408,
        "end_offset": 442,
        "raw_text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_start": 408,
      "source_end": 442,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0005",
        "section": "第一条",
        "sentence_index": 1,
        "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 408,
          "end_offset": 442,
          "raw_text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0005",
          "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
          "local_start": 52,
          "local_end": 86,
          "locator": "第一条"
        },
        "verified_original": true
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_probation_limit_adverse"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-15-01",
      "element_ids": [
        "employment_probation_limit_adverse"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-2f1080c8421252494beb",
      "quoted_text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0005",
        "clause_sha256": "f37083d232267190cc25d0c17fcdda58076eeff3f1004bdabc1c97ffc83d3a77",
        "local_start": 52,
        "local_end": 86,
        "locator": "第一条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "试用期超过法定上限或重复约定"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
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
        "SRC-2037cae9f0945abbdacb",
        "SRC-7e29da5b362957a93c9b"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0007"
      ],
      "source_spans": [
        "第二条\n乙方工作岗位为软件开发工程师。",
        "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。"
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
        "C0007"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-2037cae9f0945abbdacb",
        "SRC-7e29da5b362957a93c9b"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-2037cae9f0945abbdacb",
        "SRC-7e29da5b362957a93c9b"
      ],
      "bound_evidence_ids": [
        "SRC-2037cae9f0945abbdacb",
        "SRC-7e29da5b362957a93c9b"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0007",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。"
        },
        {
          "clause_id": "C0007",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。"
        }
      ]
    },
    {
      "review_id": "EMP-04-01",
      "element_id": "employment_work_2",
      "proposition": "具体工作地点",
      "status": "COVERED",
      "evidence_ids": [
        "SRC-c7e11b64c690866aad41"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0007"
      ],
      "source_spans": [
        "乙方主要工作地点为深圳市南山区。"
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
        "C0007"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-c7e11b64c690866aad41"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-c7e11b64c690866aad41"
      ],
      "bound_evidence_ids": [
        "SRC-c7e11b64c690866aad41"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0007",
          "quote": "乙方主要工作地点为深圳市南山区。"
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "(?:工作岗位|工作内容|岗位)[为：:][^，。；_]{2,35}|安排(?:乙方|劳动者)在[^，。；_]{2,40}岗位|从事[^，。；_]{2,60}(?:开发|维护|测试|工作)"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "(?:负责|参与|承担)[^。；\\n]{2,80}(?:研发|开发|测试|维护|研究|设计|整理|编写)"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 95,
          "selection_reason": "DIRECT_SEMANTIC_SUPPORT"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_work_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 95,
          "selection_reason": "DIRECT_SEMANTIC_SUPPORT"
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "工作地点[为：:][^，。；_]{3,60}"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_work_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 95,
          "selection_reason": "DIRECT_SEMANTIC_SUPPORT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0007",
      "location": "第二条",
      "title": "第二条",
      "text": "第二条\n乙方工作岗位为软件开发工程师。",
      "quote": "第二条\n乙方工作岗位为软件开发工程师。",
      "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二条"
      ],
      "source_start": 455,
      "source_end": 474,
      "supports_element_ids": [
        "employment_work_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 95,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
      "source_span": {
        "start_offset": 455,
        "end_offset": 474,
        "raw_text": "第二条\n乙方工作岗位为软件开发工程师。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0007",
        "section": "第二条",
        "sentence_index": 1,
        "quote": "第二条\n乙方工作岗位为软件开发工程师。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 455,
          "end_offset": 474,
          "raw_text": "第二条\n乙方工作岗位为软件开发工程师。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0007",
          "clause_sha256": "23d8f9c19ad4f1e6889b43e6f2585cfdea455819940caf72090aa0e3bf9d2bda",
          "local_start": 0,
          "local_end": 19,
          "locator": "第二条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_work_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-04-01",
      "element_ids": [
        "employment_work_1"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-2037cae9f0945abbdacb",
      "quoted_text": "第二条\n乙方工作岗位为软件开发工程师。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0007",
        "clause_sha256": "23d8f9c19ad4f1e6889b43e6f2585cfdea455819940caf72090aa0e3bf9d2bda",
        "local_start": 0,
        "local_end": 19,
        "locator": "第二条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_work_1"
        ]
      },
      "supported_propositions": [
        "具体工作岗位或职责"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0007",
      "location": "第二条",
      "title": "第二条",
      "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
      "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
      "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二条"
      ],
      "source_start": 475,
      "source_end": 568,
      "supports_element_ids": [
        "employment_work_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 95,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
      "source_span": {
        "start_offset": 475,
        "end_offset": 568,
        "raw_text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0007",
        "section": "第二条",
        "sentence_index": 1,
        "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 475,
          "end_offset": 568,
          "raw_text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0007",
          "clause_sha256": "23d8f9c19ad4f1e6889b43e6f2585cfdea455819940caf72090aa0e3bf9d2bda",
          "local_start": 20,
          "local_end": 113,
          "locator": "第二条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_work_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-04-01",
      "element_ids": [
        "employment_work_1"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-7e29da5b362957a93c9b",
      "quoted_text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0007",
        "clause_sha256": "23d8f9c19ad4f1e6889b43e6f2585cfdea455819940caf72090aa0e3bf9d2bda",
        "local_start": 20,
        "local_end": 113,
        "locator": "第二条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_work_1"
        ]
      },
      "supported_propositions": [
        "具体工作岗位或职责"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0007",
      "location": "第二条",
      "title": "第二条",
      "text": "乙方主要工作地点为深圳市南山区。",
      "quote": "乙方主要工作地点为深圳市南山区。",
      "original_excerpt": "乙方主要工作地点为深圳市南山区。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二条"
      ],
      "source_start": 569,
      "source_end": 585,
      "supports_element_ids": [
        "employment_work_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 95,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
      "source_span": {
        "start_offset": 569,
        "end_offset": 585,
        "raw_text": "乙方主要工作地点为深圳市南山区。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0007",
        "section": "第二条",
        "sentence_index": 1,
        "quote": "乙方主要工作地点为深圳市南山区。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 569,
          "end_offset": 585,
          "raw_text": "乙方主要工作地点为深圳市南山区。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0007",
          "clause_sha256": "23d8f9c19ad4f1e6889b43e6f2585cfdea455819940caf72090aa0e3bf9d2bda",
          "local_start": 114,
          "local_end": 130,
          "locator": "第二条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_work_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-04-01",
      "element_ids": [
        "employment_work_2"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-c7e11b64c690866aad41",
      "quoted_text": "乙方主要工作地点为深圳市南山区。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0007",
        "clause_sha256": "23d8f9c19ad4f1e6889b43e6f2585cfdea455819940caf72090aa0e3bf9d2bda",
        "local_start": 114,
        "local_end": 130,
        "locator": "第二条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_work_2"
        ]
      },
      "supported_propositions": [
        "具体工作地点"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "风险条款",
  "reason": "发现与本项法定保护相冲突的直接不利约定。",
  "coverage_elements": [
    {
      "review_id": "EMP-05-01",
      "element_id": "employment_hours_adverse",
      "proposition": "工时、休息与加班存在直接不利约定",
      "status": "ADVERSE",
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
        "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。"
      ],
      "source_locations": [
        "第三条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0009"
      ],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0009"
      ],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0009",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [
    {
      "clause_id": "C0009",
      "location": "第三条",
      "title": "第三条",
      "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
      "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
      "section_type": "正式合同条款",
      "block_type": "OPERATIVE_CLAUSE",
      "predicate": "不再",
      "polarity": "AFFIRMED",
      "supports_element_ids": [
        "employment_hours_adverse"
      ],
      "supporting_element_ids": [
        "employment_hours_adverse"
      ],
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第三条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
      "source_span": {
        "start_offset": 792,
        "end_offset": 841,
        "raw_text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_start": 792,
      "source_end": 841,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0009",
        "section": "第三条",
        "sentence_index": 1,
        "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 792,
          "end_offset": 841,
          "raw_text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0009",
          "clause_sha256": "8949eb3e0fff0bfe7d66e41c283eaf657206965e8b134c299b66c1a2798e7147",
          "local_start": 85,
          "local_end": 134,
          "locator": "第三条"
        },
        "verified_original": true
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-05-01",
      "element_ids": [
        "employment_hours_adverse"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-5ba79f338bb486ec0a96",
      "quoted_text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
      "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0009",
        "clause_sha256": "8949eb3e0fff0bfe7d66e41c283eaf657206965e8b134c299b66c1a2798e7147",
        "local_start": 85,
        "local_end": 134,
        "locator": "第三条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "工时、休息与加班存在直接不利约定"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "风险条款",
  "reason": "发现与本项法定保护相冲突的直接不利约定。",
  "coverage_elements": [
    {
      "review_id": "EMP-06-01",
      "element_id": "employment_wage_adverse",
      "proposition": "工资标准与支付存在直接不利约定",
      "status": "ADVERSE",
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
        "乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。"
      ],
      "source_locations": [
        "第十三条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0023"
      ],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0023"
      ],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0023",
          "quote": "乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [
    {
      "clause_id": "C0023",
      "location": "第十三条",
      "title": "第十三条",
      "text": "乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
      "quote": "乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
      "section_type": "正式合同条款",
      "block_type": "OPERATIVE_CLAUSE",
      "predicate": "甲方有权暂缓办理离职手续及支付乙方尚未结算的工资",
      "polarity": "AFFIRMED",
      "supports_element_ids": [
        "employment_wage_adverse"
      ],
      "supporting_element_ids": [
        "employment_wage_adverse"
      ],
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第十三条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
      "source_span": {
        "start_offset": 1579,
        "end_offset": 1641,
        "raw_text": "乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_start": 1579,
      "source_end": 1641,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0023",
        "section": "第十三条",
        "sentence_index": 1,
        "quote": "乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 1579,
          "end_offset": 1641,
          "raw_text": "乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0023",
          "clause_sha256": "d7119b6349d00375276638fd96e68fbe78a9ed9dcb955b25dbcb3d633c5d6304",
          "local_start": 48,
          "local_end": 110,
          "locator": "第十三条"
        },
        "verified_original": true
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-06-01",
      "element_ids": [
        "employment_wage_adverse"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-3832eb9ef78f702aca4e",
      "quoted_text": "乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
      "original_excerpt": "乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0023",
        "clause_sha256": "d7119b6349d00375276638fd96e68fbe78a9ed9dcb955b25dbcb3d633c5d6304",
        "local_start": 48,
        "local_end": 110,
        "locator": "第十三条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "工资标准与支付存在直接不利约定"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "风险条款",
  "reason": "发现与本项法定保护相冲突的直接不利约定。",
  "coverage_elements": [
    {
      "review_id": "EMP-07-01",
      "element_id": "employment_insurance_adverse",
      "proposition": "社会保险缴纳存在直接不利约定",
      "status": "ADVERSE",
      "evidence_ids": [
        "C0016"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0016"
      ],
      "source_spans": [
        "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。"
      ],
      "source_locations": [
        "第八条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0016"
      ],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0016"
      ],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0016",
          "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [
    {
      "clause_id": "C0016",
      "location": "第八条",
      "title": "第八条",
      "text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
      "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
      "section_type": "正式合同条款",
      "block_type": "OPERATIVE_CLAUSE",
      "predicate": "甲方暂不为乙方缴纳社会保险",
      "polarity": "AFFIRMED",
      "supports_element_ids": [
        "employment_insurance_adverse"
      ],
      "supporting_element_ids": [
        "employment_insurance_adverse"
      ],
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第八条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
      "source_span": {
        "start_offset": 1163,
        "end_offset": 1229,
        "raw_text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_start": 1163,
      "source_end": 1229,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0016",
        "section": "第八条",
        "sentence_index": 1,
        "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 1163,
          "end_offset": 1229,
          "raw_text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0016",
          "clause_sha256": "f4e17b4170228b7695dc427b4e453275c01f48036f493723a83e63e6d65e0a7f",
          "local_start": 18,
          "local_end": 84,
          "locator": "第八条"
        },
        "verified_original": true
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-07-01",
      "element_ids": [
        "employment_insurance_adverse"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-3f5ef2d273a66fda1daf",
      "quoted_text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
      "original_excerpt": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0016",
        "clause_sha256": "f4e17b4170228b7695dc427b4e453275c01f48036f493723a83e63e6d65e0a7f",
        "local_start": 18,
        "local_end": 84,
        "locator": "第八条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "社会保险缴纳存在直接不利约定"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "缺失",
  "reason": "未找到明确约定：劳动防护和安全培训。专项要素的适用前提待核实，未将条件不明的义务判为合同缺失。",
  "coverage_elements": [
    {
      "review_id": "EMP-08-01",
      "element_id": "employment_safety_1",
      "proposition": "劳动防护和安全培训",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_safety_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "NOT_FOUND"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
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
    "applicability_state": "CONDITIONAL_NOT_TRIGGERED",
    "premise_evidence": [],
    "premise_fact_ids": [],
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "风险条款",
  "reason": "发现与本项法定保护相冲突的直接不利约定。",
  "coverage_elements": [
    {
      "review_id": "EMP-10-01",
      "element_id": "employment_exit_adverse",
      "proposition": "解除终止条件和程序存在直接不利约定",
      "status": "ADVERSE",
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
        "未经甲方批准，乙方不得自行离职。"
      ],
      "source_locations": [
        "第十三条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0023"
      ],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0023"
      ],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0023",
          "quote": "未经甲方批准，乙方不得自行离职。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [
    {
      "clause_id": "C0023",
      "location": "第十三条",
      "title": "第十三条",
      "text": "未经甲方批准，乙方不得自行离职。",
      "quote": "未经甲方批准，乙方不得自行离职。",
      "section_type": "正式合同条款",
      "block_type": "OPERATIVE_CLAUSE",
      "predicate": "不得",
      "polarity": "AFFIRMED",
      "supports_element_ids": [
        "employment_exit_adverse"
      ],
      "supporting_element_ids": [
        "employment_exit_adverse"
      ],
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第十三条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
      "source_span": {
        "start_offset": 1562,
        "end_offset": 1578,
        "raw_text": "未经甲方批准，乙方不得自行离职。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_start": 1562,
      "source_end": 1578,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0023",
        "section": "第十三条",
        "sentence_index": 1,
        "quote": "未经甲方批准，乙方不得自行离职。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 1562,
          "end_offset": 1578,
          "raw_text": "未经甲方批准，乙方不得自行离职。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0023",
          "clause_sha256": "d7119b6349d00375276638fd96e68fbe78a9ed9dcb955b25dbcb3d633c5d6304",
          "local_start": 31,
          "local_end": 47,
          "locator": "第十三条"
        },
        "verified_original": true
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-10-01",
      "element_ids": [
        "employment_exit_adverse"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-f8172b6e21078912d195",
      "quoted_text": "未经甲方批准，乙方不得自行离职。",
      "original_excerpt": "未经甲方批准，乙方不得自行离职。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0023",
        "clause_sha256": "d7119b6349d00375276638fd96e68fbe78a9ed9dcb955b25dbcb3d633c5d6304",
        "local_start": 31,
        "local_end": 47,
        "locator": "第十三条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "解除终止条件和程序存在直接不利约定"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "缺失",
  "reason": "未找到明确约定：经济补偿依法处理、计算依据或正常结算安排。",
  "coverage_elements": [
    {
      "review_id": "EMP-11-01",
      "element_id": "employment_compensation_1",
      "proposition": "经济补偿依法处理、计算依据或正常结算安排",
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
    },
    {
      "review_id": "EMP-11-01",
      "element_id": "employment_compensation_2",
      "proposition": "解除终止后工资及补偿结算期限",
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
      "risk_relevant": false,
      "residual_gap": "可选完善解除终止后工资及经济补偿结算期限",
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
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
        "依法(?:需要|应当|应)?[^。；\\n]{0,20}支付经济补偿[^。；\\n]{0,15}(?:甲方|用人单位)(?:按照|依照|按)法律规定支付",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_compensation_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "NOT_FOUND"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "NOT_FOUND",
      "supporting_evidence": []
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_compensation_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "NOT_FOUND"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
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
        "SRC-ab1c3804160e659c5bbc"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0035"
      ],
      "source_spans": [
        "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。"
      ],
      "source_locations": [
        "第二十一条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0035"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-ab1c3804160e659c5bbc"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence_ids": [
        "SRC-ab1c3804160e659c5bbc"
      ],
      "bound_evidence_ids": [
        "SRC-ab1c3804160e659c5bbc"
      ],
      "supporting_evidence": [
        {
          "clause_id": "C0035",
          "quote": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。"
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
        "劳动争议仲裁机构[：:]\\s*[^。；\\n]{2,50}劳动人事争议仲裁委员会",
        "(?:申请|提起)(?:劳动争议仲裁|劳动仲裁|仲裁)",
        "(?:提交|向)[^。；\\n]{0,30}劳动仲裁委员会"
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "title": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "quote": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "original_excerpt": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "source_start": 0,
          "source_end": 53,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "(?:申请|提起)(?:劳动争议仲裁|劳动仲裁|仲裁)"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "title": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "quote": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "original_excerpt": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二十一条"
          ],
          "source_start": 0,
          "source_end": 53,
          "supports_element_ids": [
            "employment_dispute_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 95,
          "selection_reason": "DIRECT_SEMANTIC_SUPPORT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0035",
      "location": "第二十一条",
      "title": "第二十一条",
      "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
      "quote": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
      "original_excerpt": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二十一条"
      ],
      "source_start": 2365,
      "source_end": 2418,
      "supports_element_ids": [
        "employment_dispute_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 95,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二十一条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
      "source_span": {
        "start_offset": 2365,
        "end_offset": 2418,
        "raw_text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0035",
        "section": "第二十一条",
        "sentence_index": 1,
        "quote": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 2365,
          "end_offset": 2418,
          "raw_text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0035",
          "clause_sha256": "41328a3fbb14f78efe56d08ab22d6c162d0ca3c5b5a456d34df19d1fe316531e",
          "local_start": 0,
          "local_end": 53,
          "locator": "第二十一条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_dispute_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "EMP-12-01",
      "element_ids": [
        "employment_dispute_1"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-ab1c3804160e659c5bbc",
      "quoted_text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0035",
        "clause_sha256": "41328a3fbb14f78efe56d08ab22d6c162d0ca3c5b5a456d34df19d1fe316531e",
        "local_start": 0,
        "local_end": 53,
        "locator": "第二十一条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "source_semantic_verification": {
        "status": "PASS",
        "element_ids": [
          "employment_dispute_1"
        ]
      },
      "supported_propositions": [
        "劳动争议依法申请劳动仲裁"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "风险条款",
  "reason": "发现免除或放弃法定社会保险义务的直接约定，存在效力或履行风险，需结合适用法律及具体事实核验。",
  "coverage_elements": [
    {
      "review_id": "EMP-13-01",
      "element_id": "employment_illegal_waiver_adverse",
      "proposition": "免除或放弃法定社会保险义务",
      "status": "COVERED",
      "evidence_ids": [
        "SRC-3f5ef2d273a66fda1daf",
        "EV-e527367e9a431db5"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0016"
      ],
      "source_spans": [
        "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。"
      ],
      "source_locations": [
        "第八条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0016"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "SRC-3f5ef2d273a66fda1daf",
        "EV-e527367e9a431db5"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0016",
          "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。"
        }
      ],
      "supporting_evidence_ids": [
        "SRC-3f5ef2d273a66fda1daf",
        "EV-e527367e9a431db5"
      ]
    }
  ],
  "negative_clause_check": {
    "review_id": "EMP-13-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "ADVERSE_CLAUSE_FOUND",
    "description": "发现对应禁止性/不利约定。",
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
      "C0039",
      "C0040"
    ],
    "candidate_adverse_clauses": [
      {
        "clause_id": "C0016",
        "location": "第八条",
        "title": "第八条",
        "text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
        "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
        "section_type": "正式合同条款",
        "block_type": "OPERATIVE_CLAUSE",
        "predicate": "甲方暂不为乙方缴纳社会保险",
        "polarity": "AFFIRMED",
        "supports_element_ids": [
          "employment_illegal_waiver_adverse"
        ],
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "source_document_type": "MAIN_CONTRACT",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "document_name": "合同正文",
        "section": "第八条",
        "sentence_index": 1,
        "confidence": "high",
        "evidence_type": "CONTRACT_TEXT",
        "raw_text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
        "source_span": {
          "start_offset": 1163,
          "end_offset": 1229,
          "raw_text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "source_start": 1163,
        "source_end": 1229,
        "source_document": "contract_package/main",
        "original_document_reference": "contract_package/main",
        "derived_or_original": "ORIGINAL",
        "evidence_source": {
          "document_id": "contract_package/main",
          "document_type": "MAIN_CONTRACT",
          "document_name": "合同正文",
          "clause_id": "C0016",
          "section": "第八条",
          "sentence_index": 1,
          "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "confidence": "high",
          "evidence_block_type": "OPERATIVE_CLAUSE",
          "evidence_type": "CONTRACT_TEXT",
          "source_span": {
            "start_offset": 1163,
            "end_offset": 1229,
            "raw_text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
            "coordinate_system": "DOCUMENT_TEXT"
          },
          "derived_or_original": "ORIGINAL",
          "source_ref": {
            "document_id": "contract_package/main",
            "clause_id": "C0016",
            "clause_sha256": "f4e17b4170228b7695dc427b4e453275c01f48036f493723a83e63e6d65e0a7f",
            "local_start": 18,
            "local_end": 84,
            "locator": "第八条"
          },
          "verified_original": true
        },
        "evidence_polarity": "NEUTRAL",
        "entailment_status": "SUPPORTS",
        "supporting_element_ids": [
          "employment_illegal_waiver_adverse"
        ],
        "canonical_fact_keys": [],
        "relevance_score": 1.0,
        "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
        "review_id": "EMP-13-01",
        "element_ids": [
          "employment_illegal_waiver_adverse"
        ],
        "support_type": "DIRECT",
        "verified_original": true,
        "source_verification": {
          "status": "PASS",
          "errors": [],
          "method": "EXACT_PARSER_SOURCE_SPAN"
        },
        "evidence_id": "SRC-3f5ef2d273a66fda1daf",
        "quoted_text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
        "original_excerpt": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0016",
          "clause_sha256": "f4e17b4170228b7695dc427b4e453275c01f48036f493723a83e63e6d65e0a7f",
          "local_start": 18,
          "local_end": 84,
          "locator": "第八条"
        },
        "provenance_validation": {
          "status": "PASS",
          "evidence_type": "CONTRACT_TEXT",
          "errors": []
        }
      }
    ],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": true,
    "confidence": "high",
    "coverage_result": "风险条款"
  },
  "element_absence_searches": [
    {
      "element_id": "employment_illegal_waiver_adverse",
      "review_id": "EMP-13-01",
      "search_targets": [
        "免除或放弃法定社会保险义务"
      ],
      "query_patterns": [
        "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。"
      ],
      "query_semantic_target": "免除或放弃法定社会保险义务",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0016",
          "location": "第八条",
          "title": "第八条",
          "text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "original_excerpt": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "source_start": 17,
          "source_end": 84,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0016",
          "location": "第八条",
          "title": "第八条",
          "text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "original_excerpt": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第八条"
          ],
          "source_start": 17,
          "source_end": 84,
          "supports_element_ids": [
            "employment_illegal_waiver_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0016",
      "location": "第八条",
      "title": "第八条",
      "text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
      "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
      "section_type": "正式合同条款",
      "block_type": "OPERATIVE_CLAUSE",
      "predicate": "甲方暂不为乙方缴纳社会保险",
      "polarity": "AFFIRMED",
      "supports_element_ids": [
        "employment_illegal_waiver_adverse"
      ],
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第八条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
      "source_span": {
        "start_offset": 1163,
        "end_offset": 1229,
        "raw_text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_start": 1163,
      "source_end": 1229,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0016",
        "section": "第八条",
        "sentence_index": 1,
        "quote": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 1163,
          "end_offset": 1229,
          "raw_text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0016",
          "clause_sha256": "f4e17b4170228b7695dc427b4e453275c01f48036f493723a83e63e6d65e0a7f",
          "local_start": 18,
          "local_end": 84,
          "locator": "第八条"
        },
        "verified_original": true
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_illegal_waiver_adverse"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-13-01",
      "element_ids": [
        "employment_illegal_waiver_adverse"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-3f5ef2d273a66fda1daf",
      "quoted_text": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
      "original_excerpt": "经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0016",
        "clause_sha256": "f4e17b4170228b7695dc427b4e453275c01f48036f493723a83e63e6d65e0a7f",
        "local_start": 18,
        "local_end": 84,
        "locator": "第八条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "免除或放弃法定社会保险义务"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
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
      "C0039",
      "C0040"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
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
      "C0039",
      "C0040"
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "部分覆盖",
  "reason": "未找到明确约定：人员范围及实际接触秘密、明确约定竞业地域范围。",
  "coverage_elements": [
    {
      "review_id": "NC-01-01",
      "element_id": "employment_noncompete_scope_1",
      "proposition": "人员范围及实际接触秘密",
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
    },
    {
      "review_id": "NC-01-01",
      "element_id": "employment_noncompete_scope_2",
      "proposition": "明确约定竞业业务范围",
      "status": "COVERED",
      "evidence_ids": [
        "SRC-a040875982860994e5e1",
        "EV-de812b1f0991d25d"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0027"
      ],
      "source_spans": [
        "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。"
      ],
      "source_locations": [
        "第十六条"
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
        "SRC-a040875982860994e5e1",
        "EV-de812b1f0991d25d"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0027",
          "quote": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。"
        }
      ],
      "supporting_evidence_ids": [
        "SRC-a040875982860994e5e1",
        "EV-de812b1f0991d25d"
      ]
    },
    {
      "review_id": "NC-01-01",
      "element_id": "employment_noncompete_scope_3",
      "proposition": "明确约定竞业地域范围",
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
      "element_id": "employment_noncompete_scope_1",
      "review_id": "NC-01-01",
      "search_targets": [
        "人员范围及实际接触秘密"
      ],
      "query_patterns": [
        "(?:劳动者|乙方).{0,40}(?:实际接触|知悉|掌握).{0,35}(?:商业秘密|保密事项)"
      ],
      "query_semantic_target": "人员范围及实际接触秘密",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_noncompete_scope_1"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "NOT_FOUND"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "employment_noncompete_scope_2",
      "review_id": "NC-01-01",
      "search_targets": [
        "明确约定竞业业务范围"
      ],
      "query_patterns": [
        "竞业(?:限制|禁止).{0,25}业务范围\\s*(?:为|包括|限于|：|:)[^。；_]{3,80}",
        "(?:不得|禁止).{0,20}(?:自营|经营|从事).{0,50}(?:竞争|同类|类似).{0,20}业务",
        "(?:不得|禁止)[^。；\\n]{0,80}竞争关系[^。；\\n]{0,50}(?:包括|从事)[^。；\\n]{2,120}业务",
        "(?:竞业业务范围|竞争业务范围)[为：:][^。；\\n]{2,120}"
      ],
      "query_semantic_target": "明确约定竞业业务范围",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "title": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
          "quote": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
          "original_excerpt": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "source_start": 0,
          "source_end": 79,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "(?:不得|禁止)[^。；\\n]{0,80}竞争关系[^。；\\n]{0,50}(?:包括|从事)[^。；\\n]{2,120}业务"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "title": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
          "quote": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
          "original_excerpt": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "source_start": 0,
          "source_end": 79,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 100,
          "selection_reason": "DIRECT_OPERATIVE_WITH_VALUE"
        }
      ]
    },
    {
      "element_id": "employment_noncompete_scope_3",
      "review_id": "NC-01-01",
      "search_targets": [
        "明确约定竞业地域范围"
      ],
      "query_patterns": [
        "竞业(?:限制|禁止).{0,25}(?:地域|地区|区域)范围\\s*(?:为|包括|限于|：|:)[^。；_]{2,80}"
      ],
      "query_semantic_target": "明确约定竞业地域范围",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "title": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "quote": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "original_excerpt": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四条"
          ],
          "source_start": 0,
          "source_end": 32,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "NOT_FOUND"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0027",
      "location": "第十六条",
      "title": "第十六条",
      "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
      "quote": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
      "original_excerpt": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第十六条"
      ],
      "source_start": 1824,
      "source_end": 1903,
      "supports_element_ids": [
        "employment_noncompete_scope_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "entailment_score": 100,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第十六条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
      "source_span": {
        "start_offset": 1824,
        "end_offset": 1903,
        "raw_text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0027",
        "section": "第十六条",
        "sentence_index": 1,
        "quote": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 1824,
          "end_offset": 1903,
          "raw_text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0027",
          "clause_sha256": "309351d51f3f725f5e33274c84599999e87c97732bce7ae98e1f068fb74558c4",
          "local_start": 0,
          "local_end": 79,
          "locator": "第十六条"
        },
        "verified_original": true
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_noncompete_scope_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "review_id": "NC-01-01",
      "element_ids": [
        "employment_noncompete_scope_2"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-a040875982860994e5e1",
      "quoted_text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0027",
        "clause_sha256": "309351d51f3f725f5e33274c84599999e87c97732bce7ae98e1f068fb74558c4",
        "local_start": 0,
        "local_end": 79,
        "locator": "第十六条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "明确约定竞业业务范围"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## NC-02-01

```json
{
  "rule_id": "NC-02-01",
  "applicability": {
    "review_id": "NC-02-01",
    "applicable": true,
    "trigger_facts": [],
    "trigger_evidence": [],
    "missing_triggers": [],
    "reason": "核对离职竞业期限及补偿；未交代适用期间时不能直接按在职竞业豁免。",
    "confidence": "medium",
    "status": "APPLICABLE",
    "machine_reason": "核对离职竞业期限及补偿；未交代适用期间时不能直接按在职竞业豁免。",
    "user_reason": "合同已触发“出现离职、解除、终止安排时适用”这一适用条件。",
    "required_triggers": [],
    "satisfied_triggers": [],
    "unsatisfied_triggers": [],
    "conflicting_triggers": [],
    "trigger_fact_ids": [],
    "trigger_evidence_ids": [],
    "applicability_state": "CONDITIONAL_TRIGGERED",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "出现离职、解除、终止安排时适用",
    "triggered": true,
    "condition_text": "出现离职、解除、终止安排时适用"
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "风险条款",
  "reason": "发现与本项法定保护相冲突的直接不利约定。",
  "coverage_elements": [
    {
      "review_id": "NC-02-01",
      "element_id": "employment_noncompete_term_adverse",
      "proposition": "离职竞业期限及补偿存在直接不利约定",
      "status": "ADVERSE",
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
        "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。"
      ],
      "source_locations": [
        "第十六条"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "MISSING",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0027"
      ],
      "requirement_status": "NOT_SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0027"
      ],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0027",
          "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [],
  "evidence_clauses": [
    {
      "clause_id": "C0027",
      "location": "第十六条",
      "title": "第十六条",
      "text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
      "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
      "section_type": "正式合同条款",
      "block_type": "OPERATIVE_CLAUSE",
      "predicate": "甲方无需另行向乙方支付竞业限制经济补偿",
      "polarity": "AFFIRMED",
      "supports_element_ids": [
        "employment_noncompete_term_adverse"
      ],
      "supporting_element_ids": [
        "employment_noncompete_term_adverse"
      ],
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第十六条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
      "source_span": {
        "start_offset": 1904,
        "end_offset": 1961,
        "raw_text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_start": 1904,
      "source_end": 1961,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0027",
        "section": "第十六条",
        "sentence_index": 1,
        "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 1904,
          "end_offset": 1961,
          "raw_text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0027",
          "clause_sha256": "309351d51f3f725f5e33274c84599999e87c97732bce7ae98e1f068fb74558c4",
          "local_start": 80,
          "local_end": 137,
          "locator": "第十六条"
        },
        "verified_original": true
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "NC-02-01",
      "element_ids": [
        "employment_noncompete_term_adverse"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-355619768b1ddd44903e",
      "quoted_text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
      "original_excerpt": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0027",
        "clause_sha256": "309351d51f3f725f5e33274c84599999e87c97732bce7ae98e1f068fb74558c4",
        "local_start": 80,
        "local_end": 137,
        "locator": "第十六条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "离职竞业期限及补偿存在直接不利约定"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## NC-03-01

```json
{
  "rule_id": "NC-03-01",
  "applicability": {
    "review_id": "NC-03-01",
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "风险条款",
  "reason": "发现竞业范围或补偿明显不当的直接约定，存在效力或履行风险，需结合适用法律及具体事实核验。",
  "coverage_elements": [
    {
      "review_id": "NC-03-01",
      "element_id": "employment_noncompete_adverse_adverse",
      "proposition": "竞业范围或补偿明显不当",
      "status": "COVERED",
      "evidence_ids": [
        "SYN-ef0a43d97d46e33fd92a"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0027"
      ],
      "source_spans": [
        "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。"
      ],
      "source_locations": [
        "第十六条"
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
        "SYN-ef0a43d97d46e33fd92a"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0027",
          "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。"
        }
      ],
      "supporting_evidence_ids": [
        "SYN-ef0a43d97d46e33fd92a"
      ]
    }
  ],
  "negative_clause_check": {
    "review_id": "NC-03-01",
    "query_semantics": "ADVERSE_CLAUSE_SEARCH",
    "result": "ADVERSE_CLAUSE_FOUND",
    "description": "发现对应禁止性/不利约定。",
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
      "C0039",
      "C0040"
    ],
    "candidate_adverse_clauses": [
      {
        "clause_id": "C0027",
        "location": "第十六条",
        "title": "第十六条",
        "text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
        "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
        "section_type": "正式合同条款",
        "block_type": "OPERATIVE_CLAUSE",
        "predicate": "甲方无需另行向乙方支付竞业限制经济补偿",
        "polarity": "AFFIRMED",
        "supports_element_ids": [
          "employment_noncompete_adverse_adverse"
        ],
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "source_document_type": "MAIN_CONTRACT",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "document_name": "合同正文",
        "section": "第十六条",
        "sentence_index": 1,
        "confidence": "high",
        "evidence_type": "CONTRACT_TEXT",
        "raw_text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
        "source_span": {
          "start_offset": 1904,
          "end_offset": 1961,
          "raw_text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "source_start": 1904,
        "source_end": 1961,
        "source_document": "contract_package/main",
        "original_document_reference": "contract_package/main",
        "derived_or_original": "ORIGINAL",
        "evidence_source": {
          "document_id": "contract_package/main",
          "document_type": "MAIN_CONTRACT",
          "document_name": "合同正文",
          "clause_id": "C0027",
          "section": "第十六条",
          "sentence_index": 1,
          "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "confidence": "high",
          "evidence_block_type": "OPERATIVE_CLAUSE",
          "evidence_type": "CONTRACT_TEXT",
          "source_span": {
            "start_offset": 1904,
            "end_offset": 1961,
            "raw_text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
            "coordinate_system": "DOCUMENT_TEXT"
          },
          "derived_or_original": "ORIGINAL",
          "source_ref": {
            "document_id": "contract_package/main",
            "clause_id": "C0027",
            "clause_sha256": "309351d51f3f725f5e33274c84599999e87c97732bce7ae98e1f068fb74558c4",
            "local_start": 80,
            "local_end": 137,
            "locator": "第十六条"
          },
          "verified_original": true
        },
        "evidence_polarity": "NEUTRAL",
        "entailment_status": "SUPPORTS",
        "supporting_element_ids": [
          "employment_noncompete_adverse_adverse"
        ],
        "canonical_fact_keys": [],
        "relevance_score": 1.0,
        "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
        "review_id": "NC-03-01",
        "element_ids": [
          "employment_noncompete_adverse_adverse"
        ],
        "support_type": "DIRECT",
        "verified_original": true,
        "source_verification": {
          "status": "PASS",
          "errors": [],
          "method": "EXACT_PARSER_SOURCE_SPAN"
        },
        "evidence_id": "SRC-355619768b1ddd44903e",
        "quoted_text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
        "original_excerpt": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0027",
          "clause_sha256": "309351d51f3f725f5e33274c84599999e87c97732bce7ae98e1f068fb74558c4",
          "local_start": 80,
          "local_end": 137,
          "locator": "第十六条"
        },
        "provenance_validation": {
          "status": "PASS",
          "evidence_type": "CONTRACT_TEXT",
          "errors": []
        }
      }
    ],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": true,
    "confidence": "high",
    "coverage_result": "风险条款"
  },
  "element_absence_searches": [
    {
      "element_id": "employment_noncompete_adverse_adverse",
      "review_id": "NC-03-01",
      "search_targets": [
        "竞业范围或补偿明显不当"
      ],
      "query_patterns": [
        "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。"
      ],
      "query_semantic_target": "竞业范围或补偿明显不当",
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
        "C0039",
        "C0040"
      ],
      "search_corpus_chunks": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "text": "劳动合同（通用）",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "text": "一、劳动合同期限",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。\n合同期限自2026年9月15日起至2028年9月14日止。\n试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。\n岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。\n乙方主要工作地点为深圳市南山区。\n因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。\n岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。\n正常工作时间为周一至周五9:00—18:00，中午休息1小时。\n因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。\n双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。\n甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0010",
          "location": "第四条",
          "text": "第四条\n乙方依法享有法定节假日、年休假、婚假、产假、丧假等假期。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0011",
          "location": "四、劳动报酬",
          "text": "四、劳动报酬",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0012",
          "location": "第五条",
          "text": "第五条\n乙方每月正常工作时间工资为人民币18,000元，其中：\n基本工资：8,000元/月；\n岗位工资：6,000元/月；\n绩效工资：4,000元/月。\n甲方于每月15日前通过银行转账方式支付乙方上一个自然月工资。\n绩效工资根据甲方每月绩效考核结果发放，甲方有权根据经营状况及乙方工作表现调整绩效工资标准。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0013",
          "location": "第六条",
          "text": "第六条\n乙方试用期工资为人民币14,000元/月。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0014",
          "location": "第七条",
          "text": "第七条\n乙方迟到、早退、请假或未完成公司规定的工作任务时，甲方可以按照公司规章制度扣减相应工资或绩效奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0015",
          "location": "五、社会保险和福利待遇",
          "text": "五、社会保险和福利待遇",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0016",
          "location": "第八条",
          "text": "第八条\n甲乙双方依法参加社会保险。\n经乙方申请，在试用期内甲方暂不为乙方缴纳社会保险，甲方每月向乙方发放人民币1,500元社会保险补贴，由乙方自行办理相关社会保障事项。\n乙方转正后，甲方按照公司统一标准为乙方办理社会保险。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0017",
          "location": "第九条",
          "text": "第九条\n住房公积金按照甲方现行规章制度及当地政策执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0018",
          "location": "六、职业培训和劳动保护",
          "text": "六、职业培训和劳动保护",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0019",
          "location": "第十条",
          "text": "第十条\n甲方根据岗位需要向乙方提供必要的职业技能培训。\n如甲方为乙方提供专项培训，培训费用超过人民币20,000元的，双方可以另行签署培训服务期协议。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0020",
          "location": "第十一条",
          "text": "第十一条\n乙方应遵守甲方的信息安全、数据安全及劳动安全管理制度，不得擅自复制、下载或者向第三方披露甲方业务数据。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0021",
          "location": "七、劳动合同的变更、解除和终止",
          "text": "七、劳动合同的变更、解除和终止",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0022",
          "location": "第十二条",
          "text": "第十二条\n甲乙双方协商一致，可以变更劳动合同内容。\n但因甲方组织架构调整、经营模式变化、项目取消或岗位需求变化，甲方可根据经营管理需要调整乙方岗位、工作内容和工作地点。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0023",
          "location": "第十三条",
          "text": "第十三条\n乙方主动辞职，应至少提前60日以书面形式通知甲方。\n未经甲方批准，乙方不得自行离职。\n乙方未完成工作交接或者存在公司财物、账号、源代码、资料未归还情形的，甲方有权暂缓办理离职手续及支付乙方尚未结算的工资、奖金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0024",
          "location": "第十四条",
          "text": "第十四条\n乙方存在严重违反公司规章制度、严重失职、营私舞弊或者其他依法可以解除劳动合同情形的，甲方可以依法解除劳动合同。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0025",
          "location": "八、保密及竞业限制",
          "text": "八、保密及竞业限制",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0026",
          "location": "第十五条",
          "text": "第十五条\n乙方在任职期间知悉的甲方源代码、算法、技术方案、产品规划、客户信息、价格体系、业务数据、财务资料等均属于甲方商业秘密。\n未经甲方书面同意，乙方不得向任何第三方披露或使用。\n保密义务不因劳动合同解除或终止而终止。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0028",
          "location": "九、知识产权",
          "text": "九、知识产权",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0029",
          "location": "第十七条",
          "text": "第十七条\n乙方在任职期间因履行工作职责或者主要利用甲方设备、资金、数据、技术资料完成的软件程序、源代码、技术方案、产品设计及其他工作成果，其知识产权按照法律规定及甲方相关制度处理。\n乙方应根据甲方要求配合办理有关知识产权登记、申请及权利确认手续。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0030",
          "location": "十、双方约定的其他事项",
          "text": "十、双方约定的其他事项",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0031",
          "location": "第十八条",
          "text": "第十八条\n甲方依法制定并向乙方公示的《员工手册》《考勤管理制度》《绩效考核制度》《信息安全管理制度》等规章制度，作为本合同附件，与本合同具有相应效力。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0032",
          "location": "第十九条",
          "text": "第十九条\n乙方确认本合同所填写的联系电话和通讯地址真实有效。\n甲方向上述地址邮寄劳动关系相关文件，自邮件寄出之日起第三日视为已经送达，无论乙方是否实际签收。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0033",
          "location": "第二十条",
          "text": "第二十条\n乙方对甲方负有的赔偿责任、违约金或其他应付款项，甲方可以直接从乙方工资、奖金、报销款或其他应付款中抵扣。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0034",
          "location": "十一、劳动争议处理",
          "text": "十一、劳动争议处理",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0035",
          "location": "第二十一条",
          "text": "第二十一条\n甲乙双方因履行本合同发生劳动争议，可以协商解决；协商不成的，任何一方均可依法申请劳动争议仲裁。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0036",
          "location": "十二、其他",
          "text": "十二、其他",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0037",
          "location": "第二十二条",
          "text": "第二十二条\n本合同未尽事宜，按照国家及深圳市现行法律法规执行。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0038",
          "location": "第二十三条",
          "text": "第二十三条\n本合同一式两份，甲乙双方各执一份，自双方签字或盖章之日起生效。",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0039",
          "location": "甲方（盖章）：深圳市启明智能科技有限公司",
          "text": "甲方（盖章）：深圳市启明智能科技有限公司\n法定代表人或委托代理人：周明远\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        },
        {
          "clause_id": "C0040",
          "location": "乙方（签字）：陈泽宇",
          "text": "乙方（签字）：陈泽宇\n签订日期：2026年9月12日",
          "section_type": "正式合同条款"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "title": "第十六条",
          "text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "original_excerpt": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "source_start": 79,
          "source_end": 137,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": true,
          "score": 1.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [
            "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。"
          ],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "FOUND"
        },
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "劳动合同（通用）",
          "quote": "劳动合同（通用）",
          "original_excerpt": "劳动合同（通用）",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0002",
          "location": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "title": "甲方（用人单位）：深圳市启明智能科技有限公司",
          "text": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "quote": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "original_excerpt": "甲方（用人单位）：深圳市启明智能科技有限公司\n统一社会信用代码：91440300MA5H8Q672X\n法定代表人（主要负责人）：周明远\n注册地址：深圳市南山区科技园科苑路88号启明大厦12层\n经营地：深圳市南山区高新南七道18号创新中心A座9层\n联系电话：0755-86751236",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 141,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0003",
          "location": "乙方（劳动者）：陈泽宇",
          "title": "乙方（劳动者）：陈泽宇",
          "text": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "quote": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "original_excerpt": "乙方（劳动者）：陈泽宇\n居民身份证号码：440305199506182418\n户籍地址：广东省惠州市惠城区江北街道云山路26号\n经常居住地（通讯地址）：深圳市宝安区新安街道创业二路168号星河公寓3栋806室\n联系电话：13826581742\n根据《中华人民共和国劳动法》《中华人民共和国劳动合同法》等法律法规政策规定，甲乙双方遵循合法、公平、平等自愿、协商一致、诚实信用的原则订立本合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 195,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0004",
          "location": "一、劳动合同期限",
          "title": "劳动合同期限",
          "text": "一、劳动合同期限",
          "quote": "一、劳动合同期限",
          "original_excerpt": "一、劳动合同期限",
          "section_type": "正式合同条款",
          "heading_path": [
            "一、劳动合同期限"
          ],
          "source_start": 0,
          "source_end": 8,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "quote": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "original_excerpt": "第一条\n甲乙双方约定采用固定期限劳动合同。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 0,
          "source_end": 21,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "合同期限自2026年9月15日起至2028年9月14日止。",
          "quote": "合同期限自2026年9月15日起至2028年9月14日止。",
          "original_excerpt": "合同期限自2026年9月15日起至2028年9月14日止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 21,
          "source_end": 51,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0005",
          "location": "第一条",
          "title": "第一条",
          "text": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "quote": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "original_excerpt": "试用期自2026年9月15日起至2026年12月14日止，共3个月。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一条"
          ],
          "source_start": 51,
          "source_end": 86,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0006",
          "location": "二、工作内容和工作地点",
          "title": "工作内容和工作地点",
          "text": "二、工作内容和工作地点",
          "quote": "二、工作内容和工作地点",
          "original_excerpt": "二、工作内容和工作地点",
          "section_type": "正式合同条款",
          "heading_path": [
            "二、工作内容和工作地点"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "第二条\n乙方工作岗位为软件开发工程师。",
          "quote": "第二条\n乙方工作岗位为软件开发工程师。",
          "original_excerpt": "第二条\n乙方工作岗位为软件开发工程师。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 0,
          "source_end": 19,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "quote": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "original_excerpt": "岗位职责包括：\n负责公司企业管理平台后端系统开发、维护及性能优化；\n负责相关API接口设计及数据库设计；\n配合产品、测试及运维人员完成系统上线；\n完成甲方根据经营需要安排的其他相关工作。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 19,
          "source_end": 113,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "乙方主要工作地点为深圳市南山区。",
          "quote": "乙方主要工作地点为深圳市南山区。",
          "original_excerpt": "乙方主要工作地点为深圳市南山区。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 113,
          "source_end": 130,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "quote": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "original_excerpt": "因公司业务需要，甲方有权根据经营情况、乙方工作能力及项目安排，将乙方调整至深圳市其他办公地点、关联公司或其他岗位工作，乙方应予服从。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 130,
          "source_end": 197,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0007",
          "location": "第二条",
          "title": "第二条",
          "text": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "quote": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "original_excerpt": "岗位调整后，甲方可以根据新岗位情况相应调整乙方工资待遇，无需另行取得乙方书面同意。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二条"
          ],
          "source_start": 197,
          "source_end": 239,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0008",
          "location": "三、工作时间和休息休假",
          "title": "工作时间和休息休假",
          "text": "三、工作时间和休息休假",
          "quote": "三、工作时间和休息休假",
          "original_excerpt": "三、工作时间和休息休假",
          "section_type": "正式合同条款",
          "heading_path": [
            "三、工作时间和休息休假"
          ],
          "source_start": 0,
          "source_end": 11,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "第三条\n乙方实行标准工时工作制。",
          "quote": "第三条\n乙方实行标准工时工作制。",
          "original_excerpt": "第三条\n乙方实行标准工时工作制。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 0,
          "source_end": 16,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "quote": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "original_excerpt": "正常工作时间为周一至周五9:00—18:00，中午休息1小时。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 16,
          "source_end": 48,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "quote": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "original_excerpt": "因项目上线、客户交付等需要，乙方应服从甲方安排进行延时工作或周末加班。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 48,
          "source_end": 84,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "quote": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "original_excerpt": "双方确认，乙方月工资中已经综合考虑工作岗位可能发生的延时工作，加班时间原则上不再另行支付加班工资。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 84,
          "source_end": 134,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        },
        {
          "clause_id": "C0009",
          "location": "第三条",
          "title": "第三条",
          "text": "甲方可根据项目情况安排乙方调休。",
          "quote": "甲方可根据项目情况安排乙方调休。",
          "original_excerpt": "甲方可根据项目情况安排乙方调休。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三条"
          ],
          "source_start": 134,
          "source_end": 151,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "accepted": false,
          "score": 0.0,
          "threshold": "ALL_REQUIRED_RELATIONS",
          "relation_slots": [],
          "matched_patterns": [],
          "rejected_patterns": [],
          "decision_function": "review_v2.lease_semantics.supports",
          "result": "NOT_FOUND"
        }
      ],
      "candidate_count": 64,
      "stage_results": {
        "normalize": "CANONICAL_CANDIDATE",
        "threshold": "PASS"
      },
      "searched_document_hash": "d600ccab7eb9f16a25c48fda93df38378eead93a6245fdf90d5229312313eafb",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0027",
          "location": "第十六条",
          "title": "第十六条",
          "text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "original_excerpt": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第十六条"
          ],
          "source_start": 79,
          "source_end": 137,
          "supports_element_ids": [
            "employment_noncompete_adverse_adverse"
          ],
          "source_type": "CONTRACT_TEXT",
          "entailment_score": 95,
          "selection_reason": "DIRECT_SEMANTIC_SUPPORT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0027",
      "location": "第十六条",
      "title": "第十六条",
      "text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
      "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
      "section_type": "正式合同条款",
      "block_type": "OPERATIVE_CLAUSE",
      "predicate": "甲方无需另行向乙方支付竞业限制经济补偿",
      "polarity": "AFFIRMED",
      "supports_element_ids": [
        "employment_noncompete_adverse_adverse"
      ],
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第十六条",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "第十六条\n乙方离职后二年内，不得自行经营或到与甲方存在竞争关系的企业任职，包括但不限于从事人工智能软件、企业SaaS系统、跨境电商软件及自动化平台业务的企业。\n双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。\n乙方违反竞业限制义务的，应向甲方一次性支付人民币300,000元违约金。",
      "source_span": {
        "start_offset": 1904,
        "end_offset": 1961,
        "raw_text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
        "coordinate_system": "DOCUMENT_TEXT"
      },
      "source_start": 1904,
      "source_end": 1961,
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0027",
        "section": "第十六条",
        "sentence_index": 1,
        "quote": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": 1904,
          "end_offset": 1961,
          "raw_text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
          "coordinate_system": "DOCUMENT_TEXT"
        },
        "derived_or_original": "ORIGINAL",
        "source_ref": {
          "document_id": "contract_package/main",
          "clause_id": "C0027",
          "clause_sha256": "309351d51f3f725f5e33274c84599999e87c97732bce7ae98e1f068fb74558c4",
          "local_start": 80,
          "local_end": 137,
          "locator": "第十六条"
        },
        "verified_original": true
      },
      "evidence_polarity": "NEUTRAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_noncompete_adverse_adverse"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "NC-03-01",
      "element_ids": [
        "employment_noncompete_adverse_adverse"
      ],
      "support_type": "DIRECT",
      "verified_original": true,
      "source_verification": {
        "status": "PASS",
        "errors": [],
        "method": "EXACT_PARSER_SOURCE_SPAN"
      },
      "evidence_id": "SRC-355619768b1ddd44903e",
      "quoted_text": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
      "original_excerpt": "双方确认，乙方在职期间取得的工资待遇中已经包含竞业限制补偿，劳动关系终止后甲方无需另行向乙方支付竞业限制经济补偿。",
      "source_ref": {
        "document_id": "contract_package/main",
        "clause_id": "C0027",
        "clause_sha256": "309351d51f3f725f5e33274c84599999e87c97732bce7ae98e1f068fb74558c4",
        "local_start": 80,
        "local_end": 137,
        "locator": "第十六条"
      },
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "竞业范围或补偿明显不当"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
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
    "applicability_state": "REQUIRED_ALWAYS",
    "premise_evidence": [],
    "premise_fact_ids": [],
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
      "C0039",
      "C0040"
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
    "high_finding_count": 5,
    "core_priority_count": 5,
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
    "ADVERSE_POLARITY_AUDIT_GATE": "PASS",
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
    "CANONICAL_SEMANTIC_PROOF_GATE": "PASS",
    "VERIFIED_PASS_ORIGINAL_GATE": "PASS",
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