"""Shared extraction dependencies. No text matching or synthesized absence facts."""
from review_v2.fact_validation import FactExtractionError

ROOTS = ('non_compete.arrangement', 'contract.employment_form')
NC_CONTEXT = {'non_compete.arrangement', 'non_compete.secret_access',
              'non_compete.access_capability', 'non_compete.actual_access'}

def dependencies(concepts):
 return {c: {'concept':'contract.employment_form','required_value':'DISPATCH'} if c.startswith('dispatch.')
         else {'concept':'non_compete.arrangement','required_value':'EXISTS'}
         for c in concepts if c.startswith('dispatch.') or (c.startswith('non_compete.') and c not in NC_CONTEXT)}

def validate(facts, concepts):
 rows = [{'concept':f['concept'],'value':f.get('normalized_value',f.get('value'))} for f in facts]
 for row in rows:
  dep=dependencies(concepts).get(row['concept'])
  if dep and not any(r['concept']==dep['concept'] and r['value']==dep['required_value'] for r in rows):
   raise FactExtractionError('UNSATISFIED_FACT_DEPENDENCY',failed_stage='EXTRACTION_APPLICABILITY',
       field=row['concept'],model_raw_value=row,expected=dep,actual='no current parent fact',repairable=True)

INSTRUCTIONS = """先全文确定事实是否存在和当前模块关系，再抽具体值。required_fact_dependencies是统一依赖：
仅明确当前父事实满足required_value才提取子事实；没有当前义务、明确不设、未来另签均不得填写该模块参数。allowed_fact_concepts是唯一可输出value的字段清单；inactive_concepts只全文核验不存在当前适用事实，不在facts/additional_facts生成对象。若全文与父事实矛盾必须标unresolved或拒绝父事实，不能私自绕过字段依赖。
保密接触能力是独立背景，不能证明离职竞业义务；普通岗位不能证明派遣关系。
父义务是否已设定与子参数是否完整独立判断：已施加竞争从业约束，即便范围、期限、补偿留待以后确定，父事实仍为EXISTS。只省略未确定的子参数并记录ABSENT或真实UNCERTAIN，不得因此将父事实改为DEFERRED。DEFERRED仅限义务本身尚待另行决定。
所有concept仍必须全文检索：无事实则只列searched_concepts并省略fact；真有歧义才列unresolved_concepts。
不能用未约定、无、另行约定、不适用填入任何强类型value，也不能先生成非法字符串再强转null。
number必须真实数值；money必须真实amount_text及单位；formula必须真实计算关系；salary_base必须真实基数类型及金额。
NONE/DEFERRED/EXPLICIT_NONE仅可用于schema明确允许这些枚举的父安排字段，绝非任何子字段的通用占位值。
明确否定用schema定义的否定事实；全文未找到保留搜索元数据，不生成默认值或事实。"""


def eligible(concepts, facts):
 required=dependencies(concepts)
 return [c for c in concepts if c not in required or any(
     f['concept']==required[c]['concept'] and f.get('normalized_value',f.get('value'))==required[c]['required_value'] for f in facts)]
