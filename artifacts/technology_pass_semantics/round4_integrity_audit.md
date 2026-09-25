# Element report evidence / partial-state closure

## Confirmed production causes

1. The shared delivery extractor accepted any occurrence of 提交/交付/提供. The noun phrase `甲方提供技术资料产生的纠纷除外` therefore became a false delivery source in the canonical document facts. Both result-use and technical-document consumers inherited it. The repair distinguishes an operative delivery predicate from a document mentioned inside liability/exception language.
2. Final exact-evidence projection appended precise rows to an existing theme pool; unrelated context could survive with no element owner. The new reverse projection reads independently revalidated atom sources and preserves only explicitly owned report rows. Source context remains in diagnostic trace. Absence rows reuse executed, element-specific full-corpus search records.
3. The `invoice_and_account` composite was correctly incomplete as a whole, but its missing residual `收款账户` became the label of the PARTIAL assertion. Transaction composites now retain child states, and the production atomic adapter consumes those children separately. Invoice COVERED no longer changes account MISSING.
4. A successful no-adverse-clause search retained candidate excerpts despite having no positive element (including a non-applicable sentinel element). These candidates are now diagnostic context, not positive report proof. The independently reproduced full-corpus negative search remains required.
5. The first completed full run exposed one new regression: the expected-source adapter read only the original family and omitted later shared actor/object-scoped material-disposition elements. It now merges both existing parsers' sources. The failing production fixture and a new shared-scope unit regression pass without changing expectations.

## Counts and scope

- Before: 6 unrelated rule/source pairs: TC-05-03 one, TC-13-01 one, TC-02-02 four negative-search candidates. Repeated summary/detail displays are not counted again.
- Before: 1 false residual PARTIAL assertion, TC-04-02 account.
- After: 0 unrelated sources in the modeled semantic recheck; 0 false PARTIAL assertions.
- Final real report structural scan: 53 TC rows, 0 report evidence rows without an element link, 0 PARTIAL elements without positive source spans.
- Independent positive semantic audit: 13 selected rules, 40 audited entries (includes negative-check N/A entry), 0 mismatches. This is not a claim that every possible future legal proposition has a complete ontology.
- New public regression cases: 12. Local protected suite including the previously regressed production fixture: 115 PASS / 0 FAIL.
- Existing expectations and gate thresholds were not changed. No legacy fallback was restored.

## Real business entry

Same file: `test_data/122 测试2.docx`; authenticated `POST /review-v2/file` through the UI proxy, normal review mode.

Fresh backend PID 1536; production trace reports runtime CURRENT. `live_round4_final/report.json`: release quality gate REPORT_READY, failures empty, report generated. TC-02-02 has no orphan context evidence and its full-corpus negative verification remains PASS.

## Artifacts

- `round4_scan_before_final.json` / `round4_scan_after_final.json`
- `round4_pass_scan_final.json`
- `round4_local_closure.xml`
- `live_round4_final/report.json` / `report.md`
- First completed full run: full6 = 781 PASS / 272 FAIL, 11 new passing tests, 1 newly failing production fixture (the shared-source adapter defect above).
- Final full7: **783 PASS / 271 FAIL / 0 SKIP**, 1054 tests across 65 files. Compared with full3 (771 PASS / 271 FAIL), 12 tests were added and passed; 0 existing tests newly failed, 0 existing failures recovered, and 0 tests were removed. The intermediate shared-source regression is restored. This is not a claim that the complete technology suite is stable: the 271 pre-existing failures remain.
- Final comparison: `round4_comparison_final.json`; first-failing-assertion triage: `round4_clusters_final.json`. Buckets: extraction 50; normalization/canonical mapping 101; applicability 27; polarity 28; evidence binding 31; SEARCH_AUDIT conflict 8; report rendering 24; previously source-reviewed outdated expectations 2. Buckets are diagnostic triage, not 271 confirmed root-cause diagnoses; existing expectations were not modified.
- Interrupted full4/full5 batches are not complete regression results and are excluded from final totals.
