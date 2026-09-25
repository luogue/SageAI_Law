# Round18 licence evidence consistency — pending full acceptance

Baseline: Full48, 989 PASS / 249 FAIL. Input is the preserved Round17 licence
upload (`round17_license_input/original.docx`). The initial production replay
after source edits returned stale-runtime HTTP 503; it is not a fresh report.
The existing Round17 report supplies the before-state. Subsequent fresh normal
uploads produced the actual rejection objects and final reports.

## Confirmed causes and changes

1. `contract_facts.py` did not normalize 授权公告日/授权公告日期 to the existing
   `technology.patent.authorization_date`. Added the field aliases and exact
   original source span; kept the same canonical key. The registry quote
   selector in `engine.py` uses the same labels.
2. The composite encumbrance evaluator used an independent broad clause test,
   then searched all group members when only some were absent. It now reuses
   the existing current-rights disclosure predicate and builds residual targets
   only from absent members. Contract disclosure is still not independent proof.
3. `license_control_facts.py` recognized consent restrictions without checking
   the restricted action/object. Information disclosure/transfer now requires
   the corresponding action and information object, not patent sublicensing.
4. Material elements retained clause IDs and the first sentence of a retrieved
   paragraph. `engine.py` now carries exact element-owned material source spans,
   registers the existing direct fact map, and excludes unowned candidates.
   Claim-defense documents are not project deliverables. Headings are excluded
   in `obligation_detail_elements.py`; receipt proof requires actual signature,
   receipt or confirmation, not a delivery deadline.

No existing test expectations or Gate/verifier conditions changed.

## Verification checkpoints

`round18_final3_local.out`: 26 PASS (11 new cases plus 15 Round17 protection).
Full49/Full50 were interrupted during additional semantic source inspection;
neither is a final regression result. Full51 is running on final3 code.
Final3 backend PID19364. Real uploads and full regression remain pending;
do not declare zero new regressions before per-ID comparison completes.

## Additional source-boundary protection

Full51 was interrupted after detecting the original inline delivery test
failure. Actual assertion: fourth-article delivery evidence had disappeared.
Parser heading metadata can contain inline operative text, so heading equality
alone was too aggressive. A real obligation predicate now preserves that text;
a bare heading still supplies no delivery proof. Receipt evidence was also
restricted to signature/receipt/confirmation, not a delivery deadline.

`round18_protection8.out`: 43 PASS / 10 FAIL. All ten failures match the
existing Full48 failures in the patent subtransaction registry module.
The previously passing inline delivery test is restored. Twelve new tests and
all fifteen Round17 tests pass. No old assertion changed.

Final4 backend PID20588. Full52 and final4 live uploads are the acceptance run.
Full49–51 and earlier final reports must not be used to claim final acceptance.

## Final source propagation fixes

Full52 completed at 999 PASS / 251 FAIL. Its two newly failing tests were:
- `test_patent_identity_and_support_reuse_direct_source_facts`: the identity
  projector joined separately extracted spans in fact order, producing text
  absent from the original. It now binds each original span independently;
  no concatenated or expanded quotation is used.
- `test_material_acceptance_and_payment_rendering_are_grounded`: the new exact
  material adapter omitted parser-owned `clause_number`. The adapter now carries
  that metadata alongside the unchanged precise quote.

Both original tests pass (`round18_two_regressions.out`). No expectations were
changed. Final5 backend PID21024 loads the fixed code. Current licence and ten
available protection uploads are REPORT_READY with zero failures; runtime engine
hash matches disk. Protection risk-group sets are unchanged from Round17.
Full53 is the final-code regression run; its per-ID comparison remains pending.

## Final6 definition-source protection

Full53 was interrupted after its provisional per-ID comparison found
`test_current_application_identity_uses_basic_information_and_definition`.
The failing assertion was the first evidence location: the identity source
ranking consumed the narrowed field quote instead of the original definition
context. Formal asset definitions are now selected before verification and
ranked using their parser-owned clause; verified excerpts are not expanded.
The complete identity suite plus the two original regression cases, twelve new
cases and fifteen Round17 cases finished at 56 PASS / 6 FAIL. The six failures
are all present in Full48. File: `round18_final6_local.xml`.

Final6 backend PID12520. Full54 is the final-code acceptance run. Full53 and all
earlier interrupted runs are not final acceptance evidence.

## Completed final-code acceptance

Full54: **1001 PASS / 249 FAIL**, compared with Full48 **989 PASS / 249 FAIL**.
Twelve added tests all pass; zero newly failing, zero recovered historical tests,
zero removed/skipped tests and zero test migrations. All original test statuses
are unchanged. See `round18_final_comparison.json`.

Current report: `round18_final6/report.json` and `report.md`.
Gate REPORT_READY, empty failures/blocking_rules (zero original and expanded
blockers). Authorization date is COVERED in TC-03-04 and TC-13-02; existing
licence disclosure is positively bound and excluded from residual search.
TC-11-01 and TC-13-01 retain PARTIAL and only element-owned relevant evidence.
TC-07-01 PASS, TC-07-03 PARTIAL and TC-12-04 NOT_APPLICABLE are preserved.

All ten available protection uploads are REPORT_READY with unchanged risk-group
sets and matching runtime engine SHA256:
`d82966b98f5fc8d3b3dbaac44661522259d87215cc1247d62c02fbb37b78d9a7`.
The previously unavailable original entrusted input (SHA256 e5463c90...) remains
NOT_VERIFIED, not replaced with an invented sample. The available later entrusted
input was verified separately. Full evidence: `round18_final_acceptance.json`.

This closes the four requested evidence-consistency defects, not the 249
pre-existing technical-contract test failures.
