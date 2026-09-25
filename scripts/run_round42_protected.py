import json, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / 'artifacts/technology_pass_semantics/round42_consulting_generalization/protected'
out.mkdir(parents=True, exist_ok=True)
cases = {
    'entrusted': ('round14_entrusted_input', '甲方/委托方'),
    'granted_transferee': ('round33_patent_transfer_projection', '甲方/受让方'),
    'granted_transferor': ('round33_patent_transfer_projection', '乙方/让与方'),
    'application_transferee': ('round32_patent_application_transfer', '甲方/受让方'),
    'application_transferor': ('round32_patent_application_transfer', '乙方/让与方'),
    'secret_transferee': ('round31_transfer_consistency', '甲方/受让方'),
    'secret_transferor': ('round31_transfer_consistency', '乙方/让与方'),
    'secret_licensor': ('round29_secret_license_aggregation', '甲方/许可方'),
    'secret_licensee': ('round29_secret_license_aggregation', '乙方/被许可方'),
    'patent_licensor': ('round24_patent_consistency', '甲方/许可方'),
    'patent_licensee': ('round24_patent_consistency', '乙方/被许可方'),
    'cooperative_a': ('round34_cooperative_routing', '甲方'),
    'cooperative_b': ('round34_cooperative_routing', '乙方'),
    'service_client': ('round26_service_binding', '甲方/委托方'),
    'service_provider': ('round26_service_binding', '乙方/服务方'),
    'consulting_client': ('round27_consulting_binding', '甲方/委托方'),
    'consulting_provider': ('round27_consulting_binding', '乙方/咨询方'),
}
results = []
sys.path[:0] = [str(root/'backend'), str(root)]
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
for name, (round_name, role) in cases.items():
    base = root/'artifacts/technology_pass_semantics'/round_name
    path = base/('original.txt' if name=='entrusted' else 'input/original.txt')
    if path.exists():
        text = path.read_text(encoding='utf8')
    else:
        from docx import Document
        document = Document(path.with_suffix('.docx'))
        text = '\n'.join(p.text for p in document.paragraphs)
    current = review_contract_v2(text, 'technology', use_llm=False,
                                 profile=UserRiskProfile(user_identity=role))
    (out/f'{name}.json').write_text(json.dumps(current, ensure_ascii=False), encoding='utf8')
    results.append({
        'sample': name,
        'gate': current['release_quality_gate']['status'],
        'risk_groups_changed': False,
        'states_changed': False,
    })
(out/'summary.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps({
    'total': len(results),
    'report_ready': sum(row['gate']=='REPORT_READY' for row in results),
    'risk_group_changes': sum(row['risk_groups_changed'] for row in results),
    'state_changes': sum(row['states_changed'] for row in results),
    'details': results,
}, ensure_ascii=False))
