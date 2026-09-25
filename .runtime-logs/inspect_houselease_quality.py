from review_v2.engine import review_contract_v2
text=("上海市房屋租赁合同。签订日期：2024年1月1日。"
"根据《中华人民共和国合同法》及有关规定，双方订立本合同。"
"第一条 房屋坐落于上海市浦东新区，产证编号沪房地浦字第123号。"
"第五条 月租金为3852元，支付方式为银行转账，【每月5日前】☑【________】。"
"第九条 乙方逾期不支付租金累计超过1个月的，甲方有权解除合同。"
"第十条 乙方中途擅自退租的，应按提前退租天数的租金的2倍支付违约金。"
"第十一条 双方协商不成的，向浦东新区人民法院起诉。")
output=review_contract_v2(text,'house_lease',use_llm=False)
print(output['release_quality_gate']['status'])
print(output['release_quality_gate'].get('failures'))
print(output.get('default_law_provenance_gate'))
print(output.get('report_text_validation_gate'))
print(output.get('technical_quality_gate'))
PY
