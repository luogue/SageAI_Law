# Original patent release closure — decision and evidence audit

## Fixed input and baseline

- Input: `round6_patent/original.docx`, original upload prior `sale`.
- SHA256: `41b4a8780a82ea598e2bb200d1407338338cd8d2ffa626b22bf2aa98590c6f9a`.
- Original refusal record: `round6_final_patent_blockers.json`, 10 raw objects / 11 expanded tuples. These are not eleven root causes.
- IDs not published by the original gate remain null in the closure export. Existing traces record observed mutations; a trace observation is not substituted for a missing fact ID.
- Final acceptance uses `routers.review_v2.review_v2_file` over the normal `/review-v2/file` upload endpoint, not the diagnostic route. `use_llm=false` is retained from the original regression request.

## Confirmed roots and decision boundary

1. `_apply_final_technology_fact_projection` and `_apply_technology_finding_consistency_gate` ran after independent source verification. They could restore an earlier affirmative verdict. Both now run after generic candidate normalization but before exact verification; the final fact projection is called once. Exact verification consumes the completed report binding, not a pre-binding snapshot. The first attempted order put generic normalization after final projection and caused new regressions; that ordering was rejected after full15 and corrected.
2. `_apply_checkpoint_metadata` replaced a negative-search audit with data inferred from its display status. Canonical full-corpus audits now retain their own predicate, corpus scope and verification result. The negative verifier independently repeats the same registered predicate; missing or altered audits fail verification.
3. A generic coverage adapter discarded typed proof elements and replaced them with `core_contract_arrangement`. The adapter now preserves the modeled element IDs and exact clause/span ownership; absent source support becomes uncertainty, not remembered coverage.
4. Exact-source rejection changed the review status but left its child positive/partial status. Rejection now records an element transition and invalidates only the rejected positive claims. A remembered specialized snapshot cannot restore them. The integrity gate accepts revocation only when a matching failed verifier result and transition exist, not merely a manual-review flag.
5. Final validation previously overlaid selected rule IDs onto an earlier gate snapshot. It now runs the same strict evidence validator on the complete final snapshot, catching stale passes as well as stale failures.

The distinct state owners remain the existing schema: `applicability`, `coverage_elements`, `verified_pass_source_gate`, and findings/evaluations. No alternate truth schema or legacy evidence fallback was introduced.

## Baseline refusal disposition

| Expanded tuples | Root / first confirmed producer | Resolution |
| --- | --- | --- |
| 1: TC-11-01 | Exact-source metadata was reconstructed from a display/theme row; synthetic typed sources lacked actual fact ownership | Preserve existing clause/span mapping; do not invent typed fact bindings in the narrative binder |
| 2, 7: TC-11-04 | Confidentiality undertaking was projected as liability coverage by the confidentiality semantic producer | Undertaking stays in applicability evidence; only actual liability/remedy facts cover child requirements |
| 3–6, 9: TC-10-04 | Incomplete/overwritten negative audit followed by final PASS restoration | Registered adverse predicate, reproducible full-corpus audit, verification before final presentation |
| 8: TC-03-04 | Composite patent identity mixed found fields and a parent absence query | Independently project and search existing canonical name/number/owner/date fields; retain per-field evidence |
| 10: TC-12-01 | Aggregate actor regex consumed the claim recipient as the later liability actor | Consume existing actor-bound response facts; licensor direction is not replaced with licensee direction |
| 11: TC-13-01 | A material-delivery paragraph was discarded because its later sentence mentioned improvements | Preserve the direct delivery proposition; delivery does not establish an actual attachment |

## Same-root protection repairs

- Canonical penalty re-keying now updates `direct_element_fact_keys` and `direct_fact_bindings` together, only from source proofs verified against the same penalty fact.
- A generic confidentiality topic claim is replaced by the existing shared scope and in-contract obligation predicates. It cannot use source-code ownership as confidentiality proof.
- Entrusted guard: `test_data/122 测试2.docx`, same source and normal upload; final artifact prefix `round7c_final_guard_live`.
- Industrial sample remains a technical-service transaction and remains BLOCKED for its outstanding element bindings. It is not used to expand this patch into a separate rule-repair campaign.

