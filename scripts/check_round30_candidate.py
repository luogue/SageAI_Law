"""Validate a staged predicate module without mutating the running regression sources."""
import importlib.util,sys,pytest
path='artifacts/technology_pass_semantics/round30_transfer_roles/candidate_code/technology_adverse_evidence.py'
name='review_v2.technology_adverse_evidence'
spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
sys.modules[name]=module;spec.loader.exec_module(module)
raise SystemExit(pytest.main(['backend/tests/test_secret_transfer_roles_projection.py','backend/tests/test_patent_license_theme_recommendation_economics.py::test_all_confirmed_competition_restrictions_have_recommendation_fragments','backend/tests/test_patent_license_theme_recommendation_economics.py::test_compound_advice_is_semantic_not_rule_id_or_fixed_duration','backend/tests/test_patent_license_theme_recommendation_economics.py::test_removing_an_adverse_fact_removes_its_recommendation','backend/tests/test_cooperative_development_latest_regressions.py::test_competition_and_improvement_rules_reuse_direct_atomic_evidence','-q','--junitxml=artifacts/technology_pass_semantics/round30_transfer_roles/candidate_actor.xml']))
