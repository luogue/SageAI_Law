from dataclasses import replace
import pytest
from review_v2.shared_fact_concepts import pool, requirements, register
from review_v2.clause_parser import parse_contract_clauses
from review_v2.penalty_base import analyze

@pytest.mark.parametrize('concept,text',[
 ('accepted_handover','货物移交承运方，经其验收视为交付完成。'),
 ('accepted_handover','接收方接收货物。'),
 ('custody_duty','受托方应当妥善保管物品。'),
 ('custody_negligence_compensation','因保管不善造成货物灭失，受托方应承担赔偿责任。'),
 ('custody_negligence_compensation','未尽妥善保管义务造成设备损坏，应承担赔偿责任。'),
 ('handover_receipt','接收方应出具双方签字的交接单。'),
 ('handover_receipt','交付完成后出具《保管凭证》。'),
 ('incidental_service_fees','第四条 附加服务费\n附加装卸费；计算方式为一次性收取；总额800元。'),
 ('attachment_effect','附件与本合同具有同等效力。'),
 ('document_precedence','正文与附件不一致时，以正文为准。'),
])
def test_normalized_facts(concept,text):
 assert pool(parse_contract_clauses(text),[concept])[concept]

@pytest.mark.parametrize('concept,text',[
 ('handover_receipt','通过电子邮箱发送通知，以邮件签收视为送达。'),
 ('document_precedence','附件与合同具有同等效力。'),
 ('custody_negligence_compensation','保管不善造成毁损，不承担赔偿责任。'),
 ('accepted_handover','寄存人自己管理物品，仅租用场地。'),
])
def test_related_word_is_not_support(concept,text):
 assert not pool(parse_contract_clauses(text),[concept])[concept]

@pytest.mark.parametrize('text,expected',[
 ('服务费按每月人民币3500元计算。逾期按当月服务费的2%支付违约金。','DETERMINABLE'),
 ('保管费每月人民币2000元。按当月保管费的1%支付违约金。','DETERMINABLE'),
 ('逾期按应付未付金额的0.1%支付违约金。','DETERMINABLE'),
 ('按当月服务费的2%支付违约金。','UNDEFINED'),
 ('服务费每月2000元。服务费每月3000元。按当月服务费的1%支付违约金。','UNDEFINED'),
])
def test_cross_clause_numeric_reference(text,expected):
 assert analyze(text)[0]['status']==expected

def test_shared_pool_consumed_by_two_different_rules():
 from review_v2.safekeeping_contract_checklist import SAFEKEEPING_REVIEW_CHECKLIST
 from review_v2.priority_contract_review import judge
 base=next(c for c in SAFEKEEPING_REVIEW_CHECKLIST if c.fact_concepts==('handover_receipt',))
 clauses=parse_contract_clauses('接收方出具双方签字的交接单。')
 facts=pool(clauses,base.fact_concepts)
 other=replace(base,item_id='OTHER-RECEIPT',node_id='other_delivery_receipt')
 register(other.node_id,other.fact_concepts)
 a=judge(base,clauses,shared_facts=facts);b=judge(other,clauses,shared_facts=facts)
 assert a.coverage_status==b.coverage_status=='通过'
 assert a.evidence_clauses==b.evidence_clauses
 assert facts==pool(clauses,base.fact_concepts)

@pytest.mark.parametrize('text,status',[
 ('附件与本合同具有同等效力。','部分覆盖'),
 ('附件与本合同具有同等效力。正文与附件不一致时以正文为准。','通过'),
 ('未涉及附件。','缺失'),
])
def test_engine_atom_aggregation(text,status):
 from review_v2.engine import review_contract_v2
 report=review_contract_v2(text,'safekeeping',use_llm=False)
 item=next(i for i in report['items'] if i['node_id']=='safekeeping_attachment_priority')
 assert item['coverage_status']==status
 for e in item['coverage_elements']:
  if e['status']=='COVERED':
   assert e['evidence_ids']
   assert e['proposition'] not in item['risk_point_description']

@pytest.mark.parametrize('text,expected', [('正常保管并按约返还。',False),('双方排除留置权，保管人不得留置物品。',True)])
def test_optional_rule_prerequisite(text,expected):
 from review_v2.engine import _is_checkpoint_applicable
 from review_v2.safekeeping_contract_checklist import SAFEKEEPING_REVIEW_CHECKLIST
 rule=next(c for c in SAFEKEEPING_REVIEW_CHECKLIST if c.optional_trigger_patterns)
 assert _is_checkpoint_applicable(text,rule,'safekeeping')[0]==expected

def test_shared_fact_binding_revalidates_semantics():
 from review_v2.safekeeping_contract_checklist import SAFEKEEPING_REVIEW_CHECKLIST
 from review_v2.priority_contract_review import judge
 rule=next(c for c in SAFEKEEPING_REVIEW_CHECKLIST if c.fact_concepts==('handover_receipt',))
 clauses=parse_contract_clauses('邮件进入邮箱视为送达。')
 forged={'handover_receipt':[dict(clause_id=clauses[0].clause_id,location=clauses[0].location,
     text=clauses[0].text,supports_element_ids=['handover_receipt'])]}
 result=judge(rule,clauses,shared_facts=forged)
 assert result.coverage_status=='缺失'
 assert not result.evidence_clauses

@pytest.mark.parametrize('has_source,status,expected',[
 (True,'MISSING','SHARED_FACT_LOST_IN_FINAL_ELEMENT'),
 (False,'COVERED','FINAL_ELEMENT_WITHOUT_SHARED_FACT'),
])
def test_shared_fact_conflict_blocks_quality_gate(has_source,status,expected):
 from dataclasses import fields, MISSING
 from review_v2.engine import ReviewItemResult
 from review_v2.lease_semantics import consistency_failures
 item=ReviewItemResult(**{f.name: [] if f.name in {'matched_terms','evidence_clauses'} else ''
     for f in fields(ReviewItemResult) if f.default is MISSING and f.default_factory is MISSING})
 item.item_id='GENERIC-CONSUMER'
 item.decision_trace={'shared_concept_facts':{'handover_receipt':[{'clause_id':'C1'}] if has_source else []}}
 item.coverage_elements=[{'element_id':'handover_receipt','status':status}]
 assert any(e['requirement']==expected for e in consistency_failures([item]))
