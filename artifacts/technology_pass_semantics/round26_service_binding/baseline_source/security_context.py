"""Security-specific context, without promoting contract declarations to external facts."""
import re
from copy import deepcopy

def corporate_context(text):
 owner=re.search(r'(?:出质人|抵押人|保证人|担保人)[）)]?\s*[：:]\s*([^\n，。；]+)',text)
 debtor=re.search(r'(?:主合同债务人|债务人|借款人)[：:]\s*([^\n，。；]+)',text)
 own=bool(re.search(r'为(?:其)?(?:自身|自己|本公司)债务提供担保',text)) or bool(owner and debtor and owner[1].strip()==debtor[1].strip())
 exception=bool(re.search(r'非上市公司[^。；]{0,35}为其全资子公司[^。；]{0,25}经营活动[^。；]{0,15}担保',text))
 return {'own_debt':own,'exception_claimed':exception,'guarantor':owner[1] if owner else '', 'debtor':debtor[1] if debtor else ''}

def resolve(node, requirements, text):
 rows=deepcopy(requirements)
 from review_v2.security_semantic_aliases import extend
 rows=extend(node,rows,text)
 if node=='security_prior_encumbrances':
  instruction=('交付质物前核验现占有人及占有状态、是否已交付他人并设有在先质权、查封扣押及其他权利负担；必要时结合可查询的公示资料核验。'
   if re.search(r'动产质押|质物',text) and not re.search(r'股权质押|应收账款质押',text)
   else '办理对应权利质押登记或凭证交付前，按权利类别核验专项登记、公示资料、在先权利及顺位。'
   if re.search(r'股权质押|应收账款质押|权利质押',text)
   else '办理抵押登记前，按财产类别核验不动产登记或动产和权利担保统一登记资料中的在先抵押、查封及受偿顺位。')
  for row in rows:
   if row.get('requirement_kind')=='EXTERNAL_VERIFICATION':row['verification_instruction']=instruction
 if node=='security_company_authority' and corporate_context(text)['exception_claimed']:
  # An exception claim requires external verification; it is not automatic validity.
  for row in rows[:2]:
   row.update(requirement_kind='EXTERNAL_VERIFICATION',verification_priority='MEDIUM',
    verification_instruction='核验所主张无需机关决议例外的真实适用条件、公司上市状态及授权事实。')
 return rows
