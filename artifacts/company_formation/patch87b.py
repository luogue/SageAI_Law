from pathlib import Path
p=Path('backend/review_v2/employment_facts.py');s=p.read_text(encoding='utf-8');old="""        if any(f['fact_type']=='shareholder_transfer_exit' for f in facts) and not any(f['fact_type']=='company_capital_return' for f in facts):
            return [r for r in requirements if r['element_id']!='formation_transfer_exit_3'], []""";new="""        text = '\\n'.join(c.text for c in clauses)
        requirements = list(requirements)
        if not re.search(r'退股|退出|回购', text):
            requirements = [r for r in requirements if r['element_id']!='formation_transfer_exit_2']
        company_return = any(f['fact_type']=='company_capital_return' for f in facts)
        private_exit = any(f['fact_type']=='shareholder_transfer_exit' for f in facts)
        ambiguous_return = re.search(r'(?:返还|退还|退回)[^。]{0,30}(?:投资|出资)|(?:投资|出资)[^。]{0,30}(?:返还|退还|退回)',text)
        if not company_return and (private_exit or not ambiguous_return):
            requirements = [r for r in requirements if r['element_id']!='formation_transfer_exit_3']
        from review_v2.formation_rule_semantics import transfer_assessment
        if transfer_assessment(text)['charter_special_arrangement']:
            requirements.append(dict(element_id='formation_transfer_charter_verification',proposition='章程特殊转让安排的依据与合法性核验',semantic_patterns=(),requirement_kind='EXTERNAL_VERIFICATION',
                verification_instruction='合同声明存在章程特别转让安排，核验有效章程原件、适用条款及合法性；不直接认定旧式同意机制无效。',risk_relevant=False))
        return requirements, []""";assert old in s;s=s.replace(old,new);p.write_text(s,encoding='utf-8')
p=Path('backend/review_v2/formation_rule_semantics.py');s=p.read_text(encoding='utf-8').replace('成[立立]之?日起?','成立(?:之日)?起?');s=s.replace('from datetime import date','from datetime import date\nfrom calendar import monthrange');s=s.replace('min(lo.day,28)','min(lo.day,monthrange(lo.year+5,lo.month)[1])').replace('min(hi.day,28)','min(hi.day,monthrange(hi.year+5,hi.month)[1])');p.write_text(s,encoding='utf-8')
p=Path('backend/review_v2/company_formation_checklist.py');s=p.read_text(encoding='utf-8');s += "\nPROFILES['formation_fund_safety'][1]['semantic_patterns'] += (r'双人审批|双人签署|两人审批',)\n";p.write_text(s,encoding='utf-8')
