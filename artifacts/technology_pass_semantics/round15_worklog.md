# Round15 patent-right transfer repair

## Verified implementation

- Frozen input: `round15_patent_input/original.docx`, SHA256 `86a5970531a486d6610b6fd5ebe9875d6d86073ccc57462c8ee38781d5594b8e`.
- Current backend PID 8196, engine SHA256 `388fcfb5c709a7fd9f41a3e08115883929b51c3883cac450848bcfeb863251a3`.
- Actual uploaded report: `round15_final5_current/report.json`; REPORT_READY, zero original/expanded blockers.
- Classification: TECHNOLOGY_TRANSFER / PATENT_RIGHT_TRANSFER.
- TC-06-01 PARTIAL (disclosed continuing licence); TC-06-03 PASS; TC-06-04 PASS.
- TC-12-01 PARTIAL (title-defect remedy does not settle all implementation infringement liability); TC-12-02 PARTIAL; TC-12-03 NOT_APPLICABLE.

## Confirmed causes

1. The transfer classifier treated confidential supporting documents as a secret transaction, and did not recognize structured granted-patent attributes strongly enough.
2. A secret-transfer branch in engine.py constructed fixed adverse claims, including a 20% cap and recipient litigation expenses, whenever any third-party-claim trigger existed. This was deterministic template fabrication, not evidence of cross-request cache leakage.
3. Patent claim projection produced rule-local event sources, lost declared A/B party roles during precise-quote verification, and joined several quotes as one excerpt.
4. The shared inbound-claim extractor missed warnings/complaints/litigation and could confuse the compensation recipient with the responsible subject. Source-bound adaptation now preserves roles and actual allocations.
5. Current disclosure and contractual authority statements were gated by narrow phrasings rather than their separately verified representations.

## Modified implementation modules

- backend/review_v2/technology_asset_identity.py
- backend/review_v2/technology_service_analysis.py
- backend/review_v2/technology_patent_transfer_analysis.py
- backend/review_v2/engine.py
- backend/tests/test_registered_patent_asset_routing.py (15 new tests)
- backend/tests/test_technology_exact_truth_pipeline.py (one fixture migration affecting two unchanged test assertions; see round15_fixture_migration.md)

Verifier/release conditions were not relaxed. No legacy fallback restored. True gaps remain.

## Protection

Entrusted development plus seven existing samples (cooperative, cross-article confidentiality, patent licensing, consulting, provider cap, balanced confidentiality, ancillary services) all passed actual upload on final code. The seven manifest sample risk-group sets are unchanged from Round14 (11, 13, 13, 4, 6, 15, 19). See `round15_final5_live_manifest.json` and `round15_final5_entrusted/report.json`. The separate original guard whose file is unavailable remains NOT_VERIFIED; it is not represented by a substitute.

## Final validation

Full41 completed at 954 PASS / 259 FAIL and identified ten implementation regressions plus one fixture-drift regression. The implementation issues were fixed in claim-event field adaptation, atom-scoped negation, and adverse warranty projection protection. Local affected regressions were rerun. Full36 through full40 were interrupted before implementation freeze and are not final results.

Full42 completed on the final source snapshot:

- Batch0: 660 PASS / 142 FAIL.
- Batch1: 305 PASS / 107 FAIL.
- Total: 965 PASS / 249 FAIL / 0 SKIP.
- Versus full35 948/251: two historical failures recovered, fifteen new tests passed, zero newly failing, zero removed tests.
- The two recovered IDs are `test_current_existing_and_retained_license_reduce_full_scope_coverage` and `test_scope_narrative_does_not_invent_missing_territory_term_and_powers`, both in `test_patent_transfer_acquisition_and_remedies`.
- The fixture migration is tracked separately and is not counted as an implementation recovery.
- Details: `round15_final_comparison.json`, `full42_batch0.xml`, `full42_batch1.xml`.

After the protection uploads, the current input was uploaded again through the normal interface: `round15_final_replay_current/report.json` and `report.md`. It remains PATENT_RIGHT_TRANSFER / REPORT_READY with zero original and expanded blockers. All 55 item states and seven risk-group identities match the earlier final5 current report. Backend PID 8196 reported the final engine hash, and the file hash was rechecked after the suite completed. The 249 remaining historical failures are not claimed to be resolved.
