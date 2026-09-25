# Round17 patent implementation licence

Frozen real input: `round17_license_input/original.docx`, SHA256
`4728a43d0fb3df710ac13f90389bb14466e2286e249706d7ae410d5f7fdd73a2`.

## Reproduction, not inferred from the reported banner

`round17_before/report.json` (normal `/review-v2/file`, technology, 乙方):

- `REVIEW_EVIDENCE_ELEMENT_MISMATCH`, `TC-12-04/infringement_damage_items`:
  actual reference `C0015`; first-sentence evidence `SRC-6fc1f608318244db1af4`
  proves notification, not damages. The existing response fact's precise damages
  span was discarded by the shared-claim audit restoration helper.
- Same gate, `TC-12-04/PRIMARY_EVIDENCE`: same incorrect first-sentence evidence.
- Additional original rejection objects were narrative binding checks of patent
  identity fields in TC-03-04 / TC-13-02. These are not the two above mismatches.

TC-07-03 independently had a semantic error not caught by that initial banner:
`SRC-24efd9d3e2f61795d0af` proves the licensor's breach of exclusivity, not the
licensee's unauthorized sublicence liability.

## Confirmed shared causes and changes

1. Scope ontology did not consume colon-delimited fields in an operative scope
   list. Retain the list context and exact field span, and separate current grants
   from historical grants and restrictions on the licensor.
2. The breach predicate crossed intervening words from a breach of exclusivity
   into the phrase licence scope. Select actual unauthorized/out-of-scope acts;
   compensation remains independent of cessation.
3. Canonical registry evidence was regenerated from a clause ID with topic terms,
   then deduplicated by clause ID. Preserve typed fact spans and span-based IDs.
4. Shared-claim restoration lost the precise source and the direct-element map.
   Restore the selected source with explicit element ownership, not the paragraph.
5. Atomic candidate adaptation supplied supporting spans but not explicit binding
   edges required by strict multi-element aggregation. Emit those edges and merge
   ownership for the same exact source, while retaining independent verification.
6. Adapted atomic families were omitted from the final canonical narrative
   projection. Include the already-adapted state; stance evaluation must not
   overwrite its contract facts or residuals.

Gate/verifier rejection conditions are unchanged. No fixture assertion migration.

## Current normal-interface result

`round17_final/report.json`: REPORT_READY, 0 original / 0 expanded blockers.
Backend PID22324, engine SHA256
`ccd56e7166354f6440b588f12eb9ee037baabe660bec7d02b140561c65ece972`.

- TC-07-01: PASS. Territory `SRC-ef8fe786ebee6ade5aee`; acts
  `SRC-1af4e6b71336810bc47d`, both fourth article.
- TC-07-03: PARTIAL. Cessation/remedy `SRC-55d0e5a450e9c6360ed1`, seventeenth
  article, licensee's actual sublicensing breach. Monetary compensation remains
  MISSING with element-specific audit; the other party's compensation is not reused.
- TC-12-04 audit: direct damages source `SRC-315983a618a62bc3b843`, twelfth article,
  preserving prior-knowledge/concealment condition.

`round17_local5.out`: 17 PASS (8 new + 9 previous protection tests).
Full45 and Full46 were interrupted and are not acceptance results.

## Final3 verification checkpoint (not full-regression acceptance)

Backend PID404 loads engine SHA256
`0d2ed1a6779fdb2c57cc0d84c10d7ff0fa1715c8ee7ac8775a41b4f88ce36b43`.
`round17_final3` and `round17_final3_licensor` both return REPORT_READY, zero
original/expanded blockers. Ten obtainable protection samples also return
REPORT_READY, with unchanged risk-group sets versus their Round16 results:
cooperative, cross_article, patent, consulting, provider, balanced, ancillary,
entrusted, prior_patent, transfer. The unavailable older entrusted source remains
NOT_VERIFIED; it is not counted as an obtained protection sample.

Full47 is running against Full44 (974 PASS / 249 FAIL). Eleven new test cases
are included. A possible new failure in
`test_coverage_evidence_is_bound_to_over_scope_and_material_delivery_clauses`
requires its actual failure trace; zero new regressions is not yet established.

## Confirmed regression and final4 checkpoint

Full47 completed: 984 PASS / 250 FAIL; compared with Full44, one newly failing
test, zero recovered historical failures, eleven added cases. The actual
new failure was `KeyError: quote` in the evidence-clause consumer, caused by
an element-specific SEARCH_AUDIT row lacking public display aliases. The
audit projection now supplies `quote == quoted_text` and `location ==
SEARCH_AUDIT`, retaining AUDIT provenance and exact missing-element ownership.
No test expectation or verifier condition was changed.

A minimal check also confirmed that the scope filter wrongly discarded a
five-year licence term when another obligation in the sentence used “不得”.
Negation filtering now checks the component's governing prefix; historical
grants and breach references remain excluded. Four additional cases protect
these boundaries (fifteen new cases in this round altogether).

`round17_local7.out`: 16 PASS, including the original newly failing test.
Backend restarted as PID9828. `round17_final4/report.json`: REPORT_READY, no
blockers. All ten final4 protection reports also return REPORT_READY, with
unchanged risk-group sets. The running engine hash matches the on-disk hash.
Full48 is the final-code full regression and is still pending; do not claim
zero new regressions until its per-ID comparison completes.

## Original exact-binding rejection tuples

Both objects in the reported `2 mismatch(es)` are TC-12-04:

| element_id | original evidence_refs | rejection | correct direct source |
| --- | --- | --- | --- |
| infringement_damage_items | C0015 | No DIRECT proof with matching element/source ownership | SRC-315983a618a62bc3b843 |
| PRIMARY_EVIDENCE | C0015 | Primary evidence supports no covered element | SRC-315983a618a62bc3b843 |

The original clause-level reference resolved to notification excerpt
`SRC-6fc1f608318244db1af4`, not the damages sentence in the same article.
The corrected twelfth-article source preserves the condition that the licensor
knew and deliberately failed to disclose the dispute before signing.

The separate TC-07-03 semantic defect bound
`SRC-24efd9d3e2f61795d0af` (licensor's exclusivity breach) to the recipient's
breach. Recipient cessation is now proved by `SRC-55d0e5a450e9c6360ed1`.
There is no direct recipient monetary-compensation clause in this input;
that component remains MISSING rather than borrowing the licensor's duty.

## Final acceptance

Full48: **989 PASS / 249 FAIL / 0 SKIP**. Per-ID comparison with Full44:
**zero newly failing, zero removed, fifteen added PASS, zero historical
failure recoveries**. All 249 failures are unchanged baseline failures.
See `round17_final_comparison.json` and the two Full48 JUnit XML files.
Additional production-chain protection
`test_scope_liability_survives_file_pipeline`: PASS (`round17_extra_protection.out`).

Final current report: `round17_final4/report.json` / `report.md`.
REPORT_READY, zero original and zero expanded blockers, process 9828.
TC-07-01 PASS; TC-07-03 PARTIAL with exact recipient cessation evidence and
separate compensation absence audit. Ten obtained protection reports remain
REPORT_READY with unchanged risk groups. No Gate/verifier relaxation,
fallback restoration, old-test expectation edits, or test removals.

Modified common modules: `engine.py`, `license_control_facts.py`,
`technology_fact_ontology.py`, `element_evidence_projection.py`.
New regression module: `test_license_element_ownership.py` (15 cases).
