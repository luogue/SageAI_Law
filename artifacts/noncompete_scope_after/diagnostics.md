# 劳动合同逐项证据诊断

输入文件：60 竞业限制协议.docx
输入 SHA256：58a2b6704af3dd1ad30e713333fc1c5214b7be46aa190af7a5d2f52b38e8d28b
normalized SHA256：a65d3df62524dd61079857baf2978256c5bf36605252e91716e19a1c8b1a3eba

| rule_id | 最终状态 | 理由 |
|---|---|---|
| EMP-01-01 | PASS | 合同原文覆盖全部专项要素。 |
| NC-01-01 | PARTIAL | 未找到明确约定：人员范围及实际接触秘密。 |
| NC-02-01 | PASS | 合同原文覆盖全部专项要素。 |
| NC-03-01 | 待核验 | 合理性判断所需事实尚不完整：人员范围及实际接触秘密、劳动者具体岗位；应结合实际接触秘密及约定范围核验，不能据此直接认定范围合理或违法。 |
| EMP-12-01 | PASS | 合同原文覆盖全部专项要素。 |
| EMP-14-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |

## 全部 SEARCH_AUDIT NOT FOUND

```json
[
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
      "C0040",
      "C0041",
      "C0042",
      "C0043",
      "C0044",
      "C0045",
      "C0046",
      "C0047",
      "C0048",
      "C0049",
      "C0050",
      "C0051",
      "C0052",
      "C0053"
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
        "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
      },
      {
        "clause_id": "C0002",
        "location": "第1项",
        "title": "1. 释义",
        "section_type": "正式合同条款",
        "heading_path": [
          "1. 释义"
        ],
        "text": "1. 释义"
      },
      {
        "clause_id": "C0003",
        "location": "1.1",
        "title": "1.1 竞业限制期：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1.1 竞业限制期："
        ],
        "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
      },
      {
        "clause_id": "C0004",
        "location": "1.2",
        "title": "1.2 甲方竞争对手：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1.2 甲方竞争对手："
        ],
        "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
      },
      {
        "clause_id": "C0005",
        "location": "1.3",
        "title": "1.3 竞争行为：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1.3 竞争行为："
        ],
        "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
      },
      {
        "clause_id": "C0006",
        "location": "1.4",
        "title": "1.4 甲方的机密信息：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1.4 甲方的机密信息："
        ],
        "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
      },
      {
        "clause_id": "C0007",
        "location": "第1项",
        "title": "1.5",
        "section_type": "正式合同条款",
        "heading_path": [
          "1.5"
        ],
        "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
      },
      {
        "clause_id": "C0008",
        "location": "1.6",
        "title": "1.6 甲方客户：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1.6 甲方客户："
        ],
        "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
      },
      {
        "clause_id": "C0009",
        "location": "第2项",
        "title": "2. 在职期间竞业限制义务",
        "section_type": "正式合同条款",
        "heading_path": [
          "2. 在职期间竞业限制义务"
        ],
        "text": "2. 在职期间竞业限制义务"
      },
      {
        "clause_id": "C0010",
        "location": "第2项",
        "title": "2.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "2.1"
        ],
        "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
      },
      {
        "clause_id": "C0011",
        "location": "第2项",
        "title": "2.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "2.2"
        ],
        "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
      },
      {
        "clause_id": "C0012",
        "location": "第2项",
        "title": "2.3",
        "section_type": "正式合同条款",
        "heading_path": [
          "2.3"
        ],
        "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
      },
      {
        "clause_id": "C0013",
        "location": "第2项",
        "title": "2.4",
        "section_type": "正式合同条款",
        "heading_path": [
          "2.4"
        ],
        "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
      },
      {
        "clause_id": "C0014",
        "location": "第3项",
        "title": "3. 离职后竞业限制义务",
        "section_type": "正式合同条款",
        "heading_path": [
          "3. 离职后竞业限制义务"
        ],
        "text": "3. 离职后竞业限制义务"
      },
      {
        "clause_id": "C0015",
        "location": "第3项",
        "title": "3.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.1"
        ],
        "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
      },
      {
        "clause_id": "C0016",
        "location": "第3项",
        "title": "3.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.2"
        ],
        "text": "3.2\n乙方在离职后的 2年内 不得："
      },
      {
        "clause_id": "C0017",
        "location": "第3.2项",
        "title": "3.2.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.2.1"
        ],
        "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
      },
      {
        "clause_id": "C0018",
        "location": "第3.2项",
        "title": "3.2.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.2.2"
        ],
        "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
      },
      {
        "clause_id": "C0019",
        "location": "第3.2项",
        "title": "3.2.3",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.2.3"
        ],
        "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
      },
      {
        "clause_id": "C0020",
        "location": "第3.2项",
        "title": "3.2.4",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.2.4"
        ],
        "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
      },
      {
        "clause_id": "C0021",
        "location": "第3项",
        "title": "3.3",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.3"
        ],
        "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
      },
      {
        "clause_id": "C0022",
        "location": "第3项",
        "title": "3.4",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.4"
        ],
        "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
      },
      {
        "clause_id": "C0023",
        "location": "第3项",
        "title": "3.5",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.5"
        ],
        "text": "3.5\n本条所称关联企业，界定如下："
      },
      {
        "clause_id": "C0024",
        "location": "第3.5项",
        "title": "3.5.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.5.1"
        ],
        "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
      },
      {
        "clause_id": "C0025",
        "location": "第3.5项",
        "title": "3.5.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.5.2"
        ],
        "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
      },
      {
        "clause_id": "C0026",
        "location": "第3.5项",
        "title": "3.5.3",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.5.3"
        ],
        "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
      },
      {
        "clause_id": "C0027",
        "location": "第3.5项",
        "title": "3.5.4",
        "section_type": "正式合同条款",
        "heading_path": [
          "3.5.4"
        ],
        "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
      },
      {
        "clause_id": "C0028",
        "location": "第4项",
        "title": "4. 竞业限制的地域",
        "section_type": "正式合同条款",
        "heading_path": [
          "4. 竞业限制的地域"
        ],
        "text": "4. 竞业限制的地域"
      },
      {
        "clause_id": "C0029",
        "location": "第4项",
        "title": "4.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "4.1"
        ],
        "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
      },
      {
        "clause_id": "C0030",
        "location": "第4项",
        "title": "4.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "4.2"
        ],
        "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
      },
      {
        "clause_id": "C0031",
        "location": "第5项",
        "title": "5. 经济补偿金",
        "section_type": "正式合同条款",
        "heading_path": [
          "5. 经济补偿金"
        ],
        "text": "5. 经济补偿金"
      },
      {
        "clause_id": "C0032",
        "location": "第5项",
        "title": "5.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "5.1"
        ],
        "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
      },
      {
        "clause_id": "C0033",
        "location": "第5项",
        "title": "5.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "5.2"
        ],
        "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
      },
      {
        "clause_id": "C0034",
        "location": "第5项",
        "title": "5.3",
        "section_type": "正式合同条款",
        "heading_path": [
          "5.3"
        ],
        "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
      },
      {
        "clause_id": "C0035",
        "location": "第5项",
        "title": "5.4",
        "section_type": "正式合同条款",
        "heading_path": [
          "5.4"
        ],
        "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
      },
      {
        "clause_id": "C0036",
        "location": "第6项",
        "title": "6. 协议解除",
        "section_type": "正式合同条款",
        "heading_path": [
          "6. 协议解除"
        ],
        "text": "6. 协议解除"
      },
      {
        "clause_id": "C0037",
        "location": "第6项",
        "title": "6.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "6.1"
        ],
        "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
      },
      {
        "clause_id": "C0038",
        "location": "第6项",
        "title": "6.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "6.2"
        ],
        "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
      },
      {
        "clause_id": "C0039",
        "location": "第6项",
        "title": "6.3",
        "section_type": "正式合同条款",
        "heading_path": [
          "6.3"
        ],
        "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
      },
      {
        "clause_id": "C0040",
        "location": "第7项",
        "title": "7. 违约责任",
        "section_type": "正式合同条款",
        "heading_path": [
          "7. 违约责任"
        ],
        "text": "7. 违约责任"
      },
      {
        "clause_id": "C0041",
        "location": "第7项",
        "title": "7.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "7.1"
        ],
        "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
      },
      {
        "clause_id": "C0042",
        "location": "第7项",
        "title": "7.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "7.2"
        ],
        "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
      },
      {
        "clause_id": "C0043",
        "location": "第7项",
        "title": "7.3",
        "section_type": "正式合同条款",
        "heading_path": [
          "7.3"
        ],
        "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
      },
      {
        "clause_id": "C0044",
        "location": "第8项",
        "title": "8. 争议解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "8. 争议解决"
        ],
        "text": "8. 争议解决"
      },
      {
        "clause_id": "C0045",
        "location": "第8项",
        "title": "8.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "8.1"
        ],
        "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
      },
      {
        "clause_id": "C0046",
        "location": "第8项",
        "title": "8.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "8.2"
        ],
        "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
      },
      {
        "clause_id": "C0047",
        "location": "第8项",
        "title": "8.3",
        "section_type": "正式合同条款",
        "heading_path": [
          "8.3"
        ],
        "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
      },
      {
        "clause_id": "C0048",
        "location": "第9项",
        "title": "9. 其他事项",
        "section_type": "正式合同条款",
        "heading_path": [
          "9. 其他事项"
        ],
        "text": "9. 其他事项"
      },
      {
        "clause_id": "C0049",
        "location": "第9项",
        "title": "9.1",
        "section_type": "正式合同条款",
        "heading_path": [
          "9.1"
        ],
        "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
      },
      {
        "clause_id": "C0050",
        "location": "第9项",
        "title": "9.2",
        "section_type": "正式合同条款",
        "heading_path": [
          "9.2"
        ],
        "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
      },
      {
        "clause_id": "C0051",
        "location": "第9项",
        "title": "9.3",
        "section_type": "正式合同条款",
        "heading_path": [
          "9.3"
        ],
        "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
      },
      {
        "clause_id": "C0052",
        "location": "甲方（盖章）：上海律智人工智能科技有限公司",
        "title": "甲方（盖章）：上海律智人工智能科技有限公司",
        "section_type": "正式合同条款",
        "heading_path": [
          "9.3"
        ],
        "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
      },
      {
        "clause_id": "C0053",
        "location": "乙方（签字）：陈浩然",
        "title": "乙方（签字）：陈浩然",
        "section_type": "正式合同条款",
        "heading_path": [
          "9.3"
        ],
        "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
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
        "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。",
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
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
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
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。",
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
        "clause_id": "C0001",
        "location": "全文",
        "title": "全文",
        "section_type": "正式合同条款",
        "heading_path": [
          "全文"
        ],
        "text": "依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
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
        "location": "第1项",
        "title": "1. 释义",
        "section_type": "正式合同条款",
        "heading_path": [
          "1. 释义"
        ],
        "text": "1. 释义",
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
        "location": "1.1",
        "title": "1.1 竞业限制期：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1.1 竞业限制期："
        ],
        "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
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
        "location": "1.2",
        "title": "1.2 甲方竞争对手：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1.2 甲方竞争对手："
        ],
        "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
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
        "location": "1.3",
        "title": "1.3 竞争行为：",
        "section_type": "正式合同条款",
        "heading_path": [
          "1.3 竞争行为："
        ],
        "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。",
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
    "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NC-03-01",
    "element_id": "core_contract_arrangement",
    "review_id": "NC-03-01",
    "search_targets": [
      "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容"
    ],
    "query_patterns": [
      "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容"
    ],
    "query_semantics": "POSITIVE_REQUIRED_FACT",
    "search_mode": "OBJECTIVE_LITERAL_TARGET",
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
      "C0040",
      "C0041",
      "C0042",
      "C0043",
      "C0044",
      "C0045",
      "C0046",
      "C0047",
      "C0048",
      "C0049",
      "C0050",
      "C0051",
      "C0052",
      "C0053"
    ],
    "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
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
        "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
        "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
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
          "quote": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。"
        },
        {
          "clause_id": "C0001",
          "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        }
      ]
    },
    {
      "review_id": "EMP-01-01",
      "element_id": "employment_identity_2",
      "proposition": "劳动者姓名与身份证明",
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
        "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
        "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
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
          "quote": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。"
        },
        {
          "clause_id": "C0001",
          "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
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
        "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
        "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
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
          "quote": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。"
        },
        {
          "clause_id": "C0001",
          "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
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
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义"
        },
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
        },
        {
          "clause_id": "C0006",
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
        },
        {
          "clause_id": "C0007",
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
        },
        {
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
        },
        {
          "clause_id": "C0009",
          "location": "第2项",
          "title": "2. 在职期间竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "2. 在职期间竞业限制义务"
          ],
          "text": "2. 在职期间竞业限制义务"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        {
          "clause_id": "C0012",
          "location": "第2项",
          "title": "2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.3"
          ],
          "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
        },
        {
          "clause_id": "C0013",
          "location": "第2项",
          "title": "2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.4"
          ],
          "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
        },
        {
          "clause_id": "C0014",
          "location": "第3项",
          "title": "3. 离职后竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "3. 离职后竞业限制义务"
          ],
          "text": "3. 离职后竞业限制义务"
        },
        {
          "clause_id": "C0015",
          "location": "第3项",
          "title": "3.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.1"
          ],
          "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
        },
        {
          "clause_id": "C0016",
          "location": "第3项",
          "title": "3.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2"
          ],
          "text": "3.2\n乙方在离职后的 2年内 不得："
        },
        {
          "clause_id": "C0017",
          "location": "第3.2项",
          "title": "3.2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.1"
          ],
          "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
        },
        {
          "clause_id": "C0018",
          "location": "第3.2项",
          "title": "3.2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.2"
          ],
          "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
        },
        {
          "clause_id": "C0019",
          "location": "第3.2项",
          "title": "3.2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.3"
          ],
          "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
        },
        {
          "clause_id": "C0020",
          "location": "第3.2项",
          "title": "3.2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.4"
          ],
          "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
        },
        {
          "clause_id": "C0021",
          "location": "第3项",
          "title": "3.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.3"
          ],
          "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
        },
        {
          "clause_id": "C0022",
          "location": "第3项",
          "title": "3.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.4"
          ],
          "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
        },
        {
          "clause_id": "C0023",
          "location": "第3项",
          "title": "3.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5"
          ],
          "text": "3.5\n本条所称关联企业，界定如下："
        },
        {
          "clause_id": "C0024",
          "location": "第3.5项",
          "title": "3.5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.1"
          ],
          "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
        },
        {
          "clause_id": "C0025",
          "location": "第3.5项",
          "title": "3.5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.2"
          ],
          "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
        },
        {
          "clause_id": "C0026",
          "location": "第3.5项",
          "title": "3.5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.3"
          ],
          "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
        },
        {
          "clause_id": "C0027",
          "location": "第3.5项",
          "title": "3.5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.4"
          ],
          "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
        },
        {
          "clause_id": "C0028",
          "location": "第4项",
          "title": "4. 竞业限制的地域",
          "section_type": "正式合同条款",
          "heading_path": [
            "4. 竞业限制的地域"
          ],
          "text": "4. 竞业限制的地域"
        },
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        {
          "clause_id": "C0030",
          "location": "第4项",
          "title": "4.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.2"
          ],
          "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
        },
        {
          "clause_id": "C0031",
          "location": "第5项",
          "title": "5. 经济补偿金",
          "section_type": "正式合同条款",
          "heading_path": [
            "5. 经济补偿金"
          ],
          "text": "5. 经济补偿金"
        },
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
        },
        {
          "clause_id": "C0033",
          "location": "第5项",
          "title": "5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.2"
          ],
          "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
        },
        {
          "clause_id": "C0034",
          "location": "第5项",
          "title": "5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.3"
          ],
          "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
        },
        {
          "clause_id": "C0035",
          "location": "第5项",
          "title": "5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.4"
          ],
          "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
        },
        {
          "clause_id": "C0036",
          "location": "第6项",
          "title": "6. 协议解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "6. 协议解除"
          ],
          "text": "6. 协议解除"
        },
        {
          "clause_id": "C0037",
          "location": "第6项",
          "title": "6.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.1"
          ],
          "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
        },
        {
          "clause_id": "C0038",
          "location": "第6项",
          "title": "6.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.2"
          ],
          "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
        },
        {
          "clause_id": "C0039",
          "location": "第6项",
          "title": "6.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.3"
          ],
          "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
        },
        {
          "clause_id": "C0040",
          "location": "第7项",
          "title": "7. 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "7. 违约责任"
          ],
          "text": "7. 违约责任"
        },
        {
          "clause_id": "C0041",
          "location": "第7项",
          "title": "7.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.1"
          ],
          "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
        },
        {
          "clause_id": "C0042",
          "location": "第7项",
          "title": "7.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.2"
          ],
          "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
        },
        {
          "clause_id": "C0043",
          "location": "第7项",
          "title": "7.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.3"
          ],
          "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
        },
        {
          "clause_id": "C0044",
          "location": "第8项",
          "title": "8. 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "8. 争议解决"
          ],
          "text": "8. 争议解决"
        },
        {
          "clause_id": "C0045",
          "location": "第8项",
          "title": "8.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.1"
          ],
          "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
        },
        {
          "clause_id": "C0046",
          "location": "第8项",
          "title": "8.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.2"
          ],
          "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
        },
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
        },
        {
          "clause_id": "C0048",
          "location": "第9项",
          "title": "9. 其他事项",
          "section_type": "正式合同条款",
          "heading_path": [
            "9. 其他事项"
          ],
          "text": "9. 其他事项"
        },
        {
          "clause_id": "C0049",
          "location": "第9项",
          "title": "9.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.1"
          ],
          "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
        },
        {
          "clause_id": "C0050",
          "location": "第9项",
          "title": "9.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.2"
          ],
          "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
        },
        {
          "clause_id": "C0051",
          "location": "第9项",
          "title": "9.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
        },
        {
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
        },
        {
          "clause_id": "C0053",
          "location": "乙方（签字）：陈浩然",
          "title": "乙方（签字）：陈浩然",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
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
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
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
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义",
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
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
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
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
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
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。",
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
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
          "quote": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
          "original_excerpt": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 40,
          "source_end": 289,
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
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义"
        },
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
        },
        {
          "clause_id": "C0006",
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
        },
        {
          "clause_id": "C0007",
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
        },
        {
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
        },
        {
          "clause_id": "C0009",
          "location": "第2项",
          "title": "2. 在职期间竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "2. 在职期间竞业限制义务"
          ],
          "text": "2. 在职期间竞业限制义务"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        {
          "clause_id": "C0012",
          "location": "第2项",
          "title": "2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.3"
          ],
          "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
        },
        {
          "clause_id": "C0013",
          "location": "第2项",
          "title": "2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.4"
          ],
          "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
        },
        {
          "clause_id": "C0014",
          "location": "第3项",
          "title": "3. 离职后竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "3. 离职后竞业限制义务"
          ],
          "text": "3. 离职后竞业限制义务"
        },
        {
          "clause_id": "C0015",
          "location": "第3项",
          "title": "3.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.1"
          ],
          "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
        },
        {
          "clause_id": "C0016",
          "location": "第3项",
          "title": "3.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2"
          ],
          "text": "3.2\n乙方在离职后的 2年内 不得："
        },
        {
          "clause_id": "C0017",
          "location": "第3.2项",
          "title": "3.2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.1"
          ],
          "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
        },
        {
          "clause_id": "C0018",
          "location": "第3.2项",
          "title": "3.2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.2"
          ],
          "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
        },
        {
          "clause_id": "C0019",
          "location": "第3.2项",
          "title": "3.2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.3"
          ],
          "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
        },
        {
          "clause_id": "C0020",
          "location": "第3.2项",
          "title": "3.2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.4"
          ],
          "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
        },
        {
          "clause_id": "C0021",
          "location": "第3项",
          "title": "3.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.3"
          ],
          "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
        },
        {
          "clause_id": "C0022",
          "location": "第3项",
          "title": "3.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.4"
          ],
          "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
        },
        {
          "clause_id": "C0023",
          "location": "第3项",
          "title": "3.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5"
          ],
          "text": "3.5\n本条所称关联企业，界定如下："
        },
        {
          "clause_id": "C0024",
          "location": "第3.5项",
          "title": "3.5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.1"
          ],
          "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
        },
        {
          "clause_id": "C0025",
          "location": "第3.5项",
          "title": "3.5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.2"
          ],
          "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
        },
        {
          "clause_id": "C0026",
          "location": "第3.5项",
          "title": "3.5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.3"
          ],
          "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
        },
        {
          "clause_id": "C0027",
          "location": "第3.5项",
          "title": "3.5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.4"
          ],
          "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
        },
        {
          "clause_id": "C0028",
          "location": "第4项",
          "title": "4. 竞业限制的地域",
          "section_type": "正式合同条款",
          "heading_path": [
            "4. 竞业限制的地域"
          ],
          "text": "4. 竞业限制的地域"
        },
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        {
          "clause_id": "C0030",
          "location": "第4项",
          "title": "4.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.2"
          ],
          "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
        },
        {
          "clause_id": "C0031",
          "location": "第5项",
          "title": "5. 经济补偿金",
          "section_type": "正式合同条款",
          "heading_path": [
            "5. 经济补偿金"
          ],
          "text": "5. 经济补偿金"
        },
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
        },
        {
          "clause_id": "C0033",
          "location": "第5项",
          "title": "5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.2"
          ],
          "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
        },
        {
          "clause_id": "C0034",
          "location": "第5项",
          "title": "5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.3"
          ],
          "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
        },
        {
          "clause_id": "C0035",
          "location": "第5项",
          "title": "5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.4"
          ],
          "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
        },
        {
          "clause_id": "C0036",
          "location": "第6项",
          "title": "6. 协议解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "6. 协议解除"
          ],
          "text": "6. 协议解除"
        },
        {
          "clause_id": "C0037",
          "location": "第6项",
          "title": "6.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.1"
          ],
          "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
        },
        {
          "clause_id": "C0038",
          "location": "第6项",
          "title": "6.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.2"
          ],
          "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
        },
        {
          "clause_id": "C0039",
          "location": "第6项",
          "title": "6.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.3"
          ],
          "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
        },
        {
          "clause_id": "C0040",
          "location": "第7项",
          "title": "7. 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "7. 违约责任"
          ],
          "text": "7. 违约责任"
        },
        {
          "clause_id": "C0041",
          "location": "第7项",
          "title": "7.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.1"
          ],
          "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
        },
        {
          "clause_id": "C0042",
          "location": "第7项",
          "title": "7.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.2"
          ],
          "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
        },
        {
          "clause_id": "C0043",
          "location": "第7项",
          "title": "7.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.3"
          ],
          "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
        },
        {
          "clause_id": "C0044",
          "location": "第8项",
          "title": "8. 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "8. 争议解决"
          ],
          "text": "8. 争议解决"
        },
        {
          "clause_id": "C0045",
          "location": "第8项",
          "title": "8.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.1"
          ],
          "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
        },
        {
          "clause_id": "C0046",
          "location": "第8项",
          "title": "8.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.2"
          ],
          "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
        },
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
        },
        {
          "clause_id": "C0048",
          "location": "第9项",
          "title": "9. 其他事项",
          "section_type": "正式合同条款",
          "heading_path": [
            "9. 其他事项"
          ],
          "text": "9. 其他事项"
        },
        {
          "clause_id": "C0049",
          "location": "第9项",
          "title": "9.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.1"
          ],
          "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
        },
        {
          "clause_id": "C0050",
          "location": "第9项",
          "title": "9.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.2"
          ],
          "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
        },
        {
          "clause_id": "C0051",
          "location": "第9项",
          "title": "9.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
        },
        {
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
        },
        {
          "clause_id": "C0053",
          "location": "乙方（签字）：陈浩然",
          "title": "乙方（签字）：陈浩然",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "乙方(?:[（(][^）)\\n]{1,15}[）)])?\\s*[：:]\\s*[\\u4e00-\\u9fff·]{2,12}(?:(?!甲方)[\\s\\S]){0,180}身份证号(?:码)?\\s*[：:]\\s*[0-9Xx*＊]{15,18}"
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
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义",
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
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
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
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
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
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
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
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。",
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
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。",
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
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。",
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
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
          "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
          "original_excerpt": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 0,
          "source_end": 555,
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
        "C0039",
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义"
        },
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
        },
        {
          "clause_id": "C0006",
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
        },
        {
          "clause_id": "C0007",
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
        },
        {
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
        },
        {
          "clause_id": "C0009",
          "location": "第2项",
          "title": "2. 在职期间竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "2. 在职期间竞业限制义务"
          ],
          "text": "2. 在职期间竞业限制义务"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        {
          "clause_id": "C0012",
          "location": "第2项",
          "title": "2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.3"
          ],
          "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
        },
        {
          "clause_id": "C0013",
          "location": "第2项",
          "title": "2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.4"
          ],
          "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
        },
        {
          "clause_id": "C0014",
          "location": "第3项",
          "title": "3. 离职后竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "3. 离职后竞业限制义务"
          ],
          "text": "3. 离职后竞业限制义务"
        },
        {
          "clause_id": "C0015",
          "location": "第3项",
          "title": "3.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.1"
          ],
          "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
        },
        {
          "clause_id": "C0016",
          "location": "第3项",
          "title": "3.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2"
          ],
          "text": "3.2\n乙方在离职后的 2年内 不得："
        },
        {
          "clause_id": "C0017",
          "location": "第3.2项",
          "title": "3.2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.1"
          ],
          "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
        },
        {
          "clause_id": "C0018",
          "location": "第3.2项",
          "title": "3.2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.2"
          ],
          "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
        },
        {
          "clause_id": "C0019",
          "location": "第3.2项",
          "title": "3.2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.3"
          ],
          "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
        },
        {
          "clause_id": "C0020",
          "location": "第3.2项",
          "title": "3.2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.4"
          ],
          "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
        },
        {
          "clause_id": "C0021",
          "location": "第3项",
          "title": "3.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.3"
          ],
          "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
        },
        {
          "clause_id": "C0022",
          "location": "第3项",
          "title": "3.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.4"
          ],
          "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
        },
        {
          "clause_id": "C0023",
          "location": "第3项",
          "title": "3.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5"
          ],
          "text": "3.5\n本条所称关联企业，界定如下："
        },
        {
          "clause_id": "C0024",
          "location": "第3.5项",
          "title": "3.5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.1"
          ],
          "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
        },
        {
          "clause_id": "C0025",
          "location": "第3.5项",
          "title": "3.5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.2"
          ],
          "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
        },
        {
          "clause_id": "C0026",
          "location": "第3.5项",
          "title": "3.5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.3"
          ],
          "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
        },
        {
          "clause_id": "C0027",
          "location": "第3.5项",
          "title": "3.5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.4"
          ],
          "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
        },
        {
          "clause_id": "C0028",
          "location": "第4项",
          "title": "4. 竞业限制的地域",
          "section_type": "正式合同条款",
          "heading_path": [
            "4. 竞业限制的地域"
          ],
          "text": "4. 竞业限制的地域"
        },
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        {
          "clause_id": "C0030",
          "location": "第4项",
          "title": "4.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.2"
          ],
          "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
        },
        {
          "clause_id": "C0031",
          "location": "第5项",
          "title": "5. 经济补偿金",
          "section_type": "正式合同条款",
          "heading_path": [
            "5. 经济补偿金"
          ],
          "text": "5. 经济补偿金"
        },
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
        },
        {
          "clause_id": "C0033",
          "location": "第5项",
          "title": "5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.2"
          ],
          "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
        },
        {
          "clause_id": "C0034",
          "location": "第5项",
          "title": "5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.3"
          ],
          "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
        },
        {
          "clause_id": "C0035",
          "location": "第5项",
          "title": "5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.4"
          ],
          "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
        },
        {
          "clause_id": "C0036",
          "location": "第6项",
          "title": "6. 协议解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "6. 协议解除"
          ],
          "text": "6. 协议解除"
        },
        {
          "clause_id": "C0037",
          "location": "第6项",
          "title": "6.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.1"
          ],
          "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
        },
        {
          "clause_id": "C0038",
          "location": "第6项",
          "title": "6.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.2"
          ],
          "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
        },
        {
          "clause_id": "C0039",
          "location": "第6项",
          "title": "6.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.3"
          ],
          "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
        },
        {
          "clause_id": "C0040",
          "location": "第7项",
          "title": "7. 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "7. 违约责任"
          ],
          "text": "7. 违约责任"
        },
        {
          "clause_id": "C0041",
          "location": "第7项",
          "title": "7.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.1"
          ],
          "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
        },
        {
          "clause_id": "C0042",
          "location": "第7项",
          "title": "7.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.2"
          ],
          "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
        },
        {
          "clause_id": "C0043",
          "location": "第7项",
          "title": "7.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.3"
          ],
          "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
        },
        {
          "clause_id": "C0044",
          "location": "第8项",
          "title": "8. 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "8. 争议解决"
          ],
          "text": "8. 争议解决"
        },
        {
          "clause_id": "C0045",
          "location": "第8项",
          "title": "8.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.1"
          ],
          "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
        },
        {
          "clause_id": "C0046",
          "location": "第8项",
          "title": "8.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.2"
          ],
          "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
        },
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
        },
        {
          "clause_id": "C0048",
          "location": "第9项",
          "title": "9. 其他事项",
          "section_type": "正式合同条款",
          "heading_path": [
            "9. 其他事项"
          ],
          "text": "9. 其他事项"
        },
        {
          "clause_id": "C0049",
          "location": "第9项",
          "title": "9.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.1"
          ],
          "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
        },
        {
          "clause_id": "C0050",
          "location": "第9项",
          "title": "9.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.2"
          ],
          "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
        },
        {
          "clause_id": "C0051",
          "location": "第9项",
          "title": "9.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
        },
        {
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
        },
        {
          "clause_id": "C0053",
          "location": "乙方（签字）：陈浩然",
          "title": "乙方（签字）：陈浩然",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
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
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
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
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
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
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。",
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
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
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
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。",
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
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。",
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
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
          "quote": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
          "original_excerpt": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "source_start": 40,
          "source_end": 289,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
          "quote": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
          "original_excerpt": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "source_start": 0,
          "source_end": 159,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "text": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。",
          "quote": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。",
          "original_excerpt": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "source_start": 50,
          "source_end": 144,
          "supports_element_ids": [
            "employment_identity_name"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "text": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
          "quote": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
          "original_excerpt": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "source_start": 144,
          "source_end": 252,
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
      "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
      "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "original_excerpt": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 41,
      "source_end": 289,
      "supports_element_ids": [
        "employment_identity_1"
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
      "raw_text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "source_span": {
        "start_offset": 41,
        "end_offset": 289,
        "raw_text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。"
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
        "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_1",
        "employment_identity_2",
        "employment_identity_name"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_1",
        "employment_identity_2",
        "employment_identity_name"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "用人单位住所",
        "劳动者姓名与身份证明",
        "用人单位名称"
      ],
      "support_summary": "证明合同已约定相关合同要素、相关合同要素、相关合同要素。"
    },
    {
      "clause_id": "C0001",
      "location": "全文",
      "title": "全文",
      "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "original_excerpt": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 0,
      "source_end": 555,
      "supports_element_ids": [
        "employment_identity_2"
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
      "raw_text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "source_span": {
        "start_offset": 0,
        "end_offset": 555,
        "raw_text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
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
        "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_1",
        "employment_identity_2",
        "employment_identity_name"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_1",
        "employment_identity_2",
        "employment_identity_name"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "用人单位住所",
        "劳动者姓名与身份证明",
        "用人单位名称"
      ],
      "support_summary": "证明合同已约定相关合同要素、相关合同要素、相关合同要素。"
    },
    {
      "clause_id": "C0001",
      "location": "全文",
      "title": "全文",
      "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
      "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "original_excerpt": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "section_type": "正式合同条款",
      "heading_path": [
        "全文"
      ],
      "source_start": 41,
      "source_end": 289,
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
      "raw_text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
      "source_span": {
        "start_offset": 41,
        "end_offset": 289,
        "raw_text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。"
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
        "quote": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_identity_1",
        "employment_identity_2",
        "employment_identity_name"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "EMP-01-01",
      "element_ids": [
        "employment_identity_1",
        "employment_identity_2",
        "employment_identity_name"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "用人单位住所",
        "劳动者姓名与身份证明",
        "用人单位名称"
      ],
      "support_summary": "证明合同已约定相关合同要素、相关合同要素、相关合同要素。"
    },
    {
      "clause_id": "C0004",
      "location": "1.2",
      "title": "1.2 甲方竞争对手：",
      "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
      "quote": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
      "original_excerpt": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
      "section_type": "正式合同条款",
      "heading_path": [
        "1.2 甲方竞争对手："
      ],
      "source_start": 640,
      "source_end": 799,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "1.2",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
      "source_span": {
        "start_offset": 640,
        "end_offset": 799,
        "raw_text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0004",
        "section": "1.2",
        "sentence_index": 1,
        "quote": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
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
      "clause_id": "C0005",
      "location": "1.3",
      "title": "1.3 竞争行为：",
      "text": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。",
      "quote": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。",
      "original_excerpt": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。",
      "section_type": "正式合同条款",
      "heading_path": [
        "1.3 竞争行为："
      ],
      "source_start": 851,
      "source_end": 944,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "1.3",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
      "source_span": {
        "start_offset": 851,
        "end_offset": 944,
        "raw_text": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0005",
        "section": "1.3",
        "sentence_index": 1,
        "quote": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。"
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
      "clause_id": "C0005",
      "location": "1.3",
      "title": "1.3 竞争行为：",
      "text": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
      "quote": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
      "original_excerpt": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
      "section_type": "正式合同条款",
      "heading_path": [
        "1.3 竞争行为："
      ],
      "source_start": 945,
      "source_end": 1052,
      "supports_element_ids": [
        "employment_identity_name"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "1.3",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
      "source_span": {
        "start_offset": 945,
        "end_offset": 1052,
        "raw_text": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0005",
        "section": "1.3",
        "sentence_index": 1,
        "quote": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
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
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "部分覆盖",
  "reason": "未找到明确约定：人员范围及实际接触秘密。",
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
        "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
      ],
      "source_locations": [
        "1.1"
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
          "quote": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        }
      ]
    },
    {
      "review_id": "NC-01-01",
      "element_id": "employment_noncompete_scope_3",
      "proposition": "明确约定竞业地域范围",
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
        "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
      ],
      "source_locations": [
        "第4项"
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
          "quote": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        }
      ]
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
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义"
        },
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
        },
        {
          "clause_id": "C0006",
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
        },
        {
          "clause_id": "C0007",
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
        },
        {
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
        },
        {
          "clause_id": "C0009",
          "location": "第2项",
          "title": "2. 在职期间竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "2. 在职期间竞业限制义务"
          ],
          "text": "2. 在职期间竞业限制义务"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        {
          "clause_id": "C0012",
          "location": "第2项",
          "title": "2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.3"
          ],
          "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
        },
        {
          "clause_id": "C0013",
          "location": "第2项",
          "title": "2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.4"
          ],
          "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
        },
        {
          "clause_id": "C0014",
          "location": "第3项",
          "title": "3. 离职后竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "3. 离职后竞业限制义务"
          ],
          "text": "3. 离职后竞业限制义务"
        },
        {
          "clause_id": "C0015",
          "location": "第3项",
          "title": "3.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.1"
          ],
          "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
        },
        {
          "clause_id": "C0016",
          "location": "第3项",
          "title": "3.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2"
          ],
          "text": "3.2\n乙方在离职后的 2年内 不得："
        },
        {
          "clause_id": "C0017",
          "location": "第3.2项",
          "title": "3.2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.1"
          ],
          "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
        },
        {
          "clause_id": "C0018",
          "location": "第3.2项",
          "title": "3.2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.2"
          ],
          "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
        },
        {
          "clause_id": "C0019",
          "location": "第3.2项",
          "title": "3.2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.3"
          ],
          "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
        },
        {
          "clause_id": "C0020",
          "location": "第3.2项",
          "title": "3.2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.4"
          ],
          "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
        },
        {
          "clause_id": "C0021",
          "location": "第3项",
          "title": "3.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.3"
          ],
          "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
        },
        {
          "clause_id": "C0022",
          "location": "第3项",
          "title": "3.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.4"
          ],
          "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
        },
        {
          "clause_id": "C0023",
          "location": "第3项",
          "title": "3.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5"
          ],
          "text": "3.5\n本条所称关联企业，界定如下："
        },
        {
          "clause_id": "C0024",
          "location": "第3.5项",
          "title": "3.5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.1"
          ],
          "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
        },
        {
          "clause_id": "C0025",
          "location": "第3.5项",
          "title": "3.5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.2"
          ],
          "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
        },
        {
          "clause_id": "C0026",
          "location": "第3.5项",
          "title": "3.5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.3"
          ],
          "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
        },
        {
          "clause_id": "C0027",
          "location": "第3.5项",
          "title": "3.5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.4"
          ],
          "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
        },
        {
          "clause_id": "C0028",
          "location": "第4项",
          "title": "4. 竞业限制的地域",
          "section_type": "正式合同条款",
          "heading_path": [
            "4. 竞业限制的地域"
          ],
          "text": "4. 竞业限制的地域"
        },
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        {
          "clause_id": "C0030",
          "location": "第4项",
          "title": "4.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.2"
          ],
          "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
        },
        {
          "clause_id": "C0031",
          "location": "第5项",
          "title": "5. 经济补偿金",
          "section_type": "正式合同条款",
          "heading_path": [
            "5. 经济补偿金"
          ],
          "text": "5. 经济补偿金"
        },
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
        },
        {
          "clause_id": "C0033",
          "location": "第5项",
          "title": "5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.2"
          ],
          "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
        },
        {
          "clause_id": "C0034",
          "location": "第5项",
          "title": "5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.3"
          ],
          "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
        },
        {
          "clause_id": "C0035",
          "location": "第5项",
          "title": "5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.4"
          ],
          "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
        },
        {
          "clause_id": "C0036",
          "location": "第6项",
          "title": "6. 协议解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "6. 协议解除"
          ],
          "text": "6. 协议解除"
        },
        {
          "clause_id": "C0037",
          "location": "第6项",
          "title": "6.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.1"
          ],
          "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
        },
        {
          "clause_id": "C0038",
          "location": "第6项",
          "title": "6.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.2"
          ],
          "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
        },
        {
          "clause_id": "C0039",
          "location": "第6项",
          "title": "6.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.3"
          ],
          "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
        },
        {
          "clause_id": "C0040",
          "location": "第7项",
          "title": "7. 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "7. 违约责任"
          ],
          "text": "7. 违约责任"
        },
        {
          "clause_id": "C0041",
          "location": "第7项",
          "title": "7.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.1"
          ],
          "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
        },
        {
          "clause_id": "C0042",
          "location": "第7项",
          "title": "7.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.2"
          ],
          "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
        },
        {
          "clause_id": "C0043",
          "location": "第7项",
          "title": "7.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.3"
          ],
          "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
        },
        {
          "clause_id": "C0044",
          "location": "第8项",
          "title": "8. 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "8. 争议解决"
          ],
          "text": "8. 争议解决"
        },
        {
          "clause_id": "C0045",
          "location": "第8项",
          "title": "8.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.1"
          ],
          "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
        },
        {
          "clause_id": "C0046",
          "location": "第8项",
          "title": "8.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.2"
          ],
          "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
        },
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
        },
        {
          "clause_id": "C0048",
          "location": "第9项",
          "title": "9. 其他事项",
          "section_type": "正式合同条款",
          "heading_path": [
            "9. 其他事项"
          ],
          "text": "9. 其他事项"
        },
        {
          "clause_id": "C0049",
          "location": "第9项",
          "title": "9.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.1"
          ],
          "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
        },
        {
          "clause_id": "C0050",
          "location": "第9项",
          "title": "9.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.2"
          ],
          "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
        },
        {
          "clause_id": "C0051",
          "location": "第9项",
          "title": "9.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
        },
        {
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
        },
        {
          "clause_id": "C0053",
          "location": "乙方（签字）：陈浩然",
          "title": "乙方（签字）：陈浩然",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
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
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义",
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
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
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
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
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
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。",
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
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
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
        "(?:不得|禁止).{0,20}(?:自营|经营|从事).{0,50}(?:竞争|同类).{0,20}业务"
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
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义"
        },
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
        },
        {
          "clause_id": "C0006",
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
        },
        {
          "clause_id": "C0007",
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
        },
        {
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
        },
        {
          "clause_id": "C0009",
          "location": "第2项",
          "title": "2. 在职期间竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "2. 在职期间竞业限制义务"
          ],
          "text": "2. 在职期间竞业限制义务"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        {
          "clause_id": "C0012",
          "location": "第2项",
          "title": "2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.3"
          ],
          "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
        },
        {
          "clause_id": "C0013",
          "location": "第2项",
          "title": "2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.4"
          ],
          "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
        },
        {
          "clause_id": "C0014",
          "location": "第3项",
          "title": "3. 离职后竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "3. 离职后竞业限制义务"
          ],
          "text": "3. 离职后竞业限制义务"
        },
        {
          "clause_id": "C0015",
          "location": "第3项",
          "title": "3.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.1"
          ],
          "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
        },
        {
          "clause_id": "C0016",
          "location": "第3项",
          "title": "3.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2"
          ],
          "text": "3.2\n乙方在离职后的 2年内 不得："
        },
        {
          "clause_id": "C0017",
          "location": "第3.2项",
          "title": "3.2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.1"
          ],
          "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
        },
        {
          "clause_id": "C0018",
          "location": "第3.2项",
          "title": "3.2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.2"
          ],
          "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
        },
        {
          "clause_id": "C0019",
          "location": "第3.2项",
          "title": "3.2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.3"
          ],
          "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
        },
        {
          "clause_id": "C0020",
          "location": "第3.2项",
          "title": "3.2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.4"
          ],
          "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
        },
        {
          "clause_id": "C0021",
          "location": "第3项",
          "title": "3.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.3"
          ],
          "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
        },
        {
          "clause_id": "C0022",
          "location": "第3项",
          "title": "3.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.4"
          ],
          "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
        },
        {
          "clause_id": "C0023",
          "location": "第3项",
          "title": "3.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5"
          ],
          "text": "3.5\n本条所称关联企业，界定如下："
        },
        {
          "clause_id": "C0024",
          "location": "第3.5项",
          "title": "3.5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.1"
          ],
          "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
        },
        {
          "clause_id": "C0025",
          "location": "第3.5项",
          "title": "3.5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.2"
          ],
          "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
        },
        {
          "clause_id": "C0026",
          "location": "第3.5项",
          "title": "3.5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.3"
          ],
          "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
        },
        {
          "clause_id": "C0027",
          "location": "第3.5项",
          "title": "3.5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.4"
          ],
          "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
        },
        {
          "clause_id": "C0028",
          "location": "第4项",
          "title": "4. 竞业限制的地域",
          "section_type": "正式合同条款",
          "heading_path": [
            "4. 竞业限制的地域"
          ],
          "text": "4. 竞业限制的地域"
        },
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        {
          "clause_id": "C0030",
          "location": "第4项",
          "title": "4.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.2"
          ],
          "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
        },
        {
          "clause_id": "C0031",
          "location": "第5项",
          "title": "5. 经济补偿金",
          "section_type": "正式合同条款",
          "heading_path": [
            "5. 经济补偿金"
          ],
          "text": "5. 经济补偿金"
        },
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
        },
        {
          "clause_id": "C0033",
          "location": "第5项",
          "title": "5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.2"
          ],
          "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
        },
        {
          "clause_id": "C0034",
          "location": "第5项",
          "title": "5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.3"
          ],
          "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
        },
        {
          "clause_id": "C0035",
          "location": "第5项",
          "title": "5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.4"
          ],
          "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
        },
        {
          "clause_id": "C0036",
          "location": "第6项",
          "title": "6. 协议解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "6. 协议解除"
          ],
          "text": "6. 协议解除"
        },
        {
          "clause_id": "C0037",
          "location": "第6项",
          "title": "6.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.1"
          ],
          "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
        },
        {
          "clause_id": "C0038",
          "location": "第6项",
          "title": "6.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.2"
          ],
          "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
        },
        {
          "clause_id": "C0039",
          "location": "第6项",
          "title": "6.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.3"
          ],
          "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
        },
        {
          "clause_id": "C0040",
          "location": "第7项",
          "title": "7. 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "7. 违约责任"
          ],
          "text": "7. 违约责任"
        },
        {
          "clause_id": "C0041",
          "location": "第7项",
          "title": "7.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.1"
          ],
          "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
        },
        {
          "clause_id": "C0042",
          "location": "第7项",
          "title": "7.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.2"
          ],
          "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
        },
        {
          "clause_id": "C0043",
          "location": "第7项",
          "title": "7.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.3"
          ],
          "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
        },
        {
          "clause_id": "C0044",
          "location": "第8项",
          "title": "8. 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "8. 争议解决"
          ],
          "text": "8. 争议解决"
        },
        {
          "clause_id": "C0045",
          "location": "第8项",
          "title": "8.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.1"
          ],
          "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
        },
        {
          "clause_id": "C0046",
          "location": "第8项",
          "title": "8.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.2"
          ],
          "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
        },
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
        },
        {
          "clause_id": "C0048",
          "location": "第9项",
          "title": "9. 其他事项",
          "section_type": "正式合同条款",
          "heading_path": [
            "9. 其他事项"
          ],
          "text": "9. 其他事项"
        },
        {
          "clause_id": "C0049",
          "location": "第9项",
          "title": "9.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.1"
          ],
          "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
        },
        {
          "clause_id": "C0050",
          "location": "第9项",
          "title": "9.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.2"
          ],
          "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
        },
        {
          "clause_id": "C0051",
          "location": "第9项",
          "title": "9.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
        },
        {
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
        },
        {
          "clause_id": "C0053",
          "location": "乙方（签字）：陈浩然",
          "title": "乙方（签字）：陈浩然",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:不得|禁止).{0,20}(?:自营|经营|从事).{0,50}(?:竞争|同类).{0,20}业务"
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
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:不得|禁止).{0,20}(?:自营|经营|从事).{0,50}(?:竞争|同类).{0,20}业务"
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
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:不得|禁止).{0,20}(?:自营|经营|从事).{0,50}(?:竞争|同类).{0,20}业务"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
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
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义",
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
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
          "quote": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
          "original_excerpt": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "source_start": 0,
          "source_end": 77,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。",
          "quote": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。",
          "original_excerpt": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "source_start": 0,
          "source_end": 49,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。",
          "quote": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。",
          "original_excerpt": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "source_start": 0,
          "source_end": 60,
          "supports_element_ids": [
            "employment_noncompete_scope_2"
          ],
          "source_type": "CONTRACT_TEXT"
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
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义"
        },
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
        },
        {
          "clause_id": "C0006",
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
        },
        {
          "clause_id": "C0007",
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
        },
        {
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
        },
        {
          "clause_id": "C0009",
          "location": "第2项",
          "title": "2. 在职期间竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "2. 在职期间竞业限制义务"
          ],
          "text": "2. 在职期间竞业限制义务"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        {
          "clause_id": "C0012",
          "location": "第2项",
          "title": "2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.3"
          ],
          "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
        },
        {
          "clause_id": "C0013",
          "location": "第2项",
          "title": "2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.4"
          ],
          "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
        },
        {
          "clause_id": "C0014",
          "location": "第3项",
          "title": "3. 离职后竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "3. 离职后竞业限制义务"
          ],
          "text": "3. 离职后竞业限制义务"
        },
        {
          "clause_id": "C0015",
          "location": "第3项",
          "title": "3.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.1"
          ],
          "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
        },
        {
          "clause_id": "C0016",
          "location": "第3项",
          "title": "3.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2"
          ],
          "text": "3.2\n乙方在离职后的 2年内 不得："
        },
        {
          "clause_id": "C0017",
          "location": "第3.2项",
          "title": "3.2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.1"
          ],
          "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
        },
        {
          "clause_id": "C0018",
          "location": "第3.2项",
          "title": "3.2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.2"
          ],
          "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
        },
        {
          "clause_id": "C0019",
          "location": "第3.2项",
          "title": "3.2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.3"
          ],
          "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
        },
        {
          "clause_id": "C0020",
          "location": "第3.2项",
          "title": "3.2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.4"
          ],
          "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
        },
        {
          "clause_id": "C0021",
          "location": "第3项",
          "title": "3.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.3"
          ],
          "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
        },
        {
          "clause_id": "C0022",
          "location": "第3项",
          "title": "3.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.4"
          ],
          "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
        },
        {
          "clause_id": "C0023",
          "location": "第3项",
          "title": "3.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5"
          ],
          "text": "3.5\n本条所称关联企业，界定如下："
        },
        {
          "clause_id": "C0024",
          "location": "第3.5项",
          "title": "3.5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.1"
          ],
          "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
        },
        {
          "clause_id": "C0025",
          "location": "第3.5项",
          "title": "3.5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.2"
          ],
          "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
        },
        {
          "clause_id": "C0026",
          "location": "第3.5项",
          "title": "3.5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.3"
          ],
          "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
        },
        {
          "clause_id": "C0027",
          "location": "第3.5项",
          "title": "3.5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.4"
          ],
          "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
        },
        {
          "clause_id": "C0028",
          "location": "第4项",
          "title": "4. 竞业限制的地域",
          "section_type": "正式合同条款",
          "heading_path": [
            "4. 竞业限制的地域"
          ],
          "text": "4. 竞业限制的地域"
        },
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        {
          "clause_id": "C0030",
          "location": "第4项",
          "title": "4.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.2"
          ],
          "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
        },
        {
          "clause_id": "C0031",
          "location": "第5项",
          "title": "5. 经济补偿金",
          "section_type": "正式合同条款",
          "heading_path": [
            "5. 经济补偿金"
          ],
          "text": "5. 经济补偿金"
        },
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
        },
        {
          "clause_id": "C0033",
          "location": "第5项",
          "title": "5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.2"
          ],
          "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
        },
        {
          "clause_id": "C0034",
          "location": "第5项",
          "title": "5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.3"
          ],
          "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
        },
        {
          "clause_id": "C0035",
          "location": "第5项",
          "title": "5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.4"
          ],
          "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
        },
        {
          "clause_id": "C0036",
          "location": "第6项",
          "title": "6. 协议解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "6. 协议解除"
          ],
          "text": "6. 协议解除"
        },
        {
          "clause_id": "C0037",
          "location": "第6项",
          "title": "6.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.1"
          ],
          "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
        },
        {
          "clause_id": "C0038",
          "location": "第6项",
          "title": "6.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.2"
          ],
          "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
        },
        {
          "clause_id": "C0039",
          "location": "第6项",
          "title": "6.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.3"
          ],
          "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
        },
        {
          "clause_id": "C0040",
          "location": "第7项",
          "title": "7. 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "7. 违约责任"
          ],
          "text": "7. 违约责任"
        },
        {
          "clause_id": "C0041",
          "location": "第7项",
          "title": "7.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.1"
          ],
          "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
        },
        {
          "clause_id": "C0042",
          "location": "第7项",
          "title": "7.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.2"
          ],
          "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
        },
        {
          "clause_id": "C0043",
          "location": "第7项",
          "title": "7.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.3"
          ],
          "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
        },
        {
          "clause_id": "C0044",
          "location": "第8项",
          "title": "8. 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "8. 争议解决"
          ],
          "text": "8. 争议解决"
        },
        {
          "clause_id": "C0045",
          "location": "第8项",
          "title": "8.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.1"
          ],
          "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
        },
        {
          "clause_id": "C0046",
          "location": "第8项",
          "title": "8.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.2"
          ],
          "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
        },
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
        },
        {
          "clause_id": "C0048",
          "location": "第9项",
          "title": "9. 其他事项",
          "section_type": "正式合同条款",
          "heading_path": [
            "9. 其他事项"
          ],
          "text": "9. 其他事项"
        },
        {
          "clause_id": "C0049",
          "location": "第9项",
          "title": "9.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.1"
          ],
          "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
        },
        {
          "clause_id": "C0050",
          "location": "第9项",
          "title": "9.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.2"
          ],
          "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
        },
        {
          "clause_id": "C0051",
          "location": "第9项",
          "title": "9.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
        },
        {
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
        },
        {
          "clause_id": "C0053",
          "location": "乙方（签字）：陈浩然",
          "title": "乙方（签字）：陈浩然",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "竞业(?:限制|禁止).{0,25}(?:地域|地区|区域)范围\\s*(?:为|包括|限于|：|:)[^。；_]{2,80}"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
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
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义",
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
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
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
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
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
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。",
          "quote": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。",
          "original_excerpt": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "source_start": 0,
          "source_end": 38,
          "supports_element_ids": [
            "employment_noncompete_scope_3"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0003",
      "location": "1.1",
      "title": "1.1 竞业限制期：",
      "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
      "quote": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
      "original_excerpt": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
      "section_type": "正式合同条款",
      "heading_path": [
        "1.1 竞业限制期："
      ],
      "source_start": 562,
      "source_end": 639,
      "supports_element_ids": [
        "employment_noncompete_scope_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "1.1",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
      "source_span": {
        "start_offset": 562,
        "end_offset": 639,
        "raw_text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0003",
        "section": "1.1",
        "sentence_index": 1,
        "quote": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_noncompete_scope_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "NC-01-01",
      "element_ids": [
        "employment_noncompete_scope_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "明确约定竞业业务范围"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0029",
      "location": "第4项",
      "title": "4.1",
      "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。",
      "quote": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。",
      "original_excerpt": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。",
      "section_type": "正式合同条款",
      "heading_path": [
        "4.1"
      ],
      "source_start": 2942,
      "source_end": 2980,
      "supports_element_ids": [
        "employment_noncompete_scope_3"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第4项",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。",
      "source_span": {
        "start_offset": 2942,
        "end_offset": 2980,
        "raw_text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0029",
        "section": "第4项",
        "sentence_index": 1,
        "quote": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_noncompete_scope_3"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "NC-01-01",
      "element_ids": [
        "employment_noncompete_scope_3"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "明确约定竞业地域范围"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0010",
      "location": "第2项",
      "title": "2.1",
      "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。",
      "quote": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。",
      "original_excerpt": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。",
      "section_type": "正式合同条款",
      "heading_path": [
        "2.1"
      ],
      "source_start": 1455,
      "source_end": 1504,
      "supports_element_ids": [
        "employment_noncompete_scope_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第2项",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。",
      "source_span": {
        "start_offset": 1455,
        "end_offset": 1504,
        "raw_text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0010",
        "section": "第2项",
        "sentence_index": 1,
        "quote": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [],
      "canonical_fact_keys": [],
      "relevance_score": 0.0,
      "selection_reason": "Contextual retrieval evidence does not directly support a resolved ReviewElementTruth.",
      "review_id": "NC-01-01",
      "element_ids": [],
      "support_type": "CONTEXTUAL",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      }
    },
    {
      "clause_id": "C0011",
      "location": "第2项",
      "title": "2.2",
      "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。",
      "quote": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。",
      "original_excerpt": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。",
      "section_type": "正式合同条款",
      "heading_path": [
        "2.2"
      ],
      "source_start": 1505,
      "source_end": 1565,
      "supports_element_ids": [
        "employment_noncompete_scope_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第2项",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。",
      "source_span": {
        "start_offset": 1505,
        "end_offset": 1565,
        "raw_text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0011",
        "section": "第2项",
        "sentence_index": 1,
        "quote": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [],
      "canonical_fact_keys": [],
      "relevance_score": 0.0,
      "selection_reason": "Contextual retrieval evidence does not directly support a resolved ReviewElementTruth.",
      "review_id": "NC-01-01",
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
    "condition": "出现离职、解除、终止安排时适用",
    "triggered": true,
    "condition_text": "出现离职、解除、终止安排时适用"
  },
  "polarity": "POSITIVE_REQUIREMENT",
  "actual_status": "通过",
  "reason": "合同原文覆盖全部专项要素。",
  "coverage_elements": [
    {
      "review_id": "NC-02-01",
      "element_id": "employment_noncompete_term_1",
      "proposition": "离职竞业限制期限",
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
        "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
      ],
      "source_locations": [
        "1.1"
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
          "quote": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        }
      ]
    },
    {
      "review_id": "NC-02-01",
      "element_id": "employment_noncompete_term_2",
      "proposition": "离职后按月经济补偿的金额或计算标准",
      "status": "COVERED",
      "evidence_ids": [
        "C0032"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0032"
      ],
      "source_spans": [
        "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。"
      ],
      "source_locations": [
        "第5项"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0032"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0032"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0032",
          "quote": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。"
        }
      ]
    }
  ],
  "negative_clause_check": null,
  "element_absence_searches": [
    {
      "element_id": "employment_noncompete_term_1",
      "review_id": "NC-02-01",
      "search_targets": [
        "离职竞业限制期限"
      ],
      "query_patterns": [
        "竞业(?:限制|禁止)(?:持续)?期(?:限)?\\s*(?:为|是|：|:)\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)",
        "离职后\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)(?:内)?[^。；\\n]{0,12}(?:承担|履行|遵守)竞业(?:限制|禁止)",
        "(?:离职|解除劳动合同|终止劳动合同)后[^。；\\n]{0,12}竞业(?:限制|禁止)(?:期(?:限)?)?\\s*(?:为|：|:)?\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)"
      ],
      "query_semantic_target": "离职竞业限制期限",
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
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义"
        },
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
        },
        {
          "clause_id": "C0006",
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
        },
        {
          "clause_id": "C0007",
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
        },
        {
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
        },
        {
          "clause_id": "C0009",
          "location": "第2项",
          "title": "2. 在职期间竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "2. 在职期间竞业限制义务"
          ],
          "text": "2. 在职期间竞业限制义务"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        {
          "clause_id": "C0012",
          "location": "第2项",
          "title": "2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.3"
          ],
          "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
        },
        {
          "clause_id": "C0013",
          "location": "第2项",
          "title": "2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.4"
          ],
          "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
        },
        {
          "clause_id": "C0014",
          "location": "第3项",
          "title": "3. 离职后竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "3. 离职后竞业限制义务"
          ],
          "text": "3. 离职后竞业限制义务"
        },
        {
          "clause_id": "C0015",
          "location": "第3项",
          "title": "3.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.1"
          ],
          "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
        },
        {
          "clause_id": "C0016",
          "location": "第3项",
          "title": "3.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2"
          ],
          "text": "3.2\n乙方在离职后的 2年内 不得："
        },
        {
          "clause_id": "C0017",
          "location": "第3.2项",
          "title": "3.2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.1"
          ],
          "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
        },
        {
          "clause_id": "C0018",
          "location": "第3.2项",
          "title": "3.2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.2"
          ],
          "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
        },
        {
          "clause_id": "C0019",
          "location": "第3.2项",
          "title": "3.2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.3"
          ],
          "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
        },
        {
          "clause_id": "C0020",
          "location": "第3.2项",
          "title": "3.2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.4"
          ],
          "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
        },
        {
          "clause_id": "C0021",
          "location": "第3项",
          "title": "3.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.3"
          ],
          "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
        },
        {
          "clause_id": "C0022",
          "location": "第3项",
          "title": "3.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.4"
          ],
          "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
        },
        {
          "clause_id": "C0023",
          "location": "第3项",
          "title": "3.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5"
          ],
          "text": "3.5\n本条所称关联企业，界定如下："
        },
        {
          "clause_id": "C0024",
          "location": "第3.5项",
          "title": "3.5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.1"
          ],
          "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
        },
        {
          "clause_id": "C0025",
          "location": "第3.5项",
          "title": "3.5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.2"
          ],
          "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
        },
        {
          "clause_id": "C0026",
          "location": "第3.5项",
          "title": "3.5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.3"
          ],
          "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
        },
        {
          "clause_id": "C0027",
          "location": "第3.5项",
          "title": "3.5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.4"
          ],
          "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
        },
        {
          "clause_id": "C0028",
          "location": "第4项",
          "title": "4. 竞业限制的地域",
          "section_type": "正式合同条款",
          "heading_path": [
            "4. 竞业限制的地域"
          ],
          "text": "4. 竞业限制的地域"
        },
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        {
          "clause_id": "C0030",
          "location": "第4项",
          "title": "4.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.2"
          ],
          "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
        },
        {
          "clause_id": "C0031",
          "location": "第5项",
          "title": "5. 经济补偿金",
          "section_type": "正式合同条款",
          "heading_path": [
            "5. 经济补偿金"
          ],
          "text": "5. 经济补偿金"
        },
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
        },
        {
          "clause_id": "C0033",
          "location": "第5项",
          "title": "5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.2"
          ],
          "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
        },
        {
          "clause_id": "C0034",
          "location": "第5项",
          "title": "5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.3"
          ],
          "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
        },
        {
          "clause_id": "C0035",
          "location": "第5项",
          "title": "5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.4"
          ],
          "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
        },
        {
          "clause_id": "C0036",
          "location": "第6项",
          "title": "6. 协议解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "6. 协议解除"
          ],
          "text": "6. 协议解除"
        },
        {
          "clause_id": "C0037",
          "location": "第6项",
          "title": "6.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.1"
          ],
          "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
        },
        {
          "clause_id": "C0038",
          "location": "第6项",
          "title": "6.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.2"
          ],
          "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
        },
        {
          "clause_id": "C0039",
          "location": "第6项",
          "title": "6.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.3"
          ],
          "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
        },
        {
          "clause_id": "C0040",
          "location": "第7项",
          "title": "7. 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "7. 违约责任"
          ],
          "text": "7. 违约责任"
        },
        {
          "clause_id": "C0041",
          "location": "第7项",
          "title": "7.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.1"
          ],
          "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
        },
        {
          "clause_id": "C0042",
          "location": "第7项",
          "title": "7.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.2"
          ],
          "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
        },
        {
          "clause_id": "C0043",
          "location": "第7项",
          "title": "7.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.3"
          ],
          "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
        },
        {
          "clause_id": "C0044",
          "location": "第8项",
          "title": "8. 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "8. 争议解决"
          ],
          "text": "8. 争议解决"
        },
        {
          "clause_id": "C0045",
          "location": "第8项",
          "title": "8.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.1"
          ],
          "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
        },
        {
          "clause_id": "C0046",
          "location": "第8项",
          "title": "8.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.2"
          ],
          "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
        },
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
        },
        {
          "clause_id": "C0048",
          "location": "第9项",
          "title": "9. 其他事项",
          "section_type": "正式合同条款",
          "heading_path": [
            "9. 其他事项"
          ],
          "text": "9. 其他事项"
        },
        {
          "clause_id": "C0049",
          "location": "第9项",
          "title": "9.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.1"
          ],
          "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
        },
        {
          "clause_id": "C0050",
          "location": "第9项",
          "title": "9.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.2"
          ],
          "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
        },
        {
          "clause_id": "C0051",
          "location": "第9项",
          "title": "9.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
        },
        {
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
        },
        {
          "clause_id": "C0053",
          "location": "乙方（签字）：陈浩然",
          "title": "乙方（签字）：陈浩然",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [],
          "matched_contextual_patterns": [
            {
              "context": "竞业(?:限制|禁止)期",
              "predicate": "之日起(?:的)?\\s*[一二两三四五六七八九十百\\d]+\\s*个?\\s*(?:月|年|日|天)内[^。；\\n]{0,35}(?:不得|履行|承担)"
            }
          ],
          "matched_excluded_patterns": [],
          "required_fact_groups": {},
          "stage_trace": {
            "normalize": "OK: ParsedClause -> canonical candidate text/location/heading",
            "rerank": "score=1; semantic_hits=0; contextual_hits=1",
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
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
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义",
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
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
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
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。",
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
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
          "quote": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
          "original_excerpt": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "source_start": 0,
          "source_end": 77,
          "supports_element_ids": [
            "employment_noncompete_term_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_noncompete_term_2",
      "review_id": "NC-02-01",
      "search_targets": [
        "离职后按月经济补偿的金额或计算标准"
      ],
      "query_patterns": [
        "(?:离职|解除|终止).{0,100}(?:每月|按月).{0,30}(?:补偿.{0,12}\\d+元|\\d+元.{0,12}补偿|补偿.{0,20}\\d+[%％])",
        "经济补偿(?:金)?(?:为|：|:)[^。；\\n]{0,80}(?:每月|按月)\\s*(?:人民币)?\\s*[\\d,，]+(?:\\.\\d+)?\\s*元",
        "(?:离职后|竞业限制期间)[^。；\\n]{0,40}(?:每月|按月)[^。；\\n]{0,20}(?:支付)?(?:经济)?补偿(?:金)?\\s*(?:为|：|:)?\\s*(?:人民币)?\\s*[\\d,，]+\\s*元"
      ],
      "query_semantic_target": "离职后按月经济补偿的金额或计算标准",
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
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义"
        },
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
        },
        {
          "clause_id": "C0006",
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
        },
        {
          "clause_id": "C0007",
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
        },
        {
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
        },
        {
          "clause_id": "C0009",
          "location": "第2项",
          "title": "2. 在职期间竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "2. 在职期间竞业限制义务"
          ],
          "text": "2. 在职期间竞业限制义务"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        {
          "clause_id": "C0012",
          "location": "第2项",
          "title": "2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.3"
          ],
          "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
        },
        {
          "clause_id": "C0013",
          "location": "第2项",
          "title": "2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.4"
          ],
          "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
        },
        {
          "clause_id": "C0014",
          "location": "第3项",
          "title": "3. 离职后竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "3. 离职后竞业限制义务"
          ],
          "text": "3. 离职后竞业限制义务"
        },
        {
          "clause_id": "C0015",
          "location": "第3项",
          "title": "3.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.1"
          ],
          "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
        },
        {
          "clause_id": "C0016",
          "location": "第3项",
          "title": "3.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2"
          ],
          "text": "3.2\n乙方在离职后的 2年内 不得："
        },
        {
          "clause_id": "C0017",
          "location": "第3.2项",
          "title": "3.2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.1"
          ],
          "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
        },
        {
          "clause_id": "C0018",
          "location": "第3.2项",
          "title": "3.2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.2"
          ],
          "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
        },
        {
          "clause_id": "C0019",
          "location": "第3.2项",
          "title": "3.2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.3"
          ],
          "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
        },
        {
          "clause_id": "C0020",
          "location": "第3.2项",
          "title": "3.2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.4"
          ],
          "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
        },
        {
          "clause_id": "C0021",
          "location": "第3项",
          "title": "3.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.3"
          ],
          "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
        },
        {
          "clause_id": "C0022",
          "location": "第3项",
          "title": "3.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.4"
          ],
          "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
        },
        {
          "clause_id": "C0023",
          "location": "第3项",
          "title": "3.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5"
          ],
          "text": "3.5\n本条所称关联企业，界定如下："
        },
        {
          "clause_id": "C0024",
          "location": "第3.5项",
          "title": "3.5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.1"
          ],
          "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
        },
        {
          "clause_id": "C0025",
          "location": "第3.5项",
          "title": "3.5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.2"
          ],
          "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
        },
        {
          "clause_id": "C0026",
          "location": "第3.5项",
          "title": "3.5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.3"
          ],
          "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
        },
        {
          "clause_id": "C0027",
          "location": "第3.5项",
          "title": "3.5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.4"
          ],
          "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
        },
        {
          "clause_id": "C0028",
          "location": "第4项",
          "title": "4. 竞业限制的地域",
          "section_type": "正式合同条款",
          "heading_path": [
            "4. 竞业限制的地域"
          ],
          "text": "4. 竞业限制的地域"
        },
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        {
          "clause_id": "C0030",
          "location": "第4项",
          "title": "4.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.2"
          ],
          "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
        },
        {
          "clause_id": "C0031",
          "location": "第5项",
          "title": "5. 经济补偿金",
          "section_type": "正式合同条款",
          "heading_path": [
            "5. 经济补偿金"
          ],
          "text": "5. 经济补偿金"
        },
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
        },
        {
          "clause_id": "C0033",
          "location": "第5项",
          "title": "5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.2"
          ],
          "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
        },
        {
          "clause_id": "C0034",
          "location": "第5项",
          "title": "5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.3"
          ],
          "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
        },
        {
          "clause_id": "C0035",
          "location": "第5项",
          "title": "5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.4"
          ],
          "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
        },
        {
          "clause_id": "C0036",
          "location": "第6项",
          "title": "6. 协议解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "6. 协议解除"
          ],
          "text": "6. 协议解除"
        },
        {
          "clause_id": "C0037",
          "location": "第6项",
          "title": "6.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.1"
          ],
          "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
        },
        {
          "clause_id": "C0038",
          "location": "第6项",
          "title": "6.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.2"
          ],
          "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
        },
        {
          "clause_id": "C0039",
          "location": "第6项",
          "title": "6.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.3"
          ],
          "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
        },
        {
          "clause_id": "C0040",
          "location": "第7项",
          "title": "7. 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "7. 违约责任"
          ],
          "text": "7. 违约责任"
        },
        {
          "clause_id": "C0041",
          "location": "第7项",
          "title": "7.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.1"
          ],
          "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
        },
        {
          "clause_id": "C0042",
          "location": "第7项",
          "title": "7.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.2"
          ],
          "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
        },
        {
          "clause_id": "C0043",
          "location": "第7项",
          "title": "7.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.3"
          ],
          "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
        },
        {
          "clause_id": "C0044",
          "location": "第8项",
          "title": "8. 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "8. 争议解决"
          ],
          "text": "8. 争议解决"
        },
        {
          "clause_id": "C0045",
          "location": "第8项",
          "title": "8.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.1"
          ],
          "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
        },
        {
          "clause_id": "C0046",
          "location": "第8项",
          "title": "8.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.2"
          ],
          "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
        },
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
        },
        {
          "clause_id": "C0048",
          "location": "第9项",
          "title": "9. 其他事项",
          "section_type": "正式合同条款",
          "heading_path": [
            "9. 其他事项"
          ],
          "text": "9. 其他事项"
        },
        {
          "clause_id": "C0049",
          "location": "第9项",
          "title": "9.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.1"
          ],
          "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
        },
        {
          "clause_id": "C0050",
          "location": "第9项",
          "title": "9.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.2"
          ],
          "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
        },
        {
          "clause_id": "C0051",
          "location": "第9项",
          "title": "9.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
        },
        {
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
        },
        {
          "clause_id": "C0053",
          "location": "乙方（签字）：陈浩然",
          "title": "乙方（签字）：陈浩然",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "经济补偿(?:金)?(?:为|：|:)[^。；\\n]{0,80}(?:每月|按月)\\s*(?:人民币)?\\s*[\\d,，]+(?:\\.\\d+)?\\s*元"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
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
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义",
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
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
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
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
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
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "text": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。",
          "quote": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。",
          "original_excerpt": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "source_start": 91,
          "source_end": 154,
          "supports_element_ids": [
            "employment_noncompete_term_2"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0003",
      "location": "1.1",
      "title": "1.1 竞业限制期：",
      "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
      "quote": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
      "original_excerpt": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
      "section_type": "正式合同条款",
      "heading_path": [
        "1.1 竞业限制期："
      ],
      "source_start": 562,
      "source_end": 639,
      "supports_element_ids": [
        "employment_noncompete_term_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "1.1",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
      "source_span": {
        "start_offset": 562,
        "end_offset": 639,
        "raw_text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0003",
        "section": "1.1",
        "sentence_index": 1,
        "quote": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_noncompete_term_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "NC-02-01",
      "element_ids": [
        "employment_noncompete_term_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "离职竞业限制期限"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0032",
      "location": "第5项",
      "title": "5.1",
      "text": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。",
      "quote": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。",
      "original_excerpt": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。",
      "section_type": "正式合同条款",
      "heading_path": [
        "5.1"
      ],
      "source_start": 3120,
      "source_end": 3182,
      "supports_element_ids": [
        "employment_noncompete_term_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第5项",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。",
      "source_span": {
        "start_offset": 3120,
        "end_offset": 3182,
        "raw_text": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0032",
        "section": "第5项",
        "sentence_index": 1,
        "quote": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_COVERAGE",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_noncompete_term_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "NC-02-01",
      "element_ids": [
        "employment_noncompete_term_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "离职后按月经济补偿的金额或计算标准"
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
    "condition": "ALWAYS_APPLICABLE",
    "triggered": true
  },
  "polarity": "NEGATIVE_CLAUSE_CHECK",
  "actual_status": "待核验",
  "reason": "合理性判断所需事实尚不完整：人员范围及实际接触秘密、劳动者具体岗位；应结合实际接触秘密及约定范围核验，不能据此直接认定范围合理或违法。",
  "coverage_elements": [
    {
      "review_id": "NC-03-01",
      "element_id": "core_contract_arrangement",
      "proposition": "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容。",
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
      "element_id": "noncompete_reasonableness_prerequisites",
      "status": "CONDITION_UNRESOLVED",
      "proposition": "合理性判断所需事实尚不完整：人员范围及实际接触秘密、劳动者具体岗位；应结合实际接触秘密及约定范围核验，不能据此直接认定范围合理或违法。",
      "required_fact": "竞业范围及补偿合理性判断前提",
      "conditional_element": true,
      "prerequisite_status": "UNKNOWN",
      "prerequisite_fact": "人员、秘密接触、范围、期限及补偿事实足以判断合理性",
      "verification_instruction": "合理性判断所需事实尚不完整：人员范围及实际接触秘密、劳动者具体岗位；应结合实际接触秘密及约定范围核验，不能据此直接认定范围合理或违法。",
      "risk_relevant": false,
      "bound_evidence_ids": [],
      "evidence_refs": [],
      "evidence_selection_reason": "No direct supporting evidence was selected for this element."
    }
  ],
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
      "C0039",
      "C0040",
      "C0041",
      "C0042",
      "C0043",
      "C0044",
      "C0045",
      "C0046",
      "C0047",
      "C0048",
      "C0049",
      "C0050",
      "C0051",
      "C0052",
      "C0053"
    ],
    "candidate_adverse_clauses": [],
    "counter_evidence": [],
    "search_coverage": "SUFFICIENT",
    "adverse_clause_exists": false,
    "confidence": "high",
    "coverage_result": "INSUFFICIENT_CONTEXT"
  },
  "element_absence_searches": [
    {
      "element_id": "core_contract_arrangement",
      "review_id": "NC-03-01",
      "search_targets": [
        "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容"
      ],
      "query_patterns": [
        "合同存在可验证的“竞业范围或补偿明显不当”实质条款内容"
      ],
      "query_semantics": "POSITIVE_REQUIRED_FACT",
      "search_mode": "OBJECTIVE_LITERAL_TARGET",
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
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
      ],
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
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
        "C0047"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0047"
      ],
      "source_spans": [
        "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
      ],
      "source_locations": [
        "第8项"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0047"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0047"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0047",
          "quote": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
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
        "C0039",
        "C0040",
        "C0041",
        "C0042",
        "C0043",
        "C0044",
        "C0045",
        "C0046",
        "C0047",
        "C0048",
        "C0049",
        "C0050",
        "C0051",
        "C0052",
        "C0053"
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。\n甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。\n依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下："
        },
        {
          "clause_id": "C0002",
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义"
        },
        {
          "clause_id": "C0003",
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。"
        },
        {
          "clause_id": "C0004",
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。"
        },
        {
          "clause_id": "C0005",
          "location": "1.3",
          "title": "1.3 竞争行为：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.3 竞争行为："
          ],
          "text": "1.3 竞争行为：\n指与乙方在甲方工作期间的工作内容相同或者近似的，或与甲方主营业务有关的工作内容。\n竞争行为的内容包括但不限于乙方受聘于甲方竞争者，自行或与他人合作投资设立与甲方竞争的公司，为客户提供人工智能合同审查服务、法律大模型研发服务、企业法务自动化服务、合同风险识别服务等行为。\n竞争行为的方式包括但不限于与甲方的客户进行业务联系，代表除甲方以外的任何其他企业、公司或个人为甲方的客户提供包含竞争行为的服务，为甲方的竞争者与甲方客户建立或试图建立业务联系，与甲方的客户进行或试图进行交易等行为。"
        },
        {
          "clause_id": "C0006",
          "location": "1.4",
          "title": "1.4 甲方的机密信息：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.4 甲方的机密信息："
          ],
          "text": "1.4 甲方的机密信息：\n指甲方在生产、经营过程中所形成的，与甲方经营活动有关的、不为公众所知悉、具有商业价值并经甲方采取保密措施的信息。"
        },
        {
          "clause_id": "C0007",
          "location": "第1项",
          "title": "1.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.5"
          ],
          "text": "1.5\n甲方未以明示方式向社会公众公开披露的商品、经营及服务信息，包括但不限于：\n甲方的客户名录，包括甲方现有客户以及潜在客户；\n甲方为客户提供服务的业务流程；\n合同审查规则库；\n风险识别规则及算法；\n提示词体系；\n法律知识库；\n人工智能模型训练数据；\n模型评测数据；\n合同分类算法；\n检索增强生成系统架构；\n产品技术文档；\n源代码；\n系统架构；\n产品路线图；\n价格政策；\n销售策略；\n客户的消费习惯；\n客户的购买需求等。\n无论前述信息是否有形存在，亦不论甲方是否已经以明确的书面方式标示该信息为机密信息。"
        },
        {
          "clause_id": "C0008",
          "location": "1.6",
          "title": "1.6 甲方客户：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.6 甲方客户："
          ],
          "text": "1.6 甲方客户：\n指在乙方自甲方处离职之日，正在与甲方发生业务关系或曾经接受过甲方所提供的服务的个人、公司、企业或其他组织。"
        },
        {
          "clause_id": "C0009",
          "location": "第2项",
          "title": "2. 在职期间竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "2. 在职期间竞业限制义务"
          ],
          "text": "2. 在职期间竞业限制义务"
        },
        {
          "clause_id": "C0010",
          "location": "第2项",
          "title": "2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.1"
          ],
          "text": "2.1\n乙方在职期间不得自营或帮助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同类的业务。"
        },
        {
          "clause_id": "C0011",
          "location": "第2项",
          "title": "2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.2"
          ],
          "text": "2.2\n乙方在职期间不得从事任何与甲方产品或业务构成竞争的任何业务或行为，不得以任何形式从事与甲方有竞争关系的第二职业。"
        },
        {
          "clause_id": "C0012",
          "location": "第2项",
          "title": "2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.3"
          ],
          "text": "2.3\n乙方不得诱使甲方的其他员工与自己一同离职，或为个人或他人利益诱使甲方的其他员工离职。"
        },
        {
          "clause_id": "C0013",
          "location": "第2项",
          "title": "2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "2.4"
          ],
          "text": "2.4\n乙方确认，在职期间竞业限制义务系基于劳动者忠实义务产生，甲方无需就此向乙方额外支付补偿。"
        },
        {
          "clause_id": "C0014",
          "location": "第3项",
          "title": "3. 离职后竞业限制义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "3. 离职后竞业限制义务"
          ],
          "text": "3. 离职后竞业限制义务"
        },
        {
          "clause_id": "C0015",
          "location": "第3项",
          "title": "3.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.1"
          ],
          "text": "3.1\n乙方离职前，甲方无法通过采取脱密措施确保乙方在职期间了解、知悉或掌握的甲方机密信息丧失秘密性或不被泄漏。\n经甲方界定，确定需要乙方承担本协议项下离职后竞业限制义务的，甲方应于乙方离职前书面通知乙方，乙方的竞业限制义务应自书面通知中确认的时间或者乙方离职之日起开始生效。"
        },
        {
          "clause_id": "C0016",
          "location": "第3项",
          "title": "3.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2"
          ],
          "text": "3.2\n乙方在离职后的 2年内 不得："
        },
        {
          "clause_id": "C0017",
          "location": "第3.2项",
          "title": "3.2.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.1"
          ],
          "text": "3.2.1\n自营或协助任何第三方经营与甲方产品同类的产品或者与甲方从事业务同种类、相近或相竞争的业务；"
        },
        {
          "clause_id": "C0018",
          "location": "第3.2项",
          "title": "3.2.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.2"
          ],
          "text": "3.2.2\n受雇于甲方的竞争对手，或作为甲方竞争对手的代理人、董事、监事、顾问或代表人从事活动或以任何其他身份为甲方竞争对手提供服务、提供财务支持或担保；"
        },
        {
          "clause_id": "C0019",
          "location": "第3.2项",
          "title": "3.2.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.3"
          ],
          "text": "3.2.3\n投资于从事竞争业务的实体或个人，包括持有甲方竞争对手股东或合伙人的股份、权益或类似的权益安排。"
        },
        {
          "clause_id": "C0020",
          "location": "第3.2项",
          "title": "3.2.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.2.4"
          ],
          "text": "3.2.4\n为免歧义，本协议约定的“竞争业务”系指与甲方主营业务相同，包括但不限于：\n人工智能合同审查系统；\n企业法律SaaS；\n法律大模型；\n智能法律咨询；\n合同风险识别；\n法律知识库；\n法律文书生成；\n企业合规自动化；\n法律人工智能Agent；\n以及与前述业务相关的一切软件开发、技术服务、数据服务和咨询业务。\n“竞争对手”系指与甲方从事主营业务相同，包括但不限于北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司及其他从事相同或相近业务的企业。"
        },
        {
          "clause_id": "C0021",
          "location": "第3项",
          "title": "3.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.3"
          ],
          "text": "3.3\n乙方在职期间及离职后2年内乙方不会：\n（a）直接或间接尝试引诱或企图影响甲方的任何员工脱离与甲方的雇用关系；或\n（b）为了甲方以外的任何人之利益而直接或间接地从甲方的任何客户招揽业务，包括曾收到或索取甲方有关乙方在受雇的最后十二个月内的任何时间曾经在很大程度上了解、参与或接触过的甲方业务之提议或邀约的任何潜在客户；\n任何此等客户或潜在客户的任何附属机构；\n以及乙方曾在乙方受雇于甲方的最后十二个月期间因乙方在甲方的职责而建立的任何个别联系人；\n乙方亦不会作为其它实体的员工或顾问而参与或以任何方式协助从任何此等客户那里招揽业务，除非要招揽的业务与甲方提供给此等客户的服务不存在竞争关系。\n此外，乙方还承认并同意任何及所有与甲方的任何客户相关的“友好关系”均排他性地属于甲方所有，包括但不限于因乙方或乙方在甲方所主管的员工与甲方的任何客户之间的直接或间接联系或关系而建立的任何友好关系。"
        },
        {
          "clause_id": "C0022",
          "location": "第3项",
          "title": "3.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.4"
          ],
          "text": "3.4\n本条所称离职，以任何一方明确表示解除或辞去劳动关系的时间为准。\n乙方单方面停止履行职务的行为，亦为离职。"
        },
        {
          "clause_id": "C0023",
          "location": "第3项",
          "title": "3.5",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5"
          ],
          "text": "3.5\n本条所称关联企业，界定如下："
        },
        {
          "clause_id": "C0024",
          "location": "第3.5项",
          "title": "3.5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.1"
          ],
          "text": "3.5.1\n与甲方形成直接或间接控股、参股关系，或同为第三人直接或间接控股、参股的企业；"
        },
        {
          "clause_id": "C0025",
          "location": "第3.5项",
          "title": "3.5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.2"
          ],
          "text": "3.5.2\n无控股、参股关系，但将其指挥支配的权利置于甲方之下的企业；"
        },
        {
          "clause_id": "C0026",
          "location": "第3.5项",
          "title": "3.5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.3"
          ],
          "text": "3.5.3\n将盈利或单个经营场所的全部或部分盈利与甲方共享或转移给甲方的企业；"
        },
        {
          "clause_id": "C0027",
          "location": "第3.5项",
          "title": "3.5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "3.5.4"
          ],
          "text": "3.5.4\n与甲方存在人事关系的企业，即向甲方派遣人员或者接受甲方派遣的人员，包括股东、合伙人、董事、监事、经理、职员、代理人、顾问等。"
        },
        {
          "clause_id": "C0028",
          "location": "第4项",
          "title": "4. 竞业限制的地域",
          "section_type": "正式合同条款",
          "heading_path": [
            "4. 竞业限制的地域"
          ],
          "text": "4. 竞业限制的地域"
        },
        {
          "clause_id": "C0029",
          "location": "第4项",
          "title": "4.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.1"
          ],
          "text": "4.1\n本协议项下，乙方应履行竞业限制的地域范围为：中华人民共和国全国范围。"
        },
        {
          "clause_id": "C0030",
          "location": "第4项",
          "title": "4.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "4.2"
          ],
          "text": "4.2\n双方确认，结合甲方经营规模、业务辐射范围，前述地域范围具备合理性。"
        },
        {
          "clause_id": "C0031",
          "location": "第5项",
          "title": "5. 经济补偿金",
          "section_type": "正式合同条款",
          "heading_path": [
            "5. 经济补偿金"
          ],
          "text": "5. 经济补偿金"
        },
        {
          "clause_id": "C0032",
          "location": "第5项",
          "title": "5.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.1"
          ],
          "text": "5.1\n自乙方离职后竞业限制义务生效后，乙方切实遵守本协议项下竞业限制义务的，甲方应于每个自然月的5日前向乙方支付经济补偿金。\n乙方离职前12个月月平均工资为 人民币32,000元。\n经济补偿金为乙方离职前12个月月平均工资的 30%，即每月 人民币9,600元，且该金额不得低于劳动合同履行地最低工资标准。\n如相关法律法规有规定，甲方可代扣代缴应由乙方承担的个人所得税。"
        },
        {
          "clause_id": "C0033",
          "location": "第5项",
          "title": "5.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.2"
          ],
          "text": "5.2\n乙方自离职之日起，应在甲方支付经济补偿金之前，向甲方提供新任职单位出具的工作证明，应包含工作单位联系方式和社会保险费缴纳清单，或户籍所在地劳动与社会保障部门提供的有效的失业证明原件、有效联系地址和电话及乙方接收经济补偿金的银行账号等。\n乙方接收竞业限制补偿金的银行账户如下：\n开户行：中国工商银行上海张江支行\n户名：陈浩然\n账号：622202XXXXXXXX1234\n如乙方工作情况发生任何变动，乙方应立即向甲方提供新的证明文件。\n乙方未能及时提供前述材料的，甲方有权暂停向乙方支付经济补偿金，但暂停支付期间，乙方仍需正常履行竞业限制义务。"
        },
        {
          "clause_id": "C0034",
          "location": "第5项",
          "title": "5.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.3"
          ],
          "text": "5.3\n甲方有权在正常支付竞业补偿金的情况下，根据乙方提交的新用人单位的情况进行核查。\n若查实乙方存在本协议约定之竞业禁止情形的，甲方有权要求乙方停止违约行为、与新用人单位解除劳动关系，或按本协议约定追究乙方违约责任。"
        },
        {
          "clause_id": "C0035",
          "location": "第5项",
          "title": "5.4",
          "section_type": "正式合同条款",
          "heading_path": [
            "5.4"
          ],
          "text": "5.4\n无论乙方以何种方式离职，只要本协议约定的离职竞业限制义务生效，甲方均应按照本协议5.1条约定按时足额支付经济补偿金。\n若甲方连续三个月未足额支付竞业限制经济补偿金，乙方有权单方解除本协议项下离职竞业限制义务，解除后乙方不再受本协议离职竞业条款约束。"
        },
        {
          "clause_id": "C0036",
          "location": "第6项",
          "title": "6. 协议解除",
          "section_type": "正式合同条款",
          "heading_path": [
            "6. 协议解除"
          ],
          "text": "6. 协议解除"
        },
        {
          "clause_id": "C0037",
          "location": "第6项",
          "title": "6.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.1"
          ],
          "text": "6.1\n若乙方在本协议期限内违反本协议约定的，甲方有权书面通知乙方解除本协议，并继续追究乙方的违约责任。"
        },
        {
          "clause_id": "C0038",
          "location": "第6项",
          "title": "6.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.2"
          ],
          "text": "6.2\n乙方履行离职后竞业限制义务期间，甲方经评定后认为无需乙方继续履行竞业限制义务的，经甲方提前 1个月 书面通知乙方后，甲方可解除本协议。\n该通知自甲方按乙方提供的联系地址发出之日起发生效力。"
        },
        {
          "clause_id": "C0039",
          "location": "第6项",
          "title": "6.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "6.3"
          ],
          "text": "6.3\n本协议解除后，乙方无需再履行后续竞业限制义务，甲方无需再支付竞业限制经济补偿金；\n协议解除前乙方已发生的违约行为，甲方仍有权追责。"
        },
        {
          "clause_id": "C0040",
          "location": "第7项",
          "title": "7. 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "7. 违约责任"
          ],
          "text": "7. 违约责任"
        },
        {
          "clause_id": "C0041",
          "location": "第7项",
          "title": "7.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.1"
          ],
          "text": "7.1\n乙方违反在职期间竞业限制义务的，应当赔偿甲方实际损失；\n同时乙方应向甲方支付违约金 人民币300,000元。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。"
        },
        {
          "clause_id": "C0042",
          "location": "第7项",
          "title": "7.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.2"
          ],
          "text": "7.2\n乙方在职期间违反竞业限制义务的，视为严重违反甲方规章制度，甲方有权随时书面通知乙方解除与其签署的劳动合同，且无需向乙方支付任何经济补偿。"
        },
        {
          "clause_id": "C0043",
          "location": "第7项",
          "title": "7.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "7.3"
          ],
          "text": "7.3\n乙方离职后违反竞业限制义务的，应向甲方支付 人民币300,000元 的违约金。\n若约定违约金低于甲方实际损失的，乙方应对损失差额部分予以补足；\n若约定违约金过分高于甲方实际损失，乙方有权请求仲裁机构或人民法院予以适当调减。\n甲方实际损失包括但不限于甲方为了调查、处理、纠正乙方违反竞业禁止的行为所付出的律师费、诉讼费、仲裁费、保全费、评估费、公证费及调查取证费用等合理开支。"
        },
        {
          "clause_id": "C0044",
          "location": "第8项",
          "title": "8. 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "8. 争议解决"
          ],
          "text": "8. 争议解决"
        },
        {
          "clause_id": "C0045",
          "location": "第8项",
          "title": "8.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.1"
          ],
          "text": "8.1\n双方因签订、履行本协议发生的任何争议，应尽力通过友好协商解决。"
        },
        {
          "clause_id": "C0046",
          "location": "第8项",
          "title": "8.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.2"
          ],
          "text": "8.2\n若无法通过协商解决争议，双方可提请相关调解组织进行调解。"
        },
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
        },
        {
          "clause_id": "C0048",
          "location": "第9项",
          "title": "9. 其他事项",
          "section_type": "正式合同条款",
          "heading_path": [
            "9. 其他事项"
          ],
          "text": "9. 其他事项"
        },
        {
          "clause_id": "C0049",
          "location": "第9项",
          "title": "9.1",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.1"
          ],
          "text": "9.1\n本协议内容如与现行及将来生效的法律、行政法规强制性规定相冲突的，以法律、行政法规规定为准。"
        },
        {
          "clause_id": "C0050",
          "location": "第9项",
          "title": "9.2",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.2"
          ],
          "text": "9.2\n本协议经甲方盖章且乙方签字后即发生法律效力，本协议至乙方离职后竞业限制期限届满后终止。\n本协议壹式两份，双方各执壹份，每份具有同等法律效力。"
        },
        {
          "clause_id": "C0051",
          "location": "第9项",
          "title": "9.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "9.3\n双方确认，本协议全部条款均已充分向对方提示、说明，双方均完整理解条款含义，自愿签署本协议。\n以下无正文"
        },
        {
          "clause_id": "C0052",
          "location": "甲方（盖章）：上海律智人工智能科技有限公司",
          "title": "甲方（盖章）：上海律智人工智能科技有限公司",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "甲方（盖章）：上海律智人工智能科技有限公司\n法定代表人或授权代表签字：周明远\n日期：2026年9月8日"
        },
        {
          "clause_id": "C0053",
          "location": "乙方（签字）：陈浩然",
          "title": "乙方（签字）：陈浩然",
          "section_type": "正式合同条款",
          "heading_path": [
            "9.3"
          ],
          "text": "乙方（签字）：陈浩然\n日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。",
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
          "text": "竞业限制协议\n本协议由以下双方于 2026年9月8日 在 上海市浦东新区 签订。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲方：上海律智人工智能科技有限公司\n统一社会信用代码：91310115MA7TEST001\n联系地址：上海市浦东新区张江高科技园区科苑路88号A座1201室\n法定代表人：周明远\n乙方：陈浩然\n身份证号：31010119900101XXXX\n户籍地址：江苏省南京市玄武区中山东路188号\n联系地址：上海市浦东新区碧云路588号3幢1202室\n联系电话：13800001234\n鉴于：\n甲乙双方于2024年3月1日签订了《劳动合同》（编号：LD-2024-0301-017），双方依法建立了劳动关系。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "甲乙双方一致理解并确认，乙方作为甲方的高级技术人员，在甲方工作期间不可避免地接触、了解和知悉与甲方生产、经营相关的秘密信息；\n乙方在甲方工作期间，甲方向乙方支付工作报酬，作为对价，乙方应对甲方负有在职忠实义务及在职竞业限制义务；\n若甲方要求乙方离职后继续承担竞业限制义务的，甲方应当依据法律规定及本协议约定向乙方足额支付竞业限制经济补偿金。",
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
          "clause_id": "C0001",
          "location": "全文",
          "title": "全文",
          "section_type": "正式合同条款",
          "heading_path": [
            "全文"
          ],
          "text": "依照《中华人民共和国民法典》《中华人民共和国劳动合同法》等有关法律之规定，甲乙双方在自愿、平等、协商一致的基础上，就乙方在甲方就职期间及离职后的一定期间内，竞业限制的有关事项，达成协议如下：",
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
          "location": "第1项",
          "title": "1. 释义",
          "section_type": "正式合同条款",
          "heading_path": [
            "1. 释义"
          ],
          "text": "1. 释义",
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
          "location": "1.1",
          "title": "1.1 竞业限制期：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.1 竞业限制期："
          ],
          "text": "1.1 竞业限制期：\n指自甲方和乙方任何一方与对方终止或解除劳动合同（不论终止或解除的理由）之日起的 2年内，乙方不得自营或为他人经营与公司有竞争的业务。",
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
          "location": "1.2",
          "title": "1.2 甲方竞争对手：",
          "section_type": "正式合同条款",
          "heading_path": [
            "1.2 甲方竞争对手："
          ],
          "text": "1.2 甲方竞争对手：\n指在中国区域内所从事的业务或经营活动与甲方主营业务相同或者近似的企业、公司或个人；包括但不限于下列公司：\n北京法智云科技有限公司、深圳合同智能科技有限公司、杭州智审科技有限公司、广州法务人工智能有限公司，以及其他从事人工智能合同审查、智能法律咨询、企业法务SaaS、法律大模型及相关业务的企业。",
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
      "searched_document_hash": "1707e89bfe48138bfeddb2e31a09b81e8ed73dbd536e337bcf8e948891732223",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0047",
          "location": "第8项",
          "title": "8.3",
          "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。",
          "quote": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。",
          "original_excerpt": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。",
          "section_type": "正式合同条款",
          "heading_path": [
            "8.3"
          ],
          "source_start": 0,
          "source_end": 95,
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
      "clause_id": "C0047",
      "location": "第8项",
      "title": "8.3",
      "text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。",
      "quote": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。",
      "original_excerpt": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。",
      "section_type": "正式合同条款",
      "heading_path": [
        "8.3"
      ],
      "source_start": 4440,
      "source_end": 4535,
      "supports_element_ids": [
        "employment_dispute_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第8项",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。",
      "source_span": {
        "start_offset": 4440,
        "end_offset": 4535,
        "raw_text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0047",
        "section": "第8项",
        "sentence_index": 1,
        "quote": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "8.3\n任一方不愿调解，或者经调解无法达成一致，或者达成调解协议后一方不履行的，一方可向劳动合同履行地或甲方所在地的劳动争议仲裁委员会申请仲裁；\n对仲裁裁决不服的，可依法向人民法院提起诉讼。"
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
      "C0039",
      "C0040",
      "C0041",
      "C0042",
      "C0043",
      "C0044",
      "C0045",
      "C0046",
      "C0047",
      "C0048",
      "C0049",
      "C0050",
      "C0051",
      "C0052",
      "C0053"
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
    "contract_type": "non_compete",
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