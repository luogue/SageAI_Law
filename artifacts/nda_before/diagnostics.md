# 劳动合同逐项证据诊断

输入文件：71 保密协议.docx
输入 SHA256：5b423e488330bdac95371bc608a07baaa18cb28d47c5bd5b0897a0aac7ad499d
normalized SHA256：f0db0bb21d4ad60f16ad8412a48ef969d4ab96f84b7984ba71c50329f0ef3701

| rule_id | 最终状态 | 理由 |
|---|---|---|
| NDA-03-01 | MISSING | 未找到明确约定：信息提供方或用人单位可识别、信息接收方或劳动者可识别。 |
| NDA-01-01 | PARTIAL | 未找到明确约定：公开信息、合法独立取得及法定披露除外。 |
| NDA-02-01 | PARTIAL | 未找到明确约定：资料返还或销毁安排。 |
| NDA-04-01 | MISSING | 未找到明确约定：保密违反的停止侵害或损失赔偿。 |
| EMP-14-01 | PASS | 全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。 |
| NC-01-01 | N/A | 未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。 |
| NC-02-01 | N/A | 未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。 |
| NC-03-01 | N/A | 未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。 |

## 全部 SEARCH_AUDIT NOT FOUND

```json
[
  {
    "rule_id": "NDA-03-01",
    "element_id": "confidentiality_parties_1",
    "review_id": "NDA-03-01",
    "search_targets": [
      "信息提供方或用人单位可识别"
    ],
    "query_patterns": [
      "(?:披露方|用人单位)[：:][^。；_]{2,60}"
    ],
    "query_semantic_target": "信息提供方或用人单位可识别",
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
      "C0030"
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
        "text": "保密协议"
      },
      {
        "clause_id": "C0002",
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
      },
      {
        "clause_id": "C0003",
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义"
      },
      {
        "clause_id": "C0004",
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
      },
      {
        "clause_id": "C0005",
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
      },
      {
        "clause_id": "C0006",
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
      },
      {
        "clause_id": "C0007",
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
      },
      {
        "clause_id": "C0008",
        "location": "第一章 定义 / 保密信息不包括：",
        "title": "保密信息不包括：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "保密信息不包括："
        ],
        "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
      },
      {
        "clause_id": "C0009",
        "location": "第二章 双方义务",
        "title": "第二章 双方义务",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务"
        ],
        "text": "第二章 双方义务"
      },
      {
        "clause_id": "C0010",
        "location": "第二章 双方义务第1项",
        "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        ],
        "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
      },
      {
        "clause_id": "C0011",
        "location": "第二章 双方义务第2项",
        "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        ],
        "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
      },
      {
        "clause_id": "C0012",
        "location": "第二章 双方义务第3项",
        "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        ],
        "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
      },
      {
        "clause_id": "C0013",
        "location": "第二章 双方义务第4项",
        "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        ],
        "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
      },
      {
        "clause_id": "C0014",
        "location": "第二章 双方义务第5项",
        "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        ],
        "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
      },
      {
        "clause_id": "C0015",
        "location": "第二章 双方义务第6项",
        "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        ],
        "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
      },
      {
        "clause_id": "C0016",
        "location": "第二章 双方义务第7项",
        "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        ],
        "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
      },
      {
        "clause_id": "C0017",
        "location": "第二章 双方义务第8项",
        "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        ],
        "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
      },
      {
        "clause_id": "C0018",
        "location": "第二章 双方义务第9项",
        "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        ],
        "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
      },
      {
        "clause_id": "C0019",
        "location": "第三章 违约责任",
        "title": "第三章 违约责任",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任"
        ],
        "text": "第三章 违约责任"
      },
      {
        "clause_id": "C0020",
        "location": "第三章 违约责任第1项",
        "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
        ],
        "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
      },
      {
        "clause_id": "C0021",
        "location": "第三章 违约责任第2项",
        "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        ],
        "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
      },
      {
        "clause_id": "C0022",
        "location": "第三章 违约责任第3项",
        "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        ],
        "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
      },
      {
        "clause_id": "C0023",
        "location": "第四章 争议解决",
        "title": "第四章 争议解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决"
        ],
        "text": "第四章 争议解决"
      },
      {
        "clause_id": "C0024",
        "location": "第四章 争议解决第1项",
        "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        ],
        "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
      },
      {
        "clause_id": "C0025",
        "location": "第四章 争议解决第2项",
        "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        ],
        "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
      },
      {
        "clause_id": "C0026",
        "location": "第四章 争议解决第3项",
        "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        ],
        "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
      },
      {
        "clause_id": "C0027",
        "location": "第四章 争议解决第4项",
        "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        ],
        "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
      },
      {
        "clause_id": "C0028",
        "location": "第五章 其他条款",
        "title": "第五章 其他条款",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款"
        ],
        "text": "第五章 其他条款"
      },
      {
        "clause_id": "C0029",
        "location": "第五章 其他条款第1项",
        "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        ],
        "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
      },
      {
        "clause_id": "C0030",
        "location": "第五章 其他条款第2项",
        "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
        ],
        "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
        "text": "保密协议",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "为此，经友好协商，双方就如下条款达成协议。",
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
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义",
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
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
    "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NDA-03-01",
    "element_id": "confidentiality_parties_2",
    "review_id": "NDA-03-01",
    "search_targets": [
      "信息接收方或劳动者可识别"
    ],
    "query_patterns": [
      "(?:接收方|劳动者)[：:][^。；_]{2,60}"
    ],
    "query_semantic_target": "信息接收方或劳动者可识别",
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
      "C0030"
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
        "text": "保密协议"
      },
      {
        "clause_id": "C0002",
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
      },
      {
        "clause_id": "C0003",
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义"
      },
      {
        "clause_id": "C0004",
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
      },
      {
        "clause_id": "C0005",
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
      },
      {
        "clause_id": "C0006",
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
      },
      {
        "clause_id": "C0007",
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
      },
      {
        "clause_id": "C0008",
        "location": "第一章 定义 / 保密信息不包括：",
        "title": "保密信息不包括：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "保密信息不包括："
        ],
        "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
      },
      {
        "clause_id": "C0009",
        "location": "第二章 双方义务",
        "title": "第二章 双方义务",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务"
        ],
        "text": "第二章 双方义务"
      },
      {
        "clause_id": "C0010",
        "location": "第二章 双方义务第1项",
        "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        ],
        "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
      },
      {
        "clause_id": "C0011",
        "location": "第二章 双方义务第2项",
        "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        ],
        "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
      },
      {
        "clause_id": "C0012",
        "location": "第二章 双方义务第3项",
        "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        ],
        "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
      },
      {
        "clause_id": "C0013",
        "location": "第二章 双方义务第4项",
        "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        ],
        "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
      },
      {
        "clause_id": "C0014",
        "location": "第二章 双方义务第5项",
        "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        ],
        "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
      },
      {
        "clause_id": "C0015",
        "location": "第二章 双方义务第6项",
        "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        ],
        "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
      },
      {
        "clause_id": "C0016",
        "location": "第二章 双方义务第7项",
        "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        ],
        "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
      },
      {
        "clause_id": "C0017",
        "location": "第二章 双方义务第8项",
        "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        ],
        "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
      },
      {
        "clause_id": "C0018",
        "location": "第二章 双方义务第9项",
        "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        ],
        "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
      },
      {
        "clause_id": "C0019",
        "location": "第三章 违约责任",
        "title": "第三章 违约责任",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任"
        ],
        "text": "第三章 违约责任"
      },
      {
        "clause_id": "C0020",
        "location": "第三章 违约责任第1项",
        "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
        ],
        "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
      },
      {
        "clause_id": "C0021",
        "location": "第三章 违约责任第2项",
        "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        ],
        "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
      },
      {
        "clause_id": "C0022",
        "location": "第三章 违约责任第3项",
        "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        ],
        "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
      },
      {
        "clause_id": "C0023",
        "location": "第四章 争议解决",
        "title": "第四章 争议解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决"
        ],
        "text": "第四章 争议解决"
      },
      {
        "clause_id": "C0024",
        "location": "第四章 争议解决第1项",
        "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        ],
        "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
      },
      {
        "clause_id": "C0025",
        "location": "第四章 争议解决第2项",
        "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        ],
        "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
      },
      {
        "clause_id": "C0026",
        "location": "第四章 争议解决第3项",
        "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        ],
        "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
      },
      {
        "clause_id": "C0027",
        "location": "第四章 争议解决第4项",
        "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        ],
        "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
      },
      {
        "clause_id": "C0028",
        "location": "第五章 其他条款",
        "title": "第五章 其他条款",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款"
        ],
        "text": "第五章 其他条款"
      },
      {
        "clause_id": "C0029",
        "location": "第五章 其他条款第1项",
        "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        ],
        "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
      },
      {
        "clause_id": "C0030",
        "location": "第五章 其他条款第2项",
        "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
        ],
        "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
        "text": "保密协议",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "为此，经友好协商，双方就如下条款达成协议。",
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
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义",
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
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
    "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NDA-01-01",
    "element_id": "employment_secret_scope_2",
    "review_id": "NDA-01-01",
    "search_targets": [
      "公开信息、合法独立取得及法定披露除外"
    ],
    "query_patterns": [
      "(?:公开信息|已公开|独立开发|合法取得).{0,45}(?:除外|不属于|不受|不承担)|(?:不包括|除外).{0,40}(?:公开信息|独立开发)"
    ],
    "query_semantic_target": "公开信息、合法独立取得及法定披露除外",
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
      "C0030"
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
        "text": "保密协议"
      },
      {
        "clause_id": "C0002",
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
      },
      {
        "clause_id": "C0003",
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义"
      },
      {
        "clause_id": "C0004",
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
      },
      {
        "clause_id": "C0005",
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
      },
      {
        "clause_id": "C0006",
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
      },
      {
        "clause_id": "C0007",
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
      },
      {
        "clause_id": "C0008",
        "location": "第一章 定义 / 保密信息不包括：",
        "title": "保密信息不包括：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "保密信息不包括："
        ],
        "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
      },
      {
        "clause_id": "C0009",
        "location": "第二章 双方义务",
        "title": "第二章 双方义务",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务"
        ],
        "text": "第二章 双方义务"
      },
      {
        "clause_id": "C0010",
        "location": "第二章 双方义务第1项",
        "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        ],
        "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
      },
      {
        "clause_id": "C0011",
        "location": "第二章 双方义务第2项",
        "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        ],
        "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
      },
      {
        "clause_id": "C0012",
        "location": "第二章 双方义务第3项",
        "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        ],
        "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
      },
      {
        "clause_id": "C0013",
        "location": "第二章 双方义务第4项",
        "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        ],
        "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
      },
      {
        "clause_id": "C0014",
        "location": "第二章 双方义务第5项",
        "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        ],
        "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
      },
      {
        "clause_id": "C0015",
        "location": "第二章 双方义务第6项",
        "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        ],
        "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
      },
      {
        "clause_id": "C0016",
        "location": "第二章 双方义务第7项",
        "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        ],
        "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
      },
      {
        "clause_id": "C0017",
        "location": "第二章 双方义务第8项",
        "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        ],
        "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
      },
      {
        "clause_id": "C0018",
        "location": "第二章 双方义务第9项",
        "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        ],
        "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
      },
      {
        "clause_id": "C0019",
        "location": "第三章 违约责任",
        "title": "第三章 违约责任",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任"
        ],
        "text": "第三章 违约责任"
      },
      {
        "clause_id": "C0020",
        "location": "第三章 违约责任第1项",
        "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
        ],
        "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
      },
      {
        "clause_id": "C0021",
        "location": "第三章 违约责任第2项",
        "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        ],
        "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
      },
      {
        "clause_id": "C0022",
        "location": "第三章 违约责任第3项",
        "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        ],
        "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
      },
      {
        "clause_id": "C0023",
        "location": "第四章 争议解决",
        "title": "第四章 争议解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决"
        ],
        "text": "第四章 争议解决"
      },
      {
        "clause_id": "C0024",
        "location": "第四章 争议解决第1项",
        "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        ],
        "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
      },
      {
        "clause_id": "C0025",
        "location": "第四章 争议解决第2项",
        "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        ],
        "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
      },
      {
        "clause_id": "C0026",
        "location": "第四章 争议解决第3项",
        "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        ],
        "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
      },
      {
        "clause_id": "C0027",
        "location": "第四章 争议解决第4项",
        "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        ],
        "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
      },
      {
        "clause_id": "C0028",
        "location": "第五章 其他条款",
        "title": "第五章 其他条款",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款"
        ],
        "text": "第五章 其他条款"
      },
      {
        "clause_id": "C0029",
        "location": "第五章 其他条款第1项",
        "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        ],
        "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
      },
      {
        "clause_id": "C0030",
        "location": "第五章 其他条款第2项",
        "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
        ],
        "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
        "text": "保密协议",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "为此，经友好协商，双方就如下条款达成协议。",
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
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义",
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
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
    "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NDA-02-01",
    "element_id": "employment_secret_duty_3",
    "review_id": "NDA-02-01",
    "search_targets": [
      "资料返还或销毁安排"
    ],
    "query_patterns": [
      "(?:终止|离职|要求).{0,45}(?:返还|销毁).{0,20}(?:资料|保密信息)"
    ],
    "query_semantic_target": "资料返还或销毁安排",
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
      "C0030"
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
        "text": "保密协议"
      },
      {
        "clause_id": "C0002",
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
      },
      {
        "clause_id": "C0003",
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义"
      },
      {
        "clause_id": "C0004",
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
      },
      {
        "clause_id": "C0005",
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
      },
      {
        "clause_id": "C0006",
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
      },
      {
        "clause_id": "C0007",
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
      },
      {
        "clause_id": "C0008",
        "location": "第一章 定义 / 保密信息不包括：",
        "title": "保密信息不包括：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "保密信息不包括："
        ],
        "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
      },
      {
        "clause_id": "C0009",
        "location": "第二章 双方义务",
        "title": "第二章 双方义务",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务"
        ],
        "text": "第二章 双方义务"
      },
      {
        "clause_id": "C0010",
        "location": "第二章 双方义务第1项",
        "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        ],
        "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
      },
      {
        "clause_id": "C0011",
        "location": "第二章 双方义务第2项",
        "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        ],
        "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
      },
      {
        "clause_id": "C0012",
        "location": "第二章 双方义务第3项",
        "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        ],
        "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
      },
      {
        "clause_id": "C0013",
        "location": "第二章 双方义务第4项",
        "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        ],
        "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
      },
      {
        "clause_id": "C0014",
        "location": "第二章 双方义务第5项",
        "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        ],
        "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
      },
      {
        "clause_id": "C0015",
        "location": "第二章 双方义务第6项",
        "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        ],
        "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
      },
      {
        "clause_id": "C0016",
        "location": "第二章 双方义务第7项",
        "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        ],
        "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
      },
      {
        "clause_id": "C0017",
        "location": "第二章 双方义务第8项",
        "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        ],
        "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
      },
      {
        "clause_id": "C0018",
        "location": "第二章 双方义务第9项",
        "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        ],
        "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
      },
      {
        "clause_id": "C0019",
        "location": "第三章 违约责任",
        "title": "第三章 违约责任",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任"
        ],
        "text": "第三章 违约责任"
      },
      {
        "clause_id": "C0020",
        "location": "第三章 违约责任第1项",
        "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
        ],
        "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
      },
      {
        "clause_id": "C0021",
        "location": "第三章 违约责任第2项",
        "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        ],
        "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
      },
      {
        "clause_id": "C0022",
        "location": "第三章 违约责任第3项",
        "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        ],
        "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
      },
      {
        "clause_id": "C0023",
        "location": "第四章 争议解决",
        "title": "第四章 争议解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决"
        ],
        "text": "第四章 争议解决"
      },
      {
        "clause_id": "C0024",
        "location": "第四章 争议解决第1项",
        "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        ],
        "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
      },
      {
        "clause_id": "C0025",
        "location": "第四章 争议解决第2项",
        "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        ],
        "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
      },
      {
        "clause_id": "C0026",
        "location": "第四章 争议解决第3项",
        "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        ],
        "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
      },
      {
        "clause_id": "C0027",
        "location": "第四章 争议解决第4项",
        "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        ],
        "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
      },
      {
        "clause_id": "C0028",
        "location": "第五章 其他条款",
        "title": "第五章 其他条款",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款"
        ],
        "text": "第五章 其他条款"
      },
      {
        "clause_id": "C0029",
        "location": "第五章 其他条款第1项",
        "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        ],
        "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
      },
      {
        "clause_id": "C0030",
        "location": "第五章 其他条款第2项",
        "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
        ],
        "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
        "text": "保密协议",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "为此，经友好协商，双方就如下条款达成协议。",
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
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义",
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
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
    "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  },
  {
    "rule_id": "NDA-04-01",
    "element_id": "confidentiality_remedies_1",
    "review_id": "NDA-04-01",
    "search_targets": [
      "保密违反的停止侵害或损失赔偿"
    ],
    "query_patterns": [
      "(?:违反保密义务|泄露保密信息|泄露商业秘密).{0,65}(?:赔偿|停止侵害|消除影响)"
    ],
    "query_semantic_target": "保密违反的停止侵害或损失赔偿",
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
      "C0030"
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
        "text": "保密协议"
      },
      {
        "clause_id": "C0002",
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
      },
      {
        "clause_id": "C0003",
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义"
      },
      {
        "clause_id": "C0004",
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
      },
      {
        "clause_id": "C0005",
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
      },
      {
        "clause_id": "C0006",
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
      },
      {
        "clause_id": "C0007",
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
      },
      {
        "clause_id": "C0008",
        "location": "第一章 定义 / 保密信息不包括：",
        "title": "保密信息不包括：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "保密信息不包括："
        ],
        "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
      },
      {
        "clause_id": "C0009",
        "location": "第二章 双方义务",
        "title": "第二章 双方义务",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务"
        ],
        "text": "第二章 双方义务"
      },
      {
        "clause_id": "C0010",
        "location": "第二章 双方义务第1项",
        "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        ],
        "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
      },
      {
        "clause_id": "C0011",
        "location": "第二章 双方义务第2项",
        "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        ],
        "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
      },
      {
        "clause_id": "C0012",
        "location": "第二章 双方义务第3项",
        "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        ],
        "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
      },
      {
        "clause_id": "C0013",
        "location": "第二章 双方义务第4项",
        "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        ],
        "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
      },
      {
        "clause_id": "C0014",
        "location": "第二章 双方义务第5项",
        "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        ],
        "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
      },
      {
        "clause_id": "C0015",
        "location": "第二章 双方义务第6项",
        "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        ],
        "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
      },
      {
        "clause_id": "C0016",
        "location": "第二章 双方义务第7项",
        "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        ],
        "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
      },
      {
        "clause_id": "C0017",
        "location": "第二章 双方义务第8项",
        "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        ],
        "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
      },
      {
        "clause_id": "C0018",
        "location": "第二章 双方义务第9项",
        "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第二章 双方义务",
          "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        ],
        "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
      },
      {
        "clause_id": "C0019",
        "location": "第三章 违约责任",
        "title": "第三章 违约责任",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任"
        ],
        "text": "第三章 违约责任"
      },
      {
        "clause_id": "C0020",
        "location": "第三章 违约责任第1项",
        "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
        ],
        "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
      },
      {
        "clause_id": "C0021",
        "location": "第三章 违约责任第2项",
        "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        ],
        "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
      },
      {
        "clause_id": "C0022",
        "location": "第三章 违约责任第3项",
        "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第三章 违约责任",
          "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        ],
        "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
      },
      {
        "clause_id": "C0023",
        "location": "第四章 争议解决",
        "title": "第四章 争议解决",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决"
        ],
        "text": "第四章 争议解决"
      },
      {
        "clause_id": "C0024",
        "location": "第四章 争议解决第1项",
        "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        ],
        "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
      },
      {
        "clause_id": "C0025",
        "location": "第四章 争议解决第2项",
        "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        ],
        "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
      },
      {
        "clause_id": "C0026",
        "location": "第四章 争议解决第3项",
        "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        ],
        "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
      },
      {
        "clause_id": "C0027",
        "location": "第四章 争议解决第4项",
        "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第四章 争议解决",
          "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        ],
        "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
      },
      {
        "clause_id": "C0028",
        "location": "第五章 其他条款",
        "title": "第五章 其他条款",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款"
        ],
        "text": "第五章 其他条款"
      },
      {
        "clause_id": "C0029",
        "location": "第五章 其他条款第1项",
        "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        ],
        "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
      },
      {
        "clause_id": "C0030",
        "location": "第五章 其他条款第2项",
        "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
        "section_type": "正式合同条款",
        "heading_path": [
          "第五章 其他条款",
          "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
        ],
        "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
        "text": "保密协议",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
        "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
        "section_type": "正式合同条款",
        "heading_path": [
          "本保密协议（以下简称“本协议”）由以下双方签署："
        ],
        "text": "为此，经友好协商，双方就如下条款达成协议。",
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
        "location": "第一章 定义",
        "title": "第一章 定义",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义"
        ],
        "text": "第一章 定义",
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
        "location": "第一章 定义 / 1、协议项下活动：",
        "title": "1、协议项下活动：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "1、协议项下活动："
        ],
        "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
        "location": "第一章 定义 / 2、信息披露方与接受方：",
        "title": "2、信息披露方与接受方：",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "2、信息披露方与接受方："
        ],
        "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
        "location": "第一章 定义第3项",
        "title": "3、关联机构",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "3、关联机构"
        ],
        "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
        "location": "第一章 定义第4项",
        "title": "4、保密信息",
        "section_type": "正式合同条款",
        "heading_path": [
          "第一章 定义",
          "4、保密信息"
        ],
        "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
    "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
    "result": "NOT_FOUND",
    "supporting_evidence": []
  }
]
```

