# Eight newly failing assertions: source-level audit

Baseline: full2 batches, 740 passed / 277 failed. Tests and gate thresholds were not changed.

| Test suffix | Before expected → observed failure | Public cause | Resolution |
|---|---|---|---|
| cooperative_classification_uses_core_transaction_evidence | Core proof with prescribed heading words and funding-first ordering → precise operative quotes omit heading text | Old quotation-shape expectation | Not forced to pass. Heading remains in location. Direct R&D clauses remain evidence. Ordering a funding clause first is not required to establish the transaction. |
| claim_allocation_is_not_misreported_as_actual_infringement | No actual infringement: PASS → VERIFY | Negative-search audit was populated after positive-source gate | Prepare full-corpus adverse-predicate audit before verification; verifier independently reproduces the search. |
| scope_pass_lists_the_actual_patent_license_coverage | Six licence scope elements: PASS → stale insufficient-evidence narrative | Late local projection discarded predicate/precise-span mapping | Shared licence atom extractor binds patent name/ID, granted acts, territory, term, type and transfer boundary separately. A signing location does not prove licence territory. |
| classification_pass_has_no_insufficient_narrative | “委托开发合同” → “委托开发” | Canonical type display label lost contract suffix | Normalize the classification display label once, retaining verified transaction inputs. |
| gold_timeline_shared_facts_and_relationship_risks | Scope PASS → PARTIAL | Functional acceptance equivalent not recognized | The actual attachment says “系统应能够完成本确认书列明的主要业务功能”; recognize this conformity predicate, not a generic acceptance heading. |
| registration_effect_is_not_contract_formation | Registration PASS and effect explanation → insufficient-evidence narrative | Clause-wide projection replaced separately extracted submission/cooperation spans | Reuse registration extractor's exact source rows, preserve actor/deadline/cooperation independence and statutory-effect explanation. |
| no_actual_infringement_fact_does_not_create_tc_02_02_finding | Negative infringement finding absent → VERIFY | Same negative-search sequencing issue | Same shared preparation/independent verification repair. |
| structural_pass_is_linked_to_higher_priority_substantive_risk | TC-09-03 PASS despite a required MISSING limb → VERIFY | Old whole-rule PASS contradicts atomic states | Not forced to pass. Actual 第八条 allocates new results to 甲方; it does not establish report internal-use, third-party disclosure and provider reuse boundaries. `service_result_use_boundary` remains MISSING, so whole-rule PASS is unsupported. |

## Two unchanged assertions judged obsolete

1. Cooperative classification test checks that quoted text contains section headings or selected funding/output words and requires different first evidence locations for the two classification rules. Current operative sources include “采用深度学习视觉模型结合工业相机进行图像采集，通过乙方开发算法模型、丙方进行工艺验证、甲方提供生产环境进行联合研发。” Section identity is preserved in location, not fabricated into an exact quote. Failure of this formatting assertion does not show absent transaction evidence.
2. Technical-service structural test demands PASS while the existing modeled atom `service_result_use_boundary` is MISSING. The actual ownership clause says independently formed algorithms, models, software modules, technical solutions, improvements and patent application rights belong to 甲方. Ownership is not evidence of the separately modeled use/disclosure/reuse conditions. No test expectation or required business element was deleted to make this pass.

## Evidence artifacts

- `eight_round3.xml`: six restored / two assertions above still failing.
- `ontology_local_final.xml`: 94 passing local regressions, including 25 new ontology tests.
- `live_round3/report.json`: real authenticated production request, not diagnostic mode.
- Full-suite counts and new/regressed identities: `comparison_round3.json` after all full3 batches complete.

## Completed full-suite comparison

- Baseline: 740 PASS / 277 FAIL / 0 SKIP (1017 identities).
- Current: 771 PASS / 271 FAIL / 0 SKIP (1042 identities).
- Existing tests recovered: 6; new PASS-to-FAIL regressions: 0; removed tests: 0.
- Added ontology tests: 25, all PASS. The two audited obsolete assertions remain failures, not silently excluded.
- Current real document: `test_data/122 测试2.docx`, normal authenticated production file endpoint; `release_quality_gate.status=REPORT_READY`, failures empty, report generated.
- Remaining-failure first-assertion triage: extraction 50; normalization/canonical mapping 102; applicability 27; polarity 28; evidence binding 31; SEARCH_AUDIT conflict 7; report rendering 24; reviewed obsolete expectation 2.
- These remaining buckets are triage, not 271 established causal diagnoses: 208 assertion-signature classifications, 61 requiring causal investigation, 2 source-and-assertion-reviewed obsolete expectations. See `clusters_round3.json` for each assertion and confidence.
