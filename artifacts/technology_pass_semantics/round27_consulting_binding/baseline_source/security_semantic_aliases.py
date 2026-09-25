"""Role-bound security predicates shared by mortgage and pledge reviews."""
import re

def extend(node,rows,text):
 match=re.search(r'(甲方|乙方|丙方)[（(](?:出质人|抵押人|担保人)[）)]',text)
 if not match: match=re.search(r'(?:出质人|抵押人|担保人)[（(](?:以下简称)?(甲方|乙方|丙方)[）)]',text)
 actor='(?:出质人|抵押人|担保人'+('|' + match[1] if match else '')+')'
 gap=r'[^。；\n]{0,110}'
 def add(index,*patterns):rows[index]['semantic_patterns']=list(rows[index]['semantic_patterns'])+list(patterns)
 if node=='security_main_debt':
  add(0,r'(?:借款抵押合同|借款质押合同|借款及担保合同)[^。]{0,60}借款人(?:（[^）]*）)?[：:][^\n，。；_]{2,60}')
  add(0,r'(?:双方|甲方与乙方|乙方与甲方)[^。；]{0,35}(?:签订|签署)[^。；]{0,25}《[^》]+合同》',r'其与(?:甲方|乙方)签署的《[^》]+合同》')
  add(1,r'(?:为保障|为担保)[^。；]{0,55}(?:甲方|乙方)(?:义务|履行)[^。；]{0,35}(?:履行|义务)')
  add(2,r'(?:剩余|尚欠|未付|尚未支付)?(?:股权转让|货款|转让)?价款(?:为|：|:)?(?:人民币|港币)?[0-9][0-9,，]*(?:\.\d+)?元')
 if node=='security_scope':
  predicates=[r'(?:合同》项下|前述)(?:尚未支付的)?[^。；]{0,20}(?:价款|本金|借款)',r'(?:前述|上述|被担保)(?:债务|债权)[^。；]{0,30}利息',r'为实现债权[^。；]{0,35}(?:费用|律师费)']
  for row,p in zip(rows,predicates):
   row['contextual_patterns']=list(row.get('contextual_patterns',[]))+[{'context':r'被担保|担保范围|主债权','predicate':p}]
 if node=='security_title_authority':
  rows[0]['excluded_patterns']=list(rows[0].get('excluded_patterns',[]))+[r'(?:不|未|并非)合法持有']
  rows[1]['excluded_patterns']=list(rows[1].get('excluded_patterns',[]))+[r'(?:不具有|不享有|没有)[^。；]{0,25}(?:权利|权限|能力)']
  add(0,r'(?:抵押人|出质人|担保人)[^。；]{0,25}(?:拥有|享有)所有权')
  add(2,r'共有[^。；]{0,20}共有人同意[^。；]{0,30}(?:抵押|质押)')
  add(0,actor+r'[^。；]{0,20}(?:以其|将其|对其)?(?:享有|持有|拥有)的?应收账款')
  rows[0]['excluded_patterns'] += [r'(?:不享有|未取得|不拥有)[^。；]{0,20}应收账款']
  add(0,actor+gap+r'合法持有[^。；]{0,40}股权')
  add(1,actor+gap+r'(?:具有|享有)[^。；]{0,25}(?:权利|权限|能力)[^。；]{0,25}将该股权[^。；]{0,25}质押')
  # A holder of company equity is not necessarily a co-owner of that equity.
  # With no asserted co-ownership, verify title externally instead of demanding a denial.
  if re.search(r'股权(?:质押|出质)',text) and not re.search(r'股权[^。；]{0,20}(?:共有|共同所有)',text):
   rows[2].update(requirement_kind='EXTERNAL_VERIFICATION',verification_priority='MEDIUM',verification_instruction='核验股东名册、股权登记及是否存在代持或共有；未约定不存在共有不作为股权质押合同缺失。')
 if node=='security_prior_encumbrances':
  add(0,r'(?:不存在|未[^。；]{0,20}设置)[^。；]{0,35}(?:其他质押|其他担保|权利负担)')
 if node=='security_realization':
  add(0,r'(?:出现|发生)[^。；]{0,25}违约[^。；]{0,35}(?:依法可以实现质权|依法实现质权)',r'(?:违约|未履行)[^。；]{0,45}(?:有权|可以)[^。；]{0,20}实现质权')
 if node=='security_exercise_period':
  add(1,r'(?:主债权|全部债权|被担保债权)[^。；]{0,30}(?:全部|完全)[^。；]{0,10}(?:获得)?清偿后[^。；]{0,120}(?:解除[^。；]{0,15}质押|出质注销登记)',r'(?:全部债权|债务)[^。；]{0,15}清偿后[^。；]{0,60}注销')
 if node=='pledge_equity_asset':
  add(0,actor+gap+r'(?:持有|将其)[^。；]{0,45}(?:目标公司|有限公司)[^。；]{0,8}\d+(?:\.\d+)?%的?股权')
 if node=='pledge_equity_registration':
  rows[0]['excluded_patterns']=[r'(?:无需|无须|不负责|不得)[^。；]{0,30}(?:办理|完成)股权(?:质押|出质)登记']
  add(0,actor+r'[^。；]{0,150}(?:应|负责)[^。；]{0,120}(?:办理|完成)股权(?:质押|出质)登记')
 return rows