## NDA-03-01

```json
{
  "rule_id": "NDA-03-01",
  "applicability": {
    "review_id": "NDA-03-01",
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
  "actual_status": "缺失",
  "reason": "未找到明确约定：信息提供方或用人单位可识别、信息接收方或劳动者可识别。",
  "coverage_elements": [
    {
      "review_id": "NDA-03-01",
      "element_id": "confidentiality_parties_1",
      "proposition": "信息提供方或用人单位可识别",
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
      "review_id": "NDA-03-01",
      "element_id": "confidentiality_parties_2",
      "proposition": "信息接收方或劳动者可识别",
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
      "element_id": "confidentiality_parties_1",
      "review_id": "NDA-03-01",
      "search_targets": [
        "信息提供方或用人单位可识别"
      ],
      "query_patterns": [
        "(?:披露方|用人单位)[：:][^。；_]{2,60}"
      ],
      "query_semantic_target": "信息提供方或用人单位可识别",
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
        "C0030"
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
          "text": "保密协议"
        },
        {
          "clause_id": "C0002",
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
        },
        {
          "clause_id": "C0003",
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义"
        },
        {
          "clause_id": "C0004",
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
        },
        {
          "clause_id": "C0005",
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
        },
        {
          "clause_id": "C0006",
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
        },
        {
          "clause_id": "C0007",
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
        },
        {
          "clause_id": "C0008",
          "location": "第一章 定义 / 保密信息不包括：",
          "title": "保密信息不包括：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "保密信息不包括："
          ],
          "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
        },
        {
          "clause_id": "C0009",
          "location": "第二章 双方义务",
          "title": "第二章 双方义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务"
          ],
          "text": "第二章 双方义务"
        },
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        },
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        },
        {
          "clause_id": "C0012",
          "location": "第二章 双方义务第3项",
          "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
          ],
          "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        },
        {
          "clause_id": "C0013",
          "location": "第二章 双方义务第4项",
          "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
          ],
          "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        },
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        },
        {
          "clause_id": "C0015",
          "location": "第二章 双方义务第6项",
          "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
          ],
          "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        },
        {
          "clause_id": "C0016",
          "location": "第二章 双方义务第7项",
          "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
          ],
          "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        },
        {
          "clause_id": "C0017",
          "location": "第二章 双方义务第8项",
          "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
          ],
          "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        },
        {
          "clause_id": "C0018",
          "location": "第二章 双方义务第9项",
          "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
          ],
          "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        },
        {
          "clause_id": "C0019",
          "location": "第三章 违约责任",
          "title": "第三章 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任"
          ],
          "text": "第三章 违约责任"
        },
        {
          "clause_id": "C0020",
          "location": "第三章 违约责任第1项",
          "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
          ],
          "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
        },
        {
          "clause_id": "C0021",
          "location": "第三章 违约责任第2项",
          "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
          ],
          "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        },
        {
          "clause_id": "C0022",
          "location": "第三章 违约责任第3项",
          "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
          ],
          "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        },
        {
          "clause_id": "C0023",
          "location": "第四章 争议解决",
          "title": "第四章 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决"
          ],
          "text": "第四章 争议解决"
        },
        {
          "clause_id": "C0024",
          "location": "第四章 争议解决第1项",
          "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
          ],
          "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        },
        {
          "clause_id": "C0025",
          "location": "第四章 争议解决第2项",
          "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
          ],
          "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        },
        {
          "clause_id": "C0026",
          "location": "第四章 争议解决第3项",
          "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
          ],
          "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        },
        {
          "clause_id": "C0027",
          "location": "第四章 争议解决第4项",
          "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
          ],
          "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第五章 其他条款",
          "title": "第五章 其他条款",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款"
          ],
          "text": "第五章 其他条款"
        },
        {
          "clause_id": "C0029",
          "location": "第五章 其他条款第1项",
          "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
          ],
          "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        },
        {
          "clause_id": "C0030",
          "location": "第五章 其他条款第2项",
          "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
          ],
          "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
          "text": "保密协议",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "为此，经友好协商，双方就如下条款达成协议。",
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
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义",
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
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
      "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    },
    {
      "element_id": "confidentiality_parties_2",
      "review_id": "NDA-03-01",
      "search_targets": [
        "信息接收方或劳动者可识别"
      ],
      "query_patterns": [
        "(?:接收方|劳动者)[：:][^。；_]{2,60}"
      ],
      "query_semantic_target": "信息接收方或劳动者可识别",
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
        "C0030"
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
          "text": "保密协议"
        },
        {
          "clause_id": "C0002",
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
        },
        {
          "clause_id": "C0003",
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义"
        },
        {
          "clause_id": "C0004",
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
        },
        {
          "clause_id": "C0005",
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
        },
        {
          "clause_id": "C0006",
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
        },
        {
          "clause_id": "C0007",
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
        },
        {
          "clause_id": "C0008",
          "location": "第一章 定义 / 保密信息不包括：",
          "title": "保密信息不包括：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "保密信息不包括："
          ],
          "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
        },
        {
          "clause_id": "C0009",
          "location": "第二章 双方义务",
          "title": "第二章 双方义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务"
          ],
          "text": "第二章 双方义务"
        },
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        },
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        },
        {
          "clause_id": "C0012",
          "location": "第二章 双方义务第3项",
          "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
          ],
          "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        },
        {
          "clause_id": "C0013",
          "location": "第二章 双方义务第4项",
          "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
          ],
          "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        },
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        },
        {
          "clause_id": "C0015",
          "location": "第二章 双方义务第6项",
          "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
          ],
          "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        },
        {
          "clause_id": "C0016",
          "location": "第二章 双方义务第7项",
          "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
          ],
          "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        },
        {
          "clause_id": "C0017",
          "location": "第二章 双方义务第8项",
          "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
          ],
          "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        },
        {
          "clause_id": "C0018",
          "location": "第二章 双方义务第9项",
          "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
          ],
          "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        },
        {
          "clause_id": "C0019",
          "location": "第三章 违约责任",
          "title": "第三章 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任"
          ],
          "text": "第三章 违约责任"
        },
        {
          "clause_id": "C0020",
          "location": "第三章 违约责任第1项",
          "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
          ],
          "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
        },
        {
          "clause_id": "C0021",
          "location": "第三章 违约责任第2项",
          "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
          ],
          "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        },
        {
          "clause_id": "C0022",
          "location": "第三章 违约责任第3项",
          "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
          ],
          "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        },
        {
          "clause_id": "C0023",
          "location": "第四章 争议解决",
          "title": "第四章 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决"
          ],
          "text": "第四章 争议解决"
        },
        {
          "clause_id": "C0024",
          "location": "第四章 争议解决第1项",
          "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
          ],
          "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        },
        {
          "clause_id": "C0025",
          "location": "第四章 争议解决第2项",
          "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
          ],
          "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        },
        {
          "clause_id": "C0026",
          "location": "第四章 争议解决第3项",
          "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
          ],
          "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        },
        {
          "clause_id": "C0027",
          "location": "第四章 争议解决第4项",
          "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
          ],
          "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第五章 其他条款",
          "title": "第五章 其他条款",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款"
          ],
          "text": "第五章 其他条款"
        },
        {
          "clause_id": "C0029",
          "location": "第五章 其他条款第1项",
          "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
          ],
          "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        },
        {
          "clause_id": "C0030",
          "location": "第五章 其他条款第2项",
          "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
          ],
          "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
          "text": "保密协议",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "为此，经友好协商，双方就如下条款达成协议。",
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
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义",
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
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
      "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [],
  "termination_classification": []
}
```

