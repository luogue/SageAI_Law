import json
from pathlib import Path
from docx import Document
from review_v2.technology_service_analysis import classify_technology_transaction
from review_v2.clause_parser import parse_contract_clauses
from review_v2.domain_selection import resolve_domain_selection

root=Path(__file__).resolve().parents[1]
path=root/'artifacts/technology_pass_semantics/round43_consulting_classification/input.docx'
text='\n'.join(p.text for p in Document(path).paragraphs if p.text.strip())
(path.parent/'input/original.txt').write_text(text,encoding='utf8')
classification=classify_technology_transaction(text)
clauses=parse_contract_clauses(text)
resolution,domain,routed=resolve_domain_selection('technology',text,clauses,classification)
payload={'classification':classification,'resolution':resolution.to_public_dict(),'routed':routed}
(path.parent/'diagnosis_before.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({
 'primary_subtype':classification.get('primary_subtype'),
 'confidence':classification.get('confidence'),
 'classification_score':classification.get('classification_score'),
 'candidate_scores':classification.get('candidate_scores'),
 'evidence':classification.get('classification_evidence'),
 'document_family':resolution.document_domain.get('family'),
 'document_subtype':resolution.document_domain.get('primary_subtype'),
 'selection':resolution.selected_contract_type,
 'resolution':resolution.resolution,
 'compatibility':resolution.compatibility,
 'family_scores':resolution.classification_context.get('candidate_scores'),
},ensure_ascii=False))
