from pathlib import Path
import shutil,subprocess,hashlib,json
out=Path('artifacts/technology_pass_semantics/round21_semantics/baseline_round20/review_v2')
out.mkdir(parents=True,exist_ok=True)
for p in Path('backend/review_v2').glob('*.py'):shutil.copy2(p,out/p.name)
p=out/'engine.py';s=p.read_text(encoding='utf-8');s=s.replace(', party_requirement_states, requirement_states',', party_requirement_states').replace('requirement_states(', 'party_requirement_states(').replace('party_party_requirement_states','party_requirement_states')
s=s.replace('"party_coverage", "component_coverage", "component_quantifier",','"party_coverage",')
a=s.index('            from review_v2.secret_loss_sources import bind_elements as bind_loss_elements');b=s.index('            fee_subject =',a);s=s[:a]+s[b:]
s=s.replace('_set_multi_element_state(item, bind_loss_elements([','_set_multi_element_state(item, [',1).replace('            ], loss, clauses), secret_evidence)\n            _register_projected_direct_bindings(item)\n','            ], secret_evidence)\n',1)
s=s.replace('''        from review_v2.license_terms import declared_license_type
        type_clauses = [clause for clause in clauses if declared_license_type(clause.text)]''','''        type_clauses = [
            clause for clause in clauses
            if any(term in _compact(clause.text) for term in ("普通许可", "排他许可", "独占许可", "非独占许可"))
        ]''')
s=s.replace('''            "已覆盖：" + "；".join(_coverage_element_groups(item)[0]) + "；"
            "尚未覆盖：" + "、".join(labels) + "。"''','''            "合同已明确依法公开以及由出让方或有权第三方向公众公开的信息不再承担保密义务；"
            "尚未覆盖：" + "、".join(labels) + "。"''')
s=s.replace('''    if family == "secret_loss_arrangements":
        from review_v2.secret_loss_sources import elements
        return elements(clauses)
''','').replace("            _register_atomic_family_facts(generic_fact_graph, 'secret_loss_arrangements', clauses)\n",'')
a=s.index('    # The primary quotation must be one of the resolved coverage proofs.');b=s.index('    item.evidence_clauses = synchronized',a);s=s[:a]+s[b:];p.write_text(s,encoding='utf-8')
p=out/'technology_service_analysis.py';s=p.read_text(encoding='utf-8');git=subprocess.check_output(['git','show','HEAD:backend/review_v2/technology_service_analysis.py']).decode('utf-8');a=git.index('def analyze_technical_secret_loss_arrangement(');b=git.index('\n\nEXPENSE_ITEM_PATTERN',a);original=git[a:b];a=s.index('def analyze_technical_secret_loss_arrangement(');b=s.index('\n\nEXPENSE_ITEM_PATTERN',a);s=s[:a]+original.rstrip()+s[b:]
s=s.replace('''    from review_v2.license_terms import LICENSE_TYPE_PATTERN, declared_license_type as is_declared_license_type
    license_type_term = '(' + LICENSE_TYPE_PATTERN + ')'
''','''    license_type_term = (
        r"(独占(?:实施)?许可|排他(?:实施)?许可|普通(?:实施)?许可|"
        r"非独占(?:、[^,，。；;]{0,16})?(?:的)?(?:专利)?(?:实施)?许可)"
    )
''')
s=s.replace('        if not is_declared_license_type(segment):\n            continue\n','').replace('            if not is_declared_license_type(segment):\n                continue\n','');p.write_text(s,encoding='utf-8')
p=out/'proposition_scope.py';s=p.read_text(encoding='utf-8');s=s[:s.index('\n\ndef arrangement_matches')];s=s.replace('|即使','');a=s.index('_IMPLICIT_CONDITION =');b=s.index('\n\ndef scoped_propositions',a);s=s[:a]+s[b:];s=s.replace("            condition_context = ''\n",'').replace("    condition_context = ''\n",'')
s=s.replace('_condition(quote)','_CONDITION.search(quote)').replace('_condition(text[scope_start:])','_CONDITION.search(text[scope_start:])');s=s.replace('if condition or condition_context','if condition');s=s.replace("condition=condition[0].strip() if condition else condition_context,\n                   condition_context=condition_context,", "condition=condition[0].strip() if condition else '',")
a=s.index("        if condition and quote.rstrip().endswith");b=s.index("            gap_context = ''",a)+len("            gap_context = ''");s=s[:a]+"        elif quote.endswith(('。', '！', '？')):\n            gap_context = ''"+s[b:];p.write_text(s.rstrip()+'\n',encoding='utf-8')
p=out/'technology_adverse_evidence.py';s=p.read_text(encoding='utf-8').replace("(source['inherited_missing'] or source['condition_context'])", "source['inherited_missing']");p.write_text(s.rstrip()+'\n',encoding='utf-8')
p=out/'element_resolution.py';s=p.read_text(encoding='utf-8');s=s[:s.index('\n\ndef requirement_states')];p.write_text(s+'\n',encoding='utf-8')
p=out/'license_control_facts.py';s=p.read_text(encoding='utf-8');s=s.replace('from review_v2.license_terms import declared_license_type\n','').replace("('license_type', '许可类型', [dict(clause_id=c.clause_id, quote=q, location=c.location)\n                 for c, q, t in current if declared_license_type(t)])", "('license_type', '许可类型', grant(r'(?:普通|非独占|独占|排他)(?:实施)?许可'))");p.write_text(s,encoding='utf-8')
p=out/'technology_fact_ontology.py';s=p.read_text(encoding='utf-8').replace('from review_v2.license_terms import LICENSE_TYPE_PATTERN, declared_license_type\n','').replace("'type': LICENSE_TYPE_PATTERN", "'type': r'(?:普通|非独占|排他|独占)(?:实施)?许可'").replace("            if key == 'type' and not declared_license_type(quote):\n                continue\n",'');p.write_text(s,encoding='utf-8')
p=out/'obligation_detail_elements.py';s=p.read_text(encoding='utf-8').replace('from review_v2.proposition_scope import component_states, scoped_propositions\n','');s=s.replace('''    missing_quotes = [_compact(row['quote']) for row in scoped_propositions('\\n'.join(c.text for c in clauses))
                      if row['polarity'] == 'MISSING']
''','').replace('''        if any(compact in missing or missing in compact for missing in missing_quotes):
            exception_context = False
            exception_header = None
            continue
''','');s=s.replace('(?:以下|下列)信息不属于(?:本合同(?:项下)?)?保密(?:信息|范围)|保密.{0,8}(?:例外|除外)[：:]', '(?:以下|下列)信息不属于保密信息|保密.{0,8}(?:例外|除外)[：:]').replace("r'^(?:已经|接收方|非因|从|根据|依法).{0,60}","r'^(?:已经|接收方|从|根据).{0,60}");a=s.index('residuals=missing, source_fact_key="confidentiality.exceptions",');b=s.index('\n    return elements',a);s=s[:a]+'residuals=missing, source_fact_key="confidentiality.exceptions"))'+s[b:];p.write_text(s,encoding='utf-8')
manifest=json.loads(Path('artifacts/technology_pass_semantics/round20_polarity/manifest.json').read_text())
for row in manifest['sources']:
 p=out/Path(row['path']).name
 if not p.exists():continue
 data=p.read_bytes()
 print(p.name,hashlib.sha256(data).hexdigest()==row['sha256'],hashlib.sha256(data.replace(b'\n',b'\r\n')).hexdigest()==row['sha256'],hashlib.sha256(data).hexdigest())