## NDA-01-01

```json
{
  "rule_id": "NDA-01-01",
  "applicability": {
    "review_id": "NDA-01-01",
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
  "reason": "未找到明确约定：公开信息、合法独立取得及法定披露除外。",
  "coverage_elements": [
    {
      "review_id": "NDA-01-01",
      "element_id": "employment_secret_scope_1",
      "proposition": "明确受保护的信息内容",
      "status": "COVERED",
      "evidence_ids": [
        "C0010"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0010"
      ],
      "source_spans": [
        "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。"
      ],
      "source_locations": [
        "第二章 双方义务第1项"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0010"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0010"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0010",
          "quote": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。"
        }
      ]
    },
    {
      "review_id": "NDA-01-01",
      "element_id": "employment_secret_scope_2",
      "proposition": "公开信息、合法独立取得及法定披露除外",
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
      "element_id": "employment_secret_scope_1",
      "review_id": "NDA-01-01",
      "search_targets": [
        "明确受保护的信息内容"
      ],
      "query_patterns": [
        "(?:保密信息|商业秘密)(?:范围|内容)?(?:包括|为|：|:)[^。；_]{3,100}"
      ],
      "query_semantic_target": "明确受保护的信息内容",
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
        "C0030"
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
          "text": "保密协议"
        },
        {
          "clause_id": "C0002",
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
        },
        {
          "clause_id": "C0003",
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义"
        },
        {
          "clause_id": "C0004",
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
        },
        {
          "clause_id": "C0005",
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
        },
        {
          "clause_id": "C0006",
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
        },
        {
          "clause_id": "C0007",
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
        },
        {
          "clause_id": "C0008",
          "location": "第一章 定义 / 保密信息不包括：",
          "title": "保密信息不包括：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "保密信息不包括："
          ],
          "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
        },
        {
          "clause_id": "C0009",
          "location": "第二章 双方义务",
          "title": "第二章 双方义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务"
          ],
          "text": "第二章 双方义务"
        },
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        },
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        },
        {
          "clause_id": "C0012",
          "location": "第二章 双方义务第3项",
          "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
          ],
          "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        },
        {
          "clause_id": "C0013",
          "location": "第二章 双方义务第4项",
          "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
          ],
          "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        },
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        },
        {
          "clause_id": "C0015",
          "location": "第二章 双方义务第6项",
          "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
          ],
          "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        },
        {
          "clause_id": "C0016",
          "location": "第二章 双方义务第7项",
          "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
          ],
          "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        },
        {
          "clause_id": "C0017",
          "location": "第二章 双方义务第8项",
          "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
          ],
          "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        },
        {
          "clause_id": "C0018",
          "location": "第二章 双方义务第9项",
          "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
          ],
          "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        },
        {
          "clause_id": "C0019",
          "location": "第三章 违约责任",
          "title": "第三章 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任"
          ],
          "text": "第三章 违约责任"
        },
        {
          "clause_id": "C0020",
          "location": "第三章 违约责任第1项",
          "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
          ],
          "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
        },
        {
          "clause_id": "C0021",
          "location": "第三章 违约责任第2项",
          "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
          ],
          "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        },
        {
          "clause_id": "C0022",
          "location": "第三章 违约责任第3项",
          "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
          ],
          "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        },
        {
          "clause_id": "C0023",
          "location": "第四章 争议解决",
          "title": "第四章 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决"
          ],
          "text": "第四章 争议解决"
        },
        {
          "clause_id": "C0024",
          "location": "第四章 争议解决第1项",
          "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
          ],
          "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        },
        {
          "clause_id": "C0025",
          "location": "第四章 争议解决第2项",
          "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
          ],
          "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        },
        {
          "clause_id": "C0026",
          "location": "第四章 争议解决第3项",
          "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
          ],
          "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        },
        {
          "clause_id": "C0027",
          "location": "第四章 争议解决第4项",
          "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
          ],
          "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第五章 其他条款",
          "title": "第五章 其他条款",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款"
          ],
          "text": "第五章 其他条款"
        },
        {
          "clause_id": "C0029",
          "location": "第五章 其他条款第1项",
          "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
          ],
          "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        },
        {
          "clause_id": "C0030",
          "location": "第五章 其他条款第2项",
          "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
          ],
          "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:保密信息|商业秘密)(?:范围|内容)?(?:包括|为|：|:)[^。；_]{3,100}"
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
          "text": "保密协议",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "为此，经友好协商，双方就如下条款达成协议。",
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
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义",
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
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
      "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。",
          "quote": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。",
          "original_excerpt": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "source_start": 0,
          "source_end": 155,
          "supports_element_ids": [
            "employment_secret_scope_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_secret_scope_2",
      "review_id": "NDA-01-01",
      "search_targets": [
        "公开信息、合法独立取得及法定披露除外"
      ],
      "query_patterns": [
        "(?:公开信息|已公开|独立开发|合法取得).{0,45}(?:除外|不属于|不受|不承担)|(?:不包括|除外).{0,40}(?:公开信息|独立开发)"
      ],
      "query_semantic_target": "公开信息、合法独立取得及法定披露除外",
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
        "C0030"
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
          "text": "保密协议"
        },
        {
          "clause_id": "C0002",
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
        },
        {
          "clause_id": "C0003",
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义"
        },
        {
          "clause_id": "C0004",
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
        },
        {
          "clause_id": "C0005",
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
        },
        {
          "clause_id": "C0006",
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
        },
        {
          "clause_id": "C0007",
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
        },
        {
          "clause_id": "C0008",
          "location": "第一章 定义 / 保密信息不包括：",
          "title": "保密信息不包括：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "保密信息不包括："
          ],
          "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
        },
        {
          "clause_id": "C0009",
          "location": "第二章 双方义务",
          "title": "第二章 双方义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务"
          ],
          "text": "第二章 双方义务"
        },
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        },
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        },
        {
          "clause_id": "C0012",
          "location": "第二章 双方义务第3项",
          "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
          ],
          "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        },
        {
          "clause_id": "C0013",
          "location": "第二章 双方义务第4项",
          "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
          ],
          "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        },
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        },
        {
          "clause_id": "C0015",
          "location": "第二章 双方义务第6项",
          "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
          ],
          "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        },
        {
          "clause_id": "C0016",
          "location": "第二章 双方义务第7项",
          "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
          ],
          "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        },
        {
          "clause_id": "C0017",
          "location": "第二章 双方义务第8项",
          "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
          ],
          "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        },
        {
          "clause_id": "C0018",
          "location": "第二章 双方义务第9项",
          "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
          ],
          "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        },
        {
          "clause_id": "C0019",
          "location": "第三章 违约责任",
          "title": "第三章 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任"
          ],
          "text": "第三章 违约责任"
        },
        {
          "clause_id": "C0020",
          "location": "第三章 违约责任第1项",
          "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
          ],
          "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
        },
        {
          "clause_id": "C0021",
          "location": "第三章 违约责任第2项",
          "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
          ],
          "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        },
        {
          "clause_id": "C0022",
          "location": "第三章 违约责任第3项",
          "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
          ],
          "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        },
        {
          "clause_id": "C0023",
          "location": "第四章 争议解决",
          "title": "第四章 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决"
          ],
          "text": "第四章 争议解决"
        },
        {
          "clause_id": "C0024",
          "location": "第四章 争议解决第1项",
          "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
          ],
          "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        },
        {
          "clause_id": "C0025",
          "location": "第四章 争议解决第2项",
          "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
          ],
          "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        },
        {
          "clause_id": "C0026",
          "location": "第四章 争议解决第3项",
          "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
          ],
          "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        },
        {
          "clause_id": "C0027",
          "location": "第四章 争议解决第4项",
          "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
          ],
          "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第五章 其他条款",
          "title": "第五章 其他条款",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款"
          ],
          "text": "第五章 其他条款"
        },
        {
          "clause_id": "C0029",
          "location": "第五章 其他条款第1项",
          "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
          ],
          "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        },
        {
          "clause_id": "C0030",
          "location": "第五章 其他条款第2项",
          "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
          ],
          "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
          "text": "保密协议",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "为此，经友好协商，双方就如下条款达成协议。",
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
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义",
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
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
      "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0010",
      "location": "第二章 双方义务第1项",
      "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
      "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。",
      "quote": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。",
      "original_excerpt": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二章 双方义务",
        "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
      ],
      "source_start": 963,
      "source_end": 1118,
      "supports_element_ids": [
        "employment_secret_scope_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二章 双方义务第1项",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。",
      "source_span": {
        "start_offset": 963,
        "end_offset": 1118,
        "raw_text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0010",
        "section": "第二章 双方义务第1项",
        "sentence_index": 1,
        "quote": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_secret_scope_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "NDA-01-01",
      "element_ids": [
        "employment_secret_scope_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "明确受保护的信息内容"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## NDA-02-01

```json
{
  "rule_id": "NDA-02-01",
  "applicability": {
    "review_id": "NDA-02-01",
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
  "reason": "未找到明确约定：资料返还或销毁安排。",
  "coverage_elements": [
    {
      "review_id": "NDA-02-01",
      "element_id": "employment_secret_duty_1",
      "proposition": "限制使用披露及接触人员",
      "status": "COVERED",
      "evidence_ids": [
        "C0011"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0011"
      ],
      "source_spans": [
        "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
      ],
      "source_locations": [
        "第二章 双方义务第2项"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0011"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0011"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0011",
          "quote": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        }
      ]
    },
    {
      "review_id": "NDA-02-01",
      "element_id": "employment_secret_duty_2",
      "proposition": "保密期限或信息公开后的终止条件",
      "status": "COVERED",
      "evidence_ids": [
        "C0014"
      ],
      "entailment": "SUPPORTS",
      "verifier_confidence": "high",
      "reason": "元素级证据可支撑。",
      "claim_id": "",
      "source_clause_ids": [
        "C0014"
      ],
      "source_spans": [
        "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
      ],
      "source_locations": [
        "第二章 双方义务第5项"
      ],
      "atomic": true,
      "child_elements": [],
      "legal_proposition_ids": [],
      "required_fact_key": "",
      "fact_status": "FOUND",
      "fact_value": null,
      "fact_evidence_refs": [
        "C0014"
      ],
      "requirement_status": "SATISFIED",
      "requirement_reason": "元素级证据可支撑。",
      "evidence_refs": [
        "C0014"
      ],
      "evidence_selection_reason": "Direct evidence selected by exact source-clause ownership for this element.",
      "supporting_evidence": [
        {
          "clause_id": "C0014",
          "quote": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        }
      ]
    },
    {
      "review_id": "NDA-02-01",
      "element_id": "employment_secret_duty_3",
      "proposition": "资料返还或销毁安排",
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
      "element_id": "employment_secret_duty_1",
      "review_id": "NDA-02-01",
      "search_targets": [
        "限制使用披露及接触人员"
      ],
      "query_patterns": [
        "(?:不得|未经.{0,20}同意不得).{0,25}(?:披露|泄露|使用).{0,25}(?:保密信息|商业秘密)"
      ],
      "query_semantic_target": "限制使用披露及接触人员",
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
        "C0030"
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
          "text": "保密协议"
        },
        {
          "clause_id": "C0002",
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
        },
        {
          "clause_id": "C0003",
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义"
        },
        {
          "clause_id": "C0004",
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
        },
        {
          "clause_id": "C0005",
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
        },
        {
          "clause_id": "C0006",
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
        },
        {
          "clause_id": "C0007",
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
        },
        {
          "clause_id": "C0008",
          "location": "第一章 定义 / 保密信息不包括：",
          "title": "保密信息不包括：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "保密信息不包括："
          ],
          "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
        },
        {
          "clause_id": "C0009",
          "location": "第二章 双方义务",
          "title": "第二章 双方义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务"
          ],
          "text": "第二章 双方义务"
        },
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        },
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        },
        {
          "clause_id": "C0012",
          "location": "第二章 双方义务第3项",
          "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
          ],
          "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        },
        {
          "clause_id": "C0013",
          "location": "第二章 双方义务第4项",
          "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
          ],
          "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        },
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        },
        {
          "clause_id": "C0015",
          "location": "第二章 双方义务第6项",
          "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
          ],
          "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        },
        {
          "clause_id": "C0016",
          "location": "第二章 双方义务第7项",
          "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
          ],
          "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        },
        {
          "clause_id": "C0017",
          "location": "第二章 双方义务第8项",
          "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
          ],
          "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        },
        {
          "clause_id": "C0018",
          "location": "第二章 双方义务第9项",
          "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
          ],
          "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        },
        {
          "clause_id": "C0019",
          "location": "第三章 违约责任",
          "title": "第三章 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任"
          ],
          "text": "第三章 违约责任"
        },
        {
          "clause_id": "C0020",
          "location": "第三章 违约责任第1项",
          "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
          ],
          "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
        },
        {
          "clause_id": "C0021",
          "location": "第三章 违约责任第2项",
          "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
          ],
          "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        },
        {
          "clause_id": "C0022",
          "location": "第三章 违约责任第3项",
          "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
          ],
          "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        },
        {
          "clause_id": "C0023",
          "location": "第四章 争议解决",
          "title": "第四章 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决"
          ],
          "text": "第四章 争议解决"
        },
        {
          "clause_id": "C0024",
          "location": "第四章 争议解决第1项",
          "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
          ],
          "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        },
        {
          "clause_id": "C0025",
          "location": "第四章 争议解决第2项",
          "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
          ],
          "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        },
        {
          "clause_id": "C0026",
          "location": "第四章 争议解决第3项",
          "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
          ],
          "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        },
        {
          "clause_id": "C0027",
          "location": "第四章 争议解决第4项",
          "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
          ],
          "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第五章 其他条款",
          "title": "第五章 其他条款",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款"
          ],
          "text": "第五章 其他条款"
        },
        {
          "clause_id": "C0029",
          "location": "第五章 其他条款第1项",
          "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
          ],
          "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        },
        {
          "clause_id": "C0030",
          "location": "第五章 其他条款第2项",
          "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
          ],
          "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "text": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "(?:不得|未经.{0,20}同意不得).{0,25}(?:披露|泄露|使用).{0,25}(?:保密信息|商业秘密)"
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
          "text": "保密协议",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "为此，经友好协商，双方就如下条款达成协议。",
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
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义",
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
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
      "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "text": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。",
          "quote": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。",
          "original_excerpt": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "source_start": 24,
          "source_end": 60,
          "supports_element_ids": [
            "employment_secret_duty_1"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_secret_duty_2",
      "review_id": "NDA-02-01",
      "search_targets": [
        "保密期限或信息公开后的终止条件"
      ],
      "query_patterns": [
        "保密(?:义务)?期限.{0,25}(?:年|月|公开)|保密义务.{0,30}至.{0,30}公开"
      ],
      "query_semantic_target": "保密期限或信息公开后的终止条件",
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
        "C0030"
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
          "text": "保密协议"
        },
        {
          "clause_id": "C0002",
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
        },
        {
          "clause_id": "C0003",
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义"
        },
        {
          "clause_id": "C0004",
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
        },
        {
          "clause_id": "C0005",
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
        },
        {
          "clause_id": "C0006",
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
        },
        {
          "clause_id": "C0007",
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
        },
        {
          "clause_id": "C0008",
          "location": "第一章 定义 / 保密信息不包括：",
          "title": "保密信息不包括：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "保密信息不包括："
          ],
          "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
        },
        {
          "clause_id": "C0009",
          "location": "第二章 双方义务",
          "title": "第二章 双方义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务"
          ],
          "text": "第二章 双方义务"
        },
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        },
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        },
        {
          "clause_id": "C0012",
          "location": "第二章 双方义务第3项",
          "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
          ],
          "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        },
        {
          "clause_id": "C0013",
          "location": "第二章 双方义务第4项",
          "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
          ],
          "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        },
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        },
        {
          "clause_id": "C0015",
          "location": "第二章 双方义务第6项",
          "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
          ],
          "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        },
        {
          "clause_id": "C0016",
          "location": "第二章 双方义务第7项",
          "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
          ],
          "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        },
        {
          "clause_id": "C0017",
          "location": "第二章 双方义务第8项",
          "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
          ],
          "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        },
        {
          "clause_id": "C0018",
          "location": "第二章 双方义务第9项",
          "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
          ],
          "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        },
        {
          "clause_id": "C0019",
          "location": "第三章 违约责任",
          "title": "第三章 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任"
          ],
          "text": "第三章 违约责任"
        },
        {
          "clause_id": "C0020",
          "location": "第三章 违约责任第1项",
          "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
          ],
          "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
        },
        {
          "clause_id": "C0021",
          "location": "第三章 违约责任第2项",
          "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
          ],
          "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        },
        {
          "clause_id": "C0022",
          "location": "第三章 违约责任第3项",
          "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
          ],
          "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        },
        {
          "clause_id": "C0023",
          "location": "第四章 争议解决",
          "title": "第四章 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决"
          ],
          "text": "第四章 争议解决"
        },
        {
          "clause_id": "C0024",
          "location": "第四章 争议解决第1项",
          "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
          ],
          "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        },
        {
          "clause_id": "C0025",
          "location": "第四章 争议解决第2项",
          "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
          ],
          "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        },
        {
          "clause_id": "C0026",
          "location": "第四章 争议解决第3项",
          "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
          ],
          "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        },
        {
          "clause_id": "C0027",
          "location": "第四章 争议解决第4项",
          "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
          ],
          "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第五章 其他条款",
          "title": "第五章 其他条款",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款"
          ],
          "text": "第五章 其他条款"
        },
        {
          "clause_id": "C0029",
          "location": "第五章 其他条款第1项",
          "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
          ],
          "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        },
        {
          "clause_id": "C0030",
          "location": "第五章 其他条款第2项",
          "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
          ],
          "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
        }
      ],
      "top_k_candidates": [
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。",
          "score": 1.0,
          "accepted": true,
          "reject_reason": "ACCEPTED: 候选文本满足语义模式、必备事实组和排除过滤。",
          "matched_semantic_patterns": [
            "保密(?:义务)?期限.{0,25}(?:年|月|公开)|保密义务.{0,30}至.{0,30}公开"
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
          "text": "保密协议",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "为此，经友好协商，双方就如下条款达成协议。",
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
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义",
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
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
      "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
      "result": "FOUND",
      "supporting_evidence": [
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。",
          "quote": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。",
          "original_excerpt": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "source_start": 0,
          "source_end": 44,
          "supports_element_ids": [
            "employment_secret_duty_2"
          ],
          "source_type": "CONTRACT_TEXT"
        }
      ]
    },
    {
      "element_id": "employment_secret_duty_3",
      "review_id": "NDA-02-01",
      "search_targets": [
        "资料返还或销毁安排"
      ],
      "query_patterns": [
        "(?:终止|离职|要求).{0,45}(?:返还|销毁).{0,20}(?:资料|保密信息)"
      ],
      "query_semantic_target": "资料返还或销毁安排",
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
        "C0030"
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
          "text": "保密协议"
        },
        {
          "clause_id": "C0002",
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
        },
        {
          "clause_id": "C0003",
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义"
        },
        {
          "clause_id": "C0004",
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
        },
        {
          "clause_id": "C0005",
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
        },
        {
          "clause_id": "C0006",
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
        },
        {
          "clause_id": "C0007",
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
        },
        {
          "clause_id": "C0008",
          "location": "第一章 定义 / 保密信息不包括：",
          "title": "保密信息不包括：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "保密信息不包括："
          ],
          "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
        },
        {
          "clause_id": "C0009",
          "location": "第二章 双方义务",
          "title": "第二章 双方义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务"
          ],
          "text": "第二章 双方义务"
        },
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        },
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        },
        {
          "clause_id": "C0012",
          "location": "第二章 双方义务第3项",
          "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
          ],
          "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        },
        {
          "clause_id": "C0013",
          "location": "第二章 双方义务第4项",
          "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
          ],
          "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        },
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        },
        {
          "clause_id": "C0015",
          "location": "第二章 双方义务第6项",
          "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
          ],
          "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        },
        {
          "clause_id": "C0016",
          "location": "第二章 双方义务第7项",
          "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
          ],
          "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        },
        {
          "clause_id": "C0017",
          "location": "第二章 双方义务第8项",
          "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
          ],
          "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        },
        {
          "clause_id": "C0018",
          "location": "第二章 双方义务第9项",
          "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
          ],
          "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        },
        {
          "clause_id": "C0019",
          "location": "第三章 违约责任",
          "title": "第三章 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任"
          ],
          "text": "第三章 违约责任"
        },
        {
          "clause_id": "C0020",
          "location": "第三章 违约责任第1项",
          "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
          ],
          "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
        },
        {
          "clause_id": "C0021",
          "location": "第三章 违约责任第2项",
          "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
          ],
          "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        },
        {
          "clause_id": "C0022",
          "location": "第三章 违约责任第3项",
          "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
          ],
          "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        },
        {
          "clause_id": "C0023",
          "location": "第四章 争议解决",
          "title": "第四章 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决"
          ],
          "text": "第四章 争议解决"
        },
        {
          "clause_id": "C0024",
          "location": "第四章 争议解决第1项",
          "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
          ],
          "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        },
        {
          "clause_id": "C0025",
          "location": "第四章 争议解决第2项",
          "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
          ],
          "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        },
        {
          "clause_id": "C0026",
          "location": "第四章 争议解决第3项",
          "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
          ],
          "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        },
        {
          "clause_id": "C0027",
          "location": "第四章 争议解决第4项",
          "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
          ],
          "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第五章 其他条款",
          "title": "第五章 其他条款",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款"
          ],
          "text": "第五章 其他条款"
        },
        {
          "clause_id": "C0029",
          "location": "第五章 其他条款第1项",
          "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
          ],
          "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        },
        {
          "clause_id": "C0030",
          "location": "第五章 其他条款第2项",
          "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
          ],
          "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
          "text": "保密协议",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "为此，经友好协商，双方就如下条款达成协议。",
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
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义",
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
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
      "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
  "evidence_clauses": [
    {
      "clause_id": "C0011",
      "location": "第二章 双方义务第2项",
      "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
      "text": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。",
      "quote": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。",
      "original_excerpt": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二章 双方义务",
        "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
      ],
      "source_start": 1225,
      "source_end": 1261,
      "supports_element_ids": [
        "employment_secret_duty_1"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二章 双方义务第2项",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。",
      "source_span": {
        "start_offset": 1225,
        "end_offset": 1261,
        "raw_text": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0011",
        "section": "第二章 双方义务第2项",
        "sentence_index": 1,
        "quote": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_secret_duty_1"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "NDA-02-01",
      "element_ids": [
        "employment_secret_duty_1"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "限制使用披露及接触人员"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    },
    {
      "clause_id": "C0014",
      "location": "第二章 双方义务第5项",
      "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
      "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。",
      "quote": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。",
      "original_excerpt": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。",
      "section_type": "正式合同条款",
      "heading_path": [
        "第二章 双方义务",
        "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
      ],
      "source_start": 1427,
      "source_end": 1471,
      "supports_element_ids": [
        "employment_secret_duty_2"
      ],
      "source_type": "CONTRACT_TEXT",
      "document_id": "contract_package/main",
      "document_type": "MAIN_CONTRACT",
      "source_document_type": "MAIN_CONTRACT",
      "evidence_block_type": "OPERATIVE_CLAUSE",
      "document_name": "合同正文",
      "section": "第二章 双方义务第5项",
      "sentence_index": 1,
      "confidence": "high",
      "evidence_type": "CONTRACT_TEXT",
      "raw_text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。",
      "source_span": {
        "start_offset": 1427,
        "end_offset": 1471,
        "raw_text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
      },
      "source_document": "contract_package/main",
      "original_document_reference": "contract_package/main",
      "derived_or_original": "ORIGINAL",
      "evidence_source": {
        "document_id": "contract_package/main",
        "document_type": "MAIN_CONTRACT",
        "document_name": "合同正文",
        "clause_id": "C0014",
        "section": "第二章 双方义务第5项",
        "sentence_index": 1,
        "quote": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。",
        "confidence": "high",
        "evidence_block_type": "OPERATIVE_CLAUSE",
        "evidence_type": "CONTRACT_TEXT",
        "source_span": {
          "start_offset": -1,
          "end_offset": -1,
          "raw_text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        },
        "derived_or_original": "ORIGINAL"
      },
      "evidence_polarity": "SUPPORTS_PARTIAL",
      "entailment_status": "SUPPORTS",
      "supporting_element_ids": [
        "employment_secret_duty_2"
      ],
      "canonical_fact_keys": [],
      "relevance_score": 1.0,
      "selection_reason": "Existing evidence directly supports resolved ReviewElementTruth.",
      "review_id": "NDA-02-01",
      "element_ids": [
        "employment_secret_duty_2"
      ],
      "support_type": "DIRECT",
      "provenance_validation": {
        "status": "PASS",
        "evidence_type": "CONTRACT_TEXT",
        "errors": []
      },
      "supported_propositions": [
        "保密期限或信息公开后的终止条件"
      ],
      "support_summary": "证明合同已约定相关合同要素。"
    }
  ],
  "termination_classification": []
}
```

## NDA-04-01

```json
{
  "rule_id": "NDA-04-01",
  "applicability": {
    "review_id": "NDA-04-01",
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
  "actual_status": "缺失",
  "reason": "未找到明确约定：保密违反的停止侵害或损失赔偿。",
  "coverage_elements": [
    {
      "review_id": "NDA-04-01",
      "element_id": "confidentiality_remedies_1",
      "proposition": "保密违反的停止侵害或损失赔偿",
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
      "element_id": "confidentiality_remedies_1",
      "review_id": "NDA-04-01",
      "search_targets": [
        "保密违反的停止侵害或损失赔偿"
      ],
      "query_patterns": [
        "(?:违反保密义务|泄露保密信息|泄露商业秘密).{0,65}(?:赔偿|停止侵害|消除影响)"
      ],
      "query_semantic_target": "保密违反的停止侵害或损失赔偿",
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
        "C0030"
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
          "text": "保密协议"
        },
        {
          "clause_id": "C0002",
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。为此，经友好协商，双方就如下条款达成协议。"
        },
        {
          "clause_id": "C0003",
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义"
        },
        {
          "clause_id": "C0004",
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。"
        },
        {
          "clause_id": "C0005",
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。"
        },
        {
          "clause_id": "C0006",
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。"
        },
        {
          "clause_id": "C0007",
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。"
        },
        {
          "clause_id": "C0008",
          "location": "第一章 定义 / 保密信息不包括：",
          "title": "保密信息不包括：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "保密信息不包括："
          ],
          "text": "保密信息不包括：\n1）在披露方披露时，该保密信息已合法公开；\n2）非因违反保密义务的行为，保密信息已经或正在被公开的；\n3）在披露方披露信息之前接受方就拥有此项保密信息的；\n4）接受方从第三方获取的保密信息，而第三方不受保密义务的约束；\n5）由接受方独立开发的保密信息；\n6）按照政府机关、有管辖权的法庭或法律的要求披露的保密信息，前提是接受方应尽可能的缩小披露的范围并协助披露方在披露前采取相应保护措施。"
        },
        {
          "clause_id": "C0009",
          "location": "第二章 双方义务",
          "title": "第二章 双方义务",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务"
          ],
          "text": "第二章 双方义务"
        },
        {
          "clause_id": "C0010",
          "location": "第二章 双方义务第1项",
          "title": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
          ],
          "text": "1、双方在本协议的合作过程中，一方（“披露方”）根据本协议按以下方式披露给另一方（“接受方”）的保密信息：以书面形式披露的，应在显著位置标明“机密”或“秘密”或与此类似的标记；以口头形式披露的，披露方在披露信息时应指明该信息的保密性质，且应在该信息口头披露后的十日内以上述书面形式对该保密信息向接受方予以确认。尽管如此，对于未在十日内以书面形式向信息接受方确认其保密性质的口头信息，若依据该信息的类型、性质或其被披露时的环境可以合理的判断出其具备保密性，也应该视为保密信息。"
        },
        {
          "clause_id": "C0011",
          "location": "第二章 双方义务第2项",
          "title": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
          ],
          "text": "2、接受方同意仅将保密信息用于本协议指定的目的。未经披露方书面同意，接受方不得对任何第三方披露、公开或许可使用保密信息。"
        },
        {
          "clause_id": "C0012",
          "location": "第二章 双方义务第3项",
          "title": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
          ],
          "text": "3、接受方仅可为履行本协议之目的向出于工作需要、必须知晓的人员披露保密信息，并且接受方应保证前述人员应接受至少与本协议同等严格的保密条款的约束。"
        },
        {
          "clause_id": "C0013",
          "location": "第二章 双方义务第4项",
          "title": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
          ],
          "text": "4、接受方应采取一切合理且不低于接受方对其类似的保密信息所采取的措施来保守披露方披露的保密信息，防止保密信息被盗窃或（和）泄漏、未经授权的使用、因任何第三方的疏忽导致保密信息的泄漏。"
        },
        {
          "clause_id": "C0014",
          "location": "第二章 双方义务第5项",
          "title": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
          ],
          "text": "5、在合作过程中发生的保密信息，其保密期限为：从合作开始时起至合作终止时间之后三年为止。"
        },
        {
          "clause_id": "C0015",
          "location": "第二章 双方义务第6项",
          "title": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
          ],
          "text": "6、接受方对其关联机构的信息透露均应遵从本协议的保密规定，并且仅限于技术文档或服从于本协议条款和规定的其余技术信息；接受方应保证关联机构严格遵守本条下的保密规定，且这些关联机构对本协议下保密义务的任何违反应由接受方承担全部责任。"
        },
        {
          "clause_id": "C0016",
          "location": "第二章 双方义务第7项",
          "title": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
          ],
          "text": "7、如果接受方根据国家有关法律或行政机关依法做出的有效强制性命令或要求必须对有关保密信息进行披露的，应提前书面通知披露方，说明其拟根据该命令或要求披露有关保密信息的形式和范围，以使披露方能采取相应保护措施和/或同意在该种情形下披露有关保密信息时，应尽量将保密信息的披露控制在法律允许的最小范围之内并采取有力措施使该披露的影响降低到最低程度。"
        },
        {
          "clause_id": "C0017",
          "location": "第二章 双方义务第8项",
          "title": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
          ],
          "text": "8、双方当事人关于本合作的新闻发布会或任何其他形式的对外宣传，应事先征得对方书面同意或由双方统一规划组织。"
        },
        {
          "clause_id": "C0018",
          "location": "第二章 双方义务第9项",
          "title": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第二章 双方义务",
            "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
          ],
          "text": "9、接受方承认并同意，如其违反本协议规定的保密义务给披露方及/或关联公司造成难以弥补的严重损失，披露方将有权采取包括法律和行政手段在内的一切必要救济来维护其合法权益。"
        },
        {
          "clause_id": "C0019",
          "location": "第三章 违约责任",
          "title": "第三章 违约责任",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任"
          ],
          "text": "第三章 违约责任"
        },
        {
          "clause_id": "C0020",
          "location": "第三章 违约责任第1项",
          "title": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金："
          ],
          "text": "1、接受方同意在其有任一下述违约情况下，除应赔偿披露方因此遭受的一切损害、损失以及披露方因寻求相关救济而支出的全部费用（包括但不限于律师费及执行该赔偿的费用）外，还应支付所应投资额的20%作为违约金：\n1）接受方未经许可，为主合同约定以外的其他目的和范围使用保密信息；\n2）接受方未经披露方同意向第三方披露或/和让第三方使用保密信息；\n3）接受方有其他违反本协议保密义务的行为。"
        },
        {
          "clause_id": "C0021",
          "location": "第三章 违约责任第2项",
          "title": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
          ],
          "text": "2、以金钱补偿不足以补救由于违反本协议规定给技术提供方造成的损害，接受方同意，披露方将有权采取法律所允许的其他补救措施。"
        },
        {
          "clause_id": "C0022",
          "location": "第三章 违约责任第3项",
          "title": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第三章 违约责任",
            "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
          ],
          "text": "3、因披露方自身原因导致保密信息泄露的，接受方不承担任何责任。"
        },
        {
          "clause_id": "C0023",
          "location": "第四章 争议解决",
          "title": "第四章 争议解决",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决"
          ],
          "text": "第四章 争议解决"
        },
        {
          "clause_id": "C0024",
          "location": "第四章 争议解决第1项",
          "title": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
          ],
          "text": "1、双方如在解释或履行本协议发生争议时，应本着互相信赖、平等互利的精神进行协商，求得解决。"
        },
        {
          "clause_id": "C0025",
          "location": "第四章 争议解决第2项",
          "title": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
          ],
          "text": "2、双方若不能达成谅解，可以申请仲裁解决。仲裁在中国国际经济贸易仲裁委员会进行，由该会按《中国国际经济贸易仲裁委员会仲裁规则》进行裁决。"
        },
        {
          "clause_id": "C0026",
          "location": "第四章 争议解决第3项",
          "title": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
          ],
          "text": "3、费用由败诉方承担；仲裁机构的裁决是终局的，对各方均有约束力。"
        },
        {
          "clause_id": "C0027",
          "location": "第四章 争议解决第4项",
          "title": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第四章 争议解决",
            "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
          ],
          "text": "4、除了在仲裁过程中进行仲裁的那部分外，合同的其余部分在仲裁期间仍应继续执行。"
        },
        {
          "clause_id": "C0028",
          "location": "第五章 其他条款",
          "title": "第五章 其他条款",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款"
          ],
          "text": "第五章 其他条款"
        },
        {
          "clause_id": "C0029",
          "location": "第五章 其他条款第1项",
          "title": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
          ],
          "text": "1、本协议的订立、履行和解释均适用于中华人民共和国法律，双方的合作必须在中华人民共和国的法律、法规及其他规范性文件规定的范围内开展。"
        },
        {
          "clause_id": "C0030",
          "location": "第五章 其他条款第2项",
          "title": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。",
          "section_type": "正式合同条款",
          "heading_path": [
            "第五章 其他条款",
            "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。"
          ],
          "text": "2、本协议一式四份，各执二份。本协议经双方签署后以最后一方签署日为生效日。\n甲方：北京邮电大学（盖章）\n签字代表：张明远（签字）\n签字日期：2026年9月8日\n乙方：北京智衡数据科技有限公司（盖章）\n签字代表：李晨宇（签字）\n签字日期：2026年9月8日"
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
          "text": "保密协议",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "本保密协议（以下简称“本协议”）由以下双方签署：\n甲方：北京邮电大学\n地址：北京市海淀区西土城路10号\n联系人：张明远\n联系方式：010-62280001\n乙方：北京智衡数据科技有限公司\n地址：北京市海淀区中关村东路18号启迪科技大厦A座1208室\n联系人：李晨宇\n联系方式：010-82561236\n考虑到（1）双方拟从事协议项下活动，（2）双方在合作过程中可能向对方披露保密信息，并希望对方对所披露的信息进行保密。",
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
          "location": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "title": "本保密协议（以下简称“本协议”）由以下双方签署：",
          "section_type": "正式合同条款",
          "heading_path": [
            "本保密协议（以下简称“本协议”）由以下双方签署："
          ],
          "text": "为此，经友好协商，双方就如下条款达成协议。",
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
          "location": "第一章 定义",
          "title": "第一章 定义",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义"
          ],
          "text": "第一章 定义",
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
          "location": "第一章 定义 / 1、协议项下活动：",
          "title": "1、协议项下活动：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "1、协议项下活动："
          ],
          "text": "1、协议项下活动：\n指北京邮电大学与北京智衡数据科技有限公司合作进行面向工业知识图谱的多模态智能检索关键技术研究活动，如无特别规定，协议项下活动是指双方为工业知识图谱构建、多模态信息处理及智能检索算法研究建立技术合作、服务或其他业务关系，以及为执行那些已经建立的此类合作关系而进行的全部活动。",
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
          "location": "第一章 定义 / 2、信息披露方与接受方：",
          "title": "2、信息披露方与接受方：",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "2、信息披露方与接受方："
          ],
          "text": "2、信息披露方与接受方：\n信息披露方是指为本次合作提供先期技术支持及技术许可等信息的签约方；信息接受方是指在本次合作中相对于信息披露方的签约方。",
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
          "location": "第一章 定义第3项",
          "title": "3、关联机构",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "3、关联机构"
          ],
          "text": "3、关联机构\n是指与本协议签约方有如下关系的公司或者自然人，合伙企业或者其他商业机构：在资金、经营、购销等方面，存在直接或者间接的拥有或者控制关系；直接或者间接地同为第三者所拥有或者控制；在利益上具有相关联的其他关系。",
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
          "location": "第一章 定义第4项",
          "title": "4、保密信息",
          "section_type": "正式合同条款",
          "heading_path": [
            "第一章 定义",
            "4、保密信息"
          ],
          "text": "4、保密信息\n指在本协议签署日之前或之后由一方向另一方披露（以书面、口头或以其他方式，直接或间接地）的属商业、技术或专有性质的所有信息，包括但不限于关于或包含在软件内的信息，及关于专业技术、商业秘密、制造、营销或业务计划或财务或人事、现有或未来产品、销售、供应、客户、雇员、投资者或业务经营的任何信息，其中包括但不限于每一方的合作投入和本协议及其内容。",
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
      "searched_document_hash": "fb268d84e8c23297527b07f7eb1083a7d42a50d3c16a939da6322522a55ab504",
      "result": "NOT_FOUND",
      "supporting_evidence": []
    }
  ],
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
      "C0030"
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
      "C0030"
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
    "contract_type": "confidentiality",
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