## Validation records

- New guards: `backend/tests/test_technology_verified_decision_boundary.py` (22 cases, all passing).
- `full13` was interrupted after the real guard request exposed binding failures; it is not a complete run and must not be counted.
- `full14` was interrupted when final element inspection found two remaining false missing facts; it is not counted as a completed run.
- `full15` completed: 801 PASS / 301 FAIL, with 7 historical recoveries, 46 newly failing original tests and 20 added tests. It is an intermediate failed non-regression check, not the final acceptance run.
- `full16` is the final frozen run, compared by original test identity to `full12`; it includes 22 new guards. Do not count the new guards as recovered historical failures.
- Final normal-upload reports: `round7e_final_patent_live`, `round7e_final_industrial_live`, `round7e_final_guard_live` (worker 19444).
- Two industrial timeline assertions remain disputed and unchanged: contract validity ending before later delivery/acceptance is not itself an independently agreed performance cutoff. No test migration was made and these are not counted as recovered defects.

## Final element-level checks beyond a green gate

- A contractual declaration identifying the patent owner now enters the same `technology.patent.owner` key as a filled identity field. Its exact declaration span is retained. This does not establish that a certificate/register was uploaded or externally verified.
- Material delivery now uses the existing operative delivery-source predicate and the same document taxonomy as material scope/types. A warranty/indemnity mentioning supplied documents is not a delivery promise. The original delivery sentence now covers `delivery_obligation`; an attachment schedule and actual supplied documents remain separate requirements.
- Replaying the final technology candidate projection on the identical fact/evidence snapshot produced zero differences in coverage, applicability, elements, evidence ownership and risk fields (`round7_projection_replay.json`).
- The 10 original raw refusals / 11 expanded tuples are retained in `round7e_release_closure.json`, including their original null IDs and observed before/after stage traces. The final patent report has zero release refusals. Industrial still has outstanding refusals (`round7e_industrial_blockers.json`); entrusted remains zero.
- The liability-direction regression also exposed a cap-only sentence being consumed as an affirmative liability allocation. A cap does not independently establish an undertaking; the existing operative handling facts retain their actor. Likewise, a general compensation allocation does not establish concrete damage items in the shared coordination audit.

## Final result — non-regression acceptance NOT satisfied

- Full16: **824 PASS / 280 FAIL / 0 SKIP**, 1,104 tests. All 1,082 original identities were retained.
- On original identities alone: **802 PASS / 280 FAIL** versus baseline 820 / 262.
- Historical failures recovered: **8**. Original passing tests now failing: **26**. New protection cases: **22 PASS**, not counted as recoveries. Test migrations: **0**.
- Exact IDs and failure messages: `round7_comparison_final.json`. Do not relabel these 26 failures as obsolete tests; no such determination or migration has been completed.
- Remaining new failures include consulting/application-transfer source-predicate or exact-binding contracts, source-location identity projection, recommendation projection, and negative-review publication consistency. These remain unresolved. The original patent's successful publication is not proof that these branches are regression-free.
- Original patent real upload: **REPORT_READY**, prior `sale`, resolved `technology / TECHNOLOGY_LICENSE / PATENT_LICENSE`, zero release refusals.
- Entrusted real guard: **REPORT_READY**, zero refusals, no review-status changes against round6.
- Industrial real guard: correct technology/service routing, **BLOCKED**, **7 raw / 18 expanded** refusals (baseline 41 / 50). Two timeline assertion disputes remain unchanged and are not recoveries.
- Therefore this round closes the original patent release refusal set, but it does **not** pass the full technology non-regression acceptance. No Gate was disabled or forced ready.
