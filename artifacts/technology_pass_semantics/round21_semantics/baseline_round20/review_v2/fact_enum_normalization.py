"""Lossless scalar-enum adaptation; unknown/ambiguous values remain errors."""
import unicodedata
from review_v2.fact_validation import FactExtractionError

ALIASES = {
 # Version-one candidate spellings only. The verifier must still prove that
 # NONE explicitly negates the arrangement; this never maps absence to a fact.
 'non_compete.arrangement': {'CURRENT':'EXISTS','NONE':'EXPLICIT_NONE'},
 'contract.type':{'OPEN_ENDED':'INDEFINITE','无固定期限':'INDEFINITE','TASK_BASED':'TASK','以完成一定工作任务为期限':'TASK','FIXED_TERM':'FIXED'},
 'contract.term_limit_mode':{'任务完成':'TASK_COMPLETION','PROJECT_COMPLETION':'TASK_COMPLETION','工作任务完成':'TASK_COMPLETION',
   'EMPLOYER_DETERMINES_COMPLETION':'EMPLOYER_DETERMINED_COMPLETION','单位决定任务完成':'EMPLOYER_DETERMINED_COMPLETION',
   '自动到期':'CALENDAR_EXPIRY','无确定终止时间':'NONE'},
}

def enum_value(concept, raw, allowed):
 from review_v2.fact_scalar_normalization import unwrap_scalar
 value=unwrap_scalar(concept,raw,'enum')
 if isinstance(value,str):
  value=unicodedata.normalize('NFKC',value).strip().upper()
  value=ALIASES.get(concept,{}).get(value,value)
 if not isinstance(value,str) or value not in allowed:
  raise FactExtractionError('INVALID_ENUM',failed_stage='NORMALIZATION',field='value',model_raw_value=raw,actual=value,expected=sorted(allowed))
 return value
